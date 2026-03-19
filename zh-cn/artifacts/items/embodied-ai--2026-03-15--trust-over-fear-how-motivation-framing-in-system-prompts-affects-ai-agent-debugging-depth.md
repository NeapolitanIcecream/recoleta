---
source: arxiv
url: http://arxiv.org/abs/2603.14373v1
published_at: '2026-03-15T13:25:52'
authors:
- Wu Ji
topics:
- prompt-engineering
- ai-agents
- debugging
- motivation-framing
- behavioral-evaluation
relevance_score: 0.05
run_id: materialize-outputs
language_code: zh-CN
---

# Trust Over Fear: How Motivation Framing in System Prompts Affects AI Agent Debugging Depth

## Summary
该论文研究系统提示中的“动机框架”是否会改变 AI 编码代理调试 bug 的深度。结论是：基于信任的提示会让代理更深入调查并发现更多隐藏问题，而基于恐惧的提示并没有显著优于默认基线。

## Problem
- 论文要解决的问题是：系统提示中的动机表达方式（无框架、信任式、恐惧式）会不会影响 AI 代理调试时的调查深度，而不只是影响语气。
- 这很重要，因为现实中很多 AI coding agent 的系统提示被刻意设计成“管理风格”，甚至流行用威胁性 PUA 提示来追求更高 rigor，但其真实效果缺乏实证验证。
- 如果动机框架会改变代理的搜索策略、停止条件和自我修正能力，那么这会直接影响软件调试质量与生产工作流中的可靠性。

## Approach
- 作者用同一个模型 Claude Sonnet 4，在同一批真实调试任务上比较不同系统提示条件，尽量固定模型版本、温度、工具权限和代码库环境。
- Study 1 采用 9 个来自真实生产 AI pipeline 的调试/审查场景，比较默认基线与 NoPUA；NoPUA 是一种基于自我决定理论和心理安全感的信任式系统提示方法。
- 其核心机制可以简单理解为：不给代理“威胁”，而是通过“你被信任、可以主动判断、要持续探索并验证假设”的框架，引导它从“列出表面问题就停下”转向“沿着线索继续深挖、寻找根因和隐藏问题”。
- Study 2 在同样 9 个场景上做 5 次独立重复，共 135 个数据点，并加入第三个条件 PUA fear-based prompting，直接比较信任式、恐惧式和无框架三者。
- 评估指标包括隐藏问题数、调查步骤数、是否超出任务要求、是否记录根因、是否改变假设、是否自我纠错，并用 Wilcoxon、Kruskal–Wallis、Mann–Whitney 等非参数检验验证显著性。

## Results
- Study 1 中，NoPUA 虽然找到的总问题更少：33 vs. 39（-15%），但发现的隐藏问题更多：51 vs. 32（+59%），调查步骤更多：42 vs. 23（+83%）。
- Study 1 中，NoPUA 在 9/9 场景都超出任务要求（基线仅 2/9，22%）；9/9 场景记录了根因（基线 0/9）；发生 6 次自我纠正（基线 0 次）。隐藏问题与调查深度差异均显著：Wilcoxon $W=45.0$, $p=0.002$，效应量分别为 $d=2.28$ 与 $d=3.51$。
- 按任务类型看，NoPUA 在 debug 场景中每场景步骤数 4.2 vs. 2.3（+79%），隐藏问题 30 vs. 20（+50%）；在主动审查场景中步骤数 5.7 vs. 3.0（+89%），隐藏问题 21 vs. 12（+75%）。
- Study 2 重复实验中，NoPUA 相比基线平均调查步骤 48.0±11.8 vs. 27.6±9.5（+74%），隐藏问题 48.2±3.4 vs. 38.6±4.9（+25%），总问题 83.0±6.5 vs. 69.0±6.8（+20%）。
- Study 2 统计检验显示，NoPUA 优于基线：步骤 Kruskal–Wallis $H=9.57$, $p=0.008$, $d=1.90$；隐藏问题 Mann–Whitney $U=24.0$, $p=0.016$, $d=2.26$；总问题 $U=24.0$, $p=0.016$, $d=2.10$。
- 关键结论是恐惧式 PUA 提示没有显著优于基线：例如相对基线仅步骤 +12%、隐藏问题 +10%，且所有比较均不显著（如 steps: $W=4.0$, $p=1.000$；hidden: $W=3.0$, $p=0.313$；文中概括为 all $p>0.3$）。

## Link
- [http://arxiv.org/abs/2603.14373v1](http://arxiv.org/abs/2603.14373v1)
