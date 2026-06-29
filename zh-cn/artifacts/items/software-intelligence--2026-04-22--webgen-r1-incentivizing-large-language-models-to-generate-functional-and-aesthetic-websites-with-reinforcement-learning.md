---
source: arxiv
url: http://arxiv.org/abs/2604.20398v1
published_at: '2026-04-22T10:04:46'
authors:
- Juyong Jiang
- Chenglin Cai
- Chansung Park
- Jiasi Shen
- Sunghun Kim
- Jianguo Li
- Yue Wang
topics:
- website-generation
- reinforcement-learning
- code-generation
- multimodal-reward
- small-language-model
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# WebGen-R1: Incentivizing Large Language Models to Generate Functional and Aesthetic Websites with Reinforcement Learning

## Summary
## 摘要
WebGen-R1 用强化学习训练一个 7B 开源模型，让它生成能运行、看起来也好的多页面网站。论文称，这缩小了小型开源模型和更大前沿模型在项目级网页生成上的差距。

## 问题
- LLM 在函数级代码生成上表现不错，但多页面网站生成还要处理路由、多文件依赖、运行时行为和视觉设计。
- 现有的网站生成器往往只做到单页静态站，或者使用多智能体流水线，带来更高的 token 成本、延迟和集成失败风险。
- 这类任务很难用 RL 做奖励验证：网站可能看起来不错，但运行时会失败；完整的 GUI 智能体测试又太贵，不适合训练。

## 方法
- WebGen-R1 把模型限制在一个固定、预先验证过的 React 脚手架里，所以模型只写项目中的可变部分，而不是从头写整个应用。
- 它在昂贵的奖励评分前做两阶段检查：先做静态合规检查，再进行依赖安装、构建、本地服务和浏览器渲染。
- 奖励是级联的多模态奖励：结构无效记 0，构建失败记 0，渲染成功后再由视觉质量、运行时无错误执行和必须的规划格式信号共同组成分数。
- 视觉质量来自 VLM 对渲染截图和用户提示的评分；功能完整性则基于运行时错误和控制台错误的二元评分。
- 策略用 GRPO 优化，以处理同一提示下多个候选网站之间较高的奖励方差。

## 结果
- 训练使用 WebGen-Instruct，共 6,667 个任务；主评测使用 WebGen-Bench，共 101 个任务；分布外评测使用从 WebDev-Arena 过滤出的 119 个任务。
- 在论文对 7B 基座模型的主要前后对比中，有效渲染率从 **30.56%** 提升到 **95.89%**。
- 论文报告审美评分提升了 **44.32%**。
- 按论文中的指标，功能质量从 **1.59%** 提升到 **29.21%**。
- 作者称，WebGen-R1 在功能成功率上超过了最多 **72B** 的开源模型，并且在有效渲染和审美对齐上与 **DeepSeek-R1 671B** 具有竞争力。
- 摘要片段没有给出 Table 1 中每个基线的完整数值，所以这里无法提供逐模型的精确对比数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20398v1](http://arxiv.org/abs/2604.20398v1)
