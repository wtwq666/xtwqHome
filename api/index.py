from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from datetime import datetime

app = FastAPI()

# 允许跨域（方便本地开发时 localhost:5173 调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 所有 API 路由统一加上 /api 前缀
router = APIRouter(prefix="/api")

@router.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Vercel! 🎉", "framework": "FastAPI"}

@router.get("/hello")
def hello():
    return {
        "message": "Hello from FastAPI!",
        "framework": "FastAPI",
        "deployed_on": "Vercel Serverless",
        "language": "Python"
    }

@router.get("/time")
def get_time():
    now = datetime.now()
    return {
        "utc": now.isoformat(),
        "local": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "Asia/Shanghai",
        "tip": "这个接口由 FastAPI 运行在 Vercel 服务器上"
    }

app.include_router(router)

# Vercel Serverless Function 入口
handler = Mangum(app)
