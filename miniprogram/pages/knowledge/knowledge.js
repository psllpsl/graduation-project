// pages/knowledge/knowledge.js - 知识库页面逻辑
const { knowledgeApi } = require('../../utils/api')

Page({
  data: {
    knowledgeList: [],
    categories: [],
    currentCategory: '',
    searchValue: '',
    loading: false,
    
    // 分页相关
    page: 1,
    pageSize: 10,
    total: 0,
    hasMore: true,
    loadingMore: false
  },

  onLoad(options) {
    this.loadCategories()
    this.loadKnowledge(true) // 重置加载
  },

  onPullDownRefresh() {
    this.loadKnowledge(true) // 重置加载
    wx.stopPullDownRefresh()
  },

  onReachBottom() {
    // 触底加载更多
    if (!this.data.loadingMore && this.data.hasMore) {
      this.loadMore()
    }
  },

  // 加载分类列表
  async loadCategories() {
    try {
      const res = await knowledgeApi.getCategories()
      this.setData({
        categories: res || []
      })
    } catch (err) {
      console.error('加载分类失败:', err)
    }
  },

  // 加载知识列表
  async loadKnowledge(reset = false) {
    const { page, pageSize, currentCategory } = this.data
    
    // 重置时清空列表
    if (reset) {
      this.setData({
        knowledgeList: [],
        page: 1,
        hasMore: true
      })
    }
    
    this.setData({ 
      loading: true,
      loadingMore: false
    })

    try {
      const params = {
        skip: (this.data.page - 1) * pageSize,
        limit: pageSize
      }
      
      if (currentCategory) {
        params.category = currentCategory
      }

      const res = await knowledgeApi.getList(params)
      
      // 后端返回的是数组，需要判断是否还有更多数据
      const newList = reset ? (res || []) : [...this.data.knowledgeList, ...(res || [])]
      const hasMore = res.length === pageSize
      
      this.setData({
        knowledgeList: newList,
        loading: false,
        hasMore: hasMore,
        page: hasMore ? this.data.page + 1 : this.data.page
      })
    } catch (err) {
      console.error('加载知识失败:', err)
      this.setData({
        loading: false,
        loadingMore: false,
        knowledgeList: reset ? [] : this.data.knowledgeList
      })
    }
  },

  // 加载更多
  loadMore() {
    if (!this.data.hasMore) return
    
    this.setData({ loadingMore: true })
    this.loadKnowledge(false)
  },

  // 搜索知识
  async onSearch(e) {
    const query = e.detail.value || this.data.searchValue

    if (!query.trim()) {
      this.loadKnowledge(true)
      return
    }

    this.setData({ 
      loading: true,
      knowledgeList: []
    })

    try {
      const res = await knowledgeApi.search(query)
      this.setData({
        knowledgeList: res || [],
        loading: false
      })
    } catch (err) {
      console.error('搜索失败:', err)
      this.setData({
        loading: false,
        knowledgeList: []
      })
    }
  },

  // 输入搜索词
  onSearchInput(e) {
    this.setData({
      searchValue: e.detail.value
    })
  },

  // 清除搜索
  onClear() {
    this.setData({
      searchValue: '',
      knowledgeList: []
    })
    this.loadKnowledge(true)
  },

  // 切换分类
  onCategoryChange(e) {
    const category = e.currentTarget.dataset.category
    this.setData({
      currentCategory: category,
      knowledgeList: [],
      page: 1,
      hasMore: true
    })
    this.loadKnowledge(true)
  },

  // 点击知识卡片
  onKnowledgeTap(e) {
    const item = e.currentTarget.dataset.item

    wx.showModal({
      title: item.title,
      content: item.content,
      showCancel: false,
      confirmText: '知道了',
      confirmColor: '#4A90D9'
    })
  }
})
