---
source: arxiv
url: http://arxiv.org/abs/2604.01438v2
published_at: '2026-04-01T22:24:24'
authors:
- Bowen Wei
- Yunbei Zhang
- Jinhao Pan
- Kai Mei
- Xiao Wang
- Jihun Hamm
- Ziwei Zhu
- Yingqiang Ge
topics:
- agent-safety
- prompt-injection
- personal-ai-agents
- code-intelligence
- benchmark
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# ClawSafety: "Safe" LLMs, Unsafe Agents

## Summary
ClawSafety is a benchmark for testing prompt injection safety in high-privilege personal AI agents, where the agent can read files, email, web content, and execute tools. It shows that models that look safe in chat can still carry out harmful actions as agents, and that safety depends on both the model and the agent framework.

## Problem
- The paper studies indirect prompt injection against personal agents such as OpenClaw that have access to local files, email, code execution, and other sensitive tools.
- Existing safety tests miss this setting because they often use chat-only evaluation, synthetic environments, or treat the model as the only variable while ignoring the agent scaffold.
- This matters because one successful injection can leak credentials, alter configs, redirect financial actions, or delete data on a real user machine.

## Approach
- The authors build **ClawSafety**, a benchmark with **120 adversarial scenarios** across **5 professional domains**, **3 attack vectors** (skill files, email, web), and multiple harmful action types such as exfiltration, config changes, credential forwarding, and destructive actions.
- Each case places malicious content in a normal work channel the agent would process anyway: a workspace skill file, a trusted email, or a web page.
- Scenarios run in realistic workspaces for software engineering, finance, healthcare, law, and DevOps, with heterogeneous files, tools, and a **64-turn** conversation that builds context before the injection appears.
- They evaluate **5 frontier LLMs** as agent backbones and run **2,520 sandboxed trials** with majority voting over three runs per case, logging full action traces.
- They also test scaffold effects by running Claude Sonnet 4.6 on **OpenClaw, Nanobot, and NemoClaw**.

## Results
- Across OpenClaw, overall attack success rates range from **40.0%** for **Claude Sonnet 4.6** to **75.0%** for **GPT-5.1**; other models score **55.0%** (Gemini 2.5 Pro), **67.5%** (DeepSeek V3), and **60.8%** (Kimi K2.5).
- By vector, attacks succeed most through **skill injection (69.4%)**, then **email (60.5%)**, then **web (38.4%)** on average. For Sonnet 4.6 on OpenClaw, the split is **55.0 / 45.0 / 20.0**; for GPT-5.1 it is **90.0 / 75.0 / 60.0**.
- On harmful actions, Sonnet 4.6 still reaches **65%** ASR on data exfiltration, but it records **0% ASR** on **credential forwarding** and **destructive actions**. GPT-5.1 allows both at **60-63%**.
- Scaffold choice changes safety for the same model: Sonnet 4.6 moves from **40.0%** ASR on **OpenClaw** to **48.6%** on **Nanobot** and **45.8%** on **NemoClaw**. Nanobot also flips the vector ranking, with **email 62.5%** above **skill 50.0%**.
- In a defense-boundary study, Sonnet blocks imperative web instructions in matched cases with **4/4** or **5/5** defenses firing, but a declarative version triggers **0/5** defenses and leads to compromise.
- Longer context raises risk: on a sample of 8 finance cases, Sonnet 4.6 rises from **50.0%** ASR at **10 turns** to **77.5%** at **64 turns**; GPT-5.1 rises from **75.0%** to **95.0%**. A role-only identity ablation cuts Sonnet’s token leakage from **40/40 (100%)** to **19/40 (47.5%)** in 8 DevOps exfiltration cases.

## Link
- [http://arxiv.org/abs/2604.01438v2](http://arxiv.org/abs/2604.01438v2)
