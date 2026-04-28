---
kind: trend
trend_doc_id: 410
granularity: day
period_start: '2026-04-14T00:00:00'
period_end: '2026-04-15T00:00:00'
topics:
- coding-agents
- evaluation
- repository-context
- multi-agent-workflows
- code-editing
run_id: materialize-outputs
aliases:
- recoleta-trend-410
tags:
- recoleta/trend
- topic/coding-agents
- topic/evaluation
- topic/repository-context
- topic/multi-agent-workflows
- topic/code-editing
language_code: en
pass_output_id: 70
pass_kind: trend_synthesis
---

# Real repository evidence is the standard that current coding agents still fail to meet

## Overview
The strongest signal for this day is that coding research is tightening around evidence that can be checked in real repositories. CodeSpecBench, R²Eval, and Ace point to the same constraint from different angles: semantic understanding, repository context, and team coordination still limit current coding agents more than raw generation speed.

## Clusters

### Evaluation is moving past final-answer scoring
Benchmarks on this day keep asking a stricter question: does a model capture program intent, and can it explain that intent with checkable evidence. CodeSpecBench tests executable preconditions and postconditions, and the best repository-level pass rate is 20.2% on 500 SWE-bench Verified issues. CodeRQ-Bench then grades the reasoning itself. Its VERA evaluator beats prior judges across generation, summarization, and classification tasks, with gains up to 0.26 AUCROC. The message is practical: output quality alone still hides large semantic and reasoning gaps.

#### Evidence
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md): Executable specification benchmark and repo-level pass rates.
- [Beyond Output Correctness: Benchmarking and Evaluating Large Language Model Reasoning in Coding Tasks](../Inbox/2026-04-14--beyond-output-correctness-benchmarking-and-evaluating-large-language-model-reasoning-in-coding-tasks.md): Reasoning-quality benchmark and VERA gains over prior evaluators.

### Real repositories keep breaking benchmark confidence
Repository context is still where coding models lose most of their apparent skill. R²Eval builds input and output prediction tasks from ten real Python projects and shows average accuracy collapsing from 81.23% to 16.91% on input prediction and from 80.37% to 28.15% on output prediction versus CRUXEval. CodeSpecBench shows the same pattern in another form: function-level spec generation can approach 47.0% pass rate, while repo-level performance stays near 20%. The broad result is consistent across task formats. Real project structure, dependencies, and object-heavy state remain hard.

#### Evidence
- [Evaluating LLMs Code Reasoning Under Real-World Context](../Inbox/2026-04-14--evaluating-llms-code-reasoning-under-real-world-context.md): Real-project reasoning benchmark with large drops versus CRUXEval.
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md): Function-level versus repo-level specification results.

### Multi-agent coding is turning into workflow infrastructure
Agent work is also getting modeled as a coordination problem, not just a generation problem. Ace puts people and agents in one realtime workspace with shared chat, prompt history, previews, and cloud sessions, and frames team alignment as the bottleneck when many agents run in parallel. OpenRig approaches the same issue from local operations: define a mixed-agent team in YAML, run it in managed tmux sessions, inspect topology, and restore it after shutdown. Claude Code source analysis adds the architectural layer underneath this trend. The paper argues the agent loop itself is simple, while most system complexity sits in permissions, context compaction, extensibility, delegation, and persistence.

#### Evidence
- [One Developer, Two Dozen Agents, Zero Alignment](../Inbox/2026-04-14--one-developer-two-dozen-agents-zero-alignment.md): Multiplayer coding workspace centered on shared context and planning.
- [Show HN: OpenRig – agent harness that runs Claude Code and Codex as one system](../Inbox/2026-04-14--show-hn-openrig-agent-harness-that-runs-claude-code-and-codex-as-one-system.md): Local harness for mixed-agent teams, topology control, and restore.
- [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems](../Inbox/2026-04-14--dive-into-claude-code-the-design-space-of-today-s-and-future-ai-agent-systems.md): Source-based breakdown of where coding-agent system complexity actually lives.

### Project-wide editing rewards explicit tool use
Cross-file editing is becoming a tool-routing problem. TRACE mixes neural prediction with IDE and language-server tools such as rename and def-use analysis, then decides when tool calls are better than broad neural search. On 38K commits across 678 projects, it improves edit-location precision by 43.76%, recall by 9.96%, and edit-generation accuracy by 11.16% over prior systems. Its interactive simulation also reports 27.71% suggestion acceptance with lower time cost. That is a concrete sign that project-wide editing benefits from explicit structure around the model, not just a larger context window.

#### Evidence
- [Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction](../Inbox/2026-04-14--learning-project-wise-subsequent-code-edits-via-interleaving-neural-based-induction-and-tool-based-deduction.md): Hybrid neural-plus-tool system for project-wide subsequent edits with measured gains.
