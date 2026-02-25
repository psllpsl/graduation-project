from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseResponse
from ..models.knowledge_base import KnowledgeBase
from ..dependencies import get_current_user, get_current_admin_user
from ..models.user import User

router = APIRouter()


@router.get("/", response_model=List[KnowledgeBaseResponse], summary="获取知识库列表")
async def get_knowledge_list(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    category: Optional[str] = Query(None, description="分类筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取知识库列表（支持分页和分类筛选）
    """
    query = db.query(KnowledgeBase).filter(KnowledgeBase.is_active == 1)

    if category:
        query = query.filter(KnowledgeBase.category == category)

    knowledge_list = query.offset(skip).limit(limit).all()
    return knowledge_list


@router.get("/{knowledge_id}", response_model=KnowledgeBaseResponse, summary="获取知识详情")
async def get_knowledge(
    knowledge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据 ID 获取知识条目详细信息
    """
    knowledge = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识条目不存在"
        )
    return knowledge


@router.post("/", response_model=KnowledgeBaseResponse, status_code=status.HTTP_201_CREATED, summary="创建知识条目")
async def create_knowledge(
    knowledge_data: KnowledgeBaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # 需要管理员权限
):
    """
    创建知识条目（需要管理员权限）

    - **category**: 知识分类
    - **title**: 知识标题
    - **content**: 知识内容
    - **keywords**: 关键词
    - **source**: 来源
    - **is_active**: 是否启用
    """
    knowledge = KnowledgeBase(**knowledge_data.model_dump())
    db.add(knowledge)
    db.commit()
    db.refresh(knowledge)
    return knowledge


@router.put("/{knowledge_id}", response_model=KnowledgeBaseResponse, summary="更新知识条目")
async def update_knowledge(
    knowledge_id: int,
    knowledge_data: KnowledgeBaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    更新知识条目（需要管理员权限）
    """
    knowledge = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识条目不存在"
        )

    # 更新字段
    update_data = knowledge_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(knowledge, key, value)

    db.commit()
    db.refresh(knowledge)
    return knowledge


@router.delete("/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除知识条目")
async def delete_knowledge(
    knowledge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    删除知识条目（需要管理员权限）
    """
    knowledge = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识条目不存在"
        )

    db.delete(knowledge)
    db.commit()
    return None


@router.get("/search/query", response_model=List[KnowledgeBaseResponse], summary="搜索知识")
async def search_knowledge(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=50, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    搜索知识库

    - **q**: 搜索关键词
    """
    knowledge_list = db.query(KnowledgeBase).filter(
        KnowledgeBase.is_active == 1,
        KnowledgeBase.content.like(f"%{q}%")
    ).limit(limit).all()
    return knowledge_list


@router.get("/categories", summary="获取知识分类列表")
async def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取所有知识分类
    """
    categories = db.query(KnowledgeBase.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]
