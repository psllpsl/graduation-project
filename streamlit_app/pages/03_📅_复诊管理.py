"""
复诊管理页面
复诊计划的创建、编辑、删除
"""
import streamlit as st
from utils.auth import get_token, is_logged_in
from utils.api_client import APIClient
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="复诊管理 - 牙科修复复诊管理系统",
    page_icon="📅",
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
    st.title("📅 复诊管理")
    st.markdown("管理患者复诊计划")

with col_refresh:
    if st.button("🔄 刷新", use_container_width=True, help="获取最新复诊数据"):
        # 清除缓存数据
        if "appointments_cache" in st.session_state:
            del st.session_state.appointments_cache
        st.rerun()

st.divider()

# 获取患者列表（用于选择）
with st.spinner("加载患者列表..."):
    try:
        patients_result = client.get_patients(page=1, page_size=100)
        if isinstance(patients_result, list):
            patients = patients_result
        else:
            patients = patients_result.get("items", []) if isinstance(patients_result, dict) else []
        patient_options = {f"{p['name']} (ID: {p['id']})": p["id"] for p in patients}
    except Exception as e:
        st.error(f"加载患者失败：{str(e)}")
        patient_options = {}

# 获取复诊列表
with st.spinner("加载复诊计划..."):
    try:
        appointments_result = client.get_appointments(page=1, page_size=1000)
        if isinstance(appointments_result, list):
            appointments = appointments_result
        else:
            appointments = appointments_result.get("items", []) if isinstance(appointments_result, dict) else []
        
        # 保存到 session_state 用于刷新
        st.session_state.appointments_cache = appointments
    except Exception as e:
        st.error(f"加载复诊失败：{str(e)}")
        appointments = st.session_state.get("appointments_cache", [])

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
                # 合并日期和时间
                appointment_datetime = datetime.combine(appointment_date, appointment_time)
                
                data = {
                    "patient_id": patient_options[selected_patient],
                    "appointment_date": appointment_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                    "appointment_type": treatment_type,
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

    # 创建患者 ID 到姓名的映射
    patient_id_to_name = {p["id"]: p["name"] for p in patients}

    # 转换为 DataFrame
    df = pd.DataFrame(appointments)

    # 添加患者姓名列
    df["patient_name"] = df["patient_id"].apply(lambda x: patient_id_to_name.get(x, "未知"))

    # 显示表格 - 使用实际存在的列
    display_columns = ["patient_name", "appointment_date", "appointment_type", "status", "notes"]
    available_columns = [col for col in display_columns if col in df.columns]

    st.dataframe(
        df[available_columns],
        use_container_width=True,
        column_config={
            "patient_name": st.column_config.TextColumn("患者姓名", width="medium"),
            "appointment_date": st.column_config.DatetimeColumn("复诊日期", format="YYYY-MM-DD HH:mm"),
            "appointment_type": st.column_config.TextColumn("复诊类型", width="medium"),
            "status": st.column_config.TextColumn("状态", width="small"),
            "notes": st.column_config.TextColumn("备注", width="large")
        },
        hide_index=True
    )

    # 操作区域
    st.subheader("🔧 操作")
    
    # 创建 (复诊 ID, 患者姓名 + 复诊日期) 映射列表，用于下拉框显示
    appointment_options = [
        (a["id"], f"{patient_id_to_name.get(a['patient_id'], '未知')} - {a['appointment_date'][:16]}")
        for a in appointments
    ]
    
    selected_option = st.selectbox(
        "选择复诊计划进行操作",
        options=appointment_options,
        format_func=lambda x: x[1]  # 显示患者姓名和复诊日期
    )
    
    # 获取选中的复诊 ID
    selected_id = selected_option[0] if selected_option else None

    if selected_id:
        appointment = next((a for a in appointments if a["id"] == selected_id), None)

        if appointment:
            # 获取患者姓名
            patient_name = patient_id_to_name.get(appointment["patient_id"], "未知")
            
            # 显示详情 - 中文字段名
            with st.expander(f"📄 复诊详情 - {patient_name}"):
                # 中文字段映射
                field_names = {
                    "id": "复诊 ID",
                    "patient_id": "患者 ID",
                    "patient_name": "患者姓名",
                    "appointment_date": "复诊日期时间",
                    "appointment_type": "复诊类型",
                    "status": "当前状态",
                    "reminder_sent": "已发送提醒",
                    "reminder_time": "提醒发送时间",
                    "notes": "备注说明",
                    "created_at": "创建时间",
                    "updated_at": "最后更新时间"
                }
                
                # 状态翻译
                status_map = {
                    "pending": "📅 待复诊",
                    "completed": "✅ 已完成",
                    "cancelled": "❌ 已取消",
                    "no_show": "⚠️ 未到场"
                }
                
                for key, value in appointment.items():
                    cn_name = field_names.get(key, key)
                    # 特殊处理状态字段
                    if key == "status":
                        value = status_map.get(value, value)
                    # 特殊处理布尔值
                    elif key == "reminder_sent":
                        value = "✅ 是" if value else "❌ 否"
                    # 格式化时间字段
                    elif key in ["appointment_date", "reminder_time", "created_at", "updated_at"]:
                        if value:
                            value = value.replace("T", " ")[:19] if "T" in str(value) else str(value)[:19]
                    
                    st.write(f"**{cn_name}**: {value}")
            
            # 状态更新
            st.subheader("🔄 更新状态")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📅 待复诊", use_container_width=True, help="设置为待复诊状态"):
                    try:
                        client.update_appointment_status(selected_id, "pending")
                        st.success("更新成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"更新失败：{str(e)}")

            with col2:
                if st.button("✅ 已完成", use_container_width=True, help="设置为已完成状态"):
                    try:
                        client.update_appointment_status(selected_id, "completed")
                        st.success("更新成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"更新失败：{str(e)}")

            with col3:
                if st.button("❌ 已取消", use_container_width=True, help="设置为已取消状态"):
                    try:
                        client.update_appointment_status(selected_id, "cancelled")
                        st.success("更新成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"更新失败：{str(e)}")
            
            # 删除按钮 - 两步确认
            deleting_id = st.session_state.get("deleting_appointment_id")
            if deleting_id == selected_id:
                st.warning("⚠️ 确定要删除该复诊计划吗？")
                col_del1, col_del2 = st.columns(2)
                with col_del1:
                    if st.button("✅ 确认删除", key=f"confirm_{selected_id}", type="primary", use_container_width=True):
                        try:
                            client.delete_appointment(selected_id)
                            st.success("删除成功！")
                            st.session_state.deleting_appointment_id = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"删除失败：{str(e)}")
                with col_del2:
                    if st.button("❌ 取消", key=f"cancel_{selected_id}", use_container_width=True):
                        st.session_state.deleting_appointment_id = None
                        st.rerun()
            else:
                if st.button("🗑️ 删除复诊计划", use_container_width=True):
                    st.session_state.deleting_appointment_id = selected_id
                    st.rerun()
else:
    st.info("暂无复诊计划")
