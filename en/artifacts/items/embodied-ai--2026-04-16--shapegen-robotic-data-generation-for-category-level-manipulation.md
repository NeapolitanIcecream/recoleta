---
source: arxiv
url: http://arxiv.org/abs/2604.15569v1
published_at: '2026-04-16T22:55:39'
authors:
- Yirui Wang
- Xiuwei Xu
- Angyuan Ma
- Bingyao Yu
- Jie Zhou
- Jiwen Lu
topics:
- robot-data-generation
- category-level-manipulation
- sim2real
- shape-correspondence
- pointcloud-policy
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# ShapeGen: Robotic Data Generation for Category-Level Manipulation

## Summary
ShapeGen generates new robot manipulation demonstrations by swapping the manipulated object with other shapes from the same category while keeping the interaction physically plausible and functionally correct. The paper targets category-level manipulation, where a policy must handle unseen mugs, kettles, and other objects with large shape variation.

## Problem
- Robot policies often fail on unseen objects from the same category because action trajectories depend on object geometry, especially for fine-grained tasks such as hanging a mug or pouring from a kettle.
- Collecting real demonstrations across many object shapes is expensive because it needs many physical objects and substantial human labor.
- Prior data generation methods either focus on texture/view/configuration changes, handle only simple pick-and-place tasks, or rely on simulation and limited shape changes such as axis-aligned scaling.

## Approach
- ShapeGen builds a **Shape Library** for each object category. The library stores 3D object models and learned dense spatial warps from a common template to each shape.
- The core mechanism is a learned point-to-point warping between shapes trained with geometric supervision from signed distance functions (SDFs). This lets the system map a functional point on one object, such as the inside of a mug handle, to the corresponding functional point on another shape.
- For a real source demonstration, a human gives minimal annotation once per demo: task-relevant keypoints, an alignment cost, and a gripper keypoint. The paper says this takes about **1 minute** per source demo.
- Using the learned warp, ShapeGen computes an alignment for a new object shape, adjusts the gripper translation so the grasp remains valid, and composes a new 3D observation by replacing the original object and moving the segmented robot arm point cloud.
- The system is simulator-free and real-to-real: it uses scanned real objects, RGB-D observations, object tracking, and 3D compositing instead of running the task in simulation.

## Results
- On **hang_mug**, success on unseen object instances rises from **1/20 (5%)** with source-only training to **9/20 (45%)** with ShapeGen data.
- On **hang_mug_hard**, success rises from **1/20 (5%)** to **10/20 (50%)**.
- On **serve_kettle**, success rises from **7/20 (35%)** to **15/20 (75%)**.
- On **pour_water**, success rises from **11/20 (55%)** to **12/20 (60%)**.
- Training data scale in the main experiment: for each of **4 tasks**, the authors collect **5** teleoperated source demos with one object instance and generate **15** novel demos per source demo.
- The main claimed breakthrough is that simulator-free, real-to-real shape augmentation improves category-level generalization for fine-grained manipulation on unseen object shapes, with the largest reported gain at **+40 percentage points** on **hang_mug_hard** and **+40 points** on **hang_mug**.

## Link
- [http://arxiv.org/abs/2604.15569v1](http://arxiv.org/abs/2604.15569v1)
