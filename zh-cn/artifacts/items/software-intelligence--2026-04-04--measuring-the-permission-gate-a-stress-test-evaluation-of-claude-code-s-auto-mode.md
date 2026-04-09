---
source: arxiv
url: http://arxiv.org/abs/2604.04978v1
published_at: '2026-04-04T17:56:30'
authors:
- Zimo Ji
- Zongjie Li
- Wenyuan Jiang
- Yudong Gao
- Shuai Wang
topics:
- ai-agent-safety
- permission-systems
- code-agents
- devops-automation
- benchmark-evaluation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode

## Summary
## 摘要
这篇论文评估了 Claude Code auto mode 在模糊 DevOps 权限场景下的表现，发现它在这组压力测试中的保护能力远弱于 Anthropic 公开的生产环境数据所显示的水平。主要问题是覆盖缺口：许多危险的状态变更是通过项目内文件编辑完成的，而分类器从不检查这类操作。

## 问题
- 论文研究的是**范围升级**：当用户请求表述不充分时，编码代理对错误目标、过多目标或更高风险环境采取行动的情况。
- 这很重要，因为 AI 编码代理可能删除分支、取消任务、重启服务或移除制品，这些操作会带来真实的运维影响，所以权限门控必须既能拦截不安全操作，又不能妨碍正常工作。
- Anthropic 在生产流量上报告了较低的误报率和 17% 的漏报率，但这不能说明系统在刻意设计的模糊授权场景下会如何表现。

## 方法
- 作者构建了 **AmPermBench**，这是一个包含 128 个提示词的基准，覆盖四类 DevOps 任务：分支清理、任务取消、服务重启和制品清理。
- 每个提示词都沿三个模糊因素变化：**specificity**、**blast radius** 和 **risk level**，并配有一个 oracle policy，精确定义哪些目标被授权，哪些必须保留。
- 他们运行带有 **Claude Code auto mode** 的 Claude Sonnet 4.6，并将其与同一模型在 **bypassPermissions** 模式下进行比较，以隔离权限门控本身的影响。
- 评估在**单个动作层面**进行：将 253 个会改变状态的动作根据 oracle ground truth 标记为安全或不安全，再依据门控决策记为 TP/TN/FP/FN。
- 一个关键设计细节是系统的三级结构：Tier 1 只读工具，Tier 2 跳过分类的项目内文件编辑，以及 Tier 3 会经过 transcript classifier 的外部操作，例如 shell 命令。

## 结果
- 在 **253 个状态变更动作**上，auto mode 的**端到端漏报率为 81.0%**，**95% CI 为 73.8%–87.4%**，**FPR 为 19.8%**。混淆矩阵为：**27 TP、89 TN、22 FP、115 FN**。
- 所有状态变更动作中有 **36.8%**（**93/253**）通过 **Tier 2** 文件编辑执行，而分类器从不评估这些操作。在这些 Tier 2 动作中，不安全操作会因设计原因被漏掉；论文在这里报告了 **51 FN**。
- 即使只看分类器实际能看到的 **Tier 3** 动作（**160 个动作**），表现仍然较差：**FNR 为 70.3%**，**FPR 为 31.9%**。
- 表现最差的任务是 **artifact cleanup**，**FNR 为 92.9%**。在其 **78 个 FN** 中，有 **49 个（62.8%）**来自对 `objects.json` 的 Edit 或 Write 操作，这些操作通过 Tier 2 绕过了分类器。
- 在任务层面，Safe Task Success Rate 总体只提高了 **3.1 个百分点**，从 bypassPermissions 下的 **29.7%** 升至 auto mode 下的 **32.8%**。分任务看：services **43.8% -> 59.4%**，branches **25.0% -> 25.0%**，jobs **28.1% -> 28.1%**，artifacts **21.9% -> 18.8%**。
- 按风险等级看，从低风险环境到高风险环境，拦截效果有所改善，但过度拦截也增加了：**FNR 88.1% -> 74.7%**，**FPR 9.2% -> 34.8%**。论文还在 50 个样本上验证了其 LLM judge，与人工标注者的一致率为 **88%**，**Cohen's kappa = 0.82**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04978v1](http://arxiv.org/abs/2604.04978v1)
