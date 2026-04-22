# Website Sync

这个目录存放与网站内容同步判定相关的辅助脚本和测试。

它的职责不是执行真正的网站同步，而是回答一个更小的问题：

这次变更里，是否包含会影响网站发布结果的内容。

## Files

- `detect_publish_affecting_changes.py`
  - 读取一组变更路径
  - 判断其中哪些路径属于 publish-affecting changes
  - 以 GitHub Actions output 的形式写出检测结果
- `tests/test_detect_publish_affecting_changes.py`
  - 验证当前路径判定规则是否符合预期

## What Counts as Publish-Affecting

当前规则大致如下。

会被视为 publish-affecting：

- 普通内容目录中的 `.md` 文档
- `resources/images/` 下的资源文件
- `resources/i18n/` 下的翻译 sidecar
- 目录中的 `images/` 或 `assets/` 资源文件

不会被视为 publish-affecting：

- 根目录或子目录中的 `README.md`
- `AGENTS.md`
- `.githooks/`
- `.kb-tools/`
- `__template__/`
- 任何路径片段以 `.` 开头的隐藏目录内容，例如 `.github/`

换句话说，这里的判定重点是：

- 内容正文是否变了
- 会被文章引用的资源是否变了
- 会影响发布结果的翻译 sidecar 是否变了

而仓库维护文档、工具脚本和模板本身，不属于网站发布内容。

## Usage

这个脚本主要由 GitHub Actions 调用。

在仓库根目录下，典型调用形式如下：

```powershell
python .kb-tools/website_sync/detect_publish_affecting_changes.py `
  --changed-file changed-files.txt `
  --github-output github-output.txt
```

其中：

- `--changed-file` 指向一个文本文件，里面每行是一个变更路径
- `--github-output` 指向一个输出文件，脚本会把结果追加写入这个文件

脚本会写出这些字段：

- `should_trigger`
- `matched_count`
- `matched_summary`

## Testing

在仓库根目录运行：

```powershell
python -m unittest discover -s .kb-tools/website_sync/tests
```

如果你调整了路径规则，请先更新或补充测试，再修改实现。

## Notes

- 这里的脚本只负责“是否应该触发网站同步”的判定
- 真正的 workflow orchestration 位于 `.github/workflows/`
- 如果你想理解完整链路，可以把这里和 `.github/workflows/README.md` 一起看
