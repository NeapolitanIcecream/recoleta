---
source: hn
url: https://www.johndcook.com/blog/2026/03/01/tilde-dash/
published_at: '2026-03-03T23:27:44'
authors:
- ibobev
topics:
- bash-shell
- shell-variables
- developer-productivity
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Shell Variable

## Summary
这篇短文介绍了 Bash shell 中一个少见但实用的路径简写 `~-`，它等价于上一工作目录变量 `$OLDPWD`。作者用一个常见的双目录切换场景说明了该特性如何让文件比较等操作更方便。

## Problem
- 文章要解决的问题是：在 shell 中频繁来回切换两个目录时，如何更方便地引用“上一个工作目录”中的文件，而不只是切回去。
- 这很重要，因为开发者常在两个目录之间对比、检查或处理同名文件，若只能靠 `cd -` 切换，命令会更绕、效率更低。
- 文章也顺带澄清一个可用性问题：这个功能长期存在，却不为很多用户所知。

## Approach
- 核心机制是 Bash 的 `~-` 展开：它是 shell 对“前一个工作目录”的简写，本质上等价于变量 `$OLDPWD`。
- 最简单理解：当前在目录 A，刚从目录 B 切过来，那么 `~-` 就表示 B。
- 作者给出的典型用法是，在当前目录直接访问上一个目录里的同名文件，例如：`diff notes.org ~-/notes.org`。
- 与 `cd -` 不同，`~-` 不是执行目录切换，而是在命令参数里直接引用前一个目录路径，因此更适合比较、复制、查看等操作。

## Results
- 文中没有提供正式实验、数据集或基准测试，因此**没有量化结果**可报告。
- 最强的具体结论是：`~-` 可作为 `$OLDPWD` 的快捷写法，用于直接引用前一个工作目录。
- 文章给出的明确示例是：对两个目录中的同名文件 `notes.org` 执行比较，命令为 `diff notes.org ~-/notes.org`。
- 作者还指出该特性**并非新功能**：它自 Bash 在 **1989 年**发布以来就已存在，并且更早就出现在 C shell 中。

## Link
- [https://www.johndcook.com/blog/2026/03/01/tilde-dash/](https://www.johndcook.com/blog/2026/03/01/tilde-dash/)
