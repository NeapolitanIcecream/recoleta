---
source: arxiv
url: https://arxiv.org/abs/2605.02091v1
published_at: '2026-05-03T23:21:13'
authors:
- Edward Abrokwah
- Taher A. Ghaleb
topics:
- github-actions
- ci-compliance
- llm-auditing
- software-engineering
- code-intelligence
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing

## Summary
## 摘要
本文研究 LLM 是否能根据文档化的最佳实践审计 GitHub Actions 工作流。主要结论是：LLM 可以扩大测量规模，但可靠审计仍需要 GPT-5 处理分歧，并需要人工检查。

## 问题
- GitHub Actions 工作流可能通过语法检查，却仍违反安全性、可维护性和性能实践，例如权限过宽、硬编码密钥、未固定版本的 actions，以及缺少失败通知。
- actionlint 和 yamllint 等现有工具能发现格式错误的 YAML 和无效的 action 引用，但不能判断工作流是否遵循 GitHub 文档。
- 这很重要，因为 CI 工作流错误可能暴露密钥、扩大令牌访问范围、拖慢构建，并让故障更难诊断。

## 方法
- 作者从官方 GitHub Actions 文档中提炼出一份包含 30 项的合规检查清单，覆盖 4 个工作流部分和 8 个主题。
- 他们将每个检查项转换为 YES、NO 或 NOT APPLICABLE 审计问题。
- 他们在 95 个真实 Java GitHub Actions 工作流上测试 4 个开放权重 LLM，每个模型完成 2,850 项清单评估，总计产生 11,400 个模型输出。
- 他们接受一致和近一致的模型投票，将意见分裂的案例交给 GPT-5，并对未解决的案例进行定向人工审查。

## 结果
- 该清单包含 30 条标准：3 条工作流级标准、11 条任务级标准、15 条步骤级标准，以及 1 条权限级标准。
- 在 2,850 个清单问题中，4 个模型在 758 个案例上完全一致（27%），在 1,104 个案例上近一致（39%），在 988 个案例上意见分裂（35%）。
- 模型间一致性仅为一般，Fleiss' kappa = 0.28。
- GPT-5 加人工审查的流程将验证工作量减少了 81%，同时与专家判断保持 87% 的一致性。
- 在规模化评估中，整体工作流合规率为 28%；权限控制的合规率为 4%，Security 为 26%，Clarity 为 68%。
- 论文认为 LLM 适合用于大规模合规扫描，但涉及安全敏感内容和依赖结构推理的判断仍需要裁决和专家审查。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02091v1](https://arxiv.org/abs/2605.02091v1)
