---
source: hn
url: https://github.com/octelium/cordium
published_at: '2026-06-14T22:47:53'
authors:
- geoctl
topics:
- kubernetes-sandbox
- zero-trust-access
- identity-based-auth
- ai-agent-workflows
- remote-development
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Show HN: Cordium – FOSS identity-based sandbox platform with zero-trust access

## Summary
Cordium is a self-hosted Kubernetes sandbox platform for developers, AI agents, and CI jobs. It combines isolated workspaces with identity-based, secretless access to internal systems.

## Problem
- Remote dev boxes and agent sandboxes still need secrets copied into the workspace for SSH, databases, and APIs.
- That creates credential sprawl and makes access control harder to audit.
- Teams also need one setup for interactive coding sessions and short-lived automated jobs.

## Approach
- Runs each workspace as a rootless container sandbox on Kubernetes.
- Defines environments in YAML with image, repo, tasks, variables, ports, and resource limits.
- Uses Octelium identity-aware proxy and per-request ABAC policies to grant access at the protocol layer, so the workspace never receives upstream credentials.
- Supports browser terminal, SSH, CLI, and gRPC, plus persistent or ephemeral workspaces.
- Uses prebuilt VolumeSnapshot templates to cut startup time for heavy environments.

## Results
- The excerpt gives no benchmark table or measured evaluation results.
- It claims workspaces can access SSH servers, databases, internal HTTP APIs, Kubernetes clusters, and mTLS services without API keys, passwords, SSH private keys, or kubeconfigs entering the sandbox.
- It claims prebuilt templates reduce cold startup from minutes to seconds.
- It supports any Kubernetes cluster, from a single-node VM to multi-node production installs, and exposes OpenTelemetry audit logs for every request.

## Link
- [https://github.com/octelium/cordium](https://github.com/octelium/cordium)
