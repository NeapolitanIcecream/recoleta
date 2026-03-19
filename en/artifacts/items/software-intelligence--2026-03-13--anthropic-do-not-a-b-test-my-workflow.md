---
source: hn
url: https://backnotprop.com/blog/do-not-ab-test-my-workflow/
published_at: '2026-03-13T23:55:19'
authors:
- ramoz
topics:
- ai-tooling
- ab-testing
- developer-workflow
- transparency
- human-in-the-loop
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Anthropic, Do Not A/B Test My Workflow

## Summary
This article is not an academic paper, but a critical case analysis of the experimental design of the Claude Code product. The author argues that implicit A/B testing on core workflows harms the experience of professional users, and advocates for greater transparency, configurability, and opt-out mechanisms in AI development tools.

## Problem
- The article discusses the following problem: when AI coding tools conduct A/B tests on **core workflows** (such as plan mode) without clearly informing users or obtaining consent, it can cause users' workflows to degrade.
- This matters because Claude Code is used as a **paid professional productivity tool**; silent changes to core behavior directly affect engineers' efficiency, trust, and sense of control.
- The author further points out that a lack of transparency prevents users from determining whether performance regressions come from the model, product changes, or experiment assignment, thereby weakening “human-in-the-loop” control.

## Approach
- The article uses a case-analysis approach based on **personal experience + product feedback + developer responses**, rather than formal experimental research.
- The author observed that plan mode output deteriorated from relatively contextualized plans into **brief bullet lists**, then followed up on the cause, concluding that the system prompt contained constraints such as **capping plans at 40 lines, forbidding a context section, and prioritizing the removal of prose**.
- The article quotes a response from a Claude Code engineer in a public discussion: the experiment’s hypothesis was that **shortening plans** could reduce rate-limit hits while maintaining similar task outcomes.
- The engineer explained that the test covered “thousands of users,” and that the author’s group was the **most aggressive variant**, which limited plans to **40 lines**.
- The core mechanism can be understood simply as follows: the product team modified the length and formatting constraints of the plan-mode prompt to test whether shorter plans could reduce resource consumption without clearly harming task completion outcomes.

## Results
- **No formal, systematic quantitative evaluation metrics are provided** (such as success rate, task completion time, or code quality scores); therefore, the evidence in this text is mainly case-level and narrative.
- The only explicit experimental parameter is that the most aggressive variant limited plans to **40 lines** and removed more contextual phrasing.
- The engineer claimed the experiment covered **thousands of users**, indicating that this was not an isolated anomaly but a larger-scale online product experiment.
- The engineer’s reported early result was: **“Early results aren’t showing much impact on rate limits so I’ve ended the experiment.”** That is, in their observation, the improvement to **rate limits** was **not significant / had no clear effect**, so the experiment was ended.
- The author’s strongest claim is that the experiment **significantly worsened their personal workflow experience**, especially by reducing plan interpretability, contextual richness, and user confidence; however, the article does not provide reproducible numerical evidence to quantify this degradation.

## Link
- [https://backnotprop.com/blog/do-not-ab-test-my-workflow/](https://backnotprop.com/blog/do-not-ab-test-my-workflow/)
