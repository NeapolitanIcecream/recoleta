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
- test-automation
- rag
- human-ai-collaboration
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# Human-AI Collaboration for Scaling Agile Regression Testing: An Agentic-AI Teammate from Manual to Automated Testing

## Summary
This paper studies how to convert large volumes of manual test specifications into executable regression test scripts more quickly in industrial agile development. The authors propose an “AI teammate” with retrieval augmentation and a multi-agent workflow, used to first generate reviewable script drafts and then have humans provide oversight.

## Problem
- The problem to solve is that manual test specifications are produced faster than automation scripts can be written, causing regression automation coverage to lag behind the release cadence, increasing the burden of manual testing and slowing the feedback loop.
- This is important because in this industrial setting, automated coverage grows by only **1–2%** per release, while manual testing still accounts for **82–87%** of the total, and the absolute number of manual tests also increases by **10–20%** per release.
- Existing LLM/test generation methods typically overlook maintainability, assertion quality, project conventions, and human-AI collaboration and governance requirements in real teams.

## Approach
- The core method is a **retrieval-augmented generation (RAG) + bounded multi-agent workflow** test automation Copilot: it generates initial drafts of system-level test scripts directly from validated test specifications.
- Put simply, it first retrieves similar cases from historical “specification-script” examples, then a generation agent writes the script, the script is executed in Jenkins, an evaluation agent judges usability based on the logs, and finally a reporting agent organizes the results for review by test managers and test engineers.
- The workflow is asynchronous and batch-based: at the start of a sprint, the team exports Jira/Xray specifications to JSON, the AI pre-generates scripts, execution logs, Markdown reports, and MLflow tracking records, and humans then decide whether to accept, revise, or rewrite them.
- This mechanism emphasizes **final human approval**: the AI cannot directly merge outputs into the regression test suite, and all outputs have traceable records to satisfy governance and audit requirements.

## Results
- The evaluation is based on **61** test specifications covering **6** functional domains, with an average of about **6** steps per case (range **2–18**) and about **3–8** story points; among these, **46** AI-generated scripts were reviewed and refactored by **5** test engineers, and **10** of those scripts additionally received semantic-level manual re-review.
- The main breakthrough claimed by the authors is a productivity gain: manual semantic review shows that about **30–50%** of the AI-generated code in each script ultimately required **no modification**, indicating that the AI significantly reduced the initial authoring workload.
- The paper does not provide more standardized quantitative metrics, such as exact labor hours saved, pass rates, defect rates, or statistically significant comparisons against a human baseline; the clearest quantitative evidence is mainly the **30–50% share of unchanged code**.
- Qualitative results show that even when input specifications were pre-rated as relatively high quality (**A–B**), the AI still produced overly literal misunderstandings because of implicit domain knowledge and team conventions, and also generated hallucinated method names/API names and code that did not conform to the team’s clean code standards.
- The authors position the AI output as roughly a “**first draft from a junior test engineer**”: often functionally usable, but usually **not ready for direct production use**, still requiring human review and correction for semantic correctness, code style, reusable fragments, and report actionability.

## Link
- [http://arxiv.org/abs/2603.08190v1](http://arxiv.org/abs/2603.08190v1)
