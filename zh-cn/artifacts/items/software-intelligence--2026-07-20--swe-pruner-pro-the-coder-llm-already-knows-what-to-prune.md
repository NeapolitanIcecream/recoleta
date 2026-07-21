---
source: arxiv
url: https://arxiv.org/abs/2607.18213v1
published_at: '2026-07-20T17:47:44'
authors:
- Yuhang Wang
- Yuling Shi
- Shaoqiu Zhang
- Jialiang Liang
- Shilin He
- Siyu Ye
- Yuting Chen
- Kai Cai
- Xiaodong Gu
topics:
- code-intelligence
- software-foundation-models
- context-pruning
- coding-agents
- automated-software-production
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Pruner Pro: The Coder LLM Already Knows What to Prune

## Summary
## 总结
SWE-Pruner Pro 利用编码代理自身的隐藏状态，在不使用单独剪枝模型或额外查询的情况下移除不必要的工具输出行。在两个开放权重骨干模型和四个多轮基准测试中，该方法报告了最高 39.4% 的 token 节省，同时基本保持任务质量；在 MiMo-V2-Flash 上，Oolong 和 SWE-Bench Verified 的表现有所提升。

## 问题
- 编码代理会在多轮交互中积累冗余的文件、搜索和终端输出；在一项被引用的 SWE-Bench 设置中，工具输出占 token 总量的 70% 以上。
- 现有压缩器使用与任务无关的信号，或需要单独的评分器和显式的目标提示查询，这会增加成本，也可能无法捕捉代理当前的信息需求。
- 该论文研究的问题是：在保持任务质量并控制推理开销的同时，能否减少长上下文中的工具输出。

## 方法
- 一个轻量级剪枝头在正常的工具响应预填充阶段读取冻结骨干模型最后一层的隐藏状态，并为每个 token 预测保留或剪枝标签。
- 通过多数投票将 token 级预测转换为行级决策，保留选中的代码行，并在后续轮次中移除被剪枝的行。
- 该剪枝头为响应的行数加入一个学习得到的嵌入，并使用一个包含两个模块的前馈分类器。
- 训练使用 Claude Sonnet 4.6 对 22,609 个多轮轨迹样本进行的行级标注，以及逐样本平衡的 focal loss，使每个样本中的保留类和剪枝类获得相同权重。

## 结果
- 在约 2,260 个工具响应和 155,000 行数据上，线性探针取得了 0.83 的 AUC 和 0.63 的最佳 F1；相比之下，多数类基线的 F1 上限为 0.46。这支持了剪枝信息存在于骨干模型表示中的观点。
- 在 Qwen3-Coder-Next 上，SWE-Pruner Pro 在 SWE-QA、SWE-QA-Pro 和 Oolong 上分别减少了 34.7%、39.4% 和 13.9% 的 token；相对于不剪枝，质量变化分别为 +0.02、+0.24 和 -1.4 个百分点。
- 在 MiMo-V2-Flash 上，该方法在 SWE-QA、SWE-QA-Pro 和 Oolong 上分别减少了 6.9%、22.6% 和 30.1% 的 token；Oolong 准确率提高了 2.2 个百分点，达到 94.6。
- 在 SWE-Bench Verified 上，MiMo-V2-Flash 解决了 345/500 个任务，而不剪枝时为 326/500，提升了 3.8 个百分点；Qwen3-Coder-Next 解决了 335/500 个任务，而不剪枝时为 341/500，同时将输入 token 减少了 13.5%。
- 在一项回放研究中，服务器内剪枝头使总体耗时增加了 15.0%，且不需要额外的模型调用；不过，Qwen3-Coder-Next 的 SWE-Bench API 调用次数从 131.9 增至 139.8。
- 在消融实验中，逐样本平衡的 focal loss 达到 0.635 的行级 F1 和 7.08 的评审得分，而 BCE 分别为 0.475 和 5.95；加入长度嵌入后，评审得分从 6.86 提高到 7.08，而 F1 几乎没有变化。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18213v1](https://arxiv.org/abs/2607.18213v1)
