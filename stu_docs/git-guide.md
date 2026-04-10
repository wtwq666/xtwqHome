# Git 操作指南

> 一份简洁实用的 Git 入门与常用操作手册。

---

## 1. 配置 Git 用户信息

在首次使用 Git 前，需要先配置你的用户名和邮箱（只需配置一次）：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

查看当前配置：

```bash
git config --list
```

---

## 2. 创建 / 克隆仓库

### 2.1 克隆远程仓库

```bash
git clone https://github.com/用户名/仓库名.git
```

### 2.2 在本地初始化新仓库

```bash
cd 你的项目文件夹
git init
```

---

## 3. 日常工作流程

### 3.1 查看仓库状态

```bash
git status
```

### 3.2 添加文件到暂存区

```bash
# 添加单个文件
git add 文件名.md

# 添加所有改动
git add .
```

### 3.3 提交更改

```bash
git commit -m "本次提交的说明"
```

### 3.4 推送到远程仓库

```bash
# 第一次推送（建立追踪关系）
git push -u origin main

# 后续推送
git push
```

---

## 4. 常用查询命令

| 命令 | 作用 |
|------|------|
| `git log` | 查看提交历史 |
| `git log --oneline` | 简洁版提交历史 |
| `git remote -v` | 查看已关联的远程仓库地址 |
| `git branch` | 查看本地分支 |
| `git diff` | 查看尚未暂存的改动 |

---

## 5. 分支操作

```bash
# 创建新分支
git branch 新分支名

# 切换分支
git checkout 新分支名

# 创建并切换分支（快捷方式）
git checkout -b 新分支名

# 合并分支（先切换到目标分支，再执行合并）
git checkout main
git merge 新分支名

# 删除本地分支
git branch -d 新分支名
```

---

## 6. 拉取远程更新

在推送前，建议先拉取远程仓库的最新代码，避免冲突：

```bash
git pull
```

如果出现冲突，Git 会提示你手动编辑冲突文件，解决后再重新 `add` 和 `commit`。

---

## 7. 撤销与回退

```bash
# 撤销工作区的修改（未 add 前）
git checkout -- 文件名

# 撤销暂存区的文件（已 add 未 commit）
git reset HEAD 文件名

# 回退到上一个版本
git reset --hard HEAD^
```

---

## 8. 小贴士

- **提交信息要清晰**：尽量用简短明确的语言描述本次修改内容，例如 `fix: 修复登录按钮样式`。
- **提交前先拉取**：避免与远程代码产生冲突。
- **勤提交、勤推送**：不要等到积累了大量改动才提交，避免冲突和丢失代码。
- **`.gitignore`**：在项目根目录创建该文件，可以指定哪些文件或文件夹不被 Git 追踪（如临时文件、依赖目录等）。

---

祝你使用 Git 愉快！🎉
