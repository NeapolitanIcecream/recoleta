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
SciCrafter 测试 LLM 智能体能否发现缺失的 Minecraft 红石规则，并用这些规则建造可工作的电路。当前前沿智能体在没有帮助时成功率只有约 26%，论文发现它们在识别需要研究的问题和应用已发现规则方面都有明显缺口。

## 问题
- 当前智能体基准很少测试完整的发现到应用循环：找到未知因果规则，记录规则，并用它构建可工作的系统。
- Minecraft 红石提供可控的电路任务；尤其在任务参数扩展时，智能体不能总是依赖记忆中的事实。
- 这对自动化工程智能体很重要，因为真实任务往往需要先提出正确的实验问题，之后构建才可能成功。

## 方法
- SciCrafter 定义了 5 个红石任务族，每个任务族有 5 个难度等级，共 25 个任务：同时点亮、T 形路由、顺序激活、等距点亮和脉冲延长。
- 智能体构建电路，使灯按指定的空间或时间模式点亮；自动检查器按下按钮，并逐 tick 验证灯的状态。
- 难度通过灯的数量、延迟序列和脉冲持续时间等参数提高，迫使智能体学习信号衰减、中继器方向、中继器延迟和意外侧向连接等机制。
- 评估在 Claude Code 下运行 GPT-5.2、Gemini-3-Pro、Claude-Opus-4.5、Grok-4、GLM-4.7、Qwen3-235B、Qwen2.5-72B 和 Qwen3-32B；每个任务进行 50 次验证试验和 8 次运行。
- 诊断按顺序加入干预：关于研究内容的 oracle 提示、用于受控实验的 scientist 子智能体，以及包含 Claim、Evidence Proof、Constraints 和 Example 字段的结构化知识书。

## 结果
- 最佳基线是 Gemini-3-Pro，在 25 个任务上的成功率为 26.0%；GPT-5.2 达到 25.5%，Claude-Opus-4.5 达到 21.0%，Qwen3-32B 达到 10.5%。
- oracle 提示让强模型的成功率约翻倍：Gemini-3-Pro 从 26.0% 升至 52.5%，GPT-5.2 从 25.5% 升至 51.0%，Claude-Opus-4.5 从 21.0% 升至 46.0%。
- 加入 scientist 子智能体后，各模型又提高 7.5 到 14.0 个百分点；Gemini-3-Pro 达到 64.0%，GPT-5.2 达到 60.0%，Claude-Opus-4.5 达到 59.0%。
- 剩余的应用缺口仍然很大：Gemini-3-Pro 为 36.0 个百分点，GPT-5.2 为 40.0，Claude-Opus-4.5 为 41.0，Qwen2.5-72B 为 57.0。
- 报告的消融实验中，结构化整合优于自由形式摘要：Claim-Proof-Constraints-Example 格式达到 64.0%，自由形式摘要为 58.0%。
- 论文称，前沿模型的主要瓶颈正在转向知识缺口识别，而剩余的应用能力仍是总体上最大的绝对缺口。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24697v1](https://arxiv.org/abs/2604.24697v1)
