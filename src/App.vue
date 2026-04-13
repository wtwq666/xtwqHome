<script setup>
import { ref, onMounted, computed } from 'vue'
import MarkdownIt from 'markdown-it'

// Create a markdown-it instance
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})

// Function to render markdown
const renderMarkdown = (content) => {
  return md.render(content)
}

// 状态管理
const docsStructure = ref([])
const currentFile = ref(null)
const currentContent = ref('')
const loading = ref(false)
const error = ref('')
const expandedFolders = ref(new Set())
const breadcrumbs = ref([])
const activePath = ref('')

// 加载文档结构
async function loadDocsStructure() {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch('/api/docs')
    const data = await response.json()
    console.log('Docs structure:', data.structure)
    docsStructure.value = data.structure
  } catch (err) {
    error.value = 'Failed to load documentation structure'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// 加载文档内容
async function loadDocContent(path) {
  console.log('Loading doc content for path:', path)
  loading.value = true
  error.value = ''
  try {
    const response = await fetch(`/api/docs/${path}`)
    console.log('Response status:', response.status)
    const data = await response.json()
    console.log('Response data:', data)
    if (data.error) {
      throw new Error(data.error)
    }
    currentContent.value = data.content
    console.log('Current content set:', currentContent.value.substring(0, 100) + '...')
    currentFile.value = path
    activePath.value = path
    
    // 更新面包屑
    const pathParts = path.split('/')
    breadcrumbs.value = []
    let currentPath = ''
    for (const part of pathParts) {
      currentPath = currentPath ? `${currentPath}/${part}` : part
      breadcrumbs.value.push({
        name: part.replace('.md', ''),
        path: currentPath
      })
    }
    console.log('Breadcrumbs:', breadcrumbs.value)
  } catch (err) {
    error.value = `Failed to load document: ${err.message}`
    console.error(err)
  } finally {
    loading.value = false
    console.log('Loading complete')
  }
}

// 切换文件夹展开状态
function toggleFolder(path) {
  if (expandedFolders.value.has(path)) {
    expandedFolders.value.delete(path)
  } else {
    expandedFolders.value.add(path)
  }
}

// 检查文件夹是否展开
function isFolderExpanded(path) {
  return expandedFolders.value.has(path)
}

// 处理文件点击
function handleFileClick(file) {
  loadDocContent(file.path)
}

// 处理面包屑点击
function handleBreadcrumbClick(index) {
  const path = breadcrumbs.value[index].path
  if (path.endsWith('.md')) {
    loadDocContent(path)
  } else {
    // 展开所有父文件夹
    const pathParts = path.split('/')
    let currentPath = ''
    for (const part of pathParts) {
      currentPath = currentPath ? `${currentPath}/${part}` : part
      expandedFolders.value.add(currentPath)
    }
  }
}

// 初始化
onMounted(async () => {
  await loadDocsStructure()
  // 自动展开所有文件夹
  expandAllFolders(docsStructure.value)
  // 自动加载第一个文档
  if (docsStructure.value.length > 0) {
    const firstFolder = docsStructure.value[0]
    if (firstFolder.children && firstFolder.children.length > 0) {
      const firstFile = firstFolder.children[0]
      if (firstFile.type === 'file') {
        console.log('Auto loading first file:', firstFile)
        await loadDocContent(firstFile.path)
      }
    }
  }
})

// 自动展开所有文件夹
function expandAllFolders(items) {
  for (const item of items) {
    if (item.type === 'directory') {
      expandedFolders.value.add(item.path)
      if (item.children && item.children.length > 0) {
        expandAllFolders(item.children)
      }
    }
  }
}

// 计算属性：是否有文档内容加载
const hasContent = computed(() => currentContent.value !== '')

// 计算属性：渲染后的Markdown内容
const renderedContent = computed(() => {
  if (!currentContent.value) return ''
  console.log('Rendering markdown...')
  const result = renderMarkdown(currentContent.value)
  console.log('Rendered content length:', result.length)
  return result
})
</script>

<template>
  <div class="app">
    <!-- 侧边栏导航 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>📚 教程文档</h1>
      </div>
      <nav class="sidebar-nav">
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <ul v-else class="nav-tree">
          <li 
            v-for="item in docsStructure" 
            :key="item.path"
            @click="item.type === 'file' ? handleFileClick(item) : toggleFolder(item.path)"
            style="cursor: pointer;"
          >
            <template v-if="item.type === 'directory'">
              <div 
                class="nav-item directory" 
                style="display: flex; align-items: center; padding: 8px 20px;"
              >
                <span class="icon">{{ isFolderExpanded(item.path) ? '📁' : '📂' }}</span>
                <span class="name">{{ item.name }}</span>
              </div>
              <ul v-if="isFolderExpanded(item.path)" class="nav-children">
                <li 
                  v-for="child in item.children" 
                  :key="child.path"
                  @click="child.type === 'file' ? handleFileClick(child) : toggleFolder(child.path)"
                  style="cursor: pointer;"
                >
                  <div 
                    v-if="child.type === 'file'"
                    class="nav-item file" 
                    :class="{ active: currentFile === child.path }"
                    style="display: flex; align-items: center; padding: 8px 20px;"
                  >
                    <span class="icon" style="margin-right: 10px;">📄</span>
                    <span class="name">{{ child.name }}</span>
                  </div>
                  <div 
                    v-else
                    class="nav-item directory"
                    style="display: flex; align-items: center; padding: 8px 20px;"
                  >
                    <span class="icon" style="margin-right: 10px;">{{ isFolderExpanded(child.path) ? '📁' : '📂' }}</span>
                    <span class="name">{{ child.name }}</span>
                  </div>
                </li>
              </ul>
            </template>
            <template v-else>
              <div 
                class="nav-item file" 
                :class="{ active: currentFile === item.path }"
                style="display: flex; align-items: center; padding: 8px 20px;"
              >
                <span class="icon" style="margin-right: 10px;">📄</span>
                <span class="name">{{ item.name }}</span>
              </div>
            </template>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- 主内容区域 -->
    <main class="content">
      <header class="content-header">
        <h1>🏠 小桐大王的家</h1>
        <p class="subtitle">Vue 3 + Vite + FastAPI 全栈部署演示</p>
      </header>

      <!-- 面包屑导航 -->
      <div v-if="breadcrumbs.length > 0" class="breadcrumbs">
        <span 
          v-for="(crumb, index) in breadcrumbs" 
          :key="index"
          class="crumb"
          @click="handleBreadcrumbClick(index)"
        >
          {{ crumb.name }}
          <span v-if="index < breadcrumbs.length - 1" class="separator">/</span>
        </span>
      </div>

      <!-- 文档内容 -->
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="hasContent" class="doc-content">
        <div v-html="renderedContent"></div>
      </div>
      <div v-else class="welcome">
        <h2>欢迎使用教程文档系统</h2>
        <p>请从左侧导航栏选择一个文档开始阅读</p>
        <div class="feature-list">
          <div class="feature-item">
            <h3>📁 文件夹结构</h3>
            <p>按类别组织的教程文档</p>
          </div>
          <div class="feature-item">
            <h3>📄 Markdown 渲染</h3>
            <p>支持代码块、图片等 Markdown 元素</p>
          </div>
          <div class="feature-item">
            <h3>📱 响应式设计</h3>
            <p>适配桌面和移动设备</p>
          </div>
        </div>
        <div style="margin-top: 30px;">
          <button @click="loadDocContent('git/git-branching.md')" style="padding: 10px 20px; background: var(--accent); color: #0f172a; border: none; border-radius: 8px; cursor: pointer;">测试加载 Git 分支管理文档</button>
        </div>
      </div>

      <footer class="content-footer">
        <p>Made by wtwq666 · Deployed on Vercel</p>
      </footer>
    </main>
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
  --border: #334155;
  --sidebar-bg: #1e293b;
  --content-bg: #0f172a;
  --code-bg: #1e293b;
  --code-text: #a5b4fc;
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
}

