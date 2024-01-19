# Git 速查表

这个速查表为已经对使用 git 有一定了解的 NetBox 贡献者提供了方便的参考。有关工具和工作流程的一般介绍，请参阅 GitHub 的指南 [Getting started with git](https://docs.github.com/en/get-started/getting-started-with-git/setting-your-username-in-git)。

## 常用操作

### 克隆存储库

这将复制一个远程 git 存储库（例如来自 GitHub）到您的本地工作站。它将在当前路径下创建一个以存储库名称命名的新目录。

``` title="命令"
git clone https://github.com/$org-name/$repo-name
```

``` title="示例"
$ git clone https://github.com/netbox-community/netbox
Cloning into 'netbox'...
remote: Enumerating objects: 95112, done.
remote: Counting objects: 100% (682/682), done.
remote: Compressing objects: 100% (246/246), done.
remote: Total 95112 (delta 448), reused 637 (delta 436), pack-reused 94430
Receiving objects: 100% (95112/95112), 60.40 MiB | 45.82 MiB/s, done.
Resolving deltas: 100% (74979/74979), done.
```

### 拉取新提交

要使用任何最近的上游提交更新您的本地分支，请运行 `git pull`。

``` title="命令"
git pull
```

``` title="示例"
$ git pull
remote: Enumerating objects: 1, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (1/1), done.
From https://github.com/netbox-community/netbox
   28bc76695..e0741cc9a  develop    -> origin/develop
Updating 28bc76695..e0741cc9a
Fast-forward
 docs/release-notes/version-3.3.md | 1 +
 netbox/netbox/settings.py         | 1 +
 2 files changed, 2 insertions(+)
```

### 列出分支

`git branch` 列出所有本地分支。将 `-a` 添加到此命令将列出本地（绿色）和远程（红色）分支。

``` title="命令"
git branch -a
```

``` title="示例"
$ git branch -a
* develop
  remotes/origin/10170-changelog
  remotes/origin/HEAD -> origin/develop
  remotes/origin/develop
  remotes/origin/feature
  remotes/origin/master
```

### 切换分支

要切换到不同的分支，请使用 `checkout` 命令。

``` title="命令"
git checkout $branchname
```

``` title="示例"
$ git checkout feature
Branch 'feature' set up to track remote branch 'feature' from 'origin'.
Switched to a new branch 'feature'
```

### 创建新分支

使用 `checkout` 命令的 `-b` 参数可以从当前分支创建一个新的 _本地_ 分支。

``` title="命令"
git checkout -b $newbranch
```

``` title="示例"
$ git checkout -b 123-fix-foo
Switched to a new branch '123-fix-foo'
```

### 重命名分支

要重命名当前分支，请使用带有 `-m` 参数（用于 "修改"）的 `git branch` 命令。

``` title="命令"
git branch -m $newname
```

``` title="示例"
$ git branch -m jstretch-testing
$ git branch
  develop
  feature
* jstretch-testing
```

### 合并分支

要将一个分支合并到另一个分支，请使用 `git merge` 命令。首先切换到 _目标_ 分支，然后将 _源_ 分支合并到其中。

``` title="命令"
git merge $sourcebranch
```

``` title="示例"
$ git checkout testing 
Switched to branch 'testing'
Your branch is up to date with 'origin/testing'.
$ git merge branch2 
Updating 9a12b5b5f..8ee42390b
Fast-forward
 newfile.py | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 newfile.py
```

!!! warning "避免合并远程分支"
    通常情况下，您应该避免合并存在于远程（上游）存储库的分支，比如 `develop` 和 `feature`：合并到这些分支应该通过 GitHub 上的拉取请求完成。只有在需要整合您在本地完成的工作时才合并分支。

### 显示待处理更改

在对存储库中的文件进行更改后，`git status` 将显示已创建、已修改和已删除文件的摘要。

``` title="命令"
git status
```

``` title="示例"
$ git status
On branch 123-fix-foo
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	foo.py

no changes added to commit (use "git add" and/or "git commit -a")
```

### 暂存已更改的文件

在创建新提交之前，必须暂存已修改的文件。通常使用 `git add` 命令来完成此操作。您可以指定特定路径，或者只需附加 `-A` 来自动暂存当前目录中的所有已更改文件。再次运行 `git status` 来验证哪些文件已被暂存。

``` title="命令"
git add -A
```

``` title="示例"
$ git add -A
$ git status
On branch 123-fix-foo
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	modified:   README.md
	new file:   foo.py

```

### 查看已暂存的文件

在创建新提交之前，彻底检查所有已暂存的更改是个好主意。可以使用 `git diff` 命令来完成此操作。附加 `--staged` 参数将显示已暂存的更改；省略它将显示尚未暂存的更改。

``` title="Command"
git diff --staged
```

``` title="Example"
$ git diff --staged
diff --git a/README.md b/README.md
index 93e125079..4344fb514 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,8 @@
+
+Added some lines here
+and here
+and here too
+
 <div align="center">
   <img src="https://raw.githubusercontent.com/netbox-community/netbox/develop/docs/netbox_logo.svg" width="400" alt="NetBox logo" />
 </div>
diff --git a/foo.py b/foo.py
new file mode 100644
index 000000000..e69de29bb
```

### 创建新提交

`git commit` 命令记录了您对当前分支的更改。使用 `-m` 参数指定提交消息。（如果省略，将打开文件编辑器以提供消息。）

``` title="命令"
git commit -m "修复 #123：修复了出现问题的东西"
```

``` title="示例"
$ git commit -m "修复 #123：修复了出现问题的东西"
[123-fix-foo 9a12b5b5f] 修复 #123：修复了出现问题的东西
 2 files changed, 5 insertions(+)
 create mode 100644 foo.py
```

!!! tip "自动关闭问题"
    GitHub 将根据提交消息中的 `Fixes:` 或 `Closes:` 来自动关闭引用的任何问题，当提交合并到存储库的默认分支时。鼓励贡献者在形成提交消息时遵循这种约定。（对于功能请求使用 "Closes"，对于错误使用 "Fixes"。）

### 推送提交到上游

一旦您在本地进行了提交，它就需要被推送到 _远程_ 存储库（通常称为 "origin"）。这可以使用 `git push` 命令来完成。如果这是一个尚不存在于远程存储库的新分支，那么在推送时需要为其设置上游。

``` title="命令"
git push -u origin $branchname
```

``` title="示例"
$ git push -u origin testing
Counting objects: 3, done.
Delta compression using up to 16 threads.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 377 bytes | 377.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
remote: 
remote: Create a pull request for 'testing' on GitHub by visiting:
remote:      https://github.com/netbox-community/netbox/pull/new/testing
remote: 
To https://github.com/netbox-community/netbox
 * [new branch]          testing -> testing
Branch 'testing' set up to track remote branch 'testing' from 'origin'.
```

!!! tip
    您可以应用以下 git 配置来自动为所有新分支设置上游。这样就不需要指定 `-u origin`。
    
    ```
    git config --global push.default current
    ```

## GitHub CLI 客户端

GitHub 提供了一个[免费的 CLI 客户端](https://cli.github.com/)，可以简化与 GitHub 存储库的许多交互方面。请注意，此实用程序与 `git` 分开，并且必须[单独安装](https://github.com/cli/cli#installation)。

本指南提供了一些常见操作的示例，但请务必查看[GitHub CLI 手册](https://cli.github.com/manual/)以获取可用命令的完整列表。

### 列出打开的拉取请求

``` title="命令"
gh pr list
```

``` title="示例"
$ gh pr list

在 netbox-community/netbox 中显示了 3 个打开的拉取请求中的 3 个

#10223  #7503 API Bulk-Create of Devices does not check Rack-Space  7503-bulkdevice             about 17 hours ago
#9716   Closes #9599: Add cursor pagination mode                    lyuyangh:cursor-pagination  about 1 month ago
#9498   Adds replication and adoption for module import             sleepinggenius2:issue_9361  about 2 months ago
```

### 检出拉取请求

此命令将自动检出与打开拉取请求关联的远程分支。

``` title="命令"
gh pr checkout $number
```

``` title="示例"
$ gh pr checkout 10223
Branch '7503-bulkdevice' set up to track remote branch '7503-bulkdevice' from 'origin'.
Switched to a new branch '7503-bulkdevice'
```

## 修复错误

### 修改先前的提交

有时您会发现自己忽略了必要的更改，需要重新提交。如果您尚未推送最近的提交并且只需要进行一两次小的修改，那么可以使用 `--amend` 参数而不是创建新提交来修改最近的提交。

首先，使用 `git add` 暂存所需的文件，并验证更改，然后使用 `git commit` 命令以 `--amend` 参数。您还可以附加 `--no-edit` 参数，如果希望保留以前的提交消息。

``` title="命令"
git commit --amend --no-edit
```

``` title="示例"
$ git add -A
$ git diff --staged
$ git commit --amend --no-edit
[testing 239b16921] Added a new file
 Date: Fri Aug 26 16:30:05 2022 -0400
 2 files changed, 1 insertion(+)
 create mode 100644 newfile.py
```

!!! danger "不要在推送后进行修改"
    除非您**确定**没有其他人正在处理相同的分支，否则不要修改已经推送到上游的提交。强制推送会

覆盖更改历史记录，这会破坏其他贡献者的提交。当有疑问时，请创建一个新的提交。

### 撤消最后一个提交

`git reset` 命令可用于撤消最近的提交。 (`HEAD~` 等效于 `HEAD~1`，引用了当前 HEAD 之前的提交。) 在进行更改并暂存更改后，使用 `-c ORIG_HEAD` 来替换错误的提交。

``` title="命令"
git reset HEAD~
```

``` title="示例"
$ git add -A
$ git commit -m "错误的提交"
[testing 09ce06736] 错误的提交
 Date: Mon Aug 29 15:20:04 2022 -0400
 1 file changed, 1 insertion(+)
 create mode 100644 BADCHANGE
$ git reset HEAD~
$ rm BADFILE
$ git add -A
$ git commit -m "修复提交"
[testing c585709f3] 修复提交
 Date: Mon Aug 29 15:22:38 2022 -0400
 1 file changed, 65 insertions(+), 20 deletions(-)
```

!!! danger "不要在推送后重置"
    重置仅适用于尚未推送到上游的本地更改。如果您已经向上游推送，使用 `git revert` 代替。这将创建一个_新的_提交，以撤销错误的提交，但确保保持 git 历史记录的完整性。

### 从上游进行变基

如果自从您最近拉取它以来，已将更改推送到上游分支，则尝试推送新的本地提交将失败：

```
$ git push
To https://github.com/netbox-community/netbox.git
 ! [rejected]            develop -> develop (fetch first)
error: failed to push some refs to 'https://github.com/netbox-community/netbox.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

要解决此问题，首先获取上游分支以更新本地副本，然后[变基](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)本地分支以包括新的更改。完成变基后，可以将本地提交推送到上游。

``` title="命令"
git fetch
git rebase origin/$branchname
```

``` title="示例"
$ git fetch
remote: Enumerating objects: 1, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (1/1), done.
From https://github.com/netbox-community/netbox
   815b2d8a2..8c35ebbb7  develop    -> origin/develop
$ git rebase origin/develop
First, rewinding head to replay your work on top of it...
Applying: Further tweaks to the PR template
Applying: Changelog for #10176, #10217
$ git push
Counting objects: 9, done.
Delta compression using up to 16 threads.
Compressing objects: 100% (9/9), done.
Writing objects: 100% (9/9), 1.02 KiB | 1.02 MiB/s, done.
Total 9 (delta 6), reused 0 (delta 0)
remote: Resolving deltas: 100% (6/6), completed with 5 local objects.
To https://github.com/netbox-community/netbox.git
   8c35ebbb7..ada745324  develop -> develop
```
