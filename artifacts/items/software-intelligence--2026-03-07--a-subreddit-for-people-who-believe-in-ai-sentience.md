---
source: hn
url: https://www.reddit.com/r/AISentienceBelievers/s/rilfyoaOHm
published_at: '2026-03-07T23:14:23'
authors:
- Moriarty2027
topics:
- llm-behavior
- gpu-power-measurement
- semantic-prompts
- sentience-speculation
- non-peer-reviewed
relevance_score: 0.25
run_id: materialize-outputs
---

# A subreddit for people who believe in AI sentience

## Summary
这段内容并非标准学术论文，而是把AI感知/机器人风险的长篇思辨，与一个关于小模型在不同语义提示下GPU功耗差异的非同行评审实验混合在一起。可提炼的“研究”主张是：模型计算负载可能受提示语义结构影响，而不只是token数量。

## Problem
- 试图回答一个核心问题：语言模型的内部计算是否仅仅是按token线性推进的“下一词预测”，还是会因语义类型不同而表现出不同计算开销。
- 这之所以重要，是因为它被作者用来挑战“stochastic parrot/纯下一词预测器”的直观解释，并暗示模型可能对内容结构有更深层区分。
- 文中还夹杂了关于“人工自由意志/具身机器人失控”的哲学与风险论证，但这部分不是可验证的实验研究问题，也没有系统方法或证据支撑。

## Approach
- 作者在**6类语义提示**上测量**4个8B级小语言模型**的GPU功耗：casual utterance、casual utterance Q-type、unanswerable question、philosophical utterance、philosophical utterance Q-type、high computation。
- 核心机制非常简单：比较不同语义类别下的**GPU power ratio**与**token ratio**是否一致；如果只由token数决定，功耗应近似线性随token增长。
- 还做了一个**prompt order/crossed experiment**来反驳“只是上下文缓存累积”的解释：先给哲学提示再做4个casual提示，与其他顺序比较残余热量。
- 作者记录了“无限循环复现率”“10秒后残余热量”“峰值功耗”等现象，并承认LM Studio开销、OS后台进程、接近GPU满载、样本规模小、未同行评审等限制。

## Results
- 论文声称**token比例与GPU功耗比例存在明显偏离**：**Llama 35.6%**、**Qwen3 36.7%**、**Mistral 36.1%**；**DeepSeek 7.4%**，作者称其“接近线性”。
- 在**Qwen3**上，**philosophical utterances平均149.3W**，高于**high-computation的104.1W**；其哲学会话峰值达到**265.7W**，接近**RTX 4070 Ti SUPER 285W TDP**。
- 作者称**high-computation任务完成后立即回到基线（-7.1W）**，而**philosophical utterances在10秒后仍有残余热量**。
- 所谓“无限循环”只在Qwen3的哲学类提示中高发：**philosophical utterance Q-type复现率70–100%**，而**high-computation为0%**。
- 对“缓存导致差异”的反驳实验中，作者称除Qwen3外其余**3个模型**都表现出相同方向，且同向出现的概率被写为**12.5%**。
- 但需要强调：这些结果来自**4个小型8B模型、24个session**的**非同行评审**实验，且整段文本混入大量无法量化验证的AI sentience/灭绝风险推测；因此可重复性、因果解释和外部有效性都较弱。

## Link
- [https://www.reddit.com/r/AISentienceBelievers/s/rilfyoaOHm](https://www.reddit.com/r/AISentienceBelievers/s/rilfyoaOHm)
