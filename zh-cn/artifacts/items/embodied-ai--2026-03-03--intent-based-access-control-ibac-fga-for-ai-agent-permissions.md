---
source: hn
url: https://ibac.dev
published_at: '2026-03-03T23:57:52'
authors:
- ERROR_0x06
topics:
- ai-agent-security
- prompt-injection
- access-control
- fine-grained-authorization
- tool-use
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Intent-Based Access Control (IBAC) – FGA for AI Agent Permissions

## Summary
IBAC是一种面向AI代理的权限控制方法：它不试图让模型更会识别提示注入，而是把用户显式意图转成细粒度权限，并在每次工具调用前强制校验。核心主张是将提示注入从“检测问题”变成“即使模型被误导也无法越权执行”的授权问题。

## Problem
- AI代理在调用邮件、数据库、外部API等工具时，容易受到提示注入影响，导致模型按照恶意指令执行未被用户授权的操作。
- 现有防御常依赖输入过滤、LLM裁判或输出分类器，本质上仍要求模型“识别攻击”，因此不够稳定、可解释或确定性强。
- 这很重要，因为一旦代理连接真实工具，越权行为会直接造成数据泄露、错误操作或安全事故。

## Approach
- 将用户的**显式意图**解析为FGA（细粒度授权）元组，例如把“允许给Bob发邮件”编码成可检查的权限关系。
- 在每一次工具调用之前，基于这些元组做一次确定性的授权检查；若动作不在意图授权范围内，则直接阻止。
- 集成点只有两个：**意图解析后写入FGA元组**，以及**每次工具调用前执行校验**。
- 该机制不依赖自定义解释器、不需要双LLM架构、也不要求修改现有代理框架；额外开销据称仅为**1次额外LLM调用**加上授权检查。

## Results
- 文本给出的主要性能数字是：需要**1次额外LLM调用**，以及约**9ms**的授权检查延迟。
- 作者声称该方案可在**几分钟内**接入运行，并且只需**两个集成点/四个部署步骤**（启动OpenFGA、定义模型、写元组、查权限）。
- 未提供标准数据集、基准测试或攻击成功率等系统性定量结果，因此**没有可报告的学术基准数值**。
- 最强的具体主张是：即使提示注入“彻底破坏了LLM推理”，未获授权的工具调用仍会被确定性阻止，从而让提示注入对执行层“失去相关性”。

## Link
- [https://ibac.dev](https://ibac.dev)
