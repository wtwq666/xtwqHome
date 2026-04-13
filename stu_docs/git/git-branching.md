# Git分支管理教程

## 1. 分支概述

分支是Git中非常强大的功能，它允许你在不影响主线开发的情况下进行并行开发。通过分支，你可以：
- 开发新功能
- 修复bug
- 进行实验性开发
- 保持代码库的整洁

## 2. 分支的工作原理

Git的分支本质上是指向提交对象的指针。当你创建一个分支时，Git只是创建了一个新的指针，而不会复制任何文件。

```
              HEAD
               |
               v
main: A --- B --- C
               |
feature:       D --- E
```

## 3. 基本分支操作

### 3.1 查看分支

```bash
# 查看本地分支
git branch

# 查看远程分支
git branch -r

# 查看所有分支（本地和远程）
git branch -a

# 查看分支的最后一次提交
git branch -v

# 查看已合并到当前分支的分支
git branch --merged

# 查看未合并到当前分支的分支
git branch --no-merged
```

### 3.2 创建分支

```bash
# 创建新分支
git branch feature-branch

# 创建并切换到新分支
git checkout -b feature-branch

# 从指定提交创建分支
git branch feature-branch commit_hash

# 从远程分支创建本地分支
git checkout -b local-branch origin/remote-branch
```

### 3.3 切换分支

```bash
# 切换到已存在的分支
git checkout main

# 切换到上一个分支
git checkout -

# 创建并切换到新分支
git checkout -b feature-branch
```

### 3.4 重命名分支

```bash
# 重命名本地分支
git branch -m old-branch new-branch

# 重命名当前分支
git branch -m new-branch
```

### 3.5 删除分支

```bash
# 删除本地分支（已合并）
git branch -d feature-branch

# 强制删除本地分支（未合并）
git branch -D feature-branch

# 删除远程分支
git push origin --delete feature-branch
```

## 4. 分支合并

### 4.1 基本合并

```bash
# 切换到目标分支
git checkout main

# 合并源分支到目标分支
git merge feature-branch
```

### 4.2 合并策略

Git提供了几种合并策略：

- **recursive**：默认策略，用于合并两个分支
- **octopus**：用于合并多个分支
- **ours**：使用当前分支的内容，忽略其他分支的更改
- **theirs**：使用其他分支的内容，忽略当前分支的更改
- **subtree**：用于子树合并

```bash
# 使用特定策略合并
git merge --strategy=recursive feature-branch
```

### 4.3 快进合并

当目标分支是源分支的直接祖先时，Git会执行快进合并，这意味着Git只是将目标分支的指针向前移动到源分支的位置。

```bash
# 禁用快进合并
git merge --no-ff feature-branch
```

### 4.4 冲突解决

当合并分支时，如果两个分支对同一文件的同一部分进行了不同的修改，就会发生冲突。

解决冲突的步骤：

1. 查看冲突文件：`git status`
2. 编辑冲突文件，手动解决冲突
3. 添加解决后的文件：`git add filename.txt`
4. 提交解决：`git commit -m "Resolve conflict"`

冲突标记示例：

```
<<<<<<< HEAD
当前分支的内容
=======
合并分支的内容
>>>>>>> feature-branch
```

### 4.5 查看合并历史

```bash
# 查看分支合并历史
git log --graph --oneline --all

# 查看简化的合并历史
git log --graph --oneline
```

## 5. 分支管理策略

### 5.1 长期分支

- **main/master**：主分支，用于发布稳定版本
- **develop**：开发分支，用于集成日常开发

### 5.2 短期分支

- **feature**：功能分支，用于开发新功能
- **bugfix**：bug修复分支，用于修复bug
- **hotfix**：热修复分支，用于修复生产环境的紧急问题
- **release**：发布分支，用于准备发布

### 5.3 Git Flow工作流

Git Flow是一种流行的分支管理工作流，它定义了一套严格的分支使用规范：

