// 格式化年月 YYYY-MM
export function formatYearMonth(date) {
	if (typeof date === 'string') return date
	const year = date.getFullYear()
	const month = String(date.getMonth() + 1).padStart(2, '0')
	return `${year}-${month}`
}

// 格式化显示月份
export function formatMonth(yearMonth) {
	const [year, month] = yearMonth.split('-')
	return `${year}年${month}月`
}

// 格式化日期为 YYYY-MM-DD
export function formatDate(date) {
	if (date instanceof Date) {
		const year = date.getFullYear()
		const month = String(date.getMonth() + 1).padStart(2, '0')
		const day = String(date.getDate()).padStart(2, '0')
		return `${year}-${month}-${day}`
	}
	return date // 如果已经是格式化的字符串，直接返回
}

// 格式化日期显示为 MM月DD日
export function formatDateShort(dateStr) {
	const date = typeof dateStr === 'string' ? 
		new Date(dateStr.replace(/-/g, '/')) : 
		dateStr
	return `${date.getMonth() + 1}月${date.getDate()}日`
}

// 格式化日期显示为 YYYY年MM月DD日
export function formatDateDisplay(date) {
	if (typeof date === 'string') {
		date = new Date(date.replace(/-/g, '/'))
	}
	const year = date.getFullYear()
	const month = date.getMonth() + 1
	const day = date.getDate()
	return `${year}年${month}月${day}日`
} 