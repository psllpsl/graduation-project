"""
对话监管页面
查看 AI 对话记录，支持人工干预
"""
import streamlit as st
from utils.auth import require_login, get_token
from utils.api_client import APIClient
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="对话监管 - 牙科修复复诊管理系统",
    page_icon="💬",
    layout="wide"
)

# 要求登录
require_login()

# 获取 Token 并创建客户端
token = get_token()
if not token:
    st.error("未获取到 Token，请重新登录")
    st.stop()

client = APIClient(token=token)

# 页面标题和刷新按钮
col_title, col_refresh = st.columns([5, 1])

with col_title:
    st.title("💬 对话监管")
    st.markdown("查看 AI 对话记录，必要时进行人工干预")

with col_refresh:
    if st.button("🔄 刷新", use_container_width=True, help="获取最新对话数据"):
        st.rerun()

st.divider()

# 侧边栏筛选
with st.sidebar:
    st.subheader("🔍 筛选条件")

    # 获取患者列表
    try:
        patients_result = client.get_patients(page=1, page_size=1000)
        if isinstance(patients_result, list):
            patients = patients_result
        else:
            patients = patients_result.get("items", []) if isinstance(patients_result, dict) else []
        patient_options = {"全部": None}
        patient_options.update({f"{p['name']} (ID: {p['id']})": p["id"] for p in patients})
    except Exception:
        patient_options = {"全部": None}

    selected_patient = st.selectbox("选择患者", options=list(patient_options.keys()))

    if st.button("应用筛选", use_container_width=True):
        st.rerun()

# 获取对话列表 - 加载所有数据（按时间正序排列）
patient_id = patient_options.get(selected_patient)

with st.spinner("加载对话记录..."):
    try:
        # 获取所有对话（page_size=1000）
        result = client.get_dialogues(page=1, page_size=1000, patient_id=patient_id)
        # 后端返回的是列表
        if isinstance(result, list):
            dialogues = result
        else:
            dialogues = result.get("items", []) if isinstance(result, dict) else []
        
        # 按时间正序排列（从旧到新）
        dialogues.sort(key=lambda x: x.get("created_at", ""))
        
    except Exception as e:
        st.error(f"加载失败：{str(e)}")
        st.info("提示：如果这是第一次使用，可能还没有对话记录")
        dialogues = []

# 统计信息
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("总对话数", len(dialogues))

with col2:
    # 统计待人工干预（已标记但没有处理）
    pending_count = sum(1 for d in dialogues if d.get("is_handover"))
    st.metric("待人工干预", pending_count)

with col3:
    if dialogues:
        unique_sessions = len(set(d.get("session_id") for d in dialogues))
        st.metric("会话数", unique_sessions)
    else:
        st.metric("会话数", 0)

st.divider()

