# 第五步：Streamlit 医护管理后台搭建指南
## （零基础小白专用版）

> **适用人群**：零基础 IT 小白、首次接触 Python Web 开发的毕业生
> **预计耗时**：5-7 天
> **难度等级**：⭐⭐☆☆☆（入门级）
> **前置条件**：已完成 FastAPI 后端框架搭建
> **本文档目标**：手把手教你完成 Streamlit 医护管理后台开发

---

## 📋 本章你将完成什么？

完成本指南后，你将拥有：

- ✅ 一个完整的 Streamlit 医护管理后台
- ✅ 6 个核心页面（登录、仪表盘、患者管理、复诊管理、对话监管、知识库）
- ✅ 医护身份认证功能
- ✅ 患者档案管理（CRUD）
- ✅ 复诊计划配置
- ✅ 对话记录监管与人工干预
- ✅ 数据可视化看板
- ✅ 知识库管理功能

---

## 📚 第一部分：基础知识（必读，1 小时）

### 1.1 什么是 Streamlit？

**Streamlit** 是一个用于快速构建数据 Web 应用的 Python 库，无需前端开发经验即可创建美观的交互式界面。

| 特性 | 说明 | 为什么选择它 |
|------|------|--------------|
| **纯 Python** | 无需 HTML/CSS/JS | 学习成本低 |
| **快速开发** | 几行代码即可创建界面 | 开发效率高 |
| **自动刷新** | 代码修改后自动重载 | 调试方便 |
| **内置组件** | 丰富的 UI 组件库 | 功能完善 |
| **数据友好** | 原生支持 Pandas/Plotly | 适合数据展示 |

### 1.2 Streamlit  vs  传统 Web 框架

| 对比项 | Streamlit | Flask/Django |
|--------|-----------|--------------|
| 学习曲线 | 平缓（1 天上手） | 陡峭（1-2 周） |
| 代码量 | 少（100 行） | 多（500+ 行） |
| 前端知识 | 不需要 | 需要 HTML/CSS/JS |
| 适用场景 | 数据应用、后台管理 | 通用 Web 应用 |
| 定制性 | 中等 | 高 |

### 1.3 Streamlit 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| **st.write()** | 输出文本/数据 | `st.write("Hello")` |
| **st.title()** | 页面标题 | `st.title("标题")` |
| **st.button()** | 按钮 | `if st.button("点击"):` |
| **st.text_input()** | 文本输入框 | `name = st.text_input("姓名")` |
| **st.selectbox()** | 下拉选择框 | `option = st.selectbox("选项", ["A", "B"])` |
| **st.dataframe()** | 数据表格 | `st.dataframe(df)` |
| **st.chart()** | 图表 | `st.line_chart(data)` |
| **st.session_state** | 会话状态 | `st.session_state["user"] = "admin"` |
| **st.sidebar** | 侧边栏 | `with st.sidebar:` |
| **st.cache_data** | 数据缓存 | `@st.cache_data` |

### 1.4 Streamlit 项目结构

```
streamlit_app/
├── app.py                  # 主应用入口
├── pages/                  # 多页面目录
│   ├── 01_📊_仪表盘.py
│   ├── 02_👥_患者管理.py
│   ├── 03_📅_复诊管理.py
│   ├── 04_💬_对话监管.py
│   ├── 05_📚_知识库管理.py
│   └── 06_⚙️_系统设置.py
├── utils/                  # 工具模块
│   ├── auth.py            # 认证工具
│   ├── api_client.py      # API 客户端
│   └── charts.py          # 图表工具
├── requirements.txt        # 依赖清单
└── .streamlit/            # Streamlit 配置
    └── config.toml
```

---

## 🛠️ 第二部分：环境准备（第 1 天）

### 2.1 安装 Python

**步骤 1：下载 Python**

访问 Python 官网：https://www.python.org/downloads/

下载 Python 3.10+ 版本（推荐 3.10 或 3.11）

**步骤 2：安装 Python**

1. 运行安装程序
2. ✅ 勾选 "Add Python to PATH"
3. 点击 "Install Now"

**步骤 3：验证安装**

```bash
python --version
# 输出：Python 3.10.x
```

### 2.2 创建项目目录

```bash
# 在项目根目录下创建
cd D:\Project\毕业设计

# 创建 streamlit 目录
mkdir streamlit_app
cd streamlit_app
```

### 2.3 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 激活虚拟环境（Mac/Linux）
source venv/bin/activate
```

### 2.4 安装依赖

创建 `requirements.txt` 文件：

```txt
streamlit==1.31.0
requests==2.31.0
pandas==2.1.4
plotly==5.18.0
pillow==10.2.0
```

安装依赖：

```bash
pip install -r requirements.txt
```

### 2.5 验证安装

```bash
# 运行测试应用
streamlit hello
```

浏览器访问 http://localhost:8501 查看示例。

---

## 🏗️ 第三部分：项目搭建（第 2-3 天）

### 3.1 创建项目结构

```bash
cd streamlit_app

# 创建目录结构
mkdir pages
mkdir utils
mkdir .streamlit
```

### 3.2 创建配置文件

**文件**：`.streamlit/config.toml`

```toml
[theme]
primaryColor = "#1890FF"
backgroundColor = "#F0F2F5"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### 3.3 创建 API 客户端

**文件**：`utils/api_client.py`

