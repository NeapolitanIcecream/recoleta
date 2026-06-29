---
source: arxiv
url: http://arxiv.org/abs/2604.13109v1
published_at: '2026-04-11T03:22:21'
authors:
- Worasait Suwannik
topics:
- agentic-coding
- code-intelligence
- ai-for-research
- algorithm-optimization
- software-reproduction
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Applying an Agentic Coding Tool for Improving Published Algorithm Implementations

## Summary
The paper proposes a two-stage workflow that uses one model to find suitable recent papers and Claude Code to reproduce and improve their released implementations. Across 11 published algorithm implementations, the authors report an improvement in every case within one working day, but they also state that the results were not independently verified outside the agent environment.

## Problem
- Many research papers now release code and data, but there is little evidence on whether an agentic coding tool can take a published implementation, reproduce it, and push it past the reported baseline.
- This matters because published implementations are a large pool of concrete, runnable targets for AI-assisted research, replication, and incremental algorithm improvement.
- The paper also asks what work still needs a human when the agent can search, code, run experiments, and log iterations.

## Approach
- The workflow has two stages: a discovery stage and an improvement stage.
- In discovery, ChatGPT Deep Research searches for papers that meet explicit filters: Python or C++ code on GitHub, public datasets, runs that can finish on at least two datasets within about 30 seconds, and publication after 2021 in a Q1 or Q2 journal.
- In improvement, Claude Code reads the paper PDF, picks one metric-dataset pair, reproduces the baseline, then iterates on the implementation for up to 20 runs while saving code, results, and a short plan for each run.
- The agent stops once it beats the paper's reported result on the chosen target. The log files are meant to make each experiment auditable.
- The study applies this process to 11 domains, including combinatorial optimization, explainable AI, pattern mining, image segmentation, data streaming, distributed systems, network security, graph ML, molecular simulation, computational physics, and bioinformatics.

## Results
- The main claim is 11 out of 11 experiments showed an improvement over the selected published baseline, and each reported improvement was reached within a single working day.
- Reported quantitative gains include 193x faster runtime in combinatorial optimization, 6.4x faster runtime in pattern mining, more than 1000x faster image segmentation at high K with a global optimum, more than 2x faster lookup latency in distributed systems, and 10.5x typical to 34.3x large-instance speedups in bioinformatics.
- Other reported gains include an 8% accuracy improvement in graph ML, a more than doubled defense success rate in network security, higher F1 at 10 KB in data streaming, lower sparsity in explainable AI, and lower kinetic temperature error at all tested values in molecular simulation.
- The paper gives important caveats: the authors did not independently audit the generated code line by line, did not rerun results outside Claude Code's environment, and accepted the model's reported outputs as preliminary.
- Some comparisons are weaker than they look. The network security result used 50 benchmark networks versus 200 in the paper and relied on a surrogate simulator because the original engine was proprietary. In graph ML, the gain came from replacing the original method and the agent ran 38 iterations even though the prompt set a 20-run cap.
- The paper's broader claim is that human work still matters for target selection, checking whether the experiment is valid, judging novelty and impact, providing compute and access, managing execution risk, and writing disclosures.

## Link
- [http://arxiv.org/abs/2604.13109v1](http://arxiv.org/abs/2604.13109v1)
