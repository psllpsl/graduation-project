// pages/appointment/appointment.js - 复诊计划页面逻辑
const app = getApp()
const { appointmentApi } = require('../../utils/api')

Page({
  data: {
    appointments: [],
    loading: false,
    upcomingCount: 0,
    completedCount: 0,
    totalCount: 0
  },

  onLoad(options) {
    this.loadAppointments()
  },

  onShow() {
    // 每次显示时刷新数据
    if (app.globalData.token) {
      this.loadAppointments()
    }
  },

  onPullDownRefresh() {
    this.loadAppointments()
    wx.stopPullDownRefresh()
  },

  // 加载复诊计划
  async loadAppointments() {
    this.setData({ loading: true })

    try {
      // 使用新的 API：从 Token 中自动获取 patient_id
      const res = await appointmentApi.getMyList()
      
      // 处理数据
      const appointments = (res || []).map(item => ({
        ...item,
        appointment_date: this.formatDateTime(item.appointment_date),
        reminder_sent: item.reminder_sent ? true : false
      }))

      // 统计数据
      const upcomingCount = appointments.filter(item => item.status === 'pending').length
      const completedCount = appointments.filter(item => item.status === 'completed').length
      const totalCount = appointments.length

      this.setData({
        appointments,
        upcomingCount,
        completedCount,
        totalCount,
        loading: false
      })
    } catch (err) {
      console.error('加载复诊计划失败:', err)
      this.setData({
        loading: false,
        appointments: [],
        upcomingCount: 0,
        completedCount: 0,
        totalCount: 0
      })
    }
  },

  // 格式化日期时间
  formatDateTime(dateTime) {
    if (!dateTime) return ''
    const date = new Date(dateTime)
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${month}月${day}日 ${hours}:${minutes}`
  },

  // 点击复诊卡片
  onAppointmentTap(e) {
    const item = e.currentTarget.dataset.item
    wx.showModal({
      title: item.appointment_type,
      content: `复诊时间：${item.appointment_date}\n${item.notes ? '备注：' + item.notes : ''}`,
      showCancel: false
    })
  },

  // 确认复诊
  async onConfirm(e) {
    const id = e.currentTarget.dataset.id
    
    wx.showModal({
      title: '确认复诊',
      content: '确认已完成本次复诊吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await appointmentApi.updateStatus(id, 'completed')
            wx.showToast({
              title: '已确认',
              icon: 'success'
            })
            this.loadAppointments()
          } catch (err) {
            console.error('确认复诊失败:', err)
          }
        }
      }
    })
  },

  // 取消复诊
  async onCancel(e) {
    const id = e.currentTarget.dataset.id
    
    wx.showModal({
      title: '取消复诊',
      content: '确定要取消本次复诊吗？',
      confirmText: '取消',
      confirmColor: '#FF5252',
      success: async (res) => {
        if (res.confirm) {
          try {
            await appointmentApi.updateStatus(id, 'cancelled')
            wx.showToast({
              title: '已取消',
              icon: 'success'
            })
            this.loadAppointments()
          } catch (err) {
            console.error('取消复诊失败:', err)
          }
        }
      }
    })
  }
})
