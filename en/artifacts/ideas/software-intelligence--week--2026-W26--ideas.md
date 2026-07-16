---
kind: ideas
granularity: week
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-29T00:00:00'
run_id: 40bd31d8-93a9-46f7-8cda-d9269d9964ce
status: succeeded
topics:
- coding agents
- agent evaluation
- software engineering
- security
- cost control
- repository context
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering
- topic/security
- topic/cost-control
- topic/repository-context
language_code: en
pass_output_id: 291
pass_kind: trend_ideas
upstream_pass_output_id: 290
upstream_pass_kind: trend_synthesis
---

# Coding Agent Release Gates

## Summary
Coding-agent work is moving into the same review path as other production software: repository context has to be measured, agent configs need ownership and permission checks, and evaluation needs to cover follow-up edits, tool failures, artifact delivery, runtime, and cost.

## CI checks for coding-agent configuration files
Teams using Claude Code, Cursor, Copilot instructions, Aider, Codex, or Windsurf should treat agent rule files as reviewed repository artifacts. A small CI job can scan for known config paths, require an owner, reject plaintext secrets, require a declared permission tier, and record a hash of the approved prompt or rules file. The same job can flag copied configs across repositories so security and platform teams know when one stale instruction file has spread into many projects.

Rel(AI)Build gives a concrete pattern for this: SHA-256 content addressing, HMAC-stamped lockfiles, hash-chained audit logs, pre-tool permission checks, and compilation from one canonical Markdown+YAML definition into multiple IDE targets. Its public-repository study found 6,145 agent config files across 10,008 repositories, with 10.1% of tracked paths exact duplicates after fork adjustment and fewer than 1% declaring permission boundaries. The operational check is cheap: scan the company’s repositories for agent config files, count single-commit and duplicate files, then block configs that grant broad shell or write access without an owner and permission boundary.

### Sources
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): Rel(AI)Build reports duplicate agent configs, rare permission declarations, and specific control-plane mechanisms for hashes, lockfiles, audit logs, permission tiers, and target-specific compilers.
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): The paper describes treating agent definitions as a managed supply chain and enforcing tiered permissions before LLM invocation.
- [AI Agent Credential Crisis: Six Months of Incidents](../Inbox/2026-06-28--ai-agent-credential-crisis-six-months-of-incidents.md): Credential incident evidence supports keeping real secrets out of agent and integration execution paths.

## Repository-context recall tests before coding-agent rollout
Developer-tools teams can test whether a coding agent finds the files a human reviewer would expect before letting it edit a large service. The test set should include tasks whose answers depend on implementation files, registration code, dependency injection, configuration, tests, and cross-module constraints. Each task needs a gold set of relevant files and a score for full recall, since an agent can produce a plausible patch after missing the file that actually binds the behavior.

DeepDiscovery is a useful template because it starts from high-confidence task anchors and expands through code, configuration, test, dependency, and organizational links under a budget. In the reported industrial setting, it improved Full Recall Rate by 2.5 to 7.4 percentage points on medium-scale tasks and 1.6 to 9.2 points on large subprojects. On SWE-bench Verified, the equipped system reached a 78.6% solve rate, 8.2 points above its baseline. A practical first test is to annotate 20 recent internal bugs with the files reviewers touched, run the agent’s normal retrieval path, and compare recall before measuring patch quality.

### Sources
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): DeepDiscovery describes task-level context recovery across code, configuration, tests, dependencies, and organizational links, with reported recall and SWE-bench Verified gains.
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): The paper names missing implicit links such as configuration registration, dependency injection, event propagation, and cross-module constraints.
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): EnterpriseClawBench shows that enterprise-agent evaluation should include recovered inputs, preserved workspace state, delivered artifacts, runtime, token use, and cost.

## Regression and recovery suites for agent coding sessions
Agent evaluations should replay the way developers actually work after the first answer: follow-up edits, flaky or changed tools, and cost decisions around verification. A useful suite can start with accepted coding tasks, add nine follow-up refinement turns that should preserve the original tests, inject recoverable tool hazards such as renamed fields or output drift, and record which action the agent chose after failure. The score should include final tests, instruction adherence, artifact delivery, recovery choice, verifier calls, runtime, and token cost.

CodeChat-Eval found statistically significant correctness drops across all evaluated models after 10-turn refinement, with reported drops ranging from 19.2% for GPT-5 Nano to 69.2% for Llama 3.1 8B. ToolBench-X found that no evaluated model reached 0.60 overall accuracy across recoverable tool hazards, and that targeted hints recovered far more lost accuracy than extra interaction rounds. Bayesian control adds the cost angle: posterior-based orchestration helps most when verification is expensive and cheaper critics carry useful signals. A team can validate this in one sprint by converting 30 resolved tickets into replay sessions, adding two recoverable tool failures per task, and comparing the current fixed loop against a policy that chooses among critic, regeneration, verifier, and stop actions using measured costs.

### Sources
- [CodeChat-Eval: Evaluating Large Language Models in Multi-Turn Code Refinement Dialogues](../Inbox/2026-06-24--codechat-eval-evaluating-large-language-models-in-multi-turn-code-refinement-dialogues.md): CodeChat-Eval reports multi-turn refinement sessions and large functional correctness drops after follow-up edits.
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): ToolBench-X reports recoverable tool hazards, low overall model accuracy, and diagnosis and recovery choice as failure points.
- [Bayesian control for coding agents](../Inbox/2026-06-23--bayesian-control-for-coding-agents.md): Bayesian control frames coding-agent orchestration as cost-sensitive choices among critics, regeneration, verification, and stopping.
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): EnterpriseClawBench records delivered files, quality, cost, runtime, traces, and tool calls in reproducible workplace tasks.
