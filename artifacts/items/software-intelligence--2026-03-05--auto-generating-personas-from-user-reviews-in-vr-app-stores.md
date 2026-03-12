---
source: arxiv
url: http://arxiv.org/abs/2603.04985v1
published_at: '2026-03-05T09:25:15'
authors:
- Yi Wang
- Kexin Cheng
- Xiao Liu
- Chetan Arora
- John Grundy
- Thuong Hoang
- Henry Been-Lirn Duh
topics:
- llm
- retrieval-augmented-generation
- persona-generation
- vr-accessibility
- human-ai-interaction
relevance_score: 0.68
run_id: materialize-outputs
---

# Auto-Generating Personas from User Reviews in VR App Stores

## Summary
本文提出一个面向VR课程的自动画像系统：从Meta/Steam VR商店评论中抽取与无障碍相关的真实反馈，并用LLM+RAG生成可讨论的用户画像。其目标不是单纯生成persona，而是帮助学生更高效地发现潜在无障碍需求并提升共情。

## Problem
- VR项目早期的无障碍需求常被忽视，而传统persona制作依赖访谈、问卷或大规模数据分析，对学生和新手来说成本高、门槛高。
- VR无障碍问题与传统Web/移动端不同，如晕动症、空间导航和控制器交互等，需要更贴近VR情境的需求发现方式。
- 现有课程中缺少基于真实用户证据、可系统支持无障碍讨论的自动persona方法。

## Approach
- 从Meta Quest和Steam的**50个最热门VR应用**收集评论，使用残障相关关键词、模糊匹配和人工清洗，得到**396条**高质量无障碍相关评论。
- 将评论按VR类型（如action、social、horror、puzzle、simulation、sports）和残障/问题类别组织，切分后嵌入到Chroma向量库中做语义检索。
- 用户输入项目类型与描述后，系统先检索最相关的评论片段，再将证据送入**GPT-4o**，生成中间的结构化“dimension-value”表示，最后汇总为标准化persona，包括简介、痛点、直接引语和明确需求。
- 为减少幻觉，方法采用**RAG**把生成过程绑定到检索到的真实评论证据，而不是纯生成；系统还支持对话式追问、同类需求推荐和跨应用/跨残障类型persona对比。

## Results
- 在**24名**VR课程学生的交叉条件研究中，系统在总体共情相关评分上高于基于问卷/自行搜集资料的方法：**t = 2.989, p = .015**；system **M = 4.45, SD = 0.78**，baseline **M = 3.06, SD = 1.39**。
- 在**Perspective Taking**上显著更高：**t = 3.715, p = .004**；system **M = 4.65, SD = 0.81**，baseline **M = 3.25, SD = 1.24**。
- 在**Empathic Concern**上显著更高：**t = 2.515, p = .033**；system **M = 4.35, SD = 1.29**，baseline **M = 2.85, SD = 1.54**。
- 在**Fantasy**上**无显著差异**；system **M = 4.15, SD = 2.90**，baseline **M = 3.10, SD = 1.96**。
- 定性结果的最强主张是：学生认为基于真实评论生成的persona降低了“虚构感/抽象感”，更容易从残障用户视角理解VR无障碍问题，并增强设计责任感。
- 作者声称这是**首个**将自动生成的无障碍persona整合进VR课程教学、并用其支持无障碍需求讨论与共情提升的工作之一/首次实践。

## Link
- [http://arxiv.org/abs/2603.04985v1](http://arxiv.org/abs/2603.04985v1)
