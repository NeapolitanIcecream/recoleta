---
source: hn
url: https://ibac.dev
published_at: '2026-03-03T23:57:52'
authors:
- ERROR_0x06
topics:
- ai-agent-security
- fine-grained-authorization
- prompt-injection-defense
- tool-call-guardrails
- openfga
relevance_score: 0.92
run_id: materialize-outputs
---

# Intent-Based Access Control (IBAC) – FGA for AI Agent Permissions

## Summary
IBAC提出一种把AI代理权限直接绑定到用户显式意图上的访问控制方案，用细粒度授权替代“识别提示注入”的防御思路。其核心主张是：即使LLM被注入攻击影响推理，只要每次工具调用都做确定性权限检查，未获授权的动作也会被阻止。

## Problem
- 现有提示注入防御通常依赖让模型更聪明地识别攻击，如输入过滤、LLM裁判、输出分类器，但这类方法在模型推理被操纵时仍可能失效。
- AI代理一旦能调用邮件、数据库、外部API等工具，错误或恶意的工具调用会直接造成真实世界风险，因此需要比“检测攻击”更可靠的执行时约束。
- 该问题重要在于代理系统正走向生产环境；如果不能把用户真实意图稳定地转化为可执行权限边界，自动化软件与智能代理就难以安全落地。

## Approach
- 核心机制很简单：先把用户的显式请求解析成细粒度FGA权限元组，再在每一次工具调用前检查该调用是否被这些元组允许。
- 论文式表述中的两大集成点是：**意图解析后写入FGA tuples**，以及**每次tool call前执行授权检查**。
- 这种设计把安全问题从“判断提示是否恶意”转成“该动作是否被用户意图授权”，因此即便提示注入污染了模型内部推理，未授权动作仍会被确定性拦截。
- 实现上依赖OpenFGA等细粒度授权系统；作者声称无需自定义解释器、无需双LLM架构、也无需修改现有代理框架，只增加一次LLM调用用于意图解析。

## Results
- 文中给出的主要量化开销是：额外**1次LLM调用**用于将用户意图解析为权限元组。
- 每次授权检查的延迟约为**9ms**（~9ms authorization check）。
- 部署复杂度声明较低：作者称只需**4个步骤**即可运行，包括启动OpenFGA、定义授权模型、写入元组、工具调用前检查。
- 文段**没有提供标准数据集、成功率、攻击阻断率、误报率或与基线方法的系统性对比数字**。
- 最强的具体主张是：相较输入过滤、LLM-as-a-judge、输出分类器等依赖模型识别攻击的方法，IBAC通过确定性工具级授权，让提示注入“变得无关紧要”。

## Link
- [https://ibac.dev](https://ibac.dev)
