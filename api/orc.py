from fastapi import APIRouter
from fastapi.logger import logger
from orc_content import get_idcard_content
from fastapi.responses import JSONResponse
import base64
import random
import pandas as pd

router = APIRouter()

@router.get(path="/orc/content", summary="ORC身份证信息识别")
def get_idcard(imageBase64: str):
    b64_data = imageBase64.split(';base64,')[1]
    data = base64.b64decode(b64_data)
    file_name = "static/idcard/" + ''.join(str(random.choice(range(10))) for _ in range(10)) + ".jpg"
    with open(file_name, "wb") as f:
        f.write(data)
    result = {"code": 200, "msg": "Success"}
    try:
        content = get_idcard_content(file_name)
        df = pd.DataFrame()
        df["name"] = list(content.keys())
        df["value"] = list(content.values())
        df.to_excel("static/excel/idcard_info.xlsx", encoding="utf-8", index=False)
        logger.info(f"识别成功，识别信息 --info：{content}")
    except Exception as e:
        result["code"] = 500
        result["msg"] = f"不是有效的身份证图片 -- 错误信息:{e}"
        logger.error(result["msg"])
    return JSONResponse(status_code=result["code"], content=result)