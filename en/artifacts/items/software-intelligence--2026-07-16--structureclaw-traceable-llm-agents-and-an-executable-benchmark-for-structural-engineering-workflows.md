---
source: arxiv
url: https://arxiv.org/abs/2607.14896v1
published_at: '2026-07-16T12:13:41'
authors:
- Sizhong Qin
- Yi Gu
- Yao Jiang
- Ao Cai
- Changjian Zhou
- Shaoxuan Shuai
- Jiachang Wang
- Tianhao Shen
- Yueqiang Li
- Xinhao Li
- Li Zeng
- Yueshi Chen
- Dachen Gao
- Genrong Xu
- Wenjie Liao
- Xinzheng Lu
topics:
- engineering-agents
- executable-benchmark
- artifact-traceability
- workflow-validation
- multimodal-reconstruction
relevance_score: 0.61
run_id: materialize-outputs
language_code: en
---

# StructureClaw: Traceable LLM Agents and an Executable Benchmark for Structural Engineering Workflows

## Summary
StructureClaw evaluates structural-engineering agents through complete, executable evidence chains rather than final answers alone. Its benchmark shows that governed skills and artifact-based workflow execution substantially improve end-to-end success, while invalid-input handling and multimodal model reconstruction remain difficult.

## Problem
- Structural-engineering requests require consistent requirements, models, validation records, solver outputs, code checks, and reports; fluent text or executable-looking code can conceal missing or inconsistent artifacts.
- Existing agent evaluations usually test isolated capabilities and do not require a complete, executable, traceable workflow.
- This matters because an engineering result is only reviewable when its computational evidence and execution history support the reported conclusion.

## Approach
- StructureClaw uses governed domain skills, typed tools, backend providers, and shared typed artifact state to preserve inspectable workflow outputs.
- A ReAct-style agent loop selects tools, updates artifacts, validates models, requests clarification, repairs errors, executes supported backends, or terminates safely when execution is unsupported or unsafe.
- The structural-model protocol records geometry, topology, materials, sections, supports, loads, combinations, units, and analysis metadata; OpenSeesPy provides the main open-source analysis backend.
- StructureClaw-Bench contains 150 controlled scenarios split evenly across standard workflows, interactive robustness, and multimodal structural-model reconstruction. A scenario succeeds only when every required routing, artifact, execution, interaction, and reporting assertion passes in one run.

## Results
- Across 10 agent-model configurations and 50 standard cases per configuration, mean Success Rate increased from 56.8% in generic-only mode to 88.6% with the automatic workflow, a 31.8-percentage-point gain. All 10 configurations improved.
- Kimi-K2.6 achieved 100.0% on the 50 standard cases; DeepSeek-V4-Flash and GLM-5.2 each achieved 96.0%. The comparison is a system-level result because it changes skill routing, structural priors, artifact expectations, and validation guidance together.
- Automatic-mode diagnostic rates were 98.0% for structural-type matching, 100.0% for skill selection, and 90.8% for model matching.
- Interactive robustness produced a mean Success Rate of 91.0%, with configuration results ranging from 88.0% to 94.0%; pooled assertion rates were 89.6% for clarification, 90.7% for avoiding invalid models, and 91.0% for withholding analysis when appropriate.
- The reported remaining weaknesses are safe handling of invalid numerical inputs and fixture-consistent reconstruction from images or DXF files. The excerpt provides no aggregate multimodal Success Rate, so multimodal performance cannot be quantified here.

## Link
- [https://arxiv.org/abs/2607.14896v1](https://arxiv.org/abs/2607.14896v1)
