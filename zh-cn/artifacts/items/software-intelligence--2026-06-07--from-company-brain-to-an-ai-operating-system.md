---
source: hn
url: https://medium.com/@calufa/from-company-brain-to-an-ai-operating-system-a9378d697f1a
published_at: '2026-06-07T22:18:40'
authors:
- _hfqa
topics:
- ai-operating-system
- company-brain
- workflow-automation
- multi-agent-systems
- knowledge-base
- human-ai-interaction
relevance_score: 0.8
run_id: materialize-outputs
language_code: zh-CN
---

# From Company Brain to an AI Operating System

## Summary
## 总结
这是一个面向 AI 操作系统的产品架构，把公司数据转成按角色划分的每日简报和可执行工作流。它适用于 AI 工作流自动化和多代理公司运营，但摘录里没有给出量化评估。

## 问题
- 公司负责人每天早上都要查看 CRM、支持、支付、分析、广告、表格、邮件和文件，才能回答最基本的经营问题。
- 公司知识分散在工具、人员、文档、工单、通话、数据库和本地文件中，这让 AI 自动化很难基于当前事实运行。
- 这个系统之所以重要，是因为优先级判断出错会让流失风险、停滞交易、收入变化或目标偏移被掩盖，等发现时公司已经浪费了时间。

## 方法
- 这个系统有 5 层：集中数据源，把数据组织成公司知识库，呈现基于规则的洞察，评估目标，再生成按角色划分的简报。
- 连接器轮询 Stripe、HubSpot、Salesforce、Zendesk、Google Analytics、Meta Ads、Google Ads、Sheets、转录文本、社交媒体、数据库和桌面文件等系统。每个连接器在每次运行时都会回看最多 30 天，并保存原始事件，不覆盖它们。
- 组织层执行实体消歧、模式标准化、增强和预计算的时间序列指标。它保存虚拟表和派生表，方便工作流查询已准备好的公司上下文。
- 以自然语言写下的规则和目标会编译成可执行工作流。确定性脚本处理结构化检查，LLM 调用则对情绪、语气或转录含义等项目进行分类，并把结构化输出写回知识库。
- 一个多模型评审委员会使用 GPT、Claude、Gemini 和 Grok，分 3 个阶段：独立评估、匿名交叉审查和综合。沙箱工作流通过手动、webhook、计划任务、邮件、同步、MCP 或链式触发器运行。

## 结果
- 摘录没有报告基准测试、用户研究、准确率结果、延迟结果、成本结果、留存结果或生产影响指标。
- 最主要的具体主张是一个 5 层操作模型，把分散的公司数据变成受监控的规则、目标报告和早间简报。
- 规则示例会在客户过去 14 天内有至少 2 个负面支持工单、且超过 7 天没有登录时标记流失风险。
- 评审委员会设计使用 4 个前沿模型家族和一个 3 阶段审查流程，来降低单模型失效风险，但文章没有给出幻觉率或准确率下降的实测结果。
- 沙箱支持 7 种触发类型，把 ReAct 代理循环限制在 20 次交互，记录执行轨迹，收集 token 用量和耗时，验证工作流 DAG 以防止成环，并把链深度限制为 10。
- 示例简报包括品牌提及量周环比增长 34%、3 笔交易进入谈判阶段，以及最大一笔交易为 48K ARR，但这些只是产品示例，不是评估结果。

## Problem

## Approach

## Results

## Link
- [https://medium.com/@calufa/from-company-brain-to-an-ai-operating-system-a9378d697f1a](https://medium.com/@calufa/from-company-brain-to-an-ai-operating-system-a9378d697f1a)
