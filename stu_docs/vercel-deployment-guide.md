# Vue 3 + FastAPI 在 Vercel 上的全栈部署指南

> 本文档以 `xtwqHome` 项目为例，带你从零理解：
> 1. 项目的前后端代码是如何组织的？
> 2. Vercel 在部署时究竟做了什么？
> 3. 为什么可以实现"前后端零跨域联调"？
> 4. 本地开发和线上部署的关系是什么？

---

## 一、项目整体架构

```
xtwqHome/
├── src/
│   ├── main.js          ← Vue 3 应用入口
│   └── App.vue          ← 前端主页面（含 API 调用 UI）
├── api/
│   ├── index.py         ← FastAPI 后端（Python）
│   └── requirements.txt ← Python 依赖声明
├── index.html           ← Vite 项目的 HTML 入口
├── package.json         ← Node.js 依赖声明
├── vite.config.js       ← Vite 构建 + 本地代理配置
├── vercel.json          ← Vercel 路由重写规则
└── README.md
```

**技术栈：**
- **前端**：Vue 3 + Vite（JavaScript 单页应用）
- **后端**：FastAPI（Python 异步 Web 框架）
- **部署平台**：Vercel
- **通信方式**：HTTP `fetch`，共享同一域名

---

## 二、关键文件逐行解读

### 2.1 前端入口：`index.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>xtwqHome - Vue + FastAPI on Vercel</title>
  </head>
  <body>
    <div id="app"></div>
    <!-- 关键：type="module" 表示这是一个 ES Module 入口 -->
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

**作用：** 这是浏览器访问网站时下载的第一个文件。Vite 在开发时会拦截这个请求，把 `/src/main.js` 动态加载进来；在生产构建时，会把所有代码打包成 `dist/assets/` 下的静态文件。

---

### 2.2 Vue 入口：`src/main.js`

```javascript
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

**作用：** 创建 Vue 应用实例，并把 `App.vue` 组件挂载到 `index.html` 里的 `<div id="app"></div>` 上。

---

### 2.3 前端页面：`src/App.vue`

这是一个 Vue 单文件组件（SFC），核心逻辑在前端发起 API 请求：

```javascript
const res = await fetch('/api/hello')
const data = await res.json()
```

**注意这里的关键细节：**
- 请求的 URL 是 **相对路径**：`/api/hello`
- **不是** `http://localhost:8000/api/hello`
- **也不是** `https://某后端地址.com/api/hello`

这就是"前后端同域部署"的核心优势：前端不需要知道后端具体在哪里，只要请求 `/api/xxx`，部署平台会自动把它路由到后端。

---

### 2.4 Vite 配置：`vite.config.js`

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})
```

**配置解读：**
- `plugins: [vue()]`：让 Vite 能编译 `.vue` 文件。
- `server.proxy`：只在**本地开发**时生效。当你运行 `npm run dev`，前端在 `http://localhost:5173`，如果请求 `/api/hello`，Vite 会自动帮你转发到 `http://127.0.0.1:8000/api/hello`。这样本地开发和线上都能用同样的 `/api/xxx` 路径写代码。

> ⚠️ `server.proxy` 在 Vercel 生产环境中**完全不起作用**，它只是本地开发 convenience。

---

### 2.5 FastAPI 后端：`api/index.py`

```python
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from datetime import datetime

app = FastAPI()

# CORS 中间件：允许任何来源访问（本地开发时 localhost:5173 需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 关键：给所有路由统一加上 /api 前缀
router = APIRouter(prefix="/api")

@router.get("/hello")
def hello():
    return { "message": "Hello from FastAPI!", ... }

@router.get("/time")
def get_time():
    return { "utc": ..., "local": ..., }

app.include_router(router)

# Mangum 把 FastAPI 的 ASGI 应用包装成 AWS Lambda 可以理解的 handler
handler = Mangum(app)
```

**关键概念解释：**

#### 为什么需要 `APIRouter(prefix="/api")`？

因为 Vercel 的重写规则会把 `/api/hello` 转发给这个文件。Mangum 会把完整路径 `/api/hello` 传递给 FastAPI。如果 FastAPI 里只注册了 `/hello`，路径不匹配，就会返回 `404 Not Found`。

#### 为什么需要 `Mangum`？

FastAPI 是一个 **ASGI 应用**，需要一个 ASGI 服务器（如 Uvicorn）来运行。但在 Vercel 上，Python 代码是以 **AWS Lambda（Serverless Function）** 的形式执行的，它没有持久的 Uvicorn 进程。

`Mangum` 是一个适配器，它把 Lambda 的事件对象（HTTP 请求）翻译成 ASGI 请求，再传递给 FastAPI；然后把 FastAPI 的响应再翻译回 Lambda 的返回格式。

**简单说：Mangum = FastAPI 和 Vercel Serverless 之间的翻译官。**

---

### 2.6 Python 依赖：`api/requirements.txt`

```text
fastapi
mangum
```

Vercel 在部署 Python Function 时，会自动运行：
```bash
pip install -r api/requirements.txt
```
然后在这个环境里执行你的 `api/index.py`。

---

### 2.7 Vercel 路由配置：`vercel.json`

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

**这是整个部署逻辑的核心！**

#### 第一条规则：`/api/*` → `api/index.py`
- 所有以 `/api/` 开头的请求，都交给后端的 Python 文件处理。
- 比如 `/api/hello` → Vercel 调用 `api/index.py` 里的 `handler`，并把路径信息传进去。

