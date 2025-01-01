<template>
	<view class="work-form">
		<view class="form-item">
			<text class="label">工作时长</text>
			<input 
				type="digit" 
				v-model="hours"
				class="input" 
				placeholder="请输入工作时长(小时)"
			/>
		</view>
		
		<view class="form-item">
			<text class="label">工作内容</text>
			<textarea 
				v-model="content"
				class="textarea"
				placeholder="请输入工作内容描述"
			/>
		</view>
		
		<button class="submit-btn" @tap="handleSubmit">保存</button>
	</view>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
	date: {
		type: Date,
		required: true
	},
	initialData: {
		type: Object,
		default: () => null
	}
})

const emit = defineEmits(['save'])

const hours = ref('')
const content = ref('')

watch(() => props.initialData, (newVal) => {
	if (newVal) {
		hours.value = newVal.hours
		content.value = newVal.content
	}
}, { immediate: true })

function handleSubmit() {
	if (!hours.value) {
		uni.showToast({
			title: '请输入工作时长',
			icon: 'none'
		})
		return
	}
	
	emit('save', {
		hours: Number(hours.value),
		content: content.value
	})
}
</script>

<style lang="scss">
.work-form {
	background-color: #fff;
	padding: 30rpx;
	border-radius: 8rpx;
	
	.form-item {
		margin-bottom: 30rpx;
		
		.label {
			display: block;
			font-size: 28rpx;
			color: #333;
			margin-bottom: 20rpx;
		}
		
		.input {
			border: 1rpx solid #ddd;
			padding: 20rpx;
			border-radius: 4rpx;
		}
		
		.textarea {
			border: 1rpx solid #ddd;
			padding: 20rpx;
			border-radius: 4rpx;
			width: auto;
			height: 200rpx;
		}
	}
	
	.submit-btn {
		background-color: #007AFF;
		color: #fff;
	}
}
</style> 