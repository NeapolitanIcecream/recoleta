---
source: arxiv
url: https://arxiv.org/abs/2604.26102v1
published_at: '2026-04-28T20:35:09'
authors:
- Yikai Zhang
- Jiaxin Pei
- Kenan Li
- Maoquan Wang
- Jin Pan
- Yu Kang
- Shengyu Fu
- Elsie Nallipogu
- Junjie Hu
- Yufan Huang
- Zijian Jin
topics:
- code-editing
- swe-bench
- coding-agents
- multi-agent-systems
- reinforcement-learning
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent

## Summary
## 摘要
SWE-Edit 是一种编码智能体设计，把文件查看和补丁编写拆分给不同的子智能体处理，让主模型保持更干净的上下文，并避免处理严格的编辑格式。在 SWE-bench Verified 上，它声称相比强单体基线，问题解决率更高，编辑成功率更高，推理成本更低。

## 问题
- 标准编码智能体在同一个上下文窗口中检查文件、规划修复并输出编辑，因此探索过程中查看的文件内容会留在上下文里，可能淹没真正相关的代码。
- 编辑格式会带来失败模式：find-and-replace 需要精确字符串匹配，而整文件重写会消耗更多 token，并可能改动无关代码。
- 这一点重要，因为 SWE 智能体的大量预算花在仓库搜索和补丁应用上；上下文噪声和编辑格式失败会降低已解决问题数量并增加成本。

## 方法
- SWE-Edit 增加一个 Viewer 子智能体，接收文件路径和自然语言查询，然后只返回与任务相关的代码块，而不是整个文件。
- 它增加一个 Editor 子智能体，接收文件路径和自然语言编辑指令，然后应用补丁，无需主智能体编写精确的 find-and-replace 命令。
- 主智能体仍负责推理 bug 和修复方案，而在主要实验中，GPT-5-mini 负责查看和编辑。
- 在编辑器训练中，作者使用 GRPO 微调 Qwen3-8B，使其根据编辑请求在 find-and-replace 和整文件重写之间选择。
- 奖励在删除注释并规范化空白后使用归一化匹配，作为生成编辑是否匹配目标的低成本代理指标。

## 结果
- 在包含 500 个问题、取 3 次运行平均值的 SWE-bench Verified 上，SWE-Edit 将解决率从 69.9% 提高到 72.0%，相比基线增加 2.1 个百分点。
- 总推理成本从 $243.7 降至 $200.1，减少 17.9%；编辑成功率从 93.4% 升至 96.9%，增加 3.5 个百分点。
- 单独使用 Viewer 时，平均返回所请求文件内容的 39.7%，代码表面积减少 60.3%；在组合设置中，主智能体的非缓存输入 token 从 276.7K 降至 181.3K。
- 在 50 个留出的 PR-Edit 示例上与检索基线相比，LLM Viewer 的召回率为 93.8%，F1 为 0.272；dense retrieval 的召回率为 86.8%，F1 为 0.140；BM25 的召回率为 53.7%，F1 为 0.083。
- 在 100 个 SWE-bench Verified 实例上使用其他主推理模型时，SWE-Edit 使 Kimi K2 Thinking 的解决率提高 2.7 个百分点，MiniMax-M2.1 提高 4.1 个百分点，GLM-4.7 提高 1.6 个百分点；编辑成功率提升范围为 12.8 到 18.3 个百分点。
- GRPO 将 Qwen3-8B 在 PR-Edit 上的格式成功率从 76.8% 提高到 90.4%，GPT Grader 准确率从 56.0% 提高到 68.4%，归一化匹配从 32.0% 提高到 38.8%；作为 SWE-bench Verified 上的编辑器时，它将解决率从 68.5% 提高到 69.9%，编辑成功率从 68.6% 提高到 81.1%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26102v1](https://arxiv.org/abs/2604.26102v1)
