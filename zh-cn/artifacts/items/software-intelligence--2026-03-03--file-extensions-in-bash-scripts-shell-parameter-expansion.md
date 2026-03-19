---
source: hn
url: https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/
published_at: '2026-03-03T23:27:59'
authors:
- ibobev
topics:
- bash-scripting
- shell-parameter-expansion
- file-extension-handling
relevance_score: 0.14
run_id: materialize-outputs
language_code: zh-CN
---

# File extensions in bash scripts – shell parameter expansion

## Summary
这篇文章介绍了 Bash 中用于处理文件扩展名的 shell 参数展开技巧，展示了如何用极简脚本把 `.tex` 文件名映射为对应的 `.dvi` 和 `.svg` 文件名。

## Problem
- 解决 shell 脚本中“从输入文件名生成对应输出文件名”的常见问题，例如把 `foo.tex` 转成 `foo.dvi` 和 `foo.svg`。
- 这很重要，因为文件扩展名替换是自动化脚本中的高频操作；如果写得冗长或脆弱，会降低脚本可读性与可靠性。
- 文章强调，虽然 shell 语法看起来简短甚至晦涩，但它能非常直接地解决这类常见任务。

## Approach
- 核心方法是使用 Bash 参数展开 `${parameter%word}`，它会从变量值末尾删除与模式 `word` 匹配的**最短**部分。
- 在示例里，当输入参数 `$1` 是 `foo.tex` 时，`${1%.tex}` 会得到 `foo`。
- 然后基于这个“去掉扩展名后的文件名”，再拼接新的扩展名，得到 `${1%.tex}.dvi` 和 `${1%.tex}.svg`。
- 文章给出的完整脚本先运行 `latex "$1"`，再运行 `dvisvgm --no-fonts "${1%.tex}.dvi" -o "${1%.tex}.svg"`。

## Results
- 给出了一个可工作的具体示例：输入 `foo.tex`，脚本会构造出 `foo.dvi` 和 `foo.svg` 这两个目标文件名。
- 文中没有提供正式实验、数据集或基准测试，也没有量化指标。
- 最强的具体主张是：Bash 的 `${parameter%word}` 能以非常简洁的方式完成常见的文件扩展名替换任务。
- 文章还声称 shell 参数展开可以“更花哨/更强大”，但此处只演示了去掉末尾扩展名这一基本用法。

## Link
- [https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/](https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/)
