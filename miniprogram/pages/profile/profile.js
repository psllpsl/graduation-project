// pages/profile/profile.js - 个人中心页面逻辑
const app = getApp()
const { authApi, patientApi } = require('../../utils/api')

Page({
  data: {
    userInfo: null,
    openid: null,
    patientId: null
  },

  onLoad(options) {
    this.loadUserInfo()
  },

  onShow() {
    this.loadUserInfo()
  },

  // 加载用户信息
  loadUserInfo() {
    const userInfo = wx.getStorageSync('userInfo')
    const openid = wx.getStorageSync('openid')
    const patientId = wx.getStorageSync('patientId')

    this.setData({
      userInfo: userInfo || null,
      openid: openid || null,
      patientId: patientId || null
    })

    // 如果有 openid 但没有 patientId，尝试获取患者信息
    if (openid && !patientId) {
      this.fetchPatientInfo(openid)
    }
  },

  // 获取患者信息
  async fetchPatientInfo(openid) {
    try {
      const res = await patientApi.getByOpenid(openid)
      if (res && res.id) {
        wx.setStorageSync('patientId', res.id)
        this.setData({
          patientId: res.id,
          userInfo: {
            ...this.data.userInfo,
            name: res.name,
            phone: res.phone
          }
        })
      }
    } catch (err) {
      console.error('获取患者信息失败:', err)
    }
  },

  // 微信登录
  async onLogin() {
    wx.showLoading({
      title: '登录中...',
      mask: true
    })

    try {
      // 调用微信登录
      const loginRes = await app.wxLogin()
      
      wx.hideLoading()

      if (loginRes && loginRes.access_token) {
        wx.showToast({
          title: '登录成功',
          icon: 'success'
        })

        // 刷新页面
        this.loadUserInfo()
      }
    } catch (err) {
      console.error('登录失败:', err)
      wx.hideLoading()
      
      // 显示详细错误信息
      let errorMsg = '请稍后重试'
      if (err && err.errMsg) {
        if (err.errMsg.includes('timeout')) {
          errorMsg = '连接超时，请检查网络'
        } else if (err.errMsg.includes('fail')) {
          errorMsg = '网络请求失败'
        }
      }
      if (err && err.statusCode) {
        errorMsg = `服务器错误：${err.statusCode}`
      }
      
      wx.showModal({
        title: '登录失败',
        content: errorMsg,
        showCancel: false
      })
    }
  },

  // 个人信息
  onPatientInfo() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  },

  // 治疗记录
  onTreatmentRecords() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  },

  // 订阅消息提醒
  onSubscribeMessage() {
    // 请求订阅消息授权
    wx.requestSubscribeMessage({
      tmplIds: ['YOUR_TEMPLATE_ID'], // 替换为实际的模板 ID
      success: (res) => {
        if (res[Object.keys(res)[0]] === 'accept') {
          wx.showToast({
            title: '订阅成功',
            icon: 'success'
          })
        }
      },
      fail: (err) => {
        console.error('订阅失败:', err)
      }
    })
  },

  // 关于我们
  onAbout() {
    wx.showModal({
      title: '关于我们',
      content: '牙科修复复诊助手 v1.0.0\n\n为您提供 7×24 小时智能术后随访服务，包括复诊提醒、术后护理指导、常见问题解答等。\n\n开发团队：毕业设计项目组',
      showCancel: false,
      confirmColor: '#4A90D9'
    })
  },

  // 退出登录
  onLogout() {
    wx.showModal({
      title: '退出登录',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清除本地缓存
          wx.removeStorageSync('token')
          wx.removeStorageSync('userInfo')
          wx.removeStorageSync('openid')
          wx.removeStorageSync('patientId')
          wx.removeStorageSync('sessionId')
          
          // 清除全局状态
          app.globalData.token = null
          app.globalData.userInfo = null
          app.globalData.openid = null
          app.globalData.patientId = null
          app.globalData.sessionId = null
          
          wx.showToast({
            title: '已退出',
            icon: 'success'
          })
          
          // 刷新页面
          this.loadUserInfo()
        }
      }
    })
  }
})
