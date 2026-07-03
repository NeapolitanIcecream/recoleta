---
source: arxiv
url: https://arxiv.org/abs/2607.01904v1
published_at: '2026-07-02T09:03:32'
authors:
- Hao He
- Shyam Agarwal
- Yegor Denisov-Blanch
- Pavel Azaletskiy
- Sanmi Koyejo
- Bogdan Vasilescu
topics:
- ai-coding-tools
- software-engineering-productivity
- code-review
- human-ai-interaction
- enterprise-ai-adoption
- difference-in-differences
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# AI Writes Faster Than Humans Can Review: A Longitudinal Study of an Enterprise 2x Mandate

## Summary
## 摘要
本文用 802 名开发者和 196,212 个拉取请求的内部遥测数据研究一家企业的 AI 编码强制要求。研究发现，到 2026 年 4 月，PR 吞吐量翻了一倍，大部分增幅与 AI 采用和工具累计使用有关。

## 问题
- 公司正在强制使用 AI 编码工具，并声称生产率大幅提高，但此前可信的实地结果从 19% 的放缓到 PR 数量增加约 40% 不等。
- 本文考察一家真实公司能否达到工程产出 2 倍目标，以及评审负载和短期质量信号会发生什么变化。

## 方法
- 作者研究了一家中型 B2B 软件公司。该公司 CTO 在 2025 年 6 月设定目标：通过使用 AI，将每名工程师每月合并的 PR 数量翻倍。
- 他们将 PR 和评审历史与 Cursor、Claude Code 使用日志结合，构建了一个覆盖 2024 年 1 月至 2026 年 4 月的开发者-月份面板，包含 802 名开发者以及 364 个代码库中的 196,212 个非机器人 PR。
- 他们用错位双重差分估计开发者内部变化，并按每名开发者首次使用 AI 工具的时间对齐，而不是按公司强制要求的日期对齐。
- 他们区分采用带来的跳升和与此前累计 AI 编写代码行数相关的增长，并检验模型发布日期是否解释了这些增幅。
- 他们将采用强度视为观察性变量，因此估计结果支持采用与使用这一渠道，但不能证明精确的因果效应大小。

## 结果
- 到 2026 年 4 月，人均 PR 吞吐量达到强制要求前基线的 2.09 倍。
- 在开发者内部的分解中，采用加累计使用与给定开发者约 1.5 倍的增幅相关，并且使用工具 9 个月后轨迹达到 2 倍。
- 估计面板包含 564 名开发者；451 人采用了 AI 工具，113 人从未采用。
- 到研究窗口结束时，AI 编写的 PR 从接近零上升到约占 PR 的 90%；全部 196,212 个非机器人 PR 中有 30.2% 带有 created-by-ai 标签。
- 每名评审者的负载大约翻倍，自动化评审超过人工评审，合并率和回滚率大致持平。
- 各资历层级的增幅在统计上相近，增幅集中在较新的代码库中，并且无法在 Sonnet 4.5、Opus 4.5 和 Opus 4.6 这几代模型之间区分开。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01904v1](https://arxiv.org/abs/2607.01904v1)
