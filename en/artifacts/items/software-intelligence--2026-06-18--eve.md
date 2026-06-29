---
source: hn
url: https://vercel.com/blog/introducing-eve
published_at: '2026-06-18T23:23:48'
authors:
- gmays
topics:
- agent-runtime
- software-agents
- human-in-the-loop
- multi-agent-systems
- developer-tools
- evals
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Eve

## Summary
Eve is an open-source TypeScript agent runtime that turns an agent into a directory of files and supplies durable sessions, sandboxes, approvals, channels, tracing, and evals. Its main value is less custom production code for teams building many agents.

## Problem
- Teams rebuild the same agent infrastructure for state, tools, credentials, logging, deployment, approvals, and channel integrations.
- Agents often run across long tasks, slow systems, and human approvals, so crashes, deploys, and unsafe actions can break production use.
- This matters because Vercel says agents now trigger around 29% of deployments on its platform, up from less than 3% a year earlier.

## Approach
- An agent is a directory: `agent.ts` sets the model, `instructions.md` sets behavior, `tools/` holds typed TypeScript tools, `skills/` holds Markdown knowledge, `subagents/` holds delegated agents, `channels/` holds integrations, and `schedules/` holds cron tasks.
- Each conversation runs as a durable workflow with checkpointed steps, so it can pause, survive a crash or deploy, and resume at the same point.
- Agent-written code runs in an isolated sandbox, using Vercel Sandbox in deployment and Docker, microsandbox, or shell adapters locally.
- Tool actions can require human approval; Eve pauses without compute use until a person approves, then resumes.
- Connections use MCP or OpenAPI files with brokered auth, and runs emit OpenTelemetry traces plus file-based evals for local and CI tests.

## Results
- Vercel says it runs more than 100 production agents on Eve and that these agents now share one monorepo, conventions, observability, and upgrade path.
- Its internal data analyst agent handles more than 30,000 questions per month in Slack, with warehouse access scoped to the asker's permissions.
- Lead Agent costs about $5,000 per year to run and returns 32× that amount, with one part-time engineer maintaining it.
- Athena was built by RevOps in 6 weeks without engineers, and pipeline coverage nearly doubled after launch.
- Vertex solves 92% of support tickets on its own and escalates the rest.
- The CLI can scaffold a first agent and reach a running dev server in under 1 minute, according to Vercel.

## Link
- [https://vercel.com/blog/introducing-eve](https://vercel.com/blog/introducing-eve)
