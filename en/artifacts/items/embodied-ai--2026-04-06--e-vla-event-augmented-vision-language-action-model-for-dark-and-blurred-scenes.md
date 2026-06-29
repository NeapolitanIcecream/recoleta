---
source: arxiv
url: http://arxiv.org/abs/2604.04834v1
published_at: '2026-04-06T16:35:57'
authors:
- Jiajun Zhai
- Hao Shi
- Shangwei Guo
- Kailun Yang
- Kaiwei Wang
topics:
- vision-language-action
- event-camera
- robot-manipulation
- low-light-robustness
- motion-blur
- embodied-ai
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# E-VLA: Event-Augmented Vision-Language-Action Model for Dark and Blurred Scenes

## Summary
E-VLA adds event-camera signals to a vision-language-action robot policy so it can keep manipulating objects when RGB images are too dark or too blurred to use. The paper shows that simple event fusion already helps, and a small event adapter helps more.

## Problem
- Standard VLA robot policies depend on RGB frames, so they fail when sensing breaks down at capture time: extreme low light, black clipping, and motion blur.
- Image enhancement can improve appearance after capture, but it cannot recover information that the camera never recorded. This matters for real robot deployment, where wrist cameras move fast and lighting changes.
- Event cameras can still capture brightness changes under these conditions, but their sparse asynchronous output does not match pretrained image-based VLA backbones.

## Approach
- The paper builds **E-VLA**, an event-augmented VLA model on top of a SmolVLA-style backbone with a frozen SigLIP vision encoder and frozen LLM, plus trainable action layers.
- It converts recent event streams into image-like accumulated event maps aligned with RGB frames. The authors test event windowing and report that a **fixed recent-count window** gives more stable perception-action coupling than fixed-duration windows.
- It studies two fusion methods that keep the pretrained visual token structure: **overlay fusion**, which writes event cues directly onto the RGB image with no extra parameters, and a **hierarchical event adapter**, a small ViT-style branch that injects event features into SigLIP at layers 3, 6, 9, and 12.
- It also introduces a real synchronized **RGB-event-action** manipulation dataset collected with a DAVIS346 event camera on a teleoperated SO100 robot across Pick-Place, Sorting, and Stacking tasks under multiple illumination levels.

## Results
- Dataset scale: **724 episodes** total, with **339,310 frames**; **305** episodes at normal light and **419** episodes across lower-light settings.
- On **Pick-Place** under low light, image-only success drops from **100% at 75 lux** to **0% at 25 lux and 20 lux**. E-VLA overlay reaches **65% at 25 lux** and **60% at 20 lux**. The event adapter reaches **90% at 25 lux** and **90% at 20 lux**.
- Average Pick-Place success across **75/40/35/30/25/20 lux**: **47.5%** for image-only, **66.7%** with RetinexNet, **60.8%** with Retinexformer, **70.0%** with EvLight, **35.8%** with E2VID, **80.8%** with overlay fusion, and **94.2%** with the event adapter.
- The abstract reports motion-blur gains at **1000 ms exposure**: Pick-Place improves from **0%** for image-only to **20-25%** with E-VLA, and Sorting improves from **5%** to **32.5%**.
- The abstract also reports that under **20 lux**, Pick-Place rises from **0%** for image-only to **60%** with overlay fusion and **90%** with the event adapter.
- The introduction claims that under complete **black clipping**, E-VLA keeps task success **above 80%**, while the image-only baseline is **0%**. The excerpt does not include the full table for this setting.

## Link
- [http://arxiv.org/abs/2604.04834v1](http://arxiv.org/abs/2604.04834v1)
