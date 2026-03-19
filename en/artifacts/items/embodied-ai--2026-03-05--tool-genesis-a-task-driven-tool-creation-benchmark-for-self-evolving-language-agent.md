---
source: arxiv
url: http://arxiv.org/abs/2603.05578v1
published_at: '2026-03-05T17:44:29'
authors:
- Bowei Xia
- Mengkang Hu
- Shijian Wang
- Jiarui Jin
- Wenxiang Jiao
- Yuan Lu
- Kexin Li
- Ping Luo
topics:
- language-agents
- tool-creation
- benchmarking
- mcp
- self-evolving-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agent

## Summary
This paper introduces **Tool-Genesis**, a diagnostic benchmark for evaluating whether **language agents can autonomously create reusable tools from abstract task requirements**, rather than assuming tool interfaces are already known. Its core finding is: even the strongest models often make small mistakes in either the interface or implementation in one-shot generation, and these small errors are amplified along the pipeline, significantly dragging down final task success rates.

## Problem
- Most existing evaluations of tool use / tool generation are **spec-first**: they assume given interfaces, schemas, or high-quality reference specifications, so they cannot truly test whether models can **infer tool interfaces and implement tools** from abstract requirements.
- Many evaluations only consider final task success or failure, amounting to **black-box evaluation**; once a failure occurs, it is difficult to distinguish whether the problem came from interface design errors, code logic errors, or downstream tool-use strategy errors.
- This matters because in real deployments, tool specifications are often missing, APIs change, and long-tail requirements emerge; if agents cannot create, repair, and maintain tools by themselves, it is hard to achieve truly **self-evolving language agents**.

## Approach
- The authors build a **requirement-driven** benchmark: only natural-language requirements are provided, with no preset tool specifications, and the model must complete two steps: **interface prediction** (generating an MCP schema) and **tool materialization** (generating an executable server implementation).
- The evaluation is split into two settings: **Oracle Materialization** uses ground-truth schemas to test implementation ability, while **Cascaded Materialization** uses the model’s own predicted schemas to test end-to-end ability, thereby separating “interface errors” from “implementation errors” as much as possible.
- They design four layers of diagnostic metrics: L1 measures surface-level compliance and service executability, L2 uses **Schema-F1** to assess semantic interface matching, L3 uses **UT_soft / UT_hard** to test functional correctness and robustness on boundary/negative cases, and L4 uses a fixed agent together with generated tools to solve tasks, reporting **Oracle-Normalized Success Rate**.
- The dataset is drawn from the real MCP server ecosystem and constructed through crawling, filtering, task and trajectory generation, unit test generation, and manual review; the final benchmark retains **86 servers, 508 tools, 2150 tasks, and 9441 unit tests**, covering **24 domain classes**.

## Results
- In terms of dataset scale, Tool-Genesis contains **86** executable MCP servers, **508** tools, **24** domains, **2150** tasks, and **9441** unit tests; each task has an average of **6** execution steps and uses **3** tools, indicating that this is not a simple single-step calling benchmark.
- Under **Direct** one-shot generation, the best model, **gpt-5.1**, achieves only **Schema-F1=0.688, UT_soft=0.281, UT_hard=0.161, SR=0.372**; this shows that even strong models still have limited truly usable tool-creation ability.
- Under **Code-Agent** closed-loop repair, performance improves significantly: **gpt-5.1** reaches **Compliance=0.895, Exec=0.941, Schema-F1=0.867, UT_soft=0.421, UT_hard=0.246, SR=0.604**, one of the highest SR results in the table.
- Other models also show clear gains from closed-loop repair: for example, **gemini-3-flash-preview** improves from **Exec 0.140 / Schema-F1 0.116 / SR 0.103** in Direct to **Exec 0.977 / Schema-F1 0.912 / SR 0.581** in Code-Agent.
- Among open-source / open-weight models, **Kimi-K2** reaches **Schema-F1=0.898, UT_soft=0.389, UT_hard=0.235, SR=0.585** under Code-Agent; **Qwen3-32B** reaches **SR=0.495**, and **DeepSeek-v3.2** reaches **SR=0.449**.
- The paper’s strongest concrete claim is not that tool creation has been solved, but precisely the opposite: **small interface or implementation defects cascade and become amplified, causing sharp drops in downstream utility**; closed-loop execution feedback can substantially mitigate this, but even in the best configuration, strict unit-test performance and final success rates remain far from saturated.

## Link
- [http://arxiv.org/abs/2603.05578v1](http://arxiv.org/abs/2603.05578v1)
