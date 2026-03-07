"""
知识库管理页面
知识条目的增删改查
"""
import streamlit as st
from utils.auth import get_token, is_logged_in
from utils.api_client import APIClient

# 页面配置
st.set_page_config(
    page_title="知识库管理 - 牙科修复复诊管理系统",
    page_icon="📚",
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
    st.title("📚 知识库管理")
    st.markdown("管理牙科修复专业知识")

with col_refresh:
    if st.button("🔄 刷新", use_container_width=True, help="获取最新知识数据"):
        # 清除缓存数据
        if "knowledge_cache" in st.session_state:
            del st.session_state.knowledge_cache
        st.rerun()

st.divider()

# 获取分类列表
with st.spinner("加载分类..."):
    try:
        categories = client.get_knowledge_categories()
        if not isinstance(categories, list):
            categories = []
    except Exception:
        categories = []

# 获取知识列表
selected_category = st.selectbox("分类筛选", options=["全部"] + categories)

with st.spinner("加载知识列表..."):
    try:
        category_param = None if selected_category == "全部" else selected_category
        result = client.get_knowledge(page=1, page_size=100, category=category_param)
        # 后端返回的是列表
        if isinstance(result, list):
            knowledge_items = result
        else:
            knowledge_items = result.get("items", []) if isinstance(result, dict) else []
    except Exception as e:
        st.error(f"加载失败：{str(e)}")
        knowledge_items = []

# 操作按钮
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("➕ 新增知识", use_container_width=True):
        st.session_state.show_add_knowledge = True

# 新增知识表单
if st.session_state.get("show_add_knowledge"):
    with st.form("add_knowledge_form"):
        st.subheader("➕ 新增知识条目")
        
        category = st.selectbox("分类", options=categories if categories else ["其他"])
        title = st.text_input("标题")
        content = st.text_area("内容", height=200)
        keywords = st.text_input("关键词", placeholder="用逗号分隔多个关键词")
        source = st.text_input("来源", placeholder="如：《口腔修复学》第 8 版")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("保存", use_container_width=True)
        with col2:
            if st.form_submit_button("取消", use_container_width=True):
                st.session_state.show_add_knowledge = False
                st.rerun()
        
        if submit:
            try:
                data = {
                    "category": category,
                    "title": title,
                    "content": content,
                    "keywords": keywords,
                    "source": source
                }
                client.create_knowledge(data)
                st.success("添加成功！")
                st.session_state.show_add_knowledge = False
                st.rerun()
            except Exception as e:
                st.error(f"添加失败：{str(e)}")

# 知识列表
if knowledge_items:
    st.subheader(f"📋 知识列表 ({len(knowledge_items)} 条)")
    
    for item in knowledge_items:
        with st.expander(f"📄 {item.get('title', '无标题')} - {item.get('category', '未分类')}"):
            st.markdown(f"**关键词**: {item.get('keywords', '无')}")
            st.markdown(f"**来源**: {item.get('source', '未知')}")
            st.markdown("**内容：**")
            st.write(item.get("content", "无内容"))
            
            # 操作按钮
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ 编辑", key=f"edit_{item['id']}"):
                    st.session_state.edit_knowledge_id = item["id"]
                    st.rerun()
            with col2:
                # 检查是否正在删除这个项目
                deleting_id = st.session_state.get("deleting_knowledge_id")
                if deleting_id == item["id"]:
                    # 显示确认按钮
                    col_confirm1, col_confirm2 = st.columns(2)
                    with col_confirm1:
                        if st.button("✅ 确认", key=f"confirm_{item['id']}", type="primary", use_container_width=True):
                            try:
                                client.delete_knowledge(item["id"])
                                st.success("删除成功！")
                                st.session_state.deleting_knowledge_id = None
                                st.rerun()
                            except Exception as e:
                                # 删除可能返回 204 无响应，检查是否真的删除了
                                try:
                                    test_item = client.get_knowledge_item(item["id"])
                                    if test_item:
                                        st.error(f"删除失败：{str(e)}")
                                    else:
                                        st.success("删除成功！")
                                        st.session_state.deleting_knowledge_id = None
                                        st.rerun()
                                except Exception:
                                    # 404 表示已删除
                                    st.success("删除成功！")
                                    st.session_state.deleting_knowledge_id = None
                                    st.rerun()
                    with col_confirm2:
                        if st.button("❌ 取消", key=f"cancel_{item['id']}", use_container_width=True):
                            st.session_state.deleting_knowledge_id = None
                            st.rerun()
                else:
                    if st.button("🗑️ 删除", key=f"delete_{item['id']}", use_container_width=True):
                        st.session_state.deleting_knowledge_id = item["id"]
                        st.rerun()
    
    # 编辑知识表单
    if st.session_state.get("edit_knowledge_id"):
        knowledge_id = st.session_state.edit_knowledge_id
        item = client.get_knowledge_item(knowledge_id)
        
        with st.form(f"edit_knowledge_form_{knowledge_id}"):
            st.subheader(f"✏️ 编辑知识 (ID: {knowledge_id})")
            
            # 分类选择
            cat_options = categories if categories else ["其他"]
            current_cat = item.get("category", cat_options[0]) if cat_options else "其他"
            cat_index = cat_options.index(current_cat) if current_cat in cat_options else 0
            
            category = st.selectbox("分类", options=cat_options, index=cat_index)
            title = st.text_input("标题", value=item.get("title", ""))
            content = st.text_area("内容", value=item.get("content", ""), height=200)
            keywords = st.text_input("关键词", value=item.get("keywords", ""))
            source = st.text_input("来源", value=item.get("source", ""))
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("保存修改", use_container_width=True)
            with col2:
                if st.form_submit_button("取消", use_container_width=True):
                    st.session_state.edit_knowledge_id = None
                    st.rerun()
            
            if submit:
                try:
                    data = {
                        "category": category,
                        "title": title,
                        "content": content,
                        "keywords": keywords,
                        "source": source
                    }
                    client.update_knowledge(knowledge_id, data)
                    st.success("更新成功！")
                    st.session_state.edit_knowledge_id = None
                    st.rerun()
                except Exception as e:
                    st.error(f"更新失败：{str(e)}")

else:
    st.info("暂无知识条目")
