---
source: hn
url: https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert
published_at: '2026-03-13T23:53:52'
authors:
- primenumber1
topics:
- spaced-repetition
- memory-modeling
- learning-optimization
- review-scheduling
- educational-ai
relevance_score: 0.13
run_id: materialize-outputs
language_code: zh-CN
---

# Spaced Repetition Algorithm: A Three‐Day Journey from Novice to Expert

## Summary
这篇文章系统讲解了间隔重复算法如何从经验规则演化到基于记忆状态建模的数据驱动方法，用于自动安排复习时间以提高长期记忆效率。它更像一篇研究教程/综述，而非单一实验论文，但明确给出了SM-0、SM-2、SM-4与DSR记忆模型的核心思想。

## Problem
- 解决的问题是：**如何自动估计人的遗忘状态，并为每条学习材料安排最优复习间隔**，以在有限时间内尽量少忘记。
- 这很重要，因为人工跟踪大量知识点的遗忘曲线几乎不可能，而错误的复习安排会导致**要么忘得太多，要么复习负担过重**。
- 文章还强调，不同材料难度不同、不同记忆稳定性不同，统一固定间隔无法有效适配真实学习过程。

## Approach
- 从最早的**经验算法**讲起：SM-0通过实验寻找“在遗忘率受控时尽可能长”的复习间隔，得到近似倍增的间隔序列，如1、7、16、35天。
- SM-2进一步把材料拆成**独立卡片**，并引入**Ease Factor（容易度）**，根据每次回忆质量动态调整下次间隔；简单说，就是“记得轻松就拉长间隔，忘了就重置或缩短”。
- SM-4再引入**Optimal Interval Matrix**，不再只看单卡，而是让“相似难度、相似复习次数”的卡片共享统计信息，从群体经验中更新最优间隔。
- 在理论层面，文章提出/强调**DSR三要素记忆模型**：Difficulty、Stability、Retrievability。最核心机制是：用“当前能否回忆的概率 + 记忆衰减速度 + 材料难度”来描述记忆状态，并用这些状态预测复习效果。
- 基于上述模型，可以把用户的记忆事件日志转成记忆状态，再通过仿真器在“总时长、每日学习时长、材料集合”等约束下比较不同调度器的学习效率。

## Results
- 文章引用外部研究证明间隔重复优于集中练习：Rea & Modigliani 1985中，**分散练习组正确率70%，集中练习组53%**。
- 引用Donovan & Radosevich 1999元分析：总体加权效应量**0.46**，95%置信区间**[0.42, 0.50]**，说明间隔练习显著优于集中练习；文中解释为约**62%–64%**的使用者会优于集中练习者。
- Wozniak早期实验中，第二次复习测试不同间隔的遗忘率分别为：**2/4/6/8/10天对应0%/0%/0%/1%/17%**，据此选出约**7天**作为较优间隔。
- 第三次复习实验中，**6/8/11/13/16天对应遗忘率3%/0%/0%/0%/1%**，选择了**16天**；第四次复习中，**20/24/28/33/38天对应0%/3%/5%/3%/0%**，选择约**35天**。
- 基于这些实验，SM-0形成序列：**I(1)=1天，I(2)=7天，I(3)=16天，I(4)=35天，之后近似翻倍**；作者称其仿真表明：**总知识量长期增加，长期学习速率相对稳定**。
- 理论分析中还给出一个强结论：**期望稳定性增益在保留率约30%–40%时达到最大**。不过文中也明确说，这并不等价于整体学习速度最优，真正最优调度要看后续更正式的优化算法；本文摘录未给出统一基准上的最终SOTA定量对比。

## Link
- [https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert](https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert)
