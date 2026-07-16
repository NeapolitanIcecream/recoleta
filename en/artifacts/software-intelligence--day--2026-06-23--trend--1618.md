---
kind: trend
trend_doc_id: 1618
granularity: day
period_start: '2026-06-23T00:00:00'
period_end: '2026-06-24T00:00:00'
topics:
- coding agents
- software engineering
- agent safety
- secure code generation
- research automation
run_id: materialize-outputs
aliases:
- recoleta-trend-1618
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/secure-code-generation
- topic/research-automation
language_code: en
pass_output_id: 278
pass_kind: trend_synthesis
---

# Coding agents need census data, cost controls, and security evidence

## Overview
This period is dominated by coding-agent accountability: measuring real usage, controlling tool costs, and checking security after code runs. The strongest evidence comes from the 180M-repository census, Bayesian control, and BigBag; product items add governance needs with less evaluation.

## Findings

### Open-source agent activity measurement
The clearest empirical signal is the multi-method census of AI coding agents across more than 180 million Git repositories. It shows that bot-account lookup alone misses most activity. For Claude Code in the V2510 snapshot, the multi-method scan finds 850,157 commits, while bot-account lookup finds 28,154. The V2604 snapshot attributes 1,772,677 commits to agents, with Claude Code accounting for half. This gives supply-chain studies a stronger base than single-channel traces such as pull requests, bot names, or configuration files alone.

#### Sources
- [Detecting AI Coding Agents in Open Source: A Validated Multi-Method Census of 180 Million Repositories](../Inbox/2026-06-23--detecting-ai-coding-agents-in-open-source-a-validated-multi-method-census-of-180-million-repositories.md): Summary reports the 180M-repository census, four detection channels, commit counts, and recall gaps.

### Cost-aware coding-agent orchestration
Agent work is being treated as a control problem with explicit costs. The Bayesian control paper keeps a posterior belief that a candidate program will pass verification, then decides whether to run cheap critics, regenerate, verify, or stop. Its evaluation spans six generators and nine coding benchmarks. The reported gains are strongest when verification is expensive and cheaper critics give imperfect signals. BigBag applies a related discipline to dependency repair: it asks an agent to generate executable Java abstract syntax tree transformations, then reuses those transformations across clients affected by the same library update. The best setup reaches a 78.6% fix rate on original broken clients and a 33.3% cross-project fix rate overall.

#### Sources
- [Bayesian control for coding agents](../Inbox/2026-06-23--bayesian-control-for-coding-agents.md): Summary gives the Bayesian controller, action choices, evaluation scale, and high-verification-cost result.
- [Agentic Generation of AST Transformation Rules for Fixing Breaking Updates](../Inbox/2026-06-23--agentic-generation-of-ast-transformation-rules-for-fixing-breaking-updates.md): Summary gives BigBag’s AST transformation workflow, dataset size, fix rate, and transfer results.

### Security checks for agent-written software
Security work in the corpus asks for executable proof and readable controls. Kauge separates secure-coding knowledge, code actuation, and the gap between them, using OWASP and CERT principles plus exploit tests. The paper reports that models often know the relevant principle yet fail to put the defense at the right boundary. AutoSpec addresses a different part of the safety problem. It revises symbolic safety rules for large language model (LLM) agents using labeled execution traces, then keeps edits that improve trace-level scores. On 291 traces across code-execution and embodied-agent domains, it reports F1 scores of 0.98 and 0.93 and up to 94% false-positive reduction. Postman Passport adds a product-side example: API callers receive credential references, while real keys stay in the customer vault and are resolved through a proxy with scope checks.

#### Sources
- [SoK: AI Secure Code Generation: Progress, Pitfalls, and Paths Forward](../Inbox/2026-06-23--sok-ai-secure-code-generation-progress-pitfalls-and-paths-forward.md): Summary describes Kauge’s knowledge, actuation, and gap layers, plus the reported knowledge-actuation gap.
- [AutoSpec: Safety Rule Evolution for LLM Agents via Inductive Logic Programming](../Inbox/2026-06-23--autospec-safety-rule-evolution-for-llm-agents-via-inductive-logic-programming.md): Summary gives AutoSpec’s rule-edit method, trace count, F1 scores, and false-positive reduction.
- [Postman launches passport for securing API secret access](../Inbox/2026-06-23--postman-launches-passport-for-securing-api-secret-access.md): Summary describes Passport’s credential-reference design and proxy-based scope checks.

### Research and documentation agents at scale
Several items apply multi-agent systems to research and software knowledge work. Agon runs reusable producer-critic loops for ideas, proposals, experiments, and papers. Its evidence is operational scale: 444 loop iterations, 18 roles, projects across more than 10 scientific domains, and a month of dispatcher operation. The paper is careful that claim judgment still needs humans. LLM4MTLs adds a smaller, more testable software-engineering case. It evaluates generated model transformation language code across 47 examples, four languages, and three large language models. Few-shot examples improve syntax across all four languages, while semantic correctness depends on the language and task.

#### Sources
- [Agon: An Autonomous Large-Scale Omnidisciplinary Research System Built on Prompt Economy](../Inbox/2026-06-23--agon-an-autonomous-large-scale-omnidisciplinary-research-system-built-on-prompt-economy.md): Summary reports Agon’s producer-critic loops, operating scale, and lack of quantitative claim-validity benchmarks.
- [LLM4MTLs: Automated Generation and Empirical Evaluation of Model Transformation Languages](../Inbox/2026-06-23--llm4mtls-automated-generation-and-empirical-evaluation-of-model-transformation-languages.md): Summary gives LLM4MTLs’ evaluation setup and the split between syntactic gains and uneven semantic correctness.
