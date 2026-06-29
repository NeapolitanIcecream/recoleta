---
source: arxiv
url: https://arxiv.org/abs/2606.19980v1
published_at: '2026-06-18T09:21:27'
authors:
- Wenli Xiao
- Jia Xie
- Tonghe Zhang
- Haotian Lin
- Letian "Max" Fu
- Haoru Xue
- Jalen Lu
- Yi Yang
- Cunxi Dai
- Zi Wang
- Jimmy Wu
- Guanzhi Wang
- S. Shankar Sastry
- Ken Goldberg
- Linxi "Jim" Fan
- Yuke Zhu
- Guanya Shi
topics:
- real-world-robot-learning
- robot-policy-self-improvement
- dexterous-manipulation
- coding-agents
- robot-data-scaling
- vision-language-action
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# ENPIRE: Agentic Robot Policy Self-Improvement in the Real World

## Summary
## 摘要
ENPIRE 让编码智能体在真实硬件上改进机器人操作策略。系统运行复位、rollout、验证和代码编辑循环；完成设置后，所需人工工作很少。论文报告称，在灵巧操作任务上，真实世界成功率最高达到 99%；当 8 个机器人-智能体工作单元并行运行时，改进速度更快。

## 问题
- 真实机器人策略学习仍需要人工复位场景、判断结果、收集 rollout，并修改训练代码，这会拖慢灵巧操作的数据扩展。
- 编码智能体可以在数字环境中改进软件，但真实机器人需要安全执行边界、自动复位和可靠的成功检查，智能体才能运行实验。
- 这个问题很重要，因为在接触密集型任务上训练通用策略时，机器人时间和人工操作员时间会成为瓶颈。

## 方法
- ENPIRE 为编码智能体提供任务 API，用于硬安全限制、自动验证、自动复位、rollout 执行和训练代码编辑。
- 在第一阶段，智能体根据简短的人工反馈和演示构建复位代码以及奖励/检查器代码；获批后，这些 API 会在后续运行中固定下来。
- 在第二阶段，智能体读取日志和视频，编辑 BC/RL/启发式/代码策略训练代码，启动真实机器人 rollout，并保留能提高实测成功率的改动。
- 对于机器人集群，ENPIRE 为每台机器人分配一个智能体；智能体异步测试不同代码分支，并通过 Git 共享或复制成功方案。
- 论文加入了平均机器人利用率、GPU 利用率、平均 Token 利用率、达到成功所需 Token 数和达到成功所需时间，用来衡量智能体消耗了多少机器人时间和模型 Token 预算。

## 结果
- 摘要称，编码智能体在包括 PushT、插针入盒和扎带切割在内的真实灵巧任务上达到 99% 成功率。
- 插针任务使用 4 mm 孔，并要求评估中连续 50 次真实世界成功；论文报告称，相比所引用的人在环方法，该方法更快收敛到 100%。
- 在 Gym-PushT 仿真中，Claude Code 和 Codex 在约 2 小时内达到 95% 成功率；Kimi Code 用时约为两倍。
- 集群扩展将 Push-T 达到 1.0 归一化分数的时间从 1 个智能体时的约 5 小时降至 8 个智能体时的约 2 小时。
- 集群扩展将插针任务达到接近完美成功率的时间从 1 个智能体时的超过 1.5 小时降至 8 个智能体时的约 40 分钟。
- 扎带检查器被优化到低于 150 ms 延迟；RoboCasa365 结果报告称优于 GR00T VLA 和 CaP-X，但摘录没有给出该比较的具体成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.19980v1](https://arxiv.org/abs/2606.19980v1)
