---
source: arxiv
url: http://arxiv.org/abs/2603.05786v1
published_at: '2026-03-06T00:34:14'
authors:
- Xisen Jin
- Michael Duan
- Qin Lin
- Aaron Chan
- Zhenglun Chen
- Junyi Du
- Xiang Ren
topics:
- ai-agents
- trusted-execution-environments
- remote-attestation
- guardrails
- agent-safety
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Proof-of-Guardrail in AI Agents and What (Not) to Trust from It

## Summary
This paper proposes **proof-of-guardrail**: using TEE remote attestation to let AI agent developers cryptographically prove that “a particular open-source guardrail was indeed executed when generating this response.” It addresses **verifiability of guardrail execution**, not “actual safety,” and explicitly warns against mistaking it for a proof of safety.

## Problem
- Remotely deployed AI agents often claim to have safety guardrails, but users usually **cannot verify** whether the guardrail actually ran, was modified, or was bypassed.
- At the same time, developers are unwilling to disclose the full agent implementation (such as the system prompt or private logic), so traditional public auditing or third-party auditing is unrealistic in decentralized settings.
- This matters because agents may handle sensitive data, make high-stakes recommendations, call tools, or even generate/execute code; **false safety claims** can directly mislead user trust.

## Approach
- The core idea is simple: run the **open-source guardrail + wrapper program** inside a **TEE**, and let the hardware/cloud platform generate a **signed attestation** showing that this known code did in fact run.
- The wrapper program `f` contains the public guardrail `g`, intercepting the agent’s inputs, outputs, and tool calls; the private agent `A` is loaded as secret input, so it **can prove guardrail execution without exposing the agent’s private implementation**.
- For each user input `x`, the system returns a response `r` and attestation `σ`; the proof includes the program measurement `m` and a hash commitment to `(x, r)` or `r`, allowing users to **verify offline** the signature, code version, and response-binding relationship.
- The authors implement an end-to-end system on **OpenClaw + AWS Nitro Enclaves**, and test both a content-safety guardrail (Llama Guard 3) and a fact-checking guardrail (Loki).
- The mechanism can prove that “the guardrail was executed,” but **cannot prove that the guardrail is strong enough**: if the guardrail itself makes mistakes, can be jailbroken, or the wrapper program has vulnerabilities, the system may still produce unsafe responses.

## Results
- **Attack detection**: all 3 types of simulated attacks were identified during verification — modified guardrail code detected successfully **10/10**; tampered attestation bytes **100/100**; tampered response `r` **100/100**.
- **Latency overhead**: TEE deployment increases latency by about **25%–38%** relative to the non-TEE baseline. The paper summarizes the average as about **34%**. For example: on ToxicChat, Llama Guard 3 latency is **546.7ms vs 421.2ms（+29.7%）**; response generation **2828ms vs 2050ms（+38.0%）**.
- **Fact-checking scenario**: on FacTool-KBQA, the Loki guardrail is **20408ms vs 15964ms（+27.8%）**; response generation **2408ms vs 1930ms（+24.8%）**.
- **Proof overhead is small**: attestation generation averages **97.8ms ± 4.2**; client-side verification is only **5.1ms**.
- **Deployment cost is higher**: the TEE-based **m5.xlarge costs $0.192/hour**, while a normal **t3.micro costs $0.0104/hour**, about an **18.5×** cost increase.
- **Not a safety-breakthrough metric**: guardrail accuracy itself is not perfect. Llama Guard3 has **F1=0.56** for the Unsafe class; Loki has **F1=0.76** for Non-Factual and **F1=0.67** for Factual. Therefore, the paper’s strongest claim is **verifiable integrity of guardrail execution**, not proof that the agent is truly safe.

## Link
- [http://arxiv.org/abs/2603.05786v1](http://arxiv.org/abs/2603.05786v1)
