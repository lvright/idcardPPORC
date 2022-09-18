<template>
	<view class="content">
		<view><image class="logo" src="/static/card.png"></image></view>
		<view class="text-area">
			<text class="title"> 疫情隔离人员身份证识别程序 </text>
		</view>
		<button class="btn" type="submit" @click="camera"> 打开识别 </button>
		<button class="btn down-file-btn" type="submit"> 下载隔离人员信息表 </button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello'
			}
		},
		onLoad() {

		},
		methods: {
			camera() {
				uni.navigateTo({
					url: '/pages/index/camera'
				});
			}
		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 120rpx;
		width: 120rpx;
		margin-top: 200rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}

	.text-area {
		display: flex;
		justify-content: center;
		margin-bottom: 100rpx;
	}
	
	.btn {
		background: #0061b2;
		color: #FFFFFF;
		width: 520rpx;
		margin-top: 20rpx
	}
	
	.down-file-btn {
		background-color: #d9e8f7;
		color: #0061b2;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>
