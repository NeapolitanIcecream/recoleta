---
source: arxiv
url: http://arxiv.org/abs/2604.04967v1
published_at: '2026-04-04T02:41:09'
authors:
- Devashri Naik
- Divake Kumar
- Nastaran Darabi
- Amit Ranjan Trivedi
topics:
- collaborative-manipulation
- behavioral-shift-detection
- vision-language-action
- safe-robotics
- theory-of-mind
relevance_score: 0.75
run_id: materialize-outputs
language_code: en
---

# Belief Dynamics for Detecting Behavioral Shifts in Safe Collaborative Manipulation

## Summary
This paper studies how a robot can detect when a collaborator changes behavior during a shared manipulation task. It introduces UA-ToM, a small belief-tracking module added to a frozen vision-language-action controller, and shows better switch detection reliability and safer post-switch behavior than most baselines.

## Problem
- The paper targets **mid-episode behavioral regime switches** in collaborative manipulation, where another agent changes from one behavior type to another without warning.
- This matters because a robot that keeps acting on an old assumption can move into unsafe states and raise collision risk in shared workspaces.
- The authors argue that average detection scores can hide deployment risk: at a loose tolerance window, all methods can look perfect even when some are too slow for a 50 ms control loop.

## Approach
- UA-ToM adds a **992K-parameter belief module** on top of a **frozen 7B VLA backbone**; the backbone produces latent features, and the new module tracks the collaborator’s likely behavior over time.
- Its main mechanism is a **selective state-space belief update** that keeps a persistent hidden state, so the detector can accumulate evidence across timesteps instead of reacting only to the latest observation.
- It combines four signals: persistent belief dynamics, **causal attention** over recent observations, **prediction error** between predicted and actual collaborator actions, and **prototype memory** for behavior types.
- A fusion gate uses these signals to predict three outputs: collaborator type, switch probability, and collaborator action.
- The key idea in simple terms: keep a running belief about the other agent, watch for mismatches between expected and actual behavior, and trigger adaptation when that belief changes fast enough.

## Results
- In ManiSkill shared-workspace tasks, enabling regime-switch detection cut **post-switch collisions from 2.34 ± 0.40 to 1.11 ± 0.12 per episode**, a **52% reduction** over **5 seeds**.
- At the common **±5 step** detection window, **all methods reached 100% hard detection**, which hides meaningful differences. At the tighter **±3 step window** (about **150 ms** in a **50 ms** control loop), methods split into tiers: fast detectors **>82%**, agent-modeling methods **58–62%**, and slower recurrent methods **30–33%**.
- **UA-ToM** reached **85.7% hard detection** at **±3 steps** across **1200 episodes / 5 seeds**, the best among unassisted methods. Baselines reported: **Mamba 85.0%**, **Transformer 82.5%**, **LIAM 62.4%**, **BOCPD 58.1%**, **GRU 33.2%**, **BToM 30.4%**.
- UA-ToM also had strong reliability across seeds with **R = 0.93**, close to the privileged context-conditioned baseline at **86.1%** and **R = 0.94**.
- In extended **300-step** evaluation over **10 seeds**, **UA-ToM (MS)** achieved the lowest **close-range time (CRT)** at **4.8 ± 1.1 steps**, lower than **Oracle: 5.3 ± 0.9**, while keeping **97.5 ± 0.9%** detection. The paper interprets this as smoother belief revision producing safer clearance after the switch.
- Mechanistic analysis reports that hidden-state update magnitude rises by **17×** at regime switches, driven by a **2.3×** spike in action prediction error, while the discretization step converges to **Δ_t ≈ 0.78**. The module adds **7.4 ms** inference overhead, or **14.8%** of a **50 ms** control budget.

## Link
- [http://arxiv.org/abs/2604.04967v1](http://arxiv.org/abs/2604.04967v1)
