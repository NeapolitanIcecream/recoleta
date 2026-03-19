---
source: arxiv
url: http://arxiv.org/abs/2603.04639v1
published_at: '2026-03-04T21:59:32'
authors:
- Yinpei Dai
- Hongze Fu
- Jayjun Lee
- Yuejiang Liu
- Haoran Zhang
- Jianing Yang
- Chelsea Finn
- Nima Fazeli
- Joyce Chai
topics:
- robotic-manipulation
- memory-augmented-policy
- vision-language-action
- benchmarking
- long-horizon-control
relevance_score: 0.52
run_id: materialize-outputs
language_code: en
---

# RoboMME: Benchmarking and Understanding Memory for Robotic Generalist Policies

## Summary
This paper introduces RoboMME, a large-scale standardized benchmark for memory capabilities in robotic generalist policies, and systematically compares 14 memory-augmented variants on a unified \(\pi_{0.5}\) VLA backbone. The core conclusion is that there is no “one-size-fits-all” memory design for robotics: different tasks prefer different memory representations, but perceptual memory combined with modulator-style integration is the most balanced overall.

## Problem
- Long-horizon robotic manipulation often depends on historical information, such as counting, tracking under occlusion, cross-temporal reference, and imitation from demonstrations; relying only on the current observation is often insufficient to determine the correct action.
- Existing memory-based robotic methods use different backbones, different tasks, and different evaluation protocols, making fair comparison difficult and making it hard to know which memory mechanisms are truly effective.
- Existing benchmarks either have too few tasks and are close to being saturated, or have short horizons and insufficient demonstrations, so they cannot systematically cover temporal, spatial, object, and procedural memory demands.

## Approach
- Construct RoboMME: 16 non-Markovian, long-horizon manipulation tasks divided into 4 suites that test temporal, spatial, object, and procedural memory respectively; in total, 1,600 demonstrations, 770k training timesteps, and an average of about 481 steps per task.
- The tasks cover real memory demands such as counting, location tracking under occlusion and swapping, object identification under brief highlighting/video/language references, and reproducing demonstrated trajectories and manipulation styles.
- Build 14 memory-augmented VLAs on the unified \(\pi_{0.5}\) backbone: three categories of memory representations include symbolic (language subgoals), perceptual (historical visual tokens), and recurrent (TTT/RMT compressed states).
- Further compare three integration methods: memory-as-context (concatenating memory to the input), memory-as-modulator (using memory to modulate action experts), and memory-as-expert (adding a dedicated memory expert).
- For fair evaluation, the authors fix the memory budget at 512 tokens, perform multi-task training on 16 tasks, and compare against baselines including \(\pi_{0.5}\), past-actions, SAM2Act+, and MemER.

## Results
- In terms of benchmark scale, RoboMME covers **4 memory types**, **16 tasks**, **1,600 demonstrations**, and **770k timesteps**; compared with MemoryBench’s **3 tasks / 300 demos** and MIKASA-robo(VLA)’s **12 tasks / 1,250 demos**, it provides more complete coverage and training scale.
- Task horizons are significantly longer: RoboMME averages **481 steps/episode**; the average number of steps for individual tasks ranges from **208** (PatternLock) to **1,134** (VideoPlaceOrder), emphasizing realistic long-horizon historical dependence.
- The authors evaluate **14** in-house MME-VLA variants and **4** existing methods; under a unified setup, they find that **no single memory representation or integration strategy remains consistently optimal across all tasks**, indicating that conclusions drawn from single-task settings are not broadly generalizable.
- Qualitatively, **symbolic memory** is better at counting and short-horizon reasoning; **perceptual memory** is more critical for time-sensitive and motion-centric tasks; the best trade-off between overall performance and computational efficiency is **perceptual memory + memory-as-modulator**.
- The provided text excerpt does not include the complete main results table with **average success rates / per-task values** for each method, so a full set of quantitative SOTA metrics cannot be listed reliably; the strongest quantitative information that can be extracted with confidence is mainly the benchmark scale, task lengths, and comparison setup.

## Link
- [http://arxiv.org/abs/2603.04639v1](http://arxiv.org/abs/2603.04639v1)
