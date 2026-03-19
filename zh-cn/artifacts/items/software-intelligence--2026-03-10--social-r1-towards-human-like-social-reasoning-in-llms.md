---
source: arxiv
url: http://arxiv.org/abs/2603.09249v1
published_at: '2026-03-10T06:26:24'
authors:
- Jincenzi Wu
- Yuxuan Lei
- Jianxun Lian
- Yitian Huang
- Lexin Zhou
- Haotian Li
- Xing Xie
- Helen Meng
topics:
- social-reasoning
- theory-of-mind
- reinforcement-learning
- process-supervision
- llm-alignment
relevance_score: 0.64
run_id: materialize-outputs
language_code: zh-CN
---

# Social-R1: Towards Human-like Social Reasoning in LLMs

## Summary
本文提出 Social-R1，用更难的社会推理数据和“过程级”强化学习，让大语言模型学会更像人类的社会推理，而不是靠表面模式猜答案。核心结论是：通过对推理轨迹而非只对最终答案进行对齐，小模型也能在社会智能任务上超过更大模型。

## Problem
- 论文解决的是 LLM 在社会推理/Theory-of-Mind 任务中“看起来会做、其实靠捷径”的问题：模型常先猜答案，再事后编理由，而不是真正从故事线索推断人物心理状态。
- 这很重要，因为社会智能直接影响人机协作、对人类意图和情绪的理解，以及 AI 在开放情境中的可靠性；如果模型只会模式匹配，遇到扰动或分布外案例就会失效。
- 论文还指出现有基准过于容易，掩盖了这种脆弱性：模型在简单 ToM 基准上接近人类，但在更难的对抗测试上显著掉分。

## Approach
- 作者先构建 **ToMBench-Hard**：一个包含 **800** 道专家标注、多选式、对抗性 Theory-of-Mind 题目的基准，覆盖 belief、desire、emotion、intention、knowledge、non-literal communication 六类社会智能能力，并用三位标注者保证质量。
- 然后提出 **Social-R1**：不是只奖励答对，而是用强化学习监督“整个推理过程”。它要求模型按人类社会信息处理（SIP）的四阶段推进：先找社会线索，再解释心理状态，再明确目标，最后给出回应。
- 奖励函数是多维的：**结构奖励**保证推理按阶段展开，**内容奖励**检查每一步是否有故事证据支撑，**长度/重复奖励**抑制啰嗦和循环思考，外加格式奖励便于抽取 reasoning 与 answer。
- 内容奖励由单独训练的 reward model 提供：基于 **SocialPairs-20K** 偏好数据集训练，初始化自 Qwen3-4B；训练时对 **Qwen3-4B/8B** 做 RL，使用 **700** 个训练样本、**100** 个测试样本、**600** 个优化步，在 **8×A100 80GB** 上运行。

## Results
- **ToMBench-Hard 揭示现有模型存在“捷径幻觉”**：人类在该基准上准确率约 **0.89**；但 **DeepSeek-R1 0.61、O3 0.59、GPT-5 0.56、Qwen3-32B 0.52、Qwen3-8B 0.34**。相比之下，这些模型在较简单的 **ToM-RL** 上却有 **0.71–0.88**，说明旧基准高分不等于真实社会推理。
- **SocialR1-4B Full** 在 8 个基准上的 **Overall=0.6880**，明显高于原始 **Qwen3-4B 0.5822**，提升 **+0.1058**；同时超过 **LLaMa3.1-70B 0.6111** 和 **LLaMa3.1-70B_COT 0.6496**，也略低/接近 **Distill-Llama-70B 0.6886**。
- **SocialR1-8B Full** 达到 **Overall=0.7270**，高于 **Qwen3-8B 0.5877**（提升 **+0.1393**），也超过 **DeepSeek-R1 0.7073、GPT-5 0.6956、O3_COT 0.7163、Qwen3-32B 0.6624、Distill-Llama-70B 0.6886**，表明 8B 模型可凭训练方法胜过更大或更强基线。
- 分任务看，**SocialR1-8B Full** 在 **ToMBench-Hard Val 0.6279**、**SimpleToM 0.9675**、**EmoBench 0.7010**、**Hi-ToM 0.7083**、**TactfulToM 0.5079** 等指标上给出最强或接近最强结果；例如在 **SimpleToM** 上高于 **DeepSeek-R1 0.7187** 和 **Qwen3-32B 0.7634**。
- 奖励模型本身也有可量化质量：内容奖励模型在自动测试集 **2k pairs** 上准确率 **89.2%**，在人类校准的 **200 pairs** 子集上与人工标签一致率 **87.5%**。
- 消融表明“过程级奖励”整体有效：以 4B 为例，**only R_out=0.6332**，而 **Full=0.6880**；以 8B 为例，**only R_out=0.7004**，**Full=0.7270**。说明仅奖励最终答案不如同时约束结构、内容和效率。

## Link
- [http://arxiv.org/abs/2603.09249v1](http://arxiv.org/abs/2603.09249v1)
