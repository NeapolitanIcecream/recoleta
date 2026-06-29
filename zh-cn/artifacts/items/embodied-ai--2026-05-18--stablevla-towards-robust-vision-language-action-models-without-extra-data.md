---
source: arxiv
url: https://arxiv.org/abs/2605.18287v1
published_at: '2026-05-18T12:15:16'
authors:
- Yiyang Fu
- Chubin Zhang
- Shukai Gong
- Yufan Deng
- Kaiwei Sun
- Qiyang Min
- Qibin Hou
- Yansong Tang
- Jianan Wang
- Daquan Zhou
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-robustness
- sim2real
- adapter-tuning
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# StableVLA: Towards Robust Vision-Language-Action Models without Extra Data

## Summary
## 摘要
StableVLA 通过用信息瓶颈适配器替换常规视觉投影层，提高了 VLA 策略对未见视觉损坏的容忍度。它在不增加机器人数据或针对损坏的增强策略的情况下，报告了明显提升。

## 问题
- 当摄像头输入包含训练中未出现的模糊、噪声、天气效应或数字伪影时，VLA 模型会失效。
- 论文报告，VLA-Adapter 在干净数据上的成功率为 96%，但在损坏条件下会降到更低，在一些严重模糊案例中甚至为 0%。
- 这很重要，因为真实机器人经常面对不完美图像，而为每一种扰动都采集数据并不现实。

## 方法
- StableVLA 保持 VLA-Adapter 设定不变，把视觉编码器和 LLM 策略之间的 MLP 投影层替换为 Fused IB-Adapter。
- IB-Adapter 先对视觉特征计算按通道协方差，再用 sigmoid 门控抑制看起来像独立噪声的通道。
- 一个并行的 MLP 路径保留精细操作所需的空间细节，IB 路径补充去噪后的语义特征。
- 模型使用与 VLA-Adapter 相同的训练设置，没有额外机器人数据，也没有针对损坏的训练增强。

## 结果
- 摘要声称，在增加少于 10M 参数的情况下，平均比基线提升 30%。
- 将原始适配器替换为 IB-Adapter 后，在模拟中的合成视觉损坏上平均提升 35.2%。
- 在 LIBERO 的 severity-5 损坏下，StableVLA 在四个任务套件上的提升幅度相对 VLA-Adapter 为 40.2% 到 139.6%。
- 表 1 报告了 LIBERO severity-5 相对 VLA-Adapter 的成功率提升：Spatial 82.0% 对 58.5%，Object 70.2% 对 29.3%，Goal 71.9% 对 47.3%，Long 45.3% 对 26.2%。
- 在 CALVIN 上，StableVLA 在所有报告设置中完成的任务都多于 VLA-Adapter：干净 4.17 对 4.14，severity 3 为 2.77 对 2.56，severity 4 为 2.11 对 1.89，severity 5 为 1.51 对 1.44。
- 在带视觉损坏的真实 Pack Doll 任务中，StableVLA-0.5B 的成功率为 50%，VLA-Adapter-0.5B 为 20%，OpenPi-0.5-3B 为 40%；论文还报告了真实机器人抓取放置任务提升 31.7 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18287v1](https://arxiv.org/abs/2605.18287v1)
