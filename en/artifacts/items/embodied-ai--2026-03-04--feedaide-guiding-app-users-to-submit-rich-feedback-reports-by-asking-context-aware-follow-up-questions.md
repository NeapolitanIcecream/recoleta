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
- context-aware
- mobile-apps
- interactive-reporting
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# FeedAIde: Guiding App Users to Submit Rich Feedback Reports by Asking Context-Aware Follow-Up Questions

## Summary
FeedAIde is a context-aware interactive system for mobile app feedback collection. It uses multimodal large language models to ask follow-up questions based on screenshots and interaction context, helping users submit more complete feedback with greater value for developers. The paper presents an iOS framework implementation and validates its usability and improvements in report quality through user testing and expert review in a real gym staff app.

## Problem
- Mobile app user feedback is often **vague, lacks context, and is not actionable enough for developers**, forcing developers to repeatedly ask follow-up questions and increasing communication costs.
- The paper notes that about **45%** of developers’ replies to app store reviews ask for more details, while many users **never reply again**, or only respond after **hours to days**.
- Existing user-side feedback support methods do not combine GenAI with context such as **screenshots, device information, and interaction logs** to guide users in filling in key information at the moment of submission.

## Approach
- The core method is simple: when a user initiates feedback, the system first automatically collects context such as **screenshots, device information, app version, and interaction logs**, then lets the MLLM infer what the user may want to report.
- The system first generates up to **3** context-related feedback candidates for the user to choose from or replace with their own input; it then asks a fixed set of **2** brief adaptive follow-up questions to fill in the information developers need most.
- The prompt design is divided into three parts: **system settings/constraints**, **app description**, and **dynamic contextual information**, with an emphasis on sending only the most relevant context to avoid wasting tokens, misleading the model, and overexposing private data.
- The final model output is a structured JSON report containing a **user intent summary, developer summary, Q&A history, and contextual data**, making it easier for developers to process directly.
- The authors implemented a reusable **iOS Swift Package** supporting trigger methods such as shake-to-report, and integrated different LLM providers through an adapter library.

## Results
- The system was evaluated in a production gym staff iOS app; **7** real users participated in a within-subject study, each completing **4** feedback scenarios (**2 bug reports + 2 feature requests**).
- The developer-value evaluation was based on **54** reports collected during user testing and reviewed for quality by **2** industry experts; the conclusion was that FeedAIde improved the quality of both **bug reports and feature requests**, especially in terms of **completeness**.
- Compared with the app’s original simple text feedback form, participants subjectively rated FeedAIde as **easier to use and more helpful**; the summary does not provide specific scale scores or significance test values.
- The paper provides a real deployment context: the app had been in use for **more than 1 year** with about **20** active users, yet had previously received only **2** issue reports, indirectly suggesting that the original feedback mechanism involved high friction.
- A limitation of the quantitative results is that the provided excerpt **does not include more detailed numerical metrics** (such as means, standard deviations, p-values, or exact quality score differences), so the strongest concrete claims are improved user preference and expert-recognized gains in report completeness.

## Link
- [http://arxiv.org/abs/2603.04244v1](http://arxiv.org/abs/2603.04244v1)
