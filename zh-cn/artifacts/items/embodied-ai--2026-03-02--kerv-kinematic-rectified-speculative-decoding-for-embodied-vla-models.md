---
source: arxiv
url: http://arxiv.org/abs/2603.01581v1
published_at: '2026-03-02T08:12:03'
authors:
- Zihao Zheng
- Zhihao Mao
- Maoliang Li
- Jiayu Chen
- Xinhao Sun
- Zhaobo Zhang
- Donggang Cao
- Hong Mei
- Xiang Chen
topics:
- vision-language-action
- speculative-decoding
- robot-kinematics
- kalman-filter
- embodied-ai
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# KERV: Kinematic-Rectified Speculative Decoding for Embodied VLA Models

## Summary
本文提出 KERV，把机器人运动学引入具身 VLA 的 speculative decoding，用轻量运动学预测替代部分重推理并动态调阈值，从而加速推理且尽量不损失任务成功率。核心价值是在机器人控制里同时利用 token 生成能力和 kinematic 短时预测能力。

## Problem
- 论文解决的是 **VLA 机器人策略推理太慢** 的问题；虽然 speculative decoding 能加速，但在 VLA 中一旦草稿 token 出错，通常需要高成本 re-inference，导致加速效果受限。
- 另一个关键问题是 **接受阈值难设**：阈值太松会累积动作误差、降低成功率，太严又拿不到速度收益；固定阈值无法适应不同任务和环境。
- 这很重要，因为 VLA 是 embodied foundation model / vision-language-action 机器人的主流范式，但真实机器人控制需要更快、更稳定的闭环推理。

## Approach
- KERV 的核心思想很简单：**当 speculative decoding 的 token 出错时，不再总是让大模型重算，而是用基于运动学的 Kalman Filter 直接补完当前动作片段剩余部分**。
- 方法先把 VLA 输出 token 映射成 7-DoF 动作（位置、姿态、夹爪），并为每个 DoF 建动作缓存；KF 利用短动作上下文做一步预测。论文设置 **Predict Length = 1、Action Context = 10**，以控制运动学预测误差。
- 为避免 KF 长期预测误差积累，补偿机制并非每步都开：每次补偿后，接下来 **n=4** 步关闭 KF，再回到常规 SD。
- 第二个机制是 **基于运动学波动 K_var 的动态接受阈值调整**：不是只看 token ID 误差是否小于固定阈值，而是把误差映射到动作空间，依据运动学变化动态收紧或放宽阈值。文中多数任务使用 **r_max=15, r_min=5**。
- 系统实现上，大模型 draft/verify 放在 GPU，KF 补偿和阈值调整放在 CPU；因为这两部分 FLOPs 小但逻辑判断多，CPU+GPU 协同更合适。文中给出的计算量是：draft **0.07 GFLOPs/inf**，verify **3.92 TFLOPs/inf**；显存占用约 **700MB vs 15GB**。

## Results
- 在 **LIBERO** 四个任务套件（Goal/Object/Spatial/Long）上，KERV 相比 naive VLA+SD 声称达到 **1.48×–1.57×** 端到端加速，且“**without SR loss / nearly no Success Rate loss**”。
- 相比现有 **SpecVLA**，论文声称 KERV 取得 **27%–37%** 额外加速，同时几乎不损失成功率；摘要中直接给出这一主结论。
- **Goal**：naive VLA+SD 为 **76.2% SR, 1.00×, 159.2 steps**；SpecVLA 最快约 **1.23×**（r=15）但 SR 降到 **71.0%**；**KERV 为 75.6% SR, 1.54×, 153.5 steps**。相对 naive 提速 **54%**，相对 SpecVLA(r=15) 提速约 **25%**，SR 仅低 **0.6pt** 于 naive、但高于更快阈值下的 SpecVLA。
- **Object**：naive 为 **68.6% SR, 1.00×, 195.9 steps**；SpecVLA 为 **1.09×–1.10×**，SR 在 **58.0%–70.0%**；**KERV 为 72.3% SR, 1.49×, 186.8 steps**。相对 naive 提速 **49%**，且 SR 还提升 **3.7pt**。
- **Spatial**：naive 为 **82.8% SR, 1.00×, 127.3 steps**；SpecVLA 为 **1.24×–1.26×**，SR 在 **77.8%–85.2%**；**KERV 为 83.7% SR, 1.57×**，是表中最高速度。节选未完整给出其 steps，但文中声称四个环境里 KERV 的平均推理步数最少。
- 论文还给出一个负面对照：naive 把 SD 直接接到 VLA 上时，在四个环境里速度只有 **0.86×–0.98×**（相对 AR 的 1× 反而变慢），每步时延从 **0.188–0.198s** 升到 **0.200–0.217s**，说明如果不解决错误重推理和阈值问题，SD 在 VLA 上未必有效。

## Link
- [http://arxiv.org/abs/2603.01581v1](http://arxiv.org/abs/2603.01581v1)
