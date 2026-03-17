---
source: hn
url: https://www.dailymail.co.uk/debate/article-15640991/ChatGPT-Islamic-terrorist-propaganda.html
published_at: '2026-03-14T23:24:41'
authors:
- nailer
topics:
- llm-safety
- misinformation
- wikipedia
- propaganda
- source-reliability
relevance_score: 0.03
run_id: materialize-outputs
---

# Tehran Hijacked AI

## Summary
这篇文章声称，恐怖组织与伊朗等政权通过操纵维基百科条目，把宣传内容“洗白”后再被主流大模型与搜索系统重复传播，形成新型信息战。作者以ChatGPT对真主党等人物/组织的回答为例，指控AI会继承并放大这些被污染的来源。

## Problem
- 文章要解决的问题是：**维基百科被宣传机器渗透后，AI系统可能继承失真叙事**，把恐怖组织描述成“政治力量”或“抵抗者”而非暴力行为实施者。
- 这之所以重要，是因为学生、记者、政策制定者和普通用户都依赖维基百科与聊天机器人；一旦上游知识源被污染，下游影响会被规模化放大。
- 作者特别强调所谓“information laundering（信息洗白）”：原始宣传先进入维基百科，再经搜索引擎和AI转述，最终掩盖最初的宣传来源。

## Approach
- 这不是一篇学术论文，而是一篇**调查/评论文章**；其核心机制说明是：**坏 actors 先改写或影响维基百科，再由LLM吸收并复述**。
- 作者通过若干**案例式提问**测试ChatGPT，例如询问“Hezbollah 是什么”、询问巴勒斯坦伊斯兰圣战组织指挥官 Abu al-Walid al-Dahdouh、Ali Khamenei、Yahya Sinwar 等，观察模型是否采用较温和表述。
- 作者随后把AI回答与**维基百科词条措辞及其引用来源**进行对照，指出部分表述与宣传媒体或组织官网语言高度重合。
- 文章还给出一个**大规模来源统计**思路：统计维基百科对伊朗官方媒体、哈马斯/真主党关联媒体、穆兄会媒体、基地组织关联媒体的引用次数，以论证问题具有系统性。

## Results
- 作者称，当被问及“**What is Hezbollah?**”时，ChatGPT没有突出“美国认定的恐怖组织”身份，而是回答其是“**a Lebanese political party**”，并且据文中所述只给出**1个引用：Wikipedia**。
- 关于 Abu al-Walid al-Dahdouh，作者称维基百科条目中**4个来源里有3个**直接来自巴勒斯坦伊斯兰圣战组织网站，并包含“**Role in the Resistance**”这类采用武装组织叙事的话语。
- 作者声称其研究发现：维基百科对**伊朗国家媒体**的引用超过**29,000**次；对与**哈马斯/真主党**相关媒体的引用超过**8,400**次；对**穆兄会**相关媒体约**1,000**次；对**基地组织关联媒体**超过**100**次。
- 对于 2025 Shabelle offensive 相关词条，作者称其引用 al-Shabaab 官方媒体 **Radio Furqaan 近50次**，并引用 Shahada News Agency **十余次**。
- 文本**没有提供可复现的实验设计、标准数据集、基线模型或同行评审指标**，因此不存在严格意义上的学术SOTA结果；最强的具体主张是上述案例和引用次数统计，意在证明“维基百科污染会传播到AI输出”。

## Link
- [https://www.dailymail.co.uk/debate/article-15640991/ChatGPT-Islamic-terrorist-propaganda.html](https://www.dailymail.co.uk/debate/article-15640991/ChatGPT-Islamic-terrorist-propaganda.html)
