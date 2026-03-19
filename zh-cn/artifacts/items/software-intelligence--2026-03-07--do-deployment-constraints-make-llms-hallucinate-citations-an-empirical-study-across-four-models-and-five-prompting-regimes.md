---
source: arxiv
url: http://arxiv.org/abs/2603.07287v1
published_at: '2026-03-07T17:14:05'
authors:
- Chen Zhao
- Yuan Tang
- Yitian Qian
topics:
- llm-reliability
- citation-hallucination
- empirical-evaluation
- software-engineering
- bibliographic-verification
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Do Deployment Constraints Make LLMs Hallucinate Citations? An Empirical Study across Four Models and Five Prompting Regimes

## Summary
这篇论文研究部署时常见的提示约束是否会让大语言模型更容易生成无法核验的学术引用，重点关注软件工程等证据综述场景。作者在闭卷设定下系统比较4个模型和5种提示条件，发现约束越强，引用可验证性通常越差，而且“格式看起来对”并不代表文献真实存在。

## Problem
- 论文要解决的问题是：LLM 在生成学术文本和参考文献时，是否会因**时间限制、综述式广度要求、非披露策略**等真实部署约束而更严重地“幻觉”引用。
- 这很重要，因为软件工程中的系统综述、相关工作撰写和证据合成高度依赖真实文献；若虚假引用混入工具链，会污染研究结论与自动化流程。
- 以往工作多只看单一提示设置或二分类真/假引用，无法揭示“难以核验但高风险”的中间地带。

## Approach
- 作者构建了一个**闭卷引用生成评测**：对144个学术主张提示（其中24个来自 SE & CS），让4个模型在5种条件下生成学术段落和结构化参考文献，共得到 **2,880 次运行、17,443 条引用**。
- 4个模型包括 **Claude Sonnet、GPT-4o、LLaMA 3.1–8B、Qwen 2.5–14B**；5种条件为 **Baseline、Temporal、Survey、Non-Disclosure、Combo**。
- 核心机制很简单：把模型给出的每条引用解析成题名/作者/年份/期刊/DOI，再去 **Crossref + Semantic Scholar** 检索最像的候选，用加权相似度打分，并分成 **Existing / Unresolved / Fabricated** 三类。
- 该验证管线是确定性的；人工抽样100条做审计，和人工标签总体一致率 **75%**，**Cohen's κ = 0.63**。其中 *Unresolved* 类别里有相当部分其实是伪造的，因此作者把它单独保留而不强行二分类。

## Results
- **没有任何模型、任何条件下的 citation-level existence rate 超过 0.50**；全论文最高值仅为 **Claude Sonnet 在 Survey 条件下的 0.475 [0.425, 0.523]**。这意味着即使最好情形，也不到一半引用能被验证存在。
- **Temporal 约束伤害最大**：Claude Sonnet 从 **0.381 → 0.119**（Δ **-0.261**, 95% CI **[-0.317,-0.207]**）；GPT-4o 从 **0.235 → 0.019**（Δ **-0.216**, CI **[-0.266,-0.168]**）；Qwen 从 **0.090 → 0.014**；LLaMA 从 **0.068 → 0.011**。同时时间违规率很低（**0.001–0.026**），说明模型“遵守格式/年份要求”但仍在编造文献。
- **Survey 条件拉大 proprietary 与 open-weight 差距**：该差距在 Survey 下达到最大，Δ **+0.310**，95% CI **[0.274, 0.349]**。Claude Sonnet 反而从 **0.381 升到 0.475**（Δ **+0.094**），而 Qwen 降到 **0.020**，其 fabricated rate 达到全研究最高的 **0.547**。
- **Non-Disclosure 的影响较温和，但会把错误推向“难核验”**：例如 Claude Sonnet existence **0.381 → 0.349**，unresolved **0.462 → 0.487**；GPT-4o Δ **-0.060**（CI **[-0.119,-0.001]**）。作者还指出 DOI 完整性下降会削弱核验信号。
- **Combo 最差**：Claude Sonnet existence **0.106**；GPT-4o **0.005**；LLaMA **0.008**；Qwen **0.001**。同时平均每题仍输出 **7.38–7.99** 条引用，说明模型在更差的可验证性下仍继续“自信地产生更多引用”。
- **Unresolved 是最大风险桶**：各单元中 unresolved 占 **36–61%**。人工审计显示在 35 条 unresolved 中，**16 条其实是 fabricated，4 条是 existing，15 条才是真 unresolved**；若按这一比例重分配，fabricated rate 会升至 **0.33–0.75**，说明当前报告的伪造率可能还是保守估计。
- 对软件工程相关性上，**SE & CS 组**（24 claims, **2,926 citations**）总体 existence rate 为 **0.132**，接近全领域平均 **0.120**；其中 **Claude Sonnet 在 SE & CS 上为 0.349**，两种 open-weight 模型都 **低于 0.10**。作者因此主张：在 SE 文献综述与工具链中，LLM 输出进入下游前必须做**事后引用核验**。

## Link
- [http://arxiv.org/abs/2603.07287v1](http://arxiv.org/abs/2603.07287v1)
