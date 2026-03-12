---
source: hn
url: https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/
published_at: '2026-03-03T23:27:59'
authors:
- ibobev
topics:
- bash
- shell-scripting
- parameter-expansion
- file-extensions
relevance_score: 0.0
run_id: materialize-outputs
---

# File extensions in bash scripts – shell parameter expansion

## Summary
这篇文章介绍了 Bash 中用于处理文件扩展名的参数展开语法，展示了如何用极简脚本把 `.tex` 文件名转换为对应的 `.dvi` 和 `.svg` 文件名。核心价值在于用简洁且原生的 shell 机制解决脚本中非常常见的文件名改写问题。

## Problem
- 文章要解决的问题是：在 Bash 脚本里，如何把输入文件名的扩展名高效地替换成目标扩展名，例如把 `foo.tex` 变成 `foo.dvi` 和 `foo.svg`。
- 这很重要，因为文件扩展名转换是自动化脚本中的高频需求；如果处理繁琐、易错，就会降低 shell 脚本的可维护性和实用性。
- 作者强调 shell 语法虽然看起来简短甚至“晦涩”，但正因为它针对常见任务做了高度压缩，所以在这类场景下非常高效。

## Approach
- 核心方法是使用 Bash 参数展开 `${parameter%word}`，它会从变量值末尾删除与给定模式匹配的**最短**后缀。
- 在示例中，若输入参数 `$1` 为 `foo.tex`，则 `${1%.tex}` 会得到 `foo`，再拼接 `.dvi` 或 `.svg` 就能生成新文件名。
- 示例脚本先调用 `latex "$1"` 生成 DVI，再调用 `dvisvgm --no-fonts "${1%.tex}.dvi" -o "${1%.tex}.svg"` 生成 SVG。
- 用最简单的话说：先“去掉旧后缀”，再“加上新后缀”，全程不需要额外工具或复杂字符串处理。

## Results
- 文章没有提供正式实验、数据集或基准测试，因此**没有定量结果**可报告。
- 最具体的结果声明是：当输入为 `foo.tex` 时，`${1%.tex}` 会展开为 `foo`，进一步可得到 `foo.dvi` 和 `foo.svg`。
- 给出的完整脚本只需 **2 条命令**（`latex` 与 `dvisvgm`）以及 **1 个** Bash 参数展开模式，就能完成从 LaTeX 源文件到 SVG 输出文件名的自动转换。
- 作者的 strongest concrete claim 是：对于文件扩展名处理这类常见任务，Bash 的参数展开方式非常简洁，足以让 shell 脚本在某些场景下比改用 Python 更直接。

## Link
- [https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/](https://www.johndcook.com/blog/2026/02/28/file-extensions-bash/)
