---
source: arxiv
url: https://arxiv.org/abs/2607.14573v1
published_at: '2026-07-16T05:08:20'
authors:
- Shiyu Ying
- Xuejie Cao
- Yingfan Ma
- Yuanhao Dong
- Wenyu Chen
- Bowen Song
- Lin Zhu
topics:
- coding-agents
- software-engineering-benchmarks
- payment-integration
- repository-level-evaluation
- secure-software
- agent-skills
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Alipay-PIBench: A Realistic Payment Integration Benchmark for Coding Agents

## Summary
## 摘要
Alipay-PIBench 是一个仓库级基准，用于测试编码代理能否在真实业务应用中实现安全、可靠、端到端的支付宝支付集成。它覆盖九个特定支付产品项目和 18 个任务实例，评估功能完成情况与风险加固能力。

## 问题
- 通用编码基准通常无法覆盖服务端凭证保护、签名验证、异步通知处理，以及支付状态与本地业务状态一致性等领域要求。
- 支付集成错误可能造成资金安全风险、错误履约、状态重复转换和不安全退款，因此仅评估源代码补全能力并不充分。

## 方法
- 该基准将九个支付宝支付产品及其业务代码仓库，与两个渐进式场景配对：基础场景“功能性支付完成”和高级场景“风险感知的支付加固”。
- 任务要求跨前端、后端、支付 API、配置和业务状态逻辑进行仓库级修改；高级任务测试幂等性、异常交易、通知真实性、重复确认和退款防护。
- 针对各场景的评分标准会生成确定性的静态、单元、集成和端到端检查，并通过 LLM 辅助评估补充对产品适配性、状态一致性等语义属性的判断。
- 加权评分标准通过率（RPR）为集成检查和端到端检查赋予 2 的权重，为静态、单元和 LLM 辅助检查赋予 1 的权重。
- 配对试验在固定的任务和环境条件下，对比六个模型在使用和不使用官方 alipay-payment-integration skill 时的表现。

## 结果
- 在六个模型和 18 个任务实例中，使用 skill 时的平均 RPR 范围为 68.58% 至 91.37%。
- 使用 skill 后，平均 RPR 平均提高 10.31 个百分点；在 108 个模型—产品—场景对比中，有 101 个出现提升。
- 基础任务的平均提升幅度（+11.27 个百分点）大于高级任务（+9.35 个百分点）。
- 该基准区分了源代码级完成、可执行的支付行为和支付领域要求，说明评估支付集成需要多个评估信号和渐进式场景。
- 摘录未提供完整的逐模型、逐产品或不使用 skill 的得分表，因此它对 skill 效果的总体结论支持更充分，对详细模型排名的支持较弱。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14573v1](https://arxiv.org/abs/2607.14573v1)
