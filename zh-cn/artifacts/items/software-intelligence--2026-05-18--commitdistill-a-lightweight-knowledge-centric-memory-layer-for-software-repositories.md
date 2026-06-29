---
source: arxiv
url: https://arxiv.org/abs/2605.18284v1
published_at: '2026-05-18T12:14:28'
authors:
- Divya Chukkapalli
- Thejesh Avula
- Aditya Aggarwal
- Harsimran Singh
- Amith Tallanki
topics:
- code-intelligence
- repository-memory
- software-agents
- retrieval-augmented-generation
- developer-tools
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# CommitDistill: A Lightweight Knowledge-Centric Memory Layer for Software Repositories

## Summary
## 摘要
CommitDistill 将 git 提交历史转成一个本地、分类型的开发者和代码代理记忆存储。它最强的结果是在短上下文事实检索上优于 BM25 和 `git log --grep`，而下游 LLM 缺陷修复定位相较于不检索没有测出提升。

## 问题
- 软件项目把有用的工程知识放在提交信息、拉取请求和 issue 里，但开发者和代码助手在后续工作中经常用不上这些历史信息。
- 原始仓库检索可能把大量上下文浪费在冗长 diff 或噪声文本上，外部 embedding 服务也不适合受监管或私有代码库。
- 这篇论文针对一个很窄的用例：在决策时，从本地 git 历史里找出过去的约束、修复和失败模式。

## 方法
- CommitDistill 从提交信息里提取三类单元：Facts 表示约束，Skills 表示修复或操作，Patterns 表示重复出现的失败。
- 提取使用确定性的正则启发式、文本清理、长度过滤、按内容哈希去重，以及提交来源元数据。
- 检索在提取出的单元上使用长度归一化的 TF-IDF，并对 Patterns 和 Skills 加类型权重，再乘以前验权重。
- 最小分数阈值设为 θ=2.5，经过校准后，当查询过弱或超出范围时，工具会返回空结果。
- 这个原型完全在本地用纯 Python 运行，没有第三方依赖，并把单元以普通 JSON 存在 `.knowledge/units.json` 里。

## 结果
- 在五个公共仓库 `psf/requests`、`pallets/flask`、`expressjs/express`、`redis/redis` 和 `junit-team/junit5` 上，案例研究覆盖了 25,000 次提交，提取出 1,167 个分类型单元。
- 对 40 个 Python 单元的人类标注显示，有用精度为 0.525，Cohen’s κ = 0.633。
- 在 12 题事实型基准上、每题 256 字符预算内，CommitDistill 的命中率为 0.750，BM25 为 0.333，`git log --grep` 为 0.083。
- 当前检索器在更广泛的查询对比中报告了 36 题中命中 31 题，全部 36 个评估查询的端到端返回时间都低于 50 ms。
- 在报告的笔记本环境里，25,000 次提交的热缓存提取耗时 3.47 秒；对 10,000 次提交的提取在 4 秒内完成。
- 在一项配对的 LLM-as-judge 评估中，包含 n=200 个时间旅行式缺陷修复任务和两位评审者，任何检索条件相对于不检索控制组都没有测出统计上可检测的平均提升，CD-Hybrid 与 BM25 的正面对比也没有差异。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18284v1](https://arxiv.org/abs/2605.18284v1)
