---
source: hn
url: https://www.dailymail.co.uk/debate/article-15640991/ChatGPT-Islamic-terrorist-propaganda.html
published_at: '2026-03-14T23:24:41'
authors:
- nailer
topics:
- llm-safety
- misinformation
- wikipedia
- propaganda
- source-reliability
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Tehran Hijacked AI

## Summary
This article claims that terrorist organizations and regimes such as Iran manipulate Wikipedia entries to “launder” propaganda, which is then repeatedly propagated by mainstream large models and search systems, creating a new form of information warfare. Using ChatGPT’s answers about Hezbollah and other figures/organizations as examples, the author alleges that AI inherits and amplifies these contaminated sources.

## Problem
- The problem the article seeks to address is: **after Wikipedia is infiltrated by propaganda machines, AI systems may inherit distorted narratives**, describing terrorist organizations as “political forces” or “resistance” actors rather than perpetrators of violence.
- This matters because students, journalists, policymakers, and ordinary users all rely on Wikipedia and chatbots; once an upstream knowledge source is contaminated, downstream effects can be amplified at scale.
- The author specifically emphasizes so-called “information laundering”: original propaganda first enters Wikipedia, then is relayed through search engines and AI, ultimately obscuring the original propaganda source.

## Approach
- This is not an academic paper, but an **investigative/commentary article**; its core mechanism is described as: **bad actors first rewrite or influence Wikipedia, then LLMs absorb and restate it**.
- The author tests ChatGPT through several **case-based prompts**, such as asking “What is Hezbollah?”, and asking about Palestinian Islamic Jihad commander Abu al-Walid al-Dahdouh, Ali Khamenei, Yahya Sinwar, etc., to observe whether the model uses milder wording.
- The author then compares the AI’s answers with **the wording of Wikipedia entries and their cited sources**, arguing that some phrasing closely matches language from propaganda media or organization websites.
- The article also presents a **large-scale source-counting** idea: counting Wikipedia citations to Iranian state media, Hamas/Hezbollah-affiliated media, Muslim Brotherhood media, and al-Qaeda-affiliated media, to argue that the problem is systemic.

## Results
- The author says that when asked “**What is Hezbollah?**”, ChatGPT did not emphasize its status as a “US-designated terrorist organization,” but instead answered that it is “**a Lebanese political party**,” and, according to the article, provided only **1 citation: Wikipedia**.
- Regarding Abu al-Walid al-Dahdouh, the author says that in the Wikipedia entry, **3 of 4 sources** came directly from Palestinian Islamic Jihad websites and included language such as “**Role in the Resistance**,” adopting the armed group’s narrative.
- The author claims the research found that Wikipedia cites **Iranian state media** more than **29,000** times; cites media related to **Hamas/Hezbollah** more than **8,400** times; cites **Muslim Brotherhood**-related media about **1,000** times; and cites **al-Qaeda-affiliated media** more than **100** times.
- For entries related to the 2025 Shabelle offensive, the author says they cite al-Shabaab’s official media **Radio Furqaan nearly 50 times**, and cite Shahada News Agency **more than a dozen times**.
- The text **does not provide a reproducible experimental design, standard dataset, baseline models, or peer-reviewed metrics**, so there are no academic SOTA results in the strict sense; the strongest concrete claims are the case examples and citation-count statistics above, intended to show that “Wikipedia contamination can spread into AI outputs.”

## Link
- [https://www.dailymail.co.uk/debate/article-15640991/ChatGPT-Islamic-terrorist-propaganda.html](https://www.dailymail.co.uk/debate/article-15640991/ChatGPT-Islamic-terrorist-propaganda.html)
