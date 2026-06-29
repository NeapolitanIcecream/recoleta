---
source: arxiv
url: https://arxiv.org/abs/2606.20512v1
published_at: '2026-06-18T17:30:15'
authors:
- Asa Shepard
- Jeannie Albrecht
topics:
- coding-agents
- repository-guidance
- swe-bench
- prompt-tuning
- code-intelligence
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Probe-and-Refine Tuning of Repository Guidance for Coding Agents

## Summary
## 摘要
probe-and-refine tuning 将通用仓库指导改写为紧凑、经过失败检验的指令，从而提高编码代理的 resolve rate。主要收益是代理更常产出可评估补丁。

## 问题
- LLM 编码代理经常缺少特定仓库的操作知识，例如哪些文件包含某个子系统、要运行哪些测试，以及哪些修复容易破坏相关代码。
- 现有 AGENTS.md 风格文件的证据不一致：一些研究报告了效率提升，另一些研究报告代理遵循错误或通用指令时 resolve rate 下降。
- 这很重要，因为错误的仓库指导会把代理引到错误文件，或让它遵循脆弱的工作流，从而降低 bug 修复成功率。

## 方法
- 该方法从一个静态仓库知识库开始，该知识库由 tree-sitter 派生的结构和通用 LLM 编写的指导构成。
- 每次迭代生成 10 个合成 bug 修复探针，然后用单次 LLM 调用尝试修复，并判断当前指导在哪里失败。
- 它将这些失败汇总为对指导文件的编辑，每次迭代最多 5 处编辑，总长度上限为 3000 个字符。
- 每个仓库运行 3–5 次迭代；调优期间不使用工具，不运行代理循环，不使用强化学习，也不进行梯度更新。
- 最终指导由同一个 ReAct 风格编码代理在 SWE-bench Verified 上复用。

## 结果
- 在 500 个 SWE-bench Verified 实例、4 次试验中，Qwen3.5-35B-A3B 在 200 步设置下，probe-and-refine 达到 33.0% 的平均 resolve rate；相比之下，static_kb 为 28.3%，no_context 为 25.5%。
- 论文报告 probe-and-refine 相对 static_kb 和 no_context 的两个对比均为 p<0.001。
- 收益来自覆盖率：精炼后的指导让可评估补丁的实例增加 14.5 个百分点，而每补丁精度保持在约 59%，p=0.119。
- 在 200 步设置下，probe-and-refine 的 fallback 使用率更低：14.8%，而 static_kb 为 30.8%，no_context 为 25.6%。
- 精炼后的产物平均为 2,754 个字符，static_kb 为 1,687 个字符；新增的 104 行中，47% 是流程规则，30% 是结构规则，23% 是质量门规则。
- 主试验报告 probe-and-refine 指导带来 31 个稳定且独有的解决实例。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20512v1](https://arxiv.org/abs/2606.20512v1)
