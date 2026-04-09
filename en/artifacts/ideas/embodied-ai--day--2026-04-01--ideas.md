---
kind: ideas
granularity: day
period_start: '2026-04-01T00:00:00'
period_end: '2026-04-02T00:00:00'
run_id: 2b28af61-f822-4000-a611-e369ac085066
status: succeeded
topics:
- robot-manipulation
- surgical-ai
- world-model-safety
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/surgical-ai
- topic/world-model-safety
language_code: en
pass_output_id: 9
pass_kind: trend_ideas
upstream_pass_output_id: 8
upstream_pass_kind: trend_synthesis
---

# Pre-contact control checks

## Summary
Control work in this period points to three concrete workflow changes. In robot manipulation, torque should enter the policy at contact, not throughout the motion. In surgical automation, tool-action-specific safe-region heatmaps can be used as a visible pre-contact check. In world-model planning, evaluation should track whether small perturbations persist and change actions across rollouts, because ordinary one-step accuracy does not capture that exposure.

## Contact-gated torque fusion for diffusion-policy manipulation
A contact-gated torque path is a practical upgrade for robot manipulation teams already running vision-based diffusion policies on contact-rich tasks. The paper’s result is narrow but useful: torque helps when the policy only reads it after contact begins, and the gain is large on tasks where vision cannot reveal insertion state, friction, or load. In the reported setup, adaptive vision-torque fusion reached 82.0% average success across bottle placement, connector pull-out, and egg-boiler lid opening, ahead of torque gating alone at 68.0% and far above vision-only at 30.0%. The bottle experiment is the clearest deployment signal. Vision-only handled empty bottles at 8/10 and full bottles at 0/10, while the adaptive model kept 9/10 on empty and 7/10 on full.

The build here is straightforward: add a contact detector on external joint torque, zero out the torque branch during free motion, and log when the fusion weight turns on. That gives teams a concrete test before retraining a larger policy stack. A cheap validation pass is to replay existing robot logs and measure whether failures cluster at the first-contact window, then compare a vision-only policy against a contact-gated variant on the same SKUs with weight or fit variation. Warehousing, light assembly, and appliance handling teams would care first because they already face cases where the object looks similar before contact but behaves differently once the gripper loads it.

### Evidence
- [Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation](../Inbox/2026-04-01--learning-when-to-see-and-when-to-feel-adaptive-vision-torque-fusion-for-contact-aware-manipulation.md): Summary gives the contact-gated fusion design and the headline 82.0% vs 68.0% vs 30.0% benchmark results.
- [Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation](../Inbox/2026-04-01--learning-when-to-see-and-when-to-feel-adaptive-vision-torque-fusion-for-contact-aware-manipulation.md): Paper text states why vision misses alignment, insertion depth, and contact state in contact-rich tasks.

## Pre-contact safe-region overlays for surgical tool actions
Dense safe-region heatmaps are ready for use as a pre-contact check in surgical automation workflows for cholecystectomy. AffordTissue predicts tool-action-specific tissue interaction zones from video history and a text prompt, and its value is spatial accuracy that a controller or supervisor can inspect before the tool touches tissue. On the reported benchmark, ASSD fell to 20.557 px, compared with 60.184 px for Molmo-VLM and 81.138 px for SAM3. PCK@0.05 reached 0.517, while the baselines stayed at 0.095 and 0.128.

This points to a concrete support layer for teams building semi-autonomous surgical actions: render the predicted heatmap in the console, gate tool motion when the planned contact point leaves the permitted region, and store the heatmap with the action log for review. The ablations help define the product requirements. The language prompt is not optional, because removing the language encoder raised ASSD to 43.135 px. Tool and action conditioning also matter, so a generic anatomy mask is not enough for deployment. A cheap validation check is retrospective: run the model over recorded procedures, compare predicted regions with expert-marked contact sites, and count how often the heatmap would have triggered an early stop before a near-miss or off-target approach.

### Evidence
- [AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction](../Inbox/2026-04-01--affordtissue-dense-affordance-prediction-for-tool-action-specific-tissue-interaction.md): Summary reports the benchmark metrics and ablations showing the value of language, tool, and action conditioning.
- [AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction](../Inbox/2026-04-01--affordtissue-dense-affordance-prediction-for-tool-action-specific-tissue-interaction.md): Paper text states that the heatmap can support explicit policy guidance and early safe stop when tools deviate outside predicted safe zones.

## Trajectory-persistence tests for world-model rollout evaluation
Trajectory-persistence testing is a concrete addition to world-model evaluation for teams using imagined rollouts in planning. The paper does not establish downstream failure rates on a deployed system, but it does give a measurable audit target: how much a small perturbation grows as the model rolls forward. In the reported GRU-based RSSM experiment, the amplification ratio at step 1 reached 2.26x, and adversarial fine-tuning reduced the effect by 59.5%. A stochastic RSSM proxy dropped to 0.65x, which suggests the exposure depends on architecture.

The workflow change is to add persistence checks next to ordinary prediction error metrics before a world model is used inside a planner for robotics or driving. Teams can inject bounded perturbations into inputs or latent states, roll out several steps, and track whether action recommendations drift or recover. The paper’s DreamerV3 evidence is limited to non-zero action drift from checkpoint probing, so the immediate use is an internal red-team harness, not a claim that a production system is unsafe. A cheap first pass is to compare deterministic and stochastic variants of the same model family on the same perturbation suite and record how often the planner’s chosen action changes over the rollout horizon.

### Evidence
- [Safety, Security, and Cognitive Risks in World Models](../Inbox/2026-04-01--safety-security-and-cognitive-risks-in-world-models.md): Summary defines trajectory persistence and reports the 2.26x amplification ratio, 59.5% reduction under adversarial fine-tuning, and 0.65x stochastic proxy result.
- [Safety, Security, and Cognitive Risks in World Models](../Inbox/2026-04-01--safety-security-and-cognitive-risks-in-world-models.md): Paper text describes proof-of-concept trajectory-persistent attacks and checkpoint-level probing of DreamerV3 with non-zero action drift.
