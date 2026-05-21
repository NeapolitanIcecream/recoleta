---
source: arxiv
url: https://arxiv.org/abs/2605.05980v1
published_at: '2026-05-07T10:24:27'
authors:
- Yuan Sui
- Yulin Chen
- Yibo Li
- Xue Jiang
- Yufei He
- Yihong Dong
- Xiaoxin He
- Tianyu Gao
- Bryan Hooi
topics:
- coding-agents
- activation-steering
- agent-drift
- code-intelligence
- software-engineering-benchmarks
- automated-debugging
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# TACT: Mitigating Overthinking and Overacting in Coding Agents via Activation Steering

## Summary
## 概要
TACT 将编码代理从两类步骤级失败模式中拉回：反复围绕已知事实推理，以及在未使用近期证据的情况下反复调用工具。论文称，它无需微调或修改提示词，就能在软件工程基准上提高解决率。

## 问题
- 长时间运行的编码代理可能在几十步或几百步后发生漂移，导致无效推理、重复搜索、冗余读取文件和漏掉修复机会。
- 最终任务是否成功，无法说明一条失败轨迹是因过度思考还是过度行动而崩坏，因此步骤级诊断对可靠的编码代理很重要。
- 这些失败会降低解决率，并增加步骤数、上下文使用量和工具调用次数。

## 方法
- 论文使用 LLM 裁判将每个代理步骤标注为过度思考、过度行动或已校准；裁判依据滚动验证状态，其中包含已知事实、假设、编辑、测试结果和重复动作。
- 它在 `</think>` token 处提取隐藏状态，也就是推理结束、行动开始的位置。
- 它构建两条均值差激活方向：过度思考相对于已校准，以及过度行动相对于已校准。
- 它先将过度行动方向相对于过度思考方向正交化，然后在测试时沿两条轴对残差流进行 steering。
- steering 变体包括限制带外投影、应用固定加性偏移，或在激活离开已校准区间时应用带门控的部分校正。

## 结果
- 过度思考、过度行动和已校准步骤的隐藏状态沿漂移轴可线性分离，AUC 约为 0.9。
- 在 SWE-bench Verified、Terminal-Bench 2.0 和 CLAW-Eval 上，TACT 将 Qwen3.5-27B 的平均解决率提高了 +5.8 个百分点。
- 在 Gemma-4-26B-A4B-it 上，TACT 在同一组基准上的平均解决率提高了 +4.8 个百分点。
- TACT 最多可将解决所需步骤数减少 26 步。
- LLM 裁判相对于人类共识的召回率为：过度思考 84%、过度行动 82%、已校准 87%；相对于四个参考标注的 Cohen's kappa 为 0.73 到 0.81。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05980v1](https://arxiv.org/abs/2605.05980v1)