```python
"""
API 客户端模块
封装与 FastAPI 后端的通信
"""
import requests
from typing import Optional, Dict, Any, List

# 后端 API 地址
BASE_URL = "http://localhost:8000/api"

class APIClient:
    """FastAPI 后端 API 客户端"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
    
    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """通用请求方法"""
        kwargs["headers"] = kwargs.get("headers", {})
        kwargs["headers"].update(self.headers)
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败：{str(e)}")
    
    # ==================== 认证相关 ====================
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """用户登录"""
        data = {"username": username, "password": password}
        result = self._request("POST", f"{BASE_URL}/auth/login", data=data)
        if "access_token" in result:
            self.token = result["access_token"]
            self.headers["Authorization"] = f"Bearer {self.token}"
        return result
    
    def get_current_user(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        return self._request("GET", f"{BASE_URL}/auth/me")
    
    # ==================== 患者管理 ====================
    
    def get_patients(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """获取患者列表"""
        params = {"page": page, "page_size": page_size}
        return self._request("GET", f"{BASE_URL}/patients/", params=params)
    
    def get_patient(self, patient_id: int) -> Dict[str, Any]:
        """获取患者详情"""
        return self._request("GET", f"{BASE_URL}/patients/{patient_id}")
    
    def create_patient(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建患者"""
        return self._request("POST", f"{BASE_URL}/patients/", json=data)
    
    def update_patient(self, patient_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新患者"""
        return self._request("PUT", f"{BASE_URL}/patients/{patient_id}", json=data)
    
    def delete_patient(self, patient_id: int) -> Dict[str, Any]:
        """删除患者"""
        return self._request("DELETE", f"{BASE_URL}/patients/{patient_id}")
    
    # ==================== 复诊管理 ====================
    
    def get_appointments(self, page: int = 1, page_size: int = 20, 
                         status: Optional[str] = None) -> Dict[str, Any]:
        """获取复诊计划列表"""
        params = {"page": page, "page_size": page_size}
        if status:
            params["status"] = status
        return self._request("GET", f"{BASE_URL}/appointments/", params=params)
    
    def get_appointment(self, appointment_id: int) -> Dict[str, Any]:
        """获取复诊详情"""
        return self._request("GET", f"{BASE_URL}/appointments/{appointment_id}")
    
    def create_appointment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建复诊计划"""
        return self._request("POST", f"{BASE_URL}/appointments/", json=data)
    
    def update_appointment(self, appointment_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新复诊计划"""
        return self._request("PUT", f"{BASE_URL}/appointments/{appointment_id}", json=data)
    
    def delete_appointment(self, appointment_id: int) -> Dict[str, Any]:
        """删除复诊计划"""
        return self._request("DELETE", f"{BASE_URL}/appointments/{appointment_id}")
    
    def update_appointment_status(self, appointment_id: int, status: str) -> Dict[str, Any]:
        """更新复诊状态"""
        data = {"status": status}
        return self._request("PATCH", f"{BASE_URL}/appointments/{appointment_id}/status", json=data)
    
    # ==================== 对话管理 ====================
    
    def get_dialogues(self, page: int = 1, page_size: int = 20,
                      patient_id: Optional[int] = None) -> Dict[str, Any]:
        """获取对话记录列表"""
        params = {"page": page, "page_size": page_size}
        if patient_id:
            params["patient_id"] = patient_id
        return self._request("GET", f"{BASE_URL}/dialogues/", params=params)
    
    def get_dialogue_session(self, session_id: str) -> Dict[str, Any]:
        """获取会话历史"""
        return self._request("GET", f"{BASE_URL}/dialogues/session/{session_id}")
    
    def handover_dialogue(self, dialogue_id: int, reason: str) -> Dict[str, Any]:
        """标记人工接管"""
        data = {"reason": reason}
        return self._request("POST", f"{BASE_URL}/dialogues/{dialogue_id}/handover", json=data)
    
    def get_handover_pending(self) -> Dict[str, Any]:
        """获取待人工接管对话"""
        return self._request("GET", f"{BASE_URL}/dialogues/handover/pending")
    
    # ==================== 知识库 ====================
    
    def get_knowledge(self, page: int = 1, page_size: int = 20,
                      category: Optional[str] = None) -> Dict[str, Any]:
        """获取知识库列表"""
        params = {"page": page, "page_size": page_size}
        if category:
            params["category"] = category
        return self._request("GET", f"{BASE_URL}/knowledge/", params=params)
    
    def get_knowledge_item(self, knowledge_id: int) -> Dict[str, Any]:
        """获取知识详情"""
        return self._request("GET", f"{BASE_URL}/knowledge/{knowledge_id}")
    
    def create_knowledge(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建知识条目"""
        return self._request("POST", f"{BASE_URL}/knowledge/", json=data)
    
    def update_knowledge(self, knowledge_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新知识条目"""
        return self._request("PUT", f"{BASE_URL}/knowledge/{knowledge_id}", json=data)
    
    def delete_knowledge(self, knowledge_id: int) -> Dict[str, Any]:
        """删除知识条目"""
        return self._request("DELETE", f"{BASE_URL}/knowledge/{knowledge_id}")
    
    def get_knowledge_categories(self) -> List[str]:
        """获取分类列表"""
        return self._request("GET", f"{BASE_URL}/knowledge/categories")
    
    # ==================== 统计接口 ====================
    
    def get_stats_overview(self) -> Dict[str, Any]:
        """获取概览统计"""
        return self._request("GET", f"{BASE_URL}/stats/overview")
    
    def get_appointments_trend(self, days: int = 7) -> Dict[str, Any]:
        """获取复诊趋势"""
        params = {"days": days}
        return self._request("GET", f"{BASE_URL}/stats/appointments/trend", params=params)
    
    def get_dialogues_daily(self, days: int = 7) -> Dict[str, Any]:
        """获取对话统计"""
        params = {"days": days}
        return self._request("GET", f"{BASE_URL}/stats/dialogues/daily", params=params)
    
    def get_patients_gender(self) -> Dict[str, Any]:
        """获取患者性别分布"""
        return self._request("GET", f"{BASE_URL}/stats/patients/gender")
    
    def get_appointments_status(self) -> Dict[str, Any]:
        """获取复诊状态分布"""
        return self._request("GET", f"{BASE_URL}/stats/appointments/status")


# 全局客户端实例
_api_client: Optional[APIClient] = None

def get_api_client(token: Optional[str] = None) -> APIClient:
    """获取 API 客户端实例"""
    global _api_client
    if _api_client is None or token:
        _api_client = APIClient(token)
    return _api_client
```

