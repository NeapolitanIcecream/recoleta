---
source: arxiv
url: https://arxiv.org/abs/2605.17268v1
published_at: '2026-05-17T05:29:48'
authors:
- Nicanor Mayumu
- Xiaoheng Deng
- Patrick Mukala
topics:
- vision-language-action
- autonomous-driving
- reasoning-faithfulness
- safety-evaluation
- counterfactual-testing
- trajectory-prediction
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation

## Summary
## 摘要
本文测试 VLA 自动驾驶模型给出的 Chain-of-Causation 解释是否与场景和生成的轨迹一致。结果显示，这些解释常常不能作为安全证据。

## 问题
- VLA 自动驾驶模型可以输出自然语言推理和规划轨迹，但文本可能与场景中的对象或实际动作不一致。
- 这很重要，因为像“在前方行人处停车”这样的轨迹说明，在模型漏检行人或仍继续移动时，会误导用户或安全监控。
- 论文聚焦 Alpamayo-R1-10B，检验它的推理是否足以用于驾驶安全检查。

## 方法
- 研究评估了 300 次 Alpamayo-R1-10B 推理：每个测试片段使用 3 个随机种子，共 100 个 PhysicalAI-AV 测试片段。
- 它通过比较 Chain-of-Causation 文本中提到的对象与预测时刻附近自动标注的 3D 障碍物，来定义实体一致性。
- 它通过检查陈述动作是否与轨迹谓词匹配来定义动作一致性，例如“停车”要求最终速度低于 0.5 m/s，“减速”要求减速度超过 1.0 m/s²，“转向”要求横向位移超过 1.0 m。
- 它用前置摄像头高斯模糊（σ=3）加 10% 矩形遮挡来测试反事实忠实性，然后检查推理和轨迹是否一起变化。
- 它通过采样 2 条扩散轨迹并测量空间离散程度来估计轨迹不确定性。

## 结果
- 在 282 次包含障碍物上下文的推理中，总体推理忠实度为 42.5%；实体忠实度为 35.3%，动作忠实度为 49.6%。
- 模型的幻觉率为 8.9%，出现了 25 个幻觉实体实例；在与行人相关的场景中，有 33.3% 漏检了 94 个行人。
- 300 次推理的基线轨迹质量中，平均 minADE 为 1.992 ± 1.752 m，中位数 minADE 为 1.481 m，90 分位数为 4.018 m，95 分位数为 5.884 m，且有 21/300 次安全失败，误差超过 5 m。
- 推理与动作一致性平均为 0.483；53.3% 的推理一致性较低，37.9% 的声称停车案例实际上仍继续前进。
- 在视觉扰动下，97.7% 的轨迹发生变化；38/265 个案例，即 14.3%，是无声失败，即轨迹变了，但推理不变。
- 高忠实度推理的平均 ADE 为 1.694 m，低忠实度推理为 2.278 m；低忠实度组的误差高出 34.5%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17268v1](https://arxiv.org/abs/2605.17268v1)
