---
source: arxiv
url: http://arxiv.org/abs/2603.08190v1
published_at: '2026-03-09T10:19:13'
authors:
- Moustapha El Outmani
- Manthan Venkataramana Shenoy
- Ahmad Hatahet
- Andreas Rausch
- Tim Niklas Kniep
- Thomas Raddatz
- Benjamin King
topics:
- agentic-ai
- regression-testing
- multi-agent-systems
- retrieval-augmented-generation
- human-ai-collaboration
- software-testing
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Human-AI Collaboration for Scaling Agile Regression Testing: An Agentic-AI Teammate from Manual to Automated Testing

## Summary
This paper studies an "agentic AI teammate" for agile industrial settings that automatically converts validated manual test specifications into system-level regression test scripts while retaining human review and governance. Its core value is to increase test automation throughput and relieve the backlog from manual to automated testing without disrupting existing CI/agile processes.

## Problem
- The paper aims to solve the following problem: in agile regression testing, **manual test specifications are produced faster than executable automation scripts can be written**, causing the automation gap to keep widening and slowing feedback and release cadence.
- This matters because in Hacon's industrial environment, **manual testing still accounts for 82–87%**, and its absolute volume **grows by 10–20% per release**; meanwhile, automation coverage increases by only **1–2%** per release, indicating that the team cannot keep up with changing requirements through purely manual effort.
- Existing LLM/test-generation research often lacks industrial-grade attention to **maintainability, assertion quality, project conventions, human collaboration, and governance**, making it difficult to deploy directly in real agile teams.

## Approach
- The core method is a **retrieval-augmented generation (RAG) + bounded multi-agent workflow**: it retrieves relevant examples from historical "test specification-script" pairs, then lets the AI draft test scripts first.
- The system includes multiple roles: **Generator** produces candidate scripts, **Evaluator** checks syntax/executability/step coverage/semantic correctness based on Jenkins execution logs and an evaluation matrix, and **Reporter** generates Markdown reports for test managers and test engineers.
- The operating mechanism is straightforward: validated test specifications exported from Jira/Xray are placed into an input directory, Copilot asynchronously batch-generates scripts and executes them in a Jenkins environment; if the results are not good enough, it continues the "generate-execute-evaluate" loop within a preset iteration limit.
- The human-AI collaboration design emphasizes **limited AI autonomy with humans as the final gatekeepers**: the AI cannot directly merge outputs into the regression suite, and test engineers must review the scripts, logs, reports, and MLflow tracking information before deciding to accept, refactor, or rewrite them.
- The solution is designed as a "**silent teammate**," meaning it asynchronously prepares first drafts before a sprint begins, without interrupting engineers' daily work, while keeping the process traceable, configurable, and extensible.

## Results
- The evaluation is based on **61 test specifications** covering **6 functional domains**; each case averages about **6 steps** (range **2–18**) with story points of **3–8**. Among them, **46 AI-generated scripts** were assigned to **5 test engineers** for review and refactoring, and another **10 representative scripts** underwent manual semantic review.
- In terms of productivity, manual semantic review shows that **30–50% of the AI-generated code in each script remained unchanged after human edits**. Based on this, the paper claims that the AI significantly reduced initial authoring effort and helped narrow the gap between manual and automated testing.
- The paper does not provide more standardized quantitative results such as percentage time savings, defect rates, pass rates, or strict comparative experimental numbers against specific baseline methods; its strongest quantitative evidence is mainly the **30–50% unchanged code** figure, along with the previously noted industrial background metrics of **82–87% manual share, 1–2% automation growth, and 10–20% manual test growth**.
- In terms of quality and collaboration, even when input specifications were pre-rated **A–B (higher quality)**, the AI still produced issues due to lack of implicit domain knowledge, such as **overly literal implementations, misunderstanding business semantics, hallucinated API/method names, and failure to follow the team's clean code standards**.
- The authors position the AI output as close to **"a first draft from a junior test engineer"**: it is often partially useful functionally, but **far from being ready for direct deployment without review**; human review remains necessary to ensure maintainability, alignment with team conventions, and long-term quality.

## Link
- [http://arxiv.org/abs/2603.08190v1](http://arxiv.org/abs/2603.08190v1)
