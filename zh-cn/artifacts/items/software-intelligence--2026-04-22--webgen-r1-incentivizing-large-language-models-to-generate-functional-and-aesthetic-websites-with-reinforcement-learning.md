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
WebGen-R1 用强化学习训练一个 7B 开源模型，使其能够生成既能运行、又有良好视觉效果的多页网站。论文称，这在项目级网页生成任务上，大幅缩小了小型开源模型与更大前沿模型之间的差距。

## 问题
- LLM 在函数级代码生成上表现较好，但多页网站生成还涉及路由、多文件依赖、运行时行为和视觉设计。
- 现有网站生成器通常停留在单页静态网站，或者依赖多智能体流水线，导致 token 成本、延迟和集成失败率上升。
- 这个任务上的强化学习很难做，因为奖励不容易验证：一个网站可能看起来不错，但运行时会失败，而完整的 GUI 智能体测试又过于昂贵，不适合用于训练。

## 方法
- WebGen-R1 将模型限制在一个固定、预先验证过的 React 脚手架内，因此模型只需要编写项目中的可变部分，而不是从零生成整个应用。
- 在进入高成本奖励评分前，它先做两阶段检查：先做静态合规检查，再执行依赖安装、构建、本地启动和浏览器渲染。
- 奖励采用级联式多模态设计：结构无效记 0 分，构建失败记 0 分，渲染成功后再根据视觉质量、无运行时错误的执行情况，以及是否满足要求的规划格式信号给出综合得分。
- 视觉质量来自 VLM 对渲染截图和用户提示的评分；功能完整性是一个二元分数，依据运行时和控制台错误判断。
- 策略使用 GRPO 优化，以处理同一提示下不同候选网站之间较高的奖励方差。

## 结果
- 训练使用包含 6,667 个任务的 WebGen-Instruct；主要评测使用包含 101 个任务的 WebGen-Bench；分布外评测使用从 WebDev-Arena 过滤得到的 119 个任务。
- 在论文对 7B 基础模型的主要前后对比中，有效渲染比例从 **30.56%** 提升到 **95.89%**。
- 论文报告审美评分提升了 **44.32%**。
- 在文中报告的指标上，功能质量从 **1.59%** 提升到 **29.21%**。
- 作者称，WebGen-R1 优于参数规模最高达 **72B** 的开源模型，并且在功能成功率上可与 **DeepSeek-R1 671B** 竞争，同时在有效渲染和审美对齐评分上更高。
- 这段摘录没有给出 Table 1 中各个基线模型的完整数值，因此这里无法提供精确的逐模型对比数据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20398v1](http://arxiv.org/abs/2604.20398v1)
