---
source: hn
url: https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert
published_at: '2026-03-13T23:53:52'
authors:
- primenumber1
topics:
- spaced-repetition
- memory-modeling
- learning-schedule
- forgetting-curve
- educational-technology
relevance_score: 0.01
run_id: materialize-outputs
---

# Spaced Repetition Algorithm: A Three‐Day Journey from Novice to Expert

## Summary
这篇文章系统梳理了间隔重复算法从经验规则到记忆理论与数据驱动建模的发展脉络，核心目标是自动安排复习时间以在较少复习成本下保持记忆。它更像一篇教程/综述与研究导引，而不是单篇提出新实验结果的论文。

## Problem
- 要解决的问题是：**如何估计人已经忘了多少、忘得多快，并据此安排“最佳复习间隔”**，以减少遗忘同时避免过度复习。
- 这很重要，因为人工跟踪大量知识点几乎不可能；每条记忆的遗忘曲线和难度不同，错误排程会导致要么学得低效，要么快速遗忘。
- 文章还强调，复习频率与遗忘率之间存在张力：复习太少会忘，复习太勤也未必高效。

## Approach
- 从最早的**经验算法**讲起：SM-0 用人工实验找近似最优间隔；SM-2 引入逐卡片调度与 Ease Factor；SM-4 用 Optimal Interval Matrix 让新卡从相似旧卡的数据中受益。
- 提出更一般的**三状态记忆模型 DSR**：Difficulty（难度）、Stability（稳定性）、Retrievability（可提取性/回忆概率），把记忆表示为“多难、能撑多久、当前想起概率多大”。
- 用**遗忘曲线**近似为负指数函数，说明复习后稳定性会变化；稳定性提升受当前稳定性、回忆概率和材料难度共同影响。
- 通过**记忆事件数据**（谁、何时、复习什么、答对/答错、耗时、历史序列等）估计 DSR 状态，再用这些状态去模拟不同排程策略下的长期学习过程。
- 进一步构建**SRS 仿真器**，在“总时长限制+每日学习时间限制+有限卡片集合”下，比较不同调度器的长期效率。

## Results
- 文中引用外部研究表明，间隔重复优于集中练习：Rea & Modigliani 1985 中，分散练习组即时测试**70%** 正确率，对比集中练习组 **53%**。
- 文中引用 Donovan & Radosevich 1999 的元分析：平均加权效应量 **0.46**，95% CI **[0.42, 0.50]**；作者将其解释为约 **62%–64%** 的间隔重复用户会优于集中复习用户。
- 在 Wozniak 的早期实验中，第二次复习候选间隔 **2/4/6/8/10 天**对应遗忘率 **0%/0%/0%/1%/17%**，据此选 **7 天**；后续又得到第三次复习约 **16 天**、第四次约 **35 天** 的经验间隔。
- SM-0 的固定序列被总结为 **1, 7, 16, 35 天**，之后大致按前一间隔的 **2 倍**增长，体现“记得越稳，间隔越长”的经验规律。
- 文中给出一个重要理论性结论：**期望稳定性提升**在保留率约 **30%–40%** 时达到最大，但作者也明确指出这**不等于**整体学习速率最优。
- 没有给出该教程/摘录自身在标准基准数据集上的统一新 SOTA 数字；更强的具体主张是：DSR 模型和后续仿真框架可把事件日志转成记忆状态，并用于优化排程。

## Link
- [https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert](https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert)
