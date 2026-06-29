---
source: arxiv
url: https://arxiv.org/abs/2606.07383v1
published_at: '2026-06-05T15:21:41'
authors:
- Huixi Intelligence
- ':'
- Chen Zhang
- Chenyang Zhou
- Guanglei Ding
- Guanghui He
- Haibin Gao
- Jiajia Chen
- Jianyong Zhang
- Lianyi Yu
- Ningyi Xu
- Ping Xu
- Qingchen Li
- Yingjun Hu
- Yijia Zhang
- Yuxi Liu
topics:
- vision-language-action
- robot-foundation-model
- edge-deployment
- robot-data-scaling
- cross-embodiment
- real-time-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# RhinoVLA Technical Report

## Summary
## 摘要
RhinoVLA 是面向部署的视觉-语言-动作模型，用于在边缘硬件上进行实时机器人操作。它用 Qwen3-VL 降低视觉 token 成本，并用共享的 72D 状态-动作接口对齐混合机器人数据集。

## 问题
- VLA 策略很难在机器人板载硬件上闭环运行，因为 VLM 上下文处理和动作生成带来过高延迟。
- 论文将 VLM 视觉 token 和上下文 token 识别为主要成本来源：在模型维度固定时，以 GEMM 为主的 MLP 投影计算量随 token 数量线性增长。
- 跨机器人训练也很难，因为数据集使用不同的相机布局、动作向量含义、控制单位和机器人特定动力学。

## 方法
- RhinoVLA 使用 2.13B 参数的 Qwen3-VL 主干，因为它用 64 个合并视觉 token 表示一张 224×224 图像，而 π0.5 使用的 PaliGemma-224 需要 256 个图像 token。
- 0.40B 参数的连续 Action Expert 用 flow matching 生成动作块，并以 Qwen3-VL KV cache、机器人状态、掩码、带噪动作块、flow time 和机器人实例 ID 为条件。
- View Registry 为每张图像标注相机角色和模态，例如 head/rgb 或 left_wrist/rgb，使相机身份在不同数据集中显式可见。
- 统一的 72D 物理状态-动作槽位空间为动作维度赋予固定含义，同时用二值掩码从监督中排除缺失或无效的机器人维度。
- 机器人实例 LoRA 模块在 Action Expert 内加入低成本的机器人特定修正，同时保持 72D 输出接口和部署图共享。

## 结果
- RhinoVLA 在 Huixi R1 边缘 SoC 上达到 11.69 Hz 端到端推理速度，高于论文给出的 10 Hz 闭环控制目标。
- 论文称其下游任务性能在相近参数规模下可与 π0.5 相当，但摘录没有给出任务级准确率数字或特定数据集分数。
- 在 Jetson AGX Orin 上，论文报告 π0.5 的端到端延迟约为 858.3 ms：视觉编码器 69.3 ms，VLM 主干 528.0 ms，Action Expert 257.0 ms。
- 在该 π0.5 延迟拆分中，VLM 主干和 Action Expert 合计占运行时间的 90% 以上。
- 算子分析报告称，VLM MLP 投影 gate_proj、up_proj 和 down_proj 约占 VLM 延迟的 74.7%，注意力投影约占 7.2%。
- 在引用的 224×224 设置下，Qwen3-VL 的视觉 token 设计将每张图像的视觉 token 数量相比 PaliGemma-224 减少 4×，这是论文声称的 VLM 侧提速主要来源。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.07383v1](https://arxiv.org/abs/2606.07383v1)
