---
kind: ideas
granularity: day
period_start: '2026-04-09T00:00:00'
period_end: '2026-04-10T00:00:00'
run_id: 7d23cbbb-ba31-43ac-9d69-5819be62634e
status: succeeded
topics:
- embodied-ai
- world-models
- humanoid-control
- navigation
- dexterous-manipulation
- articulation
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/world-models
- topic/humanoid-control
- topic/navigation
- topic/dexterous-manipulation
- topic/articulation
language_code: en
pass_output_id: 45
pass_kind: trend_ideas
upstream_pass_output_id: 44
upstream_pass_kind: trend_synthesis
---

# Embodied World Models

## Summary
The clearest near-term build is a training pipeline that uses generated futures to write navigation labels offline, then deploys a small student model alone. A second concrete change is to treat robot body structure as explicit input to control models so related machines can share one learned model with less warm-up and retraining. A third practical test is a perception stage for articulated objects that estimates joints from one image before a manipulation stack selects contacts and force.

## Training-time pseudo-label generation for single-image vision-language navigation
Build a teacher-only training pipeline for single-image navigation datasets. WorldMAP gives the clearest evidence in this pack that generated future views are useful when they are converted into path supervision before deployment, not when they are kept in the runtime loop. The concrete workflow is a pseudo-label generator that takes one egocentric image plus an instruction, expands future views with a world model, projects target and obstacle regions into a bird's-eye-view cost map, and writes waypoint labels for a smaller student model. Teams shipping indoor navigation on edge hardware would care first because this keeps inference cheap: the student runs alone at test time. The cheap validation is straightforward: add the pseudo-label stage to an existing waypoint predictor and compare ADE and FDE against direct VLM prediction on held-out scenes. The result to beat is concrete. On Target-Bench, WorldMAP reports ADE 42.06 and FDE 38.87, beating Gemini-3-Pro on both and far outperforming direct Qwen3-VL-8B trajectory prediction.

### Evidence
- [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](../Inbox/2026-04-09--worldmap-bootstrapping-vision-language-navigation-trajectory-prediction-with-generative-world-models.md): Provides the teacher-student design, the training-only use of generated futures, and the concrete ADE/FDE numbers.
- [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](../Inbox/2026-04-09--worldmap-bootstrapping-vision-language-navigation-trajectory-prediction-with-generative-world-models.md): Confirms the reported 18.0% ADE and 42.1% FDE improvements over the best competing baseline.

## Morphology-conditioned state adapters for robot fleet transfer
Add a morphology adapter layer that reads robot body parameters from the USD file and feeds them into the world model or policy at every step. QWM and HEX both point to the same operational problem: control systems break when the body changes and the model has to infer static morphology from a few early motions. A practical build is a shared canonical body description service for a robot fleet, with one encoder for static body features and one mapping into fixed body-part slots for policies that need whole-body control. The first users are teams running related quadrupeds or humanoids across hardware revisions, where warm-up time, retraining cost, and unsafe early behavior slow deployment. A cheap check is to hold out one robot variant, train on the rest, and measure whether the held-out machine can start with stable behavior immediately. The current evidence supports this most clearly inside bounded robot families: QWM claims zero-shot deployment on unseen quadrupeds within the trained morphology range, and HEX reports cross-embodiment whole-body manipulation on two humanoid platforms with shared body-part state encoding and short-horizon future proprioception.

### Evidence
- [Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning](../Inbox/2026-04-09--toward-hardware-agnostic-quadrupedal-world-models-via-morphology-conditioning.md): Describes explicit morphology conditioning from USD features, the deployment goal of zero-shot transfer, and the bounded-family limitation.
- [HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation](../Inbox/2026-04-09--hex-humanoid-aligned-experts-for-cross-embodiment-whole-body-manipulation.md): Shows the same design pattern for humanoids through canonical body-part slots and future proprioception prediction across embodiments.

## Single-image articulation estimation before dexterous manipulation
Build an articulated-object preprocessor that turns a single scene image into executable joint hypotheses before planning a grasp or opening action. DailyArt makes that step more practical by estimating joint type, axis, pivot, and motion range from one closed-state image after synthesizing an opened view of the same object. BLaDA points to the missing downstream link: dexterous execution still needs object-part contact regions and task-specific constraints such as handle, knob, press, and open. Put together, this supports a workflow where a perception stage first proposes kinematic structure for cabinets, appliances, and tools, then a manipulation stack uses those joints to choose contact regions, wrist pose, and force settings. The first users are manipulation teams dealing with unfamiliar articulated objects in homes, labs, or warehouse backrooms where CAD assets and manual part annotations are rarely available. The cheap check is a narrow benchmark on doors, drawers, and lids: measure whether single-image joint proposals improve open-task success or reduce search motions compared with object-agnostic grasping. The evidence is less complete here because the available excerpts do not include final benchmark tables, but the interface is concrete enough to test.

### Evidence
- [DailyArt: Discovering Articulation from Single Static Images via Latent Dynamics](../Inbox/2026-04-09--dailyart-discovering-articulation-from-single-static-images-via-latent-dynamics.md): Provides the single-image articulation pipeline and the predicted outputs needed for downstream control: joint type, axis, pivot, and motion range.
- [BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields](../Inbox/2026-04-09--blada-bridging-language-to-functional-dexterous-actions-within-3dgs-fields.md): Provides the downstream dexterous execution interface from language and 3D contact regions to wrist pose, finger commands, and force settings.
