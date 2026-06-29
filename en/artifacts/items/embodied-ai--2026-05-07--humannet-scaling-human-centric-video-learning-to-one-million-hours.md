---
source: arxiv
url: https://arxiv.org/abs/2605.06747v1
published_at: '2026-05-07T15:21:58'
authors:
- Yufan Deng
- Daquan Zhou
topics:
- human-centric-video
- robot-data-scaling
- vision-language-action
- embodied-foundation-model
- human-to-robot-transfer
- egocentric-video
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# HumanNet: Scaling Human-centric Video Learning to One Million Hours

## Summary
HumanNet is a 1,000,000-hour human-centric video corpus for embodied learning, with first-person and third-person clips, captions, motion descriptions, and hand/body signals. The paper claims that 1,000 hours of egocentric HumanNet pretraining can match or slightly beat 100 hours of real-robot pretraining in a controlled VLA validation.

## Problem
- Robot and embodied policies need large interaction data, but real-robot datasets are costly, smaller, and often tied to one robot platform or task set.
- Human videos contain manipulation, tool use, navigation, full-body motion, and long-horizon procedures at much larger scale than teleoperated robot logs.
- The key problem is turning broad internet and collected human video into data that supports robot-relevant pretraining rather than generic video recognition.

## Approach
- HumanNet collects and filters human-centric video where human activity is central, including object manipulation, tool use, locomotion, assembly, appliance use, transport, and multi-step tasks.
- The dataset keeps both egocentric and exocentric viewpoints: first-person clips capture hand-object contact and actor intent, while third-person clips capture full-body motion and scene context.
- The pipeline uses keyword discovery, web and platform retrieval, open-source datasets, and self-collected recordings, then applies deduplication, normalization, content filtering, quality filtering, scene splitting, and clip creation.
- Annotation adds 3D hand/body pose, monocular SLAM for suitable first-person clips, motion retargeting, video captions, motion descriptions, and activity classes.
- A clip can enter the robot-ready subset when motion retargeting error is below 15 mm and valid-frame coverage exceeds 60%.

## Results
- HumanNet reports 1,000,000 hours of human-centric video with both first-person and third-person views; the paper compares this with EgoScale at 20,854 hours, Ego4D at about 3,670 hours, Ego-Exo4D at 1,286 hours, OpenEgo at 1,107 hours, and EPIC-KITCHENS-100 at about 100 hours.
- The controlled VLA validation uses the same LingBot-VLA architecture and the same downstream robot corpus: 34 hours, 100 tasks, and 20 episodes per task.
- The comparison tests four initializations: Qwen VLM, Qwen adapted with 100 hours of real-robot CoBot data, Qwen adapted with 1,000 hours of egocentric HumanNet video, and LingBot trained with 20,000 hours of real-robot data.
- Across five held-out task groups, the 1,000-hour egocentric HumanNet initialization reportedly matches and on several groups slightly surpasses the 100-hour real-robot CoBot initialization.
- The excerpt does not provide exact validation-loss values, so the strongest quantitative claim is the data-efficiency comparison: 1,000 hours of human egocentric video performs on par with or better than 100 hours of robot video under the fixed 34-hour downstream setup, while reducing the gap to a 20,000-hour robot-trained LingBot baseline.

## Link
- [https://arxiv.org/abs/2605.06747v1](https://arxiv.org/abs/2605.06747v1)
