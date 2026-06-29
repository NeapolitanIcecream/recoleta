---
source: arxiv
url: https://arxiv.org/abs/2606.10244v1
published_at: '2026-06-08T23:21:14'
authors:
- Takehiko Ohkawa
- Jumpei Arima
- Yuki Noguchi
- Masatoshi Tateno
- Makoto Sugiura
- Takuya Okubo
- Kengo Ikeuchi
- Yuma Shin
- Hiroki Nishizawa
- Naoaki Kanazawa
- Yuki Wakayama
- Daiki Fukunaga
- Koshi Makihara
- Tomohiro Motoda
- Floris Erich
- Yukiyasu Domae
- Tatsuya Matsushima
- Yohishiro Okumatsu
- Kei Ota
topics:
- bimanual-manipulation
- robot-data-scaling
- vision-language-action
- umi-interface
- dexterous-manipulation
- cross-embodiment-transfer
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# YUBI: Yielding Universal Bidigital Interface for Bimanual Dexterous Manipulation at Scale

## Summary
YUBI is a finger-driven handheld gripper and data collection setup for large-scale bimanual robot manipulation. The paper’s main claim is that better operator ergonomics plus VR pose tracking can produce much larger open UMI-style datasets and train policies that transfer across robot arms.

## Problem
- Open robot learning lacks large, accessible bimanual dexterous manipulation datasets at the scale used by private labs.
- Prior UMI-style pistol-grip devices are heavy and offset the operator’s fingers from the gripper pinch point, which hurts fine control, haptic feedback, and long collection sessions.
- SLAM-based gripper tracking can drift, while head-worn VR tracking adds neck fatigue and limits session length.

## Approach
- YUBI replaces the pistol grip with a finger-aligned design: the thumb drives one jaw, and the index and middle fingers drive the other jaw, so the gripper opens and closes with the operator’s pinch motion.
- The gripper weighs 319 g including a 119 g VR controller, compared with 780 g for original UMI and at least 905 g for VR-integrated pistol-grip systems.
- Each unit can be built for under $200 excluding the Quest 3S tracking system, using 3D-printed parts.
- The setup mounts Quest-based VR tracking on the gripper and puts the headset on a fixed rig for tabletop collection; a portable mode mounts the headset on the chest for household tasks.
- The dataset stores synchronized wrist cameras, top-view RealSense data, 6-DoF gripper poses, jaw angles, task text, and sub-action labels, then converts recordings to LeRobot format at 30 Hz.

## Results
- The dataset contains 8434 hours, 1.20M episodes, 6.80M video-language-action triplets, 119 tasks, and an average of 7.99 sub-actions per task, collected on 22 desks by 179 operators over two months.
- Scale exceeds prior UMI-style datasets cited in the paper: original UMI has 12 hours and 4 tasks, while FastUMI has about 60 hours and 22 tasks.
- In the nut pick-and-place dexterity test with 10 novice operators and 50 trials per nut size, YUBI leads UMI by +20 percentage points on M6 nuts, +10 percentage points on M5 nuts, and about 3x on M3 nuts; both devices reach at least 94% on M8-M10 nuts.
- In five operation-efficiency tasks, YUBI is faster than UMI by 1.37x for domino arrangement and up to 4.19x for phone charging.
- A single pi_0.5-based VLA policy trained on YUBI wrist data transfers across three bimanual robot platforms: UR, Franka, and Toyota ELEY, using the same YUBI gripper end-effector.
- Robot rollout success over 20 trials per task is 20/20 for ball in basket, 13/20 for stack cup pyramid, 9/20 for unfold glasses, 18/20 for pick-and-place socks, 18/20 for tape in box, and 11/20 for cup placement.

## Link
- [https://arxiv.org/abs/2606.10244v1](https://arxiv.org/abs/2606.10244v1)
