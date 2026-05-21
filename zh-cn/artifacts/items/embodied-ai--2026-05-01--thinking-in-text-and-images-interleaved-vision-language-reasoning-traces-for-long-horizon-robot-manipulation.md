---
source: arxiv
url: https://arxiv.org/abs/2605.00438v1
published_at: '2026-05-01T06:15:43'
authors:
- Jinkun Liu
- Haohan Chi
- Lingfeng Zhang
- Yifan Xie
- YuAn Wang
- Long Chen
- Hangjun Ye
- Xiaoshuai Hao
- Wenbo Ding
topics:
- vision-language-action
- long-horizon-manipulation
- robot-foundation-model
- multimodal-reasoning
- visual-planning
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Thinking in Text and Images: Interleaved Vision--Language Reasoning Traces for Long-Horizon Robot Manipulation

## Summary
## 摘要
IVLR 给机器人策略加入了显式的全任务轨迹：每个阶段包含一个文本子目标和一个 RGB 关键帧。模型先生成一次该轨迹并缓存，然后结合实时相机观测来选择动作。

## 问题
- 长时程操作需要正确的步骤顺序和空间目标；许多 VLA 策略把这类计划隐藏在模型激活中。
- 纯文本计划可以编码顺序，但会缺少姿态和接触细节；视觉预测可以显示几何信息，但可能漏掉预期的任务序列。
- 在多阶段任务中，这会影响结果：机器人可能因处理物体顺序错误或放置位置错误而失败。

## 方法
- IVLR 使用 Show-o2 1.5B 多模态 Transformer，根据初始图像和指令生成 IVLR-Trace。
- 每个轨迹阶段把一条说明文字和一个 RGB 关键帧配对：说明文字给出子目标，关键帧显示预期的视觉状态。
- 执行期间，缓存的轨迹、原始指令和当前观测输入到一个 ACT token 和一个 MLP 动作解码器，用于在闭环中预测连续动作。
- 由于机器人数据集缺少这类轨迹，作者用 Universal Visual Decomposer 对演示进行分段，将分段终点作为关键帧，并用 Qwen3-VL 为各阶段生成说明文字，从而构造伪轨迹。
- 训练结合了文本的 next-token loss、视觉关键帧的 flow-matching loss 和动作的 L1 loss，并在训练中加入轨迹噪声和遮蔽。

## 结果
- 在 LIBERO 上，IVLR 报告的平均成功率为 95.5%，其中 LIBERO-Long 为 92.4%。对比基线包括 VLA-0，平均成功率 94.7%、Long 为 87.6%；CoT-VLA，平均成功率 81.1%、Long 为 69.0%；π0-FAST，平均成功率 85.5%、Long 为 60.2%。
- LIBERO 的轨迹消融显示，长时程任务受影响最大：无轨迹在 Long 上达到 37.7%，纯文本达到 62.0%，纯视觉达到 68.4%，完整 IVLR 达到 92.4%。
- 在 SimplerEnv-WidowX 上，IVLR 报告的总体成功率为 59.4%，SpatialVLA 为 42.7%，RoboVLMs 为 37.5%，Octo-Small 为 29.5%。
- LIBERO 压力测试显示，基础设置下平均成功率为 95.5%，加入 2 cm 执行扰动后为 92.1%，遮蔽 30% 文本轨迹时为 92.2%，遮蔽 30% 视觉关键帧时为 90.0%。
- 该方法有前置成本：在一块 NVIDIA H20 GPU 上生成完整轨迹约需 10 秒，之后缓存执行以 10 Hz 运行，并使用动作分块。
- 论文只报告了仿真结果；作者列出的当前限制包括静态且完全可观测的环境、过期或错误的全局计划，以及初始规划延迟。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00438v1](https://arxiv.org/abs/2605.00438v1)
