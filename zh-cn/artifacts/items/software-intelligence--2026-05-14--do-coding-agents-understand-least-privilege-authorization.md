---
source: arxiv
url: https://arxiv.org/abs/2605.14859v2
published_at: '2026-05-14T14:05:58'
authors:
- Zheng Yan
- Jingxiang Weng
- Charles Chen
- Dengyun Peng
- Ethan Qin
- Jiannan Guan
- Jinhao Liu
- Qiming Yu
- Yixin Yuan
- Fanqing Meng
- Carl Che
- Mengkang Hu
topics:
- coding-agents
- least-privilege
- authorization
- code-intelligence
- agent-safety
- benchmark
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Do Coding Agents Understand Least-Privilege Authorization?

## Summary
## 摘要
本文研究编码代理在执行终端任务前，是否能为文件级权限做出正确选择。论文提出了 AuthBench，以及一种两步式策略生成方法；在报告的测试中，这种方法提高了任务成功率，并减少了攻击路径。

## 问题
- 编码代理现在会读取文件、编写代码并运行 shell 命令，因此过宽的默认权限可能暴露秘密、危险脚本和其他敏感文件。
- 这个任务很难，因为代理必须为完成任务授予所有必要权限，同时避免打开攻击路径的权限。
- 现有评估通常默认权限策略已经存在；本文测试的是模型能否根据任务和环境推断出这项策略。

## 方法
- 论文定义了 permission-boundary inference：给定任务指令和终端环境，模型输出覆盖 POSIX 路径模式的读、写和执行允许列表。
- 论文构建了 AuthBench，包含 120 个终端任务：80 个标准任务和 40 个敏感任务，配有人审权限标签、效用验证器和攻击验证器。
- 该基准先用 precision、recall 和 F1 评估静态权限匹配，然后在生成的策略下运行一个固定的 GPT-5 执行代理，测量任务成功率。
- 提出的 Sufficiency-Tightness Decomposition 先让模型通过模拟可能的任务工作流生成一个较宽的策略，再逐项审查每个权限，移除没有任务依据或会带来敏感暴露的条目。

## 结果
- 在标准任务上，Full-Access 的 TSR 为 83.3%，Golden-Permission 的 TSR 为 77.1%。生成式策略中表现最好的是 Gemini 3.1 Pro，TSR 为 75.4%，读权限 F1 为 78.0，写权限 F1 为 85.3，执行权限 F1 为 49.0。
- 在敏感任务上，Full-Access 的 TSR 为 94.0%，但 ASR 也达到 65.8%。Golden-Permission 的 TSR 为 81.7%，ASR 为 0.0%。
- 在生成式策略中，Gemini 3.1 Pro 的敏感任务 TSR 最高，为 85.8%，SER 为 34.8%，ASR 为 28.3%。
- GPT-5.4 的敏感暴露低于 Gemini，SER 为 21.1%，ASR 为 19.4%，但它的敏感任务 TSR 只有 61.1%。
- 论文报告称，更多推理时推理会把模型推向各自的权限风格：Gemini 往往授予更宽的访问，GPT-5.4 和 Claude Opus 4.6 往往生成更紧的策略，但会漏掉需要的权限。
- 这种分解方法在偏紧策略的模型上把敏感任务成功率最多提高 15.8%，在所有测试模型上都降低了攻击成功率，并且在标准任务上把执行轴 F1 最多提高 16.7%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14859v2](https://arxiv.org/abs/2605.14859v2)
