---
source: arxiv
url: http://arxiv.org/abs/2603.01766v1
published_at: '2026-03-02T11:48:24'
authors:
- Haoyun Liu
- Jianzhuang Zhao
- Xinyuan Chang
- Tianle Shi
- Chuanzhang Meng
- Jiayuan Tan
- Feng Xiong
- Tong Lin
- Dongjie Huo
- Mu Xu
- SongLin Dong
- Zhiheng Ma
- Yihong Gong
- Sheng Zhong
topics:
- vision-language-action
- continuous-action-representation
- implicit-neural-representation
- robot-manipulation
- impedance-control
relevance_score: 0.96
run_id: materialize-outputs
---

# Neural Implicit Action Fields: From Discrete Waypoints to Continuous Functions for Vision-Language-Action Models

## Summary
NIAF 将视觉-语言-动作模型的动作输出从离散轨迹点改为连续时间函数，以更贴合真实机器人运动的连续性。核心价值在于能以任意频率查询动作，并直接得到解析速度/加速度/jerk，从而提升长时序任务表现与真实机器人控制平滑性。

## Problem
- 现有 VLA 多预测离散 waypoints 或固定长度 action chunks，但机器人运动本质上是连续的；离散化会绑定固定采样率，难以适配不同控制频率。
- 离散表示通常缺乏高阶导数的一致约束，速度/加速度往往依赖数值微分，容易引入量化噪声、抖动和控制不稳定。
- 这很重要，因为精细 manipulation 和阻抗控制需要平滑且物理一致的参考轨迹，而不是只适合刚性位置控制的粗糙离散点列。

## Approach
- 把动作 chunk 表示为连续函数 \(\mathcal{A}(\tau)=\Phi(\tau;\theta)\)，模型不再直接输出离散动作序列，而是预测定义整条轨迹的函数参数 \(\theta\)。
- 使用多模态大语言模型（MLLM）作为 hypernetwork / hierarchical spectral modulator：根据图像、状态和语言指令，生成调制向量去重配置一个共享的 SIREN 动作解码器。
- 用 SIREN（正弦隐式网络）表示动作场，因为它天然可解析求导且具有 \(C^{\infty}\) 平滑性；因此可在任意时间点查询位置，也可直接解析得到速度、加速度和 jerk。
- 提出 grouped hyper-modulation：把不同 token 分配给 SIREN 各层的频率与相位调制，使语义信息分层地控制轨迹几何与运动学。
- 训练时除位置损失外，还可加入解析的速度损失、加速度损失和 jerk 正则；在真实机器人上，这些解析量可直接用于阻抗控制的前馈/阻尼项。

## Results
- **CALVIN, ABCD→D**：NIAF（0.77B、**无机器人大规模预训练**）Avg. Len **4.66**，高于 BEAST **4.61**、FLOWER **4.62**、UniVLA **4.63**；1/2/3/4/5 连续任务成功率分别为 **0.997/0.978/0.946/0.900/0.839**。
- **CALVIN, ABC→D**：NIAF Avg. Len **4.47**，高于 BEAST **4.42**、FLOWER **4.44**、UniVLA **4.41**；4-task 与 5-task 成功率分别为 **0.848** 和 **0.764**，优于 BEAST 的 **0.827/0.744** 与 FLOWER 的 **0.823/0.755**。
- 文中声称在 **CALVIN 和 LIBERO** 上实现了跨多种 backbone 的 **state-of-the-art**，并提到可从 Florence-2 扩展到 Qwen3-VL；但给定摘录中的 LIBERO 表格被截断，因此无法完整列出其全部数值结果。
- 真实机器人实验覆盖 **4 个任务**：Item Placement、Cup Stacking、Shape Insertion、Towel Folding。摘录未提供成功率或误差等定量指标，但作者明确声称连续动作表示可减少离散基线中的 control jitter，并支持更稳定的 impedance control。
- 相比离散 waypoint 方法，论文最强的具体主张是：NIAF 能以**无限分辨率**生成轨迹、在**单次前向**中输出连续动作场，并提供**解析无噪声**的速度/加速度/jerk 用于物理一致控制。

## Link
- [http://arxiv.org/abs/2603.01766v1](http://arxiv.org/abs/2603.01766v1)
