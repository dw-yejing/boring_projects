<template>
	<view class="container">
		<view class="date-info">
			<text class="date-text">{{formatDateDisplay(currentDate)}}</text>
		</view>
		
		<view class="form-wrap">
			<view class="form-item">
				<view class="label" @tap="handleHoursFocus">工作时长</view>
				<input 
					id="hoursInput"
					ref="hoursInputRef"
					type="digit" 
					v-model="hours"
					class="input" 
					placeholder="请输入工作时长(小时)"
					:focus="hoursInputFocus"
					@blur="onHoursBlur"
				/>
			</view>
			
			<view class="form-item">
				<view class="label" @tap="handleContentFocus">工作内容</view>
				<textarea 
					ref="textareaRef"
					v-model="content"
					class="textarea"
					placeholder="请输入工作内容描述"
					:focus="textareaFocus"
					@blur="onTextareaBlur"
					auto-height
				/>
			</view>
			
			<button class="submit-btn" @tap="handleSave">保存</button>
		</view>
	</view>
</template>

<script setup>
import { ref } from 'vue'
import { useWorkHoursStore } from '@/stores/workHours'
import { formatDate, formatDateDisplay } from '@/utils/date'
import { onLoad } from '@dcloudio/uni-app'

const store = useWorkHoursStore()
const currentDate = ref(new Date())
const hours = ref('')
const content = ref('')
const textareaRef = ref(null)
const hoursInputRef = ref(null)
const hoursInputFocus = ref(false)
const textareaFocus = ref(false)

function handleHoursFocus() {
	hoursInputFocus.value = true
	textareaFocus.value = false
}

function handleContentFocus() {
	textareaFocus.value = true
	hoursInputFocus.value = false
}

// 监听输入框失去焦点事件
function onHoursBlur() {
	hoursInputFocus.value = false
}

function onTextareaBlur() {
	textareaFocus.value = false
}

// 保存工时
async function handleSave() {
	if (!hours.value) {
		uni.showToast({
			title: '请输入工作时长',
			icon: 'none'
		})
		return
	}
	
	const hoursNum = Number(hours.value)
	if (isNaN(hoursNum) || hoursNum <= 0) {
		uni.showToast({
			title: '请输入有效的工时',
			icon: 'none'
		})
		return
	}
	
	const dateStr = formatDate(currentDate.value)
	const success = await store.saveRecord(dateStr, hoursNum, content.value)
	
	if (success) {
		uni.showToast({
			title: '保存成功',
			icon: 'success',
			success: () => {
				setTimeout(() => {
					uni.navigateBack()
				}, 0)
			}
		})
	} else {
		uni.showToast({
			title: '保存失败',
			icon: 'error'
		})
	}
}

// 加载已有记录
async function loadRecord(date) {
	try {
		const dateStr = formatDate(date)
		const record = await store.getRecord(dateStr)
		if (record) {
			hours.value = String(record.hours)
			content.value = record.content || ''
		}
	} catch (e) {
		console.error('加载记录失败:', e)
	}
}

// 使用 onLoad 替代 onMounted
onLoad((options) => {
	if (options.date) {
		currentDate.value = new Date(options.date.replace(/-/g, '/'))
		loadRecord(currentDate.value)
	} else {
		currentDate.value = new Date()
	}
})
</script>

<style lang="scss">
.container {
	padding: 30rpx;
}

.date-info {
	background-color: #fff;
	padding: 30rpx;
	border-radius: 12rpx;
	margin-bottom: 30rpx;
	
	.date-text {
		font-size: 32rpx;
		color: #333;
		font-weight: bold;
	}
}

.form-wrap {
	background-color: #fff;
	border-radius: 12rpx;
	padding: 30rpx;
	
	.form-item {
		margin-bottom: 30rpx;
		
		.label {
			display: block;
			font-size: 28rpx;
			color: #333;
			margin-bottom: 20rpx;
		}
		
		.input {
			width: 100%;
			height: 80rpx;
			border: 1rpx solid #ddd;
			border-radius: 8rpx;
			padding: 0 20rpx;
			box-sizing: border-box;
			font-size: 52rpx;
		}
		
		.textarea {
			width: 100%;
			min-height: 200rpx;
			border: 1rpx solid #ddd;
			border-radius: 8rpx;
			padding: 20rpx;
			box-sizing: border-box;
			font-size: 52rpx;
		}
	}
	
	.submit-btn {
		background-color: #007AFF;
		color: #fff;
		border-radius: 8rpx;
		margin-top: 40rpx;
		
		&:active {
			opacity: 0.8;
		}
	}
}
</style> 