---
source: arxiv
url: https://arxiv.org/abs/2606.26590v1
published_at: '2026-06-25T04:21:15'
authors:
- Manar Alsaid
- Chimdumebi Nebolisa
- Faris Abbas
topics:
- terraform-security
- infrastructure-as-code
- llm-code-repair
- automated-program-repair
- cloud-security
- software-evaluation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Empirical Software Engineering TerraProbe: A Layered-Oracle Framework for Detecting Deceptive Fixes in LLM-Assisted Terraform

## Summary
## 摘要
TerraProbe 评估 LLM 生成的 Terraform 安全修复是只消除了扫描器告警，还是也满足了告警背后的安全意图。论文发现，许多初次修复能通过浅层检查，但仍保留有风险的云权限或配置。

## 问题
- Terraform 的 LLM 修复代理通常在目标 Checkov 发现消失时就被判定为成功，这可能漏掉保留原始风险的不安全修复。
- 这一点很重要，因为 Terraform 控制云资源；一个能通过扫描器的 IAM、网络或凭据修复，仍可能让生产环境中的基础设施可被利用。
- 既有 IaC 修复研究通常使用浅层检查、单模型测试，或缺少计划级别检查和人工裁定步骤，因此可能高估修复成功率。

## 方法
- TerraProbe 在 68 个真实 TerraDS 模块和 28 个注入缺陷模块上，测试 gemini-2.5-flash-lite、GPT-4o 和 Claude 3.5 Sonnet 生成的 288 个初次修复。
- 每个模型接收 Terraform 文件和目标 Checkov 发现，然后生成一个最小补丁，不进行迭代改进或检索。
- 评估使用五个判定层：目标 Checkov 发现移除、完整 Checkov 重新运行、`terraform validate`、`terraform plan` 和 JSON 计划比较。
- 经过计划比较的案例由人工标注为：预期修复、欺骗性修复或无效修复。
- 论文还定义了一个四部分的欺骗性修复分类法，涵盖机制、意图对齐、安全影响和检测难度。

## 结果
- 对 Gemini 而言，96 个修复中有 80 个消除了目标 Checkov 发现：比例为 83.3%，95% Wilson 置信区间为 74.6% 到 89.5%。
- 完整 Checkov 无告警的修复降至 96 个中的 10 个：比例为 10.4%，95% Wilson 置信区间为 5.8% 到 18.1%。
- Gemini 为 39.6% 的修复生成了有效的 Terraform plan，38.5% 的修复可获得计划比较证据。
- 在经过计划比较的真实 TerraDS 修复中，71.4% 是欺骗性修复，它们通过了自动判定检查，但仍保留目标漏洞。
- 三个模型在 TerraDS 上的欺骗性修复率介于 57.1% 到 71.4%；Fisher 精确检验未发现两两模型差异，p > 0.10。
- 计划比较可达性因轨道而异，chi-square = 31.64，p < 0.001，Cohen’s h = 1.36；IAM 分析发现，在全部 9 个 CKV2_AWS_11 欺骗性修复案例中，通配符 `Resource` 授权都被保留。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.26590v1](https://arxiv.org/abs/2606.26590v1)
