"""
患者管理页面
患者档案的增删改查
"""
import streamlit as st
from utils.auth import get_token, is_logged_in
from utils.api_client import APIClient
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="患者管理 - 牙科修复复诊管理系统",
    page_icon="👥",
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
    st.title("👥 患者管理")
    st.markdown("管理患者档案信息")

with col_refresh:
    if st.button("🔄 刷新", use_container_width=True, help="获取最新患者数据"):
        # 清除缓存数据
        if "patients_cache" in st.session_state:
            del st.session_state.patients_cache
        if "search_name" in st.session_state:
            st.session_state.search_name = ""
        if "search_phone" in st.session_state:
            st.session_state.search_phone = ""
        st.rerun()

st.divider()

# 初始化 session_state
if "search_name" not in st.session_state:
    st.session_state.search_name = ""
if "search_phone" not in st.session_state:
    st.session_state.search_phone = ""

# 侧边栏筛选
with st.sidebar:
    st.subheader("🔍 筛选条件")
    
    # 使用 key 绑定 session_state
    search_name_input = st.text_input(
        "姓名搜索",
        value=st.session_state.search_name,
        key="search_name_input"
    )
    search_phone_input = st.text_input(
        "手机号搜索",
        value=st.session_state.search_phone,
        key="search_phone_input"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("搜索", use_container_width=True):
            st.session_state.search_name = search_name_input
            st.session_state.search_phone = search_phone_input
            st.rerun()
    
    with col2:
        if st.button("重置", use_container_width=True):
            st.session_state.search_name = ""
            st.session_state.search_phone = ""
            st.rerun()

# 获取患者列表
with st.spinner("加载患者列表..."):
    try:
        # 直接获取所有患者，不分页
        result = client.get_patients(page=1, page_size=1000)
        # 后端返回的是列表
        if isinstance(result, list):
            all_patients = result
        else:
            all_patients = result.get("items", []) if isinstance(result, dict) else []
        
        # 保存到 session_state 用于刷新
        st.session_state.patients_cache = all_patients
    except Exception as e:
        st.error(f"加载失败：{str(e)}")
        all_patients = st.session_state.get("patients_cache", [])

# 应用筛选条件
patients = all_patients
if st.session_state.search_name:
    patients = [p for p in patients if st.session_state.search_name.lower() in (p.get("name") or "").lower()]
    st.info(f"🔍 按姓名筛选：'{st.session_state.search_name}'，找到 {len(patients)} 个患者")

if st.session_state.search_phone:
    patients = [p for p in patients if st.session_state.search_phone in (p.get("phone") or "")]
    st.info(f"🔍 按手机号筛选：'{st.session_state.search_phone}'，找到 {len(patients)} 个患者")

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
        
        st.markdown("**健康信息**")
        medical_history = st.text_area("既往病史", placeholder="如：高血压、糖尿病、心脏病等（没有填'无'）")
        allergy_history = st.text_area("过敏史", placeholder="如：青霉素过敏、磺胺类过敏等（没有填'无'）")

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
                    "medical_history": medical_history if medical_history else "无",
                    "allergy_history": allergy_history if allergy_history else "无"
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
    
    # 创建 (ID, 姓名) 映射列表，用于下拉框显示
    patient_options = [(p["id"], f"{p['name']} (ID: {p['id']})") for p in patients]
    
    selected_option = st.selectbox(
        "选择患者进行操作",
        options=patient_options,
        format_func=lambda x: x[1]  # 显示姓名和 ID
    )
    
    # 获取选中的患者 ID
    selected_id = selected_option[0] if selected_option else None

    if selected_id:
        patient = next((p for p in patients if p["id"] == selected_id), None)
        
        if patient:
            # 显示详情 - 中文字段名
            with st.expander("📄 患者详情"):
                # 中文字段映射
                field_names = {
                    "id": "患者 ID",
                    "openid": "微信标识",
                    "name": "姓名",
                    "gender": "性别",
                    "age": "年龄",
                    "phone": "手机号",
                    "medical_history": "既往病史",
                    "allergy_history": "过敏史",
                    "created_at": "注册时间",
                    "updated_at": "最后更新"
                }
                
                for key, value in patient.items():
                    cn_name = field_names.get(key, key)
                    # 特殊处理空值
                    if value is None or value == "":
                        value = "未填写"
                    # 特殊处理性别
                    elif key == "gender":
                        value = "男" if value == "男" else "女" if value == "女" else "未填写"
                    # 格式化时间字段
                    elif key in ["created_at", "updated_at"]:
                        if value:
                            value = str(value)[:19]  # 去掉毫秒
                    
                    st.write(f"**{cn_name}**: {value}")
            
            # 编辑按钮
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ 编辑", use_container_width=True):
                    st.session_state.edit_patient_id = selected_id
                    st.rerun()
            with col2:
                # 检查是否正在删除这个项目
                deleting_id = st.session_state.get("deleting_patient_id")
                if deleting_id == selected_id:
                    # 显示确认按钮
                    col_confirm1, col_confirm2 = st.columns(2)
                    with col_confirm1:
                        if st.button("✅ 确认删除", key=f"confirm_{selected_id}", type="primary", use_container_width=True):
                            try:
                                client.delete_patient(selected_id)
                                st.success("删除成功！")
                                st.session_state.deleting_patient_id = None
                                st.rerun()
                            except Exception as e:
                                st.error(f"删除失败：{str(e)}")
                    with col_confirm2:
                        if st.button("❌ 取消", key=f"cancel_{selected_id}", use_container_width=True):
                            st.session_state.deleting_patient_id = None
                            st.rerun()
                else:
                    if st.button("🗑️ 删除", use_container_width=True):
                        st.session_state.deleting_patient_id = selected_id
                        st.rerun()

    # 编辑患者表单（在有患者数据时显示）
    if st.session_state.get("edit_patient_id"):
        patient_id = st.session_state.edit_patient_id
        patient = client.get_patient(patient_id)

        with st.form("edit_patient_form"):
            st.subheader(f"✏️ 编辑患者 (ID: {patient_id})")

            name = st.text_input("姓名", value=patient.get("name", ""))
            gender = st.selectbox("性别", ["男", "女"], index=0 if patient.get("gender") == "男" else 1)
            age = st.number_input("年龄", min_value=1, max_value=150, value=patient.get("age", 30))
            phone = st.text_input("手机号", value=patient.get("phone", ""))

            st.markdown("**健康信息**")
            medical_history = st.text_area(
                "既往病史",
                value=patient.get("medical_history", "") if patient.get("medical_history") != "无" else "",
                placeholder="如：高血压、糖尿病、心脏病等"
            )
            allergy_history = st.text_area(
                "过敏史",
                value=patient.get("allergy_history", "") if patient.get("allergy_history") != "无" else "",
                placeholder="如：青霉素过敏、磺胺类过敏等"
            )

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
                        "medical_history": medical_history if medical_history else "无",
                        "allergy_history": allergy_history if allergy_history else "无"
                    }
                    client.update_patient(patient_id, data)
                    st.success("更新成功！")
                    st.session_state.edit_patient_id = None
                    st.rerun()
                except Exception as e:
                    st.error(f"更新失败：{str(e)}")

else:
    # 患者列表为空时显示提示
    st.info("📭 暂无患者数据，点击上方'新增患者'按钮添加")
    if st.button("➕ 现在添加"):
        st.session_state.show_add_form = True
        st.rerun()
