---
source: arxiv
url: https://arxiv.org/abs/2606.24446v1
published_at: '2026-06-23T11:27:35'
authors:
- Frank Reyes
- Benoit Baudry
- Martin Monperrus
topics:
- code-repair
- ast-transformation
- dependency-updates
- coding-agents
- java-maven
- software-maintenance
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Agentic Generation of AST Transformation Rules for Fixing Breaking Updates

## Summary
BigBag generates executable Java AST transformation programs that repair compilation failures caused by breaking dependency updates. The main claim is that one generated transformation can fix multiple client projects affected by the same library update.

## Problem
- Dependency update tools such as Dependabot and Renovate can change versions, but they do not repair client code when an updated library removes methods, changes signatures, or moves types.
- Existing repair methods often produce a patch for one project, so the same API break must be fixed again in each affected project.
- This matters because Maven clients can break even on minor and patch releases, and repeated one-off repair does not scale across projects using the same library update.

## Approach
- BigBag gives a coding agent a broken Maven client project, the new dependency API documentation, a Java AST engine template, and the AST engine Javadoc.
- The agent runs `mvn compile`, reads compiler errors, writes a standalone Java transformation, applies it to the client source tree, and repeats using build feedback.
- The generated program traverses the AST, finds usages of the broken API, rewrites them to match the new API, and prints the modified source files.
- The paper tests two AST engines, Spoon v11.2.1 and JavaParser v3.27.1, with four models: GPT-5.4-mini, Qwen3-30B, DeepSeek-v3.2, and Gemini-3.1-Pro.
- BigBag re-applies each generated transformation outside the agent loop, then tests verified transformations on other projects hit by the same dependency update.

## Results
- The evaluation uses 157 compilation-failure breaking dependency updates from BUMP, covering 69 client projects and 70 libraries.
- The dataset includes 3 patch updates (1.9%), 63 minor updates (40.1%), and 91 major updates (58.0%). Major updates have a median of 5 compilation errors and a maximum of 100; minor updates have a median of 2 and a maximum of 35.
- Across 8 model-and-engine configurations, the best setup reaches a 94.3% compilable transformation rate.
- The best setup reaches a 78.6% fix rate after applying the generated transformations to the original broken clients.
- Generated transformations transfer across projects with a 33.3% cross-project fix rate overall.
- For breaking updates where all clients use the affected API element in the same way, cross-project fix rates reach 80% or higher; JavaParser generally performs better, and engine choice changes compilable transformation rate by up to 17.8 percentage points.

## Link
- [https://arxiv.org/abs/2606.24446v1](https://arxiv.org/abs/2606.24446v1)
