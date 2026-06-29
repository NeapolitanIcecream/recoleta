---
kind: ideas
granularity: day
period_start: '2026-04-04T00:00:00'
period_end: '2026-04-05T00:00:00'
run_id: 2b28af61-f822-4000-a611-e369ac085066
status: succeeded
topics:
- robot-learning
- safety
- data-generation
- medical-robotics
- vla
tags:
- recoleta/ideas
- topic/robot-learning
- topic/safety
- topic/data-generation
- topic/medical-robotics
- topic/vla
language_code: en
pass_output_id: 15
pass_kind: trend_ideas
upstream_pass_output_id: 14
upstream_pass_kind: trend_synthesis
---

# Action-state alignment for robot learning

## Summary
Robot learning work on this day points to three concrete moves: synthetic demonstrations that keep action labels for cross-robot transfer, behavior-switch detection that fits inside control-time safety budgets, and colonoscopy data collection that finally aligns video, commands, actuation, and tip pose for closed-loop training. The common pattern is tighter coupling between observation, action, and safety-relevant state, with numbers that are specific enough to support narrow builds and evaluation changes.

## Action-labeled synthetic demonstration pipelines for cross-embodiment bimanual transfer
Bimanual manipulation teams can now test a specific data pipeline for cross-robot transfer: generate simulator rollouts, turn them into photorealistic videos, and keep the paired action labels for policy training. CRAFT gives this approach a concrete shape. It starts from a small real dataset, builds a digital twin, replays trajectories in simulation, and uses Canny-guided video diffusion so the generated videos preserve motion structure that still matches the actions.

The practical use case is a lab that has demonstrations on one dual-arm setup and wants a policy to work on another without collecting a fresh target-robot dataset. The reported transfer numbers are large enough to justify that workflow as an engineering project, not just a data augmentation experiment. In simulation, transfer from bimanual UR5 to bimanual Franka reached 82.6% on Lift Pot, 89.3% on Place Cans, and 86.0% on Stack Bowls with no target-robot demos. In real tests from xArm7 to Franka, it reached 17/20, 15/20, and 16/20 successes on three tasks. Those results beat both simple shadow baselines and a target-data baseline reported with 100 collected target demos.

A concrete next build is an internal augmentation job for one narrow task family such as pick-place or container handling, with the simulator trajectory, rendered control video, generated photorealistic video, and original action sequence stored together as one training record. The cheap check is whether a policy trained on source-robot data plus generated target-style demonstrations cuts the amount of target teleoperation needed for one new embodiment or camera setup.

### Evidence
- [CRAFT: Video Diffusion for Bimanual Robot Data Generation](../Inbox/2026-04-04--craft-video-diffusion-for-bimanual-robot-data-generation.md): Summary gives the method, the action-label preservation, and the cross-embodiment results in simulation and real tests.
- [CRAFT: Video Diffusion for Bimanual Robot Data Generation](../Inbox/2026-04-04--craft-video-diffusion-for-bimanual-robot-data-generation.md): Abstract confirms the unified augmentation pipeline across viewpoints, lighting, background, and embodiment while keeping action labels via simulator-generated trajectories.

## Behavior-switch detection modules for shared-workspace manipulation safety
Shared-workspace robot teams can add a behavior-switch detector as a control-time safety layer in front of a frozen VLA policy. UA-ToM is a concrete example of that design. It adds a 992K belief module to a frozen 7B backbone, tracks whether a collaborator has changed behavior mid-task, and stays within a 50 ms control budget with 7.4 ms of added inference time.

The operational problem is plain: a robot that continues on an old assumption after a human or partner robot changes strategy keeps moving into the wrong space. This paper ties the detector to a timing target that matters in deployment. At a tighter ±3-step window, about 150 ms in a 50 ms loop, UA-ToM reached 85.7% hard detection across 1,200 episodes. The safety effect is also direct: enabling switch detection cut post-switch collisions from 2.34 to 1.11 per episode, a 52% reduction.

The immediate workflow change is to evaluate collaborative manipulation controllers with a narrow switch window and post-switch collision counts, not only average detection scores under loose tolerances. A concrete pilot would put a small belief tracker beside an existing shared manipulation policy, trigger a conservative fallback or replanning mode on high switch probability, and log collision and close-range time after the switch. Teams working on handover, co-carry, or shared assembly can test this without retraining the base controller.

### Evidence
- [Belief Dynamics for Detecting Behavioral Shifts in Safe Collaborative Manipulation](../Inbox/2026-04-04--belief-dynamics-for-detecting-behavioral-shifts-in-safe-collaborative-manipulation.md): Summary reports the 992K belief module on a frozen 7B VLA, the ±3-step detection result, the collision reduction, and the 7.4 ms overhead.
- [Belief Dynamics for Detecting Behavioral Shifts in Safe Collaborative Manipulation](../Inbox/2026-04-04--belief-dynamics-for-detecting-behavioral-shifts-in-safe-collaborative-manipulation.md): Abstract states the shared-workspace safety problem and the need for reliable regime-switch detection during task execution.

## Aligned multimodal colonoscopy logging for failure-recovery autonomy research
Medical robotics groups now have a concrete way to build closed-loop colonoscopy datasets that are useful for autonomy work, not just retrospective video analysis. OpenRC combines a low-cost robotic retrofit with synchronized logging of video, operator commands, actuation state, and 6-DoF distal tip pose. The data is aligned on a shared stack and released in LeRobot 2.1 format.

That changes the first useful build for labs working on robotic colonoscopy. A dataset can now include navigation, failure, and recovery episodes with action and state alignment tight enough for policy learning and control-aware evaluation. OpenRC reports 1,894 episodes over about 19 hours across 10 task variations, including 142 failure episodes and 141 recovery episodes. After alignment, residual lag between operator action and actuation state is 55.6 ms, and actuation-to-tip-pose lag is centered at 0.0 ms. The hardware cost is under $5,000 excluding the EM tracker, which lowers the barrier for replication.

A practical next step is a failure-recovery benchmark built from lumen loss, wall contact, and fold engagement episodes, with one baseline policy that predicts the next control command and one recovery policy that is only trained on rescue segments. The useful near-term audience is research teams that already have colonoscopy video but lack synchronized action and state logs for closed-loop experiments.

### Evidence
- [OpenRC: An Open-Source Robotic Colonoscopy Framework for Multimodal Data Acquisition and Autonomy Research](../Inbox/2026-04-04--openrc-an-open-source-robotic-colonoscopy-framework-for-multimodal-data-acquisition-and-autonomy-research.md): Summary gives the platform scope, hardware cost, synchronized modalities, dataset size, failure and recovery counts, and alignment residuals.
- [OpenRC: An Open-Source Robotic Colonoscopy Framework for Multimodal Data Acquisition and Autonomy Research](../Inbox/2026-04-04--openrc-an-open-source-robotic-colonoscopy-framework-for-multimodal-data-acquisition-and-autonomy-research.md): Abstract confirms the closed-loop research goal and the simultaneous recording of video, commands, actuation state, and distal tip pose.
