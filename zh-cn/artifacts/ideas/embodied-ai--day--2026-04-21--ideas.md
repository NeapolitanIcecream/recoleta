---
kind: ideas
granularity: day
period_start: '2026-04-21T00:00:00'
period_end: '2026-04-22T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world-models
- humanoids
- training-data
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/humanoids
- topic/training-data
language_code: zh-CN
---

# 具身模型训练栈

## Summary
近期最明确的变化有三点：VLA 微调前增加面向机器人的数据筛选层、为世界模型加入基于执行结果的评估流程，以及使用共享训练栈来保持骨干和数据配比实验的可比性。前两者在这组材料里有更直接的性能证据。基础设施这条线也有价值，但现有摘录对其下游收益的披露还不够完整。

## VLA 微调前面向机器人的 VLM 数据打分
VLA 预训练中的数据选择阶段已经足够明确，可以做成独立训练工具。这个任务很聚焦：给大型 VLM 语料按与机器人轨迹的相似度打分，保留最对齐的样本，并在动作微调前做一次短暂的中期训练。EmbodiedMidtrain 给出了这组工作里最清晰的做法。它在冻结的 VLM 特征上训练一个轻量分类器，用来区分 VLA 样本和通用 VLM 样本，再用这个分数给候选数据排序。论文在小模型骨干上报告了很大的提升：InternVL3.5-1B 在 SimplerEnv-Bridge 上从 36.5 提升到 56.3，在 Libero-10 上从 39.0 提升到 54.2，而且使用的样本数少于复现的基线。论文还表明，学到的选择器优于随机选择和几种替代打分规则。

第一批用户会是那些已经在为操作任务微调开源 VLM 骨干、但继续增加机器人数据后收益仍然有限的团队。这里有用的产品不是另一整套 VLA 栈，而是一个可接入现有预训练流程的语料打分与筛选层，能够导出排序后的子集，并记录哪些上游数据源提供了有用的具身样本。低成本验证方法也很直接：选一个开源骨干，在相同 token 预算下做一次“筛选子集”的中期训练，再做一次“随机子集”的对照训练，然后在 Libero-10 或 SimplerEnv-Bridge 这样的基准上比较闭环成功率。如果差距稳定存在，这就会成为中小型实验室 VLA 训练中的实用环节，因为它们无法足够快地扩大机器人数据采集规模。

### Evidence
- [EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training](../Inbox/2026-04-21--embodiedmidtrain-bridging-the-gap-between-vision-language-models-and-vision-language-action-models-via-mid-training.md): 总结了基于分类器的选择方法，以及不同骨干上的基准提升。
- [EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training](../Inbox/2026-04-21--embodiedmidtrain-bridging-the-gap-between-vision-language-models-and-vision-language-action-models-via-mid-training.md): 确认这个数据引擎能捕捉样本级对齐信号，并偏向空间性、具身性的内容。

## 以执行结果为依据的机器人世界模型评估
世界模型团队需要一种执行测试工具链，能够把预测视频转成动作，并记录任务在哪一步失败。这组材料中的两篇论文都指向同一种工作流变化。Mask World Model 通过预测未来语义掩码来获得较高的操作成功率，保留物体布局和接触线索，同时去掉纹理和光照噪声。RoboWM-Bench 则说明了这种设计为什么重要：视觉上看起来合理的生成结果，在转成机器人行为后仍然会失败，而且很多模型只能做到接触，无法完成后续整个序列。

这为一个具体的内部工具留下了空间：一个评估器，把世界模型输出送入逆动力学或动作重定向流程，然后同时评估最终成功率和接触、抬起、放置、抽屉关闭等步骤级事件。目标用户是训练预测模型、但仍按视频质量或字幕一致性来选 checkpoint 的机器人团队。RoboWM-Bench 报告了早期步骤成功和完整任务完成之间的明显差距，例如在 Put on Plate 任务里，几个模型的接触率达到 100%，但最终放置成功率低得多。在机器人任务上，即使经过微调，系统在长时序完成上仍然偏弱；Cosmos-FT 在 Put in Drawer 中接触率为 60%，但后续阶段只有 20%。一个能把这些掉点暴露出来的工具，会改变模型选择、消融实验和数据集排查方式。

低成本检查方法是：从一个世界模型现有的生成 rollout 中取一小部分，通过动作恢复重新执行，然后比较按视频指标和按可执行任务指标得到的排行榜顺序。如果排名发生变化，团队就有证据表明，当前评估流程掩盖了真正的失败模式。

### Evidence
- [RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation](../Inbox/2026-04-21--robowm-bench-a-benchmark-for-evaluating-world-models-in-robotic-manipulation.md): 提供了面向生成机器人操作视频的可执行评估协议，以及步骤级失败模式。
- [Mask World Model: Predicting What Matters for Robust Robot Policy Learning](../Inbox/2026-04-21--mask-world-model-predicting-what-matters-for-robust-robot-policy-learning.md): 表明在预测中保留语义结构可以提升 LIBERO 和 RLBench 上的下游成功率。

## 用于骨干与数据配比研究的统一 LLM 到 VLA 实验栈
跨 LLM、VLM 和 VLA 阶段的共享训练栈，正在成为机器人团队进行受控骨干和数据配比研究的实用支撑层。VLA Foundry 是这里最明确的信号。它把语言预训练、视觉语言训练和动作训练放进同一个代码库，支持混合文本、图像描述和机器人数据集，并且已经在 16 个节点、最多 128 张 GPU 上测试过。论文还报告说，换用更强的预训练骨干，比如 Qwen3-VL，可以得到一个优于作者基线的多任务桌面操作策略，虽然摘录中没有给出精确的闭环差距。

短期内值得构建的不是研究模型，而是在固定动作头、固定机器人数据集和固定评测任务下比较预训练配方的可复现实验基础设施。这很重要，因为机器人团队常常同时改动骨干、tokenizer、数据配比和动作训练代码，最后无法判断到底是哪一阶段带来了结果变化。一个可行的部署路径是内部实验运行器：把数据预处理标准化为 WebDataset shards，跟踪上游 checkpoint 血缘关系，并让骨干替换变成常规操作。第一批用户会是那些在公开和私有数据上大量进行 VLA 消融实验的实验室和平台团队。

低成本验证是一个操作性检查：复现一个基线策略，只替换 VLM 骨干，并确认训练和评估轨迹从头到尾都保持可比。如果这样每次实验能少花一周处理流水线粘合工作，这个支撑层在新的模型结果出现之前就已经有价值。

### Evidence
- [VLA Foundry: A Unified Framework for Training Vision-Language-Action Models](../Inbox/2026-04-21--vla-foundry-a-unified-framework-for-training-vision-language-action-models.md): 描述了统一训练栈、多模态数据处理、扩展能力，以及替换骨干的相关论断。
- [VLA Foundry: A Unified Framework for Training Vision-Language-Action Models](../Inbox/2026-04-21--vla-foundry-a-unified-framework-for-training-vision-language-action-models.md): 确认已发布的代码库，以及 Qwen3-VL 在多任务操作性能上优于基线的说法。