#### 第二条规则：`/*` → `/index.html`
- 其他所有请求都返回前端入口 HTML。
- 这是**单页应用（SPA）**的标准配置。因为 Vue 路由是前端控制的，直接访问 `/about` 时，服务器也要返回 `index.html`，然后 Vue 自己渲染对应页面。

---

## 三、Vercel 部署时究竟做了什么？

当你 `git push` 代码到 GitHub，`main` 分支发生变化，Vercel 会自动触发一次部署。它的内部流程大致如下：

### 步骤 1：拉取代码
从 GitHub 克隆最新仓库到构建服务器。

### 步骤 2：识别项目类型
Vercel 检测到：
- 根目录有 `package.json` → 这是一个 Node.js 项目
- 有 `index.html` + Vite 依赖 → 识别为 **Vite** 项目
- 有 `api/` 目录 + `.py` 文件 → 识别为 **Python Serverless Functions**

### 步骤 3：构建前端
```bash
cd 项目根目录
npm install
npm run build
```
Vite 会把 `src/` 下的 Vue 代码编译、打包，生成 `dist/` 目录，里面包含：
- `dist/index.html`
- `dist/assets/index-xxx.js`
- `dist/assets/index-xxx.css`

### 步骤 4：构建后端
```bash
cd api/
pip install -r requirements.txt
```
Vercel 把 `api/index.py` 及其依赖打包成一个可部署的 Serverless Function。

### 步骤 5：统一托管
Vercel 把前端 `dist/` 静态文件放到全球 CDN，同时把 `api/index.py` 注册到边缘节点。最终分配给你一个域名，比如 `https://xtwq-home-xxx.vercel.app`。

---

## 四、前后端联调原理：为什么"零跨域"？

### 传统前后端分离的痛点
如果你的前端在 `vercel.app`，后端在你家电脑的 `localhost:8000`：

```javascript
fetch('http://192.168.1.5:8000/api/hello')
```
浏览器会报 **CORS 错误**，而且你还需要内网穿透（花生壳/ngrok）才能让公网访问到本地 IP。

### xtwqHome 的解决方案
因为你的前端和后端**都部署在同一个 Vercel 项目上，共享同一个域名**：

```
首页:     https://xtwq-home-xxx.vercel.app/
前端JS:   https://xtwq-home-xxx.vercel.app/assets/index-xxx.js
后端API:  https://xtwq-home-xxx.vercel.app/api/hello
```

前端代码里写的是：
```javascript
fetch('/api/hello')
```
这个请求和前端页面**同源（Same-Origin）**，所以浏览器不会触发任何跨域拦截。这就是"零跨域"的根本原因。

---

## 五、本地开发 vs 线上部署

### 本地开发（需要同时开两个终端）

**终端 1 — 前端：**
```bash
npm run dev
# 启动在 http://localhost:5173
```

**终端 2 — 后端：**
```bash
python -m uvicorn api.index:app --reload --port 8000
# 启动在 http://localhost:8000
```

此时前端请求 `/api/hello`，因为 `vite.config.js` 里配置了 `proxy`，会被转发到 `localhost:8000/api/hello`。你在本地就能完整联调。

### 线上部署（只需要 push 代码）
```bash
git add .
git commit -m "你的修改"
git push origin main
```
Vercel 自动完成剩下的所有事情。你不需要维护服务器，不需要内网穿透。

---

## 六、踩坑记录（真实遇到的问题和解决）

### 坑 1：`Unexpected token '<'` JSON 解析错误
**现象：** 调用 `/api/hello` 时，前端报 `Unexpected token '<', "<!DOCTYPE "... is not valid JSON`。

**原因：** `vercel.json` 的路由重写规则写成了 `/api/(.*)` → `/api/$1`，但 Vercel 找不到 `/api/hello` 这个文件，于是 fallback 到了 `index.html`，返回了 HTML。

**解决：** 把规则改为 `/api/(.*)` → `/api/index.py`，让所有 `/api/*` 请求都交给 FastAPI 处理。

### 坑 2：`{"detail": "Not Found"}`
**现象：** 请求成功到达 FastAPI，但返回 404。

**原因：** FastAPI 里注册的路由是 `/hello`，但 Mangum 传递的完整路径是 `/api/hello`，路径不匹配。

**解决：** 使用 `APIRouter(prefix="/api")`，让 FastAPI 的路由也带上 `/api` 前缀。

### 坑 3：误提交 `node_modules/` 到 Git
**现象：** 仓库体积暴增到 55MB。

**解决：** 添加 `.gitignore` 忽略 `node_modules/` 和 `dist/`，并从 Git 历史里移除已提交的这些文件。

---

## 七、总结

| 问题 | 答案 |
|------|------|
| 前端是什么框架？ | Vue 3 + Vite |
| 后端是什么语言？ | Python + FastAPI |
| 部署在哪里？ | Vercel（前后端同仓） |
| 为什么不需要内网穿透？ | 后端也跑在 Vercel 云端，不是本地电脑 |
| 为什么没有跨域？ | 前后端共享同一个域名 |
| Vercel 怎么识别后端？ | `api/` 目录下的 `.py` 文件自动变成 Serverless Function |
| 本地怎么开发？ | `npm run dev` + `uvicorn api.index:app --port 8000` |
| 每次 push 会自动部署吗？ | 是的，Vercel 会自动重新构建并上线 |

---

## 八、延伸阅读

- [Vite 官方文档](https://cn.vitejs.dev/)
- [Vue 3 官方文档](https://cn.vuejs.org/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [Vercel Serverless Functions](https://vercel.com/docs/functions)
- [Mangum GitHub](https://github.com/jordaneremieff/mangum)

---

祝你学习愉快！🚀
