---
source: arxiv
url: http://arxiv.org/abs/2603.06276v1
published_at: '2026-03-06T13:34:09'
authors:
- Pranam Prakash Shetty
- Adarsh Balakrishnan
- Mengqiao Xu
- Xiaoyin Xi
- Zhe Yu
topics:
- story-point-estimation
- large-language-models
- agile-software-development
- few-shot-learning
- comparative-judgment
relevance_score: 0.84
run_id: materialize-outputs
---

# Story Point Estimation Using Large Language Models

## Summary
本文研究大语言模型能否在几乎没有项目内标注数据的情况下完成敏捷开发中的故事点估算。结论是：零样本LLM已能超过基于80%训练数据的监督式深度学习基线，少量示例还能进一步提升效果。

## Problem
- 论文解决的是**软件项目中用户故事/待办项的故事点估算**问题，这直接影响冲刺规划、资源分配和交付可预测性。
- 现有监督式方法通常需要**同一项目内大量已标注故事点数据**，而新项目或数据稀缺项目往往拿不到这些标签。
- 研究还关注一种更省人工的监督形式：**比较判断**（两个任务谁更费力），想知道它对LLM是否更容易、是否能替代少量故事点标签。

## Approach
- 在16个真实软件项目上评估4个现成LLM：Kimi、DeepSeek、Gemini Flash Lite、OpenAI GPT-5 Nano，输入为backlog item的标题和描述。
- 做**零样本故事点预测**：不给训练数据，直接让模型输出故事点，并用 Pearson 相关系数和 Spearman 排名相关评估。
- 做**少样本故事点预测**：每个项目只给5个带标签示例，并比较两种选例策略：按高频故事点抽样（Count）与按故事点量程覆盖抽样（Scale）。
- 做**比较判断实验**：让LLM直接判断一对事项中谁工作量更大，检查这是否比直接预测故事点更容易。
- 做**比较判断作为少样本上下文**的实验：给模型少量“任务A比任务B更大/更小”的例子，再让它输出故事点，看能否帮助校准项目内尺度。

## Results
- **零样本优于监督基线（平均表现）**：在16个项目上，SBERT Regression（使用**80%训练数据**）平均 Pearson **0.3175**、Comparative baseline **0.3337**；而零样本LLM中 Kimi 达 **0.3735**，DeepSeek 达 **0.4040**，均更高；Gemini **0.2363**、OpenAI **0.2712** 较弱。
- **零样本排名相关也更强**：平均 Spearman 方面，传统 Regression 为 **0.3037**、Comparative 为 **0.3222**；论文表中 Kimi 与 DeepSeek在多项目上高于这些基线，例如 DeepSeek 在 appceleratorstudio **0.3885**、aptanastudio **0.4554**、bamboo **0.3784**、clover **0.6358**。
- **若看单项目峰值**：DeepSeek 在 clover 上 Pearson **0.8364**，明显高于该项目 Regression **0.4403** 与 Comparative **0.4190**；在 datamanagement 上 DeepSeek **0.4703** 也高于 Regression **0.3775**。
- **少样本提示进一步提升**：摘要明确声称，加入**仅少量示例**后，LLM故事点预测还能优于零样本；并且比较判断也可以作为少样本示例来提升预测表现。
- **比较判断并不更容易**：摘要明确指出，LLM**预测比较判断并不比直接预测故事点更容易**，这与“对人类更容易”这一假设不同。
- **定量结果不完整**：给定摘录中，RQ2/RQ3/RQ4 的完整数值表未展示，因此无法列出少样本和比较判断实验的完整平均指标；但论文的最强定量主张是：**零样本LLM已超过使用80%训练数据的监督深度学习模型，少样本还能继续改善。**

## Link
- [http://arxiv.org/abs/2603.06276v1](http://arxiv.org/abs/2603.06276v1)
