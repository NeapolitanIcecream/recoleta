---
source: hn
url: https://www.wisdom.ai/blog/how-wisdom-gets-text-to-sql-right
published_at: '2026-06-22T23:48:57'
authors:
- sharva
topics:
- text-to-sql
- context-learning
- data-agents
- enterprise-analytics
- llm-evaluation
relevance_score: 0.67
run_id: materialize-outputs
language_code: zh-CN
---

# What it takes to get high Text-to-SQL accuracy in production

## Summary
## 摘要
WisdomAI 称，生产环境中的高 Text-to-SQL 准确率取决于持续管理的业务上下文，模型选择只是其中一部分。它的 Adaptive Context Engine 从 schema、样本、日志、文档、反馈和管理员审核中构建上下文，并在定义和数据使用方式变化时更新上下文。

## 问题
- 企业级 Text-to-SQL 在部署后会受到业务术语、schema 名称、指标定义和团队规则变化的影响，进而失败。
- 固定上下文可能让同一个问题在不同时间返回不同数字，损害用户对分析流程的信任。
- BIRD-SQL 等公开基准可能漏掉这个问题，因为部分问题在提示词中已经包含所需上下文，部分参考 SQL 也有错误。

## 方法
- ACE 从数据库 schema、抓取的数据样本、数据仓库查询日志、dbt、LookML、wiki、知识库、MCP 来源、SaaS 应用和网页中引导生成上下文。
- 每个提取出的上下文片段都有置信度分数，管理员可以自动接受高置信度条目，并审核边界情况。
- 用户反馈驱动学习：明确反馈会直接存储，含糊反馈会触发离线生成，并测试多个候选 SQL 查询。
- 新上下文在存储前会与现有上下文比对，用于检测冲突，例如 “revenue” 的两个定义，或同一筛选条件的两个列映射。
- 评估分为三个阶段：仅使用 schema 和采样的基线阶段，加入知识文件后的引导阶段，以及基于执行输出进行单次反馈、同时隐藏真实 SQL 的学习阶段。

## 结果
- 在来自 livesqlbench-base-full-v1 的 5 个经过筛选的仅查询数据集上，报告的汇总准确率从 20% 的基线提升到加入知识库文件后的 50%，再到上下文学习后的 85%；期间没有更换模型、调优 SQL 或手动构建上下文。
- WisdomAI 报告称，在启用上下文学习循环时，BIRD dev set 上的准确率为 80–92%，同时表示 BIRD 不适合评估企业上下文学习。
- 文章称，LiveSQLBench 排行榜当前第一名在所有案例类型上的准确率为 48%，而 WisdomAI 在其筛选后的仅查询设置上报告为 85%。
- 据称，对建议上下文和已审核查询进行人工审核后，生产准确率可超过 95%。
- 在一个 solar_panel 示例中，学习修正了 “latest” 行选择：基线返回 352 行，而正确答案使用 snapts 和 snapkey 的复合键排序，得到 336 行。
- 在另一个 solar_panel 示例中，学习修正了隐藏的维护成本逻辑：基线返回 $4,850，而正确答案在应用两年内的预期故障并使用正的 MTBF 记录后为 $1,541。

## Problem

## Approach

## Results

## Link
- [https://www.wisdom.ai/blog/how-wisdom-gets-text-to-sql-right](https://www.wisdom.ai/blog/how-wisdom-gets-text-to-sql-right)
