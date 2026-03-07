"""
仪表盘页面
展示系统关键指标与数据可视化
"""
import streamlit as st
from utils.auth import get_token, is_logged_in
from utils.api_client import APIClient
import plotly.express as px
import plotly.graph_objects as go
from datetime import time

# 页面配置
st.set_page_config(
    page_title="仪表盘 - 牙科修复复诊管理系统",
    page_icon="📊",
    layout="wide"
)

# 检查登录状态
if not is_logged_in():
    st.warning("⚠️ 请先登录")
    if st.button("🔐 去登录"):
        st.switch_page("pages/00_🔐_登录.py")
    st.stop()

# 获取 Token 并创建客户端
token = get_token()
if not token:
    st.error("未获取到 Token，请重新登录")
    st.stop()

client = APIClient(token=token)

# 页面标题和刷新按钮
col_title, col_refresh = st.columns([5, 1])

with col_title:
    st.title("📊 数据仪表盘")
    st.markdown("实时监控系统运行状态")

with col_refresh:
    if st.button("🔄 刷新", use_container_width=True, help="获取最新统计数据"):
        # 清除缓存数据
        for key in ["stats_cache", "trend_cache", "dialogues_cache", "gender_cache", "status_cache"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

st.divider()
with st.spinner("加载数据中..."):
    try:
        stats = client.get_stats_overview()
        appointments_trend = client.get_appointments_trend(days=7)
        dialogues_daily = client.get_dialogues_daily(days=7)
        patients_gender = client.get_patients_gender()
        appointments_status = client.get_appointments_status()
    except Exception as e:
        st.error(f"加载数据失败：{str(e)}")
        st.info("提示：后端服务需要正常运行才能显示数据")
        st.stop()

# 关键指标卡片
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 患者总数",
        value=stats.get("total_patients", 0) if isinstance(stats, dict) else 0,
        delta=stats.get("new_patients_today", 0) if isinstance(stats, dict) else 0
    )

with col2:
    st.metric(
        label="📅 今日复诊",
        value=stats.get("today_appointments", 0) if isinstance(stats, dict) else 0,
        delta=stats.get("completed_appointments_today", 0) if isinstance(stats, dict) else 0
    )

with col3:
    st.metric(
        label="💬 今日对话",
        value=stats.get("today_dialogues", 0) if isinstance(stats, dict) else 0,
        delta=f"{stats.get('dialogue_growth_rate', 0)}%" if isinstance(stats, dict) else "0%"
    )

with col4:
    st.metric(
        label="📚 知识条目",
        value=stats.get("total_knowledge", 0) if isinstance(stats, dict) else 0,
        delta=stats.get("new_knowledge_this_week", 0) if isinstance(stats, dict) else 0
    )

st.divider()

# 图表区域
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 近 7 日复诊趋势")
    if isinstance(appointments_trend, list) and len(appointments_trend) > 0:
        # 构建 7 天数据，缺失的日期补 0
        from datetime import datetime, timedelta
        import pandas as pd
        today = datetime.now().date()
        seven_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        
        # 创建数据字典
        trend_dict = {day: 0 for day in seven_days}
        for item in appointments_trend:
            date = item.get("date", "")[:10]  # 只取日期部分
            if date in trend_dict:
                trend_dict[date] = item.get("count", 0)
        
        # 使用 DataFrame 显示图表
        df = pd.DataFrame({
            "日期": list(trend_dict.keys()),
            "复诊数": list(trend_dict.values())
        })
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["日期"],
            y=df["复诊数"],
            mode="lines+markers",
            name="复诊数",
            line=dict(color="#1890FF", width=3)
        ))
        fig.update_layout(
            height=300,
            xaxis_title="日期",
            yaxis_title="复诊数",
            showlegend=False,
            xaxis=dict(
                tickangle=0,  # 日期水平显示
                tickformat="%m/%d",  # 显示月/日
                tickmode="array",
                tickvals=df["日期"],
                ticktext=[datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d") for d in df["日期"]]
            ),
            yaxis=dict(
                rangemode="tozero",  # y 轴从 0 开始
                range=[0, max(1, max(df["复诊数"]) + 1)]  # 强制 y 轴范围从 0 开始
            ),
            hovermode="x unified",  # 鼠标悬停显示数据
            dragmode=False  # 禁用拖拽
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False})
    else:
        # 没有数据时显示空白的 7 天图表
        from datetime import datetime, timedelta
        import pandas as pd
        today = datetime.now().date()
        seven_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        empty_dict = {day: 0 for day in seven_days}
        df = pd.DataFrame({
            "日期": list(empty_dict.keys()),
            "复诊数": list(empty_dict.values())
        })
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["日期"],
            y=df["复诊数"],
            mode="lines+markers",
            line=dict(color="#1890FF", width=3)
        ))
        fig.update_layout(
            height=300,
            xaxis_title="日期",
            yaxis_title="复诊数",
            showlegend=False,
            xaxis=dict(
                tickangle=0,
                tickformat="%m/%d",
                tickmode="array",
                tickvals=df["日期"],
                ticktext=[datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d") for d in df["日期"]]
            ),
            yaxis=dict(
                rangemode="tozero",
                range=[0, 1]
            ),
            hovermode="x unified",
            dragmode=False
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False})