.app {
  display: flex;
  min-height: 100vh;
}

/* 侧边栏样式 */
.sidebar {
  width: 300px;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid var(--border);
}

.sidebar-header h1 {
  font-size: 1.5rem;
  color: var(--accent);
}

.sidebar-nav {
  padding: 10px 0;
}

.nav-tree {
  list-style: none;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 8px 20px;
  cursor: pointer;
  transition: background 0.2s;
}

.nav-item:hover {
  background: rgba(56, 189, 248, 0.1);
}

.nav-item.active {
  background: rgba(56, 189, 248, 0.2);
  border-left: 3px solid var(--accent);
}

.nav-item .icon {
  margin-right: 10px;
  font-size: 1.1rem;
}

.nav-item .name {
  flex: 1;
}

.nav-children {
  list-style: none;
  margin-left: 20px;
}

/* 主内容区域样式 */
.content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: var(--content-bg);
}

.content-header {
  text-align: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}

.content-header h1 {
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

/* 面包屑导航 */
.breadcrumbs {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  font-size: 0.9rem;
  color: var(--muted);
}

.crumb {
  cursor: pointer;
  transition: color 0.2s;
}

.crumb:hover {
  color: var(--accent);
}

.separator {
  margin: 0 8px;
}

/* 文档内容样式 */
.doc-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: var(--card-bg);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.doc-content h1, .doc-content h2, .doc-content h3, .doc-content h4, .doc-content h5, .doc-content h6 {
  color: var(--accent);
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.doc-content p {
  margin-bottom: 1em;
}

.doc-content ul, .doc-content ol {
  margin-left: 20px;
  margin-bottom: 1em;
}

.doc-content li {
  margin-bottom: 0.5em;
}

.doc-content code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--code-text);
  font-family: monospace;
}

.doc-content pre {
  background: var(--code-bg);
  padding: 16px;
  border-radius: 12px;
  overflow-x: auto;
  margin-bottom: 1em;
}

.doc-content pre code {
  background: none;
  padding: 0;
  color: var(--code-text);
}

.doc-content blockquote {
  border-left: 4px solid var(--accent);
  padding-left: 16px;
  margin: 1em 0;
  color: var(--muted);
}

/* 欢迎页面 */
.welcome {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  padding: 40px;
  background: var(--card-bg);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.welcome h2 {
  color: var(--accent);
  margin-bottom: 20px;
}

.welcome p {
  color: var(--muted);
  margin-bottom: 40px;
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.feature-item {
  padding: 20px;
  background: rgba(56, 189, 248, 0.1);
  border-radius: 12px;
  transition: transform 0.2s;
}

.feature-item:hover {
  transform: translateY(-5px);
}

.feature-item h3 {
  color: var(--accent);
  margin-bottom: 10px;
}

.feature-item p {
  color: var(--muted);
  margin-bottom: 0;
}

/* 加载和错误状态 */
.loading, .error {
  text-align: center;
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
  background: var(--card-bg);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.error {
  color: #ef4444;
}

/* 页脚 */
.content-footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.9rem;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: 200px;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
  
  .content {
    flex: 1;
  }
  
  .content-header h1 {
    font-size: 2rem;
  }
  
  .feature-list {
    grid-template-columns: 1fr;
  }
}
</style>
