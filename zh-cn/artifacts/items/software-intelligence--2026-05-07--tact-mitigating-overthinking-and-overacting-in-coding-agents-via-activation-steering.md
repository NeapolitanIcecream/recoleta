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
## 总结
TACT 让编码代理避开两类步骤级失败模式：对已知事实反复推理，以及在没有利用最新证据的情况下反复调用工具。论文声称，在不微调模型、也不改提示词的情况下，它能在软件工程基准上提高解决率。

## 问题
- 长时间运行的编码代理可能在几十步甚至上百步里发生漂移，导致推理重复、反复搜索、重复读文件，以及漏掉修复点。
- 只看最终是否完成任务，无法判断失败轨迹是因为过度思考还是过度行动，所以步骤级诊断对可靠的编码代理很重要。
- 这些失败会拉低解决率，并增加步骤数、上下文占用和工具调用次数。

## 方法
- 论文用一个 LLM 评审器给每个代理步骤标注为过度思考、过度行动或已校准，并维护一个滚动的已验证状态，里面包含已知事实、假设、修改、测试结果和重复动作。
- 它在 `</think>` 这个 token 处提取隐藏状态，也就是推理结束、行动开始的位置。
- 它构建了两个均值差分激活方向：过度思考相对于已校准，以及过度行动相对于已校准。
- 它先让过度行动方向与过度思考方向正交，再在测试时沿这两个轴对残差流进行引导。
- 这些引导变体要么限制带外投影，要么施加固定的加性偏移，要么在激活偏离已校准区间时施加门控的部分修正。

## 结果
- 过度思考、过度行动和已校准步骤的隐藏状态，沿漂移轴可以线性分离，AUC 约为 0.9。
- 在 SWE-bench Verified、Terminal-Bench 2.0 和 CLAW-Eval 上，TACT 让 Qwen3.5-27B 的平均解决率提高了 +5.8 个百分点。
- 在 Gemma-4-26B-A4B-it 上，TACT 在同一组基准上的平均解决率提高了 +4.8 个百分点。
- TACT 最多把解决所需步骤数减少 26 步。
- 这个 LLM 评审器相对人工共识，对过度思考的召回率为 84%，对过度行动为 82%，对已校准为 87%；与四个参考标注相比，Cohen's kappa 为 0.73 到 0.81。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05980v1](https://arxiv.org/abs/2605.05980v1)
