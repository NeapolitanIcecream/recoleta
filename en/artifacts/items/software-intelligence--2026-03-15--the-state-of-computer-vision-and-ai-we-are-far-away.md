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
- ai-limitations
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# The state of Computer Vision and AI: we are far away

## Summary
This is an opinionated commentary whose core argument is: with the mainstream vision tasks and data setups of the time alone, we were still very far from human-like scene understanding and commonsense reasoning. Using a humorous photo, the author shows that truly “understanding” an image requires far more than classification and detection—it requires large amounts of implicit knowledge, physical intuition, and theory-of-mind reasoning.

## Problem
- The article discusses the problem of **how computer vision/AI can acquire human-like scene understanding and commonsense reasoning from pixels**. This matters because truly “seeing” the real world is not just about recognizing objects, but also about understanding 3D structure, physics, intentions, social context, and what is likely to happen next.
- The author argues that existing tasks such as **ImageNet classification**, **Pascal VOC detection**, pose estimation, and action recognition are all too local and fragmented to support holistic understanding of the humor/meaning in complex scenes.
- The deeper issue is not just the reasoning algorithms themselves, but also **how to collect training data in the right form** so that a system has a chance to learn knowledge like “how a scale works,” “what a person cannot see,” and “how others will react.”

## Approach
- This is not a technical paper proposing a new algorithm, but rather a **cognitive task decomposition** built around a photo example: it breaks down, layer by layer, the kinds of knowledge humans invoke when they instantly understand an image.
- The simplest explanation of the core mechanism is that when humans look at an image, they are not merely doing 2D pattern matching; they are simultaneously performing **identity recognition, mirror disambiguation, 3D scene reconstruction, human-object interaction understanding, physical causal reasoning, viewpoint/visibility reasoning, mental-state reasoning, and social-identity reasoning**.
- On this basis, the author argues that there is a huge “iceberg” between pixels and semantics: the visible pixels are only the surface, while the real difficulty lies in recovering hidden structure and causal relations with the help of prior knowledge.
- The article further offers a directional judgment: the future may require **embodiment, long-term temporal experience, interaction with the world, and some kind of active learning/reasoning architecture**, rather than relying only on more static images and a few training tricks.

## Results
- **No experiments, dataset, or quantitative metrics are provided**; this is an opinion piece rather than empirical research.
- The strongest concrete claim is that understanding a single humorous photo involves at least about **10 layers of reasoning** as listed by the author, including mirror recognition, person identity, scale/posture, the foot applying force to the scale, physical causality, the subject’s field-of-view limitations, psychological expectations about body weight, others’ anticipation of his confusion, and the social context implied by presidential identity.
- The author directly judges the state of computer vision and AI at the time as “**very, very far**,” and believes the path from current benchmark tasks to human-level understanding is “**long, uncertain and unclear**.”
- The article also explicitly rejects an optimistic assumption: **more image/video/text data plus better objective functions/SGD tricks alone** will not naturally cause these full capabilities to emerge; what is missing is “many key puzzle pieces,” especially the right forms of data and experience.

## Link
- [http://karpathy.github.io/2012/10/22/state-of-computer-vision/](http://karpathy.github.io/2012/10/22/state-of-computer-vision/)
