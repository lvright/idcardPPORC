from api.orc import get_idcard, router
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.include_router(router, tags=["ORC身份证信息识别"])

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        debug=True,
        reload=True,
        port=8089
    )