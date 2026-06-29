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
Anthropic 正在限制 Mythos Preview 的访问，因为这个模型可以自主发现并利用软件漏洞，而且公司认为它的能力已经危险到不适合公开发布。文章把 Mythos 描述为一款高端的进攻和防御型网络安全模型，并介绍了 Anthropic 的受控发布计划。

## 问题
- 这篇文章关注的是能比人工安全研究人员更快、规模更大地发现并武器化软件漏洞的 AI 系统。
- 这一点很重要，因为具备强自主找漏洞和写利用代码能力的模型，既能帮助防守方加固代码，也能帮助攻击者攻陷操作系统、浏览器、服务器和关键基础设施。
- Anthropic 认为失控发布会带来安全风险，所以眼前的问题是，如何把这种模型用于防御，同时又不让它容易被滥用来做进攻。

## 方法
- Anthropic 把 Mythos Preview 做成了一个“极度自主”的模型，面向网络安全任务提供高级推理能力，目标接近资深安全研究员的水平。
- 直接说，这个模型会扫描软件、找出漏洞、复现漏洞，并在很少人工帮助下写出概念验证利用代码或利用链。
- Anthropic 没有公开发布，而是把访问权限给少量经过审核的组织，让他们用它来防御性扫描自己的代码和开源系统。
- 这次发布包含 Project Glasswing，AWS、Apple、Cisco、Google、Microsoft、Nvidia、Palo Alto Networks 和 Linux Foundation 等公司会在真实的安全工作流里测试这个模型。
- Anthropic 还配套了防护措施、政府简报，以及对测试者和开源安全组织的资金支持。

## 结果
- Anthropic 说，Mythos Preview 可以找到“数以万计的漏洞”。文章没有给出这个说法的基准表或正式评估设置。
- Anthropic 表示，之前公开的模型 Opus 4.6 在开源软件中找到了大约 **500 个零日漏洞**，而 Mythos Preview 的产出远高于这个数字。
- 在测试中，Mythos Preview 在 **所有主要操作系统和网页浏览器** 中都找到了漏洞，其中包括一些被认为有 **几十年历史**、而且在多次人工安全测试中都没被发现的漏洞。
- 这个模型在 **83.1% 的案例**里第一次尝试就复现了漏洞，并创建了概念验证利用代码。
- Anthropic 说，这个模型找到了多个 Linux 内核漏洞，并且自主把它们串联起来，实现了对 Linux 机器的 **完全控制**。
- 另一个报告案例中，这个模型找到了一个 **27 年前**的 OpenBSD 漏洞，攻击者可以借此 **远程让运行它的任何机器崩溃**。

## Problem

## Approach

## Results

## Link
- [https://www.axios.com/2026/04/07/anthropic-mythos-preview-cybersecurity-risks](https://www.axios.com/2026/04/07/anthropic-mythos-preview-cybersecurity-risks)
