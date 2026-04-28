---
source: hn
url: https://www.technologyreview.com/2026/04/17/1135416/how-robots-learn-brief-contemporary-history/
published_at: '2026-04-18T22:11:04'
authors:
- billybuckwheat
topics:
- robot-learning-history
- vision-language-action
- sim2real
- robot-foundation-models
- humanoid-robots
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Robots learn: A brief, contemporary history

## Summary
This article gives a short history of how robot learning shifted from hand-written rules to data-driven models, simulation training, and foundation-model-style policies. It argues that this shift is a main reason robotics investment and deployment rose sharply in the mid-2020s.

## Problem
- Traditional robotics depended on engineers specifying rules for each situation, which breaks down for messy real-world tasks like folding clothes, handling novel objects, or interacting with people.
- Policies trained only in simulation often fail on real robots because small differences in friction, lighting, materials, and sensing can change outcomes.
- General-purpose robots need to map language, vision, and state into actions across many tasks, but older scripted systems had weak language ability and poor adaptability.

## Approach
- The article traces three main learning shifts: rule-based control, reinforcement learning in simulation, and large-scale action prediction from multimodal data.
- In simulation-based learning, robots improve by trial and error with reward signals. Domain randomization varies physics and visuals across many simulated worlds so the policy transfers better to reality.
- In foundation-model-style robotics, systems take camera views, sensor readings, joint states, and language instructions, then predict the next robot action many times per second.
- Some companies collect data from deployed robots in warehouses or other work settings, then use that real-world feedback to improve the model over time.
- The piece uses case studies: Jibo for social interaction limits, OpenAI Dactyl for sim-to-real dexterous manipulation, Google RT-1/RT-2 for vision-language-action control, Covariant RFM-1 for warehouse picking, and Agility Digit for humanoid deployment.

## Results
- Humanoid robot investment reached **$6.1 billion in 2025**, about **4x** the amount invested in **2024**, according to the article.
- Google collected data for **17 months** across **700 tasks** to build RT-1. RT-1 achieved **97%** success on tasks it had seen before and **76%** on unseen instructions.
- OpenAI's Dactyl later applied sim-based techniques to Rubik's Cube solving, with **60%** success overall and **20%** on particularly hard scrambles.
- Covariant deployed warehouse robot systems at customer sites such as Crate & Barrel and released RFM-1 in **2024**, but the article gives no benchmark table or aggregate success rate.
- Agility's Digit is described as one of the first humanoids used for real warehouse work by Amazon, Toyota, and GXO. A concrete limitation is payload: Digit can lift **35 pounds**.
- The article is a journalistic overview, not a research paper, so quantitative evidence is selective and there is no unified experimental comparison across methods or systems.

## Link
- [https://www.technologyreview.com/2026/04/17/1135416/how-robots-learn-brief-contemporary-history/](https://www.technologyreview.com/2026/04/17/1135416/how-robots-learn-brief-contemporary-history/)
