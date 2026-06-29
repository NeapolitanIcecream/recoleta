---
source: arxiv
url: https://arxiv.org/abs/2604.24697v1
published_at: '2026-04-27T16:58:04'
authors:
- Zhou Ziheng
- Huacong Tang
- Jinyuan Zhang
- Haowei Lin
- Bangcheng Yang
- Qian Long
- Fang Sun
- Yizhou Sun
- Yitao Liang
- Ying Nian Wu
- Demetri Terzopoulos
- Xiaofeng Gao
topics:
- ai-agents
- minecraft-benchmark
- scientific-discovery
- multi-agent-systems
- causal-reasoning
- redstone-circuits
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# Can Current Agents Close the Discovery-to-Application Gap? A Case Study in Minecraft

## Summary
## 摘要
SciCrafter 测试 LLM 智能体能否发现 Minecraft 红石中缺失的规则，并把这些规则用到可工作的电路里。当前最强模型在没有帮助时的成功率只有约 26%，论文发现它们在判断该研究什么，以及把已发现的规则用于构建上，都存在明显缺口。

## 问题
- 现有智能体基准很少测试完整的“发现到应用”循环：找到未知因果规则，记录下来，再用它构建可工作的系统。
- Minecraft 红石提供了可控的电路任务，智能体不能总靠记忆里的事实，尤其是在任务参数扩大时。
- 这对自动化工程智能体很重要，因为真实任务常常需要先提出正确的实验问题，构建才可能成功。

## 方法
- SciCrafter 定义了 5 类红石任务，每类 5 个难度等级，共 25 个任务：同时点亮、T 形分支布线、顺序激活、等距点亮和脉冲延长。
- 智能体要搭建能按指定空间或时间模式点亮灯的电路；自动检查器会按下按钮并验证每个 tick 的灯状态。
- 难度通过灯的数量、延迟序列和脉冲时长等参数提升，这迫使智能体学习信号衰减、中继器方向、中继器延迟以及意外的侧向连接等机制。
- 评测在 Claude Code 下运行 GPT-5.2、Gemini-3-Pro、Claude-Opus-4.5、Grok-4、GLM-4.7、Qwen3-235B、Qwen2.5-72B 和 Qwen3-32B，每个任务做 50 次验证试验，共 8 次运行。
- 诊断部分按顺序加入干预：告诉智能体该查什么的 oracle 提示、用于受控实验的 scientist 子智能体，以及带有 Claim、Evidence Proof、Constraints 和 Example 字段的结构化知识书。

## 结果
- 最好的基线是 Gemini-3-Pro，在 25 个任务上的成功率为 26.0%；GPT-5.2 为 25.5%，Claude-Opus-4.5 为 21.0%，Qwen3-32B 为 10.5%。
- 对强模型来说，oracle 提示大约能让成功率翻倍：Gemini-3-Pro 从 26.0% 升到 52.5%，GPT-5.2 从 25.5% 升到 51.0%，Claude-Opus-4.5 从 21.0% 升到 46.0%。
- 加入 scientist 子智能体后，各模型又提升了 7.5 到 14.0 个百分点；Gemini-3-Pro 达到 64.0%，GPT-5.2 达到 60.0%，Claude-Opus-4.5 达到 59.0%。
- 剩余的应用缺口仍然很大：Gemini-3-Pro 为 36.0 个百分点，GPT-5.2 为 40.0，Claude-Opus-4.5 为 41.0，Qwen2.5-72B 为 57.0。
- 论文报告的消融结果显示，结构化整理优于自由文本总结：Claim-Proof-Constraints-Example 格式达到 64.0%，自由文本总结为 58.0%。
- 论文认为，前沿模型的主要瓶颈正在转向知识缺口识别，而剩余的应用能力仍然是总体上最大的绝对缺口。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24697v1](https://arxiv.org/abs/2604.24697v1)
