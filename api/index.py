from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

# 允许跨域（方便本地开发时 localhost:5173 调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Vercel! 🎉", "framework": "FastAPI"}

@app.get("/hello")
def hello():
    return {
        "message": "Hello from FastAPI!",
        "framework": "FastAPI",
        "deployed_on": "Vercel Serverless",
        "language": "Python"
    }

@app.get("/time")
def get_time():
    from datetime import datetime
    now = datetime.now()
    return {
        "utc": now.isoformat(),
        "local": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "Asia/Shanghai",
        "tip": "这个接口由 FastAPI 运行在 Vercel 服务器上"
    }

# Vercel Serverless Function 入口
handler = Mangum(app)
