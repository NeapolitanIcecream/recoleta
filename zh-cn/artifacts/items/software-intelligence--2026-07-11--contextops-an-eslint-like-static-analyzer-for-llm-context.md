---
source: hn
url: https://github.com/Abhijeet777ui/contextops
published_at: '2026-07-11T22:36:06'
authors:
- Abhijeet_Buag
topics:
- llm-context-analysis
- static-analysis
- prompt-engineering
- rag-systems
- ai-quality-gates
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# ContextOps, an ESLint-like static analyzer for LLM context

## Summary
## 摘要
ContextOps 是一个确定性的、与模型无关的静态分析器，用于在推理前检查 LLM 上下文的结构质量。它无需调用模型或访问网络，即可生成 0–100 的上下文健康分数、诊断信息、令牌估算结果，以及兼容 CI 的质量门禁。

## 问题
- LLM 应用经常向模型发送重复的检索片段、过大的系统提示词、过长的对话历史和过多的工具输出。
- 这些结构问题会增加令牌成本和延迟，降低行为可预测性，并可能在长期运行的智能体工作流中耗尽上下文窗口。
- 现有的提示词评估和模型评估无法直接衡量推理前的上下文结构。

## 方法
- ContextOps 接受结构化上下文字典、OpenAI 消息列表或普通字符串，并使用 n-gram 重叠、Jaccard 相似度和精确匹配等词法方法进行分析。
- 它评估四个维度：冗余度、密度、结构和来源集中度。分数计算方式为 `max(0, min(100, round(100 - total_penalty)))`。
- 它报告重复令牌、近重复片段、令牌分布、预计节省量、结构问题和建议修复措施。它不评估语义相关性、事实正确性、幻觉、推理能力或输出质量。
- `rag` 等配置会调整警告阈值，但全局 0–100 分数保持不变。CLI 检查、快照差异、稳定性报告、Python API、LangChain 回调和 GitHub Actions 可用于质量门禁和回归跟踪。

## 结果
- 给定示例获得了 81/100 的上下文健康分数，其中检测到 214 个重复令牌，检索内容占上下文的 78%，有两个近重复的检索片段，预计可节省 12% 的令牌。
- ContextOps 声称，对于最多 5,000 个令牌的负载，运行时间低于 2 秒；对于 50,000 个令牌的负载，运行时间低于 10 秒。
- 该引擎具有确定性，只需要 `tiktoken` 和 `click` 等 Python 依赖；它不使用 GPU、嵌入、推理 API、网络连接或外部服务。
- ContextBench 包含五个类别的 1,500 个样本，并要求优化器提交结果达到 CHS ≥78 的质量下限，但摘录没有提供实测准确率、误报率、优化器排行榜结果或与其他分析器的比较。
- ContextSecBench 增加了 9,500 个对抗性负载，覆盖提示注入隐藏、截断欺骗、语义拒绝服务、上下文污染和格式破坏，但摘录没有提供该数据集上的性能结果。

## Problem

## Approach

## Results

## Link
- [https://github.com/Abhijeet777ui/contextops](https://github.com/Abhijeet777ui/contextops)
