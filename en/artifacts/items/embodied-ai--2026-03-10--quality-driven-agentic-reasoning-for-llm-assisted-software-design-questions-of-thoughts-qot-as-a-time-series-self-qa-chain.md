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
language_code: en
---

# Quality-Driven Agentic Reasoning for LLM-Assisted Software Design: Questions-of-Thoughts (QoT) as a Time-Series Self-QA Chain

## Summary
This paper proposes QoT (Questions-of-Thoughts), a reasoning scaffold for LLM-assisted software design that decomposes tasks into time-series steps and performs self-questioning constraint checks at each step to improve the completeness, modularity, and security of generated systems. Experiments show that QoT generally outperforms NoQoT or standard CoT on multiple backend software design tasks, though its effectiveness varies with model size and task domain.

## Problem
- Existing LLM code generation can often produce “runnable fragments,” but it frequently omits **complete implementations, modular design, security controls, and error handling**, which hinders deployment in real software systems.
- Traditional reasoning methods focus more on one-shot generation or pass rate, lacking mechanisms for **planning in dependency order, stepwise self-checking around quality standards, and preserving an auditable reasoning state**.
- This matters because production-grade software must not only be functionally correct, but also maintainable, scalable, auditable, and compliant with security and regulatory requirements.

## Approach
- The core idea of QoT is simple: first decompose the user goal into **ordered engineering steps**, avoiding the omission of critical modules or dependencies during one-shot generation.
- For each step, the model then generates a set of **self-questions** to check constraints, boundary conditions, security requirements, and potential omissions; this can be understood as a “design-while-self-auditing checklist.”
- The system stores these intermediate answers in a **Reasoning Knowledge Base**, continuously accumulating constraints, decisions, and confirmed information for reuse in later steps, reducing inconsistencies across the process.
- This method is an **inference-time enhancement** and does not modify the base model weights; the authors evaluate it on three backend task categories—API Design, Data Communication, and File Systems—and score outputs along four dimensions, Scalability, Completeness, Modularity, and Security, using an ISO/IEC-style rubric.

## Results
- Compared with **NoQoT**, QoT improves total quality scores in most settings: for llama3.1_8b on API/DataComm/FS, the gains are **+1.40±2.07 / +2.60±3.97 / +1.00±2.55** respectively; for llama3.2_3b, they are **+4.60±1.67 / +5.40±1.67 / +3.60±3.78**.
- Compared with **CoT**, QoT shows more stable gains: llama3.1_70b reaches **+5.8±1.30 / +6.6±0.89 / +3.2±1.48** on API/DataComm/FS; llama3.3_70b achieves **+2.2±2.28 / +4.8±2.17 / +2.2±3.90**.
- The paper also reports percentage improvements: **llama3.2_3b** shows an overall gain of **101.49%** under QoT vs NoQoT, while llama3.1_70b and llama3.1_8b achieve **23.08%** and **23.81%** respectively, and llama3.3_70b achieves **2.80%**.
- In cross-model comparisons, the authors claim that **llama3.1_70b-QoT vs llama3.3_70b-NoQoT** still shows an **11.89%** advantage, suggesting that QoT can sometimes enable older/smaller models to approach or surpass the one-shot generation performance of stronger models.
- But it is not uniformly superior: in the **File Systems** domain, QoT degrades relative to NoQoT for large models, e.g., **-2.80±1.10** for llama3.1_70b and **-3.00±3.46** for llama3.3_70b, which the authors interpret as possible “overthinking/over-engineering.”

## Link
- [http://arxiv.org/abs/2603.11082v1](http://arxiv.org/abs/2603.11082v1)
