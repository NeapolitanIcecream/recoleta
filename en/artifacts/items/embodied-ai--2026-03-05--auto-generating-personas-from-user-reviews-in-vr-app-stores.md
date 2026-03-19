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
- llm-persona-generation
- virtual-reality
- accessibility
- user-reviews
- rag
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Auto-Generating Personas from User Reviews in VR App Stores

## Summary
This paper proposes an auto-generated user persona system for VR courses: it extracts real accessibility-related feedback from Meta and Steam VR store reviews and uses LLM + RAG to generate personas that support requirements discussions. The study shows that these personas grounded in real reviews are better than traditional survey-based approaches at improving students' empathy and sense of responsibility toward users with disabilities.

## Problem
- Accessibility requirements are rarely discussed systematically in the early stages of VR projects, while traditional persona creation is time-consuming and depends on research skills, making students prone to producing superficial or fabricated personas.
- VR accessibility issues differ from those on the web or mobile, such as motion sickness, spatial navigation, and controller interaction barriers, and are often overlooked in design education.
- A method is needed that can quickly turn **real user evidence** into discussable personas, helping students identify latent accessibility requirements more accurately.

## Approach
- Reviews were collected from the **50 most popular VR apps** in the Meta Quest and Steam stores. Using disability-related keywords, fuzzy matching, and manual cleaning, the authors obtained **396 high-quality accessibility reviews**.
- The reviews were organized by VR app type (such as action, social, horror, puzzle, simulation, sports) and by disability/issue type, then split into semantic chunks and vectorized into a Chroma database.
- During generation, the system first retrieves the most relevant reviews based on project type and disability group, then feeds the evidence into a **GPT-4o + RAG** pipeline. It first forms an intermediate “dimension-value” structure and then generates a standardized persona including a profile, pain points, direct quotes, and explicit needs.
- The system supports conversational use: students can enter project context and request similar personas or suggestions for specific needs; to reduce hallucinations, outputs are always constrained by the retrieved real reviews.

## Results
- In a cross-condition user study with **24** VR course students, the system achieved a higher overall empathy score than the survey-based method: **t = 2.989, p = .015**; system **M = 4.45, SD = 0.78**, survey **M = 3.06, SD = 1.39**.
- **Perspective Taking** improved significantly: **t = 3.715, p = .004**; system **M = 4.65, SD = 0.81**, survey **M = 3.25, SD = 1.24**.
- **Empathic Concern** improved significantly: **t = 2.515, p = .033**; system **M = 4.35, SD = 1.29**, survey **M = 2.85, SD = 1.54**.
- No significant difference was found for **Fantasy**; only the mean difference was reported: system **M = 4.15, SD = 2.90**, survey **M = 3.10, SD = 1.96**.
- The paper's strongest claims are that the system makes it easier for students to understand VR accessibility issues from the perspective of users with disabilities, reduces the abstraction of “fictional personas,” and strengthens their sense of design responsibility.
- The paper does not report system-level objective metrics such as persona generation quality, retrieval accuracy, or hallucination rate; the main evidence comes from questionnaires and interviews in an educational setting.

## Link
- [http://arxiv.org/abs/2603.04985v1](http://arxiv.org/abs/2603.04985v1)
