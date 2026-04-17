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
A1 是一个用于机器人操作的开源视觉-语言-动作模型，目标是在不明显牺牲任务成功率的前提下降低推理成本。它的核心思路是：当动作已经稳定时提前停止骨干网络计算，并通过复用前一层的部分动作结果来减少 flow matching 的去噪计算。

## 问题
- 用于机器人控制的视觉-语言-动作模型通常使用大型视觉-语言骨干网络，再加上扩散或基于 flow 的动作头，因此实时部署速度慢、成本高。
- 只缩短骨干网络的加速方法会让动作头继续成为瓶颈，尤其是在动作生成需要 10 到 20 步去噪时。
- 这对机器人操作很关键，因为控制循环需要在实际硬件上保持低延迟，而不只是追求基准测试中的高准确率。

## 方法
- A1 将基于预训练 Molmo 的 VLM 骨干网络，与 flow-matching 动作头（`A1-FM`）或更简单的 MLP 动作头（`A1-MLP`）结合起来。
- 在训练阶段，它对骨干网络中间层输出的动作进行监督，因此模型在完整堆栈尚未运行完之前就能产生可用动作。
- 在推理阶段，它比较当前层预测的动作与前一层的动作。如果两者差异低于校准后的阈值，就提前退出。
- 对于 flow matching，它提出了 **层间截断 Flow Matching**：每层只运行少量去噪步骤，例如 2 步，并用当前层预测的动作作为下一层的热启动，而不是从随机噪声重新开始。
- 它在多个开放机器人数据集上进行了预训练，包括 DROID、AgiBot、RoboCOIN、RoboMind、GM-100 和 RoboChallenge，此外还有覆盖多种机器人的 15,951 条内部轨迹。

## 结果
- 在 **RoboChallenge** 上，A1 报告的平均成功率为 **29.00%**，高于 **pi_0: 28.33%**、**X-VLA: 21.33%** 和 **RDT-1B: 15.00%**。
- 在 **Franka、AgiBot、OpenArm 和 Dobot-Arm** 等真实机器人上，A1 报告的平均成功率为 **56.7%**。摘录称这一结果高于基线，但显示出来的文本里没有给出基线数值。
- 在 **LIBERO** 上，A1 报告的平均成功率为 **96.6%**。在显示的表格中，这一结果高于 **pi_0: 94.2%**，低于 **OpenVLA-OFT: 97.1%**，并且接近 **pi_0.5: 96.9%**。
- 在 **VLABench** 上，A1 报告的平均成功率为 **53.5%**。在显示的表格中，这一结果高于 **pi_0: 42.0%** 和 **pi_0.5: 49.5%**。
- 在效率方面，论文声称 flow-matching 推理的**单回合延迟最高可降低 72%**，并且在性能损失较小的情况下，**骨干网络计算量最高可减少 76.6%**。
- 文中给出的一个具体延迟例子是：在其设置下，**LIBERO** 上 flow-matching 推理的单回合耗时从 **37.8s 降到 10.5s**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05672v3](http://arxiv.org/abs/2604.05672v3)
