---
source: arxiv
url: http://arxiv.org/abs/2603.09226v1
published_at: '2026-03-10T05:49:47'
authors:
- Noboru Myers
- Sankalp Yamsani
- Obin Kwon
- Joohyung Kim
topics:
- robot-data-collection
- teleoperation
- bimanual-manipulation
- portable-robotics
- imitation-learning
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# TRIP-Bag: A Portable Teleoperation System for Plug-and-Play Robotic Arms and Leaders

## Summary
TRIP-Bag proposes a portable dual-arm teleoperation data collection system that fits inside a commercial suitcase, aiming to combine laboratory-grade high-fidelity teleoperation with deployability in in-the-wild settings. Its core value is lowering the barrier to collecting robot manipulation data in order to support scaling data for learning-based manipulation policies.

## Problem
- Robot manipulation learning lacks large-scale, high-quality, cross-environment demonstration data, which directly limits the development of imitation learning and robotic foundation models.
- Although portable handheld/vision-based collection solutions are suitable for in-the-wild data collection, they usually suffer from an **embodiment gap** between the human and the robot, making the actions hard to transfer directly to the target robot.
- Traditional teleoperation systems can provide high-fidelity data, but they typically depend on fixed laboratory infrastructure, with high transport, assembly, and calibration costs, making it difficult to scale to multi-scene data collection.

## Approach
- Proposes **TRIP-Bag**: integrates two plug-and-play robotic arms, two scalable puppeteer leaders, three RGB-D cameras, and a compute unit into a single commercial suitcase, creating an out-of-the-box teleoperation platform.
- Uses **direct joint-to-joint mapping** puppeteering teleoperation rather than handheld devices or vision-based hand pose estimation, reducing the embodiment gap by design while preserving full proprioceptive state logging.
- The software is based on ROS2 and the PAPRLE framework: the leader publishes joint states, and a teleoperation node converts them in real time into follower commands while performing self-collision checks and tracking-error feedback.
- During data collection, it synchronously records 3 RGB-D image streams, robot observations such as joint position/velocity/torque, and joint-command actions; cameras run at 30 Hz, joints update at 125 Hz, and the final synchronized recording is at 50 Hz.
- The system improves deployment speed and cross-site transportability through plug-and-play interfaces and a foldable stowage design, with the goal of rapidly collecting high-fidelity bimanual manipulation data in real kitchens, offices, workshops, and similar environments.

## Results
- Portability: the complete system has a **total weight of 29.8 kg** and fits into a standard commercial suitcase; the paper states it can be transported internationally as checked luggage. For experts, the average setup time from opening the case to first teleoperation was **200 seconds**, also summarized in the paper as **within 5 minutes**.
- Data scale: using this system, the authors collected **1,238 demonstrations** across **22 different environments**, covering two bimanual tasks; they additionally collected **200 demonstrations** from **10 non-expert users** for usability analysis.
- Non-expert usability: each non-expert first watched a **3-minute** instructional video, then performed **10 trials** for each task. The paper reports that **10/10 participants ultimately completed Task 1**, and the time to successful completion consistently decreased with the number of trials; Task 2 was initially harder, but its success rate also increased with repeated practice. No more detailed per-round numerical table is provided.
- Learning feasibility: the authors trained the **ACT (Action Chunking Transformer)** baseline policy on the collected data, training each task separately; the input was **3 RGB-D streams + current joint states**, and the output was a future joint trajectory. The results indicate that the policy “can complete the task” and exhibits behaviors such as re-grasping after failure.
- Quantitative performance: the paper excerpt **does not provide** policy success rate, average return, or numerical comparisons against baselines such as ALOHA, Gello, or handheld solutions, so its strongest evidence is mainly deployment speed, collection scale, number of environments, and experimental observations showing that non-experts can get started quickly.
- Compared with prior systems in the table, the authors claim TRIP-Bag simultaneously provides: **in-the-wild deployment, puppeteering, joint-space control, direct embodiment mapping, calibration-free, operator gripper feedback, full proprioceptive logging**; and they claim that, to the best of their knowledge, this is the first system to satisfy all of these properties at once.

## Link
- [http://arxiv.org/abs/2603.09226v1](http://arxiv.org/abs/2603.09226v1)
