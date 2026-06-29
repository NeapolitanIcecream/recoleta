---
source: arxiv
url: https://arxiv.org/abs/2606.04397v1
published_at: '2026-06-03T03:26:56'
authors:
- Ameya Gawde
- Vyzantinos Repantis
- Harshvardhan Singh
- Lucy Moys
topics:
- code-intelligence
- llm-agents
- developer-documentation
- retrieval-augmented-generation
- repository-analysis
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Context-as-a-Service: Surfacing Cross-File Dependency Chains for LLM-Generated Developer Documentation

## Summary
## 概要
CaaS 是一个可通过工具调用的检索层，帮助 LLM 编码代理用仓库中的证据检查开发者文档。在两个生产 SDK 案例中，它发现了基线代理配合常规仓库工具漏掉的 8 个文档或教程问题。

## 问题
- LLM 生成的开发者文档读起来可能没问题，但它写的行为说法却可能错，因为相关证据散在其他文件、测试、示例或平台文档里。
- 文件读取、关键词搜索和符号导航等标准工具，常常找不到语义依赖链，比如延迟清理行为，或在别处创建的必需组件。
- 这很重要，因为错误的 API 注释和教程会让开发者错误使用 SDK，或者写出在编译时或运行时失败的示例。

## 方法
- CaaS 会为目标代码库索引源代码、API 参考、测试、示例和上游文档。
- 它把 BM25 关键词检索和 DRAMA 稠密检索结合起来，再用倒数排名融合合并排序结果。
- LLM 代理在文档审查或生成过程中调用 CaaS，拿到带文件元数据的排序片段，然后打开验证某个说法所需的源文件。
- 检索到的片段被当作候选证据。只有当证据支持一个具体的文档修正或教程修复时，才保留该发现。

## 结果
- 评估使用 Claude Sonnet 4.6，在一个约 200 个源文件的生产 SDK 上运行了 2 个文档工作流；每种效率条件运行 5 次。
- API 参考审查：基线找到了 5 个缺失的公共成员文档；CaaS 找到相同的 5 个问题，并额外发现 4 个问题，分别是 2 个跨文件事实错误和 2 条 API 注释说明不充分。
- 教程验证：基线验证了 17 条 API 说法；CaaS 额外发现 4 个问题，分别是 1 个可执行的 URI bug、1 个 API 用法改进和 2 个缺失的前置条件。
- 在两项研究中，保留的问题数从基线的 5 个增加到 CaaS 的 13 个，所以 CaaS 额外找出了 8 个常规仓库工具漏掉的问题。
- 两项任务的效率都提高了：API 审查的墙钟时间从 4.1 ± 0.7 分钟降到 3.2 ± 0.4 分钟，输入 token 从 17.4K ± 1.8K 降到 14.6K ± 1.3K。
- 教程验证的墙钟时间从 17.2 ± 2.1 分钟降到 11.4 ± 1.3 分钟，输入 token 从 112.3K ± 8.6K 降到 76.8K ± 6.2K；代价是 LLM 调用次数更多，从 17.4 ± 1.9 增加到 30.2 ± 2.4。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04397v1](https://arxiv.org/abs/2606.04397v1)