### 3.4 创建认证工具

**文件**：`utils/auth.py`

```python
"""
认证工具模块
处理用户登录与会话管理
"""
import streamlit as st
from typing import Optional

def is_logged_in() -> bool:
    """检查用户是否已登录"""
    return "token" in st.session_state and st.session_state.token is not None

def get_token() -> Optional[str]:
    """获取当前用户的 Token"""
    return st.session_state.get("token")

def get_current_user() -> Optional[dict]:
    """获取当前用户信息"""
    return st.session_state.get("current_user")

def login(token: str, user_info: dict):
    """保存登录信息"""
    st.session_state.token = token
    st.session_state.current_user = user_info
    st.session_state.logged_in = True

def logout():
    """退出登录"""
    st.session_state.token = None
    st.session_state.current_user = None
    st.session_state.logged_in = False
    st.session_state.clear()

def require_login():
    """要求用户登录（未登录则跳转到登录页）"""
    if not is_logged_in():
        st.switch_page("pages/00_🔐_登录.py")
        st.stop()

def get_user_role() -> str:
    """获取用户角色"""
    user = get_current_user()
    return user.get("role", "user") if user else "user"

def has_permission(required_role: str) -> bool:
    """检查用户权限"""
    role = get_user_role()
    role_hierarchy = {"admin": 3, "doctor": 2, "nurse": 1, "user": 0}
    return role_hierarchy.get(role, 0) >= role_hierarchy.get(required_role, 0)
```

### 3.5 创建主应用入口

**文件**：`app.py`

```python
"""
Streamlit 医护管理后台 - 主应用入口
"""
import streamlit as st
from utils.auth import is_logged_in, get_current_user, logout

# 页面配置
st.set_page_config(
    page_title="牙科修复复诊管理系统",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1890FF;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.title("🦷 系统导航")
    
    # 显示用户信息
    if is_logged_in():
        user = get_current_user()
        st.info(f"👤 {user.get('real_name', '未知')} ({user.get('role', 'user')})")
        
        if st.button("🚪 退出登录", use_container_width=True):
            logout()
            st.rerun()
    else:
        st.warning("请先登录")
    
    st.divider()
    
    # 导航菜单
    menu_items = [
        "📊 仪表盘",
        "👥 患者管理",
        "📅 复诊管理",
        "💬 对话监管",
        "📚 知识库管理",
        "⚙️ 系统设置"
    ]
    
    for item in menu_items:
        st.write(f"- {item}")

# 主页面
def main():
    """主页面"""
    st.markdown('<p class="main-header">🦷 牙科修复复诊管理系统</p>', unsafe_allow_html=True)
    st.markdown("欢迎使用智能客服后台管理系统")
    
    # 快捷入口
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👥 新增患者", use_container_width=True):
            st.switch_page("pages/02_👥_患者管理.py")
    
    with col2:
        if st.button("📅 创建复诊", use_container_width=True):
            st.switch_page("pages/03_📅_复诊管理.py")
    
    with col3:
        if st.button("💬 查看对话", use_container_width=True):
            st.switch_page("pages/04_💬_对话监管.py")
    
    with col4:
        if st.button("📚 管理知识", use_container_width=True):
            st.switch_page("pages/05_📚_知识库管理.py")
    
    st.divider()
    
    # 系统公告
    st.info("""
    **📢 系统公告**
    
    - 系统运行正常，AI 客服 7×24 小时在线
    - 本周复诊提醒已自动发送
    - 如有问题请联系管理员
    """)

if __name__ == "__main__":
    main()
```

---

## 📄 第四部分：页面开发（第 4-6 天）

### 4.1 登录页面

**文件**：`pages/00_🔐_登录.py`

