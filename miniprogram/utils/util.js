// utils/util.js - 工具函数

/**
 * 格式化时间
 * @param {Date|string} date - 日期对象或字符串
 * @param {string} format - 格式模板
 * @returns {string}
 */
export function formatTime(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return ''
  
  const d = typeof date === 'string' ? new Date(date) : date
  
  const year = d.getFullYear()
  const month = (d.getMonth() + 1).toString().padStart(2, '0')
  const day = d.getDate().toString().padStart(2, '0')
  const hours = d.getHours().toString().padStart(2, '0')
  const minutes = d.getMinutes().toString().padStart(2, '0')
  const seconds = d.getSeconds().toString().padStart(2, '0')
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 格式化相对时间
 * @param {Date|string} date - 日期对象或字符串
 * @returns {string}
 */
export function formatRelativeTime(date) {
  if (!date) return ''
  
  const d = typeof date === 'string' ? new Date(date) : date
  const now = new Date()
  const diff = now - d
  
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) {
    return `${days}天前`
  } else if (hours > 0) {
    return `${hours}小时前`
  } else if (minutes > 0) {
    return `${minutes}分钟前`
  } else {
    return '刚刚'
  }
}

/**
 * 防抖函数
 * @param {Function} fn - 要执行的函数
 * @param {number} delay - 延迟时间（毫秒）
 * @returns {Function}
 */
export function debounce(fn, delay = 300) {
  let timer = null
  return function(...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

/**
 * 节流函数
 * @param {Function} fn - 要执行的函数
 * @param {number} delay - 延迟时间（毫秒）
 * @returns {Function}
 */
export function throttle(fn, delay = 300) {
  let lastTime = 0
  return function(...args) {
    const now = Date.now()
    if (now - lastTime >= delay) {
      fn.apply(this, args)
      lastTime = now
    }
  }
}

/**
 * 验证手机号
 * @param {string} phone - 手机号
 * @returns {boolean}
 */
export function validatePhone(phone) {
  return /^1[3-9]\d{9}$/.test(phone)
}

/**
 * 验证身份证号
 * @param {string} idCard - 身份证号
 * @returns {boolean}
 */
export function validateIdCard(idCard) {
  return /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(idCard)
}

/**
 * 生成随机字符串
 * @param {number} length - 长度
 * @returns {string}
 */
export function randomString(length = 16) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * 生成会话 ID
 * @returns {string}
 */
export function generateSessionId() {
  return 'sess_' + Date.now() + '_' + randomString(9)
}

/**
 * 显示加载提示
 * @param {string} title - 提示文字
 */
export function showLoading(title = '加载中...') {
  wx.showLoading({
    title,
    mask: true
  })
}

/**
 * 隐藏加载提示
 */
export function hideLoading() {
  wx.hideLoading()
}

/**
 * 显示成功提示
 * @param {string} title - 提示文字
 */
export function showSuccess(title = '操作成功') {
  wx.showToast({
    title,
    icon: 'success',
    duration: 2000
  })
}

/**
 * 显示错误提示
 * @param {string} title - 提示文字
 */
export function showError(title = '操作失败') {
  wx.showToast({
    title,
    icon: 'none',
    duration: 2000
  })
}

/**
 * 复制到剪贴板
 * @param {string} text - 要复制的文字
 */
export function copyToClipboard(text) {
  wx.setClipboardData({
    data: text,
    success: () => {
      wx.showToast({
        title: '已复制',
        icon: 'success'
      })
    }
  })
}

/**
 * 拨打电话
 * @param {string} phoneNumber - 电话号码
 */
export function makePhoneCall(phoneNumber) {
  wx.makePhoneCall({
    phoneNumber,
    fail: () => {
      wx.showToast({
        title: '拨打失败',
        icon: 'none'
      })
    }
  })
}

export default {
  formatTime,
  formatRelativeTime,
  debounce,
  throttle,
  validatePhone,
  validateIdCard,
  randomString,
  generateSessionId,
  showLoading,
  hideLoading,
  showSuccess,
  showError,
  copyToClipboard,
  makePhoneCall
}
