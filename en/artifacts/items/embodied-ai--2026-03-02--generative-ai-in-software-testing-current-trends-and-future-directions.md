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
- llm-for-testing
- prompt-engineering
- fine-tuning
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Generative AI in Software Testing: Current Trends and Future Directions

## Summary
This is a review paper on the current state and future directions of generative AI applications in software testing. The paper systematically examines the potential, methods, and challenges of generative AI in tasks such as test case generation, test data, test oracles, and test prioritization.

## Problem
- Software testing is costly and labor-intensive; the paper notes that it can account for **more than 50%** of development costs, and it is even harder to scale in continuous integration/continuous delivery environments.
- Traditional manual testing and scripted automation often face problems such as **insufficient coverage, lack of test data, and low efficiency**, making it difficult to keep up with growing software complexity.
- Although there has already been research on using AI for testing, there has been a lack of a comprehensive review specifically focused on **why generative AI is suitable for software testing, what exactly it can do, and what gaps still remain**.

## Approach
- The paper uses a **literature review/systematic survey** approach rather than proposing a new testing algorithm; it analyzes four research questions around AI types, the effectiveness of generative AI, its application potential, and its advantages and disadvantages.
- The authors retrieved literature from sources such as **Google Scholar, ScienceDirect, arXiv, IEEE Xplore**, and applied predefined inclusion/exclusion criteria to select English-language materials related to software testing from the time range **2000–2024**.
- A total of **59** papers were ultimately included, and the applications of generative AI in testing were organized by topic, including **test case generation, input generation, oracle generation, test data creation, test case prioritization**, among others.
- The paper further summarizes two core mechanisms: **fine-tuning** (adapting pretrained LLMs with testing/code data to better suit testing tasks) and **prompt engineering** (using better prompts to make the model generate more usable testing results).
- The core idea can be simply understood as enabling large language models to “understand requirements and code,” then automatically generate testing-related content, and improve usability through validation, repair, and iteration.

## Results
- This is a review paper and **does not provide a unified self-built experimental benchmark**; its main results come from representative figures and trend summaries in the reviewed literature.
- After literature screening, **59** relevant papers were included in total; the authors state that **after 2019**, with the rise of OpenAI-related models, the number of related publications increased significantly.
- In the cited work, after fine-tuning, **A3Test** reportedly achieved **147% higher correctness** and **97.2% higher speed** compared with other pretrained generative Transformers.
- In the cited work, **ChatUniTest** used prompt engineering and an automated repair pipeline, reporting **about 59.6% code coverage**, while other fine-tuned LLMs mentioned in the paper achieved around **38%–42%**.
- The paper also cites Fan et al.’s conclusion that, through prompt engineering, code-generation-related performance on **CodeX, CodeGeeX, CodeGen** can improve by **50%–80%**, covering languages such as **Python, Java, JavaScript**.
- The paper’s strongest conclusion is that generative AI has clear potential to improve test coverage, efficiency, and cost control, but it is still constrained by factors such as **prompt quality, data privacy, implementation complexity, bias, and data requirements**.

## Link
- [http://arxiv.org/abs/2603.02141v1](http://arxiv.org/abs/2603.02141v1)
