---
source: arxiv
url: https://arxiv.org/abs/2605.21996v1
published_at: '2026-05-21T04:54:55'
authors:
- Murong Ma
- Tianyu Chen
- Yun Lin
- Shuai Lu
- Qinglin Zhu
- Yeyun Gong
- Zhiyong Huang
- Peng Cheng
- Yan Lu
- Jin Song Dong
topics:
- software-engineering-agents
- code-intelligence
- sft-data-curation
- process-supervision
- swe-bench
- reference-patches
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# From Patches to Trajectories: Privileged Process Supervision for Software-Engineering Agents

## Summary
## 摘要
P2T 使用开发者参考补丁来筛选更短、也更有用的软件工程代理训练轨迹。它通过判断每一步是否揭示了修复所需证据，并阻止参考补丁泄漏，来改进 SFT 数据。

## 问题
- 在完整教师轨迹上做 SFT，会让学生模仿每个中间步骤，包括没有依据的推理、重复查看文件、循环，以及碰巧通过测试的行为。
- 只按最终结果过滤的训练，只检查最终补丁是否通过测试，因此不会直接给出步骤质量或轨迹长度的信号。
- 论文引用的 SWE-Gym 池中，70.2% 的 Qwen3-Coder-480B 教师实例和 64.7% 的 GLM-5-FP8 教师实例没有提供监督，因为教师从未到达通过的补丁。

## 方法
- P2T 把开发者参考补丁当作特权筛选数据：筛选者可以查看它，但学生看不到。
- 逆向阶段把参考补丁转换成一个过程图，包含导出修复所需的事实和里程碑，例如文件位置、运行行为、根因、编辑计划、代码修改和验证。
- 前向阶段采样被遮蔽的教师续写，最多把一步修改到一个可用的图节点，并保留进展超过阈值的最短片段。
- 通过 groundedness 检查阻止泄漏，要求修改后的步骤只提到已观察到的仓库实体，并且其主张必须由可见轨迹前缀支持。
- 只有当提交的补丁通过任务测试套件时，最终轨迹才会保留。

## 结果
- 训练使用了约 1.8k 个经筛选的 SWE-Gym 实例，来源是 2,438 个真实 Python 问题的池；拒绝采样基线运行在 2,126 个可执行实例上。
- 逆向阶段构建了 33,106 个过程图节点，每个实例的中位数为 18 个节点。
- 在包含 500 个实例的 SWE-bench Verified 上，P2T 相比按结果过滤的 SFT，Pass@1 最高提升 10.8 个点。
- 论文报告，在相同计价基准下，平均每个实例的推理成本约降低 15 美元，同时提高了 Pass@1。
- 结果在 SWE-bench Verified 和包含 300 个实例的 SWE-bench Lite 上都出现了，覆盖两个教师模型：Qwen3-Coder-480B-A35B-Instruct 和 GLM-5-FP8。
- 基线包括 SWE-Gym 风格的通过测试拒绝采样和 SWE-Lego 工具错误掩蔽；论文说，一个按规模匹配的消融版本仍然优于这两者，这支持了关于数据质量而不是数据规模的判断。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21996v1](https://arxiv.org/abs/2605.21996v1)
