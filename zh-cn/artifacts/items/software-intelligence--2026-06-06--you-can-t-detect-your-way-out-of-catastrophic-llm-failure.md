---
source: hn
url: https://github.com/joseteiadirector/teia-igo-vs-claude-opus-4.8/blob/main/README.en.md
published_at: '2026-06-06T23:25:17'
authors:
- joseteia26
topics:
- llm-safety
- ai-governance
- failure-containment
- model-monitoring
- red-teaming
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# You can't detect your way out of catastrophic LLM failure

## Summary
## 摘要
这篇论文的主张是，LLM 安全不能只靠检测来阻止灾难性行为；系统需要一种约束，让高破坏性动作根本无法触发。论文提出了观测治理基础设施（IGO），附带公开的 KAPI 公式、生产环境测量，以及与 Claude Opus 4.8 的一场记录在案的压力测试。

## 问题
- 它讨论的是 LLM 灾难性失效：有害动作可能在监控指标发现异常之前就已经发生。
- 这对 AI 代理和自动化系统很重要，因为有些错误还能补救，但涉及不可逆伤害的动作需要明确的运行边界。
- 论文把常见的模型漂移和幻觉检测，与面向毁灭性风险的控制区分开来；后者里，第二轮学习循环可能来得太晚。

## 方法
- IGO 使用 4 层架构：第 1 到第 3 层监测可恢复的失败，第 4 层限制那些必须保持不可触及的动作。
- 摘要中展示的核心指标是 CPI：`CPI = max(0, 100 - (σ_temporal × 2))`，其中时间置信度方差会降低分数。
- CPI 分段是公开的：高于 80 表示稳定，低于 50 表示认知波动严重。
- 这项研究把 Zenodo 上的公开公式、生产数据库测量，以及与 Claude Opus 4.8 的认识论红队辩论结合在一起。
- 直白地说，这种方法会监测模型在可恢复情况下的不稳定，并阻止那些一旦发生就不能接受的高后果动作。

## 结果
- 作者报告称，KAPI 测量覆盖了 4 家有文档记录的机构，涉及公共卫生、高等教育和设计，使用的是数据库中的数据，没有模拟值或估算值。
- 审计覆盖了 4 个全球 LLM；面向客户端的公开数据经过匿名化或汇总处理。
- 据报告，生产案例中的 CPI 大约在 22 到 55 之间，低于作者定义的 80 以上稳定区间，也接近或低于 50 的临界阈值。
- 原生幻觉检测据称捕捉到了严重错误，其中包括一个被评为 HIGH 的 Claude 错误。
- 据报告，Claude Opus 4.8 在记录的压力测试中承认了 3 个论点：类似 hash 的不可预测性、衍生检测的充分性，以及检测与约束之间的对等关系。
- 论文认为主要结论是一个架构边界：检测处理可恢复的失败，第 4 层约束处理毁灭性风险动作。

## Problem

## Approach

## Results

## Link
- [https://github.com/joseteiadirector/teia-igo-vs-claude-opus-4.8/blob/main/README.en.md](https://github.com/joseteiadirector/teia-igo-vs-claude-opus-4.8/blob/main/README.en.md)