with col2:
    st.subheader("💬 近 7 日对话量")
    if isinstance(dialogues_daily, list) and len(dialogues_daily) > 0:
        # 构建 7 天数据，缺失的日期补 0
        from datetime import datetime, timedelta
        import pandas as pd
        today = datetime.now().date()
        seven_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        
        # 创建数据字典
        dialogue_dict = {day: 0 for day in seven_days}
        for item in dialogues_daily:
            date = item.get("date", "")[:10]  # 只取日期部分
            if date in dialogue_dict:
                dialogue_dict[date] = item.get("count", 0)
        
        # 使用 DataFrame 显示图表
        df = pd.DataFrame({
            "日期": list(dialogue_dict.keys()),
            "对话数": list(dialogue_dict.values())
        })
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["日期"],
            y=df["对话数"],
            marker_color="#722ED1"
        ))
        fig.update_layout(
            height=300,
            xaxis_title="日期",
            yaxis_title="对话数",
            showlegend=False,
            xaxis=dict(
                tickangle=0,  # 日期水平显示
                tickformat="%m/%d",  # 显示月/日
                tickmode="array",
                tickvals=df["日期"],
                ticktext=[datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d") for d in df["日期"]]
            ),
            yaxis=dict(
                rangemode="tozero",  # y 轴从 0 开始
                range=[0, max(1, max(df["对话数"]) + 1)]  # 强制 y 轴范围从 0 开始
            ),
            hovermode="x unified",  # 鼠标悬停显示数据
            dragmode=False  # 禁用拖拽
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False})
    else:
        # 没有数据时显示空白的 7 天图表
        from datetime import datetime, timedelta
        import pandas as pd
        today = datetime.now().date()
        seven_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        empty_dict = {day: 0 for day in seven_days}
        df = pd.DataFrame({
            "日期": list(empty_dict.keys()),
            "对话数": list(empty_dict.values())
        })
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["日期"],
            y=df["对话数"],
            marker_color="#722ED1"
        ))
        fig.update_layout(
            height=300,
            xaxis_title="日期",
            yaxis_title="对话数",
            showlegend=False,
            xaxis=dict(
                tickangle=0,
                tickformat="%m/%d",
                tickmode="array",
                tickvals=df["日期"],
                ticktext=[datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d") for d in df["日期"]]
            ),
            yaxis=dict(
                rangemode="tozero",
                range=[0, 1]
            ),
            hovermode="x unified",
            dragmode=False
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False})

# 第二行图表
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 患者性别分布")
    if isinstance(patients_gender, list) and len(patients_gender) > 0:
        fig = px.pie(
            values=[item.get("count", 0) for item in patients_gender],
            names=[item.get("gender", "未知") for item in patients_gender],
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无数据")

with col2:
    st.subheader("📅 复诊状态分布")
    if isinstance(appointments_status, list) and len(appointments_status) > 0:
        fig = px.pie(
            values=[item.get("count", 0) for item in appointments_status],
            names=[item.get("status", "未知") for item in appointments_status],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无数据")
