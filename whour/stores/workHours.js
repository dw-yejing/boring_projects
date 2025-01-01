import { defineStore } from 'pinia'
import { db } from '@/utils/db.js'

export const useWorkHoursStore = defineStore('workHours', {
    state: () => ({
        monthRecords: [],
        currentMonth: formatYearMonth(new Date())
    }),

    getters: {
        sortedRecords: (state) => {
            return [...state.monthRecords].sort((a, b) => {
                return new Date(a.date) - new Date(b.date)
            })
        },
        
        totalHours: (state) => {
            return state.monthRecords.reduce((total, record) => {
                return total + (Number(record.hours) || 0)
            }, 0).toFixed(1)
        }
    },

    actions: {
        // 初始化数据库
        async init() {
            try {
                await db.init()
            } catch (e) {
                console.error('数据库初始化失败:', e)
            }
        },

        // 获取指定日期的记录
        async getRecord(date) {
            try {
                return await db.getRecord(date)
            } catch (e) {
                console.error('获取记录失败:', e)
                return null
            }
        },

        // 加载月度数据
        async loadMonthData(yearMonth = null) {
            if (yearMonth) {
                this.currentMonth = yearMonth
            }
            try {
                const records = await db.getMonthRecords(this.currentMonth)
				
                this.monthRecords = records.map(record => ({
                    ...record,
                    hours: Number(record.hours)
                }))
            } catch (e) {
                console.error('加载数据失败:', JSON.stringify(e))
                this.monthRecords = []
            }
        },

        // 保存工时记录
        async saveRecord(date, hours, content) {
            try {
                const existingRecord = await db.getRecord(date)
                if (existingRecord) {
                    await db.updateRecord(date, hours, content)
                } else {
                    await db.saveRecord(date, hours, content)
                }
                // 保存后刷新当月数据
                await this.loadMonthData()
                return true
            } catch (e) {
                console.error('保存失败:', e)
                return false
            }
        }
    }
})

function formatYearMonth(date) {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    return `${year}-${month}`
} 