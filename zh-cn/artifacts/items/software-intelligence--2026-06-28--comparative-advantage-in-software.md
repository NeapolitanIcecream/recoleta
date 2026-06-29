---
source: hn
url: https://achad4.substack.com/p/comparative-advantage-in-software
published_at: '2026-06-28T22:19:35'
authors:
- achad4
topics:
- ai-software-products
- coding-agents
- llm-applications
- product-strategy
- agent-workflows
- restaurant-erp
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# Comparative Advantage in Software

## Summary
## 摘要
这篇文章认为，AI 生成代码之后，软件的价值取决于产品是否能比客户直接使用通用模型更好地降低 token 成本，或提高任务正确性。这是一篇商业和产品策略文章，使用 Kintow 的餐厅运营案例，而非实验研究。

## 问题
- 编码代理降低了构建软件的成本，因此买方需要更明确的理由来为他们可能用 Claude 或其他 LLM 复现的产品付费。
- 轻量 AI 封装如果只是在模型调用之外增加很少功能，价值可能下降。
- 复杂的运营软件在维护状态、执行工作流、避免会让用户损失时间或金钱的错误时，仍然有价值。

## 方法
- 该方法是一个成本模型：通过询问任务需要多少 token、这些 token 有多正确，来比较产品和直接使用 LLM 的差异。
- 产品通过工作流、领域模型、类型化数据和确定性步骤，减少所需的模型推理量，从而创造价值。
- 产品也通过上下文工程、评估、持久状态和纠错工作流，提高正确性，从而创造价值。
- Kintow 将这一思路用于餐厅 ERP 任务，例如库存、损耗、配方、人工、自动采购和发票解析。

## 结果
- 摘录没有报告实验、数据集、基线或准确率指标。
- 文章提出 2 个产品杠杆：降低完成任务所需的 token 数量，并提高每个生成 token 的正确性。
- 自动采购需要精确的状态和审批控制，因为采购可能影响餐厅约 30% 的收入。
- 发票解析可以用 Claude 处理单个文档，但重复运行可能产生差异，并且无法与目录同步；文中提出的修复方法是评估、上下文工程和纠错工作流。
- 最具体的有力主张是，当维护和可靠性成本超过产品成本时，使用电子表格、既有工具或自建系统的客户仍可能购买专业软件。

## Problem

## Approach

## Results

## Link
- [https://achad4.substack.com/p/comparative-advantage-in-software](https://achad4.substack.com/p/comparative-advantage-in-software)
