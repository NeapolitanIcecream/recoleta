---
source: arxiv
url: https://arxiv.org/abs/2607.11390v1
published_at: '2026-07-13T10:54:38'
authors:
- Minase Mekete Mengistu
- Juri Di Rocco
- Phuong T. Nguyen
- Davide Di Ruscio
topics:
- infrastructure-as-code
- llm-agents
- automated-repair
- cloud-security
- terraform
- tool-grounding
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# TerraRepair: A Tool-Grounded LLM Agent for Infrastructure-as-Code Repair

## Summary
TerraRepair uses an LLM agent with Terraform dependency retrieval, installed provider schemas, scanner feedback, and structured escalation to repair cloud security findings. On the studied benchmarks, it raises scanner-verified AWS repair rates by 51.8 percentage points for Checkov and 27.6 points for Trivy over a one-shot baseline, while missing deployment-specific context limits full autonomy.

## Problem
- Terraform security scanners identify misconfigurations, but developers still need to create valid repairs that preserve security intent and match the installed cloud provider schema.
- One-shot LLM repair can invent unsupported Terraform constructs, introduce validation errors, or claim success after only suppressing a scanner warning.
- The problem matters because invalid or semantically unsafe infrastructure changes can reach deployment despite passing basic scanner checks.

## Approach
- TerraRepair runs a single ReAct-style agent for each scanner finding with a ten-step repair limit.
- The agent queries a dependency graph for cross-resource values, retrieves the installed Terraform provider schema, proposes one resource-block patch, and re-runs the scanner on that patch.
- The system returns a scanner-verified repair only after the original finding clears; it emits a structured escalation when required deployment-specific information is unavailable or the process does not converge.
- The evaluation compares TerraRepair with a controlled one-shot baseline using the same model, scanner versions, finding sets, patching logic, and final rescanning procedure across TerraGoat and KaiMonkey, AWS, Azure, and GCP.

## Results
- On the combined AWS benchmark, TerraRepair reaches 78.4% +/- 0.8% scanner-verified fixes with Checkov versus 26.6% +/- 1.4% for the baseline, a gain of 51.8 percentage points.
- With Trivy, TerraRepair reaches 72.4% +/- 4.0% versus 44.8% +/- 1.4%, a gain of 27.6 percentage points.
- The baseline claimed-versus-verified gap ranges from 44.8 to 73.6 percentage points; TerraRepair reduces it to -2.9 to +1.8 points.
- In a semantic audit of 171 scanner-verified AWS repairs, 135 were judged correct by majority vote, or 78.9% with a 95% confidence interval of 72.2% to 84.4%; Fleiss' kappa was 0.54.
- Removing schema lookup lowers the Checkov fix rate by 21.7 points, and removing dependency-graph retrieval lowers it by 15.6 points on TerraGoat AWS; removing scanner feedback lowers it by 1.1 points.
- TerraRepair escalates 25.4% of findings across the full evaluation, with missing external deployment context accounting for 82.7% of escalations. It introduces zero new Terraform validation errors on AWS, but 26 new errors occur in Azure and GCP repairs.

## Link
- [https://arxiv.org/abs/2607.11390v1](https://arxiv.org/abs/2607.11390v1)
