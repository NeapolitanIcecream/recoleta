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
- tool-creation-benchmark
- language-agents
- code-generation
- mcp
- self-evolving-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agent

## Summary
Tool-Genesis is a diagnostic benchmark for the tool-creation capabilities of "self-evolving language agents." It requires models to infer tool interfaces solely from abstract task requirements, generate executable implementations, and measures the reusability and utility of these tools in real tasks. The paper shows that even the most advanced models often make small interface or implementation errors in one-shot generation, and these errors are amplified in later stages of the pipeline, causing significant end-to-end performance degradation.

## Problem
- Existing tool-use/tool-creation evaluations mostly rely on predefined specifications or reference interfaces, so they cannot truly test whether an agent can **autonomously design tools from vague requirements**.
- Many benchmarks look only at final task outcomes like a “black box,” making it difficult to distinguish whether failures come from **interface design errors, code implementation errors, or tool-use strategy errors**.
- This matters because in real deployments, API/tool specifications are often missing, changing, or incomplete; if agents cannot create, repair, and maintain tools, it is hard for them to support long-term software automation and self-evolving capabilities.

## Approach
- Proposes **Tool-Genesis**: a requirement-driven tool-creation benchmark that asks models to generate **MCP tool schema** and **executable server implementations** from natural-language requirements, rather than merely calling existing APIs.
- Splits the task into two stages: **interface prediction** (first inferring tool names, parameters, constraints, and descriptions) and **tool materialization** (then writing executable implementations according to the schema), and distinguishes **Oracle Materialization** from **Cascaded Materialization** to isolate different sources of error.
- Designs a four-layer evaluation: L1 surface compliance/executability, L2 **Schema-F1** interface semantic fidelity, L3 **UT_soft / UT_hard** functional correctness (including boundary/negative-case tests), and L4 downstream task success rate **SR**.
- Introduces **oracle-normalized success rate**, comparing generated tools with reference ground-truth tools under the same task distribution to quantify “how far they still are from ideal usable tools.”
- The dataset is built through MCP server collection, task and trajectory generation, unit test extraction/synthesis, and manual review, ultimately containing **86 servers, 508 tools, 24 domains, 2150 tasks, 9441 unit tests**; the manually reviewed Cohen’s kappa is **0.85**.

## Results
- In terms of benchmark scale, Tool-Genesis covers **86** MCP servers, **508** tools, **24** domains, **2150** tasks, and **9441** unit tests; the average task length is **53** tokens, with an average of **6** execution steps and **3** tools used.
- Under **Direct** one-shot generation, even the best model **gpt-5.1** achieves only: Compliance **0.826**, Exec **0.759**, Schema-F1 **0.688**, UT_soft **0.281**, UT_hard **0.161**, and SR **0.372**, showing that end-to-end usability remains limited in single-pass generation.
- Under **Code-Agent** closed-loop repair, the best results improve significantly: **gpt-5.1** reaches Compliance **0.895**, Exec **0.941**, Schema-F1 **0.867**, UT_soft **0.421**, UT_hard **0.246**, and SR **0.604**; **Kimi-K2** achieves an SR of **0.585**, and **gemini-3-flash-preview** achieves an SR of **0.581**.
- The paper emphasizes that closed-loop execution feedback brings improvements across layers. For example, **gemini-3-flash-preview** improves from Direct to Code-Agent as follows: Exec **0.140→0.977**, Schema-F1 **0.116→0.912**, UT_soft **0.084→0.448**, UT_hard **0.037→0.255**, and SR **0.103→0.581**.
- Even when upstream signals are relatively strong, downstream utility can still be clearly insufficient, exposing a “utility-conversion bottleneck.” For example, in Table 2, **Qwen3-32B (Code-Agent)** has Exec **0.892** and Schema-F1 **0.801**, but its SR is only **0.495**; this shows that having a reasonable-looking interface does not mean the tool is truly robust and usable.
- The paper’s core conclusion is that **even state-of-the-art models still struggle to accurately construct tool interfaces and executable logic in a one-shot setting**, and these small initial errors accumulate and amplify along the pipeline; Tool-Genesis therefore functions more like a “diagnostic instrument” for locating root causes than merely a leaderboard.

## Link
- [http://arxiv.org/abs/2603.05578v1](http://arxiv.org/abs/2603.05578v1)
