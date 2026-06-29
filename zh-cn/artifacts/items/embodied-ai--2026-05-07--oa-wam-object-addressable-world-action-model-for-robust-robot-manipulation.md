---
source: arxiv
url: https://arxiv.org/abs/2605.06481v1
published_at: '2026-05-07T16:06:08'
authors:
- Yushan Liu
- Peibo Sun
- Shoujie Li
- Yifan Xie
- Lingfeng Zhang
- Xintao Chao
- Shiyuan Dong
- Fang Chen
- Xiao-Ping Zhang
- Wenbo Ding
topics:
- vision-language-action
- world-action-model
- object-centric-slots
- robot-manipulation
- libero-plus
- flow-matching-actions
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# OA-WAM: Object-Addressable World Action Model for Robust Robot Manipulation

## Summary
## 摘要
OA-WAM 通过把每个对象槽拆成固定的身份地址和变化的内容状态，让世界-动作机器人策略可以直接定位对象。它在 LIBERO、SimplerEnv 和与目标绑定相关的 LIBERO-Plus 场景变化测试上报告了最高或接近最高的操作成功率。

## 问题
- 现有 World Action Model 会把未来场景预测成图像、token 流或全局 latent，因此目标身份容易和背景、姿态、干扰物混在一起。
- 这很重要，因为机器人策略在标准基准上可能得分很高，但在相机视角、布局、机器人初始位姿、光照、语言或传感器噪声变化时会失效。
- 论文关注的是点名对象的指令，比如选红色杯子，而不是旁边的干扰物。

## 方法
- 每一帧被转换成 N+1 个槽：1 个机器人槽和最多 16 个对象槽。
- 每个对象槽都有一个 32 维固定地址，来自语言标签和初始 DINOv3 特征；还有一个 256 维内容向量，每一帧由 SAM 3 和 DINOv3 更新；另外还加上时间和角色嵌入。
- 一个 Chameleon 风格的 7B transformer 以 block-causal 序列处理文本、图像 VQ tokens、本体感觉、过去动作、各个槽和动作查询。
- 跨槽注意力的 key 只读取固定地址切片，每个 transformer 层都会把这个地址切片重置为缓存值。这样，槽的路由会继续绑定到对象身份，而内容和姿态可以变化。
- 一个 world head 预测下一帧的每槽内容和姿态，一个 flow-matching action head 一次输出 16 步连续动作块。

## 结果
- 在 LIBERO 上，OA-WAM 报告的平均成功率是 97.8%，高于 π0.5 的 96.9%、VLA-JEPA 的 97.2% 和 MemoryVLA 的 96.5%。
- 在 SimplerEnv WidowX Visual Matching 上，它报告的平均成功率是 79.3%，高于 CoWVLA 的 76.0%、MemoryVLA 的 71.9% 和 InternVLA-M1 的 71.7%。
- 在 LIBERO-Plus 上，它报告的平均成功率是 83.9%，而 π0.5 为 85.7%；它整体分数较低主要来自 Sensor Noise，那里它是 75.6%，Cosmos-Policy 为 92.7%。
- 在 LIBERO-Plus 的几何轴上，它报告的结果是 Camera 80.5%、Robot init 89.6%、Layout 82.8% 和 Geo Avg 84.3%，比 π0.5 的 Geo Avg 79.5% 高 4.8 分。
- 因果槽干预测试报告 OA-WAM 的 swap-binding cosine 为 0.87，而八个 holistic 基线为 0.09 或更低。
- 一项消融结果说，去掉 addr-only key projection 会让 LIBERO-Plus Camera 下降 13.3 分，而 in-distribution LIBERO 只变化 1.5 分。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06481v1](https://arxiv.org/abs/2605.06481v1)
