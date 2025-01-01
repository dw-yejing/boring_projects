<template>
	<view class="container">
		
		<view class="calendar-wrap">
			<work-calendar 
				:value="currentDate"
				:work-hours="workHoursData"
				@select="handleDateSelect"
				@monthChange="handleMonthChange"
			/>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import WorkCalendar from '@/components/work-calendar/index.vue'
import { useWorkHoursStore } from '@/stores/workHours'
import { formatDate, formatYearMonth } from '@/utils/date'

const store = useWorkHoursStore()
const currentDate = ref(new Date())

// 计算日历显示的工时数据
const workHoursData = computed(() => {
	const hoursData = {}
	store.monthRecords.forEach(record => {
		hoursData[record.date] = record.hours
	})
	return hoursData
})

// 日期选择
function handleDateSelect(date) {
	const dateStr = formatDate(date)
	uni.navigateTo({
		url: `/pages/record/index?date=${dateStr}`
	})
}

// 处理月份变化
function handleMonthChange(date) {
	currentDate.value = date
	const yearMonth = formatYearMonth(date)
	store.loadMonthData(yearMonth)
}

// 页面显示时刷新数据
onShow(() => {
	const yearMonth = formatYearMonth(currentDate.value)
	store.loadMonthData(yearMonth)
})

// 页面加载时初始化数据库并加载数据
onMounted(async () => {
	try {
		await store.init()
		const yearMonth = formatYearMonth(currentDate.value)
		await store.loadMonthData(yearMonth)
	} catch (e) {
		console.error('初始化失败:', e)
	}
})
</script>

<style lang="scss">
.container {
	padding: 30rpx;
}

.calendar-wrap {
	background-color: #fff;
	border-radius: 12rpx;
	margin-bottom: 30rpx;
}
</style>