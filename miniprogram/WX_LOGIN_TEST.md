# 微信小程序登录测试说明

## 问题说明

微信登录需要真实的 AppID 和 Secret，在开发阶段如果没有这些配置，登录会失败。

## 解决方案

### 方案一：使用测试账号（推荐）

1. 访问微信测试账号平台：https://developers.weixin.qq.com/miniprogram/dev/devtools/sandbox.html
2. 申请测试账号
3. 获取测试 AppID 和 Secret
4. 填入后端代码

### 方案二：修改后端代码使用模拟登录

修改 `backend/app/api/auth.py` 中的 wx_login 接口：

```python
@router.post("/wx-login", response_model=WxLoginResponse, summary="微信登录")
async def wx_login(
    request: WxLoginRequest,
    db: Session = Depends(get_db)
):
    """
    微信小程序登录接口（开发测试版）
    """
    # 开发模式：使用模拟的 openid
    import uuid
    
    # 使用固定的测试 openid（方便调试）
    openid = "test_openid_" + request.code[-6:] if request.code else "test_openid_123456"
    
    # 查询或创建患者
    patient = db.query(Patient).filter(Patient.openid == openid).first()
    
    if not patient:
        patient = Patient(
            openid=openid,
            name=f"测试用户_{openid[-6:]}",
            gender=None,
            age=None,
            phone=None,
            medical_history=None,
            allergy_history=None
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
    
    # 生成 JWT Token
    from ..utils.jwt import create_access_token
    from ..config import settings
    
    token_data = {
        "sub": f"patient:{patient.id}",
        "openid": openid,
        "role": "patient"
    }
    
    expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=token_data, expires_delta=expire)
    
    return WxLoginResponse(
        access_token=access_token,
        token_type="bearer",
        openid=openid,
        user={
            "id": patient.id,
            "openid": openid,
            "name": patient.name,
            "phone": patient.phone,
            "gender": patient.gender,
            "age": patient.age
        }
    )
```

### 方案三：使用真实微信配置

1. 注册微信小程序账号
2. 获取 AppID 和 Secret
3. 填入后端代码中的 `WX_APPID` 和 `WX_SECRET`

---

## 快速测试步骤

1. 重启后端服务
2. 在小程序中点击登录
3. 系统会自动创建测试用户并登录

---

**更新日期**：2026-03-03
