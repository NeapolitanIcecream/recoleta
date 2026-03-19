---
source: hn
url: https://www.anthropic.com/constitution
published_at: '2026-03-08T22:50:29'
authors:
- doener
topics:
- ai-alignment
- constitutional-ai
- safety-governance
- model-behavior
- human-oversight
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Claude's Constitution

## Summary
这不是一篇传统实验型论文，而是一份公开的**AI行为宪法**：Anthropic用它来定义Claude应具备的价值观、优先级和行为边界，并声明该文档会直接影响模型训练与部署。其核心贡献在于把“安全、伦理、公司规范、帮助性”的排序与解释公开化，作为可复用的对齐规范。

## Problem
- 解决的问题是：**如何让通用大模型在开放场景中既有帮助性，又不危险、不欺骗、且可被人类监督**。
- 这很重要，因为前沿AI可能成为“改变世界的力量”；如果模型价值观不稳、规则不清或会规避监督，就可能造成难以挽回的风险。
- 传统只靠硬规则的做法往往覆盖不全、遇到新情境容易失效；但完全依赖模型自由判断又会降低可预测性和可审计性。

## Approach
- 提出一套面向Claude训练与行为约束的**Constitution（宪法）**，将模型目标按优先级定义为：**broadly safe > broadly ethical > compliant with Anthropic’s guidelines > genuinely helpful**。
- 核心机制是：**少量硬约束 + 强调价值观与判断力的整体式决策**，而不是把所有行为都写成僵硬规则。简单说，就是先教模型“成为什么样的代理”，再让它在具体场景里权衡决策。
- 文档细化了多个行为维度：帮助性、公司专项指南、伦理、安全、以及对模型自身“性质/身份”的理解；并强调在冲突时优先维护人类监督与纠偏能力。
- 在帮助性上，作者引入类似**principal hierarchy**的思路，要求模型综合考虑operator、user及第三方利益，关注即时需求、最终目标、隐含偏好、自主性与长期福祉。
- 该宪法被明确声明为**训练过程中的关键依据**与最终权威文件，并以**CC0**公开发布，鼓励外部复用。

## Results
- 提供的摘录**没有报告任何定量实验结果**，没有给出数据集、基线、胜率、准确率或安全指标提升数值。
- 最强的具体主张是：这份宪法**直接塑造Claude的行为**，并在训练中发挥“crucial role（关键作用）”。
- 文中明确给出了4级优先级排序：**安全 > 伦理 > Anthropic指南 > 帮助性**，这是其最具体的操作化成果之一。
- 作者声称该方法比纯规则体系更适合泛化到新情境，因为它更依赖**价值观与判断力**而非静态清单，但摘录中**未提供实证比较数字**。
- 还声称Anthropic会在system cards中公开模型行为与宪法理想之间的偏差，强调**透明披露意图与偏差**，但同样未给出量化证据。

## Link
- [https://www.anthropic.com/constitution](https://www.anthropic.com/constitution)
