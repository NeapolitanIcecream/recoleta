---
source: arxiv
url: https://arxiv.org/abs/2605.25665v1
published_at: '2026-05-25T10:15:24'
authors:
- Satadru Sengupta
- Tamunokorite Briggs
- Ivan Myshakivskyi
topics:
- software-foundation-models
- code-intelligence
- multi-agent-software-engineering
- automated-software-production
- human-ai-interaction
- agent-verification
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Meta-Engineering Harnesses for AI-Native Software Production: A Contract-Driven Adversarial Verification Architecture with Early Deployment Report

## Summary
## 摘要
本文提出一种面向 AI 原生软件生产的、由契约驱动的 harness，目标是让由智能体构建的软件更容易在重复性工作中进行验证、部署和改进。

## 问题
- AI 编码智能体可以生成有用产物，但生产工作需要持续的验证、维护、部署和升级。
- 小型服务公司常常需要网站、预订、支付、工作流自动化和 AI 智能体接口，而内部没有技术团队。
- 单次提示和一次性人工审查会漏掉隐藏假设、契约缺口、模型盲区和业务规则失效。

## 方法
- 该 harness 将原始运营需求转成明确契约，契约定义行为、角色、API、状态转换、不变量、错误、认证规则、QA 目标和验收标准。
- 双阶段契约编译器先补全缺失假设，再移除未被支持的范围并改写含糊条款。
- 角色专门化智能体分别处理契约编译、实现、对抗性测试生成、产品审查、架构审查、安全审查、QA、交付和仲裁。
- 验证使用彼此独立的构建者和测试者智能体执行基于契约的测试，并结合面向产品、架构、UX、安全、后端、前端和部署风险的按角色审查流程。
- 一个四方仲裁器把失败归类为 bug、规格缺口、噪声或契约歧义，然后把下一步动作分派到实现修复、契约更新、验证器校准或重启。

## 结果
- 早期部署覆盖 3 到 4 周和 17 个功能，包括应用内支付、排期、产品落地页、Slack 通知、MCP 搜索工具集成、6 个服务提供商网站和 bug 修复。
- 系统针对各个功能生成了 18 套对抗性测试套件，另为排期模块生成了 15 套额外校准套件。
- 它在合并前发现了 5 个 bug 或实现缺口，包括缺失的 Slack 通知字段和一次代码库规范违规。
- 在支付案例研究中，后端在 2 个循环内通过了 CI，但之后仍漏掉 2 个业务逻辑用例：定金扣减和折扣计算。
- 前端支付流程在 1 次尝试内完成实现，但 React Native 依赖和环境问题需要人工介入。
- 论文报告的是早期运行证据，不是与 SWE-bench、SWE-agent 或其他基线的受控基准比较。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.25665v1](https://arxiv.org/abs/2605.25665v1)