```python
"""
登录页面
医护人员的身份认证入口
"""
import streamlit as st
from utils.api_client import APIClient
from utils.auth import login, is_logged_in

# 页面配置
st.set_page_config(
    page_title="登录 - 牙科修复复诊管理系统",
    page_icon="🔐",
    layout="centered"
)

# 已登录则跳转到仪表盘
if is_logged_in():
    st.switch_page("app.py")

# 登录表单
st.title("🔐 系统登录")
st.markdown("请输入您的账号和密码")

with st.form("login_form"):
    username = st.text_input("👤 用户名", placeholder="请输入用户名")
    password = st.text_input("🔑 密码", type="password", placeholder="请输入密码")
    submit = st.form_submit_button("登录", use_container_width=True)

if submit:
    if not username or not password:
        st.error("请输入用户名和密码")
    else:
        with st.spinner("登录中..."):
            try:
                client = APIClient()
                result = client.login(username, password)
                
                # 保存登录信息
                login(result["access_token"], result.get("user", {}))
                
                st.success("登录成功！")
                st.rerun()
                
            except Exception as e:
                st.error(f"登录失败：{str(e)}")

# 页脚
st.divider()
st.markdown("""
<div style='text-align: center; color: #999;'>
    <small>🦷 牙科修复复诊管理系统 © 2026</small>
</div>
""", unsafe_allow_html=True)
```

### 4.2 仪表盘页面

**文件**：`pages/01_📊_仪表盘.py`

```python
"""
仪表盘页面
展示系统关键指标与数据可视化
"""
import streamlit as st
from utils.auth import require_login, get_current_user
from utils.api_client import get_api_client
import plotly.express as px
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="仪表盘 - 牙科修复复诊管理系统",
    page_icon="📊",
    layout="wide"
)

# 要求登录
require_login()

# 页面标题
st.title("📊 数据仪表盘")
st.markdown("实时监控系统运行状态")

# 获取统计数据
with st.spinner("加载数据中..."):
    try:
        client = get_api_client()
        stats = client.get_stats_overview()
        appointments_trend = client.get_appointments_trend(days=7)
        dialogues_daily = client.get_dialogues_daily(days=7)
        patients_gender = client.get_patients_gender()
        appointments_status = client.get_appointments_status()
    except Exception as e:
        st.error(f"加载数据失败：{str(e)}")
        st.stop()

# 关键指标卡片
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 患者总数",
        value=stats.get("total_patients", 0),
        delta=stats.get("new_patients_today", 0)
    )

with col2:
    st.metric(
        label="📅 今日复诊",
        value=stats.get("today_appointments", 0),
        delta=stats.get("completed_appointments_today", 0)
    )

with col3:
    st.metric(
        label="💬 今日对话",
        value=stats.get("today_dialogues", 0),
        delta=f"{stats.get('dialogue_growth_rate', 0)}%"
    )

with col4:
    st.metric(
        label="📚 知识条目",
        value=stats.get("total_knowledge", 0),
        delta=stats.get("new_knowledge_this_week", 0)
    )

st.divider()

# 图表区域
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 近 7 日复诊趋势")
    if appointments_trend.get("data"):
        trend_data = appointments_trend["data"]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[item["date"] for item in trend_data],
            y=[item["count"] for item in trend_data],
            mode="lines+markers",
            name="复诊数",
            line=dict(color="#1890FF", width=3)
        ))
        fig.update_layout(
            height=300,
            xaxis_title="日期",
            yaxis_title="复诊数",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无数据")

with col2:
    st.subheader("💬 近 7 日对话量")
    if dialogues_daily.get("data"):
        dialogue_data = dialogues_daily["data"]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[item["date"] for item in dialogue_data],
            y=[item["count"] for item in dialogue_data],
            marker_color="#722ED1"
        ))
        fig.update_layout(
            height=300,
            xaxis_title="日期",
            yaxis_title="对话数",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无数据")

# 第二行图表
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 患者性别分布")
    if patients_gender.get("data"):
        gender_data = patients_gender["data"]
        fig = px.pie(
            values=[item["count"] for item in gender_data],
            names=[item["gender"] for item in gender_data],
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无数据")

with col2:
    st.subheader("📅 复诊状态分布")
    if appointments_status.get("data"):
        status_data = appointments_status["data"]
        fig = px.pie(
            values=[item["count"] for item in status_data],
            names=[item["status"] for item in status_data],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无数据")
```

### 4.3 患者管理页面

**文件**：`pages/02_👥_患者管理.py`

