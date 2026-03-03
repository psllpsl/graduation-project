// utils/api.js - 网络请求封装

const app = getApp()

/**
 * 封装 request 请求
 * @param {Object} options - 请求配置
 * @returns {Promise}
 */
function request(options) {
  return new Promise((resolve, reject) => {
    const token = wx.getStorageSync('token')
    
    wx.request({
      url: options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
        ...options.header
      },
      timeout: options.timeout || 60000,
      success: (res) => {
        // HTTP 状态码判断
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // 未授权，先检查本地是否有 token
          const token = wx.getStorageSync('token')
          if (!token) {
            // 本来就没登录，不显示错误
            reject(new Error('未登录'))
            return
          }
          // 有 token 但返回 401，说明 token 失效了
          wx.showToast({
            title: '登录已过期',
            icon: 'none'
          })
          // 清除本地缓存
          wx.removeStorageSync('token')
          wx.removeStorageSync('userInfo')
          wx.removeStorageSync('patientId')
          // 跳转到登录页
          setTimeout(() => {
            wx.reLaunch({
              url: '/pages/profile/profile'
            })
          }, 1500)
          reject(new Error('未授权'))
        } else {
          // 其他错误
          const errorMsg = res.data.detail || res.data.message || '请求失败'
          wx.showToast({
            title: errorMsg,
            icon: 'none',
            duration: 2000
          })
          reject(res.data)
        }
      },
      fail: (err) => {
        console.error('请求失败:', err)
        wx.showToast({
          title: '网络错误，请稍后重试',
          icon: 'none',
          duration: 2000
        })
        reject(err)
      }
    })
  })
}

/**
 * GET 请求
 * @param {string} url - 请求地址
 * @param {object} data - 请求参数
 */
export function get(url, data = {}) {
  return request({ url, method: 'GET', data })
}

/**
 * POST 请求
 * @param {string} url - 请求地址
 * @param {object} data - 请求数据
 */
export function post(url, data = {}) {
  return request({ url, method: 'POST', data })
}

/**
 * PUT 请求
 * @param {string} url - 请求地址
 * @param {object} data - 请求数据
 */
export function put(url, data = {}) {
  return request({ url, method: 'PUT', data })
}

/**
 * DELETE 请求
 * @param {string} url - 请求地址
 * @param {object} data - 请求参数
 */
export function del(url, data = {}) {
  return request({ url, method: 'DELETE', data })
}

// ==================== API 接口封装 ====================

const baseUrl = app.globalData.baseUrl

/**
 * 用户认证相关 API
 */
export const authApi = {
  // 微信登录
  wxLogin: (code) => post(`${baseUrl}/auth/wx-login`, { code }),
  
  // 获取当前用户信息
  getCurrentUser: () => get(`${baseUrl}/auth/me`),
  
  // 退出登录
  logout: () => post(`${baseUrl}/auth/logout`)
}

/**
 * 患者相关 API
 */
export const patientApi = {
  // 获取患者信息
  getPatientInfo: (id) => get(`${baseUrl}/patients/${id}`),
  
  // 更新患者信息
  updatePatient: (id, data) => put(`${baseUrl}/patients/${id}`, data),
  
  // 按 openid 获取患者
  getByOpenid: (openid) => get(`${baseUrl}/patients/by-openid/${openid}`)
}

/**
 * 复诊计划相关 API
 */
export const appointmentApi = {
  // 获取我的复诊计划（从 Token 中提取 patient_id）
  getMyList: () => get(`${baseUrl}/appointments/patient/my`),
  
  // 获取复诊详情
  getDetail: (id) => get(`${baseUrl}/appointments/${id}`),
  
  // 更新复诊状态
  updateStatus: (id, status) => {
    return new Promise((resolve, reject) => {
      const token = wx.getStorageSync('token')
      wx.request({
        url: `${baseUrl}/appointments/${id}/status?status=${status}`,
        method: 'PATCH',
        header: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        success: resolve,
        fail: reject
      })
    })
  }
}

/**
 * 对话相关 API
 */
export const dialogueApi = {
  // 发送消息并获取 AI 回复（患者专用接口）
  sendMessage: (data) => post(`${baseUrl}/dialogues/chat`, data),
  
  // 获取会话历史
  getSessionHistory: (sessionId) => get(`${baseUrl}/dialogues/session/${sessionId}`),
  
  // 获取对话列表
  getList: (params) => get(`${baseUrl}/dialogues`, params)
}

/**
 * 知识库相关 API
 */
export const knowledgeApi = {
  // 获取知识列表
  getList: (params) => get(`${baseUrl}/knowledge`, params),
  
  // 获取知识详情
  getDetail: (id) => get(`${baseUrl}/knowledge/${id}`),
  
  // 搜索知识
  search: (query) => get(`${baseUrl}/knowledge/search/query`, { query }),
  
  // 获取分类列表
  getCategories: () => get(`${baseUrl}/knowledge/categories`)
}

/**
 * 统计相关 API
 */
export const statsApi = {
  // 获取概览统计
  getOverview: () => get(`${baseUrl}/stats/overview`),
  
  // 获取复诊依从性
  getCompliance: () => get(`${baseUrl}/stats/appointments/compliance`)
}

export default {
  request,
  get,
  post,
  put,
  del,
  authApi,
  patientApi,
  appointmentApi,
  dialogueApi,
  knowledgeApi,
  statsApi
}
