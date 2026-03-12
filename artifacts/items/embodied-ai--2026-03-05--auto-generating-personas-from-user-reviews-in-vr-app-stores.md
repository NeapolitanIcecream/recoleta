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
- llm-persona-generation
- virtual-reality
- accessibility
- user-reviews
- rag
relevance_score: 0.02
run_id: materialize-outputs
---

# Auto-Generating Personas from User Reviews in VR App Stores

## Summary
本文提出一个面向VR课程的自动生成用户画像系统：从Meta与Steam VR商店评论中抽取与无障碍相关的真实反馈，用LLM+RAG生成画像以支持需求讨论。研究表明，这种基于真实评论的画像比传统调查式做法更能提升学生对残障用户的共情与责任感。

## Problem
- VR项目早期很少系统化地讨论无障碍需求，而传统用户画像制作费时、依赖调研能力，学生容易做出表面化或臆造画像。
- VR无障碍问题与网页/移动端不同，如晕动症、空间导航和控制器交互障碍，常在设计教育中被忽视。
- 需要一种能把**真实用户证据**快速转化为可讨论画像的方法，以帮助学生更准确地识别潜在无障碍需求。

## Approach
- 从**50个最热门VR应用**的Meta Quest与Steam商店抓取评论，利用残障相关关键词、模糊匹配和人工清洗，得到**396条高质量无障碍评论**。
- 将评论按VR应用类型（如action、social、horror、puzzle、simulation、sports）和残障/问题类型组织，切分为语义片段并向量化存入Chroma数据库。
- 生成时先按项目类型和残障组别检索最相关评论，再把证据送入**GPT-4o + RAG**流程，先形成中间的“维度-取值”结构，再生成标准化persona，包含简介、痛点、直接引语和明确需求。
- 系统支持对话式使用：学生可输入项目背景、请求相似persona或特定需求建议；为降低幻觉，输出始终受检索到的真实评论约束。

## Results
- 在**24名**VR课程学生的交叉条件用户研究中，系统总体共情得分高于调查式方法：**t = 2.989, p = .015**；system **M = 4.45, SD = 0.78**，survey **M = 3.06, SD = 1.39**。
- **Perspective Taking**显著提升：**t = 3.715, p = .004**；system **M = 4.65, SD = 0.81**，survey **M = 3.25, SD = 1.24**。
- **Empathic Concern**显著提升：**t = 2.515, p = .033**；system **M = 4.35, SD = 1.29**，survey **M = 2.85, SD = 1.54**。
- **Fantasy**未见显著差异；仅报告均值差：system **M = 4.15, SD = 2.90**，survey **M = 3.10, SD = 1.96**。
- 论文的 strongest claims 是：系统让学生更容易从残障用户视角理解VR无障碍问题，减少“虚构画像”的抽象感，并增强设计责任感。
- 论文未报告画像生成质量、检索准确率、幻觉率等系统级客观指标；主要证据来自教育场景中的问卷与访谈。

## Link
- [http://arxiv.org/abs/2603.04985v1](http://arxiv.org/abs/2603.04985v1)
