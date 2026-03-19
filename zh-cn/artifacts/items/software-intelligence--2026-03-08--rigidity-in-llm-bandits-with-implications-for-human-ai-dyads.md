---
source: arxiv
url: http://arxiv.org/abs/2603.07717v1
published_at: '2026-03-08T16:42:25'
authors:
- Haomiaomiao Wang
- "Tom\xE1s E Ward"
- Lili Zhang
topics:
- llm-behavior
- decision-making
- bandit-learning
- human-ai-dyads
- cognitive-modeling
relevance_score: 0.43
run_id: materialize-outputs
language_code: zh-CN
---

# Rigidity in LLM Bandits with Implications for Human-AI Dyads

## Summary
本文研究把大语言模型当作二臂老虎机中的“决策者”时，是否会表现出稳定且可重复的决策偏差。结论是：LLM 往往把微小的初始或位置线索放大成僵化策略，而且这种现象在常见解码参数变化下依然稳健。

## Problem
- 论文要解决的问题是：**LLM 在交互式决策中是否存在稳健的行为偏差，而不仅仅是准确率层面的误差**。
- 这很重要，因为在人机协作中，模型的早期偏向、顺序效应和过度自信，可能持续影响人的判断，形成偏差放大。
- 现有基准通常测“答对没有”，但较少测**模型如何学习、何时探索、是否会僵化坚持一个选择**。

## Approach
- 作者把 DeepSeek、GPT-4.1、Gemini-2.5 当作实验参与者，在二臂老虎机任务中测试：对称奖励条件（0.25/0.25）和非对称奖励条件（0.75/0.25）。
- 每个条件做 **200 次独立模拟 × 100 轮试验**，并比较 4 种解码设置：Strict、Moderate、Default-like、Exploratory，改变 temperature 与 top-p。
- 为了强制二选一，输出限制为 **1 个 token**，只接受 `X` 或 `Y`；无效输出记为失败并计入分析。
- 行为上统计总奖励、目标臂选择率、loss-shift / win-shift、choice bias、stubbornness、amplification、rigidity 等指标。
- 机制上使用**分层 Rescorla-Wagner 学习模型 + softmax 策略**拟合，核心解释非常简单：模型**更新很慢（低学习率）但一旦偏向就选得非常死（高逆温）**，所以早期偶然信号会被迅速固化。

## Results
- 在对称条件（0.25/0.25）下，理论上应接近 50/50 和约 **25/100** 奖励；LLM 的总奖励确实接近机会水平，例如 DeepSeek **24.60±0.62**、Gemini-2.5 **24.71±0.56**、GPT-4.1 **25.38±0.61**，但选择分布明显偏斜，说明**不是更会学，而是更会固化偏好**。
- 对称条件下，Gemini-2.5 在严格解码时最偏向先出现的 X：**(X,Y)=(0.61±0.44, 0.39±0.44)**；GPT-4.1 也偏 X，如 **(0.55±0.40, 0.45±0.40)**；而严格条件下 Loss-Shift 几乎为 0：DeepSeek **0.03±0.00**、Gemini **0.03±0.00**、GPT-4.1 **0.09±0.01**。
- 对称条件下的“僵化”指标很高：Strict 设置下 Stubbornness Rate 达 DeepSeek **0.97±0.02**、Gemini **0.95±0.03**、GPT-4.1 **0.90±0.04**；Rigidity Index 接近封顶 **0.96–0.99±0.01**。作者据此声称：**在模糊环境中，LLM 会把微弱的位置线索放大成顽固的一臂策略**。
- 在非对称条件（0.75/0.25）下，模型通常会选中更优臂，但仍然过于僵化。总奖励低于理想 oracle 的 **75/100**，例如 DeepSeek **72.68±1.44**、GPT-4.1 **73.15±0.92**、Gemini 严格设置峰值 **74.22±1.00**。
- 非对称条件下目标臂选择率在严格设置几乎封顶：DeepSeek **0.95±0.03**、Gemini **0.98±0.02**、GPT-4.1 **0.96±0.01**；但 Adjusted Choice Bias Index 为 **-0.04 到 -0.09**，表示相对 oracle 仍然**复查不足、探索不足**。
- 计算模型给出的关键机制结果是：对称条件组学习率 **μ_A=0.09–0.22**，逆温几乎封顶 **μ_τ=4.9984–4.9991**；非对称条件学习率稍升到 **0.17–0.33**，但逆温仍极高 **4.991–4.998**。这被作者视为本文的核心突破：**用一个简单的认知模型把“噪声放大成偏差”和“僵化利用”统一解释为低学习率 + 极高确定性选择**。

## Link
- [http://arxiv.org/abs/2603.07717v1](http://arxiv.org/abs/2603.07717v1)
