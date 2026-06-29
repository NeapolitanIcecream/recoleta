---
source: arxiv
url: https://arxiv.org/abs/2606.03461v1
published_at: '2026-06-02T10:37:47'
authors:
- Sidi Yang
- Chaofan Tao
- Jierun Chen
- Tiezheng Yu
- Ruoyu Wang
- Yuxin Jiang
- Yiming Du
- Wendong Xu
- Jing Xiong
- Taiqiang Wu
- Lifeng Shang
- Xiaohui Li
- Ngai Wong
- Haoli Bai
topics:
- terminal-agents
- code-intelligence
- agent-training
- software-foundation-models
- trajectory-distillation
- human-ai-interaction
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# What Makes Interaction Trajectories Effective for Training Terminal Agents?

## Summary
## 总结
论文发现，最好的 terminal agent 教师并不是单独基准分最高的模型。DeepSeek-V3.2 生成的学生比 Claude Opus 4.6 更强，因为它的轨迹包含更多 inspect-act-verify 行为，学生可以直接模仿。

## 问题
- terminal agent 依赖交互轨迹训练，但教师选择通常把教师的任务成功率当作主要信号。
- 这很重要，因为高分 agent 可能用很短、隐藏或缺少明确环境依据的动作完成任务，给学生的监督更少。
- 论文想知道，哪些轨迹属性能让 terminal-agent 微调数据更好地迁移到 Qwen3-8B 和 Qwen3-32B 学生模型。

## 方法
- 作者构建了 Terminal-Lego，这是一条管线，把 StackOverflow 问题转成经过 Docker 验证的 terminal-agent 任务，覆盖 90 多个技术领域。
- 他们使用同一个 Terminus-2 terminal harness，收集来自 DeepSeek-V3.2、Claude Opus 4.6、Qwen3.5-Plus 和 GLM-5 的轨迹。
- 他们在匹配的任务集合上比较教师，这些任务里所有教师都解出了同一批实例，然后对相同的 Qwen3 学生模型做微调。
- 核心机制是 Environment-Grounded Supervision：有用的轨迹会展示 agent 检查文件或状态、执行动作、检查输出并调整策略。
- 他们定义了 Targeted Observation Ratio (TOR)，指由同一路径或相关状态的早期相关观察支撑的动作命令占比。

## 结果
- 在 Terminal-Bench 2.0 上，Claude Opus 4.6 作为独立 agent 的得分是 69.4，DeepSeek-V3.2 是 39.3；在 8.1K 匹配成功轨迹上做 SFT 后，DeepSeek-V3.2 训练出的学生更强：Qwen3-8B 达到 10.5% Pass@1，Qwen3-32B 达到 20.6%，而 Claude 的结果分别是 5.6% 和 15.5%。
- 使用 15.3K 条 Terminal-Lego 轨迹时，Qwen3-32B 在 Terminal-Bench 2.0 上达到 24.3%，文中将其报告为相对基座模型提升 7 倍，并且接近此前用超过 30 倍数据训练得到的 SOTA。
- 更长的轨迹本身不能解释提升：在 1.1K 个困难实例上，DeepSeek-V3.2 最短的成功轨迹给 Qwen3-32B 带来的效果优于最长轨迹，分别是 13.9% 对 12.7%；尽管最长轨迹有更多轮次，12.2 对 8.9，也有更多错误轮次，3.8 对 2.7。
- 去掉显式错误信息轨迹后，DeepSeek-V3.2 仍然领先：在 1.7K 条无错误轨迹上，Qwen3-32B 使用 DeepSeek-V3.2 时达到 19.1%，而使用 Claude 时是 10.5%，使用 Qwen3.5-Plus 时是 11.2%，使用 GLM-5 时是 15.4%。
- 在 8.1K 条 DeepSeek-V3.2 轨迹中屏蔽观察-命令监督后，TOR 从 13.4% 降到 5.3%，Qwen3-32B 从 20.6% 降到 13.8%，Qwen3-8B 从 10.5% 降到 3.8%。
- 在数据规模固定时，优先选高 TOR 轨迹有帮助：在 1.1K 条成功的 DeepSeek-V3.2 轨迹上，Qwen3-32B 使用高 TOR 数据达到 14.6%，使用低 TOR 数据达到 11.8%，使用随机数据达到 13.8%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03461v1](https://arxiv.org/abs/2606.03461v1)
