---
source: arxiv
url: http://arxiv.org/abs/2603.11721v1
published_at: '2026-03-12T09:28:25'
authors:
- Wenxian Yang
- Hanzheng Qiu
- Bangqun Zhang
- Chengquan Li
- Zhiyong Huang
- Xiaobin Feng
- Rongshan Yu
- Jiahong Dong
topics:
- llm-agents
- clinical-workflows
- agentic-operating-system
- multi-agent-systems
- long-term-memory
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# When OpenClaw Meets Hospital: Toward an Agentic Operating System for Dynamic Clinical Workflows

## Summary
This paper proposes a "hospital agent operating system" architecture for dynamic clinical workflows in hospitals. It is built on an OpenClaw-style skill library, but adapts it to healthcare settings through operating-system-level isolation, document-driven multi-agent collaboration, and hierarchical long-term memory. The core goal is to enable LLM agents to handle the large number of non-preprogrammed, long-tail clinical tasks in hospitals while ensuring safety, auditability, and scalability.

## Problem
- Existing general-purpose LLM agent frameworks typically assume **broad-permission execution** (file system, network, code execution), which fundamentally conflicts with hospitals' privacy, compliance, and auditing requirements.
- Existing memory/RAG approaches based on vector retrieval break medical records into context-free fragments, making it difficult to preserve **longitudinal, temporal, and document-structured** clinical information.
- Hospital workflows are inherently **multi-role, document-centered** collaborative systems rather than a single conversational interface; traditional HIS/EHR/CDSS systems are also mostly built around fixed processes and struggle to cover long-tail clinical needs.

## Approach
- Proposes a **restricted execution environment** inspired by Linux multi-user systems: each role agent (patient, physician, nurse, etc.) runs in an independently isolated namespace, with direct file access, external network access, and dynamic code loading prohibited, and may only invoke pre-audited skills.
- Uses a **medical skill library** as the only executable unit of action: skills have typed interfaces and can access internal hospital resources only through predefined, narrow-permission connectors, thereby pushing security constraints down to the runtime and system layers.
- Designs a **document-centered multi-agent collaboration mechanism**: agents do not communicate directly, but coordinate through write/change events on shared clinical documents; the event stream records version numbers, writer roles, and page references, forming a traceable audit trail.
- Proposes a **page-indexed memory architecture**: a patient's long-term record is organized as a tree-structured document hierarchy, with each internal node maintaining a manifest file; during queries, the agent reads manifests layer by layer and selects relevant subtrees, replacing vector-similarity retrieval.
- Provides **local incremental maintenance** for dynamic updates: a single document change only requires updating the affected node and necessary ancestor-node manifests. The paper states the maintenance complexity as `O(d)` per change, or at most `O(L)` incremental LLM calls.

## Results
- This paper is an **architecture/system design proposal** and, in the provided excerpt, **does not report experimental metrics, benchmark results, or clinical deployment outcomes**, so there are no precise performance numbers to fill in (such as accuracy, AUROC, throughput, or latency).
- The paper's strongest concrete technical claim is that page-indexed memory **does not rely on vector embeddings at all**, and therefore can adapt to medical-record document collections with real-time changes **without embedding computation, offline index building, or index rebuilding**.
- In terms of complexity, the authors explicitly claim that manifest maintenance costs **`O(d)` per change** (`d` is node depth), and under ancestor propagation the worst case is **`O(L)` incremental LLM calls**, rather than batch reprocessing the entire corpus.
- In terms of system constraints, the authors claim that agent actions are limited to **two categories**: invoking pre-audited medical skills and reading/writing shared clinical documents; cross-agent coordination is completed through a **single append-only mutation event stream**, thereby improving safety, transparency, and auditability.
- At the capability level, the authors claim that this architecture can support **on-demand skill composition** to handle long-tail clinical needs beyond fixed workflows, such as multi-year laboratory trend analysis, rare drug interactions, and personalized analysis across care episodes, but the excerpt does not provide quantitative comparisons.

## Link
- [http://arxiv.org/abs/2603.11721v1](http://arxiv.org/abs/2603.11721v1)
