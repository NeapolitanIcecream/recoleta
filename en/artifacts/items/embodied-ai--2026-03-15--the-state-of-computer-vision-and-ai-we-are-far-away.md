---
source: hn
url: http://karpathy.github.io/2012/10/22/state-of-computer-vision/
published_at: '2026-03-15T23:41:14'
authors:
- stickynotememo
topics:
- computer-vision
- scene-understanding
- common-sense-reasoning
- embodiment
- ai-critique
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# The state of Computer Vision and AI: we are far away

## Summary
This is an opinion piece arguing that computer vision and AI at the time were still very, very far from “understanding images like humans do.” Using a funny photo as an example, the author shows that true visual understanding requires far more than classification and detection: it also depends on common sense, physics, social cognition, and theory-of-mind reasoning.

## Problem
- The article discusses the problem of **how to enable machines to understand a scene, object interactions, physical causality, personal identity, intentions, and mental states from a single image the way humans do**, rather than merely assigning labels or drawing bounding boxes.
- This matters because humans’ natural understanding of images relies on a large amount of implicit knowledge; without these capabilities, existing CV systems may perform well on benchmarks yet still remain far from true intelligence.
- The author points out that the core difficulty is not just the reasoning algorithms, but also **how to acquire the training data and experience needed to support such reasoning**, such as how objects work and how people interact with their environment.

## Approach
- This is not a paper proposing a new algorithm, but rather a **conceptual/critical analysis**: using a photo example of “Obama secretly stepping on a scale,” it breaks down layer by layer the chain of knowledge required for humans to understand the joke.
- The author argues that the core mechanism should involve multiple layers of reasoning: **3D scene understanding, mirror recognition, identity recognition, human pose and object affordances, physical causality, visibility/attention, future event prediction, and modeling other people’s mental states**.
- The article criticizes mainstream CV tasks at the time (such as ImageNet classification and Pascal VOC detection) as being too narrow and fragmented to approach full scene understanding.
- The author further suggests a directional hypothesis: relying only on more static images/videos/text and training tricks may not be enough; **embodiment may also be necessary**, allowing systems to learn about the world through long-term, structured, temporally coherent interactive experience.

## Results
- **No experiments, datasets, or quantitative metrics are provided**; this is a position/commentary article and does not report reproducible experimental results.
- The strongest concrete claim is that the SOTA at the time was mainly evaluated on tasks such as **1-of-k image classification on ImageNet** and **object detection/bounding boxes on Pascal VOC**, but there is a huge gap between these tasks and human-like scene understanding.
- The author’s key conclusion is that recovering the “huge iceberg of knowledge” behind a single RGB image is extremely difficult, and current CV/AI is “very, very far away.”
- Another important forward-looking view is that to achieve more human-like visual understanding, systems may need **years of structured, temporally coherent experience and the ability to interact actively**, i.e., some kind of embodied learning framework.

## Link
- [http://karpathy.github.io/2012/10/22/state-of-computer-vision/](http://karpathy.github.io/2012/10/22/state-of-computer-vision/)
