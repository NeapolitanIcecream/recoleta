---
source: arxiv
url: http://arxiv.org/abs/2604.23781v1
published_at: '2026-04-26T16:05:02'
authors:
- Fanqing Meng
- Lingxiao Du
- Zijian Wu
- Guanzheng Chen
- Xiangyan Liu
- Jiaqi Liao
- Chonghe Jiang
- Zhenglin Wan
- Jiawei Gu
- Pengfei Zhou
- Rui Huang
- Ziqi Zhao
- Shengyuan Ding
- Ailing Yu
- Bo Peng
- Bowei Xia
- Hao Sun
- Haotian Liang
- Ji Xie
- Jiajun Chen
- Jiajun Song
- Liu Yang
- Ming Xu
- Qionglin Qiu
- Runhao Fu
- Shengfang Zhai
- Shijian Wang
- Tengfei Ma
- Tianyi Wu
- Weiyang Jin
- Yan Wang
- Yang Dai
- Yao Lai
- Youwei Shu
- Yue Liu
- Yunzhuo Hao
- Yuwei Niu
- Jinkai Huang
- Jiayuan Zhuo
- Zhennan Shen
- Linyu Wu
- Cihang Xie
- Yuyin Zhou
- Jiaheng Zhang
- Zeyu Zheng
- Mengkang Hu
- Michael Qizhe Shieh
topics:
- agent-benchmarks
- multimodal-agents
- multi-turn-evaluation
- dynamic-environments
- coworker-agents
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# ClawMark: A Living-World Benchmark for Multi-Turn, Multi-Day, Multimodal Coworker Agents

## Summary
## 摘要
ClawMark 是一个面向 AI 协作代理的基准，测试代理在多天、多轮、多种数据类型的工作中，如何应对代理控制范围之外不断变化的环境。它衡量了早期代理基准大多没有覆盖的一点：当文件、邮件、日历和其他工具在多个工作日之间持续变化时，代理是否还能持续发挥作用。

## 问题
- 现有代理基准通常只测试一次静态会话，但真实的协作代理面对的是跨越多天持续推进的工作。
- 在真实办公环境中，轮次之间外部世界会发生变化：新邮件到达，日历安排变动，记录被编辑，证据也可能出现在 PDF、图像、音频、视频或电子表格中。
- 这很重要，因为一个代理在静止场景里看起来表现很强，但当它必须刷新状态、长期跟踪进度，并根据原始多模态证据采取行动时，可能会失败。

## 方法
- 论文提出了 **ClawMark**，这是一个包含 **13 种专业场景中的 100 个任务** 的基准。每个任务跨越 **2 到 6 轮**（平均 **3.6**），其中每一轮对应设定中的一个工作日。
- 任务在一个动态沙箱中运行，包含 **五个有状态服务**：文件系统、电子邮件、日历、知识库和电子表格。环境会在轮次之间变化，变化形式包括已告知的“loud events”和未告知的“silent mutations”。
- 证据是多模态的，且未转写。该版本包含 **1,072 个原始材料**，如 PDF、图像、音频、视频和电子表格。
- 评分完全基于规则。该基准使用 **1,537 个确定性的 Python 检查器**，其中包括 **55 条红线约束**，并且**不**使用 LLM-as-judge 评分。
- 作者在统一测试框架下评估了 **七个前沿代理系统**，用于比较当前模型处理长期、有状态协作工作流的能力。

## 结果
- ClawMark 认为自己相对以往工作处在一个独特的基准设定中：在列出的基准里，它是唯一一个同时具备 **multi-day tasks = yes**、**dynamic environment = yes**、**full multimodal input = yes** 和 **rule-based verification** 的基准。
- 在这套 100 任务基准上，最高的 **weighted score** 是 **Claude Sonnet 4.6** 的 **75.8**。接下来是 **Claude Opus 4.6 的 74.6** 和 **GPT-5.4 的 72.0**。
- 在更严格的 **Task Success** 指标上，最佳模型是 **Claude Opus 4.6，20.0%**，其次是 **Claude Sonnet 4.6，14.0%**，以及 **GPT-5.4，9.0%**。这说明部分进展很常见，但完整的端到端任务完成仍然少见。
- 不同模型的红线失败率不同：**Claude Sonnet 4.6 为 3.6%**，**Claude Opus 4.6 为 5.5%**，**GPT-5.4 为 3.6%**，**Qwen 3.6 Plus 为 14.5%**，**Kimi K2.5 为 9.1%**。
- 对 **73 个三轮任务** 的逐轮分析显示，在第一次外部环境更新后的第 2 天，**7 个模型中有 6 个**表现下降。报告中 **Claude Sonnet 4.6** 与 **GPT-5.4** 的分差从 **第 1 天的 +6.5 分** 缩小到 **第 3 天的 +4.0 分**。
- 主要的实证结论是，当前前沿代理在动态办公工作流中通常能取得部分进展，但一旦外部世界发生变化，它们仍然难以完整完成跨多天的任务。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23781v1](http://arxiv.org/abs/2604.23781v1)
