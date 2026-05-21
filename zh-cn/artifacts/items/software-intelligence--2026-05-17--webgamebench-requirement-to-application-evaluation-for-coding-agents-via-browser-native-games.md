---
source: arxiv
url: https://arxiv.org/abs/2605.17637v1
published_at: '2026-05-17T20:07:12'
authors:
- Wenyu Zhang
- Guoliang You
- Tianlun
- Haotian Zhao
- Tianshu Zhu
- Haoran Wang
- Xiaoxuan Tang
- Mingyang Dai
- Jingnan Gu
- Daxiang Dong
- Jianmin Wu
topics:
- coding-agents
- software-benchmark
- browser-games
- runtime-evaluation
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games

## Summary
## 摘要
WebGameBench 通过检查交付的浏览器游戏是否能在真实浏览器中运行来评估编码智能体，而不只看代码能否构建。论文显示，可玩交付与完整满足需求之间存在很大差距。

## 问题
- 编码智能体基准常给函数、仓库补丁、终端轨迹或构建结果打分，但用户拿到的是应用；应用可能能加载，却仍不满足运行时需求。
- 浏览器原生游戏能在小型应用中暴露许多失效模式：输入处理、空间映射、规则、状态变化、计分、胜负条件、重启流程和可见反馈。
- 这对自动化软件生产很重要，因为智能体交付了可加载页面，仍可能漏掉需求中描述的行为。

## 方法
- 该基准包含 111 个冻结的 Structured WebGame Specification 任务，覆盖 7 类玩法。
- 每个智能体获得一次标准化生成机会，构建一个浏览器原生源代码产物，并将其暴露为本地浏览器 URL。
- 一个基于 Codex 的运行时评估器通过 Playwright 控制 Chrome，与游戏交互，并将其标记为 Excellent、Usable 或 Unusable。
- 评估器根据编码智能体使用的同一份规格，判断可观察到的浏览器行为。
- 任务还包含功能点元数据，以及基于规格结构和规则深度的 D1-D4 难度标签。

## 结果
- 在 111 个任务、12 个编码智能体和 14 个评估配置中，最佳配置 opus-4-7 达到 76.9% Usable 率、20.2% Excellent 率，覆盖率为 93.7%。
- opus-4-6 达到 73.0% Usable 和 19.0% Excellent；gpt-5-5 达到 63.6% Usable 和 16.4% Excellent；gemini-3.1-pro 达到 63.6% Usable 和 15.9% Excellent。
- 得分较低的配置的 Usable 率介于 38.3% 到 52.8% 之间，其中 kimi-k2.5 为 38.3% Usable 和 8.4% Excellent。
- 按难度分层显示，汇总 Usable 率为：D1 73.7%、D2 76.1%、D3 52.1%、D4 12.6%。
- 在 43 个产物的人工评审集上，随着评估器推理强度提高，二元 Usable 率一致性提升：Medium 的准确率为 66.7%、macro-F1 为 65.9%；High 为 82.1% 和 80.8%；XHigh 为 85.0% 和 82.9%。
- XHigh 下精确三分类一致性较低，准确率为 50.0%、macro-F1 为 50.5%，主要原因是 Excellent 和 Usable 标签之间存在分歧。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17637v1](https://arxiv.org/abs/2605.17637v1)
