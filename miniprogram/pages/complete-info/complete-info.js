// pages/complete-info/complete-info.js - 首次登录完善信息页面逻辑
const app = getApp()
const { patientApi } = require('../../utils/api')

Page({
  data: {
    name: '',
    gender: '男',
    ageIndex: 0,
    ages: ['请选择年龄', ...Array.from({length: 100}, (_, i) => (i + 1) + '岁')],
    phone: '',
    medicalHistory: '',
    allergyHistory: '',
    canSubmit: false
  },

  onLoad() {
    // 页面加载时检查是否已登录
    const token = wx.getStorageSync('token')
    if (!token) {
      wx.reLaunch({ url: '/pages/profile/profile' })
    }
  },

  // 输入框输入
  onInput(e) {
    const field = e.currentTarget.dataset.field
    const value = e.detail.value
    
    this.setData({ [field]: value }, () => {
      this.checkCanSubmit()
    })
  },

  // 年龄选择器变化
  onAgeChange(e) {
    this.setData({
      ageIndex: parseInt(e.detail.value)
    }, () => {
      this.checkCanSubmit()
    })
  },

  // 检查是否可以提交
  checkCanSubmit() {
    const { name, ageIndex, phone } = this.data
    const canSubmit = name.trim() && ageIndex > 0 && phone.trim() && phone.length === 11
    this.setData({ canSubmit })
  },

  // 提交信息
  async onSubmit() {
    if (!this.data.canSubmit) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      })
      return
    }

    wx.showLoading({
      title: '提交中...',
      mask: true
    })

    try {
      const token = wx.getStorageSync('token')
      const patientId = wx.getStorageSync('patientId')
      
      // 准备提交数据
      const submitData = {
        name: this.data.name.trim(),
        gender: this.data.gender,
        age: this.data.ageIndex,
        phone: this.data.phone.trim(),
        medical_history: this.data.medicalHistory.trim() || null,
        allergy_history: this.data.allergyHistory.trim() || null
      }

      // 调用更新接口
      await this.completeApi(token, patientId, submitData)

      wx.hideLoading()

      wx.showToast({
        title: '提交成功',
        icon: 'success',
        duration: 2000
      })

      // 更新本地缓存
      const userInfo = wx.getStorageSync('userInfo')
      if (userInfo) {
        userInfo.name = submitData.name
        userInfo.phone = submitData.phone
        wx.setStorageSync('userInfo', userInfo)
      }

      // 延迟跳转到首页
      setTimeout(() => {
        wx.reLaunch({ url: '/pages/index/index' })
      }, 1500)

    } catch (err) {
      console.error('提交信息失败:', err)
      wx.hideLoading()

      let errorMsg = '提交失败，请稍后重试'
      if (err && err.errMsg) {
        if (err.errMsg.includes('timeout')) {
          errorMsg = '网络超时，请检查网络'
        }
      }
      if (err && err.statusCode) {
        errorMsg = `服务器错误：${err.statusCode}`
      }

      wx.showModal({
        title: '提交失败',
        content: errorMsg,
        showCancel: false
      })
    }
  },

  // 完善信息 API
  completeApi(token, patientId, data) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${app.globalData.baseUrl}/patients/complete`,
        method: 'POST',
        data: data,
        header: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        success: resolve,
        fail: reject
      })
    })
  }
})
