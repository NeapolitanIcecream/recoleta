---
source: arxiv
url: http://arxiv.org/abs/2604.22238v1
published_at: '2026-04-24T05:27:27'
authors:
- Khoa Vo
- Sieu Tran
- Taisei Hanyu
- Yuki Ikebe
- Duy Nguyen
- Bui Duy Quoc Nghi
- Minh Vu
- Anthony Gunderman
- Chase Rainwater
- Anh Nguyen
- Ngan Le
topics:
- vision-language-action
- long-horizon-manipulation
- non-markovian-planning
- semantic-graph-state
- code-as-planner
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models

## Summary
CodeGraphVLP targets long-horizon robot manipulation where the next action depends on earlier observations, not just the current camera frame. It combines a persistent semantic graph, a one-time synthesized code planner, and object-focused prompting for a VLA policy.

## Problem
- Standard Vision-Language-Action models usually act from the latest observation, which fails on non-Markovian tasks where key evidence may be occluded or only visible earlier.
- History-based extensions can miss sparse past evidence or add latency and compute cost as the context window grows.
- VLM-in-the-loop hierarchical planners can improve long-horizon reasoning, but repeated model calls are slow and language-only subtask prompts still leave visual grounding brittle in clutter.

## Approach
- The system builds and updates a persistent semantic graph of task-relevant objects, attributes, and relations across time using segmentation, relevance filtering, cross-view association, tracking, and rule-based relation induction.
- An LLM is called once at task start to write a task-specific Python planner that reads the graph, checks progress with simple predicates, stores lightweight task memory, and outputs the next subtask plus the relevant objects.
- The executor VLA does not see the full cluttered scene. It receives a short subtask instruction and images masked to keep only the planner-selected objects.
- Training matches deployment: recorded demonstrations are converted into subtask-conditioned, masked observations, and the VLA is fine-tuned by imitation learning on those inputs.

## Results
- On three real-world tabletop tasks, CodeGraphVLP reports an average success rate of **81.7%**, above **Gr00T N1.5 + Multi-frame: 56.7%**, **Gr00T N1.5: 31.7%**, **π0: 30.0%**, **π0.5: 5.0%**, and **π0 FAST: 0.0%**.
- On **Pick-and-Place Twice**, CodeGraphVLP reaches **80%** full success and **100%** on the intermediate "PnP Once" metric, versus **75% / 100%** for Gr00T N1.5 + Multi-frame and **35% / 50%** for Gr00T N1.5.
- On **Place-and-Stack**, CodeGraphVLP reaches **80%** success and **95%** on the intermediate "Drop Cube" metric, versus **50% / 50%** for Gr00T N1.5 + Multi-frame and **40% / 40%** for Gr00T N1.5.
- On **Swap Cups**, CodeGraphVLP reaches **85%** success and **100%** on the intermediate "Stage Cup" metric, versus **45% / 90%** for Gr00T N1.5 + Multi-frame and **20% / 70%** for Gr00T N1.5.
- The paper also claims substantially lower planning latency than VLM-in-the-loop planning, but the excerpt does not include the actual latency numbers.
- Training data size in the real-world setup is **100** demos for Pick-and-Place Twice, **100** for Place-and-Stack, and **200** for Swap Cups.

## Link
- [http://arxiv.org/abs/2604.22238v1](http://arxiv.org/abs/2604.22238v1)
