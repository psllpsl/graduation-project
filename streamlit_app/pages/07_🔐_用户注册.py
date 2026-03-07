"""
用户注册页面
需要管理员密码确认
"""
import streamlit as st
from utils.api_client import APIClient

# 页面配置
st.set_page_config(
    page_title="用户注册 - 牙科修复复诊管理系统",
    page_icon="🔐",
    layout="centered"
)

# 页面标题
st.title("🔐 用户注册")
st.markdown("创建新的医护账号（需要管理员确认）")

# 返回登录链接
if st.button("← 返回登录"):
    st.switch_page("pages/00_🔐_登录.py")

st.divider()

# 说明
st.info("""
**注册流程：**
1. 填写新用户信息
2. 输入管理员账号和密码进行验证
3. 点击"注册"
""")

# 注册表单
with st.form("register_form"):
    st.subheader("填写注册信息")
    
    # 第一部分：新用户信息
    st.markdown("**1️⃣ 新用户信息**")
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("👤 用户名", placeholder="3-50 个字符", max_chars=50)
        real_name = st.text_input("📛 真实姓名", placeholder="请输入真实姓名", max_chars=50)
    
    with col2:
        password = st.text_input("🔑 密码", type="password", placeholder="至少 6 个字符")
        confirm_password = st.text_input("🔑 确认密码", type="password", placeholder="再次输入密码")
    
    role = st.selectbox("👔 角色", options=["doctor", "admin"], help="选择用户角色")
    phone = st.text_input("📱 手机号", placeholder="选填", max_chars=20)
    
    st.divider()
    
    # 第二部分：管理员验证
    st.markdown("**2️⃣ 管理员身份验证**")
    col3, col4 = st.columns(2)
    with col3:
        admin_username = st.text_input("管理员用户名", placeholder="admin", key="admin_user")
    with col4:
        admin_password = st.text_input("管理员密码", type="password", placeholder="输入 admin 密码", key="admin_pass")
    
    st.divider()
    
    submit = st.form_submit_button("注册", use_container_width=True, type="primary")

if submit:
    # 验证输入
    if not username or not password or not real_name:
        st.error("请填写用户名、密码和真实姓名")
    elif len(password) < 6:
        st.error("密码至少需要 6 个字符")
    elif password != confirm_password:
        st.error("两次输入的密码不一致")
    elif not admin_username or not admin_password:
        st.error("请填写管理员账号和密码进行验证")
    else:
        with st.spinner("注册中..."):
            try:
                client = APIClient()
                
                # 调用注册 API（带管理员验证）
                result = client._request("POST", f"{client.BASE_URL}/auth/register", json={
                    "username": username,
                    "password": password,
                    "real_name": real_name,
                    "role": role,
                    "phone": phone,
                    "admin_username": admin_username,
                    "admin_password": admin_password
                })
                
                st.success("注册成功！")
                st.info(f"用户名：{username}\n角色：{role}")
                
                # 跳转到登录页面
                st.switch_page("pages/00_🔐_登录.py")
                
            except Exception as e:
                error_msg = str(e)
                if "用户名已存在" in error_msg:
                    st.error("用户名已存在，请更换其他用户名")
                elif "管理员身份验证失败" in error_msg:
                    st.error("管理员身份验证失败，请检查管理员账号")
                elif "管理员密码错误" in error_msg:
                    st.error("管理员密码错误")
                else:
                    st.error(f"注册失败：{error_msg}")
