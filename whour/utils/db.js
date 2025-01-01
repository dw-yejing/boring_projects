// 数据库操作服务
const DB_NAME = 'workhours.db'
const STORAGE_KEY = 'work_records'

// 判断是否在H5环境
const isH5 = process.env.UNI_PLATFORM === 'h5'

export const db = {
	// 初始化数据库
	async init() {
		if (isH5) {
			// H5环境使用localStorage
			return Promise.resolve()
		}
		
		return new Promise((resolve, reject) => {
			// #ifdef APP-PLUS
			plus.sqlite.openDatabase({
				name: DB_NAME,
				path: '_doc/workhours.db',
				success(e) {
					console.log('数据库打开成功')
					// 先检查表是否存在
					plus.sqlite.selectSql({
						name: DB_NAME,
						sql: "SELECT name FROM sqlite_master WHERE type='table' AND name='work_records'",
						success(data) {
							if (data.length === 0) {
								// 表不存在，创建表
								plus.sqlite.executeSql({
									name: DB_NAME,
									sql: `CREATE TABLE IF NOT EXISTS work_records (
										id INTEGER PRIMARY KEY AUTOINCREMENT,
										date TEXT NOT NULL,
										hours REAL NOT NULL,
										content TEXT,
										created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
									)`,
									success(e) {
										console.log('数据表创建成功')
										resolve(e)
									},
									fail(e) {
										console.error('数据表创建失败', e)
										reject(e)
									}
								})
							} else {
								// 表已存在，直接返回成功
								console.log('数据表已存在')
								resolve()
							}
						},
						fail(e) {
							console.error('检查表是否存在失败', e)
							reject(e)
						}
					})
				},
				fail(e) {
					console.error('数据库打开失败', e)
					reject(e)
				}
			})
			// #endif
		})
	},

	// 保存工时记录
	async saveRecord(date, hours, content) {
		if (isH5) {
			try {
				const records = this._getStorageRecords()
				records[date] = { date, hours, content }
				uni.setStorageSync(STORAGE_KEY, JSON.stringify(records))
				return Promise.resolve()
			} catch (e) {
				return Promise.reject(e)
			}
		}
		
		// #ifdef APP-PLUS
		const sql = `INSERT INTO work_records (date, hours, content) VALUES ('${date}', ${hours}, '${content}')`
		return new Promise((resolve, reject) => {
			plus.sqlite.executeSql({
				name: DB_NAME,
				sql: sql,
				success(e) {
					resolve(e)
				},
				fail(e) {
					console.error('保存失败', JSON.stringify(e))
					reject(e)
				}
			})
		})
		// #endif
	},

	// 获取指定日期的工时记录
	async getRecord(date) {
		if (isH5) {
			const records = this._getStorageRecords()
			return Promise.resolve(records[date] || null)
		}
		
		// #ifdef APP-PLUS
		const sql = `SELECT * FROM work_records WHERE date = '${date}'`
		return new Promise((resolve, reject) => {
			plus.sqlite.selectSql({
				name: DB_NAME,
				sql: sql,
				success(data) {
					resolve(data[0] || null)
				},
				fail(e) {
					reject(e)
				}
			})
		})
		// #endif
	},

	// 获取月度工时记录
	async getMonthRecords(yearMonth) {
		if (isH5) {
			const records = this._getStorageRecords()
			const monthRecords = Object.values(records).filter(record => {
				return record.date.startsWith(yearMonth)
			})
			return Promise.resolve(monthRecords.sort((a, b) => a.date.localeCompare(b.date)))
		}
		
		// #ifdef APP-PLUS
		const sql = `SELECT * FROM work_records WHERE strftime('%Y-%m', date) = '${yearMonth}' ORDER BY date`
		return new Promise((resolve, reject) => {
			plus.sqlite.selectSql({
				name: DB_NAME,
				sql: sql,
				success(data) {
					resolve(data)
				},
				fail(e) {
					reject(e)
				}
			})
		})
		// #endif
	},

	// 更新工时记录
	async updateRecord(date, hours, content) {
		if (isH5) {
			try {
				const records = this._getStorageRecords()
				records[date] = { date, hours, content }
				uni.setStorageSync(STORAGE_KEY, JSON.stringify(records))
				return Promise.resolve()
			} catch (e) {
				return Promise.reject(e)
			}
		}
		
		// #ifdef APP-PLUS
		const sql = `UPDATE work_records SET hours = ${hours}, content = '${content}' WHERE date = '${date}'`
		return new Promise((resolve, reject) => {
			plus.sqlite.executeSql({
				name: DB_NAME,
				sql: sql,
				success(e) {
					resolve(e)
				},
				fail(e) {
					reject(e)
				}
			})
		})
		// #endif
	},

	// 获取本地存储的记录（H5环境使用）
	_getStorageRecords() {
		try {
			const data = uni.getStorageSync(STORAGE_KEY)
			return data ? JSON.parse(data) : {}
		} catch (e) {
			console.error('读取存储失败:', e)
			return {}
		}
	}
} 