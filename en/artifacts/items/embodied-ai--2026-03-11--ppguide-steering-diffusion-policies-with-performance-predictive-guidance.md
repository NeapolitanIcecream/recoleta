---
source: arxiv
url: http://arxiv.org/abs/2603.10980v1
published_at: '2026-03-11T17:10:16'
authors:
- Zixing Wang
- Devesh K. Jha
- Ahmed H. Qureshi
- Diego Romeres
topics:
- diffusion-policy
- inference-time-guidance
- multiple-instance-learning
- robot-manipulation
- imitation-learning
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# PPGuide: Steering Diffusion Policies with Performance Predictive Guidance

## Summary
PPGuide proposes a method for guiding diffusion-based robotic policies **at inference time**, using sparse success/failure terminal signals rather than dense rewards or world models to improve robustness. The core idea is to first automatically identify “which observation-action chunks most affect success or failure” within a trajectory, and then use that signal to apply gradient guidance during the sampling process.

## Problem
- Although diffusion policies can learn complex, multi-modal manipulation behaviors, small errors in generated action sequences can accumulate over time, causing long-horizon tasks to fail.
- Existing methods for improving robustness typically rely on **more expert data/corrective demonstrations**, **dense rewards**, or **world models**, which are often costly or difficult to obtain in robotic settings.
- The challenge is: given only a binary success/failure label for the entire trajectory, how can this sparse supervision be turned into a differentiable action-guidance signal usable at every timestep?

## Approach
- First, collect rollouts from the pre-trained diffusion policy at checkpoints from different training stages, yielding diverse trajectories containing both successes and failures.
- Treat an entire trajectory as an MIL bag, and each observation-action chunk as an instance; use **attention-based Multiple Instance Learning** to automatically identify the most relevant chunks using only trajectory-level success/failure labels.
- Use the MIL attention weights to create pseudo-labels, dividing instances into **Success-Relevant (SR)**, **Failure-Relevant (FR)**, and **Irrelevant (IR)**; the paper states that the number of IR instances is more than **10x** that of SR/FR.
- Train a lightweight three-class guider on these pseudo-labels; at inference time, compute the gradient of the classifier’s log-probabilities for SR/FR with respect to the action, **promoting SR and suppressing FR**, and inject this gradient into the diffusion denoising process.
- To reduce inference cost, the paper proposes **alternating guidance**: guidance is not added at every denoising step, but every other step, claiming performance close to constant guidance with lower computation.

## Results
- Evaluated on 8 tasks from Robomimic and MimicGen, where the base diffusion policy was trained using only **10% of the original expert demonstrations**; PPGuide training data came from rollouts at epochs **250/300/350/400/450**, and testing was conducted on checkpoints at epochs **500/550**.
- Compared with the baseline Diffusion Policy (DP), PPGuide shows clear gains on multiple tasks: for example, **Square** improves from **62%→72%(+10)**@500 and **58%→66%(+8)**@550; **Transport** from **60%→68%(+8)**@500 and **68%→76%(+8)**@550; **Mug Cleanup D1** from **26%→36%(+10)**@550.
- Gains also appear on harder or longer-horizon tasks: **Coffee D2** from **54%→58%(+4)**@500 and **46%→58%(+12)**@550; **Kitchen D1** from **40%→44%(+4)**@550; **Coffee Preparation D1** from **18%→22%(+4)**@550.
- Compared with its variants, **PPGuide-CG** (constant guidance at every step) and **PPGuide** (alternating guidance) both overall outperform the random-sampling-style methods **PPGuide-SS/DP-SS**; the authors claim alternating guidance “almost matches” constant guidance while significantly reducing extra forward-pass computation.
- Evaluation with heterogeneous base policies (Table III) shows some generalization: **Square** at epoch **1300** improves from **54%→70%(+16)**, and **Transport** at epoch **1300** from **56%→74%(+18)**, though there are also occasional drops, such as **Transport 1500** from **74%→70%(-4)**.
- The paper’s central empirical claim is that, **without a world model, without dense rewards, and without retraining the main policy**, PPGuide can consistently improve the success rate of pre-trained diffusion policies across multiple tasks.

## Link
- [http://arxiv.org/abs/2603.10980v1](http://arxiv.org/abs/2603.10980v1)
