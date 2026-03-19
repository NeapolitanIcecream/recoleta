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
- clinical-ai
- agent-architecture
- long-term-memory
- retrieval-architecture
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# When OpenClaw Meets Hospital: Toward an Agentic Operating System for Dynamic Clinical Workflows

## Summary
This paper proposes a "hospital agentic operating system" architecture for hospital environments, transforming general-purpose LLM agents into a constrained, auditable, and long-memory clinical workflow coordination layer. The core contribution is the combination of execution isolation, document-driven multi-agent collaboration, page-indexed memory, and a pre-audited medical skills library to address safety and long-horizon context challenges in hospital settings.

## Problem
- Existing LLM agent frameworks typically assume open computing environments and often require broad system permissions, which conflicts with hospital requirements for privacy, security, auditability, and compliance.
- Common RAG/vector retrieval methods fragment longitudinal patient records into decontextualized pieces, making it difficult to preserve temporal order, causal relationships, and clinical context across phases of care.
- Hospital workflows are inherently multi-role, document-centered, and involve many long-tail clinical needs; fixed preprogrammed hospital IT systems struggle to cover these ad hoc composite tasks.

## Approach
- Proposes a restricted execution environment: each patient/doctor/staff agent runs in its own isolated namespace and can access resources only through predefined skill interfaces; arbitrary filesystem access, external internet access, and dynamic code execution are prohibited. The security boundary is enforced by OS mechanisms rather than prompt constraints.
- Uses document-centered multi-agent collaboration: agents do not communicate directly, but coordinate through writes to shared clinical documents and change event streams; each write carries a version number and forms an append-only, auditable event trail.
- Designs a page-indexed memory architecture: medical records are organized into a tree-structured document hierarchy, with each internal node maintaining a manifest summary; during retrieval, the LLM reads manifests layer by layer and chooses branches to drill down into, rather than using vector similarity retrieval.
- Introduces a medical skills library: capabilities such as vital sign aggregation, medication adherence tracking, and report generation are encapsulated as static, typed, pre-audited modules. Agents can dynamically compose these skills according to goals to handle clinical tasks not covered by preprogrammed workflows.
- Uses localized updates for memory maintenance: after document changes, only the relevant manifests are updated incrementally. The authors claim the maintenance cost is `O(d)` per change or at most `O(L)`, without requiring full-library index rebuilding or embedding recomputation.

## Results
- This is an excerpt from an architecture/systems design paper and does not provide empirical experiments, benchmark datasets, or quantitative performance results, so there are **no reportable accuracy, recall, efficiency, or clinical outcome figures**.
- The complexity claims explicitly given in the paper include: the local manifest maintenance cost for a single change is `O(d)` (`d` is the tree depth), and the authors state that ancestor-level incremental updates require at most `O(L)` LLM calls, with no need for embedding recomputation.
- The authors claim that this architecture is safer than traditional open-ended agents: least privilege, auditing, and resource isolation are achieved through kernel-level mechanisms such as Linux user isolation, seccomp, AppArmor, and auditd/inotify, but no quantitative security evaluation is provided.
- The authors claim it is better suited than vector RAG for longitudinal clinical records: page-indexed memory preserves document hierarchy, time ranges, and document types, and can operate under real-time medical record changes without offline graph construction or index rebuilding, but no comparative retrieval metrics are provided.
- The paper uses cases such as continuous monitoring, emergency triage, and urgent escalation to illustrate that the system can support dynamic clinical workflows and ad hoc task composition; these are conceptual scenario demonstrations, not quantitative validation based on real hospital deployment.

## Link
- [http://arxiv.org/abs/2603.11721v1](http://arxiv.org/abs/2603.11721v1)
