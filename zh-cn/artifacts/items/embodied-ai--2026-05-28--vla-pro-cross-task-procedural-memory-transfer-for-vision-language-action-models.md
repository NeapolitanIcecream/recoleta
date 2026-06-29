---
source: arxiv
url: https://arxiv.org/abs/2605.29562v1
published_at: '2026-05-28T08:14:08'
authors:
- Shengyu Si
- Yuanzhuo Lu
- Ruimeng Yang
- Ziyi Ye
- Zuxuan Wu
- Yu-Gang Jiang
topics:
- vision-language-action
- robot-foundation-model
- procedural-memory
- cross-task-generalization
- lora-adaptation
- manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# VLA-Pro: Cross-Task Procedural Memory Transfer for Vision-Language-Action Models

## Summary
## 总结
VLA-Pro 为 VLA 策略加入可检索的 LoRA 程序记忆，让它们能复用已见操作任务中的经验，并迁移到未见任务上。它在 RoboTwin、RLBench 和真实机器人任务上，配合 π0.5、RDT 和 X-VLA 主干都报告了明显提升。

## 问题
- 当新任务中的物体、场景或动作模式与训练数据不同，VLA 机器人策略常常无法在未见任务上泛化，即使新任务和已见任务很接近也一样。
- 混合任务微调会把策略拉向训练中更常见的行为，比如指令需要不同空间关系时，模型却偏向把物体放到支架上。
- 这很重要，因为通用机器人策略需要跨任务迁移，而不是为每个新操作任务都重新收集演示或微调。

## 方法
- 训练时，VLA-Pro 先在所有已见任务上学习一个共享的基础 LoRA，再为每个已见任务微调一个任务专属 LoRA 适配器。
- 每条记忆把该任务的 LoRA 和一组结构化程序状态配对：动作类型、物体几何形状、末端执行器朝向和目标交互点。
- 推理时，视觉语言模型从图像、指令和之前的交互历史中提取当前程序状态。
- 系统通过对这些结构化字段做动作感知匹配，检索最接近的前 k 条任务记忆，然后用 Softmax 相似度权重融合这些检索到的 LoRA 权重。
- 融合后的 LoRA 会加载到当前动作块中生成动作，随后在下一块动作前卸载。

## 结果
- 在 RoboTwin 上，VLA-Pro 将 X-VLA 的平均成功率从 17.0% 提高到 30.0%，将 RDT 从 11.1% 提高到 34.1%，将 π0.5 从 40.4% 提高到 59.3%。RDT 的结果是论文中报告的最大相对提升，约 207%。
- 在 RoboTwin 的 place_bell_behind 任务上，π0.5 的成功率从 0.0% 提高到 100.0%。
- 在 RLBench 零样本任务上，VLA-Pro 搭配 π0.5 在至少有一种方法成功的 9 个任务里取得了最高平均成功率，分别比 RDT 高 10.7 个百分点、比 AtomicVLA 高 6.2 个百分点、比 π0.5 基线高 7.1 个百分点。
- 在使用 UR7e 机械臂、6 个留出任务、每个任务 20 次试验的真实世界测试中，π0.5 的平均成功率从 5.8% 提高到 65.0%。
- 在 RLBench 的 top-k 消融实验中，k=2 的平均成功率达到 20.9%，而 π0.5 基线为 13.8%，相对提升 51.4%；k=1 为 16.9%，k=3 为 16.4%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29562v1](https://arxiv.org/abs/2605.29562v1)
