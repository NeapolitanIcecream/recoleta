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
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection

## Summary
RIVA proposes a multi-agent LLM system for detecting configuration drift in cloud infrastructure, focusing on the unreliability of agent systems when tools return silent erroneous results. Its core contribution is significantly improving task success rate and efficiency on AIOpsLab through multi-tool cross-validation and history tracking.

## Problem
- The paper addresses the problem of **configuration drift detection in IaC (Infrastructure as Code) environments**: production cloud resources may deviate from declarative configurations because of code defects, manual changes, or system updates.
- This matters because configuration drift can lead to **service outages, security vulnerabilities, and increased operational complexity**, while manually continuously checking large-scale logs, metrics, and system state is labor-intensive and error-prone.
- Existing LLM agents usually assume external tools are always correct; once a tool returns a **wrong but seemingly normal** result, the agent cannot tell whether it reflects real drift or a broken tool, leading to missed detections or false alarms.

## Approach
- RIVA uses two specialized agents working together: the **Verifier Agent** selects properties from the IaC specification to verify and determines whether they are satisfied; the **Tool Generation Agent** generates and executes different verification tool calls for those properties.
- The core mechanism is simple: **do not trust a single tool result; instead, use multiple different tools / diagnostic paths to verify the same property**. If the results agree, confidence increases; if they conflict, the system continues reasoning and cross-checking.
- The system maintains a shared **Tool Call History**, recording for each property the commands, outputs, and brief analyses from different tools; the Verifier draws a conclusion only after the same property has accumulated results from K different tools.
- The Tool Generation Agent reviews the history and deliberately generates new tool calls **different from previous methods** to verify the same issue from another angle, improving robustness to faulty tool outputs.
- The authors integrated this method into AIOpsLab and compared it with a standard **single-agent ReAct** baseline on detection, localization, and analysis tasks under both correct-tool and erroneous-tool conditions.

## Results
- When **erroneous tool outputs are present**, RIVA improves the **average task success rate** on AIOpsLab from ReAct’s **27.3% to 50.0%**, recovering much of the performance lost because of faulty tools.
- When **no erroneous tool outputs** are present, RIVA still raises average success rate from **28.0% to 43.8%**, showing that the gains come not only from robustness but also from better multi-agent division of labor.
- A concrete example: in the **localization task**, ReAct achieves **22.2%** with correct tools, but drops to **11.1%** when `get_logs` is faulty; RIVA reaches **20.0%** under the same faulty-tool condition. At the same time, RIVA achieves **40.0%** on localization with correct tools, and **20.0%** when both `get_logs` + `read_metrics` are faulty.
- In the **detection task**, ReAct scores **50.0%** with correct tools, but unexpectedly rises to **62.5%** with faulty `get_logs`; the paper explains this by noting that detection is simpler, and empty logs push the agent to rely more on more focused metric information. This shows that tool errors can have accidental and uncontrollable effects on single-agent behavior, whereas RIVA is more stable.
- In terms of efficiency, under correct-tool conditions, **80%** of RIVA tasks finish within **15 steps**, while only **60%** of ReAct tasks do; RIVA’s step-count peak is **17**, whereas **33%** of ReAct runs hit the **45-step** limit. RIVA’s peak token usage is about **38,000**, versus about **78,000** for ReAct.
- Under erroneous-tool conditions, RIVA still uses at most about **17 steps**, while **37%** of ReAct tasks exceed that threshold; peak token usage is about **50,000** (RIVA) versus **90,000** (ReAct). In addition, the hyperparameter **K=2** performs best: average success rates are **43.75%/46.67%/53.33%** (correct tools / faulty `get_logs` / faulty `read_metrics`), while **K=1** is close to ReAct, and **K=3** drops to **0%** because of insufficient diagnostic paths.

## Link
- [http://arxiv.org/abs/2603.02345v1](http://arxiv.org/abs/2603.02345v1)
