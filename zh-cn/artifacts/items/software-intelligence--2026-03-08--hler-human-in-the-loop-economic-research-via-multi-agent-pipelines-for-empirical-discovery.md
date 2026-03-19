---
source: arxiv
url: http://arxiv.org/abs/2603.07444v1
published_at: '2026-03-08T03:40:34'
authors:
- Chen Zhu
- Xiaolu Wang
topics:
- multi-agent-systems
- human-in-the-loop
- economic-research
- dataset-aware-generation
- automated-scientific-workflows
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# HLER: Human-in-the-Loop Economic Research via Multi-Agent Pipelines for Empirical Discovery

## Summary
HLER 是一个面向经济学实证研究的人机协同多智能体流水线，目标是在保留关键人工把关的前提下自动化数据审计、选题、计量分析、写作与审稿。其核心贡献是“数据集感知”的问题生成和双反馈循环，从而减少空想式选题并提升端到端研究产出稳定性。

## Problem
- 现有“AI 科学家”式系统偏向全自动，但经济学/社会科学实证研究高度依赖**数据可行性、识别策略设计与人类判断**，纯文本生成很容易提出无法验证或不可信的问题。
- 不受约束的 LLM 选题常出现**幻觉式假设**：需要的数据变量不存在、研究设计与数据结构不匹配、或超出可支持的计量方法。
- 这很重要，因为实证研究的可信度取决于**数据验证、透明分析、可复现性和经济意义判断**，而不是只生成一篇看似合理的论文。

## Approach
- 提出一个**multi-agent pipeline**，由协调器串联 7 类专用代理：data-audit、data-profiling、question、data-collection、econometrics、paper、review。
- 核心机制是**dataset-aware hypothesis generation**：先做数据审计与统计画像，再让 LLM 在变量可用性、缺失模式、分布特征和数据结构约束下生成研究问题，避免脱离数据的空想。
- 设计了两个循环：**question quality loop**（生成→可行性筛选→人工选题）和 **research revision loop**（自动审稿→补充分析→改稿），让系统像真实研究一样迭代。
- 在关键节点加入**human decision gates**：人类研究者负责研究问题选择和最终发表批准，其他高重复工作尽量自动化。
- 计量执行由程序化统计库完成，支持 **OLS、fixed-effects、difference-in-differences、event-study**，LLM 主要负责规划、解释与写作。

## Results
- 在 **3 个数据集、14 次完整流水线运行**中，数据集感知选题生成了 **79** 个候选问题，其中 **69 个可行，成功率 87%**；无约束生成是 **82 个中 34 个可行，41%**。等价地，不可行比例从 **59% 降到 13%**。
- 无约束生成的主要失败原因中，**42%** 来自变量缺失，**35%** 来自研究设计与数据结构不兼容；这直接支持作者关于“数据约束能抑制幻觉式选题”的主张。
- 端到端完成率为 **12/14 = 86%**；失败的 **2 次** 都发生在固定效应估计对稀疏子样本的收敛问题上，系统可记录错误并安全停止。
- 修订循环中，**12 个完成运行**的平均审稿总分从初稿 **4.8** 提升到第一次修订 **5.9**，最终稿 **6.3**（1-10 分）；其中 **clarity +2.1**、**identification credibility +1.4**，而 **novelty 仅 +0.3**，说明循环主要提升表达与稳健性而非研究新颖性本身。
- 运行效率方面，单次完整流水线约 **20–25 分钟**，平均 API 成本 **$0.8–$1.5/次**；文中称这低于 AI Scientist 报告的 **$6–$15/篇**。
- CHNS 案例中：数据含 **285 变量、57,203 观测**；选题阶段 **8 个候选中 7 个可行**；分析样本 **19,466 观测**；稿件从 **5,563 词**经 **3 轮**修订增至 **7,282 词**，审稿总分从 **4.6** 升至 **6.5**，其中 identification **3.2→5.8**、clarity **4.1→6.9**。

## Link
- [http://arxiv.org/abs/2603.07444v1](http://arxiv.org/abs/2603.07444v1)