# 对话列表 - 按会话分组显示
if dialogues:
    st.subheader(f"📋 对话记录 ({len(dialogues)} 条)")

    # 按会话分组
    sessions = {}
    for dialogue in dialogues:
        session_id = dialogue.get("session_id", "unknown")
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append(dialogue)

    # 显示每个会话（带删除确认）
    # 按会话倒序排列（最新的会话在上面）
    for session_id, session_dialogues in reversed(list(sessions.items())):
        # 检查该会话是否有已接管的对话
        has_handover = any(d.get("is_handover") for d in session_dialogues)
        
        # 如果正在删除这个会话，默认展开
        is_deleting = st.session_state.get("delete_session_id") == session_id
        
        # 会话折叠框
        with st.expander(
            f"💬 会话 {session_id[:8]}... - {len(session_dialogues)} 条对话 "
            f"{'✅ 已接管' if has_handover else ''}",
            expanded=is_deleting  # 删除时保持展开
        ):
            # 显示该会话的所有对话（正序：从旧到新）
            for dialogue in session_dialogues:
                st.markdown(f"**🕐 时间**: {dialogue.get('created_at', '未知时间')}")
                
                col_user, col_ai = st.columns(2)
                
                with col_user:
                    st.markdown("**🧑 用户消息：**")
                    st.info(dialogue.get("user_message", "无"))
                
                with col_ai:
                    st.markdown("**🤖 AI 回复：**")
                    st.success(dialogue.get("ai_response", "无"))
                
                st.divider()
            
            # 会话级别的操作按钮
            st.markdown("**🔧 会话操作**")
            col1, col2 = st.columns(2)
            
            with col1:
                if has_handover:
                    # 已接管，显示取消按钮
                    if st.button("✅ 取消接管", key=f"cancel_session_{session_id}", type="primary", use_container_width=True):
                        # 取消该会话所有对话的接管状态
                        for d in session_dialogues:
                            try:
                                client.handover_dialogue(d['id'], "取消人工接管")
                            except Exception:
                                pass
                        st.success("已取消接管")
                        st.rerun()
                else:
                    # 未接管，显示接管按钮
                    if st.button("👤 接管此会话", key=f"handover_session_{session_id}", use_container_width=True):
                        st.session_state.handover_session_id = session_id
                        st.session_state.handover_session_dialogues = session_dialogues
                        st.rerun()
            
            with col2:
                # 删除按钮 - 设置 session_state 并刷新
                if st.button("🗑️ 删除此会话", key=f"delete_btn_{session_id}", type="secondary", use_container_width=True):
                    st.session_state.delete_session_id = session_id
                    st.session_state.delete_session_dialogues = session_dialogues
                    st.rerun()
            
            # 如果正在删除，显示确认表单（在操作按钮下方）
            if is_deleting:
                st.divider()
                st.warning(f"⚠️ 确定要删除会话 **{session_id[:8]}...** 共 **{len(session_dialogues)}** 条对话吗？此操作不可恢复！")
                
                col_del1, col_del2 = st.columns(2)
                with col_del1:
                    if st.button("✅ 确认删除", key=f"confirm_delete_{session_id}", type="primary", use_container_width=True):
                        success_count = 0
                        error_count = 0
                        
                        # 删除该会话所有对话
                        for d in session_dialogues:
                            dialogue_id = d.get('id')
                            try:
                                result = client._request("DELETE", f"{client.BASE_URL}/dialogues/{dialogue_id}")
                                success_count += 1
                            except Exception as e:
                                error_count += 1
                                # 忽略 204 响应的解析错误
                                if "Expecting value" not in str(e):
                                    st.error(f"删除对话 {dialogue_id} 失败：{str(e)}")
                        
                        if success_count > 0:
                            st.success(f"✅ 成功删除 {success_count} 条对话")
                        
                        st.session_state.delete_session_id = None
                        st.session_state.delete_session_dialogues = None
                        st.rerun()
                
                with col_del2:
                    if st.button("❌ 取消", key=f"cancel_delete_{session_id}", use_container_width=True):
                        st.session_state.delete_session_id = None
                        st.rerun()

    # 接管会话表单
    if st.session_state.get("handover_session_id"):
        session_id = st.session_state.handover_session_id

        with st.form(f"handover_form_session_{session_id}"):
            st.subheader("👤 接管会话")
            st.info(f"将接管会话 {session_id[:8]}... 共 {len(st.session_state.handover_session_dialogues)} 条对话")
            reason = st.text_area("接管原因", placeholder="说明为什么需要人工接管")

            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("提交", use_container_width=True)
            with col2:
                if st.form_submit_button("取消", use_container_width=True):
                    st.session_state.handover_session_id = None
                    st.session_state.handover_session_dialogues = None
                    st.rerun()

            if submit:
                try:
                    # 标记该会话所有对话为接管状态
                    for d in st.session_state.handover_session_dialogues:
                        try:
                            client.handover_dialogue(d['id'], reason)
                        except Exception:
                            pass
                    st.success("接管成功！")
                    st.session_state.handover_session_id = None
                    st.session_state.handover_session_dialogues = None
                    st.rerun()
                except Exception as e:
                    st.error(f"接管失败：{str(e)}")

else:
    st.info("暂无对话记录")
