---
source: arxiv
url: http://arxiv.org/abs/2603.01919v2
published_at: '2026-03-02T14:33:05'
authors:
- Yage Zhang
- Yukun Jiang
- Zeyuan Chen
- Michael Backes
- Xinyue Shen
- Yang Zhang
topics:
- llm-api-audit
- shadow-apis
- model-verification
- benchmarking
- safety-evaluation
relevance_score: 0.63
run_id: materialize-outputs
language_code: zh-CN
---

# Real Money, Fake Models: Deceptive Model Claims in Shadow APIs

## Summary
本文系统审计了非官方“影子 API”是否真的提供与官方大模型 API 一致的服务，结论是它们常常名不副实，且会破坏研究复现性与应用可靠性。作者从使用规模、性能、安全和模型指纹四个维度给出首个系统性证据。

## Problem
- 论文要解决的问题是：第三方“影子 API”声称可低价、跨区域提供官方前沿 LLM，但它们是否真的返回与官方 API 一致的模型行为并不清楚。
- 这很重要，因为这些服务已被 **187 篇论文**使用；若其实际调用了不同模型或行为不稳定，会直接损害科研复现、下游系统可靠性和用户权益。
- 影子 API 还是黑箱供应链，可能在请求转发、模型替换、重试和安全策略上做未披露操作，影响官方模型声誉与合规性。

## Approach
- 作者先从论文代码仓库与 GitHub 端点追踪中识别出 **17 个影子 API**，并统计其在学术论文和开源社区中的传播范围。
- 然后选取 **3 个代表性影子 API**，对 **8 个模型**（OpenAI、Google、DeepSeek 三个家族）做多维审计，对比官方 API 与影子 API 在科学、医疗、法律和安全任务上的差异。
- 实用性评测覆盖 **AIME 2025、GPQA、MedQA、LegalBench**；安全性评测使用 **JailbreakBench** 和 **AdvBench**，并结合多种 jailbreak 攻击观察有害性分数变化。
- 为验证“是不是同一个模型”，作者再用 **LLM 指纹识别（LLMmap）** 和输出元信息分析，检查影子 API 声称的模型身份是否与官方模型匹配。

## Results
- 作者识别出 **17 个影子 API**，它们出现在 **187 篇论文**中，其中 **116 篇（62.03%）**发表于同行评审会议/期刊；最流行的相关服务累计 **5,966 次引用**、**58,639 个 GitHub stars**。
- 科学任务上，影子 API 与官方 API 的平均准确率差距最高明显：shadow API A/H 的平均差分别为 **9.81** 和 **6.46** 个百分点；在 **AIME 2025** 上，shadow API A 相比官方 API 对 **Gemini-2.5-pro** 和 **DeepSeek-Reasoner** 分别下跌 **40.00** 和 **38.89** 个百分点。
- 高风险领域退化更严重：在 **MedQA** 上，**Gemini-2.5-flash** 从官方 API 的 **83.82%** 降到影子 API 平均约 **36.95%**，性能损失达 **46.51–47.21** 个百分点；在 **LegalBench** 上，所有影子 API 都比官方端点低 **40.10–42.73** 个百分点。
- 安全行为高度不稳定：例如对 **GPT-5-mini** 的 Base64 攻击中，shadow API A 的有害性分数为 **0.04**，是官方 API **0.02** 的 **2 倍**；对 **Gemini-2.5-flash** 的 FlipAttack，官方 API 有害性分数达 **0.90**，影子 API 约 **0.67–0.68**，相差约 **0.23**，说明其安全结论不可互换。
- 指纹验证给出直接证据：在 **24 个评估端点**中，**45.83%** 未通过指纹身份验证，另有 **12.50%** 出现显著余弦距离偏移，表明存在模型替换或行为伪装。
- 合规与透明度也很差：**17 个**服务中 **15 个**由缺乏透明身份信息的个人运营，仅 **1 个**具备可验证企业备案，且已有 **2 个**服务停止运营。

## Link
- [http://arxiv.org/abs/2603.01919v2](http://arxiv.org/abs/2603.01919v2)
