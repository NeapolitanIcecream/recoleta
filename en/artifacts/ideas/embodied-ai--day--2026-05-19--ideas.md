---
kind: ideas
granularity: day
period_start: '2026-05-19T00:00:00'
period_end: '2026-05-20T00:00:00'
run_id: bfdb3bae-77e6-44b1-88f2-6274001cf2f7
status: succeeded
topics:
- Embodied AI
- Vision-language-action models
- Robot manipulation
- World models
- Robot evaluation
- Synthetic data
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vision-language-action-models
- topic/robot-manipulation
- topic/world-models
- topic/robot-evaluation
- topic/synthetic-data
language_code: en
pass_output_id: 187
pass_kind: trend_ideas
upstream_pass_output_id: 186
upstream_pass_kind: trend_synthesis
---

# Robot Policy Stress Testing

## Summary
Robot teams can make VLA reliability easier to debug by adding stage-level manipulation tests, latency-injection runs for asynchronous control, and generated 3DGS flight scenes with dynamics-aware trajectories. The strongest cases are evaluation and deployment checks, because the reported failures are tied to concrete stages, perturbations, and delay values.

## Stage-level manipulation evaluation for VLA release checks
A robot team evaluating a VLA policy for fine manipulation should add task graphs and stage metrics before using a policy in part-sensitive tasks. MetaFine shows why: object-level grasping can look high while part-level control fails. The reported best policy reaches 80% on Grasp Part, 68% on Press Part, and 12% on Rotate Along under part-level constraints, while conventional evaluation can overstate fine-grained ability by up to 70%.

A practical release check would split each hardware task into language understanding, spatial perception, and motor behavior stages. For a peg-in-hole task, the dashboard should show grasp, align, insert, and trajectory smoothness separately. MetaFine’s peg-in-hole results show near-zero overall success across five VLAs, but stage metrics still identify different failure points: OpenVLA-OFT grasps in 47% of trials and aligns in 19%, while pi_0.5 grasps in 39% and aligns in 0%.

This is useful for model selection and repair work. MetaFine reports that replacing pi_0.5’s SigLIP encoder with a multi-scale cross-attention encoder, while freezing the VLM backbone and action head, raises grasp success from 39% to 67% and alignment from 0% to 32%. That gives evaluation teams a direct path from failed stage to component-level fix.

### Sources
- [Beyond Binary Success: A Diagnostic Meta-Evaluation Framework for Fine-Grained Manipulation](../Inbox/2026-05-19--beyond-binary-success-a-diagnostic-meta-evaluation-framework-for-fine-grained-manipulation.md): MetaFine reports atomic manipulation skills, perturbation tests, stage metrics, headline inflation, and component repair results.
- [Beyond Binary Success: A Diagnostic Meta-Evaluation Framework for Fine-Grained Manipulation](../Inbox/2026-05-19--beyond-binary-success-a-diagnostic-meta-evaluation-framework-for-fine-grained-manipulation.md): The paper describes the diagnostic setup and its use for finding visual encoder bottlenecks in fine-grained manipulation.

## Latency-injection tests for asynchronous VLA control
VLA deployment teams should add delay as a controlled test variable in simulation and hardware canary runs. DEFLECT shows that asynchronous inference creates a specific runtime failure: the robot keeps executing an older action chunk while the model computes the next chunk, so the new chunk may be conditioned on stale vision and stale scene state.

The failure can be measured with a delay sweep. On Kinetix, naive asynchronous rollover drops from 89% success to under 1% when inference delay reaches seven control steps. DEFLECT trains on offline fresh-versus-stale action pairs and reports 83.3% average success over delays d=0-7, with 73.5% success for unseen high delays d=5-7. The same paper reports real-robot gains on Conveyor-II, where DEFLECT reaches 90.0% full-task success versus 83.3% for VLASH and 46.7% for pi_0.5.

A cheap adoption test is to replay existing trajectories with injected delays d=0-7, log the age of the visual observation used for each executed chunk, and track success by delay bucket. Teams using flow-matching VLA policies can then test a DEFLECT-style offline post-training step without changing the runtime inference path.

### Sources
- [DEFLECT: Delay-Robust Execution via Flow-matching Likelihood-Estimated Counterfactual Tuning for VLA Policies](../Inbox/2026-05-19--deflect-delay-robust-execution-via-flow-matching-likelihood-estimated-counterfactual-tuning-for-vla-policies.md): DEFLECT defines the asynchronous inference failure, the fresh-versus-stale offline training method, and delay-sweep results.
- [DEFLECT: Delay-Robust Execution via Flow-matching Likelihood-Estimated Counterfactual Tuning for VLA Policies](../Inbox/2026-05-19--deflect-delay-robust-execution-via-flow-matching-likelihood-estimated-counterfactual-tuning-for-vla-policies.md): The abstract states the async rollout collapse and frames DEFLECT as a drop-in offline refinement for existing async VLA stacks.
- [DEFLECT: Delay-Robust Execution via Flow-matching Likelihood-Estimated Counterfactual Tuning for VLA Policies](../Inbox/2026-05-19--deflect-delay-robust-execution-via-flow-matching-likelihood-estimated-counterfactual-tuning-for-vla-policies.md): The paper gives the real-world stale-observation mechanism, including a conveyor example where execution lags behind the conditioned observation.

## Generated 3DGS scene pipeline for UAV vision-language navigation data
Teams building aerial vision-language navigation models can test a generated-data pipeline before funding large real-flight collection. FlyMirage describes a concrete workflow: use an LLM to design scenes, generate 3D Gaussian Splatting environments, render RGB and depth views, run open-vocabulary object detection for 3D boxes, select safe navigation targets, and plan dynamically feasible UAV trajectories with EGO-Planner.

The reported scale is large enough for a pilot dataset. FlyMirage contains 500 generated 3DGS scenes and about 50,000 navigation trajectories with 6-DoF action space and kinematics. The paper reports more than 5,000 unique object labels, typical scenes with 60 to 100 object instances, and a cost of about $2 per scene with rendering on an NVIDIA RTX 4070.

A useful first check is to generate 20 to 50 scenes in the target domain, inspect object-box quality after distance pruning, and run the planner through the same safety and travel-distance constraints used in the paper. If model training improves on generated scenes but fails on a small real-flight validation set, the gap is likely in visual realism, annotation quality, or trajectory dynamics rather than dataset size alone.

### Sources
- [FlyMirage: A Fully Automated Generation Pipeline for Diverse and Scalable UAV Flight Data via Generative World Model](../Inbox/2026-05-19--flymirage-a-fully-automated-generation-pipeline-for-diverse-and-scalable-uav-flight-data-via-generative-world-model.md): FlyMirage gives the automated scene-generation, annotation, target-selection, planning, filtering, scale, and cost details.
- [FlyMirage: A Fully Automated Generation Pipeline for Diverse and Scalable UAV Flight Data via Generative World Model](../Inbox/2026-05-19--flymirage-a-fully-automated-generation-pipeline-for-diverse-and-scalable-uav-flight-data-via-generative-world-model.md): The abstract describes the full aerial VLN generation pipeline with LLM scene design, 3DGS scenes, semantic acquisition, and feasible UAV trajectories.
