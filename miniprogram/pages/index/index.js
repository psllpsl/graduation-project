// pages/index/index.js - 对话主界面逻辑
const app = getApp()
const { dialogueApi } = require('../../utils/api')

Page({
  data: {
    messages: [],
    inputValue: '',
    canSend: false,
    isLoading: false,
    currentTime: '',
    currentSessionId: '',
    quickQuestions: [
      '种植牙术后多久能吃饭？',
      '烤瓷牙能用多久？',
      '活动义齿怎么清洗？',
      '复诊前要注意什么？',
      '术后疼痛正常吗？'
    ]
  },

  onLoad(options) {
    // 获取当前时间
    this.setCurrentTime()
    
    // 加载会话历史
    this.loadSessionHistory()
  },

  onShow() {
    // 页面显示时，检查登录状态
    if (!app.globalData.token) {
      wx.showModal({
        title: '提示',
        content: '请先登录',
        showCancel: false,
        success: () => {
          wx.switchTab({
            url: '/pages/profile/profile'
          })
        }
      })
      return
    }

    // 检查 sessionId 是否变化（切换用户时）
    const currentSessionId = wx.getStorageSync('sessionId')
    if (currentSessionId && currentSessionId !== this.data.currentSessionId) {
      // 会话 ID 变化了，清空消息列表
      console.log('检测到会话切换，清空消息列表')
      this.setData({
        messages: [],
        currentSessionId: currentSessionId
      })
    }
  },

  // 设置当前时间
  setCurrentTime() {
    const now = new Date()
    const hours = now.getHours().toString().padStart(2, '0')
    const minutes = now.getMinutes().toString().padStart(2, '0')
    this.setData({
      currentTime: `${hours}:${minutes}`
    })
  },

  // 加载会话历史
  async loadSessionHistory() {
    const sessionId = wx.getStorageSync('sessionId')
    if (!sessionId) return

    try {
      const res = await dialogueApi.getSessionHistory(sessionId)
      if (res && res.length > 0) {
        const messages = res.map(item => ({
          id: item.id,
          content: item.user_message,
          isUser: true,
          time: this.formatTime(item.created_at)
        }, {
          id: item.id + '_reply',
          content: item.ai_response,
          isUser: false,
          time: this.formatTime(item.created_at)
        })).flat()
        
        this.setData({ messages })
        this.scrollToBottom()
      }
    } catch (err) {
      console.error('加载会话历史失败:', err)
    }
  },

  // 格式化时间
  formatTime(timeStr) {
    const date = new Date(timeStr)
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  },

  // 输入框输入
  onInput(e) {
    const value = e.detail.value
    const hasValue = value && value.trim().length > 0
    console.log('输入内容:', value, 'canSend:', hasValue)
    this.setData({
      inputValue: value,
      canSend: hasValue
    })
  },

  // 发送消息
  async onSend() {
    const { inputValue, messages, isLoading, canSend, lastMessage } = this.data

    // 检查输入和加载状态
    if (!inputValue || !inputValue.trim() || isLoading || !canSend) {
      console.log('无法发送：inputValue=', inputValue, 'isLoading=', isLoading, 'canSend=', canSend)
      return
    }

    console.log('开始发送消息:', inputValue.trim())

    // 立即清空输入框（防止残留）
    this.setData({
      inputValue: '',
      canSend: false,
      isLoading: true
    })

    // 添加用户消息
    const userMessage = {
      id: Date.now(),
      content: inputValue.trim(),
      isUser: true,
      time: this.getCurrentTime()
    }

    this.setData({
      messages: [...messages, userMessage]
    })
    this.scrollToBottom()

    // 调用 AI 接口
    try {
      const sessionId = wx.getStorageSync('sessionId') || app.globalData.sessionId
      const patientId = wx.getStorageSync('patientId')

      if (!patientId) {
        throw new Error('请先完善个人信息')
      }

      const res = await dialogueApi.sendMessage({
        patient_id: patientId,
        session_id: sessionId,
        user_message: inputValue.trim(),
        message_type: 'consultation'
      })

      // 添加 AI 回复
      const aiMessage = {
        id: Date.now() + 1,
        content: res.ai_response || '抱歉，我暂时无法回答您的问题，请稍后再试。',
        isUser: false,
        time: this.getCurrentTime()
      }

      this.setData({
        messages: [...this.data.messages, aiMessage],
        isLoading: false
      })
      // AI 回复后自动滚动到底部，确保用户能看到完整回复
      setTimeout(() => {
        this.scrollToBottom()
      }, 100)

    } catch (err) {
      console.error('发送消息失败:', err)

      // 添加错误提示
      const errorMessage = {
        id: Date.now() + 1,
        content: '消息发送失败，请稍后重试',
        isUser: false,
        time: this.getCurrentTime()
      }

      this.setData({
        messages: [...this.data.messages, errorMessage],
        isLoading: false
      })
      // 错误时也滚动到底部
      setTimeout(() => {
        this.scrollToBottom()
      }, 100)
    }
  },

  // 快捷问题
  onQuickQuestion(e) {
    const question = e.currentTarget.dataset.question
    // 设置输入值和 canSend
    this.setData({
      inputValue: question,
      canSend: true
    })
    // 然后发送
    this.onSend()
  },

  // 滚动到底部
  scrollToBottom() {
    const { messages } = this.data
    if (messages.length > 0) {
      this.setData({
        scrollToView: `msg-${messages.length - 1}`
      })
    }
  },

  // 获取当前时间
  getCurrentTime() {
    const now = new Date()
    const hours = now.getHours().toString().padStart(2, '0')
    const minutes = now.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  },

  onPullDownRefresh() {
    this.loadSessionHistory()
    wx.stopPullDownRefresh()
  }
})
