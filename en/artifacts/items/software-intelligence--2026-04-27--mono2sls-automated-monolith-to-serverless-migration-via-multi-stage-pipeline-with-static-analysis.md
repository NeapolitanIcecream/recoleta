---
source: arxiv
url: https://arxiv.org/abs/2604.24550v1
published_at: '2026-04-27T14:44:07'
authors:
- Xingyan Chen
- Yuxin Su
- Zishan Su
- Yang Yu
- Zibin Zheng
topics:
- serverless-migration
- code-intelligence
- multi-agent-systems
- software-modernization
- aws-sam
- static-analysis
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Mono2Sls: Automated Monolith-to-Serverless Migration via Multi-Stage Pipeline with Static Analysis

## Summary
Mono2Sls automates migration of monolithic Flask and Express backends into deployable AWS SAM serverless applications. It combines static code analysis with four tool-using LLM agents that plan the architecture, generate Lambda code, write SAM templates, and check consistency.

## Problem
- Moving a monolith to serverless requires aligned changes across API routing, Lambda boundaries, application code, IAM, DynamoDB, Cognito, SQS/EventBridge, and SAM templates.
- Manual migration is slow and error-prone because a small mismatch between code and infrastructure can block deployment or break API behavior.
- General code assistants often lack a stable cross-artifact contract for serverless migration, so handler code, routes, permissions, and template resources can drift apart.

## Approach
- Static analysis extracts HTTP entry points, file tags, cross-file call edges, async hints, and DynamoDB schema candidates into `analysis_report.json`.
- An Architect agent turns those facts into `blueprint.json`, mapping business endpoints to Lambda functions and choosing Cognito, synchronous Lambda calls, SQS, or EventBridge where needed.
- A Code Developer agent rewrites Flask/Express handlers into Lambda handlers, adapts identity to Cognito claims, removes global state, and adds SDK calls for inter-Lambda communication.
- A SAM Engineer agent generates `template.yaml` with DynamoDB, Cognito, API Gateway, Lambda, layer, queue, and event resources, then runs `cfn-lint` through a validation tool.
- A Consistency Validator runs 11 cross-artifact checks across generated code, SAM, and the blueprint, then applies fixes and re-validates.

## Results
- The benchmark covers 6 applications, 10,478 lines of code, 76 observable business endpoints, 24 DynamoDB tables, authentication in 6/6 apps, and async patterns in 4/6 apps.
- Mono2Sls reports 100% deployment success without manual fixes across the 6 benchmark applications.
- End-to-end correctness reaches 66.1%, compared with 53.7% to 61.2% for the commercial baselines.
- API-coverage F1 reaches 98.7%, compared with 88.4% for the commercial baselines.
- The ablation study reports that static-analysis-guided architecture planning adds 23.4 percentage points to end-to-end correctness.
- The paper also claims more consistent use of AWS-native authentication and asynchronous patterns, though the excerpt does not provide the detailed per-pattern counts.

## Link
- [https://arxiv.org/abs/2604.24550v1](https://arxiv.org/abs/2604.24550v1)
