---
source: hn
url: https://www.johndcook.com/blog/2026/03/01/tilde-dash/
published_at: '2026-03-03T23:27:44'
authors:
- ibobev
topics:
- bash-shell
- command-line
- shell-variables
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# Shell Variable

## Summary
这不是一篇研究论文，而是一则关于 Bash shell 小技巧的短文，介绍了 `~-` 作为上一个工作目录（`$OLDPWD`）的快捷写法。它的价值在于提高命令行中两个目录之间切换与文件比较的效率。

## Problem
- 文章要解决的问题是：用户经常在两个目录之间来回切换，但并不知道如何更方便地直接引用“上一个工作目录”。
- 这很重要，因为命令行工作流里频繁切目录、比较同名文件是常见需求，少量语法改进就能减少输入与出错概率。
- 文中还顺带澄清了一个认知问题：`~-` 并不是新特性，而是 Bash 自 1989 年起就支持的功能。

## Approach
- 核心机制非常简单：`~-` 是 shell 展开语法，等价于变量 `$OLDPWD`，即“上一次所在的工作目录”。
- 用户平时可用 `cd -` 返回上一个目录；而 `~-` 则允许在命令参数中直接引用该目录路径。
- 最直接的使用方式是跨两个目录比较同名文件，例如：`diff notes.org ~-/notes.org`。
- 文章通过个人使用场景说明，这个语法特别适合在两个目录间反复切换时减少路径输入。

## Results
- 文中没有提供实验、基准或定量评测结果，因此没有论文式指标、数据集或基线比较可报告。
- 最强的具体结论是：`~-` 可作为 `$OLDPWD` 的快捷写法，用于直接引用上一个工作目录。
- 给出的具体示例是：在当前目录执行 `diff notes.org ~-/notes.org`，即可比较当前目录与前一目录中的同名文件 `notes.org`。
- 文章声称该特性并非近期加入：它自 Bash 1989 年发布以来就已存在，并且更早来自 C shell。

## Link
- [https://www.johndcook.com/blog/2026/03/01/tilde-dash/](https://www.johndcook.com/blog/2026/03/01/tilde-dash/)
