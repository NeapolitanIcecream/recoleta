---
source: arxiv
url: https://arxiv.org/abs/2606.13608v1
published_at: '2026-06-11T17:23:54'
authors:
- Xiaoyuan Liu
- Jianhong Tu
- Yuqi Chen
- Siyuan Xie
- Sihan Ren
- Tianneng Shi
- Gal Gantar
- Evan Sandoval
- Donghyun Lee
- Daniel Miao
- Peter J. Gilbert
- Nick Hynes
- Mauro Staver
- Warren He
- David Marn
- Andrew Low
- Xi Zhang
- Elron Bandel
- Michal Shmueli-Scheuer
- Siva Reddy
- Alexandre Drouin
- Alexandre Lacoste
- Ramayya Krishnan
- Elham Tabassi
- Yu Su
- Victor Barres
- Chenguang Wang
- Wenbo Guo
- Dawn Song
topics:
- agent-evaluation
- benchmark-standardization
- multi-agent-systems
- a2a
- mcp
- reproducibility
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# AgentBeats: Agentifying Agent Assessment for Openness, Standardization, and Reproducibility

## Summary
## 总结
AgentBeats 提出 Agentified Agent Assessment（AAA），把基准测试做成一个裁判代理，通过 A2A 和 MCP 与被测代理交互来评估它们。它针对固定基准脚手架与不同真实代理之间的不匹配，主张这种方式能提高开放性、标准化、互操作性和可复现性。

## 问题
- 代理评估是碎片化的：每个基准都有自己的脚手架，以及对输入、工具和控制方式的假设。
- 把很多代理和很多基准逐一集成，会产生 N x M 的定制工作，限制覆盖范围和公平性。
- 基准设置常常和生产环境不同，因此报告分数可能遗漏真实世界中的行为和风险。

## 方法
- AAA 把基准本身当作一个代理，由它负责任务、工具、评分和报告。
- 裁判代理和被测代理通过 A2A 进行任务管理，通过 MCP 进行工具访问，因此基准不再需要为每个代理单独做一个定制接口。
- 基准逻辑可以用两种方式内化：程序化内化，把原始评估流程写死；语义内化，用自然语言表达评估流程。
- AgentBeats 用五种运行模式实现 AAA，以适配开放性、隐私和可复现性的约束。
- 这个工作流有三个角色：发起评估的委托方、运行基准的裁判代理，以及一个或多个被评估的被测代理。

## 结果
- 论文报告了一场为期五个月的开放竞赛，包含 12 个类别中的 298 个裁判代理，以及来自独立参与者的 467 个被测代理。
- 这场竞赛把数十个基准代理化，覆盖编程、网页浏览、医疗保健和多代理游戏。
- 在一个编程案例研究中，代理化评估在可以对比的地方与公开记录一致，并补出了之前缺失的一对一结果。
- 作者还报告了模型与其原生脚手架之间的协同适配效应。
- 摘要没有给出标准基准指标表，因此最强的量化主张来自部署研究的规模，以及“保真度得到保持”这一结论。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13608v1](https://arxiv.org/abs/2606.13608v1)
