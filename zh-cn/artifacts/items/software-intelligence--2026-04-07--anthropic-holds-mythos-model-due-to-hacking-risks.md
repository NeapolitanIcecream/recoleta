---
source: hn
url: https://www.axios.com/2026/04/07/anthropic-mythos-preview-cybersecurity-risks
published_at: '2026-04-07T23:02:18'
authors:
- FergusArgyll
topics:
- cybersecurity
- vulnerability-discovery
- autonomous-agents
- code-intelligence
- model-release-policy
relevance_score: 0.71
run_id: materialize-outputs
language_code: zh-CN
---

# Anthropic holds Mythos model due to hacking risks

## Summary
## 摘要
Anthropic 正在限制 Mythos Preview 的访问，因为该模型可以自主发现并利用软件漏洞，其能力水平让公司认为不适合公开发布。这篇文章将 Mythos 描述为一个高端的网络安全模型，可用于进攻和防御，并介绍了 Anthropic 的受控发布计划。

## 问题
- 文章关注的是这样一类 AI 系统：它们发现并武器化软件缺陷的速度更快、规模更大，超过了人类安全研究员。
- 这很重要，因为一个具备强大自主找漏洞和编写利用代码能力的模型，既可以帮助防守方加固代码，也可能帮助攻击者攻破操作系统、浏览器、服务器和关键基础设施。
- Anthropic 将不受控发布视为安全风险，因此眼下的问题是，如何把这种模型用于防御，同时又不让进攻性滥用变得容易。

## 方法
- Anthropic 将 Mythos Preview 构建为一个“高度自主”的模型，具备面向网络安全任务的高级推理能力，目标能力水平接近高级安全研究员。
- 简单说，这个模型可以扫描软件、发现漏洞、复现漏洞，并在几乎不需要人工帮助的情况下编写概念验证利用代码或利用链。
- Anthropic 没有公开发布它，而是只向少数经过审核的组织开放访问，让它们用该模型对自己的代码和开源系统进行防御性扫描。
- 这次发布还包括 Project Glasswing，由 AWS、Apple、Cisco、Google、Microsoft、Nvidia、Palo Alto Networks 和 Linux Foundation 等大型机构在真实安全工作流中测试该模型。
- Anthropic 还为这次发布配套了防护措施、政府简报，以及对测试人员和开源安全团体的资金支持。

## 结果
- 根据 Anthropic 的说法，Mythos Preview 可以发现“数以万计的漏洞”。文章没有给出支持这一说法的基准测试表或正式评估设置。
- Anthropic 表示，其此前公开发布的模型 Opus 4.6 在开源软件中发现了约 **500 个零日漏洞**，而 Mythos Preview 的产出远高于这个数字。
- 在测试中，Mythos Preview 在**所有主要操作系统和网页浏览器**中都发现了漏洞，其中包括一些被认为已有**数十年历史**、且多轮人工安全测试都未发现的缺陷。
- 该模型在 **83.1% 的案例**中，第一次尝试就成功复现了漏洞并生成概念验证利用代码。
- Anthropic 表示，该模型发现了多个 Linux 内核缺陷，并自主将其串联起来，从而能够**完全控制一台 Linux 机器**。
- 在另一项报告中的案例里，该模型发现了一个已有 **27 年历史**的 OpenBSD 漏洞，可能让攻击者**远程使任何运行该系统的机器崩溃**。

## Problem

## Approach

## Results

## Link
- [https://www.axios.com/2026/04/07/anthropic-mythos-preview-cybersecurity-risks](https://www.axios.com/2026/04/07/anthropic-mythos-preview-cybersecurity-risks)
