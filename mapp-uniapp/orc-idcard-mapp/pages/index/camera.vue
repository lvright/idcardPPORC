<template>
	<view class="cameraBg">
		<camera device-position="back" flash="auto" style="width: 100%; height: 100vh">
			<cover-image src="@/static/index/cameraBg.png" class="scan-img"> </cover-image>
			<cover-view class="scanBtn" v-if="scanShow">
				<cover-view class="beat" @click="scan">
					<cover-image class="beatImg" src="@/static/index/album.png"></cover-image>
					<cover-view> 相册 </cover-view>
				</cover-view>
				<cover-view class="album" @click="takePhoto">
					<cover-image class="albumImg" src="@/static/index/beat.png"></cover-image>
					<cover-view> 识别 </cover-view>
				</cover-view>
			</cover-view>
		</camera>
	</view>
</template>

<script>
import { http } from '@/api/api.config.js'
 
export default {
data() {
    return {
		scanShow: true
    }
},
	methods: {
		// 相册
		scan() {
			// 选择图片
			uni.chooseImage({
				count: 1,
				sizeType: ['original', 'compressed'],
				sourceType: ['album'],
				success: (res) => {
					this.compress(res.tempFilePaths[0])
				}
			})
		},
		// 启动图片压缩
		compress(tempFilePaths) {
			const vm = this
			vm.scanShow = false
			uni.showLoading({
				title: '智能识别中...'
			})
			uni.compressImage({
				src: tempFilePaths,
				quality: 80,
				success: (imageRes) => {
				// 获取类型
					uni.getImageInfo({
						src: imageRes.tempFilePath,
						success(imageInfo) {
						  // 转base64
							uni.getFileSystemManager().readFile({
								filePath: imageRes.tempFilePath,
								encoding: 'base64',
								success: (base) => {
									// 返回base64格式
									const base64Data = 'data:image/' + imageInfo.type + ';base64,' + base.data
									vm.camera64(base64Data)
								},
								fail: (err) => {
									console.log(err)
								}
							})
						}
					})
				}
			})
		},
		// 拿到图片开始进行识别
		camera64(base64Data) {
			// 拿到base64,不需要base64  就把上层的转换去掉
			this.scanShow = true
			uni.hideLoading()
			console.log(base64Data,'base64Data图片')
			// 此处为后端接口 传base64图片 进行ocr识别
			uni.request({
				method: "GET",
				url: "http://127.0.0.1:8089/orc/content",
				data: { imageBase64: base64Data },
				success(res) {
					console.log(res)
					if (res.code === 200) {
						uni.hideLoading()
						uni.showToast({
							title: '已识别到身份证',
							duration: 2000
						});
						if (data.body.vin) {
							this.goPage('/pages/product/index?vin=' + data.body.vin, true, 'redirectTo')
						} else {
							this.msg('无法识别,请重新拍照')
						}
					}
				}
			})
		},
		// 拍照
		takePhoto() {
			const ctx = uni.createCameraContext()
			ctx.takePhoto({
				quality: 'high',
				success: (res) => {
					this.compress(res.tempImagePath)
				}
			})
		},
		error(e) {
			console.log(e.detail)
		}
	}
}
</script>

<style lang="scss" scoped>
.cameraBg {
  width: 100%;
  height: 100vh;
  position: fixed;
  .scan-img {
    width: 100%;
    height: 1624rpx;
    z-index: 1;
  }
  .scanBtn {
    width: 100%;
    z-index: 99999;
    position: fixed;
    bottom: 100rpx;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .beat {
      position: absolute;
      bottom: 0rpx;
      left: 100rpx;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      font-size: 24rpx;
      font-weight: 400;
      color: #ffffff;
      .beatImg {
        width: 88rpx;
        height: 88rpx;
        margin-bottom: 30rpx;
      }
    }
    .album {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      font-size: 24rpx;
      font-weight: 400;
      color: #ffffff;
      .albumImg {
        width: 120rpx;
        height: 120rpx;
        margin-bottom: 30rpx;
      }
    }
  }
}
</style>
