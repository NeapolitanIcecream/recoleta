---
source: arxiv
url: http://arxiv.org/abs/2603.04985v1
published_at: '2026-03-05T09:25:15'
authors:
- Yi Wang
- Kexin Cheng
- Xiao Liu
- Chetan Arora
- John Grundy
- Thuong Hoang
- Henry Been-Lirn Duh
topics:
- llm
- retrieval-augmented-generation
- persona-generation
- vr-accessibility
- human-ai-interaction
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Auto-Generating Personas from User Reviews in VR App Stores

## Summary
This paper proposes an automated persona system for VR courses: it extracts real accessibility-related feedback from reviews in the Meta/Steam VR app stores and uses LLM + RAG to generate discussable user personas. Its goal is not simply to generate personas, but to help students more efficiently discover latent accessibility needs and improve empathy.

## Problem
- Accessibility requirements in the early stages of VR projects are often overlooked, while traditional persona creation relies on interviews, questionnaires, or large-scale data analysis, making it costly and difficult for students and novices.
- Accessibility issues in VR differ from those in traditional web/mobile settings, such as motion sickness, spatial navigation, and controller interaction, and therefore require requirement-discovery methods that are more grounded in VR contexts.
- Existing courses lack an automated persona method grounded in real user evidence that can systematically support accessibility discussions.

## Approach
- Reviews were collected from the **50 most popular VR apps** on Meta Quest and Steam. Using disability-related keywords, fuzzy matching, and manual cleaning, the authors obtained **396** high-quality accessibility-related reviews.
- The reviews were organized by VR genre (e.g., action, social, horror, puzzle, simulation, sports) and disability/issue category, then chunked and embedded into a Chroma vector database for semantic retrieval.
- After the user inputs a project type and description, the system first retrieves the most relevant review snippets, then sends that evidence to **GPT-4o** to generate an intermediate structured "dimension-value" representation, which is finally aggregated into a standardized persona including a profile, pain points, direct quotes, and explicit needs.
- To reduce hallucinations, the method uses **RAG** to bind generation to retrieved real review evidence rather than relying on pure generation; the system also supports conversational follow-up questions, similar-needs recommendations, and persona comparison across apps/disability types.

## Results
- In a crossover study with **24** students in a VR course, the system scored higher overall on empathy-related measures than questionnaire/self-collected-material methods: **t = 2.989, p = .015**; system **M = 4.45, SD = 0.78**; baseline **M = 3.06, SD = 1.39**.
- It was significantly higher on **Perspective Taking**: **t = 3.715, p = .004**; system **M = 4.65, SD = 0.81**; baseline **M = 3.25, SD = 1.24**.
- It was significantly higher on **Empathic Concern**: **t = 2.515, p = .033**; system **M = 4.35, SD = 1.29**; baseline **M = 2.85, SD = 1.54**.
- There was **no significant difference** on **Fantasy**; system **M = 4.15, SD = 2.90**; baseline **M = 3.10, SD = 1.96**.
- The strongest claim from the qualitative results is that students felt personas generated from real reviews reduced the sense of being “fictional/abstract,” made it easier to understand VR accessibility issues from the perspective of users with disabilities, and strengthened their sense of design responsibility.
- The authors claim this is **one of the first** works / the **first practice** to integrate automatically generated accessibility personas into VR course teaching and use them to support accessibility requirement discussions and empathy building.

## Link
- [http://arxiv.org/abs/2603.04985v1](http://arxiv.org/abs/2603.04985v1)
