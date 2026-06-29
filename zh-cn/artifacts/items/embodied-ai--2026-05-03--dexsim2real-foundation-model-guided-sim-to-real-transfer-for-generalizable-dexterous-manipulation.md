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
## 总结
DexSim2Real 通过用视觉-语言模型调节仿真随机化，在仿真中训练灵巧机器人策略，并将其迁移到装有 Allegro Hand 的真实 Franka Panda 机器人上。

## 问题
- 仅在仿真中训练的灵巧操作策略到了真实机器人上常常失效，因为仿真和硬件在外观、物理动力学、相机位姿、摩擦、质量和传感器信号上都不同。
- 标准的域随机化需要手工设定范围，还可能训练出不真实的仿真世界，这会损害插入、在手旋转、工具使用和倾倒这类接触丰富的任务。
- 这个问题很重要，因为灵巧手需要可靠的零样本迁移，才能减少真实数据采集、人工调参和在硬件上的高风险试错。

## 方法
- FM-DR 把 GPT-4V 作为视觉真实性评审：它按 1–10 分对渲染的仿真图像和真实参考图像在光照、纹理、几何和物理合理性上进行评分。
- CMA-ES 在仿真参数上的高斯混合分布上做优化，参数包括摩擦、质量缩放、光照、纹理噪声和相机位姿噪声；熵项保持训练分布中的变化。
- TVCAP 用单独的编码器处理 RGB、触觉读数和本体感觉，然后用双向交叉注意力，让视觉在接触时关注触觉，触觉也关注视觉。
- PSC 用 LLM 把自然语言任务拆成子技能，当子技能成功率超过 0.8 时提高任务难度，当成功率超过 0.9 时串接技能。
- 最终策略在 Isaac Sim 中用 PPO 训练，并直接部署到真实机器人上；这些 sim-to-real 方法不需要真实示范。

## 结果
- 在 6 个真实世界任务上，每个任务 50 次试验、3 个随机种子，DexSim2Real 的平均成功率是 78.2%。表中 Act3D 在 100 个真实示范下为 66.1%，DrEureka 为 65.1%，DeXtreme 为 59.2%，ADR 为 54.2%，Vanilla DR 为 45.2%。
- DexSim2Real 的任务成功率分别是：抓取放置 92.3%，堆叠 85.7%，插销插入 78.4%，在手旋转 71.2%，工具使用 67.8%，倾倒 73.5%。
- DexSim2Real 的平均 sim-to-real gap 是 8.3%，Vanilla DR 为 28.5%，ADR 为 19.2%。
- 消融结果显示：去掉 FM-DR 并使用 Vanilla DR 时为 65.8%，去掉 FM-DR 并使用 ADR 时为 69.3%，去掉触觉输入时为 70.1%，用拼接代替交叉注意力时为 72.4%，去掉 PSC 时为 68.9%。
- FM-DR 把平均 VLM 真实性评分从 4.2/10 提高到 7.8/10，把摩擦均值误差从 0.35 降到 0.08，并且相对均匀随机化把熵降低了 18%。
- 论文写到，FM-DR 每个任务大约需要 200–300 次 VLM 查询，CMA-ES 的种群大小为 16，运行 50 代，额外增加约 2 个 GPU 小时的开销。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05241v1](https://arxiv.org/abs/2605.05241v1)
