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

		<!-- 字体大小调整浮动按钮 -->
		<view class="font-size-control">
			<view class="font-size-btn" @tap="showFontPanel = true">
				<text class="iconfont">Aa</text>
			</view>
		</view>

		<!-- 字体大小调整面板 -->
		<view class="font-size-panel" v-if="showFontPanel" @tap.stop>
			<view class="panel-mask" @tap="showFontPanel = false"></view>
			<view class="panel-content">
				<view class="panel-header">
					<text>字体大小</text>
					<text class="close-btn" @tap="showFontPanel = false">×</text>
				</view>
				<view class="panel-body">
					<button class="size-btn" @tap="decreaseFontSize">A-</button>
					<text class="size-value">{{fontSize}}</text>
					<button class="size-btn" @tap="increaseFontSize">A+</button>
				</view>
				<button class="reset-btn" @tap="resetFontSize">重置</button>
			</view>
		</view>
	</view>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useWorkHoursStore } from '@/stores/workHours'
import { formatMonth, formatDateShort, formatDate } from '@/utils/date'

const store = useWorkHoursStore()
const baseFontSize = 32
const fontSizeStep = 4
const fontSize = ref(uni.getStorageSync('listFontSize') || baseFontSize)
const showFontPanel = ref(false)

// 计算字体大小样式
const fontSizeStyle = computed(() => fontSize.value + 'rpx')

// 增大字体
function increaseFontSize() {
	if (fontSize.value < 60) {
		fontSize.value += fontSizeStep
		console.log("===", fontSize.value)
		saveFontSize()
	}
}

// 减小字体
function decreaseFontSize() {
	if (fontSize.value > 24) {
		fontSize.value -= fontSizeStep
		saveFontSize()
	}
}

// 重置字体
function resetFontSize() {
	fontSize.value = baseFontSize
	saveFontSize()
}

// 保存字体大小
function saveFontSize() {
	uni.setStorageSync('listFontSize', fontSize.value)
	// 添加反馈提示
	uni.showToast({
		title: '字体大小已更新',
		icon: 'none',
		duration: 500
	})
}

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
	padding: 20rpx 12rpx;
	height: 100vh;
	box-sizing: border-box;
	display: flex;
	flex-direction: column;
}

.statistics-header {
	margin-bottom: 20rpx;
	
	.month-picker {
		background-color: #fff;
		padding: 16rpx;
		border-radius: 8rpx;
		
		.picker-text {
			font-size: 36rpx;
			color: #333;
			text-align: center;
		}
	}
}

.statistics-content {
	flex: 1;
	background-color: #fff;
	border-radius: 12rpx;
	padding: 20rpx 12rpx;
	margin-bottom: 20rpx;
	display: flex;
	flex-direction: column;
	
	.total-hours {
		text-align: center;
		margin-bottom: 20rpx;
		
		.label {
			font-size: 32rpx;
			color: #666;
			margin-right: 20rpx;
		}
		
		.value {
			font-size: 48rpx;
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
			padding: 16rpx 0;
			border-bottom: 1rpx solid #eee;
			font-size: v-bind(fontSizeStyle);
			color: #666;
			font-weight: bold;
			text-align: center;
		}
		
		.list-content {
			flex: 1;
		}
		
		.list-item {
			display: flex;
			padding: 16rpx 0;
			border-bottom: 1rpx solid #eee;
			font-size: v-bind(fontSizeStyle);
			
			&:last-child {
				border-bottom: none;
			}
		}
		
		.date-col {
			width: 160rpx;
			font-size: v-bind(fontSizeStyle);
			text-align: center;
		}
		
		.hours-col {
			width: 120rpx;
			text-align: center;
			font-size: v-bind(fontSizeStyle);
			padding: 0 10rpx;
		}
		
		.content-col {
			flex: 1;
			font-weight: 500;
			font-size: v-bind(fontSizeStyle);
			text-align: left;
			padding-left: 20rpx;
			white-space: normal;
			word-break: break-all;
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

.font-size-control {
	position: fixed;
	right: 20rpx;
	top: 20rpx;
	z-index: 100;
	
	.font-size-btn {
		width: 80rpx;
		height: 80rpx;
		background: #007AFF;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.2);
		
		.iconfont {
			color: #fff;
			font-size: 32rpx;
			font-weight: bold;
		}
		
		&:active {
			opacity: 0.8;
		}
	}
}

.font-size-panel {
	position: fixed;
	left: 0;
	right: 0;
	top: 0;
	bottom: 0;
	z-index: 999;
	
	.panel-mask {
		position: absolute;
		left: 0;
		right: 0;
		top: 0;
		bottom: 0;
		background: rgba(0,0,0,0.4);
	}
	
	.panel-content {
		position: absolute;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		width: 560rpx;
		background: #fff;
		border-radius: 20rpx;
		padding: 30rpx;
		
		.panel-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 30rpx;
			font-size: 32rpx;
			
			.close-btn {
				font-size: 40rpx;
				color: #999;
				padding: 0 20rpx;
				
				&:active {
					opacity: 0.8;
				}
			}
		}
		
		.panel-body {
			display: flex;
			align-items: center;
			justify-content: space-between;
			margin-bottom: 30rpx;
			
			.size-btn {
				width: 120rpx;
				height: 80rpx;
				line-height: 80rpx;
				background: #f5f5f5;
				border-radius: 8rpx;
				font-size: 32rpx;
				
				&:active {
					opacity: 0.8;
				}
			}
			
			.size-value {
				font-size: 36rpx;
				color: #333;
				font-weight: bold;
			}
		}
		
		.reset-btn {
			width: 100%;
			height: 80rpx;
			line-height: 80rpx;
			background: #f5f5f5;
			color: #666;
			font-size: 28rpx;
			
			&:active {
				opacity: 0.8;
			}
		}
	}
}
</style> 