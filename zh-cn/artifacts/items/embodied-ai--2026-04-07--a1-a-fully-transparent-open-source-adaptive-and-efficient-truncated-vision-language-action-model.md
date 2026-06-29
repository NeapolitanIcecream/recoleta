---
source: arxiv
url: http://arxiv.org/abs/2604.05672v3
published_at: '2026-04-07T10:18:40'
authors:
- Kaidong Zhang
- Jian Zhang
- Rongtao Xu
- Yu Sun
- Shuoshuo Xue
- Youpeng Wen
- Xiaoyu Guo
- Minghao Guo
- Weijia Liufu
- Liu Zihou
- Kangyi Ji
- Yangsong Zhang
- Jiarun Zhu
- Jingzhi Liu
- Zihang Li
- Ruiyi Chen
- Meng Cao
- Jingming Zhang
- Shen Zhao
- Xiaojun Chang
- Feng Zheng
- Ivan Laptev
- Xiaodan Liang
topics:
- vision-language-action
- generalist-robot-policy
- adaptive-inference
- flow-matching
- robot-data-scaling
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# A1: A Fully Transparent Open-Source, Adaptive and Efficient Truncated Vision-Language-Action Model

## Summary
## 摘要
A1 是一个用于机器人操作的开源视觉-语言-行动模型，目标是在不过多牺牲任务成功率的前提下降低推理成本。它的核心思路是：当动作已经稳定时提前停止主干网络，并通过复用上一层的部分动作来减少 flow matching 去噪计算。

## 问题
- 用于机器人控制的视觉-语言-行动模型通常依赖大型视觉-语言主干和扩散或 flow-based 动作头，这会让实时部署变慢，成本更高。
- 只缩短主干网络的加速方法会把动作头留成瓶颈，尤其是在动作生成需要 10 到 20 步去噪时。
- 这对机器人操作很关键，因为控制回路需要在实际硬件上保持低延迟，而不只是高基准准确率。

## 方法
- A1 将预训练的基于 Molmo 的 VLM 主干与 flow-matching 动作头（`A1-FM`）或更简单的 MLP 动作头（`A1-MLP`）结合起来。
- 训练时，它对来自中间主干层的动作进行监督，这样模型在完整流程结束前就能输出可用动作。
- 推理时，它比较当前层预测的动作与上一层的动作。如果差异低于校准阈值，就提前退出。
- 对于 flow matching，它引入了 **Inter-Layer Truncated Flow Matching**：每层只运行少量去噪步数，比如 2 步，并用当前层预测的动作作为下一层的 warm-start，而不是从随机噪声重新开始。
- 它预训练于多个开源机器人数据集，包括 DROID、AgiBot、RoboCOIN、RoboMind、GM-100 和 RoboChallenge，以及跨多个机器人的 15,951 条内部轨迹。

## 结果
- 在 **RoboChallenge** 上，A1 的平均成功率为 **29.00%**，高于 **pi_0: 28.33%**、**X-VLA: 21.33%** 和 **RDT-1B: 15.00%**。
- 在 **Franka、AgiBot、OpenArm 和 Dobot-Arm** 等真实机器人上，A1 的平均成功率为 **56.7%**。原文说这高于基线，但所示文本没有给出基线数值。
- 在 **LIBERO** 上，A1 的平均成功率为 **96.6%**。在所示表格中，这高于 **pi_0: 94.2%**，低于 **OpenVLA-OFT: 97.1%**，接近 **pi_0.5: 96.9%**。
- 在 **VLABench** 上，A1 的平均成功率为 **53.5%**。在所示表格中，这高于 **pi_0: 42.0%** 和 **pi_0.5: 49.5%**。
- 在效率方面，论文声称 flow-matching 推理的每回合延迟最多降低 **72%**，主干计算量最多减少 **76.6%**，且性能损失很小。
- 文中的一个具体延迟例子是：在他们的设置下，LIBERO 上的 flow-matching 推理每回合从 **37.8s** 降到 **10.5s**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05672v3](http://arxiv.org/abs/2604.05672v3)
