<template>
	<view class="calendar">
		<view class="calendar-header">
			<view class="header-controls">
				<button class="month-btn" @tap="changeMonth('prev')">上个月</button>
				<text class="month-text">{{currentYearMonth}}</text>
				<button class="month-btn" @tap="changeMonth('next')">下个月</button>
			</view>
		</view>
		
		<view class="weekday-row">
			<text v-for="day in weekDays" :key="day" class="weekday">{{day}}</text>
		</view>
		
		<view class="days-grid">
			<view 
				v-for="(day, index) in days" 
				:key="index"
				class="day-cell"
				:class="getDayClass(day)"
				@tap="handleDayClick(day)"
			>
				<text class="day-text">{{day.date}}</text>
				<text v-if="day.hours" class="hours-text">{{day.hours}}h</text>
			</view>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
	value: {
		type: Date,
		default: () => new Date()
	},
	workHours: {
		type: Object,
		default: () => ({})
	}
})

const emit = defineEmits(['select', 'monthChange'])

const weekDays = ['日', '一', '二', '三', '四', '五', '六']
const currentDate = ref(new Date(props.value))

const currentYearMonth = computed(() => {
	const year = currentDate.value.getFullYear()
	const month = currentDate.value.getMonth() + 1
	return `${year}年${month}月`
})

const days = computed(() => {
	const year = currentDate.value.getFullYear()
	const month = currentDate.value.getMonth()
	const firstDay = new Date(year, month, 1)
	const lastDay = new Date(year, month + 1, 0)
	
	const days = []
	
	// 上月剩余日期
	const firstDayWeek = firstDay.getDay()
	const prevMonthLastDay = new Date(year, month, 0).getDate()
	for (let i = firstDayWeek - 1; i >= 0; i--) {
		const date = prevMonthLastDay - i
		days.push({
			date,
			fullDate: new Date(year, month - 1, date),
			isCurrentMonth: false,
			isToday: false
		})
	}
	
	// 当月日期
	const today = new Date()
	for (let i = 1; i <= lastDay.getDate(); i++) {
		const fullDate = new Date(year, month, i)
		const dateKey = formatDate(fullDate)
		days.push({
			date: i,
			fullDate,
			isCurrentMonth: true,
			isToday: isToday(fullDate, today),
			hours: props.workHours[dateKey]
		})
	}
	
	// 下月开始日期
	const remainingDays = 42 - days.length // 保持6行
	for (let i = 1; i <= remainingDays; i++) {
		days.push({
			date: i,
			fullDate: new Date(year, month + 1, i),
			isCurrentMonth: false,
			isToday: false
		})
	}
	
	return days
})

function isToday(date1, date2) {
	return date1.getFullYear() === date2.getFullYear() &&
		date1.getMonth() === date2.getMonth() &&
		date1.getDate() === date2.getDate()
}

function formatDate(date) {
	return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

function getDayClass(day) {
	return {
		'current-month': day.isCurrentMonth,
		'other-month': !day.isCurrentMonth,
		'today': day.isToday,
		'has-hours': day.hours && day.hours > 0,
		'weekend': day.fullDate.getDay() === 0 || day.fullDate.getDay() === 6
	}
}

function changeMonth(type) {
	const date = new Date(currentDate.value)
	if (type === 'prev') {
		date.setMonth(date.getMonth() - 1)
	} else {
		date.setMonth(date.getMonth() + 1)
	}
	currentDate.value = date
	// 触发月份变化事件
	emit('monthChange', date)
}

function handleDayClick(day) {
	if (!day.isCurrentMonth) return
	emit('select', day.fullDate)
}

// 监听外部value变化
watch(() => props.value, (newVal) => {
	currentDate.value = new Date(newVal)
})
</script>

<style lang="scss">
.calendar {
	background-color: #fff;
	border-radius: 8rpx;
	padding: 20rpx;
	
	.calendar-header {
		margin-bottom: 20rpx;
		
		.header-controls {
			display: flex;
			align-items: center;
			justify-content: space-between;
			padding: 0 20rpx;
			margin-bottom: 20rpx;
			
			.month-btn {
				margin: 0;
				min-width: 140rpx;
				padding: 12rpx 24rpx;
				font-size: 28rpx;
				color: #007AFF;
				background: rgba(0, 122, 255, 0.1);
				border: none;
				border-radius: 30rpx;
				line-height: 1.8;
				font-weight: 500;
				box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
				transition: all 0.2s ease;
				
				&::after {
					display: none;
				}
				
				&:active {
					transform: scale(0.98);
					background: rgba(0, 122, 255, 0.15);
					box-shadow: 0 1rpx 4rpx rgba(0, 0, 0, 0.05);
				}
			}
			
			.month-text {
				font-size: 34rpx;
				font-weight: bold;
				color: #333;
				min-width: 180rpx;
				text-align: center;
			}
		}
	}
	
	.weekday-row {
		display: flex;
		margin-bottom: 10rpx;
		
		.weekday {
			flex: 1;
			text-align: center;
			font-size: 28rpx;
			color: #999;
			padding: 20rpx 0;
		}
	}
	
	.days-grid {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		gap: 2rpx;
		background-color: #f5f5f5;
		
		.day-cell {
			aspect-ratio: 1;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			background-color: #fff;
			position: relative;
			
			&.other-month {
				.day-text {
					color: #ccc;
				}
			}
			
			&.today {
				.day-text::after {
					content: '今';
					position: absolute;
					top: 4rpx;
					right: 4rpx;
					font-size: 20rpx;
					color: #007AFF;
				}
			}
			
			&.weekend:not(.other-month) {
				.day-text {
					color: #ff6b6b;
				}
			}
			
			&.has-hours {
				background-color: #007AFF;
				
				.day-text, .hours-text {
					color: #fff;
				}
			}
			
			.day-text {
				font-size: 28rpx;
				color: #333;
			}
			
			.hours-text {
				font-size: 24rpx;
				margin-top: 4rpx;
				color: #666;
			}
		}
	}
}
</style> 