// pages/knowledge/knowledge.js - 知识库页面逻辑
const { knowledgeApi } = require('../../utils/api')

Page({
  data: {
    knowledgeList: [],
    categories: [],
    currentCategory: '',
    searchValue: '',
    loading: false
  },

  onLoad(options) {
    this.loadCategories()
    this.loadKnowledge()
  },

  onPullDownRefresh() {
    this.loadKnowledge()
    wx.stopPullDownRefresh()
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
  async loadKnowledge() {
    this.setData({ loading: true })

    try {
      const params = {}
      if (this.data.currentCategory) {
        params.category = this.data.currentCategory
      }

      const res = await knowledgeApi.getList(params)
      this.setData({
        knowledgeList: res || [],
        loading: false
      })
    } catch (err) {
      console.error('加载知识失败:', err)
      this.setData({
        loading: false,
        knowledgeList: []
      })
    }
  },

  // 搜索知识
  async onSearch(e) {
    const query = e.detail.value || this.data.searchValue
    
    if (!query.trim()) {
      this.loadKnowledge()
      return
    }

    this.setData({ loading: true })

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
    this.loadKnowledge()
  },

  // 切换分类
  onCategoryChange(e) {
    const category = e.currentTarget.dataset.category
    this.setData({
      currentCategory: category
    })
    this.loadKnowledge()
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
