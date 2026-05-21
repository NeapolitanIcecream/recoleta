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
本文测试 VLA 自动驾驶模型给出的因果链解释是否与场景和生成轨迹一致。结果显示，这些解释常常不能作为安全证据。

## 问题
- VLA 驾驶模型可以输出自然语言推理和规划轨迹，但文本可能与场景中的物体或实际采取的动作不一致。
- 这会带来风险，因为当模型漏检行人或继续行驶时，“为前方行人停车”这类轨迹说明可能误导用户或安全监控系统。
- 论文聚焦 Alpamayo-R1-10B，检验其推理是否足够忠实，可用于驾驶安全检查。

## 方法
- 研究评估了 300 次 Alpamayo-R1-10B 推理：100 个 PhysicalAI-AV 测试片段，每个片段使用 3 个随机种子。
- 研究通过比较因果链文本中提到的物体与预测时间附近自动标注的 3D 障碍物，定义实体忠实度。
- 研究通过检查陈述动作是否匹配轨迹谓词，定义动作忠实度，例如“停车”对应最终速度低于 0.5 m/s，“减速”对应减速度超过 1.0 m/s²，转向对应横向位移超过 1.0 m。
- 研究使用前置摄像头高斯模糊 σ=3 加 10% 矩形遮挡来测试反事实忠实度，然后检查推理和轨迹是否一起变化。
- 研究通过采样 2 条扩散轨迹并测量空间扩散范围来估计轨迹不确定性。

## 结果
- 在 282 次带障碍物上下文的推理中，整体推理忠实度为 42.5%；实体忠实度为 35.3%，动作忠实度为 49.6%。
- 模型的幻觉率为 8.9%，包含 25 个幻觉实体实例；在 33.3% 的行人相关场景中漏检了 94 名行人。
- 300 次推理的基线轨迹质量为：平均 minADE 1.992 ± 1.752 m，中位数 minADE 1.481 m，第 90 百分位 4.018 m，第 95 百分位 5.884 m，且有 21/300 次安全失败的误差超过 5 m。
- 推理-动作一致性平均值为 0.483；53.3% 的推理一致性较低，37.9% 声称停车的案例实际继续行驶。
- 在视觉扰动下，97.7% 的轨迹发生变化；38/265 个案例，即 14.3%，属于静默失败：轨迹变化但推理保持不变。
- 高忠实度推理的平均 ADE 为 1.694 m，低忠实度推理为 2.278 m；低忠实度组的误差高出 34.5%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17268v1](https://arxiv.org/abs/2605.17268v1)
