---
source: arxiv
url: http://arxiv.org/abs/2603.02141v1
published_at: '2026-03-02T18:01:43'
authors:
- Tanish Singla
- Qusay H. Mahmoud
topics:
- generative-ai
- software-testing
- llm-for-code
- prompt-engineering
- fine-tuning
- literature-review
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Generative AI in Software Testing: Current Trends and Future Directions

## Summary
This paper is a review of generative AI in software testing, systematically examining its applications, advantages, and limitations in tasks such as test case generation, test oracles, test data, and prioritization. The paper emphasizes improving the testing capabilities of large models through fine-tuning and prompt engineering, and notes that this direction has gained momentum rapidly in recent years.

## Problem
- Software testing accounts for **more than 50%** of development costs, and manual testing becomes inefficient and expensive as system complexity increases and in CI/CD scenarios.
- Traditional testing often faces problems such as **insufficient coverage**, lack of test data, and reliance on human experience to guess user behavior, which affects defect detection and delivery quality.
- There is a lack of a comprehensive perspective in research specifically focused on "how generative AI can systematically improve the entire software testing lifecycle," so it is necessary to summarize the current status, opportunities, and challenges.

## Approach
- The paper uses a **literature review** method centered on four research questions: types of AI in software testing, the effectiveness of generative AI, its application potential, and its advantages and disadvantages.
- Sources searched include **Google Scholar, SpringerLink, ScienceDirect, ResearchGate, arXiv, IEEE Xplore**, with inclusion/exclusion criteria applied; the time range is **2000–2024**.
- A final set of **59** relevant papers was selected and analyzed, organizing the content around core generative AI testing tasks: test case generation, input/output and oracle generation, data generation, test prioritization, and more.
- The paper argues that there are two main mechanisms for improving the testing capabilities of generative AI: **fine-tuning** makes models better aligned with testing tasks, while **prompt engineering** enables models to produce more usable testing results under a given context.
- It also discusses applicability boundaries and risks, such as data privacy, bias, implementation complexity, and dependence on high-quality data and correct prompts.

## Results
- The review process ultimately included **59** papers; the authors note that related research grew significantly **after the emergence of OpenAI in 2019**, indicating that generative AI testing has become a rapidly growing research direction.
- The paper cites **A3Test**: after fine-tuning, compared with other pretrained generative Transformers, it achieved a **147% improvement in correctness** and a **97.2% improvement in speed**.
- The paper cites **ChatUniTest**: a prompt-engineering-only method can achieve about **59.6% code coverage**, while the other fine-tuned LLMs compared in the paper achieve about **38%–42%**.
- The paper cites work by Fan et al.: through prompt engineering, CodeX, CodeGeeX, and CodeGen improved performance by about **50%–80%** on code generation tasks in Python, Java, JavaScript, and other languages.
- The paper’s strongest overall conclusion is that generative AI can improve **test coverage, efficiency, and cost reduction**, and is especially suitable for test case generation, validation, and IoT testing; however, this is a review paper, and most of the figures come from the surveyed studies rather than from the paper’s own experiments.

## Link
- [http://arxiv.org/abs/2603.02141v1](http://arxiv.org/abs/2603.02141v1)