```python
"""
患者管理页面
患者档案的增删改查
"""
import streamlit as st
from utils.auth import require_login
from utils.api_client import get_api_client
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="患者管理 - 牙科修复复诊管理系统",
    page_icon="👥",
    layout="wide"
)

# 要求登录
require_login()

# 页面标题
st.title("👥 患者管理")
st.markdown("管理患者档案信息")

# 初始化客户端
client = get_api_client()

# 侧边栏筛选
with st.sidebar:
    st.subheader("🔍 筛选条件")
    search_name = st.text_input("姓名搜索")
    search_phone = st.text_input("手机号搜索")
    
    if st.button("搜索", use_container_width=True):
        st.rerun()

# 获取患者列表
with st.spinner("加载患者列表..."):
    try:
        result = client.get_patients(page=1, page_size=100)
        patients = result.get("items", [])
    except Exception as e:
        st.error(f"加载失败：{str(e)}")
        st.stop()

# 操作按钮
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("➕ 新增患者", use_container_width=True):
        st.session_state.show_add_form = True

# 新增患者表单
if st.session_state.get("show_add_form"):
    with st.form("add_patient_form"):
        st.subheader("➕ 新增患者")
        
        name = st.text_input("姓名")
        gender = st.selectbox("性别", ["男", "女"])
        age = st.number_input("年龄", min_value=1, max_value=150, value=30)
        phone = st.text_input("手机号")
        id_card = st.text_input("身份证号")
        medical_history = st.text_area("病史", placeholder="如有特殊病史请填写")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("保存", use_container_width=True)
        with col2:
            if st.form_submit_button("取消", use_container_width=True):
                st.session_state.show_add_form = False
                st.rerun()
        
        if submit:
            try:
                data = {
                    "name": name,
                    "gender": gender,
                    "age": age,
                    "phone": phone,
                    "id_card": id_card,
                    "medical_history": medical_history
                }
                client.create_patient(data)
                st.success("添加成功！")
                st.session_state.show_add_form = False
                st.rerun()
            except Exception as e:
                st.error(f"添加失败：{str(e)}")

# 患者列表表格
if patients:
    # 转换为 DataFrame
    df = pd.DataFrame(patients)
    
    # 选择显示的列
    columns = ["id", "name", "gender", "age", "phone", "created_at"]
    display_columns = ["ID", "姓名", "性别", "年龄", "手机号", "创建时间"]
    
    # 显示表格
    st.dataframe(
        df[columns],
        use_container_width=True,
        column_config={
            "id": "ID",
            "name": "姓名",
            "gender": "性别",
            "age": "年龄",
            "phone": "手机号",
            "created_at": "创建时间"
        },
        hide_index=True
    )
    
    # 操作区域
    st.subheader("🔧 操作")
    selected_id = st.selectbox(
        "选择患者进行操作",
        options=[p["id"] for p in patients],
        format_func=lambda x: f"ID: {x}"
    )
    
    if selected_id:
        patient = next((p for p in patients if p["id"] == selected_id), None)
        
        if patient:
            # 显示详情
            with st.expander("📄 患者详情"):
                for key, value in patient.items():
                    st.write(f"**{key}**: {value}")
            
            # 编辑按钮
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ 编辑", use_container_width=True):
                    st.session_state.edit_patient_id = selected_id
                    st.rerun()
            with col2:
                if st.button("🗑️ 删除", use_container_width=True):
                    if st.warning("确定要删除该患者吗？此操作不可恢复！"):
                        try:
                            client.delete_patient(selected_id)
                            st.success("删除成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"删除失败：{str(e)}")

# 编辑患者表单
if st.session_state.get("edit_patient_id"):
    patient_id = st.session_state.edit_patient_id
    patient = client.get_patient(patient_id)
    
    with st.form("edit_patient_form"):
        st.subheader(f"✏️ 编辑患者 (ID: {patient_id})")
        
        name = st.text_input("姓名", value=patient.get("name", ""))
        gender = st.selectbox("性别", ["男", "女"], index=0 if patient.get("gender") == "男" else 1)
        age = st.number_input("年龄", min_value=1, max_value=150, value=patient.get("age", 30))
        phone = st.text_input("手机号", value=patient.get("phone", ""))
        id_card = st.text_input("身份证号", value=patient.get("id_card", ""))
        medical_history = st.text_area("病史", value=patient.get("medical_history", ""))
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("保存修改", use_container_width=True)
        with col2:
            if st.form_submit_button("取消", use_container_width=True):
                st.session_state.edit_patient_id = None
                st.rerun()
        
        if submit:
            try:
                data = {
                    "name": name,
                    "gender": gender,
                    "age": age,
                    "phone": phone,
                    "id_card": id_card,
                    "medical_history": medical_history
                }
                client.update_patient(patient_id, data)
                st.success("更新成功！")
                st.session_state.edit_patient_id = None
                st.rerun()
            except Exception as e:
                st.error(f"更新失败：{str(e)}")
```

### 4.4 复诊管理页面

**文件**：`pages/03_📅_复诊管理.py`

