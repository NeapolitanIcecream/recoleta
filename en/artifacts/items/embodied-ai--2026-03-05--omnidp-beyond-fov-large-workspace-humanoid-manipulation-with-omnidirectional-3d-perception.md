---
source: arxiv
url: http://arxiv.org/abs/2603.05355v2
published_at: '2026-03-05T16:34:53'
authors:
- Pei Qu
- Zheng Li
- Yufei Jia
- Ziyun Liu
- Liang Zhu
- Haoang Li
- Jinni Zhou
- Jun Ma
topics:
- humanoid-manipulation
- lidar-perception
- diffusion-policy
- point-cloud-policy
- omnidirectional-perception
- teleoperation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception

## Summary
This paper proposes OmniDP, an end-to-end LiDAR-driven visuomotor policy for humanoid robot manipulation, using 360° point clouds to replace narrow-FOV RGB-D perception and support large-workspace manipulation beyond the camera’s field of view. Its core value is enabling the robot to reliably detect targets, avoid obstacles, and perform whole-body coordinated manipulation even in scenarios where frequent base repositioning is difficult.

## Problem
- Existing RGB-D/depth-camera policies usually have a narrow field of view. Once the target or obstacle lies outside the camera view, this can lead to grasp failures, collisions, or frequent repositioning.
- For humanoid robots, additional active vision mechanisms, third-person cameras, or multi-camera calibration introduce mechanical complexity, latency, calibration dependence, and real-time performance issues.
- This matters because large-area tasks in real unstructured environments—such as handover, wiping, and pouring—often require robots to maintain omnidirectional environmental awareness and operate safely even when moving the body is inconvenient.

## Approach
- The authors propose **OmniDP**: the input consists of 360° point clouds from a head-mounted panoramic LiDAR and a 43-dimensional proprioceptive state, and the output is 28-dimensional upper-limb joint actions; the lower body/waist is controlled by pretrained HOMIE, enabling whole-body coordinated manipulation.
- The perception encoder uses point-cloud pyramid convolution and introduces **Time-Aware Attention Pooling (TAP)**: historical point clouds within a short time window are concatenated, each point is augmented with a relative timestamp, and attention gives more weight to newer observations, mitigating issues from LiDAR sparsity, flicker, and instability in single-frame pooling.
- For point-cloud preprocessing, points beyond 1.3 m are first cropped according to manipulator reachability, then uniformly downsampled to 4096 points to balance near-field geometric information and real-time inference efficiency.
- To train the policy, the authors build a lightweight XR whole-body teleoperation system based on Meta Quest 3, collecting demonstration data on Unitree G1 that includes walking, trunk adjustment, coordinated dual-arm motion, and dexterous hand operation.
- One key engineering detail is that the point cloud is represented directly in the LiDAR’s own coordinate frame, so deployment does not require extrinsic calibration, improving cross-environment adaptability.

## Results
- **Overall task success rate (6 tasks, including simulation and real world)**: OmniDP achieves **82/120**, significantly outperforming **DP 18/120, DP3 22/120, iDP3 25/120**.
- **The advantage on out-of-view (OV) tasks is especially clear**: for example, in simulated **Pour (OV)**, OmniDP achieves **12/20**, while **DP/DP3/iDP3 are all 0/20**; for real **Hand Over (OV)**, it is **12/20 vs all baselines 0/20**; for real **Pour (OV)**, **11/20 vs all baselines 0/20**; for real **Wipe (OV)**, **16/20 vs all baselines 0/20**.
- **It is also stronger on standard visible tasks**: in simulated Pick & Place, OmniDP reaches **16/20**, higher than **DP 10/20, DP3 13/20, iDP3 14/20**; in real Pick & Place, OmniDP achieves **15/20**, higher than **8/20, 9/20, 11/20**.
- **Obstacle-avoidance evaluation**: when obstacles are outside the camera view, OmniDP has a success rate of **14/20** and a collision rate of **5/20**; in contrast, **DP 0/20, 20/20**, **DP3 0/20, 18/20**, **iDP3 0/20, 18/20**, showing that omnidirectional perception significantly improves safety.
- **Generalization evaluation (Pick & Place)**: on different instances, different lighting, and different scenes, the results are **13/20**, **15/20**, and **12/20**, all better than **iDP3’s 12/20, 12/20, 10/20**, and also better than the weaker DP/DP3.
- **Ablation study**: on the Hand Over task, full OmniDP achieves **12/20**; removing omnidirectional observation reduces it to **0/20**; removing TAP lowers it to **9/20**, indicating that both 360° perception and time-aware attention pooling are critical to performance.

## Link
- [http://arxiv.org/abs/2603.05355v2](http://arxiv.org/abs/2603.05355v2)
