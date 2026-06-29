---
kind: ideas
granularity: day
period_start: '2026-06-02T00:00:00'
period_end: '2026-06-03T00:00:00'
run_id: edd4390d-9f48-48dc-9b0a-7b341ee71fb4
status: succeeded
topics:
- agentic software engineering
- LLM training
- code repair
- terminal agents
- multi-agent orchestration
- developer tooling
- agent trust
tags:
- recoleta/ideas
- topic/agentic-software-engineering
- topic/llm-training
- topic/code-repair
- topic/terminal-agents
- topic/multi-agent-orchestration
- topic/developer-tooling
- topic/agent-trust
language_code: en
pass_output_id: 225
pass_kind: trend_ideas
upstream_pass_output_id: 224
upstream_pass_kind: trend_synthesis
---

# Intermediate Evidence Gates for Coding Agents

## Summary
Agentic coding work is becoming easier to improve when teams preserve intermediate evidence: suspicious lines in repair loops, explicit dependency gates in multi-agent execution, and trace quality signals for terminal-agent training. The practical work is to add small scoring and validation layers around existing agents, then compare pass rates, review load, and rework on recent tasks.

## Line-ranked repair candidates for failed coding-agent runs
A coding-agent repair loop can give the model a ranked set of likely faulty lines before it asks for another edit. FLARE shows the concrete shape: a lightweight diagnostic model scores lexical units, pools them to line-level suspiciousness, prompts refinements against the top-k lines, runs tests, and keeps the candidate with the best execution outcome. With k=10, FLARE improved Pass@1 across five base models on LiveCodeBench and BigCodeBench, while its diagnostic model reached 67% Top-1 and 89% Top-10 localization accuracy on 100 LiveCodeBench tasks.

The workflow fits teams already collecting failed agent patches in CI. Store the failing program, test output, token probabilities if available, ranked suspicious lines, generated candidates, and test outcomes. Add a small behavior check for proposed edits: Neural Change Prediction reports that mutation-output pairs can train a model to predict the likely effect of a code change, with fine-tuned GPT-4.1 reaching 95% accuracy for output-change prediction on single Python mutations. A pilot can replay recent failed generations and compare execution-only repair against line-ranked candidate search on pass rate and review minutes per accepted fix.

### Evidence
- [FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement](../Inbox/2026-06-02--flare-fine-grained-diagnostic-feedback-for-llm-code-refinement.md): FLARE reports line-level suspiciousness, top-k repair search, Pass@1 gains, and localization accuracy.
- [FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement](../Inbox/2026-06-02--flare-fine-grained-diagnostic-feedback-for-llm-code-refinement.md): The paper abstract states that top-k suspicious-region search improves iterative LLM code refinement.
- [Neural Change Prediction: Relating Software Changes to Their Effects and Vice Versa](../Inbox/2026-06-02--neural-change-prediction-relating-software-changes-to-their-effects-and-vice-versa.md): Neural Change Prediction reports training on mutation-output pairs and high accuracy for predicting behavior effects of code changes.

## Dependency-graph dispatch with planning and code score gates for agent-written changes
Multi-agent coding runs should expose task dependencies before implementation starts. SPOQ gives a concrete operating pattern: split an epic into 1-4 hour tasks, build a DAG, dispatch independent tasks in parallel waves, and require planning and code validation gates before moving to the next stage. The reported gains are practical for teams with limited model concurrency: SPOQ measured a stable 1.4x speedup on a 2-slot real LLM backend and raised test pass rate from 91.25% to 99.75% with dual validation.

This is most useful for teams letting agents open pull requests from larger tickets. The adoption change is to add a human planning checkpoint before agents code, then require a scored code gate after each task. The human role is specific: approve task splits, resolve ambiguous requirements, and review risky design choices. A broader synthesis cites 456,535 agent-authored pull requests across 61,453 repositories, while also reporting lower merge rates and fewer structural changes for agent-authored pull requests. That pattern supports adding gates around agent work where mergeability and design fit matter.

### Evidence
- [SPOQ: Specialist Orchestrated Queuing for Multi-Agent Software Engineering](../Inbox/2026-06-02--spoq-specialist-orchestrated-queuing-for-multi-agent-software-engineering.md): SPOQ describes DAG task decomposition, parallel waves, validation gates, human participation, and reported speed and pass-rate results.
- [SPOQ: Specialist Orchestrated Queuing for Multi-Agent Software Engineering](../Inbox/2026-06-02--spoq-specialist-orchestrated-queuing-for-multi-agent-software-engineering.md): The abstract details 1.4x speedup on a 2-slot backend, dual validation gains, and deployment-scale results.
- [Human-AI Collaboration and the Transformation of Software Engineering Work](../Inbox/2026-06-02--human-ai-collaboration-and-the-transformation-of-software-engineering-work.md): The synthesis cites large-scale agent-authored pull request evidence and identifies human specification, verification, and governance needs.

## Trace quality gates for terminal-agent fine-tuning data
Terminal-agent training data should be selected by whether the trace shows useful inspect-act-verify behavior. The terminal-agent study found that a lower-scoring teacher, DeepSeek-V3.2, trained stronger Qwen3 students than Claude Opus 4.6 because its traces exposed more environment-grounded steps. Masking observation-command links cut Targeted Observation Ratio from 13.4% to 5.3% and dropped Qwen3-32B performance from 20.6% to 13.8%.

A training team can turn this into a trace gate. Log file inspections, commands, test runs, error messages, and the path or state each command depends on. Score each successful trajectory for Targeted Observation Ratio, keep high-TOR traces at fixed data budgets, and flag traces where an action has no visible supporting observation. EvoTrainer points in the same operational direction for long-horizon software agents: its trainer reads rollouts, logs, configs, code diffs, and metrics, then updates diagnostics when current evidence cannot explain outcomes. The cheap validation is an SFT run on matched successful traces split by TOR and measured on Terminal-Bench-style tasks.

### Evidence
- [What Makes Interaction Trajectories Effective for Training Terminal Agents?](../Inbox/2026-06-02--what-makes-interaction-trajectories-effective-for-training-terminal-agents.md): The terminal-agent study defines Targeted Observation Ratio and reports stronger student performance from traces with inspect-act-verify behavior.
- [What Makes Interaction Trajectories Effective for Training Terminal Agents?](../Inbox/2026-06-02--what-makes-interaction-trajectories-effective-for-training-terminal-agents.md): The abstract describes environment-grounded supervision and data efficiency from Terminal-Lego trajectories.
- [EvoTrainer: Co-Evolving LLM Policies and Training Harnesses for Autonomous Agentic Reinforcement Learning](../Inbox/2026-06-02--evotrainer-co-evolving-llm-policies-and-training-harnesses-for-autonomous-agentic-reinforcement-learning.md): EvoTrainer describes training-side diagnostics over rollouts, logs, configs, and code diffs for agentic RL decisions.
