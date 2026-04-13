from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from datetime import datetime
import os
import json

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

@router.get("/docs")
def get_docs_structure():
    """获取文档目录结构"""
    docs_dir = "stu_docs"
    result = []
    
    def traverse_directory(directory, path=""):
        items = []
        for item in os.listdir(os.path.join(docs_dir, directory)):
            item_path = os.path.join(directory, item)
            full_path = os.path.join(docs_dir, item_path)
            if os.path.isdir(full_path):
                items.append({
                    "name": item,
                    "path": item_path,
                    "type": "directory",
                    "children": traverse_directory(item_path, item_path)
                })
            elif item.endswith(".md"):
                items.append({
                    "name": item[:-3],  # 移除 .md 后缀
                    "path": item_path,
                    "type": "file"
                })
        return items
    
    result = traverse_directory("")
    return {"structure": result}

@router.get("/docs/{path:path}")
def get_doc_content(path: str):
    """获取文档内容"""
    file_path = os.path.join("stu_docs", path)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    if not file_path.endswith(".md"):
        return {"error": "Not a Markdown file"}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

app.include_router(router)

# Vercel Serverless Function 入口
handler = Mangum(app)
