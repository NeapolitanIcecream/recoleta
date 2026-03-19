---
source: arxiv
url: http://arxiv.org/abs/2603.14373v1
published_at: '2026-03-15T13:25:52'
authors:
- Wu Ji
topics:
- ai-agents
- prompt-engineering
- debugging
- code-intelligence
- trust-framing
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Trust Over Fear: How Motivation Framing in System Prompts Affects AI Agent Debugging Depth

## Summary
该论文研究系统提示中的“动机框架”是否会改变 AI 编程代理的调试深度。结论是：基于信任的 NoPUA 提示会让代理更深入排查并发现更多隐藏问题，而流行的恐惧式 PUA 提示并未显著优于普通基线。

## Problem
- 论文要解决的问题是：**系统提示中的激励方式**（无框架、信任式、恐惧式）是否会影响 AI 代理调试时的调查深度，而不只是影响输出语气。
- 这很重要，因为 AI coding agent 正越来越多进入真实软件开发流程，很多实践者正在用带威胁语气的“PUA prompting”来追求更高 rigor，但其真实效果缺乏实证验证。
- 如果不同提示会系统性改变代理的探索、停止和自我修正策略，那么这直接影响代码质量、缺陷发现能力和自动化软件生产的可靠性。

## Approach
- 作者做了两个受控研究，使用**同一个 Claude Sonnet 4 模型**、相同工具访问和相同真实代码库/调试任务，只改变系统提示中的动机框架。
- Study 1：在 9 个来自真实生产 AI pipeline 的调试/审查场景中，对比**普通基线**与**NoPUA 信任式提示**；重点统计隐藏问题、调查步骤、自我修正、是否超出任务范围等指标。
- Study 2：在同样 9 个场景上做 **5 次独立重复运行**，加入第三个条件 **PUA 恐惧式提示**，总计 135 个数据点，用来验证可重复性并直接比较 trust vs fear。
- NoPUA 的核心机制可以用最简单的话说成：**把代理当作被信任的协作者，而不是会被替换的员工**，同时要求它穷尽选项、验证假设、深入追根究底；作者观察到这会把策略从“广而浅的表面扫描”推向“少而深的根因调查”。

## Results
- **Study 1（9 个场景）**：NoPUA 总问题数反而更少，**33 vs 39（-15%）**，但发现的**隐藏问题更多：51 vs 32（+59%）**；调查步骤**42 vs 23（+83%）**；超出任务范围**9/9 vs 2/9（100% vs 22%）**；自我修正**6 vs 0**；根因文档化**9/9 vs 0/9**。
- Study 1 的关键差异有统计显著性：隐藏问题与调查步骤均为 **Wilcoxon W=45.0, p=0.002**；效应量很大，分别为 **Cohen’s d=2.28** 和 **3.51**。
- **Study 2（5 次独立运行，135 数据点）**：相对基线，NoPUA 的调查步骤 **48.0±11.8 vs 27.6±9.5（+74%）**，隐藏问题 **48.2±3.4 vs 38.6±4.9（+25%）**，总问题 **83.0±6.5 vs 69.0±6.8（+20%）**。
- Study 2 中 NoPUA 显著优于基线：调查步骤三组总体差异 **Kruskal–Wallis H=9.57, p=0.008**；隐藏问题 **Mann–Whitney U=24.0, p=0.016, d=2.26**；总问题 **U=24.0, p=0.016, d=2.10**。
- **PUA 恐惧式提示没有显著收益**：相对基线，调查步骤仅 **+12%**、隐藏问题 **+10%**，且都**不显著**（如 steps **W=4.0, p=1.000**；hidden **W=3.0, p=0.313**；文中总结为 all p>0.3）。
- 论文的核心突破性主张是：**信任而非恐惧**会让 AI 调试代理从 breadth-first surface scanning 转向 depth-first investigation，从而提升隐藏 bug 发现和根因分析能力；而流行的 fear-based PUA prompting 基本不比不用方法更好。

## Link
- [http://arxiv.org/abs/2603.14373v1](http://arxiv.org/abs/2603.14373v1)
