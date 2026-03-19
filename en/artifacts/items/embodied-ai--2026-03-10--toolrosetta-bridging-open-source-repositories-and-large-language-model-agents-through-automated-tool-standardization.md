---
source: arxiv
url: http://arxiv.org/abs/2603.09290v1
published_at: '2026-03-10T07:19:43'
authors:
- Shimin Di
- Xujie Yuan
- Hanghui Guo
- Chaoqian Ouyang
- Zhangze Chen
- Ling Yue
- Libin Zheng
- Jia Zhu
- Shaowu Pan
- Jian Yin
- Min-Ling Zhang
- Yong Rui
topics:
- llm-agents
- tool-standardization
- model-context-protocol
- repo-to-tool
- scientific-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# ToolRosetta: Bridging Open-Source Repositories and Large Language Model Agents through Automated Tool Standardization

## Summary
ToolRosetta aims to automatically convert tools scattered across open-source code repositories and APIs, which are difficult to invoke directly, into MCP-standard tools callable by LLM agents. It seeks to replace manual wrapping with automated standardization, thereby improving tool reuse, task completion rates, and cross-domain scalability.

## Problem
- The paper addresses the following issue: although there are many practical tools in open-source repositories, their interfaces are heterogeneous, dependencies are complex, and they lack a unified executable standard, making it difficult for LLM agents to invoke them reliably.
- This matters because current tool-using agents rely heavily on manual organization and hand-crafted tool wrapping, which is costly and unscalable when extending to large-scale, long-tail, and cross-disciplinary tools.
- If code cannot be automatically turned into callable services, then even if an LLM can “understand” a repository, it is still difficult for it to truly complete scientific computing or complex workflow tasks.

## Approach
- The core method is a multi-agent automatic conversion framework: it first understands the user task, then searches for relevant GitHub repositories/APIs, and finally automatically wraps candidate code into MCP-compatible services.
- Its mechanism can be understood simply as “translating messy code repositories into unified tool interfaces”: including repository cloning, semantic analysis, environment configuration, interface extraction, service generation, and validation.
- The system includes a Planning agent, Tool-search agent, MCP-construction agent, Security agent, and Review agent, which are responsible for planning, retrieval, construction, security inspection, and failure repair, respectively.
- To improve success rates, ToolRosetta uses a Review-Revise-Fix (RRF) iterative repair process to perform root-cause analysis on failed conversion cases and patch them over multiple rounds.
- It also adds a security inspection layer to detect potential malicious code, privacy leakage, or trojan risks, reducing the risks of directly executing third-party code in an open ecosystem.

## Results
- ToolRosetta automatically converted **1580** tools from **122** GitHub repositories into standardized executable interfaces, covering **6** major domains and **35** subdisciplines.
- On the 122-repository conversion benchmark, the first-round conversion success rate was **53.0%**, higher than the **49.6%** of the GPT-4o service-only baseline; human engineers achieved **82.9%**. If GPT-4o was asked to generate the full repository-to-MCP stack in one shot, the success rate was only **3.3% (4/122)**.
- In terms of efficiency, ToolRosetta took an average of **210.1 s** per repository, compared with **1589.4 s** for humans (about **26.5 min**), corresponding to an **86.8%** reduction in time and a **7.6×** speedup.
- After **3** rounds of RRF repair, the domain macro-average conversion success rate increased from **54.2%** to **69.3%**, and the benchmark weighted success rate increased from **53.0%** to **68.4%**; among them, Scientific Community & Society showed the largest improvement, reaching **+24.4** percentage points.
- On downstream tasks, ToolRosetta achieved a macro-average task completion accuracy of **55.6%** across 6 scientific categories, and **52.1%** on average across **35** subdisciplines; it ranked first in **5** of the **6** categories. The paper states that its six-domain macro-average accuracy improved by **more than 31%** relative to the strongest baseline.
- On **21** OOD subdomains, ToolRosetta achieved an average accuracy of **57.4%**, significantly higher than SciToolAgent’s **11.7%**, ChemCrow’s **3.3%**, RepoMaster’s **24.0%**, and OpenAgents’ **21.5%**. After injecting tools converted by ToolRosetta into other systems, RepoMaster improved from **24.2%** to **34.8%** (**+10.6**), and OpenAgents improved from **22.0%** to **35.4%** (**+13.4**).
- In the case study on perovskite material discovery, the system proposed an Sn–Pb formulation with **50% lower lead content**; wet-lab experiments verified a power conversion efficiency of **17%**, close to its predicted **16%–19%** range.

## Link
- [http://arxiv.org/abs/2603.09290v1](http://arxiv.org/abs/2603.09290v1)
