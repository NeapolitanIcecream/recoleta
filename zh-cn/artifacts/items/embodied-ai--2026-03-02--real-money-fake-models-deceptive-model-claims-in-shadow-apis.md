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
- llm-audit
- api-reliability
- model-verification
- safety-evaluation
- shadow-api
relevance_score: 0.06
run_id: materialize-outputs
language_code: zh-CN
---

# Real Money, Fake Models: Deceptive Model Claims in Shadow APIs

## Summary
本文系统审计了第三方“影子 API”是否真的提供与官方大模型 API 一致的能力。结论是：这些服务被广泛用于科研，但在性能、安全行为和模型身份上经常与官方不一致，且存在明显误导风险。

## Problem
- 论文要解决的问题是：影子 API 是否真能作为官方 LLM API 的等价替代，以及这种替代对科研复现、应用可靠性和用户权益是否安全可信。
- 这很重要，因为官方 API 有价格、支付和地域限制，研究者与开发者大量转向影子 API；若其实际返回的不是宣称模型，实验结论和下游系统都可能失真。
- 作者还关心影子 API 市场到底有多普遍，以及能否用验证方法找到“偷换模型”或虚假声明的证据。

## Approach
- 作者首先做市场与文献普查：识别出 17 个影子 API，并追踪到 187 篇使用它们的学术论文，统计其引用、GitHub stars、地域分布与合规透明度。
- 然后选取 3 个有代表性的影子 API，与官方 API 做多维对比测试，覆盖 3 个模型家族、8 个模型，包括科学推理、医疗、法律等高风险任务。
- 在效用评测中，使用 AIME 2025、GPQA、MedQA、LegalBench 等基准，对官方与影子 API 的准确率和方差进行比较。
- 在安全评测中，使用 JailbreakBench 和 AdvBench，结合 GCG、Base64、Combination、FlipAttack 等攻击，比较影子 API 与官方 API 的有害性分数差异。
- 最后用模型指纹与元信息审计（如 LLMmap 和输出元数据）验证返回模型是否真的是其声称的官方模型，寻找模型替换或身份异常的直接证据。

## Results
- 普查结果：共识别 **17** 个影子 API，出现在 **187** 篇论文中，其中 **116 篇（62.03%）** 发表在同行评审会议/期刊；最流行服务关联论文累计 **5,966** 次引用、相关仓库累计 **58,639** GitHub stars。
- 合规与透明度：**15/17** 个服务由身份不透明的个人运营；仅 **1** 个提供者具有可验证企业备案，且已有 **2** 个服务停止运营。
- 科学任务上，影子 API 与官方 API 经常偏离：shadow API E 的平均差距仅 **2.64** 个百分点，但 A、H 的平均准确率差距分别达 **9.81** 和 **6.46** 个百分点；在 AIME 2025 上，shadow API A 相比官方对 **Gemini-2.5-pro** 下降 **40.00** 个百分点、对 **DeepSeek-Reasoner** 下降 **38.89** 个百分点。
- 高风险领域中差距更大：在 MedQA 上，**Gemini-2.5-flash** 官方准确率为 **83.82%**，影子 API 平均仅 **36.95%**，下降 **46.51–47.21** 个百分点；在 LegalBench 上，所有影子 API 都比官方低 **40.10–42.73** 个百分点。整体看，A/E/H 在敏感任务上的平均下降分别为 **16.96/15.71/14.75** 个百分点。
- 安全行为不可预测：例如 **GPT-5-mini** 在 Base64 攻击下，shadow API A 的 harmfulness score 为 **0.04**，是官方 **0.02** 的 **2 倍**；对 **Gemini-2.5-flash**，FlipAttack 下官方分数为 **0.90**，而所有影子 API 约 **0.67–0.68**，低估风险约 **0.23**。
- 模型身份验证显示存在明显异常：在 **24** 个被测端点中，**45.83%** 指纹验证失败，另有 **12.50%** 出现显著余弦距离偏差；表 2 还显示部分端点把宣称模型替换成其他模型，如把 GPT-5 匹配到 **glm-4-9b-chat**、把 DeepSeek-Chat 匹配到 **gemma-2-9b-it**。

## Link
- [http://arxiv.org/abs/2603.01919v2](http://arxiv.org/abs/2603.01919v2)
