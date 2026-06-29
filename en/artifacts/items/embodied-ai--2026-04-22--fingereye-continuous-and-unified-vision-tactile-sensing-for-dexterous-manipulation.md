---
source: arxiv
url: http://arxiv.org/abs/2604.20689v2
published_at: '2026-04-22T15:37:34'
authors:
- Zhixuan Xu
- Yichen Li
- Xuanye Wu
- Tianyu Qiu
- Lin Shao
topics:
- vision-tactile-sensing
- dexterous-manipulation
- imitation-learning
- sim2real
- robot-sensing
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# FingerEye: Continuous and Unified Vision-Tactile Sensing for Dexterous Manipulation

## Summary
FingerEye is a low-cost fingertip sensor that keeps one visual stream active before contact, at contact onset, and after contact. The paper pairs this hardware with an imitation-learning policy and a simulation digital twin for dexterous manipulation.

## Problem
- Dexterous manipulation needs feedback across the whole interaction: approach, first touch, and force regulation after contact.
- Common tactile sensors such as GelSight only become useful after contact, while external cameras give weak or occluded cues near the contact region.
- This gap makes contact initiation unstable in tasks that need millimeter-scale alignment and fast force adjustment, such as standing a coin or picking thin objects.

## Approach
- FingerEye combines two fingertip RGB cameras with a compliant silicone ring and a transparent acrylic cover carrying 35 AprilTags. Before contact, the cameras see the object; after contact, ring deformation moves the tagged plate, so the same cameras also measure touch-related deformation.
- The two cameras have different placements and focal setups: a tip camera for close deformation sensing and a root camera for wider pre-contact scene visibility. This gives implicit stereo depth and continuous sensing without switching modalities.
- Contact wrench is inferred from the 6D pose change of the AprilTag layout. The system estimates plate pose with multi-tag PnP plus Levenberg–Marquardt refinement, using all visible tag corners for better stability under occlusion and deformation.
- For control, the paper uses a transformer imitation-learning policy that fuses images from multiple FingerEye sensors and a wrist camera, plus robot joint states and recent tag-pose history, to predict chunks of future actions.
- To improve generalization with limited real data, the authors build a FingerEye digital twin in Isaac Lab and mix real demonstrations with a smaller simulated set that is heavily visually randomized.

## Results
- The sensor hardware is compact and cheap: about 28.0 × 25.4 × 26.0 mm per module, built from off-the-shelf and 3D-printed parts, with material cost around $60.
- Sensitivity analysis reports minimum detectable wrench of [4.30, 4.22, 9.93, 0.32, 0.13, 8.55]^T in mN and mN·m across the six force/torque axes.
- For force–deformation calibration, the authors collect more than 1,000 synchronized wrench–pose pairs across all 6 dimensions, train on 80% and test on 20%, and report high test R^2 with low test RMSE in Fig. 4. The excerpt does not include the exact per-axis numbers.
- In delicate grasping, a LEAP Hand with FingerEye grasps 9 fragile or deformable objects, halting finger motion when fingertip normal deformation indicates contact. The paper claims consistent contact-onset detection and damage-free lifting.
- The paper claims successful dexterous manipulation on tasks including coin standing, chip picking, letter retrieving, and syringe manipulation.
- The excerpt does not provide task-level policy success rates, baseline comparisons, or sim-augmentation gains, so the main quantitative evidence available here is the sensor cost, size, sensitivity, and the >1,000-sample wrench calibration setup.

## Link
- [http://arxiv.org/abs/2604.20689v2](http://arxiv.org/abs/2604.20689v2)
