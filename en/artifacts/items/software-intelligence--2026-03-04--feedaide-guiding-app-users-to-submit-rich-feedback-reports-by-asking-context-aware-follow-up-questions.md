---
source: arxiv
url: http://arxiv.org/abs/2603.04244v1
published_at: '2026-03-04T16:31:55'
authors:
- Ali Ebrahimi Pourasad
- Meyssam Saghiri
- Walid Maalej
topics:
- user-feedback
- multimodal-llm
- mobile-apps
- requirements-engineering
- human-ai-interaction
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# FeedAIde: Guiding App Users to Submit Rich Feedback Reports by Asking Context-Aware Follow-Up Questions

## Summary
FeedAIde is a context-aware interactive framework for collecting mobile app feedback. It uses multimodal large language models to proactively ask for key information while users submit feedback. It aims to both lower the barrier for users to express issues and provide developers with more complete, more actionable bug reports and feature requests.

## Problem
- Mobile app users often submit feedback that is **vague and lacking context**, while developers need detailed information that is reproducible and can be prioritized.
- This information gap causes developers to repeatedly ask follow-up questions; the paper notes that about **45%** of developer replies ask for more details, while many users **never reply again** or take **hours to days** to provide additional information.
- Existing user-side feedback methods are often simple text boxes and lack immediate use of context such as **screenshots, device information, and interaction logs**, resulting in low-quality feedback and high processing costs.

## Approach
- Proposes **FeedAIde**: when a user triggers feedback, the system automatically collects context, including **screenshots, device information, app version, and recent interaction logs**.
- Uses a **Multimodal Large Language Model (MLLM)** to first generate up to **3** feedback options the user may want to express based on the context; the user can directly select one or enter their own.
- After the user makes a selection, the model then asks **2 fixed** short, context-relevant follow-up questions to fill in the information developers need most, while avoiding overly technical or overly long questions.
- It then integrates the user's answers and the context into a structured JSON report containing **userIntentSummary**, **developerSummary**, Q&A history, and context data, making it easier for developers to consume.
- The authors implemented a **Swift Package** that can be integrated into iOS apps, supports shake-to-report, and uses prompt engineering to control language, question format, privacy, and context trimming.

## Results
- Evaluated on a real internal iOS app for a gym: **7** real users, **4** feedback scenarios (**2 bugs + 2 feature requests**), and a total of **54** collected and reviewed reports.
- Compared with the original simple text form, participants subjectively considered **FeedAIde easier to use and more helpful**; the excerpt does not provide specific Likert means or significance test values.
- **2 industry experts** assessed the quality of **54 reports** and concluded that FeedAIde improved the quality of both **bug reports** and **feature requests**, especially in terms of **completeness**.
- The paper does not report more detailed quantitative metrics in the provided excerpt (such as average scores, effect sizes, or p-values); the strongest concrete conclusion is that, compared with a traditional text box, reports produced by FeedAIde were judged by experts to be **higher quality and more complete**.
- The authors also note limitations: the system can still be improved, for example by making follow-up questions better probe **root causes** rather than focusing too much on surface-level solutions proposed by users.

## Link
- [http://arxiv.org/abs/2603.04244v1](http://arxiv.org/abs/2603.04244v1)
