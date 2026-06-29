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
最清楚的近期开花点是三件事：VLA 微调前的机器人对齐数据筛选层、面向世界模型的执行式评测流程，以及让骨干和数据混合实验保持可比性的共享训练栈。前两者在语料里有最直接的性能证据。基础设施这一项也有价值，但现有摘录里展示的下游收益还不完整。

## 机器人对齐的 VLM 数据打分，放在 VLA 微调前
VLA 预训练中的数据筛选环节已经足够具体，可以单独做成一个训练工具。任务很明确：给大规模 VLM 语料按与机器人轨迹的相似度打分，保留最对齐的样本，再在动作微调前做一段简短的中间训练。EmbodiedMidtrain 给出了这套方法里最清楚的做法。它先在冻结的 VLM 特征上训练一个轻量二分类器，把 VLA 样本和通用 VLM 样本分开，再用这个分数给候选数据排序。结果在小型骨干上提升很大：InternVL3.5-1B 在 SimplerEnv-Bridge 上从 36.5 提升到 56.3，在 Libero-10 上从 39.0 提升到 54.2，而且使用的样本数比复现的基线更少。论文还显示，这个学习到的筛选器优于随机选择和几种替代打分规则。

最先会用到它的是那些已经在微调开放 VLM 骨干做操控任务、但仅靠增加机器人数据收效不大的团队。这里需要的不是另一套完整的 VLA 栈，而是一个接入现有预训练流程的语料打分和筛选层，导出排序后的子集，并记录哪些上游来源提供了有用的具身样本。一个成本很低的验证方法很直接：选一个开放骨干，在相同 token 预算下分别跑一次选中子集的中间训练和一次随机子集对照，然后在 Libero-10 或 SimplerEnv-Bridge 这样的基准上比较闭环成功率。如果差距还在，这就会变成小型实验室里 VLA 训练的实用环节，因为它们没法把机器人采集速度再提得更快。

### Evidence
- [EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training](../Inbox/2026-04-21--embodiedmidtrain-bridging-the-gap-between-vision-language-models-and-vision-language-action-models-via-mid-training.md): Summarizes the classifier-based selection method and the benchmark gains across backbones.
- [EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training](../Inbox/2026-04-21--embodiedmidtrain-bridging-the-gap-between-vision-language-models-and-vision-language-action-models-via-mid-training.md): Confirms that the data engine captures sample-level alignment signals and favors spatial, embodied content.

## 面向机器人世界模型的执行导向评测
世界模型团队需要一个执行测试台，把生成的视频转成动作，并记录任务在哪一步出错。这个数据包里的两篇论文指向了同一类流程变化。Mask World Model 通过预测未来的语义 mask 来报告很高的操控成功率，保留了物体布局和接触线索，同时去掉了纹理和光照噪声。RoboWM-Bench 进一步说明了为什么这种选择重要：视觉上合理的生成结果，在转成机器人行为后仍会失败，而且很多模型只做到接触，没有完成后续序列。

这给内部工具留下了明确空间：一个评测器，把世界模型输出送入逆动力学或动作重定向模块，然后同时给最终成功和步骤级事件打分，比如接触、抬起、放置或抽屉关闭。目标用户是训练预测模型、但仍按视频质量或字幕一致性挑 checkpoint 的机器人团队。RoboWM-Bench 显示，早期步骤成功和完整完成之间差距很大，比如 Put on Plate 里有些模型的接触率能到 100%，但最终放置远低得多。在机器人任务上，即使经过微调，系统在长时序完成上仍然很弱；Cosmos-FT 在 Put in Drawer 里接触率有 60%，后续阶段只有 20%。一个能把这些掉点暴露出来的工具，会直接影响模型选择、消融分析和数据集排错。

一个低成本检查方法是，拿一个世界模型现有的生成轨迹，挑一小部分重新走一遍动作恢复流程，再比较视频指标和可执行任务指标下的排行榜顺序。如果排序变了，团队就有证据说明当前评测流程把真实失败模式藏起来了。

### Evidence
- [RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation](../Inbox/2026-04-21--robowm-bench-a-benchmark-for-evaluating-world-models-in-robotic-manipulation.md): Provides the executable-evaluation protocol and step-level failure patterns for generated robot manipulation videos.
- [Mask World Model: Predicting What Matters for Robust Robot Policy Learning](../Inbox/2026-04-21--mask-world-model-predicting-what-matters-for-robust-robot-policy-learning.md): Shows that preserving semantic structure in prediction can raise downstream success rates on LIBERO and RLBench.

## 统一的 LLM 到 VLA 实验栈，用于骨干和数据混合研究
贯穿 LLM、VLM 和 VLA 各阶段的共享训练栈，正在变成机器人团队做骨干和数据配比研究时的一层实用支撑。VLA Foundry 给出了一个具体信号。它把语言预训练、视觉语言训练和动作训练打包到同一个代码库里，支持混合的文本、图像字幕和机器人数据集，并且已经在 16 个节点上的 128 张 GPU 上测试过。论文还报告说，换成更强的预训练骨干，比如 Qwen3-VL，会得到一个多任务桌面操控策略，超过作者的基线，虽然摘录里没有给出准确的闭环差距。

短期要做的不是研究模型，而是可复现的基础设施，用来在固定动作头、固定机器人数据集和固定评测任务下比较不同预训练配方。这很重要，因为机器人团队常常同时改骨干、分词器、数据混合和动作训练代码，最后却分不清是哪一阶段带来了结果变化。一个合适的部署路径，是内部实验运行器：把数据预处理标准化成 WebDataset 分片，跟踪上游 checkpoint 的来源链路，并把骨干替换变成常规操作。最先用到它的是在公开和私有数据上做大量 VLA 消融的实验室和平台团队。

一个低成本验证步骤是操作性的：复现一个基线策略，只替换 VLM 骨干，并确认训练和评测轨迹在端到端上仍然可比。如果这样能让每次实验少掉一周的流水线拼接工作，这一层支撑在新的模型结果出来之前就已经值回来了。

### Evidence
- [VLA Foundry: A Unified Framework for Training Vision-Language-Action Models](../Inbox/2026-04-21--vla-foundry-a-unified-framework-for-training-vision-language-action-models.md): Describes the unified training stack, multimodal data handling, scale support, and backbone-swap claim.
- [VLA Foundry: A Unified Framework for Training Vision-Language-Action Models](../Inbox/2026-04-21--vla-foundry-a-unified-framework-for-training-vision-language-action-models.md): Confirms the released codebase and the claim that Qwen3-VL improves multi-task manipulation performance over baseline.
