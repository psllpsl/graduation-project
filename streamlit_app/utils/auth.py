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
