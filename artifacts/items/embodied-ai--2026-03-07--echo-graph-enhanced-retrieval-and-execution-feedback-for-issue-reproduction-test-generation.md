---
source: arxiv
url: http://arxiv.org/abs/2603.07326v1
published_at: '2026-03-07T20:11:30'
authors:
- Zhiwei Fei
- Yue Pan
- Federica Sarro
- Jidong Ge
- Marc Liu
- Vincent Ng
- He Ye
topics:
- issue-reproduction
- test-generation
- code-graph-retrieval
- execution-feedback
- fail-to-pass-validation
relevance_score: 0.03
run_id: materialize-outputs
---

# Echo: Graph-Enhanced Retrieval and Execution Feedback for Issue Reproduction Test Generation

## Summary
Echo 是一个用于自动生成“问题复现测试”的代理系统，目标是从含糊的 issue 描述中产出可执行、可验证的失败测试。它把代码图检索、自动执行、补丁辅助验证和基于反馈的迭代修正结合起来，在 SWT-Bench Verified 上达到新的开源 SOTA。

## Problem
- 论文解决的是**根据 issue 报告自动生成 bug 复现测试**的问题；这很重要，因为缺少可复现测试会拖慢定位根因、修复缺陷和 CI 质量保障。
- 现有方法常见瓶颈包括：代码上下文检索不准、真实仓库中的测试执行命令难以自动发现，以及缺少可靠 oracle 来判断测试是否真在复现该 bug。
- 如果测试只是“报错”但不是因目标 bug 报错，开发者仍然得手工排查，因此需要满足 **fail-to-pass**：在原始版本失败、在修复版本通过。

## Approach
- Echo 先把仓库转成一个**异构代码图**（文件、语法树节点、文本块及其关系），再用 LLM 驱动的**自动查询改写**反复检索，直到拿到足够且紧凑的 focal code 与相关回归测试。
- 它使用一个补丁生成器产生**候选修复补丁**，把补丁后的代码库当作近似 oracle，帮助判断生成的测试是否满足 fail-to-pass。
- 在测试生成阶段，LLM 基于 issue、焦点代码、相关测试和补丁，生成**单个独立的最小复现测试文件**，而不是采样大量候选再排序。
- Echo 会**自动推断并执行测试命令**，在受限只读容器中运行该测试，收集执行日志作为反馈。
- 若测试未通过语义验证或双版本检查，系统会把执行日志回灌给生成器迭代修改；双版本检查是**规则式**的，不依赖 LLM，最多重试两次。

## Results
- 在 **SWT-Bench Verified (SWT-Bench-V)** 上，Echo 报告 **66.28% success rate**，论文声称这是**开源方法中的新 SOTA**。
- 相比以往常见的“生成多个候选再筛选”，Echo 强调**每个 issue 只生成一个测试**，主打更好的**成本-性能权衡**；但摘录中未给出具体成本数字或与各基线的逐项百分比差值。
- 论文明确声称其**自动执行生成测试**是“**first-of-its-kind**”特性，可更自然地接入真实开发工作流。
- 摘录未提供完整排行榜数字、方差、显著性检验，或对具体基线（如 e-Otter++ / Issue2Test）的详细数值对比；可确认的最核心定量结果是 **66.28%**。

## Link
- [http://arxiv.org/abs/2603.07326v1](http://arxiv.org/abs/2603.07326v1)
