---
source: hn
url: https://www.piersonmarks.com/posts/testing-agent-written-prs-in-the-cloud
published_at: '2026-03-04T23:59:50'
authors:
- PiersonMarks
topics:
- ai-coding-agents
- preview-environments
- github-actions
- supabase
- oidc-auth
- developer-workflow
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Setting Up Preview Envs to Test Agent PRs Without Ever Pulling Locally

## Summary
This article describes a cloud-based preview testing workflow for AI coding agent PRs: each PR automatically gets its own isolated Vercel preview site and Supabase database branch, allowing reviewers to validate functionality and UX directly in the browser without pulling code locally. The key fix is using a GitHub Action to automatically populate WorkOS third-party authentication configuration on each Supabase preview branch, resolving the critical blocker where “the preview environment deploys successfully but users cannot log in.”

## Problem
- When multiple AI agents submit PRs in parallel, **testing** rather than writing code becomes the main bottleneck; pulling branches locally one by one, configuring environments, and running migrations slows down the entire async development workflow.
- Reviewing a GitHub diff alone cannot verify whether functionality actually works, especially when it comes to checking the full UX and protected routes after login.
- Supabase preview branches copy the database and policies, but **do not automatically copy third-party authentication configuration**; when using external OIDC providers such as WorkOS, preview environments lose their testing value because login does not work.

## Approach
- Build an end-to-end PR preview pipeline: Linear assigns tickets to AI agents, and after the agent submits a PR, GitHub Actions trigger a Vercel preview deployment and creation of an isolated Supabase database branch.
- Treat the “preview environment” directly as the “test environment”: each PR gets a unique URL and isolated database, avoiding conflicts in shared staging and eliminating the need for local environment setup.
- Use a GitHub Action to call the **Supabase Management API**: when a PR is opened, updated, or reopened, it polls for the corresponding Supabase preview branch, then writes the WorkOS OIDC configuration to `/v1/projects/{ref}/config/auth/third-party-auth`.
- Make the workflow **idempotent**: first check whether the target preview branch already has WorkOS configuration, and exit if it does to avoid duplicate writes; it also supports manual retries via `workflow_dispatch`.
- Because Supabase preview branch creation is delayed, the script uses polling with up to **5 retries, 10 seconds apart** to wait for the branch to become visible.

## Results
- The article claims to achieve a “**fully async**” agent PR testing workflow: from assigning a ticket, to the agent submitting a PR, to the reviewer clicking the preview link to validate functionality, the entire process requires **no local code checkout**.
- Each PR gets an **isolated database branch** and an **independent preview URL**; the author emphasizes three direct benefits: parallel testing, no resource contention across multiple agents, and avoiding contamination of the staging database.
- The feedback loop is described as “**minutes, not hours**,” but the article **does not provide formal experimental data, benchmark datasets, or reproducible metrics**.
- The most specific technical result given is that using the Supabase Management API’s third-party authentication configuration endpoint, plus **5×10-second** polling and idempotency checks, can turn a preview environment that originally “deploys successfully but cannot log in” into one that supports full login and interactive testing.
- The method is claimed to generalize to other **OIDC** providers such as Auth0 and Clerk; however, the author also explicitly states that they **have not personally verified all alternative providers**.

## Link
- [https://www.piersonmarks.com/posts/testing-agent-written-prs-in-the-cloud](https://www.piersonmarks.com/posts/testing-agent-written-prs-in-the-cloud)
