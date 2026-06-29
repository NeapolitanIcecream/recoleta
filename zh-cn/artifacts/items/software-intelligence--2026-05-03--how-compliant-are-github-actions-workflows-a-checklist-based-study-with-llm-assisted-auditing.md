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
本文研究 LLM 是否能依据文档中的最佳实践审计 GitHub Actions 工作流。核心结论是，LLM 可以扩大测量规模，但可靠审计仍需要 GPT-5 处理分歧并进行人工检查。

## 问题
- GitHub Actions 工作流可以通过语法检查，但仍可能违反安全、可维护性和性能方面的实践，例如权限过宽、密钥硬编码、动作未固定版本，以及缺少失败通知。
- 现有工具如 actionlint 和 yamllint 只能检查 YAML 是否格式错误、动作引用是否无效，不能判断工作流是否符合 GitHub 文档。
- 这很重要，因为 CI 工作流错误会泄露密钥、扩大 token 访问范围、拖慢构建，并让故障更难排查。

## 方法
- 作者从 GitHub Actions 官方文档中提炼出一份 30 项合规检查清单，覆盖 4 个工作流部分和 8 个主题。
- 他们把每个检查项都改写成 YES、NO 或 NOT APPLICABLE 的审计问题。
- 他们在 95 个真实世界的 Java GitHub Actions 工作流上测试了 4 个开权重 LLM，每个模型完成 2,850 次检查，总计 11,400 个模型输出。
- 他们接受全票和近乎全票的模型投票，把分歧案例交给 GPT-5，再对未解决案例进行针对性人工复核。

## 结果
- 这份检查清单包含 30 项标准：3 项工作流级、11 项作业级、15 项步骤级，以及 1 项权限级标准。
- 在 2,850 个检查问题中，4 个模型全票一致的有 758 个案例（27%），近乎全票一致的有 1,104 个案例（39%），分歧的有 988 个案例（35%）。
- 模型间一致性只有一般水平，Fleiss' kappa = 0.28。
- GPT-5 加人工复核的流程把核验工作量减少了 81%，同时与专家判断保持 87% 一致。
- 在大规模评估中，整体工作流合规率为 28%；权限控制合规率为 4%，Security 为 26%，Clarity 为 68%。
- 论文认为，LLM 适合大规模合规扫描，但对安全敏感、依赖结构的判断仍需要裁定和专家复核。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02091v1](https://arxiv.org/abs/2605.02091v1)
