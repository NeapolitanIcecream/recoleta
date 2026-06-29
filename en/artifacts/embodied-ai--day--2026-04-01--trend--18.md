---
kind: trend
trend_doc_id: 18
granularity: day
period_start: '2026-04-01T00:00:00'
period_end: '2026-04-02T00:00:00'
topics:
- robot-manipulation
- surgical-ai
- world-model-safety
run_id: materialize-outputs
aliases:
- recoleta-trend-18
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/surgical-ai
- topic/world-model-safety
language_code: en
pass_output_id: 8
pass_kind: trend_synthesis
---

# Control work is getting more explicit about contact, safe regions, and rollout risk

## Overview
The period is small but coherent: control papers are tying perception to action at the point where mistakes become physical. The strongest evidence is in robotics and surgery, where models gain value by exposing contact state or safe interaction regions. A world-model survey adds a second message: once prediction sits inside planning, safety evaluation has to track how errors persist across rollouts.

## Clusters

### Contact-aware sensor fusion in manipulation
Robot manipulation work today is highly task-conditional. In the contact-aware manipulation paper, the best result comes from using torque only when contact is detected, then mixing vision and torque inside the diffusion policy. That simple timing rule matters: the method reaches 82.0% average success across three real tasks, ahead of torque gating alone at 68.0%, while vision-only and plain feature concatenation both stay at 30.0%. The error pattern is concrete. Vision-only handles empty bottles at 8/10 but drops to 0/10 on full bottles, while the adaptive fusion model keeps 9/10 on empty and 7/10 on full. This points to a narrow but important lesson for robot control: extra sensing helps when the policy knows when to trust it.

#### Evidence
- [Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation](../Inbox/2026-04-01--learning-when-to-see-and-when-to-feel-adaptive-vision-torque-fusion-for-contact-aware-manipulation.md): Summary gives the adaptive contact gate design and the main benchmark numbers.

### Dense safe-region prediction for surgical actions
Surgical automation work is getting more explicit about where an action may safely happen. AffordTissue predicts a dense heatmap for tool-action-specific tissue interaction before contact, using text, video history, and a dedicated decoder. The payoff is in spatial accuracy, not just classification. ASSD falls to 20.557 px, compared with 60.184 px for Molmo-VLM and 81.138 px for SAM3, while PCK@0.05 reaches 0.517 versus 0.095 and 0.128. The ablations also show that the prompt content matters. Removing the language encoder raises ASSD to 43.135 px, and removing tool or action conditioning also hurts. This makes the paper useful as a safety layer story: the model can expose a predicted safe zone that a controller or human can inspect before tool contact.

#### Evidence
- [AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction](../Inbox/2026-04-01--affordtissue-dense-affordance-prediction-for-tool-action-specific-tissue-interaction.md): Summary contains the dataset scope, model inputs, main benchmark metrics, and ablations on language and conditioning.

### World models are getting audited for persistent failure modes
World-model research today is dominated by risk framing rather than new capability gains. The key claim is that rollout-based planning can preserve and amplify small errors or attacks across imagined futures. The paper defines this with a trajectory-persistence metric and reports a 2.26x amplification ratio on a GRU-based recurrent state-space model, with a 59.5% reduction after adversarial fine-tuning. A stochastic proxy drops to 0.65x, so the exposure depends on architecture. The evidence is still limited. The DreamerV3 result shows non-zero action drift from checkpoint probing, but the paper does not provide a full downstream failure-rate benchmark. That leaves this as a useful warning and evaluation agenda, with lighter empirical grounding than the day’s two task papers.

#### Evidence
- [Safety, Security, and Cognitive Risks in World Models](../Inbox/2026-04-01--safety-security-and-cognitive-risks-in-world-models.md): Summary gives the threat model, persistence metric, and proof-of-concept results including amplification and fine-tuning effects.
