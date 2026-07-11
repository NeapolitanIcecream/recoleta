---
source: arxiv
url: https://arxiv.org/abs/2607.07480v1
published_at: '2026-07-08T14:43:08'
authors:
- Erfan Entezami
- Madeline Endres
topics:
- ai-code-generation
- personalization-bias
- software-fairness
- human-ai-interaction
- web-development
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Biased or Personalized? The Impact of Personal Information on AI-driven Development

## Summary
AI coding assistants can change generated websites based on a developer’s inferred age and gender, even when the task prompt is otherwise the same. The paper shows this in web development through controlled generations and a small user study on ChatGPT personalization.

## Problem
- It studies whether personal information about the developer changes generated software beyond stated requirements.
- This matters because AI coding tools can personalize output in ways users may not see, including UI choices, placeholder content, and code organization.
- If those changes follow age or gender stereotypes, generated software can carry bias into applications made by non-expert users.

## Approach
- The authors generated 800 websites with ChatGPT-4.1 and DeepSeek-V3.2 using two tasks: a personal website and an online shop.
- They created 20 personas across young women, older women, young men, and older men. Each prompt changed only the persona name and age.
- They measured three artifact areas: interface design, template content, and code structure.
- For categorical outcomes they used chi-square, Fisher-Freeman-Halton, or z tests; for continuous code metrics they used Mann-Whitney U tests with Benjamini-Hochberg correction.
- They also ran a 20-person observational study in which participants used their own ChatGPT accounts to build personal websites, then discussed personalization and bias.

## Results
- In 120 manually reviewed personal websites, every site had Hobbies and Skills sections, but Photo Gallery appeared in only 10/120 cases and all were for older personas; for DeepSeek this age effect was z=3.25, p=0.003.
- Contact sections appeared 58/120 times. Older personas received 37/58 Contact sections, compared with 21/58 for younger personas: z=2.92, p=0.004. Among younger personas, young men received 15 Contact sections and young women received 6: z=2.78, p=0.005.
- Color choices differed by persona group. In GPT-4.1, 24/31 dark-blue personal websites were for men; in DeepSeek, 29/35 dark-blue personal websites were for men. Pink and purple appeared only for women in the reviewed sample.
- Color-persona associations had p<0.05 with Cramer's V values reported as 0.36-0.53; examples include GPT-4.1 dark blue with p<0.001, V=0.535 and DeepSeek green with p<0.001, V=0.434.
- For online shops, the excerpt reports that sites generated for women contained fewer files and less JavaScript, with p=0.007.
- In the 20-participant study, participants mainly treated personalization as content selection, while the controlled study found demographic effects in UI and code structure too.

## Link
- [https://arxiv.org/abs/2607.07480v1](https://arxiv.org/abs/2607.07480v1)
