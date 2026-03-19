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
- ai-agent-safety
- trusted-execution-environment
- remote-attestation
- guardrails
- verifiable-inference
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Proof-of-Guardrail in AI Agents and What (Not) to Trust from It

## Summary
This paper proposes Proof-of-Guardrail: enabling remote AI agents to use a TEE to generate cryptographic proofs that can be verified offline, proving that a specific open-source guardrail was indeed executed before generating a response. It also emphasizes that such proof can only show that the guardrail was executed, not that the system is actually safe.

## Problem
- Problem addressed: when users interact with remotely deployed AI agents, they usually can only trust the developer’s claim that a safety guardrail is being used, but cannot verify whether that guardrail actually ran, was replaced, or was bypassed.
- This matters because agents are increasingly handling sensitive information, high-stakes recommendations, and automatic tool calls; once safety measures are falsely advertised, users may accept dangerous outputs under misplaced trust.
- Existing approaches either require disclosing the agent implementation (unrealistic, since system prompts and implementations are private assets) or rely on third-party auditing (often impractical in cross-platform and decentralized settings).

## Approach
- Core mechanism: run the open-source guardrail and wrapper inside a Trusted Execution Environment (TEE), which performs hardware-level measurement of the actual code being run and produces a signed remote attestation.
- The developer’s private agent is loaded into the same protected environment as secret input; this lets users verify that the guardrail code was indeed executed without exposing implementation details of the private agent.
- For each user input x, the system generates a response r, and includes in the attestation the code measurement m and a hash commitment to the input/output, d=Hash(x,r) (or an implementation variant that binds only r); users can verify offline that the signature, measurement, and hash all match.
- The authors implement the system on the OpenClaw agent, deploy it on AWS Nitro Enclaves, and integrate a content-safety guardrail (Llama Guard 3) and a fact-checking guardrail (Loki), demonstrating an end-to-end chatbot scenario.
- The paper explicitly states the boundary: the method guarantees the integrity of guardrail execution, not that the guardrail is strong enough or that the agent’s true safety against jailbreaks/bypasses is guaranteed.

## Results
- End-to-end feasibility: implemented on OpenClaw + AWS Nitro Enclaves, with a Telegram bot that can return attestation on demand and support offline user verification.
- All simulated attacks were detected: when the guardrail code was modified, measurement mismatch detected 10/10; when attestation bytes were tampered with, signature failure detected 100/100; when the response r was tampered with, input/output hash mismatch detected 100/100.
- Latency overhead is generally acceptable: the paper summarizes in the introduction an average additional latency of about **34%**. By component, on ToxicChat Llama Guard 3 latency is **546.7ms vs 421.2ms (+29.7%)**, and response generation is **2828ms vs 2050ms (+38.0%)**; on FacTool-KBQA Loki verification is **20408ms vs 15964ms (+27.8%)**, and response generation is **2408ms vs 1930ms (+24.8%)**.
- Proof generation/verification cost is low: attestation generation adds **97.8±4.2ms**, and client-side verification takes only **5.1ms**.
- Deployment cost is significantly higher: the TEE setup uses **m5.xlarge $0.192/hour**, compared with a standard **t3.micro $0.0104/hour**, about **18.5×** higher cost.
- The paper also reports the guardrail’s own performance, showing that “having proof ≠ being safe”: Llama Guard 3 achieves **F1=0.56** on the Unsafe category (Precision **0.59** / Recall **0.54**), while Loki achieves **F1=0.76** on the Non-Factual category and **F1=0.67** on the Factual category; accordingly, the authors explicitly oppose presenting this as proof-of-safety.

## Link
- [http://arxiv.org/abs/2603.05786v1](http://arxiv.org/abs/2603.05786v1)
