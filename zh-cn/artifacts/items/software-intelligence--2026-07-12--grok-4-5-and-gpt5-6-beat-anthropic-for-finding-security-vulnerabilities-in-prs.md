---
source: hn
url: https://docs.damsecure.ai/blog/pr-review-security-benchmark/
published_at: '2026-07-12T22:57:23'
authors:
- pcollins123
topics:
- code-intelligence
- security-review
- software-foundation-models
- automated-software-production
- human-ai-interaction
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Grok 4.5 and GPT5.6 beat Anthropic for finding security vulnerabilities in PRs

## Summary
## 摘要
Dam Secure 使用 10 个包含预置访问控制漏洞的合成 PR，对 10 个 AI 模型进行了拉取请求安全审查基准测试。在报告的成本与质量前沿中，GPT-5.6 Sol 领先；Grok 4.5 和 Gemini 3.1 Flash Lite 提供了成本更低的替代方案。

## 问题
- 安全团队需要能够检测拉取请求中新增代码所引入漏洞的模型。
- 模型选择会影响召回率、误报率、审查成本和 token 用量。
- 全代码扫描结果无法直接衡量拉取请求审查性能。

## 方法
- 基准测试使用了 10 个 PR，每个 PR 都包含一个预置的访问控制缺陷，例如 IDOR、缺少身份验证或授权失效。
- 每个模型都使用相同的 Dam Secure 扫描器和工具集运行五次。智能体可以读取完整文件，也可以使用 grep 搜索变更文件。
- 数据集由私有合成代码仓库和嵌入真实提交历史、按时间逆向重放的真实 CVE 组成。
- 研究人员使用召回率、精确率、F1、每个 PR 的成本，以及每个真实阳性的成本，根据隐藏的真实标签对发现结果进行评分。
- 作者还测试了 Pydantic 和 Claude Code 工具链，并报告了相近的排名。

## 结果
- GPT-5.6 Sol 的召回率为 100%，F1 为 0.91，每个 PR 的成本为 $0.70。作者报告称，在性能相近的情况下，它的成本比 GPT-5.5 低约 45%。
- Grok 4.5 以每个 PR $0.20 的成本进入报告中的前沿，F1 为 0.77，召回率为 74%，精确率为 80.4%。
- Gemini 3.1 Flash Lite 的每个 PR 成本约为 $0.04，F1 为 0.75，召回率为 68%，精确率为 82.9%。
- 使用 Opus 4.8 回退配置的 Fable 5，每个 PR 的成本约为 $3.61，在质量和成本两项指标上都低于 GPT-5.6 Sol。10.7% 的运行触发了回退。
- 测试的 Anthropic 模型均未进入报告中的成本与质量前沿。
- 该基准测试只覆盖 PR 扫描，因此不能据此确定模型在开放式全代码漏洞扫描中的排名。

## Problem

## Approach

## Results

## Link
- [https://docs.damsecure.ai/blog/pr-review-security-benchmark/](https://docs.damsecure.ai/blog/pr-review-security-benchmark/)
