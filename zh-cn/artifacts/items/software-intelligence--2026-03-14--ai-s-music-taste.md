---
source: hn
url: https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/
published_at: '2026-03-14T23:57:07'
authors:
- caaaadr
topics:
- audio-llm
- multimodal-evaluation
- model-behavior
- subjective-judgment
- music-analysis
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# AI's Music Taste

## Summary
这篇文章做了一个轻量级趣味实验：让多模态音频模型为不同歌曲写短评并打分，以观察“AI 的音乐口味”。它更像模型行为展示而非严格学术论文，但能反映当前音频输入大模型在主观审美任务上的差异与不稳定性。

## Problem
- 作者想回答一个简单但有意思的问题：**不同 AI 模型在听音乐后会表现出怎样的“审美偏好”**。
- 这个问题重要之处不在于建立标准音乐评测，而在于揭示：当模型处理**开放式、主观性很强的音频任务**时，输出可能出现明显分歧、怪异偏好和稳定性问题。
- 文中也隐含指出现实限制：**可用的音频输入模型很少**，同时还要支持**结构化输出**，这限制了系统化比较。

## Approach
- 作者选取了一小批可通过 **OpenRouter** 使用、同时支持**音频输入**和**结构化输出**的模型进行测试。
- 给这些模型播放一系列歌曲与声音样本，并要求它们**生成简短评论并给出评分**。
- 比较不同模型对同一音频的评价差异，观察是否存在一致偏好、极端评分或明显反常结果。
- 记录异常情况；例如 **Healer Alpha** 经常出现奇怪输出和报错，因此部分结果被标记为 **NA**。

## Results
- 文中**没有提供系统性的定量指标**，例如样本规模、平均分、方差、准确率或统计显著性，因此没有严格可复现的数值结论。
- 最具体的发现是若干模型偏好差异：**Gemini** 明显不喜欢 *Never Gonna Give You Up*，而 **voxtral** 则很喜欢它。
- **voxtral** 甚至喜欢“**指甲刮黑板**”这种作者刻意加入的糟糕声音样本，显示其审美判断可能与人类直觉显著偏离。
- 对 **Ye 的 Champion**，**Gemini** 评价偏低到中性，但作者称其对 **Yeezus** 时期作品评价更高。
- **Gemini Pro** 很讨厌 **Rebecca Black - Friday**；而较小版本模型却很喜欢它。对 **PSY - GANGNAM STYLE** 也出现类似分歧。
- 整体上，文章最强的结论是：当前支持音频的 LLM/多模态模型在**主观音乐评价**上表现出明显的**模型间差异、不稳定性与反常偏好**。

## Link
- [https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/](https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/)
