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
## 总结
ClawMark 是一个面向 AI 同事代理的基准，覆盖多天、多轮次和多种数据类型，且环境会在代理无法控制的情况下变化。它衡量的是早期代理基准大多没有覆盖的差距：当文件、邮件、日历和其他工具在工作日之间持续变化时，代理还能否保持有用。

## 问题
- 现有代理基准通常只测试一个静态会话，但真实的同事代理要面对跨多天持续进行的工作。
- 在真实办公场景中，世界会在轮次之间变化：新邮件会到达，日程会调整，记录会被编辑，证据也可能出现在 PDF、图片、音频、视频或电子表格中。
- 这很重要，因为一个在冻结场景里表现很强的代理，在需要刷新状态、跟踪进度并基于原始多模态证据行动时，可能会失败。

## 方法
- 论文提出了 **ClawMark**，一个包含 **100 个任务、覆盖 13 个职业场景** 的基准。每个任务跨 **2 到 6 个轮次**（平均 **3.6**），每个轮次对应一个虚构工作日。
- 任务运行在一个动态沙箱中，包含 **五个有状态服务**：文件系统、邮件、日历、知识库和电子表格。环境会通过已宣布的“loud events”和未宣布的“silent mutations”在轮次之间变化。
- 证据是多模态且未经转写的。发布内容包含 **1,072 个原始素材**，例如 PDF、图片、音频、视频和电子表格。
- 评分完全基于规则。基准使用 **1,537 个确定性的 Python 检查器**，其中包括 **55 个红线约束**，且 **不** 使用 LLM-as-judge 评分。
- 作者在统一的执行框架下评估了 **7 个前沿代理系统**，用来比较当前模型如何处理长期、有状态的同事工作流。

## 结果
- 与以往工作相比，ClawMark 的基准设置有明显区别：在列出的基准中，它是唯一一个同时满足 **多天任务 = 是**、**动态环境 = 是**、**完整多模态输入 = 是** 和 **基于规则验证** 的基准。
- 在这个 100 任务基准上，最高的 **加权分数** 是 **Claude Sonnet 4.6** 的 **75.8**。随后是 **Claude Opus 4.6 的 74.6** 和 **GPT-5.4 的 72.0**。
- 在更严格的 **Task Success** 指标上，最佳模型是 **Claude Opus 4.6，20.0%**，其次是 **Claude Sonnet 4.6，14.0%** 和 **GPT-5.4，9.0%**。这说明部分进展很常见，但完整的端到端完成仍然少见。
- 红线失败率因模型而异：**Claude Sonnet 4.6** 为 **3.6%**，**Claude Opus 4.6** 为 **5.5%**，**GPT-5.4** 为 **3.6%**，**Qwen 3.6 Plus** 为 **14.5%**，**Kimi K2.5** 为 **9.1%**。
- 对 **73 个三轮次任务** 的轮次级分析显示，**7 个模型中有 6 个** 在第一轮外部环境更新后，于第 2 天出现下降。报告中的 **Claude Sonnet 4.6** 与 **GPT-5.4** 差距从 **第 1 天的 +6.5 分** 缩小到 **第 3 天的 +4.0 分**。
- 主要实证结论是，当前前沿代理常常能在动态办公工作流中取得部分进展，但当外部世界发生变化后，它们仍然很难完整完成多天任务。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23781v1](http://arxiv.org/abs/2604.23781v1)
