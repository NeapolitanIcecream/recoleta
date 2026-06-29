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
WebGameBench 通过检查交付的浏览器游戏是否能在真实浏览器中运行来评估编码代理，而不是只看代码是否能构建。论文显示，可玩交付和完全满足需求之间存在明显差距。

## 问题
- 编码代理基准常常给函数、仓库补丁、终端轨迹或构建结果打分，但用户拿到的是一个应用，它可能能加载，却仍然不符合运行时要求。
- 浏览器原生游戏在小体量应用里暴露出很多失败模式：输入处理、空间映射、规则执行、状态变化、得分、胜负条件、重启流程和可见反馈。
- 这对自动化软件生产很重要，因为代理即使交付了一个能加载的页面，仍然可能没有满足需求里描述的行为。

## 方法
- 这个基准包含 111 个冻结的 Structured WebGame Specification 任务，覆盖 7 个游戏家族。
- 每个代理只有一次标准化生成尝试，生成一个可构建的浏览器原生源码工件，并把它暴露为本地浏览器 URL。
- 一个基于 Codex 的运行时评估器通过 Playwright 控制 Chrome，和游戏交互，并将其标注为 Excellent、Usable 或 Unusable。
- 评估器根据编码代理使用的同一份规范来判断可观察的浏览器行为。
- 任务还包含功能点元数据，以及基于规范结构和规则深度的 D1-D4 难度标签。

## 结果
- 在 111 个任务、12 个编码代理和 14 种评估配置上，最佳配置 opus-4-7 达到 76.9% 的 usable rate 和 20.2% 的 excellent rate，覆盖率为 93.7%。
- opus-4-6 达到 73.0% 的 usable 和 19.0% 的 excellent；gpt-5-5 达到 63.6% 的 usable 和 16.4% 的 excellent；gemini-3.1-pro 达到 63.6% 的 usable 和 15.9% 的 excellent。
- 得分较低的配置 usable rate 介于 38.3% 到 52.8% 之间，其中 kimi-k2.5 的 usable 为 38.3%，excellent 为 8.4%。
- 难度分层显示，合并后的 usable rate 在 D1 为 73.7%，D2 为 76.1%，D3 为 52.1%，D4 为 12.6%。
- 在一个 43 个工件的人类复核集上，二元 usable-rate 一致性会随着评估器推理投入增加而提高：Medium 的准确率为 66.7%，macro-F1 为 65.9%；High 为 82.1% 和 80.8%；XHigh 为 85.0% 和 82.9%。
- XHigh 下的三分类精确一致率更低，为 50.0% 准确率和 50.5% macro-F1，主要因为 Excellent 和 Usable 标注之间存在分歧。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17637v1](https://arxiv.org/abs/2605.17637v1)
