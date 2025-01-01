<template>
	<view class="container">
		<view class="statistics-header">
			<view class="month-picker">
				<picker mode="date" fields="month" :value="store.currentMonth" @change="handleMonthChange">
					<view class="picker-text">{{formatMonth(store.currentMonth)}}</view>
				</picker>
			</view>
		</view>
		
		<view class="statistics-content">
			<view class="total-hours">
				<text class="label">本月工时</text>
				<text class="value">{{store.totalHours}}小时</text>
			</view>
			
			<view class="daily-list">
				<view class="list-header">
					<text class="date-col">日期</text>
					<text class="hours-col">工时</text>
					<text class="content-col">工作内容</text>
				</view>
				<scroll-view scroll-y class="list-content">
					<view v-for="item in store.sortedRecords" :key="item.date" class="list-item">
						<text class="date-col">{{formatDateShort(item.date)}}</text>
						<text class="hours-col">{{item.hours}}h</text>
						<text class="content-col">{{item.content || '-'}}</text>
					</view>
				</scroll-view>
			</view>
		</view>
		
		<button class="export-btn" @tap="handleExport">导出统计</button>
	</view>
</template>

<script setup>
import { onMounted } from 'vue'
import { useWorkHoursStore } from '@/stores/workHours'
import { formatMonth, formatDateShort, formatDate } from '@/utils/date'

const store = useWorkHoursStore()

// 月份切换
function handleMonthChange(e) {
	store.loadMonthData(e.detail.value)
}

// 导出统计
function handleExport() {
	// 生成导出内容
	let content = `${formatMonth(store.currentMonth)}工时统计\n\n`
	content += `总工时：${store.totalHours}小时\n\n`
	content += `日期\t工时\t工作内容\n`
	store.sortedRecords.forEach(record => {
		content += `${formatDate(record.date)}\t${record.hours}h\t${record.content || '-'}\n`
	})
	
	// 在H5端或APP端，可以直接复制到剪贴板
	// #ifdef H5 || APP-PLUS
	uni.setClipboardData({
		data: content,
		showToast: true,
		success: () => {
			console.log("数据已复制到剪贴板")
		}
	})
	// #endif
	
	// 在小程序端，可以保存为文件或使用其他方式分享
	// #ifdef MP
	uni.showModal({
		title: '导出统计',
		content: '暂不支持导出功能，请截图保存',
		showCancel: false
	})
	// #endif
}

onMounted(() => {
	store.loadMonthData()
})
</script>

<style lang="scss">
.container {
	padding: 30rpx;
	height: 100vh;
	box-sizing: border-box;
	display: flex;
	flex-direction: column;
}

.statistics-header {
	margin-bottom: 30rpx;
	
	.month-picker {
		background-color: #fff;
		padding: 20rpx;
		border-radius: 8rpx;
		
		.picker-text {
			font-size: 32rpx;
			color: #333;
			text-align: center;
		}
	}
}

.statistics-content {
	flex: 1;
	background-color: #fff;
	border-radius: 12rpx;
	padding: 30rpx;
	margin-bottom: 30rpx;
	display: flex;
	flex-direction: column;
	
	.total-hours {
		text-align: center;
		margin-bottom: 40rpx;
		
		.label {
			font-size: 28rpx;
			color: #666;
			margin-right: 20rpx;
		}
		
		.value {
			font-size: 40rpx;
			color: #007AFF;
			font-weight: bold;
		}
	}
	
	.daily-list {
		flex: 1;
		display: flex;
		flex-direction: column;
		
		.list-header {
			display: flex;
			padding: 20rpx 0;
			border-bottom: 1rpx solid #eee;
			font-size: 28rpx;
			color: #666;
			font-weight: bold;
		}
		
		.list-content {
			flex: 1;
		}
		
		.list-item {
			display: flex;
			padding: 20rpx 0;
			border-bottom: 1rpx solid #eee;
			font-size: 28rpx;
			
			&:last-child {
				border-bottom: none;
			}
		}
		
		.date-col {
			width: 180rpx;
		}
		
		.hours-col {
			width: 100rpx;
			text-align: center;
		}
		
		.content-col {
			flex: 1;
			color: #666;
		}
	}
}

.export-btn {
	background-color: #007AFF;
	color: #fff;
	
	&:active {
		opacity: 0.8;
	}
}
</style> 