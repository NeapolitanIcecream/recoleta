---
source: arxiv
url: http://arxiv.org/abs/2603.11080v1
published_at: '2026-03-10T22:30:28'
authors:
- Chang Liu
- Sibo Tian
- Xiao Liang
- Minghui Zheng
topics:
- vision-language-action
- robotic-disassembly
- agentic-framework
- contact-rich-manipulation
- failure-recovery
relevance_score: 0.46
run_id: materialize-outputs
language_code: en
---

# SELF-VLA: A Skill Enhanced Agentic Vision-Language-Action Framework for Contact-Rich Disassembly

## Summary
SELF-VLA proposes an agentic framework that embeds explicit “skills” into VLA robotic policies for contact-rich, long-horizon e-waste disassembly. It aims to address the near-total failure of purely end-to-end VLA methods in precise industrial disassembly, and significantly improves success rates through skill invocation and failure recovery.

## Problem
- E-waste disassembly must cope with large product variation, uncertain states, long operation sequences, and contact-rich manipulation. Traditional manual labor is costly, inefficient, and carries safety and health risks.
- Existing robotic disassembly systems mostly rely on staged perception-planning-execution pipelines, which are engineering-heavy, accumulate errors, and generalize poorly, making them hard to adapt to real-time uncertainty.
- Existing end-to-end VLAs are effective on everyday tabletop manipulation, but their success rates are close to zero on high-precision, strongly constrained disassembly tasks such as CPU/RAM removal, limiting their industrial usefulness.

## Approach
- The framework consists of three parts: **VLA-planner** is responsible for approaching the target based on vision + language; after reaching a suitable pose, it outputs a special **stop token**; then the **skill library** is invoked to execute predefined contact-rich disassembly skills; if grasping fails, **VLA-corrector** re-grasps and restores the subsequent process.
- The core idea is: instead of forcing a single VLA policy to learn the entire complex disassembly process end to end, let it first “move into place and understand when to switch,” then hand the most precise and procedural parts over to explicit skill execution.
- The stop token is encoded into the gripper action dimension using the out-of-physical-range value 255, allowing skill switching to be triggered without modifying the original VLA output head.
- The skill library uses sequences of relative/absolute waypoints: relative waypoints adapt to different initial poses for extraction, while absolute waypoints handle placement; failure is automatically detected through gripper width differences and continuous drop detection at 50Hz.
- The dataset contains 528 real demonstrations (264 CPU, 264 RAM), and trajectories are annotated into four stages: approaching, skill execution, correction, and skill resumption, for LoRA fine-tuning of OpenVLA, OpenVLA-OFT, π0.5, and π0.5-Droid.

## Results
- Data scale: a total of **528** real demonstrations, including **264** CPU extraction and **264** RAM removal; training/evaluation covers **8** collection configurations, and testing uses **5** unseen component positions/poses, with **20** evaluation runs per task per model setting.
- On **RAM removal**, the best end-to-end baseline is **π0.5-Droid FT-10Hz: 7/20 final success (35%)**; the best SELF-VLA result is **π0.5-Droid FT-10Hz: 12/20 (60%)**, an improvement of **+5/20 = +25 percentage points** over the best end-to-end method.
- On **RAM removal**, SELF-VLA reaches **9/20 (45%)** final success with **π0.5 FT-10Hz**, while the corresponding end-to-end model achieves only **4/20 (20%)**; under **π0.5-Droid FT-30Hz**, SELF-VLA reaches **11/20 (55%)**, versus **5/20 (25%)** for end-to-end.
- On **CPU extraction**, the best end-to-end baseline is only **π0.5-Droid FT-30Hz: 2/20 final success (10%)**; the best SELF-VLA result is **π0.5-Droid FT-10Hz: 17/20 (85%)**, an improvement of **+15/20 = +75 percentage points** over the best end-to-end method.
- On **CPU extraction**, SELF-VLA reaches **10/20 (50%)** final success with **OpenVLA-OFT FT-10Hz**, while the corresponding end-to-end model is **0/20**; with **π0.5 FT-10Hz**, it reaches **11/20 (55%)**, while the corresponding end-to-end model is **0/20**.
- The pretrained models almost all fail: for example, OpenVLA, OpenVLA-OFT, π0.5, and π0.5-Droid have **PT final success of 0/20** on most settings across both tasks, showing that the paper’s main contribution is the substantial gain from “skill enhancement + recovery mechanism” in industrial disassembly scenarios, rather than simply relying on off-the-shelf VLA capability.

## Link
- [http://arxiv.org/abs/2603.11080v1](http://arxiv.org/abs/2603.11080v1)
