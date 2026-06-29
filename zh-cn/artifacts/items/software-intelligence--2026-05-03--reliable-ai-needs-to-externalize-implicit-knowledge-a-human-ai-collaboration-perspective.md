---
source: arxiv
url: https://arxiv.org/abs/2605.02010v1
published_at: '2026-05-03T18:31:45'
authors:
- Hengyu Liu
- Tianyi Li
- Zhihong Cui
- Yushuai Li
- Zhangkai Wu
- Torben Bach Pedersen
- Kristian Torp
- Christian S. Jensen
topics:
- ai-reliability
- human-ai-collaboration
- knowledge-objects
- implicit-knowledge
- agent-memory
- software-engineering
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# Reliable AI Needs to Externalize Implicit Knowledge: A Human-AI Collaboration Perspective

## Summary
## 总结
本文认为，AI 的可靠性需要有人类可验证的隐性知识记录，例如推理模式、操作流程和领域判断。文中提出 Knowledge Objects 作为结构化产物，把这些知识显式化，便于验证、修正、复用和追踪来源。

## 问题
- 现有可靠性方法主要检查显性知识，比如检索到的文档、引用、置信分数或存储的记忆，但许多有用的 AI 行为来自训练中学到的隐性模式。
- 这一点在高风险知识工作中很重要，因为幻觉、过度自信和对提示词敏感，都会让能力很强的系统变得不安全，或者让人难以信任其结果。
- 文中引用了具体失效率：专门的法律 AI 工具在 17–34% 的查询中会出现幻觉；通用 LLM 在 58–88% 的可验证法律问题上会出错；GPT-4 在系统综述任务中会对 28.6% 的医学参考文献产生幻觉。

## 方法
- 核心机制是 Knowledge Object：一种结构化记录，包含主张或流程、支撑证据或推理、适用范围和限制，以及验证元数据。
- AI 会生成候选 Knowledge Object，把原本会留在模型行为或交互轨迹中的模式外显出来。
- 人类专家审查这些对象，验证、拒绝、修正，或补充适用范围限制。
- 系统会保存来源、验证状态和修正记录，这样后续用户可以看到谁检查过某条主张、何时检查、以及它适用于哪里。
- 在软件工程中，一个 Knowledge Object 可能会说明：在 Java/Spring 连接池场景里，单例数据库连接在每秒超过 100 个请求时会带来线程安全问题，并以 12 份事故复盘和压力测试作为依据。

## 结果
- 这是一篇立场论文，没有报告 Knowledge Objects 的新基准、用户研究、实现结果或消融结果。
- 文中认为主要收益在经济性上：AI 先生成结构化知识，专家再验证有边界的产物，而不是每次都从头核查每个 AI 答案。
- 文中指出，组织知识中只有 5–20% 有文档记录，剩下的 80–95% 是隐性知识，而现有的 RAG、微调、自我验证和代理记忆方法都不能把这些知识直接变成可检查的内容。
- 文中用已有研究来说明可靠性缺口：名义上 99% 的 LLM 置信区间，平均只有 65% 的时间覆盖真实答案；纠正尝试后，阿谀奉承倾向仍有 78.5%；提示词格式变化会让准确率最多波动 76 个百分点。
- 文中认为，经过验证的 Knowledge Objects 可以把专家验证、修正、适用范围限制和来源记录保留下来，让后续 AI 辅助工作中的可靠性在不同用户之间累积。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02010v1](https://arxiv.org/abs/2605.02010v1)
