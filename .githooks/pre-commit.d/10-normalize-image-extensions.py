#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys


IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.svg'}
REVIEW_NEEDED = 2


def log(message):
    prefix = os.environ.get("GITHOOK_LOG_PREFIX", "")
    print(f"{prefix}image: {message}", flush=True)


def get_staged_files():
    """获取暂存区中的文件列表"""
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only'],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


def rename_with_git(file, new_file):
    """使用 git mv 重命名，兼容大小写不敏感的文件系统"""
    temp_file = f"{new_file}.__rename_tmp__"
    counter = 1

    while os.path.exists(temp_file):
        temp_file = f"{new_file}.__rename_tmp__{counter}"
        counter += 1

    subprocess.run(['git', 'mv', '-f', '--', file, temp_file], check=True)
    subprocess.run(['git', 'mv', '-f', '--', temp_file, new_file], check=True)


def rename_image_extensions(files):
    """将大写图片后缀名转换为小写"""
    renamed = False

    for file in files:
        if not os.path.isfile(file):
            continue
        _, ext = os.path.splitext(file)
        if ext.lower() in IMAGE_EXTENSIONS and ext != ext.lower():
            new_file = file[:-len(ext)] + ext.lower()
            rename_with_git(file, new_file)
            renamed = True
            log(f"renamed {file} -> {new_file}")

    return renamed


def main():
    files = get_staged_files()
    if not files:
        log("ok, no staged files")
        sys.exit(0)

    renamed = rename_image_extensions(files)

    if renamed:
        log("staged renamed image paths")
        sys.exit(REVIEW_NEEDED)

    log("ok, no uppercase image extensions found")
    sys.exit(0)


if __name__ == '__main__':
    main()