1. **main/master**：只包含已发布的代码
2. **develop**：集成所有开发工作
3. **feature**：从develop分支创建，完成后合并回develop
4. **release**：从develop分支创建，用于准备发布，完成后合并回main和develop
5. **hotfix**：从main分支创建，用于修复生产环境问题，完成后合并回main和develop

### 5.4 GitHub Flow工作流

GitHub Flow是一种更简单的分支管理工作流：

1. **main**：主分支，始终保持可部署状态
2. **feature**：从main分支创建，完成后通过Pull Request合并回main

### 5.5 GitLab Flow工作流

GitLab Flow是GitHub Flow的扩展，增加了环境分支：

1. **main**：主分支
2. **feature**：功能分支
3. **environment**：环境分支（如staging、production）

## 6. 高级分支操作

### 6.1 分支重基

重基（rebase）是一种将一个分支的更改应用到另一个分支的方法，它会改变提交历史。

```bash
# 切换到特性分支
git checkout feature-branch

# 重基到主分支
git rebase main

# 解决可能的冲突
# 继续重基
git rebase --continue

# 取消重基
git rebase --abort
```

### 6.2 交互式重基

交互式重基允许你在重基过程中修改提交历史。

```bash
# 重基最近5次提交
git rebase -i HEAD~5

# 编辑提交历史
# 选项：pick, reword, edit, squash, fixup, exec, drop
```

### 6.3 分支筛选

```bash
# 按提交数量筛选分支
git branch --sort=-committerdate

# 按名称筛选分支
git branch | grep feature
```

### 6.4 分支同步

```bash
# 同步远程分支到本地
git fetch origin

# 同步本地分支到远程
git push origin feature-branch

# 强制推送（谨慎使用）
git push origin feature-branch --force
```

## 7. 分支最佳实践

1. **保持分支整洁**：定期删除不再需要的分支
2. **分支命名规范**：使用有意义的分支名称，如`feature/login`, `bugfix/issue-123`
3. **频繁合并**：定期将主分支的更改合并到特性分支，减少冲突
4. **提交信息规范**：使用清晰、简洁的提交信息
5. **代码审查**：在合并分支前进行代码审查
6. **测试**：在合并分支前确保代码通过测试
7. **文档**：记录分支管理策略，确保团队成员了解

## 8. 常见问题解决

### 8.1 合并冲突

- **原因**：两个分支对同一文件的同一部分进行了不同的修改
- **解决方法**：手动编辑冲突文件，解决冲突后提交

### 8.2 分支丢失

- **原因**：删除了包含未合并更改的分支
- **解决方法**：使用`git reflog`找回丢失的提交，然后创建新分支

### 8.3 重基冲突

- **原因**：重基过程中遇到冲突
- **解决方法**：解决冲突后使用`git rebase --continue`继续重基，或使用`git rebase --abort`取消重基

### 8.4 远程分支不显示

- **原因**：本地分支没有与远程分支关联
- **解决方法**：使用`git fetch origin`获取远程分支信息，然后使用`git checkout -b local-branch origin/remote-branch`创建本地分支

## 9. 分支管理工具

### 9.1 Git命令行

Git自带的命令行工具是最基础、最强大的分支管理工具。

### 9.2 Git GUI工具

- **GitHub Desktop**：GitHub官方的GUI工具
- **GitKraken**：功能强大的Git GUI工具
- **SourceTree**：Atlassian开发的Git GUI工具
- **TortoiseGit**：Windows平台的Git GUI工具

### 9.3 IDE集成

大多数IDE都集成了Git功能，如：
- **Visual Studio Code**：内置Git支持
- **IntelliJ IDEA**：内置Git支持
- **Eclipse**：通过EGit插件支持Git

## 10. 学习资源

- [Git分支管理官方文档](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [GitHub分支管理指南](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches)
- [Git Flow工作流](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow工作流](https://docs.github.com/en/get-started/quickstart/github-flow)
- [GitLab Flow工作流](https://docs.gitlab.com/ee/topics/gitlab_flow.html)

---

本教程涵盖了Git分支管理的核心内容，希望对您的学习有所帮助。如有任何问题，请查阅官方文档或参考相关资源。