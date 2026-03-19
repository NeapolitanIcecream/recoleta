---
source: arxiv
url: http://arxiv.org/abs/2603.09023v1
published_at: '2026-03-09T23:38:32'
authors:
- Tony Mason
topics:
- llm-systems
- context-management
- demand-paging
- virtual-memory
- agentic-ai
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# The Missing Memory Hierarchy: Demand Paging for LLM Context Windows

## Summary
This paper redefines the LLM context window as an “L1 cache” rather than full memory, and proposes Pichay, a proxy-based demand paging system, to manage context. The core argument is that the large amount of context waste in current agentic LLM systems is fundamentally a virtual memory problem that has not been systematically addressed.

## Problem
- The paper addresses the problem that **LLM/agent session context windows become filled with accumulated history, tool definitions, and old tool results** over time, leading to context limits, attention degradation, and costs that worsen as sessions grow longer.
- Across 857 production sessions, 54,170 API calls, and 4.45 billion effective input tokens, the authors measure that **21.8% of tokens are structural waste**: 11.0% unused tool schema, 2.2% duplicate content, and 8.7% stale tool results.
- This matters because the current approach is mainly to enlarge context windows, but the processing and attention costs of long sessions still rise, and session state still cannot be systematically retained and reclaimed.

## Approach
- The core method is **Pichay**: a transparent HTTP proxy placed between the client and the inference API that inspects the full message stream on each request, automatically removes content that is “temporarily unnecessary but can be retrieved again” from the context, and leaves behind a short “paging marker.”
- When the model later requests the same content again (for example, rereading a removed file), the system treats this as a **page fault**—that is, the model is telling the system, “I still need the content that was moved away earlier.”
- The system distinguishes between two kinds of content: **garbage collection** for temporary tool outputs that cannot be reliably re-fetched, and **paging** for content such as file reads that can be re-fetched by address. This distinction is necessary to correctly measure the true page fault rate.
- It uses a very simple **FIFO eviction by user-turn age** (in the experiments, τ=4 turns, s_min=500 bytes), and adds **fault-driven pinning**: once a page has caused a page fault due to eviction, that version of the content is pinned thereafter and is no longer repeatedly evicted.
- More broadly, the paper also proposes **cooperative memory management**: through phantom tools and cleanup tags, the model can actively release cold content, request restoration of paged-out content, or compress conversation history into summaries, forming a complete L1/L2/L3/L4 memory hierarchy design.

## Results
- In production-corpus measurements, the authors report **21.8% structural waste**, broken down as **11.0%** unused tool schema, **2.2%** duplicate content, and **8.7%** stale tool results; among these, stale tool results have a median repeated-processing amplification of **84.4×**.
- Offline replay experiments covered **1.4 million simulated evictions** and report a **page fault rate of only 0.0254%**, indicating that much of the removed content is in fact never needed again.
- In online production deployment, across a **681-turn** session, the system **reduced context consumption by up to 93%**, from **5,038KB to 339KB**.
- The paper also gives a specific production case: the session’s remaining available context increased from **7% to 43%**, extending a session that was “about to die from context exhaustion” into one with substantial headroom remaining.
- Under extreme sustained pressure, the system remains operational, but exhibits classic **thrashing**: evicted content is repeatedly faulted back in, showing that when the working set exceeds the resident set, the method follows the same known operating-system behavior.
- L3 conversation compaction and L4 cross-session persistent memory have been designed / partially implemented, but the paper states that **only the first two levels (L1 eviction and L2 pinning) were quantitatively evaluated**; L3 has not yet been evaluated at scale.

## Link
- [http://arxiv.org/abs/2603.09023v1](http://arxiv.org/abs/2603.09023v1)
