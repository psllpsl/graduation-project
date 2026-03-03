// app.js
App({
  onLaunch() {
    // 小程序启动时执行
    console.log('牙科修复复诊助手小程序启动')
    
    // 检查登录状态
    this.checkLogin()
  },

  globalData: {
    userInfo: null,
    openid: null,
    sessionKey: null,
    token: null,
    // 后端 API 地址
    // 模拟器使用：http://localhost:8000/api
    // 真机调试使用：http://你的电脑 IP:8000/api
    // 当前配置：10.14.168.76（请根据实际网络环境修改）
    baseUrl: 'http://10.14.168.76:8000/api',
    // 会话 ID（用于多轮对话）
    sessionId: null
  },

  // 检查登录状态
  checkLogin() {
    const token = wx.getStorageSync('token')
    const userInfo = wx.getStorageSync('userInfo')
    
    if (token && userInfo) {
      this.globalData.token = token
      this.globalData.userInfo = userInfo
      console.log('用户已登录')
    } else {
      console.log('用户未登录，需要授权')
    }
  },

  // 微信登录
  wxLogin() {
    return new Promise((resolve, reject) => {
      wx.login({
        success: (res) => {
          if (res.code) {
            // 将 code 发送到后端，换取 openid 和 session
            wx.request({
              url: `${this.globalData.baseUrl}/auth/wx-login`,
              method: 'POST',
              data: {
                code: res.code
              },
              success: (result) => {
                if (result.statusCode === 200 && result.data.access_token) {
                  // 清除旧的会话数据（切换用户时很重要）
                  wx.removeStorageSync('sessionId')
                  
                  // 保存 token 和用户信息
                  wx.setStorageSync('token', result.data.access_token)
                  wx.setStorageSync('userInfo', result.data.user)
                  wx.setStorageSync('openid', result.data.openid)
                  // 保存 patientId（用于后续 API 调用）
                  if (result.data.user && result.data.user.id) {
                    wx.setStorageSync('patientId', result.data.user.id)
                  }

                  this.globalData.token = result.data.access_token
                  this.globalData.userInfo = result.data.user
                  this.globalData.openid = result.data.openid
                  if (result.data.user && result.data.user.id) {
                    this.globalData.patientId = result.data.user.id
                  }

                  // 生成新的会话 ID
                  const sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
                  this.globalData.sessionId = sessionId
                  wx.setStorageSync('sessionId', sessionId)

                  resolve(result.data)
                } else {
                  reject(result.data)
                }
              },
              fail: (err) => {
                reject(err)
              }
            })
          } else {
            reject(new Error('微信登录失败'))
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  }
})
