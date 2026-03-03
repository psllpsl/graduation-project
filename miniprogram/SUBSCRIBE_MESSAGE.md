# 微信小程序订阅消息配置指南

## 一、申请订阅消息模板

### 1.1 登录微信公众平台

1. 访问 https://mp.weixin.qq.com/
2. 使用小程序管理员账号登录
3. 进入「功能」→「订阅消息」

### 1.2 添加模板

在订阅消息页面，点击「添加模板」，搜索并添加以下模板：

#### 推荐模板（医疗/复诊类）

| 模板名称 | 模板 ID | 用途 |
|----------|--------|------|
| 就诊提醒 | 待申请 | 复诊前提醒患者 |
| 预约成功通知 | 待申请 | 预约成功后通知 |
| 服务进度通知 | 待申请 | 通用服务通知 |

**注意**：模板 ID 需要在微信公众平台申请后获取，每个小程序的模板 ID 可能不同。

### 1.3 配置模板关键词

以"就诊提醒"模板为例，配置关键词：

```
{{thing1.DATA}} - 就诊类型
{{time2.DATA}} - 就诊时间
{{thing3.DATA}} - 就诊地点
{{thing4.DATA}} - 温馨提示
```

---

## 二、前端请求订阅授权

### 2.1 在适当时机请求授权

在用户点击"订阅消息提醒"时触发：

```javascript
// pages/profile/profile.js
onSubscribeMessage() {
  wx.requestSubscribeMessage({
    tmplIds: [
      'YOUR_TEMPLATE_ID_1',  // 替换为实际模板 ID
      'YOUR_TEMPLATE_ID_2'   // 如有多个模板
    ],
    success: (res) => {
      console.log('订阅结果:', res)
      
      // 处理订阅结果
      if (res[Object.keys(res)[0]] === 'accept') {
        wx.showToast({
          title: '订阅成功',
          icon: 'success'
        })
        
        // 保存订阅状态到本地
        wx.setStorageSync('subscribed', true)
        
        // 可选：将订阅状态同步到后端
        this.saveSubscriptionToServer()
      } else {
        wx.showToast({
          title: '您已拒绝订阅',
          icon: 'none'
        })
      }
    },
    fail: (err) => {
      console.error('订阅失败:', err)
      wx.showToast({
        title: '订阅失败，请重试',
        icon: 'none'
      })
    }
  })
}
```

### 2.2 订阅说明

- 一次性订阅：用户每次点击都需要重新授权
- 长期订阅：仅对特定场景开放（如政务民生、医疗等）
- 建议：使用一次性订阅即可

---

## 三、后端发送订阅消息

### 3.1 获取 Access Token

```python
# Python 示例
import requests

def get_access_token():
    appid = 'YOUR_APPID'
    secret = 'YOUR_APP_SECRET'
    
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
    response = requests.get(url)
    data = response.json()
    
    return data.get('access_token')
```

### 3.2 发送订阅消息

```python
# Python 示例
def send_subscribe_message(openid, template_id, data):
    access_token = get_access_token()
    
    url = f'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={access_token}'
    
    payload = {
        "touser": openid,
        "template_id": template_id,
        "page": "pages/index/index",  # 点击消息跳转页面
        "miniprogram_state": "formal",  # formal-正式版，trial-体验版，develop-开发版
        "lang": "zh_CN",
        "data": data
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# 使用示例
send_subscribe_message(
    openid='USER_OPENID',
    template_id='YOUR_TEMPLATE_ID',
    data={
        'thing1': {'value': '复诊提醒'},
        'time2': {'value': '2026 年 3 月 15 日 09:00'},
        'thing3': {'value': 'XX 口腔诊所'},
        'thing4': {'value': '请按时复诊，如有不适请及时就医'}
    }
)
```

---

## 四、在后端集成发送功能

### 4.1 在 FastAPI 后端添加发送接口

```python
# backend/app/api/notification.py
from fastapi import APIRouter, Depends, HTTPException
from ..services.wechat_service import WechatService

router = APIRouter()

@router.post("/subscribe")
async def subscribe_reminder(
    patient_id: int,
    current_user: dict = Depends(get_current_user)
):
    """患者订阅复诊提醒"""
    # 记录订阅状态到数据库
    pass

@router.post("/send-reminder")
async def send_appointment_reminder(
    appointment_id: int,
    current_user: dict = Depends(get_current_user)
):
    """发送复诊提醒消息"""
    # 调用微信 API 发送消息
    pass
```

### 4.2 创建微信服务类

```python
# backend/app/services/wechat_service.py
import requests
import time

class WechatService:
    def __init__(self):
        self.appid = "YOUR_APPID"
        self.secret = "YOUR_APP_SECRET"
        self.access_token = None
        self.token_expires_at = 0
    
    def get_access_token(self):
        """获取微信 access_token"""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        self.access_token = data.get("access_token")
        self.token_expires_at = time.time() + 7000  # 7200 秒，预留 200 秒余量
        
        return self.access_token
    
    def send_subscribe_message(self, openid, template_id, page, data):
        """发送订阅消息"""
        access_token = self.get_access_token()
        
        url = f"https://api.weixin.qq.com/cgi-bin/message/subscribe/send"
        params = {"access_token": access_token}
        
        payload = {
            "touser": openid,
            "template_id": template_id,
            "page": page,
            "miniprogram_state": "formal",
            "lang": "zh_CN",
            "data": data
        }
        
        response = requests.post(url, params=params, json=payload)
        return response.json()
```

---

## 五、定时任务发送提醒

### 5.1 配置 APScheduler 定时任务

```python
# backend/app/services/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()

def check_and_send_reminders():
    """检查并发送即将到期的复诊提醒"""
    # 查询明天需要复诊的患者
    # 调用 WechatService 发送消息
    pass

# 每天上午 9 点执行
scheduler.add_job(
    check_and_send_reminders,
    'cron',
    hour=9,
    minute=0
)

scheduler.start()
```

---

## 六、常见问题

### Q1: 订阅消息发不出去？

**A**: 检查以下几点：
1. 模板 ID 是否正确
2. Access Token 是否有效
3. 用户是否已授权订阅
4. 消息发送频率是否超限

### Q2: 用户拒绝订阅后还能再请求吗？

**A**: 可以。用户拒绝后，下次仍可再次请求授权。但建议不要频繁请求，以免引起用户反感。

### Q3: 订阅消息有数量限制吗？

**A**: 有。每个用户每天最多接收 3 条相同模板的订阅消息。

### Q4: 如何查看订阅消息发送记录？

**A**: 在微信公众平台 → 功能 → 订阅消息 → 发送记录 中查看。

---

## 七、测试步骤

1. **开发环境测试**：
   - 在微信开发者工具中测试订阅授权
   - 使用真机调试功能测试消息接收

2. **体验版测试**：
   - 上传代码到微信后台
   - 设置为体验版
   - 添加体验成员
   - 在真机上测试完整流程

3. **正式版发布**：
   - 提交审核
   - 审核通过后发布
   - 监控发送记录和用户反馈

---

## 八、参考资料

- [微信小程序订阅消息官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/subscribe-message.html)
- [微信开放社区](https://developers.weixin.qq.com/community/)
- [微信公众平台](https://mp.weixin.qq.com/)
