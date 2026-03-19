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
- uav-navigation
- vision-language-action
- end-to-end-control
- embodied-ai
- autonomous-landing
relevance_score: 0.24
run_id: materialize-outputs
language_code: en
---

# AerialVLA: A Vision-Language-Action Model for UAV Navigation via Minimalist End-to-End Control

## Summary
AerialVLA proposes a minimalist end-to-end Vision-Language-Action framework for UAV vision-language navigation, directly mapping dual-view images and fuzzy language prompts to continuous control and landing actions. The core claim is that removing dense oracle guidance and external object detectors can instead yield a more autonomous, more efficient, and more robust navigation policy in unseen environments.

## Problem
- Existing UAV vision-language navigation methods often rely on **dense oracle directional prompts**, making the model behave more like a passive follower rather than truly performing spatial reasoning and autonomous navigation.
- Many methods also depend on **external object detectors** to decide when to land, causing a disconnect between perception and control and limiting robustness and realism.
- UAVs require continuous control and fine-grained visual alignment in open 3D environments, which is harder than ground-based 2D navigation and is important for GPS-unreliable scenarios such as search and rescue and inspection.

## Approach
- Uses **minimalist dual-view perception**: only front and downward views are retained, vertically concatenated, and fed into the visual encoder of OpenVLA-7B to reduce multi-camera redundancy and inference overhead.
- Uses **fuzzy directional prompting**: the relative orientation estimated by onboard IMU/GPS is discretized into coarse prompts such as “straight ahead” and “forward-right,” replacing stepwise oracle guidance and forcing the model to perform active visual localization.
- Uses **numerically tokenized action outputs**: the 3-DoF actions \(\langle \Delta x, \Delta z, \Delta \psi \rangle\) are discretized into 99 bins and mapped directly to the LLM’s existing numeric vocabulary, rather than training new action tokens.
- Through a **unified landing mechanism**, navigation and stopping are merged into a single policy: the model can either output LAND or predict near-zero displacement to trigger landing, without requiring an external detector.
- Training uses **behavior cloning** and adds geometric consistency filtering, removing about 4% of training frames that would introduce causal ambiguity under fuzzy prompts.

## Results
- On the **Seen** test split of the TravelUAV benchmark, AerialVLA achieves **47.96% SR** and **38.54% SPL**, outperforming the strongest baseline LongFly at **36.39% SR / 31.07% SPL**, improvements of **+11.57** and **+7.47** percentage points respectively.
- On the Seen-Hard subset, AerialVLA achieves **46.30% SR** versus **33.94%** for LongFly, an improvement of **+12.36** percentage points; however, its NE is **93.16**, slightly worse than LongFly’s **85.20**.
- The paper claims that in **unseen environments**, AerialVLA achieves “**nearly three times the success rate of the leading baseline**” and stronger generalization, but the provided excerpt does not include the full corresponding table values, so the specific SR/SPL numbers cannot be verified item by item.
- In terms of computational efficiency, on an RTX 4090, AerialVLA has total latency of **0.38s** and memory usage of **17GB**, making it faster and lighter than TravelUAV at **0.63s** and **20GB**; although its VLA backbone takes **0.35s** (vs. 0.26s), it eliminates the **0.37s** Assist and Grounding DINO modules, with fuzzy prompting adding only **0.03s**.
- The training setup uses **7,922** trajectories and about **420k** frames on TravelUAV, with LoRA training only about **2.98%** of parameters, using **4×RTX 4090** to train for **5 epochs** over about **35 hours**.

## Link
- [http://arxiv.org/abs/2603.14363v1](http://arxiv.org/abs/2603.14363v1)
