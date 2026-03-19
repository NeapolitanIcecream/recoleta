---
source: hn
url: https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/
published_at: '2026-03-15T22:50:17'
authors:
- dnautics
topics:
- tool-selection
- agent-experience
- tool-augmented-llm
- retrieval-ranking
- multi-agent-systems
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Millwright: Smarter Tool Selection from Agent Experience

## Summary
Millwright is a large-scale tool selection approach for AI agents that uses "semantic relevance + historical usage feedback" to narrow the candidate tool set and continuously improve ranking as the agent gains experience. It also turns the tool selection process into an observable data asset for identifying bad tools, seeding cold starts, and discovering opportunities for new tools.

## Problem
- When an agent faces hundreds to thousands of tools, stuffing all tool definitions into context crowds out space for RAG, planning, and conversation history, so more efficient tool routing is needed.
- Semantic matching alone cannot reflect a tool's actual effectiveness on real tasks, and cannot adapt online to tools that look right in description but are actually unusable or broken.
- An ideal system should be able to return a small number of highly relevant tools on demand, support broader search after failure, and keep learning from usage feedback.

## Approach
- Maintain a `toolshed` index that exposes only two interfaces: `suggest_tools` to start a session and return ranked candidate tools, and `review_tools` to write back feedback after the task ends.
- `suggest_tools` first decomposes the task into atomic sub-needs, then vectorizes the query; on one hand it uses cosine similarity between the query vector and tool descriptions to produce semantic recommendations, and on the other hand it searches a historical review index for similar queries and produces historical recommendations based on the tool's aggregated fitness on similar tasks.
- Merge and deduplicate semantic and historical recommendations, and add "None of these are correct" or "Create a custom tool"; the system can also randomly inject a small number of tools for exploration, similar to an epsilon-greedy multi-armed bandit.
- `review_tools` records an append-only log of `<tool, embedded query, reported fitness>`, with feedback granularity at the "tool × query" level rather than a global score, avoiding incorrectly penalizing a tool on tasks where it is not applicable.
- The system periodically compresses the review log into an `<embedded query, tool, aggregate fitness>` index, and can merge neighboring queries by clustering per tool (for example, using a k-means-style approach) to control index size while supporting shadow testing and rollback.

## Results
- The article **does not provide experimental data or quantitative results on standard benchmarks**; it does not report accuracy, success rate, latency, cost, or numerical comparisons with Toolshed / pure semantic retrieval / Top-N strategies.
- The explicit capability claim is that, even with **128K to 1M+** context windows still being limited, Millwright reduces the context occupied by tool catalogs by showing only fewer and more relevant tools.
- Compared with approaches that only do RAG for tools, the author claims it adds "experience-driven dynamic reranking," which can continuously update tool fitness based on the agent's **four types of feedback** (`perfect`, `related`, `unrelated`, `broken`).
- The system claims to support large-scale catalog scenarios, gradually learning better routing among "**hundreds or thousands** of tools," and triggering a "create new tool" workflow when candidates are exhausted.
- At the implementation level, the author provides deployable components rather than performance numbers: example embedding models include **all-MiniLM-L6-v2 (22M parameters, 384 dimensions)**, e5, `text-embedding-3-small`; storage options include **SQLite/pg_vector**, with **Pinecone/Clickhouse** for larger scale.
- An additional claim is improved observability: through a timestamped review log, the system can identify effect changes after tool version releases, query distribution drift, and spikes in `broken` feedback, though the article does not provide concrete numerical examples.

## Link
- [https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/](https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/)
