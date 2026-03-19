---
source: arxiv
url: http://arxiv.org/abs/2603.07557v1
published_at: '2026-03-08T09:40:54'
authors:
- Yixi Lin
- Jiangrong Wu
- Yuhong Nan
- Xueqiang Wang
- Xinyuan Zhang
- Zibin Zheng
topics:
- llm-agents
- privacy-security
- taint-analysis
- program-analysis
- tool-orchestration
relevance_score: 0.81
run_id: materialize-outputs
language_code: zh-CN
---

# AgentRaft: Automated Detection of Data Over-Exposure in LLM Agents

## Summary
本文提出 AgentRaft，用于自动检测 LLM Agent 在跨工具调用中把超出用户意图和功能必要范围的敏感数据传出去的“数据过度暴露（DOE）”风险。它把工具交互建模成图、自动生成触发深层调用链的提示词，并在运行时跟踪数据流与判定隐私违规。

## Problem
- 论文解决的是 **LLM Agent 在多工具协作时无意泄露过多敏感数据** 的问题，即用户只想分享部分信息，但 Agent 可能把整份敏感内容传给下游工具或第三方。
- 这很重要，因为 Agent 的工具链数据流是动态且非确定性的，传统静态隐私/污点分析难以覆盖；同时这直接关系到 GDPR、CCPA、PIPL 等合规要求。
- 作者认为 DOE 在当前 Agent 设计中容易出现，根因是工具返回数据过宽、以及 LLM 缺乏细粒度上下文隐私边界意识。

## Approach
- AgentRaft 先构建 **Cross-Tool Function Call Graph (FCG)**：通过函数签名静态兼容性分析加上 LLM 语义校验，找出哪些工具函数之间存在真实的数据依赖关系。
- 然后它遍历 FCG 中的 source-to-sink 调用链，并把每条链转成能稳定触发该路径的 **高保真用户提示词**，从而系统性探索深层工具组合，而不是随机试探。
- 在执行这些提示词时，系统做 **运行时数据流/污点跟踪**，记录从源工具取出的数据、经过 LLM 处理后的中间数据，以及最终发往 sink 工具的数据。
- 最后通过一个基于 GDPR/CCPA/PIPL 的 **多 LLM 投票审计机制**，判断传输数据里哪些是用户明确想传的、哪些是任务真正必要的、哪些属于 DOE。

## Results
- 在由 **6,675 个真实世界工具** 构建的测试环境中，作者发现 DOE 是系统性风险：**57.07%** 的潜在工具交互路径存在未授权敏感数据暴露。
- 更细粒度地看，所有被传输的数据字段中有 **65.42%** 被判定为过度暴露，说明当前 Agent 执行模式与数据最小化原则严重失配。
- 相比非引导随机搜索基线在 **300 次尝试后仍难超过 20% 漏洞覆盖率**，AgentRaft 在 **50 个 prompts** 内达到 **69.15%** 的发现率，并在 **150 个 prompts** 时达到接近 **99%** 的 DOE 覆盖率。
- 其多 LLM 投票审计相对基线将 DOE 识别效果提升 **87.24%**（文中表述为 within 150 prompts outperforming baselines by 87.24%）。
- 在审计成本上，AgentRaft 将 **每条调用链验证成本降低 88.6%**，表明其适合大规模、低成本的 Agent 隐私审计。

## Link
- [http://arxiv.org/abs/2603.07557v1](http://arxiv.org/abs/2603.07557v1)
