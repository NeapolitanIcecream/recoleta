---
source: hn
url: https://ajchambeaud.com/blog/is-code-still-relevant/
published_at: '2026-03-02T22:58:56'
authors:
- facundo_olano
topics:
- ai-coding-agents
- software-engineering
- code-generation
- human-ai-collaboration
- developer-workflow
relevance_score: 0.92
run_id: materialize-outputs
---

# Is Code Still Relevant?

## Summary
这篇文章讨论了在 AI 编码代理快速进步后，程序员是否仍然重要，以及“写代码”本身在软件开发中的地位是否正在下降。作者的核心判断是：代码依然重要，但程序员的价值正从手写实现转向规格、架构、评审、测试与系统级判断。

## Problem
- 文章要解决的问题是：当 AI 已能生成大量代码时，**代码是否仍是软件工程的核心**，以及**程序员还扮演什么角色**。
- 这很重要，因为它直接影响软件工程的工作流、人才培养、初级岗位门槛，以及“非开发者是否能直接用 AI 产出软件”的行业判断。
- 作者还关注一个现实风险：如果把代码完全当黑盒交给代理，可能带来回归、架构退化和复杂度失控。

## Approach
- 这不是一篇实验论文，而是一篇**基于一线开发者长期实践的经验分析**：作者对比了 Copilot、ChatGPT、Cursor、Claude Code 等工具在真实开发中的作用变化。
- 核心机制可以概括为：**人负责提出需求、提供上下文、做架构和评审；AI 负责生成和修改代码；人再测试、纠偏和验收**。
- 作者描述了从“手写代码 + AI 补全”到“主要靠代理改代码”的迁移过程，强调高效前提是开发者仍理解实现细节，而不是盲目 YOLO 式放权。
- 文中进一步提出一种角色重构：程序员的主要价值正转移到**系统思维、调试、权衡取舍、把模糊需求转成可执行规格**，而不只是手工编码。

## Results
- 最明确的量化证据来自作者个人实践：**在过去 6 个月里，没有完全独立手写过一行代码**，说明 AI 代理已能覆盖其日常开发的大部分编码环节。
- 作者声称自使用 **Claude Code** 后，**几乎停止手动写代码**，并认为“手写代码已经显得太慢”；这是强烈的效率主张，但**文中没有给出正式基准、数据集或对照实验**。
- 相比早期工具，作者认为 **Copilot 的自动补全体验差且经常不符合意图**；**Cursor** 通过更自然的补全和 IDE 内上下文读取改善了体验；**Claude Code** 则进一步把流程推进到“提示—审阅—测试”为主的代理式开发。
- 作者给出的关键边界结论是：**当前 AI 代理对非开发者操作者效果仍不稳定**，更容易犯错和引入回归，因为他们通常不会识别循环依赖、临时补丁和架构漂移等问题。
- 对未来的 strongest claim 是：代码不会马上消失，也还不能成为完全黑盒；但在软件行业中，**代码会变得不那么显性，而程序员将更多承担产品、QA、架构与规范制定等多角色职责**。

## Link
- [https://ajchambeaud.com/blog/is-code-still-relevant/](https://ajchambeaud.com/blog/is-code-still-relevant/)
