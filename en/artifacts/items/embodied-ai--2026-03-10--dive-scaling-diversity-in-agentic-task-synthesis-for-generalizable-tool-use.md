---
source: arxiv
url: http://arxiv.org/abs/2603.11076v1
published_at: '2026-03-10T20:54:23'
authors:
- Aili Chen
- Chi Zhang
- Junteng Liu
- Jiangjie Chen
- Chengyu Du
- Yunji Li
- Ming Zhong
- Qin Wang
- Zhengmao Zhu
- Jiayuan Song
- Ke Ji
- Junxian He
- Pengyu Zhao
- Yanghua Xiao
topics:
- tool-use-llm
- synthetic-data
- ood-generalization
- agent-training
- task-synthesis
relevance_score: 0.41
run_id: materialize-outputs
language_code: en
---

# DIVE: Scaling Diversity in Agentic Task Synthesis for Generalizable Tool Use

## Summary
Dive is a data synthesis method for training tool-using LLMs. Its core idea is to first call real tools to collect evidence, and then generate tasks in reverse from the execution traces, thereby improving both diversity and verifiability. The paper shows that across a wide range of OOD benchmarks, increasing “task/tool diversity” improves generalization more than simply increasing data volume.

## Problem
- Existing post-training for tool-using LLMs often relies on synthesized tasks, but these tasks are usually limited to fixed task families and fixed toolsets, causing poor generalization to new tasks and new toolsets, and even negative transfer.
- To improve generalization, training data must be both **diverse** and **executable/verifiable**; however, the more diversity one pursues, the easier it becomes to generate unsolvable or unverifiable tasks.
- Existing approaches either rely on expensive specialized pipelines to extract data, depend on unstable simulated tools, or use a “write tasks first, then verify” process, all of which create bottlenecks in quality and scalability.

## Approach
- Proposes **evidence-first** synthesis: instead of writing questions first, it executes real tools first, collects real outputs, and then infers answerable questions and gold answers only from that evidence, so **executability and verifiability** are guaranteed by construction.
- Expands diversity through three decoupled resource pools: **373 verified tools** (covering general-purpose plus 4 expert domains), about **5,000 seed entities** per domain, and query-only exemplars from multiple task families.
- In each synthesis round, it randomly samples a configuration: a seed, a tool subset of **15–50 tools**, and **3–5 exemplars**; it then runs an “evidence collection–task derivation” loop for up to **K=3** iterations to induce multi-step, heterogeneous tool-use patterns.
- Training uses two stages: first SFT cold-start on synthesized tasks, then RL on tasks with reference answers; the paper uses **Qwen3-8B** as the backbone, with **48k** SFT trajectories and **3.2k** frontier tasks for RL.

## Results
- The paper claims that after training **Qwen3-8B** on Dive data, average performance across **9 OOD benchmarks** improves by **+22 points**, and it achieves a **+68%** advantage over the “strongest 8B baseline” (overall conclusion from the abstract).
- Looking at the main results table, the improvement from **Qwen3-8B (base)** to **Dive-8B (RL)** is substantial: GAIA **22.4→61.2** (+38.8), HLE **6.4→17.8** (+11.4), BrowseComp **1.3→16.4** (+15.1), Xbench-DS **24.0→58.1** (+34.1).
- There are also gains on domain/specialized-tool OOD benchmarks: FinSearchComp-T2 **28.6→67.3** (+38.7), T3 **7.1→37.3** (+30.2), Finance Agent Benchmark **2.0→34.0** (+32.0), MedAgentBench **38.4→57.3** (+18.9), SWE-bench Verified **10.8→18.3** (+7.5), Toolathlon **0.9→8.3** (+7.4).
- Compared with 8B baselines, Dive-8B (RL) is clearly stronger on most benchmarks; for example, versus **WebExplorer-8B**: GAIA **61.2 vs 50.0**, FinSearchComp-T2 **67.3 vs 35.9**, Finance Agent Benchmark **34.0 vs 4.0**; versus **EnvScaler-8B**: GAIA **61.2 vs 25.8**, SWE **18.3 vs 11.5**, Toolathlon **8.3 vs 2.2**.
- Moving from SFT to RL brings further gains: Dive-8B improves from SFT to RL on Dive-Eval **35.4→42.5**, GAIA **49.3→61.2**, HLE **13.8→17.8**, MedAgentBench **50.2→57.3**, indicating that diversified data can further amplify RL gains.
- The abstract also gives a key analytical conclusion: **diversity scaling outperforms quantity scaling**. Even with **4×** less data, it still outperforms simply piling on more data for OOD generalization; however, the excerpt does not provide finer-grained numbers for that analysis.

## Link
- [http://arxiv.org/abs/2603.11076v1](http://arxiv.org/abs/2603.11076v1)
