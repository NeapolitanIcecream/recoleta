---
source: arxiv
url: http://arxiv.org/abs/2604.14723v1
published_at: '2026-04-16T07:33:16'
authors:
- Sarmad Sohail
- Ghufran Haider
topics:
- enterprise-ai-safety
- tool-using-agents
- action-contracts
- access-control
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Bounded Autonomy for Enterprise AI: Typed Action Contracts and Consumer-Side Execution

## Summary
This paper argues that enterprise AI safety depends more on execution architecture than on making the model smarter. It presents BAL, a system where the model can propose actions, but typed contracts, permission checks, scoped context, validation, and optional approval gates control what can actually run.

## Problem
- Enterprise software is stateful, permission-sensitive, and multi-tenant, so LLM mistakes can cause unauthorized actions, wrong-entity edits, malformed requests, and cross-workspace execution.
- Prompting and model alignment do not solve the main operational risk when the model is too close to direct backend execution.
- The paper targets seven failure families, including unauthorized actions, tenant or workspace scope errors, ambiguous entity resolution, malformed payloads, unsafe high-impact workflows, stale or ungoverned capabilities, and direct model-to-backend mutation.

## Approach
- The core method is a bounded-autonomy layer called BAL. The model interprets intent and proposes actions, but every executable action is defined as a typed action contract owned by the enterprise application.
- Each contract includes an input schema, permission predicate, validation function, execution callback, and result format. The app publishes a governed action manifest, and BAL reasons only over that manifest.
- Capability exposure is filtered per user at runtime, so the planner only sees actions the current user is allowed to invoke under the app's real authorization system.
- Before any side effect, BAL applies validation, tenant and workspace scoping, ambiguity handling, and optional human approval for sensitive workflows.
- Execution stays on the consumer side: BAL does not mutate enterprise state directly. Approved actions run through the application’s own services, routes, authorization, and persistence layer.

## Results
- In a deployed multi-tenant enterprise application, the authors tested 25 scenario trials across 7 failure families under three conditions: manual operation, unconstrained AI with selected safety layers disabled, and full BAL.
- Full BAL completed 23 of 25 tasks with **zero unsafe executions**. The 2 incomplete tasks were contained without enterprise side effects.
- The unconstrained AI setup completed **17 of 25** tasks, worse than full BAL by **6 tasks**.
- Both AI settings were faster than manual work, with reported speedups of **13-18×** over manual operation; the introduction reports **13.5×** for the bounded-autonomy system.
- Several safeguards, including permission filtering, workspace isolation, and manifest governance, intercepted **100% of targeted violations** because they were enforced in code rather than estimated from model behavior.
- The paper reports one failure class that backend authorization could not catch on its own: **2 wrong-entity mutations** passed because the user had permission and the payload was structurally valid. The authors claim BAL's disambiguation and confirmation steps are the layer that stops this case.

## Link
- [http://arxiv.org/abs/2604.14723v1](http://arxiv.org/abs/2604.14723v1)
