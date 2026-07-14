---
source: arxiv
url: https://arxiv.org/abs/2607.11390v1
published_at: '2026-07-13T10:54:38'
authors:
- Minase Mekete Mengistu
- Juri Di Rocco
- Phuong T. Nguyen
- Davide Di Ruscio
topics:
- infrastructure-as-code
- llm-agents
- automated-repair
- cloud-security
- terraform
- tool-grounding
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# TerraRepair: A Tool-Grounded LLM Agent for Infrastructure-as-Code Repair

## Summary
## 摘要
TerraRepair 使用配备 Terraform 依赖检索、已安装提供商架构、扫描器反馈和结构化升级机制的 LLM agent，修复云安全问题。在所研究的基准测试中，与一次性基线相比，它将扫描器验证的 AWS 修复率提高了 51.8 个百分点（Checkov）和 27.6 个百分点（Trivy）；缺少部署特定上下文时，系统无法完全自主完成修复。

## 问题
- Terraform 安全扫描器可以识别配置错误，但开发者仍需创建有效修复，同时保留安全意图并匹配已安装的云提供商架构。
- 一次性 LLM 修复可能编造不受支持的 Terraform 构造，产生验证错误，或仅抑制扫描器警告就声称修复成功。
- 这个问题会影响部署安全：无效或语义上不安全的基础设施变更可能在通过基本扫描器检查后进入部署。

## 方法
- TerraRepair 为每个扫描器发现运行一个 ReAct 风格的 agent，最多执行十个修复步骤。
- agent 查询依赖图以获取跨资源值，检索已安装的 Terraform 提供商架构，提出一个资源块补丁，并对该补丁重新运行扫描器。
- 只有在原始问题消失后，系统才会返回经扫描器验证的修复；如果缺少部署所需的特定信息，或修复过程未能收敛，系统会发出结构化升级。
- 评估在 TerraGoat 和 KaiMonkey 的 AWS、Azure 和 GCP 环境中进行，将 TerraRepair 与受控的一次性基线进行比较。两者使用相同的模型、扫描器版本、问题集合、补丁逻辑和最终重新扫描流程。

## 结果
- 在合并后的 AWS 基准测试中，TerraRepair 使用 Checkov 达到 78.4% +/- 0.8% 的扫描器验证修复率，基线为 26.6% +/- 1.4%，提高了 51.8 个百分点。
- 使用 Trivy 时，TerraRepair 的修复率为 72.4% +/- 4.0%，基线为 44.8% +/- 1.4%，提高了 27.6 个百分点。
- 基线的声称修复率与验证修复率之间的差距为 44.8 至 73.6 个百分点；TerraRepair 将该差距降至 -2.9 至 +1.8 个百分点。
- 在对 171 个经扫描器验证的 AWS 修复进行语义审计时，多数投票认为其中 135 个正确，即 78.9%；95% 置信区间为 72.2% 至 84.4%，Fleiss' kappa 为 0.54。
- 在 TerraGoat AWS 中，移除架构查询会使 Checkov 修复率下降 21.7 个百分点，移除依赖图检索会使修复率下降 15.6 个百分点；移除扫描器反馈只会使修复率下降 1.1 个百分点。
- 在完整评估中，TerraRepair 对 25.4% 的问题进行升级，其中 82.7% 的升级由缺少外部部署上下文导致。它在 AWS 中没有引入新的 Terraform 验证错误，但在 Azure 和 GCP 修复中引入了 26 个新错误。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11390v1](https://arxiv.org/abs/2607.11390v1)