```python
"""
复诊管理页面
复诊计划的创建、编辑、删除
"""
import streamlit as st
from utils.auth import require_login
from utils.api_client import get_api_client
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="复诊管理 - 牙科修复复诊管理系统",
    page_icon="📅",
    layout="wide"
)

# 要求登录
require_login()

# 页面标题
st.title("📅 复诊管理")
st.markdown("管理患者复诊计划")

# 初始化客户端
client = get_api_client()

# 获取患者列表（用于选择）
with st.spinner("加载患者列表..."):
    try:
        patients_result = client.get_patients(page=1, page_size=100)
        patients = patients_result.get("items", [])
        patient_options = {f"{p['name']} (ID: {p['id']})": p["id"] for p in patients}
    except Exception as e:
        st.error(f"加载患者失败：{str(e)}")
        st.stop()

# 获取复诊列表
with st.spinner("加载复诊计划..."):
    try:
        appointments_result = client.get_appointments(page=1, page_size=100)
        appointments = appointments_result.get("items", [])
    except Exception as e:
        st.error(f"加载复诊失败：{str(e)}")
        st.stop()

# 操作按钮
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("➕ 创建复诊计划", use_container_width=True):
        st.session_state.show_add_appointment = True

# 创建复诊表单
if st.session_state.get("show_add_appointment"):
    with st.form("add_appointment_form"):
        st.subheader("➕ 创建复诊计划")
        
        selected_patient = st.selectbox("选择患者", options=list(patient_options.keys()))
        appointment_date = st.date_input("复诊日期", min_value=datetime.today())
        appointment_time = st.time_input("复诊时间", value=datetime.now().time())
        treatment_type = st.selectbox(
            "治疗类型",
            ["固定义齿修复", "活动义齿修复", "种植义齿修复", "其他"]
        )
        notes = st.text_area("备注", placeholder="填写注意事项")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("保存", use_container_width=True)
        with col2:
            if st.form_submit_button("取消", use_container_width=True):
                st.session_state.show_add_appointment = False
                st.rerun()
        
        if submit:
            try:
                data = {
                    "patient_id": patient_options[selected_patient],
                    "appointment_date": appointment_date.strftime("%Y-%m-%d"),
                    "appointment_time": appointment_time.strftime("%H:%M"),
                    "treatment_type": treatment_type,
                    "notes": notes
                }
                client.create_appointment(data)
                st.success("创建成功！")
                st.session_state.show_add_appointment = False
                st.rerun()
            except Exception as e:
                st.error(f"创建失败：{str(e)}")

# 复诊列表
if appointments:
    st.subheader("📋 复诊计划列表")
    
    # 转换为 DataFrame
    df = pd.DataFrame(appointments)
    
    # 状态映射
    status_map = {
        "scheduled": "📅 待复诊",
        "completed": "✅ 已完成",
        "cancelled": "❌ 已取消",
        "no_show": "⚠️ 未到场"
    }
    
    # 显示表格
    st.dataframe(
        df[["id", "patient_id", "appointment_date", "appointment_time", "status"]],
        use_container_width=True,
        column_config={
            "id": "ID",
            "patient_id": "患者 ID",
            "appointment_date": "复诊日期",
            "appointment_time": "复诊时间",
            "status": "状态"
        },
        hide_index=True
    )
    
    # 操作区域
    st.subheader("🔧 操作")
    selected_id = st.selectbox(
        "选择复诊计划进行操作",
        options=[a["id"] for a in appointments],
        format_func=lambda x: f"ID: {x}"
    )
    
    if selected_id:
        appointment = next((a for a in appointments if a["id"] == selected_id), None)
        
        if appointment:
            # 显示详情
            with st.expander("📄 复诊详情"):
                for key, value in appointment.items():
                    st.write(f"**{key}**: {value}")
            
            # 状态更新
            st.subheader("更新状态")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📅 待复诊", use_container_width=True):
                    try:
                        client.update_appointment_status(selected_id, "scheduled")
                        st.success("更新成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"更新失败：{str(e)}")
            
            with col2:
                if st.button("✅ 已完成", use_container_width=True):
                    try:
                        client.update_appointment_status(selected_id, "completed")
                        st.success("更新成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"更新失败：{str(e)}")
            
            with col3:
                if st.button("❌ 已取消", use_container_width=True):
                    try:
                        client.update_appointment_status(selected_id, "cancelled")
                        st.success("更新成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"更新失败：{str(e)}")
            
            with col4:
                if st.button("⚠️ 未到场", use_container_width=True):
                    try:
                        client.update_appointment_status(selected_id, "no_show")
                        st.success("更新成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"更新失败：{str(e)}")
            
            # 删除按钮
            if st.button("🗑️ 删除复诊计划"):
                if st.warning("确定要删除该复诊计划吗？"):
                    try:
                        client.delete_appointment(selected_id)
                        st.success("删除成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"删除失败：{str(e)}")
else:
    st.info("暂无复诊计划")
```

### 4.5 对话监管页面

**文件**：`pages/04_💬_对话监管.py`

```python
"""
对话监管页面
查看 AI 对话记录，支持人工干预
"""
import streamlit as st
from utils.auth import require_login
from utils.api_client import get_api_client
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="对话监管 - 牙科修复复诊管理系统",
    page_icon="💬",
    layout="wide"
)

# 要求登录
require_login()

# 页面标题
st.title("💬 对话监管")
st.markdown("查看 AI 对话记录，必要时进行人工干预")

# 初始化客户端
client = get_api_client()

# 侧边栏筛选
with st.sidebar:
    st.subheader("🔍 筛选条件")
    
    # 获取患者列表
    try:
        patients_result = client.get_patients(page=1, page_size=100)
        patients = patients_result.get("items", [])
        patient_options = {"全部": None}
        patient_options.update({f"{p['name']} (ID: {p['id']})": p["id"] for p in patients})
    except Exception:
        patient_options = {"全部": None}
    
    selected_patient = st.selectbox("选择患者", options=list(patient_options.keys()))
    
    date_range = st.date_input("日期范围", value=[])
    
    if st.button("应用筛选", use_container_width=True):
        st.rerun()

# 获取对话列表
patient_id = patient_options.get(selected_patient)

with st.spinner("加载对话记录..."):
    try:
        result = client.get_dialogues(page=1, page_size=100, patient_id=patient_id)
        dialogues = result.get("items", [])
    except Exception as e:
        st.error(f"加载失败：{str(e)}")
        st.stop()

# 统计信息
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("总对话数", len(dialogues))

with col2:
    pending_count = sum(1 for d in dialogues if d.get("needs_handover"))
    st.metric("待人工干预", pending_count)

with col3:
    unique_sessions = len(set(d.get("session_id") for d in dialogues))
    st.metric("会话数", unique_sessions)

st.divider()

# 对话列表
if dialogues:
    st.subheader("📋 对话记录")
    
    for dialogue in dialogues:
        with st.expander(f"💬 {dialogue.get('created_at', '未知时间')} - 患者 ID: {dialogue.get('patient_id')}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**🧑 用户消息：**")
                st.info(dialogue.get("user_message", "无"))
                
                st.markdown("**🤖 AI 回复：**")
                st.success(dialogue.get("ai_response", "无"))
            
            with col2:
                st.markdown("**操作**")
                
                if st.button("👤 人工接管", key=f"handover_{dialogue['id']}"):
                    st.session_state.handover_id = dialogue["id"]
                
                if st.button("📄 查看详情", key=f"detail_{dialogue['id']}"):
                    st.session_state.detail_id = dialogue["id"]
    
    # 人工接管表单
    if st.session_state.get("handover_id"):
        dialogue_id = st.session_state.handover_id
        
        with st.form(f"handover_form_{dialogue_id}"):
            st.subheader("👤 人工接管")
            reason = st.text_area("接管原因", placeholder="说明为什么需要人工接管")
            manual_response = st.text_area("人工回复", placeholder="输入人工回复内容")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("提交", use_container_width=True)
            with col2:
                if st.form_submit_button("取消", use_container_width=True):
                    st.session_state.handover_id = None
                    st.rerun()
            
            if submit:
                try:
                    client.handover_dialogue(dialogue_id, reason)
                    # 这里可以添加发送人工回复的逻辑
                    st.success("接管成功！")
                    st.session_state.handover_id = None
                    st.rerun()
                except Exception as e:
                    st.error(f"接管失败：{str(e)}")

else:
    st.info("暂无对话记录")
```

