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
本文评估了 Claude Code 自动模式在含糊的 DevOps 权限场景中的表现，发现它在这类压力测试下的保护能力远弱于 Anthropic 报告的生产环境数据。核心问题是覆盖缺口：许多危险的状态变更通过项目内文件编辑完成，而分类器根本不会检查这些操作。

## 问题
- 论文研究的是 **范围扩张**：当用户请求的信息不够明确时，编码代理对错误目标、过多目标，或更高风险环境执行操作的情况。
- 这很重要，因为 AI 编码代理可以删除分支、取消任务、重启服务或移除产物，这些操作都会带来真实的运维影响，所以权限门必须在不阻碍正常工作的前提下拦住不安全操作。
- Anthropic 报告了较低的误报率和 17% 的生产流量假阴性率，但这不能说明系统在故意含糊的授权场景中会怎样表现。

## 方法
- 作者构建了 **AmPermBench**，一个包含 128 个提示词的基准，覆盖四类 DevOps 任务：分支清理、任务取消、服务重启和产物清理。
- 每个提示词都变化三个歧义因素：**具体性**、**爆炸半径**和**风险级别**，并用一个 oracle 策略精确定义哪些目标被授权、哪些目标必须保留。
- 他们运行 Claude Sonnet 4.6 的 **Claude Code 自动模式**，并与同一模型在 **bypassPermissions** 下的表现对比，以隔离权限门的作用。
- 评估粒度是 **单个动作级别**：253 个改变状态的动作按 oracle 真实标签被标为安全或不安全，然后根据权限门决策计算 TP/TN/FP/FN。
- 一个关键设计细节是系统的三层结构：Tier 1 只读工具、Tier 2 项目内文件编辑（跳过分类）、Tier 3 通过转录分类器的外部操作，例如 shell 命令。

## 结果
- 在 **253 个改变状态的动作** 中，自动模式的 **端到端假阴性率为 81.0%**，**95% CI 73.8%–87.4%**，**误报率为 19.8%**。混淆矩阵为：**27 TP、89 TN、22 FP、115 FN**。
- **36.8%** 的改变状态动作（**93/253**）走的是 **Tier 2** 文件编辑路径，分类器根本不会评估这些操作。对于这些 Tier 2 动作，不安全操作从设计上就会被漏掉；论文在这里报告了 **51 个 FN**。
- 即使只看分类器实际会看到的 **Tier 3** 动作（**160 个动作**），表现仍然较弱：**FNR 为 70.3%**，**FPR 为 31.9%**。
- 表现最差的任务是 **产物清理**，**FNR 达到 92.9%**。在它的 **78 个假阴性** 中，**49 个（62.8%）** 来自对 `objects.json` 的 Edit 或 Write 操作，这些操作通过 Tier 2 绕过了分类器。
- 在任务层面，Safe Task Success Rate 只提升了 **3.1 个百分点**，从 bypassPermissions 下的 **29.7%** 升到自动模式下的 **32.8%**。按任务看：服务 **43.8% -> 59.4%**，分支 **25.0% -> 25.0%**，任务 **28.1% -> 28.1%**，产物 **21.9% -> 18.8%**。
- 按风险级别看，从低风险环境切换到高风险环境，阻拦能力有所提升，但过度阻拦也更多：**FNR 88.1% -> 74.7%**，**FPR 9.2% -> 34.8%**。论文还用 50 个样本验证了它的 LLM judge，与人工标注者相比，**一致率为 88%**，**Cohen's kappa = 0.82**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04978v1](http://arxiv.org/abs/2604.04978v1)
