---
source: arxiv
url: http://arxiv.org/abs/2603.02345v1
published_at: '2026-03-02T19:28:27'
authors:
- Sami Abuzakuk
- Lucas Crijns
- Anne-Marie Kermarrec
- Rafael Pires
- Martijn de Vos
topics:
- llm-agents
- configuration-drift
- infrastructure-as-code
- multi-agent-systems
- tool-reliability
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection

## Summary
RIVA proposes a multi-agent system for infrastructure-as-code (IaC) configuration drift detection, focusing on the real-world problem that “tool outputs themselves may be wrong.” Its core contribution is to have two LLM agents cross-validate the same property through different tool paths, thereby improving detection reliability when unreliable tools are present.

## Problem
- The problem it addresses is whether deployed cloud infrastructure has deviated from the IaC specification, i.e., configuration drift detection and verification.
- This matters because drift can arise from IaC defects, manual hotfixes, system updates, or cloud API anomalies, which can in turn lead to service outages, security risks, and high manual troubleshooting costs.
- Existing LLM agents usually assume external tool outputs are trustworthy; once a tool silently returns incorrect, stale, or empty results, the agent cannot tell whether it reflects real drift or a tool failure, leading to missed detections or false alarms.

## Approach
- RIVA uses two specialized agents working together: the **Verifier Agent** selects which properties from the IaC specification should be checked and determines compliance, while the **Tool Generation Agent** generates and executes tool calls for those properties.
- The core mechanism is simple: **do not trust a single tool result; instead, use different tools / different diagnostic paths to cross-validate the same property**. If multiple independent paths agree, the conclusion is more trustworthy.
- The system maintains a shared **Tool Call History**, recording up to K distinct tool executions per property, including commands, results, and brief analysis; the Verifier only reaches a conclusion after obtaining K independent pieces of evidence for the same property.
- The Tool Generation Agent consults the history, specifically generates “unused” new verification paths, and retries with corrected parameters or syntax when a call fails, improving tool diversity and robustness.
- The paper mainly uses K=2; when K=1, it nearly degenerates into a standard single-path agent, while K=3 fails in AIOpsLab because there are not enough available diagnostic paths.

## Results
- On AIOpsLab, when **erroneous tool outputs are present**, RIVA improves average accuracy across all tasks from **27.3%** with the baseline ReAct agent to **50.0%**.
- When **no erroneous tool outputs** are present, RIVA also increases average task success rate from **28.0%** to **43.8%**, showing that the gains come not only from fault tolerance but also from multi-agent role separation.
- A concrete example: in localization tasks, ReAct achieves **22.2%** with correct tools, but drops to **11.1%** with erroneous `get_logs`; RIVA reaches **20.0%** under the same erroneous tool condition. The paper also notes that RIVA’s performance across all tasks is “always greater than or equal to” ReAct’s performance under correct-tool conditions.
- In terms of efficiency, with correct tools **80%** of RIVA tasks finish within **15 steps**, while only **60%** of ReAct tasks do; RIVA’s step-count peak is **17**, whereas **33%** of ReAct runs hit the **45-step** limit.
- In terms of token cost, with correct tools RIVA peaks at about **38,000 tokens**, versus about **78,000** for ReAct; under erroneous tools, RIVA peaks at about **50,000**, versus about **90,000** for ReAct.
- Ablation on hyperparameter K: **RIVA(K=1)** has an average success rate close to ReAct’s (correct tools **27.67** vs ReAct **28.00**); **RIVA(K=2)** performs best (correct tools **43.75**, erroneous `get_logs` **46.67**, erroneous `read_metrics` **53.33**); **RIVA(K=3)** is **0%** in all three settings because the benchmark environment lacks 3 distinguishable diagnostic paths.

## Link
- [http://arxiv.org/abs/2603.02345v1](http://arxiv.org/abs/2603.02345v1)
