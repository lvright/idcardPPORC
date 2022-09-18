import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import paddlehub as hub
import cv2
import re

def get_idcard_orc(test_img_path: list) -> dict:
    # 待预测图片
    ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
    np_images = [cv2.imread(image_path) for image_path in test_img_path]
    results = ocr.recognize_text(
        images=np_images,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
        use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
        output_dir='static/ocr_result',  # 图片的保存路径，默认设为 ocr_result；
        visualization=True,  # 是否将识别结果保存为图片文件；
        box_thresh=0.5,  # 检测文本框置信度的阈值；
        text_thresh=0.5)  # 识别中文文本置信度的阈值；
    return results

def get_idcard_content(imageBaseStr) -> dict:
    content = {}
    result = get_idcard_orc([imageBaseStr])
    for res in result:
        data = res["data"]
        for info in data:

            if re.findall(r"姓名", info["text"]):
                content.update({"姓名": info["text"][-3:]})

            if re.findall(r"\d", info["text"]):
                content.update({"身份证号码": info["text"]})

            if re.findall(r"性别", info["text"]):
                content.update({"性别": info["text"][2:3]})

            if re.findall(r"民族", info["text"]):
                content.update({"民族": info["text"][5:]})

            if re.findall(r".*年.*月.*日", info["text"]):
                content.update({"出生年月": info["text"]})

            if re.findall(r".*省.*市", info["text"]):
                content.update({"住址": info["text"][2:]})

            if re.findall(r".*区|.*村+.*号", info["text"]):
                content["住址"] = content["住址"] + info["text"]

    return content