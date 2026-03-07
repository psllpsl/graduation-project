"""
系统设置页面
系统参数配置
"""
import streamlit as st
from utils.auth import get_token, is_logged_in
from datetime import time

# 页面配置
st.set_page_config(
    page_title="系统设置 - 牙科修复复诊管理系统",
    page_icon="⚙️",
    layout="wide"
)

# 检查登录状态
if not is_logged_in():
    st.warning("⚠️ 请先登录")
    if st.button("🔐 去登录"):
        st.switch_page("pages/00_🔐_登录.py")
    st.stop()

# 页面标题和刷新按钮
col_title, col_refresh = st.columns([5, 1])

with col_title:
    st.title("⚙️ 系统设置")
    st.markdown("配置系统运行参数")

with col_refresh:
    if st.button("🔄 刷新", use_container_width=True, help="刷新页面"):
        st.rerun()

st.divider()

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
    
    reminder_time = st.time_input("提醒发送时间", value=time(9, 0))
    
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
