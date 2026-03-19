---
source: arxiv
url: http://arxiv.org/abs/2603.04317v1
published_at: '2026-03-04T17:37:05'
authors:
- Elan Barenholtz
topics:
- static-word-embeddings
- probing
- world-models
- distributional-semantics
- spatial-temporal-structure
relevance_score: 0.24
run_id: materialize-outputs
language_code: zh-CN
---

# World Properties without World Models: Recovering Spatial and Temporal Structure from Co-occurrence Statistics in Static Word Embeddings

## Summary
本文表明，仅由文本共现训练得到的静态词向量（GloVe、Word2Vec）中，已经能线性恢复出相当强的空间结构和较弱但稳定的时间结构。作者据此质疑：仅凭线性 probe 可解码性，并不能证明 LLM 学到了超越文本的“世界模型”。

## Problem
- 论文要解决的问题是：LLM 隐状态中可线性解码出的地理/时间信息，究竟说明模型形成了“世界模型”，还是这些结构本来就潜伏在文本共现统计里。
- 这很重要，因为很多关于“LLM 是否具备世界模型”的论证，依赖的正是 probe 能否从表示中读出空间和时间变量。
- 如果静态词嵌入也能做到类似解码，那么“能被线性读出”本身就不是足够强的证据。

## Approach
- 用与相关 LLM probing 工作相同类别的方法：对静态词向量 GloVe 6B 300d 和 Word2Vec Google News 300d 训练 ridge regression 线性探针。
- 在两个数据集上做预测：100 个世界城市的纬度、经度、气温等属性，以及 194 位历史人物的出生/死亡/中年年份。
- 用负对照检验选择性：同时预测海拔、GDP、人⼝等属性，看 probe 是否只是“什么都能读出来”。
- 做语义解释分析：计算词汇与城市向量的相似度，找出哪些词的分布最能跟纬度/温度/时代对齐。
- 做语义子空间消融：移除“国家名”“气候词”等 PCA 子空间，再看预测性能下降多少，并与同维度随机消融比较。

## Results
- 世界城市上，静态嵌入可恢复显著地理信号：纬度测试集 $R^2$ 为 0.709（GloVe）和 0.663（Word2Vec），经度为 0.782 和 0.866，温度为 0.471 和 0.617。
- 历史人物时间预测较弱但稳定：出生年份 $R^2$ 为 0.484（GloVe）和 0.521（Word2Vec）；死亡年份为 0.460 和 0.516；中年年份为 0.472 和 0.519，MAE 约 338–364 年，说明更多是“时代级”而非精确年代信号。
- 负对照显示并非任意世界属性都可线性恢复：GDP per capita 的 $R^2$ 最低到 -2.577，人口最低到 -2.960，海拔接近 0 或为负，说明信号具有选择性。
- 与 LLM 结果相比，作者引用 Llama-2-70B 在相关城市坐标任务上可达 $R^2=0.91$；虽然更高，但静态词向量已达到 0.71–0.87，足以说明“线性可解码”不能单独支持超越文本的表征结论。
- 语义分析显示信号可解释：如温暖城市更接近 *dengue*、*cyclone*、*tropical*（最高相关约 $r=+0.62$），寒冷城市更接近 *chemist*、*physicist*、*skiing*（最低约 $r=-0.67$）；cold–warm 复合分数与温度相关 $r=-0.79$、与纬度相关 $r=0.61$，modern–ancient 与出生年相关 $r=0.63$。
- 子空间消融提供更强证据：移除“国家名”20维子空间后，纬度 $R^2$ 下降 0.409（$z=25.9$），温度下降 0.420（$z=11.0$）；移除“气候与天气”19维子空间后，温度 $R^2$ 下降 0.639（$z=14.6$）；同时移除六类语义子空间后，纬度从 0.71 降到 0.27（下降 62%），温度从 0.47 降到 -0.83，而随机移除 105 维仅使纬度下降约 0.05。

## Link
- [http://arxiv.org/abs/2603.04317v1](http://arxiv.org/abs/2603.04317v1)
