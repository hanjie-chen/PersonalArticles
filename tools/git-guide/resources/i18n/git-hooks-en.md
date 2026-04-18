---
Title: Git Hooks Usage Guide
SourceBlob: aa2cad30895b14a47419bd83b344928cea365446
---

```
BriefIntroduction: Use a Git hook to check image file extensions and convert them to lowercase. Because my website runs on Linux, it is case-sensitive. But I often edit Markdown on Windows, which is not case-sensitive. That means images can display correctly on Windows while returning 404 Not Found on my website.
```

<!-- split -->

# Before we begin

Suppose we run into a problem like this: in a Windows environment, we have a Git repository that contains images, and those image file extensions may use both uppercase and lowercase letters, such as `.PNG` and `.png`.

If we need to rename uppercase image extensions to lowercase, and also ensure that every future commit keeps image extensions lowercase, what should we do?

A straightforward idea is to first scan the existing image files, rename any uppercase extensions to lowercase, commit the change, and then `git push` it to GitHub.

The first problem we will encounter is that Windows file names are case-insensitive. Git does have a solution for this, which is to [enable case sensitivity](./Git使用指南#Git between different OS) specifically in the Git repository.

But how do we ensure that all future committed images also use lowercase extensions? We can try using Git Hooks to automatically trigger a script that we write ourselves.

# Git Hooks

Git Hooks are a scripting mechanism in Git that allows you to automatically run custom scripts before or after certain events in a Git repository. They can help you automate workflows, perform code quality checks, enforce commit conventions, and more.

Git Hooks are divided into two categories:

1. **Client-side Hooks**: Run in the local repository and respond to operations such as commit, merge, and push. They are commonly used for code formatting, code checks, commit message validation, and so on.
2. **Server-side Hooks**: Run in the remote repository (server) and respond to events such as receiving pushes or updating refs. They are commonly used to enforce commit policies, trigger continuous integration, and so on.

> [!note]
>
> server-side hooks:
>
> If you manage your own Git server, you can use server-side hooks to enforce stricter policies. For example, you can block commits containing certain keywords, or automatically deploy code after a push is received.
>
> **Note**: If you use a hosted Git platform such as GitHub or GitLab, you usually cannot customize server-side hooks. However, these platforms provide Webhooks, CI/CD integrations, and similar features that can achieve comparable results.

## `./git/hooks` dir

Git Hooks are stored in the `.git/hooks` directory of each repository. By default, this directory contains some example scripts ending with `.sample`.

```powershell
PS C:\Users\Plain\PersonalArticles\.git\hooks> ls

    Directory: C:\Users\Plain\PersonalArticles\.git\hooks

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---            1/8/2025  2:33 AM            478 applypatch-msg.sample
-a---            1/8/2025  2:33 AM            896 commit-msg.sample
-a---            1/8/2025  2:33 AM           4726 fsmonitor-watchman.sample
-a---            1/8/2025  2:33 AM            189 post-update.sample
-a---            1/8/2025  2:33 AM            424 pre-applypatch.sample
-a---            1/8/2025  2:33 AM           1649 pre-commit.sample
-a---            1/8/2025  2:33 AM            416 pre-merge-commit.sample
-a---            1/8/2025  2:33 AM           1374 pre-push.sample
-a---            1/8/2025  2:33 AM           4898 pre-rebase.sample
-a---            1/8/2025  2:33 AM            544 pre-receive.sample
-a---            1/8/2025  2:33 AM           1492 prepare-commit-msg.sample
-a---            1/8/2025  2:33 AM           2783 push-to-checkout.sample
-a---            1/8/2025  2:33 AM           2308 sendemail-validate.sample
-a---            1/8/2025  2:33 AM           3650 update.sample
```

These example scripts are templates you can use as references. If you want to enable a hook, simply remove the `.sample` extension, write your own script, and make sure the script has executable permission.

## Sharing Git Hooks in a Project

By default, Git Hooks are not added to version control, which means other users who clone the repository will not automatically get your hook scripts. To solve this, we can store the hook scripts inside the repository and configure `hooksPath`.

Create a directory in the repository to store hook scripts:

```bash
mkdir .githooks
```

Move your hook script into that directory:

```bash
mv .git/hooks/pre-commit .githooks/pre-commit
```

Tell Git to use the custom hooks directory:

```bash
git config core.hooksPath .githooks
```

Add the hooks directory to version control:

```bash
git add .githooks
git commit -m "Add git hooks"
```

This way, after other developers clone the repository, they will also get the hook scripts.

# Check uppercase image extensions

We use the `pre-commit` hook to automatically run a script before the `git commit` command. I chose Python because both my Windows and Linux environments have Python available.

Main function: before code is committed, automatically convert the extensions of all image files in the staging area whose extensions contain uppercase letters to lowercase.

pre-commit

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def get_staged_files():
    """获取暂存区中的文件列表"""
    result = subprocess.run(['git', 'diff', '--cached', '--name-only'], stdout=subprocess.PIPE, text=True)
    files = result.stdout.strip().split('\n')
    return files

def rename_image_extensions(files):
    """将大写图片后缀名转换为小写"""
    image_extensions = ['.PNG', '.JPG', '.JPEG', '.GIF', '.BMP', '.TIFF', '.SVG']
    renamed = False

    for file in files:
        if not os.path.isfile(file):
            continue
        _, ext = os.path.splitext(file)
        if ext.upper() in image_extensions and ext != ext.lower():
            new_file = file[:-len(ext)] + ext.lower()
            os.rename(file, new_file)
            # 更新暂存区的文件
            subprocess.run(['git', 'add', new_file])
            subprocess.run(['git', 'rm', '--cached', file])
            renamed = True
            print(f"rename file: {file} -> {new_file}")

    return renamed

def main():
    files = get_staged_files()
    if not files or files == ['']:
        sys.exit(0)

    renamed = rename_image_extensions(files)

    if renamed:
        print("image extension name lowercased, staging area updated")
        print("please confirm change, and run git commit again to commit")
        sys.exit(1)  # 终止提交，让用户检查更改
    else:
        sys.exit(0)  # 正常结束，允许提交

if __name__ == '__main__':
    main()
```

test

```powershell
PS C:\Users\Plain\PersonalArticles> touch test.PNG
Created new file: test.PNG
PS C:\Users\Plain\PersonalArticles> ls

    Directory: C:\Users\Plain\PersonalArticles

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----            1/8/2025  2:33 AM                __template__
d----            1/9/2025  6:59 AM                .githooks
d----            1/9/2025  3:46 AM                azure
d----            1/8/2025  2:33 AM                devops
d----            1/8/2025  2:33 AM                personal-growth
d----            1/8/2025  2:33 AM                system-setup
d----            1/8/2025  2:33 AM                technical
d----            1/8/2025  2:33 AM                tools-guide
-a---           1/10/2025  2:26 AM           1189 README.md
-a---           1/10/2025  2:27 AM              0 test.PNG

PS C:\Users\Plain\PersonalArticles> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        test.PNG

no changes added to commit (use "git add" and/or "git commit -a")
PS C:\Users\Plain\PersonalArticles> git add .
PS C:\Users\Plain\PersonalArticles> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md
        new file:   test.PNG

PS C:\Users\Plain\PersonalArticles> git commit -m "add test.PNG fiel to test pre-commit"
rm 'test.PNG'
rename file: test.PNG -> test.png
image extension name lowercased, staging area updated
please confirm change, and run git commit again to commit
PS C:\Users\Plain\PersonalArticles> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md
        new file:   test.png

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   tools-guide/git-guide/git-hooks.md

PS C:\Users\Plain\PersonalArticles> git commit -m "add test image"
[main 50b252f] add test image
 2 files changed, 2 insertions(+), 2 deletions(-)
 create mode 100644 test.png
PS C:\Users\Plain\PersonalArticles> git push
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (4/4), 399 bytes | 199.00 KiB/s, done.
Total 4 (delta 2), reused 1 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To github.com:hanjie-chen/PersonalArticles.git
   d29a98c..50b252f  main -> main
```

result

![pre-commit success](./resources/images/pre-commit-test.png)

## Code walkthrough

### File header:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

The first line, `#!/usr/bin/env python3`, is a Shebang used to specify that the script should be interpreted by `python3`. When the script is executed directly on a Unix/Linux system, the system will use the specified interpreter to run it.

> [!note]
>
> Pay special attention here: the system must have the `python3` environment variable available, not just the `python` environment variable. In the following case, the script will not run:
>
> ```shell
> ➜ articles git:(main) ✗ python3 --version
> ➜ articles git:(main) ✗ python --version
> Python 3.11.4
> ```
>
> It will fail, and there will be no error message at all.

The second line, `# -*- coding: utf-8 -*-`, specifies that the script file uses UTF-8 encoding, which is important for correctly handling strings that contain non-ASCII characters.

### Import the required modules:

```python
import os
import sys
import subprocess
```

- The `os` module provides functionality for interacting with the operating system, such as working with files and directories.
- The `sys` module provides functionality for interacting with the Python interpreter, such as exiting the program and accessing command-line arguments.
- The `subprocess` module allows us to start new processes, connect to their input/output/error pipes, and retrieve their return values.

### Get the list of files in the staging area:

```python
def get_staged_files():
    """获取暂存区中的文件列表"""
    result = subprocess.run(['git', 'diff', '--cached', '--name-only'], stdout=subprocess.PIPE, text=True)
    files = result.stdout.strip().split('\n')
    return files
```

- Use `subprocess.run` to execute the Git command `git diff --cached --name-only` and retrieve the list of changed files in the staging area.
  - `stdout=subprocess.PIPE` means the standard output of the subprocess is captured into `result.stdout`.
  - `text=True` means the output is handled as a string.
- Split the output by lines to get the file list `files`.

### Convert uppercase image extensions to lowercase:

```python
def rename_image_extensions(files):
    """将大写图片后缀名转换为小写"""
    image_extensions = ['.PNG', '.JPG', '.JPEG', '.GIF', '.BMP', '.TIFF', '.SVG']
    renamed = False

    for file in files:
        if not os.path.isfile(file):
            continue
        _, ext = os.path.splitext(file)
        if ext.upper() in image_extensions and ext != ext.lower():
            new_file = file[:-len(ext)] + ext.lower()
            os.rename(file, new_file)
            # 更新暂存区的文件
            subprocess.run(['git', 'add', new_file])
            subprocess.run(['git', 'rm', '--cached', file])
            renamed = True
            print(f"rename file: {file} -> {new_file}")

    return renamed
```

- Define a list `image_extensions` that contains uppercase image extensions.
- Iterate through the list of staged files:
  - Use `os.path.isfile(file)` to check whether the file exists in the working tree.
  - Use `os.path.splitext(file)` to split the file name and extension.
  - Check the following conditions:
    - `ext.upper() in image_extensions`: whether the file extension, converted to uppercase, is in the image extension list.
    - `ext != ext.lower()`: whether the extension contains uppercase letters.
  - If both conditions are met:
    - Use `ext.lower()` to convert the extension to lowercase and generate the new file name `new_file`.
    - Use `os.rename(file, new_file)` to rename the file.
    - Update the Git staging area:
      - `git add new_file`: add the new file to the staging area.
      - `git rm --cached file`: remove the old file from the staging area, but only from the index, not from the working tree.
    - Set `renamed = True` to indicate that at least one file was renamed.
    - Output the rename information.

### Main function entry point:

```python
def main():
    files = get_staged_files()
    if not files or files == ['']:
        sys.exit(0)

    renamed = rename_image_extensions(files)

    if renamed:
        print("image extension name lowercased, staging area updated")
        print("please confirm change, and run git commit again to commit")
        sys.exit(1)  # 终止提交，让用户检查更改
    else:
        sys.exit(0)  # 正常结束，允许提交

if __name__ == '__main__':
    main()
```

- Call `get_staged_files()` to get the list of files in the staging area.
- If there are no files in the staging area, the program exits normally and allows the commit to continue.
- Call `rename_image_extensions(files)` to process the files.
- Decide the next step based on the value of `renamed`:
  - If any files were renamed, output a message and stop the commit (`sys.exit(1)`) so the user can review the changes and commit again.
  - If no files were renamed, the program exits normally (`sys.exit(0)`) and allows the commit to continue.
