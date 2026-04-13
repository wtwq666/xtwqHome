# Git基础命令教程

## 1. Git简介

Git是一个分布式版本控制系统，用于跟踪项目中文件的变化。它允许你：
- 跟踪代码历史
- 协作开发
- 回滚到之前的版本
- 创建分支进行并行开发

## 2. 安装Git

### Windows
1. 从[Git官网](https://git-scm.com/download/win)下载安装程序
2. 运行安装程序，按照默认选项进行安装
3. 安装完成后，打开命令提示符或Git Bash，输入`git --version`验证安装成功

### macOS
1. 使用Homebrew安装：`brew install git`
2. 或从[Git官网](https://git-scm.com/download/mac)下载安装程序
3. 安装完成后，打开终端，输入`git --version`验证安装成功

### Linux
1. Ubuntu/Debian：`sudo apt install git`
2. CentOS/RHEL：`sudo yum install git`
3. 安装完成后，打开终端，输入`git --version`验证安装成功

## 3. 初始化仓库

### 创建新仓库
```bash
# 创建并进入项目目录
mkdir my-project
cd my-project

# 初始化Git仓库
git init
```

### 克隆现有仓库
```bash
# 克隆远程仓库
git clone https://github.com/username/repository.git

# 克隆到指定目录
git clone https://github.com/username/repository.git my-directory
```

## 4. 基本工作流程

### 1. 查看状态
```bash
git status
```

### 2. 添加文件到暂存区
```bash
# 添加单个文件
git add filename.txt

# 添加所有文件
git add .

# 添加特定类型的文件
git add *.txt
```

### 3. 提交更改
```bash
# 提交暂存区的更改
git commit -m "提交信息"

# 提交所有更改（跳过暂存区）
git commit -a -m "提交信息"

# 修改上次提交
git commit --amend -m "新的提交信息"
```

### 4. 查看提交历史
```bash
# 查看所有提交历史
git log

# 查看简洁的提交历史
git log --oneline

# 查看最近n次提交
git log -n 5

# 查看提交历史的详细信息
git log --stat
```

### 5. 查看文件差异
```bash
# 查看工作区与暂存区的差异
git diff

# 查看暂存区与上次提交的差异
git diff --cached

# 查看两个提交之间的差异
git diff commit1 commit2
```

### 6. 撤销更改
```bash
# 撤销工作区的更改
git checkout -- filename.txt

# 撤销暂存区的更改
git reset HEAD filename.txt

# 回滚到指定提交
git reset --hard commit_hash
```

## 5. 远程仓库操作

### 1. 查看远程仓库
```bash
git remote -v
```

### 2. 添加远程仓库
```bash
git remote add origin https://github.com/username/repository.git
```

### 3. 推送更改到远程仓库
```bash
# 推送主分支到远程仓库
git push origin main

# 推送指定分支到远程仓库
git push origin feature-branch

# 推送所有分支
git push --all origin

# 推送标签
git push --tags origin
```

### 4. 从远程仓库拉取更改
```bash
# 拉取并合并远程更改
git pull origin main

# 只拉取不合并
git fetch origin
```

### 5. 移除远程仓库
```bash
git remote remove origin
```

## 6. 分支管理

### 1. 查看分支
```bash
# 查看本地分支
git branch

# 查看远程分支
git branch -r

# 查看所有分支
git branch -a
```

### 2. 创建分支
```bash
# 创建新分支
git branch feature-branch

# 创建并切换到新分支
git checkout -b feature-branch
```

### 3. 切换分支
```bash
git checkout main
```

### 4. 合并分支
```bash
# 切换到目标分支
git checkout main

# 合并源分支到目标分支
git merge feature-branch
```

### 5. 删除分支
```bash
# 删除本地分支
git branch -d feature-branch

# 强制删除本地分支
git branch -D feature-branch

# 删除远程分支
git push origin --delete feature-branch
```

## 7. 标签管理

### 1. 创建标签
```bash
# 创建轻量级标签
git tag v1.0.0

# 创建带注释的标签
git tag -a v1.0.0 -m "版本1.0.0"
```

### 2. 查看标签
```bash
git tag
```

### 3. 推送标签
```bash
git push origin v1.0.0

# 推送所有标签
git push origin --tags
```

### 4. 删除标签
```bash
# 删除本地标签
git tag -d v1.0.0

# 删除远程标签
git push origin --delete v1.0.0
```

## 8. 忽略文件

### 创建.gitignore文件
```bash
touch .gitignore
```

### .gitignore文件示例
```
# 操作系统文件
.DS_Store
Thumbs.db

# 编译产物
build/
dist/
*.class

# 依赖管理
node_modules/
venv/

# 编辑器配置
.vscode/
.idea/
*.swp
*.swo

# 环境变量
.env
.env.local

# 日志文件
logs/
*.log
```

## 9. 配置Git

### 1. 全局配置
```bash
# 设置用户名
git config --global user.name "Your Name"

# 设置邮箱
git config --global user.email "your.email@example.com"

# 设置默认编辑器
git config --global core.editor "code --wait"

# 设置差异比较工具
git config --global diff.tool vscode
git config --global difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"

# 启用彩色输出
git config --global color.ui true
```

### 2. 查看配置
```bash
git config --list

# 查看全局配置
git config --global --list
```

## 10. 常见问题解决

### 1. 冲突解决
当合并分支或拉取更改时，可能会遇到冲突。解决冲突的步骤：
1. 查看冲突文件：`git status`
2. 编辑冲突文件，手动解决冲突
3. 添加解决后的文件：`git add filename.txt`
4. 提交解决：`git commit -m "Resolve conflict"`

### 2. 撤销错误提交
```bash
# 撤销上次提交，但保留更改
git reset HEAD~1

# 撤销上次提交，丢弃更改
git reset --hard HEAD~1

# 撤销指定提交
git revert commit_hash
```

### 3. 找回丢失的提交
```bash
# 查看所有引用（包括已删除的提交）
git reflog

# 恢复到指定引用
git checkout HEAD@{1}
```

## 11. 最佳实践

1. **提交信息规范**：使用清晰、简洁的提交信息，描述更改的内容和原因
2. **定期提交**：频繁提交小的、有意义的更改，而不是一次性提交大量更改
3. **分支管理**：使用分支进行功能开发和bug修复，保持主分支的稳定性
4. **代码审查**：在合并分支前进行代码审查
5. **备份**：定期推送更改到远程仓库，确保代码安全
6. **忽略文件**：使用.gitignore文件排除不需要版本控制的文件
7. **标签管理**：使用标签标记重要的版本

## 12. 常用命令速查表

| 命令 | 描述 |
|------|------|
| `git init` | 初始化Git仓库 |
| `git clone` | 克隆远程仓库 |
| `git add` | 添加文件到暂存区 |
| `git commit` | 提交更改 |
| `git status` | 查看工作区状态 |
| `git log` | 查看提交历史 |
| `git diff` | 查看文件差异 |
| `git push` | 推送更改到远程仓库 |
| `git pull` | 从远程仓库拉取更改 |
| `git branch` | 管理分支 |
| `git checkout` | 切换分支 |
| `git merge` | 合并分支 |
| `git tag` | 管理标签 |
| `git remote` | 管理远程仓库 |
| `git config` | 配置Git |

## 13. 学习资源

- [Git官方文档](https://git-scm.com/doc)
- [Pro Git书籍](https://git-scm.com/book/en/v2)
- [GitHub Git教程](https://docs.github.com/en/get-started/using-git)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

本教程涵盖了Git的基础命令和使用方法，希望对您的学习有所帮助。如有任何问题，请查阅官方文档或参考相关资源。