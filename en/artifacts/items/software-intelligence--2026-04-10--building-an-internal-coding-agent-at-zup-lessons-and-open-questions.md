---
source: arxiv
url: http://arxiv.org/abs/2604.09805v1
published_at: '2026-04-10T18:28:59'
authors:
- Gustavo Pinto
- Pedro Eduardo de Paula Naves
- Ana Paula Camargo
- Marselle Silva
topics:
- coding-agents
- enterprise-ai
- tool-design
- agent-safety
- human-oversight
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Building an Internal Coding Agent at Zup: Lessons and Open Questions

## Summary
This paper describes CodeGen, Zup’s internal coding agent, and argues that production success depends more on tool design, safety controls, state handling, and trust calibration than on prompt tuning or model choice alone.
It is a lessons paper from a real deployment, with concrete architectural and product decisions plus open research questions.

## Problem
- Enterprise teams can build coding-agent prototypes, but many fail in production because real codebases, shell access, CI/CD integration, and developer trust create risks that benchmarks do not cover.
- Common failure modes include broken or truncated file rewrites, unsafe shell actions, stale-context edits, unreliable sessions, and low developer trust.
- This matters because unreliable agents create review overhead, safety incidents, and wasted engineering time when prototypes never become daily tools.

## Approach
- Zup built CodeGen as a three-part system: a CLI executor on the developer machine, a FastAPI backend, and a central orchestration engine called Maestro that runs a ReAct-style tool loop.
- The agent gives reasoning to the LLM, while the orchestrator handles context assembly, tool dispatch, stop conditions, logging, reconnection, and safety boundaries.
- Tool design is a main part of the method: `read` enforces current context, `edit` uses targeted string replacement instead of full-file rewrites, and `shell` runs commands with layered restrictions and audit logging.
- Safety is enforced across the whole tool set, not per tool in isolation, because one tool can bypass restrictions on another if capabilities overlap.
- Human oversight is progressive: users can start in approval mode for edits and shell commands, use a planning mode to inspect proposed actions, and move to autonomous mode as trust grows.

## Results
- The paper does not report controlled benchmark gains or A/B test metrics such as pass@k, SWE-bench, or measured productivity deltas.
- It claims that improving tool descriptions, parameter schemas, and error contracts produced more reliable behavior than prompt engineering alone, but gives no numeric comparison.
- It reports a concrete design change: replacing full-file rewrites with targeted string-replacement edits reduced failures tied to truncation and omission in long files, though no rate is provided.
- The deployed system includes concrete operating parameters: Redis session memory with a 24-hour TTL, WebSocket sessions dropped after 20 minutes of inactivity, and task reconnection to resume long-running jobs.
- The paper states that developers usually begin in approval mode and later switch to autonomous mode, and that this gradual oversight model helped adoption, but it provides no adoption numbers.
- Its strongest contribution is practical evidence from a production internal agent plus a catalog of 13 design decisions and 6 open questions, rather than a new algorithm with quantified benchmark gains.

## Link
- [http://arxiv.org/abs/2604.09805v1](http://arxiv.org/abs/2604.09805v1)
