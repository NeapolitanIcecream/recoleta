---
source: arxiv
url: https://arxiv.org/abs/2605.13778v1
published_at: '2026-05-13T16:57:51'
authors:
- Jiahui Niu
- Kefan Gu
- Yucheng Zhao
- Shengwen Liang
- Tiancai Wang
- Xing Hu
- Ying Wang
- Huawei Li
topics:
- vision-language-action
- diffusion-policy
- speculative-inference
- robot-replanning
- latency-optimization
- dexterous-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Realtime-VLA FLASH: Speculative Inference Framework for Diffusion-based VLAs

## Summary
## 概要
Realtime-VLA FLASH 通过用低成本的草稿动作块替代许多完整重规划调用，加速基于扩散的视觉-语言-动作策略；主 Action Expert 会并行检查这些草稿动作块。在 LIBERO 上，它将平均推理延迟从 58.0 ms 降至 19.1 ms，成功率只小幅下降。

## 问题
- 基于扩散的 VLA，例如 $\pi_0$，在机器人重规划期间需要反复执行多步动作去噪，导致每轮完整推理都很慢。
- 在抓取移动传送带上物体等高速任务中，重规划慢会让机器人继续执行过时的动作块。
- 现有推测解码方法适用于离散自回归 token，但 dVLA 输出连续动作块，并且没有可用于接受检查的 token 概率。

## 方法
- FLASH 增加两条推理路径：常规完整路径，以及在许多重规划轮次中使用的更快 flash 路径。
- 一个小型草稿模型根据当前视觉特征、语言和机器人状态并行预测完整的未来动作块；它约有 110M 参数，而 VLM 约有 2.7B 参数。
- 主模型的 Action Expert 在不执行完整顺序去噪的情况下验证草稿：它采样少量 flow-matching 时间步，并行重建动作端点，并检查它们是否与草稿保持接近。
- 机器人执行草稿动作块中通过验证的最长前缀。如果没有任何前缀通过距离阈值，FLASH 会回退到完整路径。
- 阶段感知回退会检查夹爪切换，并在接近抓取或释放阶段时返回完整推理，因为这些阶段的小动作误差可能导致失败。

## 结果
- 在 LIBERO 上，Torch-$\pi_0$ 的平均成功率为 94.1%，任务级延迟为 58.0 ms，单动作延迟为 5.0 ms。FLASH+Triton-$\pi_0$ 的平均成功率为 93.8%，延迟为 19.1 ms，单动作延迟为 1.9 ms。
- FLASH+Triton-$\pi_0$ 相比 Torch-$\pi_0$ 报告了 3.04x 的任务级加速，平均成功率下降 0.3 个百分点。
- 经过 Triton 优化后，一轮 flash 路径耗时 7.8 ms；原始完整推理轮次耗时 58.0 ms。
- 不使用 Triton 的 FLASH 将 LIBERO 平均延迟降至 34.9 ms，在平均成功率为 93.4% 的情况下实现 1.66x 加速。
- FLASH+Triton 通过 flash 路径处理 LIBERO 中 66.8% 的重规划轮次，接受的前缀平均覆盖 12 动作重规划窗口的 69.7%。
- 在真实传送带分拣中，论文报告其在传送带速度最高 15 m/min 时成功抓取，而对比方法失败。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13778v1](https://arxiv.org/abs/2605.13778v1)
