---
kind: ideas
granularity: day
period_start: '2026-04-16T00:00:00'
period_end: '2026-04-17T00:00:00'
run_id: 006dd63e-d43e-4c5c-97bc-f01a25413d82
status: succeeded
topics:
- robotics
- vision-language-action
- data generation
- dexterous manipulation
- sim2real
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/data-generation
- topic/dexterous-manipulation
- topic/sim2real
language_code: en
pass_output_id: 75
pass_kind: trend_ideas
upstream_pass_output_id: 74
upstream_pass_kind: trend_synthesis
---

# Physical data augmentation for robot manipulation

## Summary
Robotics work in this window gives three concrete workflow changes. Mobile manipulation teams can add docking-pose augmentation around existing demonstrations to recover performance under navigation error. Category-level manipulation teams can generate new real demonstrations by warping object geometry within a class, which looks useful for handle- and contact-sensitive tasks. Dexterous hand groups can cut collection cost with attached portable teleoperation rigs that improve operator success and speed on real hardware.

## Docking-pose augmentation for mobile manipulation policies
Mobile manipulators need a docking-robust data pipeline, not just a better controller. DockAnywhere gives a concrete recipe: record a small set of demonstrations at one docking pose, split each trajectory into approach motion and contact-rich skill segments, keep the manipulation segment fixed, and regenerate only the approach for new feasible base poses. The paper also changes the camera setup for this workflow by using a fixed third-person RGB-D view, then edits observations in 3D point-cloud space so the new view and the reused action sequence stay aligned.

This looks practical for teams already running a two-stage stack with navigation followed by fixed-base manipulation. The reported failure is direct: plain DP3 falls from 88.6% success with one docking point to 17.8% when evaluated across five docking points. With DockAnywhere augmentation, overall success reaches 78.9%, and most of the gain appears by four augmented docking points. A cheap validation step is to take one existing mobile manipulation task, collect demonstrations from one dock, synthesize three or four nearby docks, and measure whether success at unseen stops recovers without recollecting the contact phase of the task.

### Evidence
- [DockAnywhere: Data-Efficient Visuomotor Policy Learning for Mobile Manipulation via Novel Demonstration Generation](../Inbox/2026-04-16--dockanywhere-data-efficient-visuomotor-policy-learning-for-mobile-manipulation-via-novel-demonstration-generation.md): Provides the core method, failure mode under docking shifts, and the main success-rate comparisons including 78.9% overall success and the drop to 17.8% for plain DP3 across five docking points.
- [DockAnywhere: Data-Efficient Visuomotor Policy Learning for Mobile Manipulation via Novel Demonstration Generation](../Inbox/2026-04-16--dockanywhere-data-efficient-visuomotor-policy-learning-for-mobile-manipulation-via-novel-demonstration-generation.md): Confirms the paper frames the method as lifting one demonstration to diverse feasible docking configurations for mobile manipulation.

## Real-to-real shape augmentation for category-level manipulation
Category-level manipulation teams can now build a real-to-real data generation step around object geometry instead of recollecting demonstrations for every new mug, kettle, or handle shape. ShapeGen uses a shape library with learned dense warps between objects in the same category, then asks for light human annotation per source demo to map task-relevant points and adjust the grasp. The reported annotation cost is about one minute per source demo, which keeps the workflow close to ordinary teleoperation collection.

The reported gains are large enough to justify a narrow deployment around tasks where geometry drives failure. On unseen objects, hang_mug rises from 5% to 45%, hang_mug_hard from 5% to 50%, and serve_kettle from 35% to 75%. The weakest result here is pour_water, which only moves from 55% to 60%, so this looks most useful for tasks with tight functional contact points such as handles, hooks, and pour poses. A cheap check is to scan a small object family already used in training, generate warped demonstrations from five hand-collected source demos, and compare success on held-out shapes before expanding the pipeline.

### Evidence
- [ShapeGen: Robotic Data Generation for Category-Level Manipulation](../Inbox/2026-04-16--shapegen-robotic-data-generation-for-category-level-manipulation.md): Contains the simulator-free real-to-real method, the minimal human annotation requirement, and the task-level gains on unseen object instances.
- [ShapeGen: Robotic Data Generation for Category-Level Manipulation](../Inbox/2026-04-16--shapegen-robotic-data-generation-for-category-level-manipulation.md): Confirms the paper targets category-level geometric variation in real-world manipulation.

## Attached dexterous teleoperation rigs for lower-cost real-hand data collection
Dexterous hand labs have a clear chance to lower the cost of data collection by standardizing on a portable attached teleoperation rig. DEX-Mouse is built from off-the-shelf parts for under USD 150, avoids per-user calibration, and adds current-based kinesthetic force feedback. The attached setup matters because it reduces the mismatch between human motion and robot-hand motion: the robot hand is mounted on the operator's forearm, and the system uses simple proportional retargeting instead of a heavier morphology-specific mapping stack.

The reported user study gives a useful first benchmark for adoption. In the attached configuration, DEX-Mouse reaches 86.67% overall success and 10.05 seconds average completion time, ahead of the two glove baselines in the study. The gap versus remote teleoperation is also large: 86.67% versus 52.5% overall success for DEX-Mouse itself. For a lab choosing between another custom glove build and a simpler collection rig, the immediate test is small and cheap: run the same three contact-rich tasks in attached and remote modes, track completion rate and time per operator, and check whether the higher-quality data offsets the narrower physical setup.

### Evidence
- [DEX-Mouse: A Low-cost Portable and Universal Interface with Force Feedback for Data Collection of Dexterous Robotic Hands](../Inbox/2026-04-16--dex-mouse-a-low-cost-portable-and-universal-interface-with-force-feedback-for-data-collection-of-dexterous-robotic-hands.md): Provides the hardware cost, attached-versus-remote setup, and the user-study results including success rates and completion times.
- [DEX-Mouse: A Low-cost Portable and Universal Interface with Force Feedback for Data Collection of Dexterous Robotic Hands](../Inbox/2026-04-16--dex-mouse-a-low-cost-portable-and-universal-interface-with-force-feedback-for-data-collection-of-dexterous-robotic-hands.md): Confirms the system is open-sourced for replication and adoption and states the headline attached-configuration result.
