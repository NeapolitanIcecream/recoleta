---
source: arxiv
url: http://arxiv.org/abs/2603.11082v1
published_at: '2026-03-10T23:49:09'
authors:
- Yen-Ku Liu
- Yun-Cheng Tsai
topics:
- llm-software-engineering
- agentic-reasoning
- inference-time-scaffolding
- self-questioning
- code-generation-evaluation
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Quality-Driven Agentic Reasoning for LLM-Assisted Software Design: Questions-of-Thoughts (QoT) as a Time-Series Self-QA Chain

## Summary
本文提出 QoT（Questions-of-Thoughts），一种面向 LLM 辅助软件设计的推理脚手架，把任务拆成时间序列步骤，并在每一步做自问自答式约束检查，以提升生成系统的完整性、模块化和安全性。实验表明，QoT 在多个后端软件设计任务上通常优于无 QoT 或普通 CoT，但效果会随模型规模与任务域而变化。

## Problem
- 现有 LLM 代码生成常能写出“能跑的片段”，但在**完整实现、模块化设计、安全控制、错误处理**上经常遗漏，这会阻碍真实软件落地。
- 传统推理方式更关注一次性生成或 pass rate，缺少**按依赖顺序规划、围绕质量标准逐步自检、保留可审计推理状态**的机制。
- 这很重要，因为生产级软件不仅要功能正确，还要可维护、可扩展、可审计，并满足安全与合规要求。

## Approach
- QoT 的核心很简单：先把用户目标拆成**有顺序的工程步骤**，避免一口气生成时漏掉关键模块或依赖。
- 对每个步骤，模型再生成一组**自我提问**，用于检查约束、边界条件、安全要求和潜在遗漏；可理解为“边设计边自查清单”。
- 系统把这些中间答案存入一个**Reasoning Knowledge Base**，持续累积约束、决策和已确认信息，供后续步骤复用，减少前后不一致。
- 该方法是**推理时增强**，不改基础模型权重；作者在 API Design、Data Communication、File Systems 三类后端任务上评估，并用 ISO/IEC 风格 rubric 对 Scalability、Completeness、Modularity、Security 四维打分。

## Results
- 相比 **NoQoT**，QoT 在多数设置上提升总质量分：llama3.1_8b 在 API/DataComm/FS 上分别为 **+1.40±2.07 / +2.60±3.97 / +1.00±2.55**；llama3.2_3b 为 **+4.60±1.67 / +5.40±1.67 / +3.60±3.78**。
- 相比 **CoT**，QoT 的提升更稳定：llama3.1_70b 在 API/DataComm/FS 上达到 **+5.8±1.30 / +6.6±0.89 / +3.2±1.48**；llama3.3_70b 为 **+2.2±2.28 / +4.8±2.17 / +2.2±3.90**。
- 论文还报告百分比改进：**llama3.2_3b** 在 QoT vs NoQoT 下总体提升 **101.49%**，llama3.1_70b 和 llama3.1_8b 分别为 **23.08%**、**23.81%**，llama3.3_70b 为 **2.80%**。
- 跨模型比较中，作者声称 **llama3.1_70b-QoT vs llama3.3_70b-NoQoT** 仍有 **11.89%** 优势，说明 QoT 有时能让旧/小模型逼近或超过更强模型的单次生成。
- 但并非全胜：在 **File Systems** 域，QoT 相对 NoQoT 对大模型出现退化，如 llama3.1_70b 为 **-2.80±1.10**、llama3.3_70b 为 **-3.00±3.46**，作者将其解释为可能的“过度思考/过度工程化”。

## Link
- [http://arxiv.org/abs/2603.11082v1](http://arxiv.org/abs/2603.11082v1)
