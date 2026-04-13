<script setup>
import { ref } from 'vue'

const helloResult = ref(null)
const timeResult = ref(null)
const loadingHello = ref(false)
const loadingTime = ref(false)

async function callHello() {
  loadingHello.value = true
  try {
    const res = await fetch('/api/hello')
    helloResult.value = await res.json()
  } catch (e) {
    helloResult.value = { error: e.message }
  } finally {
    loadingHello.value = false
  }
}

async function callTime() {
  loadingTime.value = true
  try {
    const res = await fetch('/api/time')
    timeResult.value = await res.json()
  } catch (e) {
    timeResult.value = { error: e.message }
  } finally {
    loadingTime.value = false
  }
}
</script>

<template>
  <div class="container">
    <header>
      <h1>🏠 小桐大王的家</h1>
      <p class="subtitle">Vue 3 + Vite + FastAPI 全栈部署演示</p>
    </header>

    <main>
      <section class="card">
        <h2>技术栈</h2>
        <ul class="tech-list">
          <li><b>前端：</b>Vue 3 + Vite</li>
          <li><b>后端：</b>Python FastAPI</li>
          <li><b>部署：</b>Vercel（前后端同仓）</li>
        </ul>
      </section>

      <section class="card">
        <h2>FastAPI 接口测试</h2>
        <p class="hint">点击下方按钮，前端通过 <code>fetch('/api/xxx')</code> 调用后端接口：</p>

        <div class="api-group">
          <div class="api-item">
            <div class="api-url">GET /api/hello</div>
            <button class="btn primary" @click="callHello" :disabled="loadingHello">
              {{ loadingHello ? '请求中...' : '发送请求' }}
            </button>
            <pre v-if="helloResult" class="result">{{ JSON.stringify(helloResult, null, 2) }}</pre>
          </div>

          <div class="api-item">
            <div class="api-url">GET /api/time</div>
            <button class="btn primary" @click="callTime" :disabled="loadingTime">
              {{ loadingTime ? '请求中...' : '发送请求' }}
            </button>
            <pre v-if="timeResult" class="result">{{ JSON.stringify(timeResult, null, 2) }}</pre>
          </div>
        </div>
      </section>

      <section class="card">
        <h2>本地开发说明</h2>
        <p>在本地开发时，Vite 会自动把 <code>/api</code> 请求代理到 <code>http://127.0.0.1:8000</code>。</p>
        <p>因此你需要同时启动前端和后端：</p>
        <pre class="code-block"># 终端 1：启动前端
npm run dev

# 终端 2：启动 FastAPI 后端
python -m uvicorn api.index:app --reload --port 8000</pre>
      </section>
    </main>

    <footer>
      <p>Made by wtwq666 · Deployed on Vercel</p>
    </footer>
  </div>
</template>

<style>
:root {
  --bg: #0f172a;
  --card-bg: #1e293b;
  --text: #f1f5f9;
  --muted: #94a3b8;
  --accent: #38bdf8;
  --accent-hover: #0ea5e9;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
  padding: 60px 20px;
}

.container {
  max-width: 720px;
  margin: 0 auto;
}

header {
  text-align: center;
  margin-bottom: 40px;
}

header h1 {
  font-size: 2.8rem;
  background: linear-gradient(90deg, var(--accent), #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: var(--muted);
  font-size: 1.1rem;
  margin-top: 8px;
}

.card {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 28px;
  margin-bottom: 24px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.card h2 {
  color: var(--accent);
  font-size: 1.3rem;
  margin-bottom: 14px;
}

.tech-list {
  margin-left: 20px;
  color: var(--muted);
}

.tech-list li {
  margin-bottom: 8px;
}

.hint {
  color: var(--muted);
  margin-bottom: 16px;
}

.api-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.api-item {
  background: #0b1220;
  border-radius: 12px;
  padding: 18px;
}

.api-url {
  font-family: monospace;
  color: #a5b4fc;
  background: #1e293b;
  padding: 8px 12px;
  border-radius: 6px;
  display: inline-block;
  margin-bottom: 12px;
}

.btn {
  padding: 10px 18px;
  border-radius: 8px;
  border: none;
  background: var(--accent);
  color: #0f172a;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn:hover:not(:disabled) {
  background: var(--accent-hover);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.result {
  margin-top: 14px;
  padding: 14px;
  background: #0f172a;
  border-radius: 8px;
  color: #86efac;
  font-family: monospace;
  white-space: pre-wrap;
  min-height: 60px;
}

.code-block {
  margin-top: 14px;
  padding: 16px;
  background: #0b1220;
  border-radius: 12px;
  color: #a5b4fc;
  font-family: monospace;
  overflow-x: auto;
}

footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.9rem;
  margin-top: 20px;
}

code {
  background: #0b1220;
  padding: 2px 6px;
  border-radius: 4px;
  color: #a5b4fc;
}
</style>
