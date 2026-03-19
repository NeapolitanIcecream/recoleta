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
- multi-agent-systems
- scientific-ai
- software-reuse
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# ToolRosetta: Bridging Open-Source Repositories and Large Language Model Agents through Automated Tool Standardization

## Summary
ToolRosetta proposes an automated framework that converts heterogeneous open-source code repositories and APIs on GitHub into MCP-standard tools that can be directly invoked by LLM agents, reducing the cost of manual wrapping and experiment reproduction. Its core value is discovering, standardizing, and safely executing long-tail specialized tools on demand within the open tool ecosystem, thereby significantly improving scientific task completion rates.

## Problem
- Most existing high-value tools are buried in heterogeneous code repositories and lack unified, executable standard interfaces, making them difficult for LLMs to invoke reliably.
- Manually transforming repositories into MCP tools requires understanding the code, configuring environments, rewriting interfaces, and debugging services, leading to high labor costs and poor scalability.
- Fixed, manually curated tool libraries have limited coverage and often fail on cross-disciplinary or OOD tasks because there is “no suitable tool.”

## Approach
- Uses a hierarchical multi-agent pipeline: the Planning agent plans the toolchain, the Tool-search agent retrieves and evaluates relevant repositories, and the MCP-construction agent automatically completes cloning, semantic analysis, environment configuration, and MCP service generation.
- Treats “repository/API → MCP tool” as a unified translation problem, automatically wrapping heterogeneous implementations into standardized, executable service interfaces callable by LLMs.
- Introduces a Review-Revise-Fix iterative repair mechanism: when validation fails, the Review agent performs root-cause analysis and generates a repair plan, iterating until tests pass or the process stops.
- Adds a Security Agent to inspect privacy leakage, malicious logic, and security risks during tool generation and execution, reducing the risks of directly executing open-source code.
- The standardized tools generated are not only used by ToolRosetta itself, but can also be injected into other agent systems and reused as portable infrastructure.

## Results
- Automated standardization scale: successfully converted **1,580 tools** from **122 GitHub repositories** into standardized executable interfaces, covering **6 domains** and **35 subdisciplines**.
- Repository conversion success rate: first-round success rate of **53.0%**, higher than the **49.6%** baseline where GPT-4o only generated `MCP_service.py`; if GPT-4o is asked to generate the full repository-to-MCP stack in one shot, the success rate is only **3.3% (4/122)**; human engineers achieve **82.9%**.
- Conversion efficiency: averaged **210.1 seconds** per repository, compared with **1589.4 seconds (26.5 minutes)** for humans, reducing time by **86.8%**, about **7.6×** faster.
- Iterative repair gains: after three rounds of RRF, the domain-level macro-average success rate rose from **54.2%** to **69.3%** (**+15.1 percentage points**), and the weighted benchmark success rate rose from **53.0%** to **68.4%**; the largest single-domain improvement appeared in Scientific Community & Society, reaching **+24.4 percentage points**.
- Downstream task performance: across six major scientific categories, ToolRosetta achieved a macro-average task completion accuracy of **55.6%**, and across 35 subdisciplines averaged **52.1%**; it ranked first in **5/6** categories. Relative to the “strongest baseline,” it claims **over 31%** improvement in macro-average accuracy.
- OOD and transfer gains: across **21 OOD subdomains**, ToolRosetta achieved an average accuracy of **57.4%**, significantly higher than SciToolAgent **11.7%**, ChemCrow **3.3%**, RepoMaster **24.0%**, and OpenAgents **21.5%**; after injecting its standardized tools into RepoMaster, the macro average increased from **24.2%→34.8% (+10.6)**, and after injecting them into OpenAgents, from **22.0%→35.4% (+13.4)**. A case study also reported discovering a perovskite formulation with **50% lower lead content**, with wet-lab validated PCE of **17%**, close to the predicted range of **16%–19%**.

## Link
- [http://arxiv.org/abs/2603.09290v1](http://arxiv.org/abs/2603.09290v1)
