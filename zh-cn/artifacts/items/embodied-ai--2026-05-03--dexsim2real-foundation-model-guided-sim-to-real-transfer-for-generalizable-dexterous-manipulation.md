---
source: arxiv
url: https://arxiv.org/abs/2605.05241v1
published_at: '2026-05-03T17:29:29'
authors:
- Zijian Zeng
- Fei Ding
- Huiming Yang
- Xianwei Li
- Yuhao Liao
topics:
- sim2real
- dexterous-manipulation
- vision-language-models
- domain-randomization
- visuo-tactile-policy
- robot-foundation-models
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation

## Summary
## 摘要
DexSim2Real 在仿真中训练灵巧机器人策略，并通过视觉语言模型调节仿真随机化，将策略迁移到配有 Allegro Hand 的真实 Franka Panda 上。

## 问题
- 在仿真中训练的灵巧操作策略常在真实机器人上失败，因为视觉外观、物理特性、相机位姿、摩擦、质量和传感器信号在仿真与硬件之间存在差异。
- 标准域随机化需要手工调节取值范围，并且可能在不真实的仿真世界中训练，这会损害插入、手内旋转、工具使用和倾倒等接触密集型任务的表现。
- 这个问题很重要，因为灵巧手需要可靠的零样本迁移，以减少真实世界数据采集、人工调参和硬件上的不安全试错。

## 方法
- FM-DR 使用 GPT-4V 作为视觉真实感评估器：它将渲染的仿真图像与真实参考图像进行比较，并按 1–10 分评价光照、纹理、几何形状和物理合理性。
- CMA-ES 优化仿真参数上的高斯混合分布，包括摩擦、质量缩放、光照、纹理噪声和相机位姿噪声；熵项让训练分布保留变化。
- TVCAP 用独立编码器编码 RGB、触觉读数和本体感知，然后使用双向交叉注意力，使视觉在接触期间可以关注触觉，触觉也可以关注视觉。
- PSC 使用 LLM 将自然语言任务拆分为子技能，在子技能成功率超过 0.8 时提高任务难度，并在成功率超过 0.9 后串联技能。
- 最终策略在 Isaac Sim 中用 PPO 训练，并在真实机器人上直接部署；这些 sim-to-real 方法不使用真实演示。

## 结果
- 在六个真实世界任务上，每个任务 50 次试验、3 个种子，DexSim2Real 报告的平均成功率为 78.2%。表中报告 Act3D 使用 100 个真实演示时为 66.1%，DrEureka 为 65.1%，DeXtreme 为 59.2%，ADR 为 54.2%，Vanilla DR 为 45.2%。
- DexSim2Real 的任务成功率分别为 92.3% Pick-Place、85.7% Stacking、78.4% Peg Insertion、71.2% In-Hand Rotation、67.8% Tool Use 和 73.5% Pouring。
- DexSim2Real 的平均 sim-to-real 差距为 8.3%，相比之下 Vanilla DR 为 28.5%，ADR 为 19.2%。
- 消融实验报告：去掉 FM-DR 并使用 Vanilla DR 时为 65.8%，去掉 FM-DR 并使用 ADR 时为 69.3%，去掉触觉输入时为 70.1%，用拼接替代交叉注意力时为 72.4%，去掉 PSC 时为 68.9%。
- FM-DR 将平均 VLM 真实感得分从 4.2/10 提高到 7.8/10，将摩擦均值误差从 0.35 降到 0.08，并且相对于均匀随机化将熵降低 18%。
- 论文报告称，FM-DR 每个任务大约需要 200–300 次 VLM 查询，使用种群大小为 16、迭代 50 代的 CMA-ES，并增加约 2 个 GPU 小时的额外开销。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05241v1](https://arxiv.org/abs/2605.05241v1)
