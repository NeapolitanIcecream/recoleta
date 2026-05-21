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
OA-WAM 通过把每个对象槽拆成固定身份地址和会变化的内容状态，让世界-动作机器人策略能直接寻址对象。论文报告称，在与目标绑定相关的 LIBERO、SimplerEnv 和 LIBERO-Plus 场景变化测试中，它的操作成功率达到最高或接近最高。

## 问题
- 现有 World Action Models 将未来场景预测为图像、token 流或全局潜变量，因此目标身份可能与背景、姿态和干扰物混在一起。
- 这一点会影响性能，因为机器人策略可能在标准基准上得分很高，但在相机视角、布局、机器人初始姿态、光照、语言或传感器噪声变化时失败。
- 论文关注会点名对象的指令，例如选择红色马克杯，而不是旁边的干扰物。

## 方法
- 每一帧被转换为 N+1 个槽：一个机器人槽和最多 16 个对象槽。
- 每个对象槽包含一个 32 维固定地址，由语言标签和初始 DINOv3 特征生成；还包含一个 256 维内容向量，该向量每帧由 SAM 3 和 DINOv3 更新；另有时间和角色嵌入。
- 一个 Chameleon 风格的 7B transformer 以 block-causal 序列处理文本、图像 VQ token、本体感觉、过去动作、槽和动作查询。
- 跨槽注意力的 key 只读取固定地址切片，并且每个 transformer 层都会把该地址切片重置为缓存值。这样，槽路由会绑定到对象身份，同时内容和姿态可以变化。
- 一个 world head 预测下一帧的逐槽内容和姿态，一个 flow-matching action head 在一次前向传播中输出 16 步连续动作块。

## 结果
- 在 LIBERO 上，OA-WAM 报告平均成功率为 97.8%，高于 π0.5 的 96.9%、VLA-JEPA 的 97.2% 和 MemoryVLA 的 96.5%。
- 在 SimplerEnv WidowX Visual Matching 上，OA-WAM 报告平均成功率为 79.3%，高于 CoWVLA 的 76.0%、MemoryVLA 的 71.9% 和 InternVLA-M1 的 71.7%。
- 在 LIBERO-Plus 上，OA-WAM 报告平均成功率为 83.9%，π0.5 为 85.7%；它的总体分数较低，主要来自 Sensor Noise，在该项上它得到 75.6%，Cosmos-Policy 为 92.7%。
- 在 LIBERO-Plus 几何轴上，OA-WAM 报告 Camera 80.5%、Robot init 89.6%、Layout 82.8%、Geo Avg 84.3%，比 π0.5 的 Geo Avg 79.5% 高 4.8 个百分点。
- 一项因果槽干预测试报告称，OA-WAM 的 swap-binding cosine 为 0.87，八个整体式基线为 0.09 或更低。
- 消融实验称，移除 addr-only key projection 会让 LIBERO-Plus Camera 下降 13.3 个百分点，同时让分布内 LIBERO 变化 1.5 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06481v1](https://arxiv.org/abs/2605.06481v1)