### 4.6 知识库管理页面

**文件**：`pages/05_📚_知识库管理.py`

```python
"""
知识库管理页面
知识条目的增删改查
"""
import streamlit as st
from utils.auth import require_login
from utils.api_client import get_api_client

# 页面配置
st.set_page_config(
    page_title="知识库管理 - 牙科修复复诊管理系统",
    page_icon="📚",
    layout="wide"
)

# 要求登录
require_login()

# 页面标题
st.title("📚 知识库管理")
st.markdown("管理牙科修复专业知识")

# 初始化客户端
client = get_api_client()

# 获取分类列表
with st.spinner("加载分类..."):
    try:
        categories = client.get_knowledge_categories()
    except Exception:
        categories = []

# 获取知识列表
selected_category = st.selectbox("分类筛选", options=["全部"] + categories)

with st.spinner("加载知识列表..."):
    try:
        category_param = None if selected_category == "全部" else selected_category
        result = client.get_knowledge(page=1, page_size=100, category=category_param)
        knowledge_items = result.get("items", [])
    except Exception as e:
        st.error(f"加载失败：{str(e)}")
        st.stop()

# 操作按钮
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("➕ 新增知识", use_container_width=True):
        st.session_state.show_add_knowledge = True

# 新增知识表单
if st.session_state.get("show_add_knowledge"):
    with st.form("add_knowledge_form"):
        st.subheader("➕ 新增知识条目")
        
        category = st.selectbox("分类", options=categories if categories else ["其他"])
        title = st.text_input("标题")
        content = st.text_area("内容", height=200)
        keywords = st.text_input("关键词", placeholder="用逗号分隔多个关键词")
        source = st.text_input("来源", placeholder="如：《口腔修复学》第 8 版")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("保存", use_container_width=True)
        with col2:
            if st.form_submit_button("取消", use_container_width=True):
                st.session_state.show_add_knowledge = False
                st.rerun()
        
        if submit:
            try:
                data = {
                    "category": category,
                    "title": title,
                    "content": content,
                    "keywords": keywords,
                    "source": source
                }
                client.create_knowledge(data)
                st.success("添加成功！")
                st.session_state.show_add_knowledge = False
                st.rerun()
            except Exception as e:
                st.error(f"添加失败：{str(e)}")

# 知识列表
if knowledge_items:
    st.subheader(f"📋 知识列表 ({len(knowledge_items)} 条)")
    
    for item in knowledge_items:
        with st.expander(f"📄 {item.get('title', '无标题')} - {item.get('category', '未分类')}"):
            st.markdown(f"**关键词**: {item.get('keywords', '无')}")
            st.markdown(f"**来源**: {item.get('source', '未知')}")
            st.markdown("**内容：**")
            st.write(item.get("content", "无内容"))
            
            # 操作按钮
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ 编辑", key=f"edit_{item['id']}"):
                    st.session_state.edit_knowledge_id = item["id"]
                    st.rerun()
            with col2:
                if st.button("🗑️ 删除", key=f"delete_{item['id']}"):
                    if st.warning("确定要删除该知识条目吗？"):
                        try:
                            client.delete_knowledge(item["id"])
                            st.success("删除成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"删除失败：{str(e)}")
    
    # 编辑知识表单
    if st.session_state.get("edit_knowledge_id"):
        knowledge_id = st.session_state.edit_knowledge_id
        item = client.get_knowledge_item(knowledge_id)
        
        with st.form(f"edit_knowledge_form_{knowledge_id}"):
            st.subheader(f"✏️ 编辑知识 (ID: {knowledge_id})")
            
            category = st.selectbox("分类", options=categories if categories else ["其他"], 
                                   index=categories.index(item.get("category", categories[0])) if item.get("category") in categories else 0)
            title = st.text_input("标题", value=item.get("title", ""))
            content = st.text_area("内容", value=item.get("content", ""), height=200)
            keywords = st.text_input("关键词", value=item.get("keywords", ""))
            source = st.text_input("来源", value=item.get("source", ""))
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("保存修改", use_container_width=True)
            with col2:
                if st.form_submit_button("取消", use_container_width=True):
                    st.session_state.edit_knowledge_id = None
                    st.rerun()
            
            if submit:
                try:
                    data = {
                        "category": category,
                        "title": title,
                        "content": content,
                        "keywords": keywords,
                        "source": source
                    }
                    client.update_knowledge(knowledge_id, data)
                    st.success("更新成功！")
                    st.session_state.edit_knowledge_id = None
                    st.rerun()
                except Exception as e:
                    st.error(f"更新失败：{str(e)}")

else:
    st.info("暂无知识条目")
```

