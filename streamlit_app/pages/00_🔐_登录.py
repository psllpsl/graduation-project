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

# 已登录则跳转到主页面
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
                user_info = result.get("user", {})
                login(result["access_token"], user_info)

                st.success("登录成功！")
                st.rerun()

            except Exception as e:
                error_msg = str(e)
                # 根据错误类型显示友好提示
                if "认证失败" in error_msg or "账号密码" in error_msg:
                    st.error("🔐 账号或密码错误，请重试")
                elif "权限不足" in error_msg:
                    st.error("⚠️ 权限不足，无法登录")
                elif "网络请求失败" in error_msg:
                    st.error("🌐 无法连接服务器，请检查后端服务是否启动")
                else:
                    st.error(f"登录失败：{error_msg}")

# 页脚
st.divider()

# 添加注册和忘记密码入口
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("📝 注册账号", use_container_width=True):
        st.switch_page("pages/07_🔐_用户注册.py")

with col2:
    if st.button("🔑 忘记密码", use_container_width=True):
        st.switch_page("pages/08_🔑_忘记密码.py")

with col3:
    st.markdown(
        """
        <div style='text-align: center; color: #999; margin-top: 10px;'>
            <small>🦷 牙科修复复诊管理系统 © 2026</small>
        </div>
        """,
        unsafe_allow_html=True
    )
