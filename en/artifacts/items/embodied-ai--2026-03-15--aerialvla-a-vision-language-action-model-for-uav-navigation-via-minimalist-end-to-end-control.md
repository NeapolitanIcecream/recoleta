---
source: arxiv
url: http://arxiv.org/abs/2603.14363v1
published_at: '2026-03-15T13:02:13'
authors:
- Peng Xu
- Zhengnan Deng
- Jiayan Deng
- Zonghua Gu
- Shaohua Wan
topics:
- vision-language-action
- uav-navigation
- embodied-ai
- end-to-end-control
- sim2real
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# AerialVLA: A Vision-Language-Action Model for UAV Navigation via Minimalist End-to-End Control

## Summary
AerialVLA proposes a minimalist end-to-end VLA model for UAV vision-language navigation, directly mapping dual-view images and fuzzy language prompts to continuous control and landing actions. It aims to break free from existing UAV-VLN dependence on oracle directional prompts and external object detectors, enabling navigation and precise landing under a more autonomous setting.

## Problem
- Existing UAV VLN methods often rely on **dense oracle directional guidance**, making models behave more like they “follow prompts” rather than perform true spatial reasoning and autonomous navigation.
- Many systems also depend on **external object detectors** to decide when to land, creating a disconnect between perception and control and reducing robustness in open environments.
- UAVs in dynamic 3D environments require continuous control and fine-grained visual localization, which are critical for real-time performance, stability, and generalization, and directly affect usability in GPS-unreliable scenarios such as search-and-rescue and inspection.

## Approach
- Use **minimalist dual-view perception**: retain only forward-facing and downward-facing images, vertically concatenate them, and feed them into the OpenVLA-7B visual encoder to reduce redundant input and latency while supporting both forward navigation and ground alignment for landing.
- Use **fuzzy directional prompts**: discretize relative orientation from onboard IMU/GPS into coarse language prompts such as “straight ahead” and “forward-right,” replacing step-by-step oracle instructions and forcing the model to rely more on active visual localization.
- Use **numerically tokenized action outputs**: discretize continuous 3-DoF actions \(\langle \Delta x, \Delta z, \Delta\psi \rangle\) into 99 bins and map them directly to existing numeric tokens in the LLM, avoiding the need to relearn a special action vocabulary.
- **Unify navigation and landing** within a single policy: the model can output LAND or output a near-zero displacement action as a stop signal, eliminating the need for an external detector to trigger landing.
- Training uses **behavior cloning** and adds geometric-consistency filtering, removing about 4% of training frames where fuzzy prompts and expert actions are clearly contradictory.

## Results
- On the TravelUAV Seen test set, AerialVLA achieves **47.96% SR**, **38.54% SPL**, **65.88 NE**, and **57.69% OSR**.
- Compared with the strongest baseline LongFly, it improves on the Seen set to **+11.57 SR** (47.96 vs. 36.39) and **+7.47 SPL** (38.54 vs. 31.07); the paper also reports an SR advantage of **+12.36** (46.30 vs. 33.94) on the Hard subset.
- Compared with NavFoM, Seen-set SR rises from **29.17%** to **47.96%**; compared with TravelUAV-DA, SR rises from **17.45%** to **47.96%**.
- In computational efficiency, AerialVLA requires **17GB VRAM** and **0.38s total latency** on an RTX 4090, better than TravelUAV’s **20GB** and **0.63s**; its own VLA inference takes **0.35s**, and fuzzy prompting adds only **0.03s**.
- Data and training scale: it uses the TravelUAV *UAV-Need-Help* task, trained on **7,922 trajectories / 420k frames**, with testing including **1,418** Seen trajectories, **629** Unseen Object trajectories, and **958** Unseen Map trajectories.
- The abstract claims that in **unseen scenarios** it achieves “**nearly 3× success rate**” relative to leading baselines, but the current excerpt does not include the corresponding full table values, so this cannot be verified line by line.

## Link
- [http://arxiv.org/abs/2603.14363v1](http://arxiv.org/abs/2603.14363v1)
