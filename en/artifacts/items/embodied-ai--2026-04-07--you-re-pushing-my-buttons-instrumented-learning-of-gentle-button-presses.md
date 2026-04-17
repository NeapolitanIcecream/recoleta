---
source: arxiv
url: http://arxiv.org/abs/2604.05954v1
published_at: '2026-04-07T14:46:55'
authors:
- Raman Talwar
- Remko Proesmans
- Thomas Lips
- Andreas Verleysen
- Francis wyffels
topics:
- contact-rich-manipulation
- imitation-learning
- audio-conditioned-policy
- training-time-instrumentation
- button-pressing
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# You're Pushing My Buttons: Instrumented Learning of Gentle Button Presses

## Summary
This paper tests whether a robot can use extra sensors during training to learn gentler contact behavior without needing those sensors at deployment. On a button-pressing task, instrumented audio supervision lowers contact force but does not raise success rate.

## Problem
- Contact-rich manipulation is hard to learn from camera input and proprioception because the key contact event is only partly visible.
- For button pressing, success alone is not enough; the robot should press with low force to avoid harsh interaction.
- The paper asks whether training-time instrumentation can improve policy quality without making inference depend on the instrumented object.

## Approach
- The setup uses a UR3e arm, wrist RGB camera, fingertip microphone, wrist force-torque sensor, and a button with a binary pressed/unpressed signal available only during training.
- The authors collect demonstrations automatically: the robot approaches from randomized start poses, detects the press event from the instrumented button signal, and retracts.
- They fine-tune an Audio Spectrogram Transformer pretrained on AudioSet into a binary click detector using the privileged button-state labels; this detector reaches **F1 = 0.988** with **1.2% false negatives** on validation.
- They train Diffusion Policy with vision and audio using three integration choices: Deep Fusion with fine-tuned AST embeddings, Deep Fusion with fine-tuned AST logits, and Soft Sensor, which trains on true button state and swaps in AST predictions at test time.
- They compare these against a baseline that uses a generic AudioSet-pretrained AST without task-specific fine-tuning.

## Results
- The click detector works well as a training signal source: **F1 = 0.988** and **1.2% false negatives** on validation.
- Task success rates are close across all policies: **45% to 55%** over **40 rollouts per model**, with overlapping **Bayesian 95% credible intervals**.
- Expert demonstrations have median peak vertical force **3.41 N** during successful rollouts.
- The generic audio baseline is harsher at **6.98 N** median peak force; Deep Fusion reduces this to **5.87 N** with fine-tuned embeddings and **5.95 N** with fine-tuned classifier outputs.
- Soft Sensor performs worst on force at **9.37 N**, which the authors attribute to train-test mismatch and up to **50 ms** latency from spectrogram creation.
- Wasserstein distance to the expert force distribution follows the same pattern: **5.0 N** for Soft Sensor, **4.6 N** for generic AST, **2.8 N** for Deep Fusion with fine-tuned classifier, and **2.5 N** for Deep Fusion with fine-tuned embeddings, the closest to expert behavior.

## Link
- [http://arxiv.org/abs/2604.05954v1](http://arxiv.org/abs/2604.05954v1)
