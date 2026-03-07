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
    initial_sidebar_state="collapsed"
)

# 主页面
def main():
    """主页面"""
    
    # 未登录时显示登录提示
    if not is_logged_in():
        st.markdown('# 🦷 牙科修复复诊管理系统')
        st.markdown("欢迎使用智能客服后台管理系统")
        st.divider()
        st.warning("⚠️ 请先登录后使用系统", icon="🔐")
        st.markdown(
            """
            <div style='text-align: center; margin: 20px 0;'>
                <p style='color: #666; margin-bottom: 15px;'>使用医护账号登录系统</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔐 去登录", use_container_width=True, type="primary"):
                st.switch_page("pages/00_🔐_登录.py")
        return
    
    # 已登录时显示主界面
    # 顶部用户信息栏
    col_user, col_logout = st.columns([4, 1])

    with col_user:
        user = get_current_user()
        st.markdown(f"### 👤 欢迎，{user.get('real_name', '未知')} ({user.get('role', 'user')})")

    with col_logout:
        if st.button("🚪 退出登录", use_container_width=True):
            logout()
            st.rerun()

    st.divider()

    # 页面标题
    st.markdown('# 🦷 牙科修复复诊管理系统')
    st.markdown("欢迎使用智能客服后台管理系统")

    # 快捷入口
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("👥 患者管理", use_container_width=True):
            st.switch_page("pages/02_👥_患者管理.py")

    with col2:
        if st.button("📅 复诊管理", use_container_width=True):
            st.switch_page("pages/03_📅_复诊管理.py")

    with col3:
        if st.button("💬 对话监管", use_container_width=True):
            st.switch_page("pages/04_💬_对话监管.py")

    with col4:
        if st.button("📚 知识库管理", use_container_width=True):
            st.switch_page("pages/05_📚_知识库管理.py")

    st.divider()

    # 第二行功能
    col5, col6 = st.columns(2)

    with col5:
        if st.button("📊 数据仪表盘", use_container_width=True):
            st.switch_page("pages/01_📊_仪表盘.py")

    with col6:
        if st.button("⚙️ 系统设置", use_container_width=True):
            st.switch_page("pages/06_⚙️_系统设置.py")

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
