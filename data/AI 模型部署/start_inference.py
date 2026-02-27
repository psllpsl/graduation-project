# Qwen2.5 推理服务启动脚本（Transformers 版本）
# 使用方法：python start_inference.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional, List

# ========== 配置 ==========
MODEL_PATH = "./models/dental_qwen_merged"  # 模型路径
HOST = "0.0.0.0"
PORT = 8080
MAX_TOKENS = 512
TEMPERATURE = 0.7

# ========== 加载模型 ==========
print("=" * 60)
print("🚀 正在加载牙科修复 AI 模型...")
print("=" * 60)

print(f"模型路径：{MODEL_PATH}")

# 检查 CUDA
if torch.cuda.is_available():
    print(f"✅ CUDA 可用 - GPU: {torch.cuda.get_device_name(0)}")
    device = "cuda"
else:
    print("⚠️  使用 CPU 推理（较慢）")
    device = "cpu"

# 加载 tokenizer
print("加载 Tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    padding_side="left"
)

# 加载模型
print("加载模型权重...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True,
    low_cpu_mem_usage=True
)

model.eval()

print(f"✅ 模型加载完成！")
print(f"   模型类型：{model.config.model_type}")
print(f"   词表大小：{len(tokenizer)}")
print("=" * 60)


# ========== 推理函数 ==========
def generate_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = MAX_TOKENS,
    temperature: float = TEMPERATURE
) -> str:
    """
    生成 AI 回复
    """
    # 构建对话格式
    if system_prompt:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    else:
        messages = [{"role": "user", "content": prompt}]
    
    # 应用 chat template
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    # 生成
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=temperature,
        do_sample=True,
        top_p=0.9,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.eos_token_id
    )
    
    # 解码回复
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 提取 assistant 回复部分
    if "assistant" in response:
        response = response.split("assistant")[-1].strip()
    
    return response


# ========== FastAPI 服务 ==========
app = FastAPI(
    title="牙科修复 AI 推理服务",
    description="基于 Qwen2.5-7B 的牙科修复领域 AI 推理 API",
    version="1.0.0"
)


class GenerateRequest(BaseModel):
    """生成请求"""
    prompt: str
    system_prompt: Optional[str] = None
    max_tokens: Optional[int] = MAX_TOKENS
    temperature: Optional[float] = TEMPERATURE


class GenerateResponse(BaseModel):
    """生成响应"""
    text: str
    model: str = "dental_qwen"


class ChatMessage(BaseModel):
    """聊天消息"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """聊天请求（OpenAI 兼容格式）"""
    messages: List[ChatMessage]
    max_tokens: Optional[int] = MAX_TOKENS
    temperature: Optional[float] = TEMPERATURE


class ChatResponse(BaseModel):
    """聊天响应（OpenAI 兼容格式）"""
    choices: List[dict]
    model: str = "dental_qwen"


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "牙科修复 AI 推理服务已启动",
        "model": "dental_qwen",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "memory_used": f"{torch.cuda.memory_allocated(0) / 1024**3:.2f} GB" if torch.cuda.is_available() else "N/A"
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    简单生成接口
    
    - **prompt**: 用户输入
    - **system_prompt**: 系统提示词（可选）
    - **max_tokens**: 最大生成 token 数
    - **temperature**: 温度参数
    """
    try:
        text = generate_response(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            max_tokens=request.max_tokens or MAX_TOKENS,
            temperature=request.temperature or TEMPERATURE
        )
        return GenerateResponse(text=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    """
    OpenAI 兼容格式的聊天接口
    
    - **messages**: 消息列表 [{"role": "user/system", "content": "..."}]
    - **max_tokens**: 最大生成 token 数
    - **temperature**: 温度参数
    """
    try:
        # 提取系统消息和用户消息
        system_prompt = None
        user_message = None
        
        for msg in request.messages:
            if msg.role == "system":
                system_prompt = msg.content
            elif msg.role == "user":
                user_message = msg.content
        
        if not user_message:
            raise HTTPException(status_code=400, detail="缺少用户消息")
        
        text = generate_response(
            prompt=user_message,
            system_prompt=system_prompt,
            max_tokens=request.max_tokens or MAX_TOKENS,
            temperature=request.temperature or TEMPERATURE
        )
        
        return ChatResponse(
            choices=[{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": text
                },
                "finish_reason": "stop"
            }]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
async def test_inference():
    """测试推理功能"""
    test_questions = [
        "种植牙术后多久能吃饭？",
        "活动义齿刚戴上很不舒服，正常吗？",
        "烤瓷牙能用多久？"
    ]
    
    results = []
    for q in test_questions:
        try:
            answer = generate_response(q)
            results.append({
                "question": q,
                "answer": answer[:100] + "..." if len(answer) > 100 else answer
            })
        except Exception as e:
            results.append({
                "question": q,
                "error": str(e)
            })
    
    return {"test_results": results}


if __name__ == "__main__":
    print("\n✅ 准备启动推理服务...")
    print(f"   访问地址：http://localhost:{PORT}")
    print(f"   API 文档：http://localhost:{PORT}/docs")
    print(f"   健康检查：http://localhost:{PORT}/health")
    print(f"   测试接口：http://localhost:{PORT}/test")
    print("\n按 Ctrl+C 停止服务\n")
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info"
    )
