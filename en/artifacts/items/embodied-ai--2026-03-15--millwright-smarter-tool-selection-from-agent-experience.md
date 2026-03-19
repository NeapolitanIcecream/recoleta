---
source: hn
url: https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/
published_at: '2026-03-15T22:50:17'
authors:
- dnautics
topics:
- tool-selection
- agent-experience
- rag-tools
- adaptive-ranking
- vector-retrieval
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Millwright: Smarter Tool Selection from Agent Experience

## Summary
Millwright proposes an adaptive tool-selection mechanism for large-scale tool catalogs: it first uses semantic retrieval to narrow the candidate set, then reranks using feedback from the agent’s historical tool usage. Its core value is enabling the agent to see more suitable tools more quickly within limited context, while continuously improving through experience.

## Problem
- Large models have limited available context; when the number of tools reaches the hundreds or thousands, directly stuffing many tool definitions into context crowds out space for RAG, planning, and conversation history.
- Semantic matching alone cannot capture whether a tool is actually effective in real execution; tools with similar semantic relevance may differ greatly in actual success rate, stability, and suitability.
- Existing RAG-style tool selection can retrieve by relevance, but lacks an online experience-feedback loop, so it cannot continuously update tool priority based on the agent’s actual usage outcomes.

## Approach
- Maintain a "toolshed" index that exposes only two interfaces: `suggest_tools` for querying and returning ranked candidate tools by task, and `review_tools` for writing back tool feedback after the task is completed.
- First decompose the task query into subtasks, then embed the subqueries as vectors; one ranking signal comes from the cosine similarity between the "query vector vs tool description vector," i.e. semantic relevance.
- Another ranking signal comes from historical experience: store a review log of `<tool, embedded query, reported fitness>`, and rerank tools by the "similarity-weighted aggregated fitness" from historical queries similar to the current query.
- Merge and deduplicate the semantic ranking and historical ranking; retain "None of these are correct" to continue exploration, and optionally inject a small number of random candidates, similar to epsilon-greedy, to avoid exploitation without exploration.
- Model feedback at the query-tool pair level rather than as a global tool score; later, use clustering/compression to merge similar queries into centroids, forming a more compact historical index while also supporting monitoring of tool degradation, shifts in task distribution, and potential new tool opportunities.

## Results
- The text does not provide standard benchmarks, datasets, or quantitative experimental results, so there are no verifiable figures for accuracy, success rate, latency, or cost.
- The strongest claim in the paper/article is that, under large catalogs of "hundreds to thousands of tools," Millwright can present fewer but more relevant tools using an adjustable context budget, while retaining exhaustive/paginated exploration when initial suggestions fail.
- It claims that compared with semantic RAG alone or a static tool library, it adds an online learning feedback loop based on agent usage feedback, allowing tool ranking to "get better over time," with scores that are conditioned on the query rather than being coarse global ratings.
- It also claims to support discovery of new tool opportunities: when existing tools are insufficient, it can trigger "Create a custom tool," and use the review log/index for observation, such as detecting spikes in "broken" evaluations to identify tool failures.

## Link
- [https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/](https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/)
