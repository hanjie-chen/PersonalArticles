# KB Translator

这个目录存放 knowledge base 的翻译辅助工具。

如果你要修改这里的脚本，请先读完这个 README，再动代码。

## Files

- `list-candidates.py`
  - 扫描仓库，列出当前需要翻译或重翻的中文主稿
- `translate.py`
  - 调用 Codex CLI，把候选文章翻译到 `resources/i18n/<same-name>-en.md`
- `workflow.py`
  - 共享逻辑，包括候选检测、`source_blob` 判断、调用 Codex、写入英文稿
- `tests/`
  - 这套翻译工具的测试

## Usage

在仓库根目录运行：

```powershell
python .kb-tools/translator/list-candidates.py
python .kb-tools/translator/translate.py
```

也可以在 `translator/` 目录里运行：

```powershell
python .\list-candidates.py
python .\translate.py
```

常用参数：

- `--limit`
  - 限制本次列出或翻译的文章数量，默认是 `1`
- `--model`
  - 仅 `translate.py` 支持
  - 显式指定 Codex 模型；如果不传，就使用本机 Codex CLI 的默认模型
- `root_dir`
  - 可选
  - 默认会自动推导仓库根目录；只有在你想对别的目录做测试时才需要显式传入

例如：

```powershell
python .kb-tools/translator/list-candidates.py --limit 5
python .kb-tools/translator/translate.py --limit 1
python .kb-tools/translator/translate.py --limit 1 --model gpt-5.4
```

## How It Works

- 只把“可发布且目录中存在 `resources/images/` 的顶层 `.md`”视为可翻译主稿
- 英文稿路径固定为 `resources/i18n/<same-name>-en.md`
- 英文稿顶部会写入一行：

```md
<!-- source_blob: <git-blob-hash> -->
```

- 如果英文稿不存在，则状态为 `missing_translation`
- 如果英文稿存在，但 `source_blob` 和当前中文主稿不一致，则状态为 `outdated_translation`
- `translate.py` 遇到 `missing_translation` 或 `outdated_translation` 时，会整篇重写英文稿，不做增量更新
- 如果翻译失败：
  - 不会创建半成品文件
  - 已有英文稿也不会被覆盖

## Testing

在仓库根目录运行：

```powershell
python -m unittest discover -s .kb-tools/translator/tests
```

## Notes

- 这套工具目前是手动命令，不是定时 automation，也不是 pre-push hook
- 如果后面要调整判定规则、输出格式或翻译 prompt，优先修改 `workflow.py`
