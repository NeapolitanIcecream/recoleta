---
source: arxiv
url: http://arxiv.org/abs/2603.09100v1
published_at: '2026-03-10T02:20:35'
authors:
- Jackson Nguyen
- Rui En Koe
- Fanyu Wang
- Chetan Arora
- Alessio Ferrari
topics:
- requirements-engineering
- uml-generation
- large-language-models
- software-modeling
- llm-as-a-judge
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Class Model Generation from Requirements using Large Language Models

## Summary
This paper studies whether large language models can automatically convert natural-language requirements into UML class diagrams, and further evaluates whether LLMs can also serve as reliable reviewers of diagram quality. The authors propose a dual-validation framework of “LLM generation + LLM judging + human review” for automated modeling in requirements engineering.

## Problem
- Converting software requirements into UML class diagrams usually relies on manual work, is time-consuming, requires specialized expertise, and can easily lead to misunderstandings between requirements engineers and stakeholders.
- Existing automation methods are mostly rule-based NLP approaches, with limited ability to generalize to complex or heterogeneous domain requirements; meanwhile, the actual effectiveness and reliability of LLMs for this task still lack systematic validation.
- In many real-world scenarios, there is no standard-answer class diagram, so the question is not only “Can LLMs generate good diagrams?” but also “Can LLMs evaluate these diagrams reliably?”

## Approach
- Compare 4 generation models: GPT-5, Claude Sonnet 4.0, Gemini 2.5 Flash Thinking, and Llama-3.1-8B-Instruct, generating PlantUML class diagrams from natural-language requirements.
- Use chain-of-thought prompting to break the task into: extracting entities/attributes/associations, deciding inheritance and interfaces, completing multiplicities, and finally checking PlantUML syntax.
- Test on 8 heterogeneous datasets covering domains such as data management, recycling systems, camping, healthcare, embedded systems, inventory, pacemakers, and cyber-physical systems; requirement set sizes range from 12 to 187 items.
- Use two independent LLM judges (Grok, Mistral Small 3.1 24B) for pairwise comparisons, scoring across 5 dimensions: completeness, correctness, standards conformance, comprehensibility, and terminological consistency.
- Then use human experts for human-in-the-loop validation, combining Spearman correlation, Cohen’s kappa, significance tests, and Cohen’s d to analyze agreement between LLM judging and human judging.

## Results
- The paper claims that LLMs can generate UML class diagrams that are “structurally coherent and semantically meaningful,” and that there is “significant agreement” between LLM judging and human judging, supporting their use as both modeling assistants and evaluators in automated requirements engineering workflows.
- The experiments cover **8 datasets**, **4 generation models**, and **2 LLM judges**, with evaluation across **5 quality criteria**.
- The numbers of requirements in the datasets are: g14-datahub **67**, g04-recycling **51**, g12-camperplus **13**, UHOPE **12**, Autopilot **14**, Finite State Machine **13**, Inventory **22**, Pacemaker **187**.
- The provided text excerpt does not give specific final performance values, such as model win rates, Spearman \(\rho\), Cohen’s kappa, Cohen’s d, p-values, or human comparison scores, so precise quantitative margins cannot be reported.
- The strongest concrete conclusion currently supported is that the authors claim the dual-validation framework shows that LLM-generated UML diagrams are usable in both structural and semantic terms, and that LLM-based automatic evaluation is “highly aligned/consistent” with expert judgment.

## Link
- [http://arxiv.org/abs/2603.09100v1](http://arxiv.org/abs/2603.09100v1)
