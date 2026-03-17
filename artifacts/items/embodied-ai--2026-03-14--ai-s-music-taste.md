---
source: hn
url: https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/
published_at: '2026-03-14T23:57:07'
authors:
- caaaadr
topics:
- audio-understanding
- multimodal-llm
- model-evaluation
- music-preference
relevance_score: 0.03
run_id: materialize-outputs
---

# AI's Music Taste

## Summary
这篇文章不是正式学术论文，而是一篇有趣的实验性博客：作者让若干支持音频输入的大模型给不同歌曲写短评并打分，以观察“AI 的音乐品味”。它更像是定性对比与趣味案例汇总，而不是系统性的研究论文。

## Problem
- 探索音频多模态模型是否会对音乐形成可比较的“偏好”，并能否对歌曲进行评论与评分。
- 这个问题有趣之处在于：它测试了模型在开放式音频理解、主观评价和结构化输出上的能力。
- 但当前可用模型很少，因为需要同时支持**音频输入**和**结构化输出**，可测试范围受限。

## Approach
- 作者选取了一小批在 OpenRouter 上可用、且支持音频输入与结构化输出的模型进行评测。
- 对“大范围歌曲”输入音频，让模型生成**短评**并给出**评分**，再横向比较不同模型对同一首歌的反应。
- 结果主要通过趣味观察呈现，例如不同模型对流行歌曲、网络梗歌曲、甚至刻意难听声音的偏好差异。
- 作者还记录了异常情况：例如 Healer Alpha 经常输出奇怪结果或报错，因此部分结果被记为 NA。

## Results
- 文本摘录**没有提供系统性的量化指标**，如样本总数、平均分、相关系数、准确率或基准比较结果。
- 最强的具体结论是若干定性发现：**Gemini** 很讨厌 Rick Astley 的 *Never Gonna Give You Up*，而 **voxtral** 却很喜欢它。
- **voxtral** 甚至喜欢“**nails on a chalkboard**”这种故意设计的糟糕声音，显示其偏好可能与人类直觉明显不同。
- **Gemini** 对 Ye 的 *Champion* 观感偏差或一般，但对其 *Yeezus* 时期作品评价更高。
- **Gemini Pro** 明确“讨厌” Rebecca Black 的 *Friday*；而较小版本模型却似乎很喜欢它，对 PSY 的 *GANGNAM STYLE* 也出现类似分歧。
- **Healer Alpha** 经常产生异常输出和错误，导致部分结果为 **NA**，这表明模型稳定性本身也是实验中的显著观察点。

## Link
- [https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/](https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/)
