from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
from ..database import get_db
from ..schemas.dialogue import DialogueCreate, DialogueResponse
from ..models.dialogue import Dialogue
from ..dependencies import get_current_user
from ..models.user import User
from ..services.ai_service import get_ai_service
from ..utils.redis_cache import cache
from ..config import settings

router = APIRouter()


@router.get("/", response_model=List[DialogueResponse], summary="获取对话记录列表")
async def get_dialogues(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    patient_id: Optional[int] = Query(None, description="患者 ID 筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取对话记录列表（支持分页和患者筛选）
    """
    query = db.query(Dialogue)

    if patient_id:
        query = query.filter(Dialogue.patient_id == patient_id)

    dialogues = query.order_by(Dialogue.created_at.desc()).offset(skip).limit(limit).all()
    return dialogues


@router.get("/{dialogue_id}", response_model=DialogueResponse, summary="获取对话记录详情")
async def get_dialogue(
    dialogue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据 ID 获取对话记录详细信息
    """
    dialogue = db.query(Dialogue).filter(Dialogue.id == dialogue_id).first()
    if not dialogue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话记录不存在"
        )
    return dialogue


@router.post("/", response_model=DialogueResponse, status_code=status.HTTP_201_CREATED, summary="创建对话记录")
async def create_dialogue(
    dialogue_data: DialogueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新的对话记录（调用 AI 生成回复）

    - **patient_id**: 患者 ID
    - **session_id**: 会话 ID
    - **user_message**: 用户消息
    - **message_type**: 消息类型
    """
    # 获取会话历史（从 Redis 缓存）
    cache_key = f"dialogue_session:{dialogue_data.session_id}"
    session_history = cache.lrange(cache_key, 0, 9)  # 获取最近 10 条对话

    # 格式化上下文
    context = ""
    if session_history:
        context_parts = []
        for msg in session_history:
            if isinstance(msg, dict):
                context_parts.append(f"用户：{msg.get('user_message', '')}\nAI: {msg.get('ai_response', '')}")
        context = "\n".join(context_parts)

    # 检索相关知识
    ai_service = get_ai_service()
    knowledge = ai_service.search_knowledge(db, dialogue_data.user_message)

    # 生成 AI 回复
    ai_response = ai_service.generate_response(
        user_message=dialogue_data.user_message,
        context=context,
        knowledge=knowledge,
        session_id=dialogue_data.session_id
    )

    # 创建对话记录
    dialogue = Dialogue(
        patient_id=dialogue_data.patient_id,
        session_id=dialogue_data.session_id,
        user_message=dialogue_data.user_message,
        ai_response=ai_response,
        message_type=dialogue_data.message_type
    )

    db.add(dialogue)
    db.commit()
    db.refresh(dialogue)

    # 更新会话历史到 Redis
    cache.lpush(cache_key, {
        "user_message": dialogue_data.user_message,
        "ai_response": ai_response
    })
    cache.ltrim(cache_key, 0, 19)  # 保留最近 20 条
    cache.expire(cache_key, settings.REDIS_SESSION_EXPIRE)

    return dialogue


@router.get("/session/{session_id}", response_model=List[DialogueResponse], summary="获取会话对话历史")
async def get_dialogues_by_session(
    session_id: str,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取指定会话的所有对话记录
    """
    dialogues = db.query(Dialogue).filter(
        Dialogue.session_id == session_id
    ).order_by(Dialogue.created_at).offset(skip).limit(limit).all()
    return dialogues


@router.post("/{dialogue_id}/handover", response_model=DialogueResponse, summary="标记为人工接管")
async def mark_handover(
    dialogue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    将对话标记为需要人工接管

    当 AI 无法妥善处理时，医护人员可以介入处理
    """
    dialogue = db.query(Dialogue).filter(Dialogue.id == dialogue_id).first()
    if not dialogue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话记录不存在"
        )

    dialogue.is_handover = 1
    db.commit()
    db.refresh(dialogue)
    return dialogue


@router.get("/handover/pending", response_model=List[DialogueResponse], summary="获取待人工接管的对话")
async def get_pending_handover_dialogues(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取所有待人工接管的对话记录
    """
    dialogues = db.query(Dialogue).filter(
        Dialogue.is_handover == 1
    ).order_by(Dialogue.created_at.desc()).offset(skip).limit(limit).all()
    return dialogues
