# Vercel部署教程

## 1. Vercel简介

Vercel是一个全球分布式的云平台，专为前端应用、静态网站和无服务器函数设计。它提供了以下核心功能：
- 全球CDN加速
- 自动HTTPS
- 一键部署
- 持续集成/持续部署(CI/CD)
- 无服务器函数支持
- 环境变量管理
- 自定义域名支持

## 2. 账户注册与配置

### 2.1 注册Vercel账户

1. 访问[Vercel官网](https://vercel.com/)
2. 点击"Sign Up"按钮
3. 选择注册方式：
   - GitHub
   - GitLab
   - Bitbucket
   - 邮箱
4. 按照提示完成注册流程

### 2.2 账户设置

1. 登录Vercel后，点击右上角的头像，选择"Settings"
2. 在"Profile"页面，填写个人信息
3. 在"Billing"页面，设置支付方式（如果需要使用付费功能）
4. 在"Team"页面，创建或加入团队（如果需要团队协作）

## 3. 项目连接

### 3.1 从Git仓库导入项目

1. 登录Vercel后，点击"New Project"按钮
2. 选择Git提供商（GitHub、GitLab、Bitbucket）
3. 授权Vercel访问你的Git仓库
4. 选择要部署的仓库
5. 点击"Import"按钮

### 3.2 手动上传项目

1. 登录Vercel后，点击"New Project"按钮
2. 选择"Import Third-Party Git Repository"或"Deploy from Local Folder"
3. 按照提示上传项目文件或输入Git仓库URL

## 4. 构建命令设置

### 4.1 自动检测构建命令

Vercel会根据项目类型自动检测构建命令：
- **Next.js**：`next build`
- **React**：`npm run build`
- **Vue**：`npm run build`
- **Angular**：`ng build --prod`
- **Static Site Generators**：如Hugo、Jekyll等

### 4.2 手动设置构建命令

1. 在项目导入页面，展开"Configure Project"选项
2. 在"Build Command"字段中输入自定义构建命令
3. 在"Output Directory"字段中输入构建输出目录
4. 点击"Deploy"按钮

### 4.3 示例构建配置

| 项目类型 | 构建命令 | 输出目录 |
|---------|---------|---------|
| Next.js | `next build` | `.next` |
| React | `npm run build` | `build` |
| Vue | `npm run build` | `dist` |
| Angular | `ng build --prod` | `dist` |
| Gatsby | `gatsby build` | `public` |
| Hugo | `hugo` | `public` |

## 5. 环境变量配置

### 5.1 添加环境变量

1. 在Vercel控制台中，选择项目
2. 点击"Settings"选项卡
3. 点击"Environment Variables"
4. 点击"Add"按钮
5. 输入变量名和值
6. 选择环境（Development、Preview、Production）
7. 点击"Save"按钮

### 5.2 环境变量管理

- **批量添加**：点击"Import"按钮，上传包含环境变量的`.env`文件
- **变量继承**：Preview环境会继承Development环境的变量，Production环境需要单独设置
- **敏感变量**：Vercel会加密存储环境变量，确保安全性

### 5.3 环境变量使用

在项目代码中使用环境变量：

```javascript
// Next.js
export default function Home() {
  return <div>{process.env.NEXT_PUBLIC_API_URL}</div>;
}

// React (Create React App)
function App() {
  return <div>{process.env.REACT_APP_API_URL}</div>;
}
```

## 6. 部署流程

### 6.1 首次部署

1. 导入项目后，Vercel会自动开始构建和部署
2. 构建过程中，Vercel会执行构建命令，生成静态文件
3. 部署完成后，Vercel会提供一个默认域名（如`project-name.vercel.app`）
4. 点击域名可以访问部署后的应用

### 6.2 后续部署

- **Git推送**：当你向Git仓库推送代码时，Vercel会自动触发新的部署
- **手动部署**：在Vercel控制台中，选择项目，点击"Deployments"选项卡，点击"Redeploy"按钮

### 6.3 部署环境

Vercel提供三种部署环境：
- **Development**：本地开发环境
- **Preview**：预览环境，用于测试Pull Request
- **Production**：生产环境，面向用户的正式版本

## 7. 域名绑定

### 7.1 添加自定义域名

1. 在Vercel控制台中，选择项目
2. 点击"Settings"选项卡
3. 点击"Domains"
4. 输入自定义域名（如`example.com`）
5. 点击"Add"

### 7.2 DNS配置

1. 登录你的域名注册商（如GoDaddy、阿里云等）
2. 找到DNS设置
3. 添加以下DNS记录：
   - **A记录**：将域名指向Vercel的IP地址（如`76.76.21.21`）
   - **CNAME记录**：将子域名指向`cname.vercel-dns.com`
4. 等待DNS生效（通常需要10分钟到24小时）

### 7.3 HTTPS配置

Vercel会自动为自定义域名生成并配置HTTPS证书，无需手动操作。证书会在到期前自动续期。

## 8. 持续集成/持续部署设置

### 8.1 Git集成

Vercel与Git仓库深度集成：
- **自动部署**：当你向Git仓库推送代码时，Vercel会自动触发部署
- **Pull Request预览**：当你创建或更新Pull Request时，Vercel会自动创建预览部署
- **部署状态**：Vercel会在Git仓库中显示部署状态

### 8.2 部署配置文件

在项目根目录创建`vercel.json`文件，配置部署选项：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### 8.3 部署钩子

使用部署钩子触发部署：
1. 在Vercel控制台中，选择项目
2. 点击"Settings"选项卡
3. 点击"Deploy Hooks"
4. 输入钩子名称
5. 选择分支
6. 点击"Create Hook"
7. 使用生成的URL触发部署

## 9. 无服务器函数

### 9.1 创建无服务器函数

在项目中创建`api`目录，添加函数文件：

```javascript
// api/hello.js
module.exports = (req, res) => {
  res.status(200).json({ message: 'Hello World!' });
};
```

### 9.2 函数配置

在`vercel.json`中配置函数：

```json
{
  "version": 2,
  "functions": {
    "api/*.js": {
      "maxDuration": 10
    }
  }
}
```

### 9.3 函数访问

部署后，函数可以通过`https://project-name.vercel.app/api/hello`访问。

## 10. 监控与日志

### 10.1 部署日志

1. 在Vercel控制台中，选择项目
2. 点击"Deployments"选项卡
3. 点击具体部署的"View Logs"按钮
4. 查看构建和部署日志

### 10.2 函数日志

1. 在Vercel控制台中，选择项目
2. 点击"Functions"选项卡
3. 点击具体函数的"View Logs"按钮
4. 查看函数执行日志

### 10.3 性能监控

Vercel提供基本的性能监控：
- **部署时间**：构建和部署的时间
- **访问统计**：页面访问次数和响应时间
- **函数执行**：函数执行次数和响应时间

## 11. 常见问题排查

### 11.1 构建失败

- **原因**：依赖安装失败，构建命令错误，代码错误
- **解决方法**：
  1. 查看构建日志，定位错误信息
  2. 检查依赖配置（package.json）
  3. 检查构建命令是否正确
  4. 修复代码错误

### 11.2 部署成功但页面空白

- **原因**：路由配置错误，资源路径错误，API调用失败
- **解决方法**：
  1. 检查浏览器控制台错误
  2. 检查路由配置（如Next.js的路由）
  3. 检查资源路径是否正确
  4. 检查API调用是否成功

### 11.3 域名绑定失败

- **原因**：DNS配置错误，域名未实名认证
- **解决方法**：
  1. 检查DNS配置是否正确
  2. 等待DNS生效
  3. 确保域名已实名认证

### 11.4 环境变量不生效

- **原因**：环境变量未正确设置，变量名错误
- **解决方法**：
  1. 检查环境变量是否正确设置
  2. 确保变量名与代码中使用的一致
  3. 重新部署项目

### 11.5 函数执行失败

- **原因**：函数代码错误，依赖缺失，执行时间超限
- **解决方法**：
  1. 查看函数日志，定位错误信息
  2. 修复函数代码
  3. 确保依赖正确安装
  4. 优化函数执行时间

## 12. 最佳实践

1. **项目结构**：使用清晰的项目结构，便于Vercel检测和构建
2. **依赖管理**：使用package.json管理依赖，确保依赖版本一致
3. **环境变量**：使用环境变量管理敏感信息，避免硬编码
4. **构建优化**：优化构建过程，减少构建时间
5. **缓存策略**：合理设置缓存策略，提高访问速度
6. **错误处理**：添加适当的错误处理，提高应用稳定性
7. **监控**：定期查看部署日志和性能监控，及时发现问题
8. **自动化**：使用Git hooks和CI/CD流程，自动化部署过程

## 13. Vercel CLI

### 13.1 安装Vercel CLI

```bash
# 使用npm安装
npm i -g vercel

# 使用yarn安装
yarn global add vercel
```

### 13.2 常用CLI命令

```bash
# 登录Vercel
vercel login

# 部署项目
vercel

# 部署到生产环境
vercel --prod

# 查看项目信息
vercel ls

# 查看部署历史
vercel deployments

# 配置环境变量
vercel env add

# 撤销部署
vercel remove
```

## 14. 高级配置

### 14.1 构建输出配置

在`vercel.json`中配置构建输出：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "next.config.js",
      "use": "@vercel/next"
    },
    {
      "src": "api/*.js",
      "use": "@vercel/node"
    }
  ]
}
```

### 14.2 路由配置

在`vercel.json`中配置路由：

```json
{
  "version": 2,
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/blog/(.*)",
      "dest": "/blog/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### 14.3 边缘网络配置

在`vercel.json`中配置边缘网络：

```json
{
  "version": 2,
  "regions": ["iad1", "sfo1", "fra1", "sin1"]
}
```

## 15. 学习资源

- [Vercel官方文档](https://vercel.com/docs)
- [Vercel CLI文档](https://vercel.com/docs/cli)
- [Vercel示例项目](https://vercel.com/examples)
- [Next.js部署指南](https://nextjs.org/docs/deployment)
- [Vercel博客](https://vercel.com/blog)

---

本教程涵盖了Vercel部署的各个方面，希望对您的学习有所帮助。如有任何问题，请查阅官方文档或参考相关资源。