"""
忘记密码 - 重置密码页面
需要管理员身份验证
"""
import streamlit as st
from utils.api_client import APIClient

# 页面配置
st.set_page_config(
    page_title="忘记密码 - 牙科修复复诊管理系统",
    page_icon="🔑",
    layout="centered"
)

# 页面标题
st.title("🔑 忘记密码")
st.markdown("重置用户密码（需要管理员确认）")

# 返回登录链接
if st.button("← 返回登录", key="back_to_login"):
    st.switch_page("pages/00_🔐_登录.py")

st.divider()

# 说明
st.info("""
**重置密码流程：**
1. 输入需要重置密码的用户名
2. 输入管理员账号和密码进行身份验证
3. 输入新密码并确认
4. 点击"重置密码"
""")

# 重置密码表单
with st.form("reset_password_form"):
    st.subheader("填写重置信息")
    
    # 第一部分：要重置的用户
    st.markdown("**1️⃣ 需要重置密码的账号**")
    target_username = st.text_input("用户名", placeholder="要重置哪个用户的密码？", key="target_user")
    
    st.divider()
    
    # 第二部分：管理员验证
    st.markdown("**2️⃣ 管理员身份验证**")
    col1, col2 = st.columns(2)
    with col1:
        admin_username = st.text_input("管理员用户名", placeholder="admin", key="admin_user")
    with col2:
        admin_password = st.text_input("管理员密码", type="password", placeholder="输入 admin 密码", key="admin_pass")
    
    st.divider()
    
    # 第三部分：新密码
    st.markdown("**3️⃣ 设置新密码**")
    col3, col4 = st.columns(2)
    with col3:
        new_password = st.text_input("新密码", type="password", placeholder="至少 6 个字符", key="new_pass")
    with col4:
        confirm_password = st.text_input("确认密码", type="password", placeholder="再次输入新密码", key="confirm_pass")
    
    st.divider()
    
    submit = st.form_submit_button("重置密码", use_container_width=True, type="primary")

if submit:
    # 验证输入
    if not target_username or not admin_username or not admin_password:
        st.error("请填写所有必填项")
    elif not new_password or not confirm_password:
        st.error("请填写新密码")
    elif len(new_password) < 6:
        st.error("密码至少需要 6 个字符")
    elif new_password != confirm_password:
        st.error("两次输入的密码不一致")
    else:
        with st.spinner("重置密码中..."):
            try:
                client = APIClient()
                
                # 调用重置密码 API（使用 params）
                result = client._request("POST", 
                    f"{client.BASE_URL}/auth/reset-password",
                    params={
                        "target_username": target_username,
                        "admin_username": admin_username,
                        "admin_password": admin_password,
                        "new_password": new_password
                    }
                )
                
                st.success("✅ 密码重置成功！")
                st.info(f"用户：{target_username}\n请使用新密码登录")
                
                # 跳转到登录页面
                st.switch_page("pages/00_🔐_登录.py")
                
            except Exception as e:
                error_msg = str(e)
                if "管理员验证失败" in error_msg or "管理员密码错误" in error_msg:
                    st.error("管理员身份验证失败，请检查管理员账号和密码")
                elif "用户不存在" in error_msg:
                    st.error(f"用户 '{target_username}' 不存在")
                else:
                    st.error(f"重置失败：{error_msg}")
