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
## 摘要
论文认为，AI 可靠性需要让人类可验证的隐性知识记录，例如推理模式、流程和领域判断。论文提出知识对象（Knowledge Objects），将这类知识整理成结构化工件，用于验证、纠正、复用和来源追踪。

## 问题
- 现有可靠性方法主要检查显性知识，例如检索到的文档、引用、置信度分数或已存储记忆，但许多有用的 AI 行为来自训练期间学到的隐性模式。
- 这会影响高风险知识工作，因为幻觉、过度自信和提示敏感性会让能力较强的系统变得不安全，或提高信任成本。
- 论文引用了具体失败率：专用法律 AI 工具在 17–34% 的查询中出现幻觉，通用 LLM 在 58–88% 的可验证法律问题上出错，GPT-4 在系统综述任务中生成的医学参考文献有 28.6% 属于幻觉。

## 方法
- 核心机制是知识对象：一种结构化记录，包含主张或流程、支持证据或推理、适用范围和限制，以及验证元数据。
- AI 通过外化模式生成候选知识对象；这些模式原本会隐藏在模型行为或交互轨迹中。
- 人类专家检查这些对象，验证、拒绝、纠正它们，或添加适用范围限制。
- 系统保存来源、验证状态和修正内容，使后续用户可以看到某项主张由谁检查、何时检查，以及适用于哪些场景。
- 在软件工程中，一个知识对象可能会说明：在 Java/Spring 连接池环境中，当请求量超过每秒 100 次时，单例数据库连接会导致线程安全问题；其依据包括 12 份事故复盘和负载测试。

## 结果
- 这是一篇立场论文，没有报告关于知识对象的新基准测试、用户研究、实现结果或消融结果。
- 论文主张，主要收益在经济层面：AI 起草结构化知识，使专家验证边界明确的工件，而无需从头重新检查每个 AI 答案。
- 论文认为，组织知识中只有 5–20% 被记录下来，剩余 80–95% 是隐性知识；当前的 RAG、微调、自验证和智能体记忆方法无法让这些知识被直接检查。
- 论文用既有研究说明可靠性缺口：名义上 99% 的 LLM 置信区间平均只有 65% 的时间覆盖真实答案；纠正尝试后，迎合性仍保持在 78.5%；提示格式变化最多可使准确率变化 76 个百分点。
- 论文主张，经过验证的知识对象可以保留专家验证、修正、适用范围限制和来源信息，让可靠性在后续 AI 辅助工作中跨用户积累。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02010v1](https://arxiv.org/abs/2605.02010v1)