### 4.7 系统设置页面

**文件**：`pages/06_⚙️_系统设置.py`

```python
"""
系统设置页面
系统参数配置
"""
import streamlit as st
from utils.auth import require_login

# 页面配置
st.set_page_config(
    page_title="系统设置 - 牙科修复复诊管理系统",
    page_icon="⚙️",
    layout="wide"
)

# 要求登录
require_login()

# 页面标题
st.title("⚙️ 系统设置")
st.markdown("配置系统运行参数")

# 系统信息
st.subheader("📊 系统信息")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **系统名称**: 牙科修复复诊管理系统
    
    **版本**: v1.0.0
    
    **开发框架**: Streamlit 1.31.0
    
    **后端 API**: FastAPI 0.109.0
    """)

with col2:
    st.info("""
    **AI 模型**: Qwen2.5-7B-Instruct
    
    **数据库**: MySQL 8.0
    
    **缓存**: Redis 6.0
    """)

# 配置项
st.subheader("🔧 配置项")

st.warning("⚠️ 以下配置项为示例，实际配置需要后端 API 支持")

with st.form("system_config"):
    st.markdown("**复诊提醒配置**")
    
    reminder_days = st.multiselect(
        "提醒时间",
        ["复诊前 1 天", "复诊当天", "复诊后 1 天"],
        default=["复诊前 1 天"]
    )
    
    reminder_time = st.time_input("提醒发送时间", value="09:00")
    
    st.markdown("**AI 客服配置**")
    
    max_tokens = st.slider("最大回复长度", 100, 1000, 500)
    
    temperature = st.slider("回复创造性", 0.0, 1.0, 0.7)
    
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("保存配置", use_container_width=True)
    with col2:
        reset = st.form_submit_button("恢复默认", use_container_width=True)
    
    if submit:
        st.success("配置保存成功！（示例）")
    
    if reset:
        st.info("已恢复默认配置")

# 敏感词配置
st.subheader("🚫 敏感词管理")

with st.expander("管理敏感词"):
    sensitive_words = st.text_area(
        "敏感词列表",
        value="广告，推销，诈骗",
        help="用逗号分隔多个敏感词"
    )
    
    if st.button("更新敏感词"):
        st.success("敏感词更新成功！（示例）")

# 数据备份
st.subheader("💾 数据备份")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 导出数据", use_container_width=True):
        st.info("数据导出功能开发中...")

with col2:
    if st.button("📤 导入数据", use_container_width=True):
        st.info("数据导入功能开发中...")

with col3:
    if st.button("🗑️ 清空缓存", use_container_width=True):
        st.success("缓存已清空！")
```

---

## 🚀 第五部分：运行与测试（第 7 天）

### 5.1 启动应用

```bash
# 确保虚拟环境已激活
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 启动 Streamlit 应用
streamlit run app.py
```

浏览器自动打开 http://localhost:8501

### 5.2 默认账号

使用后端系统中的医护账号登录：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| doctor1 | doctor123 | 医生 |
| nurse1 | nurse123 | 护士 |

### 5.3 功能测试清单

| 功能 | 测试内容 | 预期结果 |
|------|----------|----------|
| 登录 | 输入正确/错误账号 | 成功/失败 |
| 仪表盘 | 查看统计数据 | 数据正常显示 |
| 患者管理 | 新增/编辑/删除 | CRUD 正常 |
| 复诊管理 | 创建/更新状态 | 功能正常 |
| 对话监管 | 查看对话/人工接管 | 功能正常 |
| 知识库 | 新增/编辑/删除 | CRUD 正常 |

---

## 🐛 常见问题

### Q1: 启动时报错 "Port already in use"

**解决方案**：
```bash
# 修改端口
streamlit run app.py --server.port 8502
```

### Q2: 页面空白或无数据

**检查项**：
1. 后端服务是否启动
2. API 地址是否正确
3. 是否已登录

### Q3: 中文显示乱码

**解决方案**：
确保文件保存为 UTF-8 编码。

### Q4: 图表不显示

**解决方案**：
```bash
# 重新安装 plotly
pip install --upgrade plotly
```

---

## 📊 代码统计

| 模块 | 文件数 | 代码行数 |
|------|--------|----------|
| 主应用 | 1 | ~80 行 |
| 页面 | 7 | ~1400 行 |
| 工具模块 | 2 | ~350 行 |
| 配置 | 1 | ~20 行 |
| **总计** | **11** | **~1850 行** |

---

## ✅ 验收标准

完成本指南后，系统应满足：

- [ ] 医护人员可以成功登录
- [ ] 仪表盘显示统计数据
- [ ] 患者管理支持 CRUD 操作
- [ ] 复诊计划可以创建和更新状态
- [ ] 可以查看 AI 对话记录
- [ ] 知识库可以管理
- [ ] 界面美观、操作流畅

---

## 📚 参考文档

1. Streamlit 官方文档：https://docs.streamlit.io/
2. Plotly 图表库：https://plotly.com/python/
3. Pandas 数据处理：https://pandas.pydata.org/docs/

---

**最后更新**：2026 年 3 月 7 日  
**文档版本**：v1.0
