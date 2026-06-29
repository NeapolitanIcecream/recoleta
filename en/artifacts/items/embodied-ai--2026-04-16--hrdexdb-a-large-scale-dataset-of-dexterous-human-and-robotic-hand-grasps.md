---
source: arxiv
url: http://arxiv.org/abs/2604.14944v1
published_at: '2026-04-16T12:38:14'
authors:
- Jongbin Lim
- Taeyun Ha
- Mingi Choi
- Jisoo Kim
- Byungjun Kim
- Subin Jeon
- Hanbyul Joo
topics:
- dexterous-manipulation
- human-robot-dataset
- cross-embodiment-learning
- tactile-sensing
- grasp-dataset
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# HRDexDB: A Large-Scale Dataset of Dexterous Human and Robotic Hand Grasps

## Summary
HRDexDB is a paired human-robot dexterous grasp dataset built to study how grasp skills transfer across embodiments. It combines synchronized multi-view video, 3D motion, object pose, tactile sensing, and success labels for the same set of objects and related human and robot grasps.

## Problem
- Existing hand and robot manipulation datasets usually cover only one side: human hands, robot hands, or low-DoF grippers. They rarely align human and robot grasps on the same objects with comparable motions.
- Dexterous manipulation needs more than RGB video. Learning grasp behavior and contact-rich control also needs 3D hand or robot motion, object 6D pose, tactile signals, and failure cases.
- Marker-based gloves and sparse camera setups can reduce image quality or fail under occlusion, which makes precise hand-object tracking hard.

## Approach
- The paper introduces **HRDexDB**, a markerless paired dataset of dexterous grasps for human hands and multiple robot hand embodiments on the same 100 objects.
- Data is captured with a unified system: **21 calibrated external RGB cameras + 2 egocentric cameras**, all synchronized at **30 Hz**, with robot states and tactile signals aligned to the camera frames.
- The robot platform uses an **xArm6** with **three dexterous hands**: **Allegro Hand**, **Inspire RH56DFTP**, and **Inspire RH56F1**. Human data adds the fourth embodiment.
- Pairing is created through a mimicry protocol: a human performs a grasp, then a teleoperator reproduces the same grasp strategy with the robot, so the human and robot trials match in object, scene, and task intent.
- Reconstruction combines calibrated multi-view capture, MANO-based human hand fitting, robot kinematics, camera-to-robot calibration, object **6D pose** tracking, tactile sensing, and **success/failure** labels in one world coordinate system.

## Results
- Dataset scale: **1.4K grasping trials**, **100 objects**, **4 embodiments**, and about **12.8M frames**.
- Modalities per sequence include **21 multi-view RGB streams**, **2 egocentric views**, **3D human hand or robot trajectories**, **object 6D pose**, **tactile signals** for robotic hands, and **binary success/failure annotations**.
- Compared with prior paired human-robot datasets in Table 1, HRDexDB claims a rarer combination of properties in one dataset: **dexterous robot hands**, **tactile sensing**, **markerless capture**, **3D hand reconstruction**, and **object 6D pose**, with **23 views** at **2048×1536** resolution.
- The paper claims HRDexDB is the **first large-scale markerless paired human-robot dexterous manipulation dataset** with synchronized tactile data and multiple robotic hand embodiments.
- The excerpt does **not report learning benchmark scores or task-performance gains** for trained models. Its main claimed result is the dataset and capture system itself, with ongoing expansion from **100+ objects toward 1,000 objects**.

## Link
- [http://arxiv.org/abs/2604.14944v1](http://arxiv.org/abs/2604.14944v1)
