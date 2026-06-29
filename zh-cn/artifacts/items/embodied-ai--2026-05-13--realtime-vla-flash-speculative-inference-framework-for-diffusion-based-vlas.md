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
## 摘要
Realtime-VLA FLASH 通过用廉价的草拟动作块替换许多完整重规划调用，并让主 Action Expert 并行检查这些动作块，来加速基于扩散的视觉-语言-动作策略。在 LIBERO 上，它把平均推理延迟从 58.0 ms 降到 19.1 ms，成功率只小幅下降。

## 问题
- 像 $\pi_0$ 这样的基于扩散的 VLA 在机器人重规划时需要反复进行多步动作去噪，这让每一轮完整推理都很慢。
- 在快速任务里，重规划太慢会让机器人执行过时的动作块，比如在移动传送带上抓取物体。
- 现有的 speculative decoding 方法适用于离散自回归 token，但 dVLA 输出的是连续动作块，而且没有可用于接受检查的 token 概率。

## 方法
- FLASH 增加了两条推理路径：正常的完整路径，以及在许多重规划轮次中使用的更快 flash 路径。
- 一个小型草拟模型，参数约 1.1 亿，而较大的 VLM 约有 27 亿参数，从当前视觉特征、语言和机器人状态出发，并行预测完整的未来动作块。
- 主模型的 Action Expert 不需要完整的顺序去噪就能验证这个草稿：它采样几个 flow-matching 时间步，并行重建动作端点，再检查它们是否与草稿保持接近。
- 机器人执行已草拟动作块中最长、通过验证的前缀。如果没有前缀通过距离阈值，FLASH 就回退到完整路径。
- 一个感知阶段的回退机制会检查夹爪切换，并在接近抓取或释放阶段时回到完整推理，因为这时很小的动作误差都可能导致失败。

## 结果
- 在 LIBERO 上，Torch-$\pi_0$ 的平均成功率为 94.1%，任务级延迟为 58.0 ms，每动作延迟为 5.0 ms。FLASH+Triton-$\pi_0$ 的平均成功率为 93.8%，延迟为 19.1 ms，每动作延迟为 1.9 ms。
- FLASH+Triton-$\pi_0$ 相比 Torch-$\pi_0$ 的任务级速度提升为 3.04x，平均成功率下降 0.3 个百分点。
- 在 Triton 优化下，一轮 flash 路径耗时 7.8 ms，而原始完整推理轮次为 58.0 ms。
- 不使用 Triton 的 FLASH 将 LIBERO 平均延迟降到 34.9 ms，成功率平均为 93.4%，速度提升 1.66x。
- FLASH+Triton 通过 flash 路径处理了 LIBERO 上 66.8% 的重规划轮次，平均接受的前缀覆盖了 12 动作重规划窗口的 69.7%。
- 在真实传送带分拣任务中，论文报告在传送带速度最高 15 m/min 时仍能成功抓取，而对比方法会失败。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13778v1](https://arxiv.org/abs/2605.13778v1)
