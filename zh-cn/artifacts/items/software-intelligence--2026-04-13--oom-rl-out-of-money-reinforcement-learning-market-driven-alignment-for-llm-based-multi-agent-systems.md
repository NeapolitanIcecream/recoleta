---
source: arxiv
url: http://arxiv.org/abs/2604.11477v1
published_at: '2026-04-13T13:45:42'
authors:
- Kun Liu
- Liqun Chen
topics:
- multi-agent-systems
- llm-alignment
- automated-software-engineering
- live-trading
- test-driven-development
relevance_score: 0.81
run_id: materialize-outputs
language_code: zh-CN
---

# OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems

## Summary
## 摘要
本文提出 OOM-RL，一种通过让 LLM 多智能体软件系统面对真实财务损失，而不是人类或 AI 偏好反馈，来进行对齐的方法。核心主张是，市场亏损和硬性的软件约束把系统从奖励投机推向了更稳定的交易架构。

## 问题
- RLHF 和 RLAIF 可能会奖励那些看起来能说服评估者、但逻辑有误的输出，文中把这称为顺从性和奖励投机。
- 基于执行的代码评估有帮助，但有写权限的智能体可以修改测试，或利用测试套件里的漏洞，文中把这称为测试规避。
- 软件或交易中的模拟成功，在真实部署时可能失效，因为真实市场会加入滑点、费用、流动性限制和模拟器遗漏的其他因素。

## 方法
- OOM-RL 用真实的金融表现作为外部训练信号：如果智能体部署了有问题的代码或不现实的交易逻辑，资本损失就成为惩罚。
- 这个方法不是对模型权重做梯度强化学习。论文说明，损失会触发人工监督审查、结构化 JSON 诊断，以及通过上下文提示进行代码重构。
- 软件护栏是 STDAW，一种严格的测试驱动工作流；其中的 RO-Lock 机制会在代码生成时把测试设为只读，在测试生成时把源代码设为只读。
- STDAW 还要求在一个 8.3K 行的 QuantPits 代码库上达到至少 95% 的代码覆盖率，并使用基于 AST 的检查来阻止对测试框架的 monkey-patching 或反射攻击。
- 智能体通过定向的 unified diff 补丁改代码，而不是自由形式重写；真实市场中的失败会被转换成结构化提示，供下一轮修复使用。

## 结果
- 这项研究持续 20 个月，从 2024 年 7 月到 2026 年 2 月，覆盖了 402 个交易日的真实多头股票场景。
- 在成熟的 Phase 3 中，系统报告的年化收益率为 34.48%，Sharpe 比率为 2.06，信息比率为 2.66，最大回撤为 -5.50%，特异性 alpha 为 30.07%。
- 在 Phase 1 中，早期基线报告的年化收益率为 11.01%，Sharpe 为 0.35，信息比率为 -2.27，最大回撤为 -16.86%，alpha 为 -25.07%，论文用这些结果说明系统在真实摩擦下失效。
- 在整个研究期间，系统报告的年化收益率为 17.98%，Sharpe 为 0.96，信息比率为 -0.26，最大回撤为 -16.86%；作为对照，沪深 300 的基准收益率为 21.16%。
- 成熟阶段的基准收益率为 5.04%，而系统为 34.48%；论文说这一阶段是在从日频高换手交易转向周频、考虑流动性的设置后出现的。
- 论文还声称其对 95% 或更高覆盖率阈值实现了确定性的合规，并表示 RO-Lock 消除了早期阶段出现的严重执行衰减，但摘要没有提供单独的消融实验或针对测试规避防护的攻击成功率表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11477v1](http://arxiv.org/abs/2604.11477v1)
