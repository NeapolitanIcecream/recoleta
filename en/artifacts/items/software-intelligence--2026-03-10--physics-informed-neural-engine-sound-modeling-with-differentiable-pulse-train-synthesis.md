---
source: arxiv
url: http://arxiv.org/abs/2603.09391v1
published_at: '2026-03-10T09:03:35'
authors:
- Robin Doerfler
- Lonce Wyse
topics:
- neural-audio-synthesis
- physics-informed-learning
- differentiable-dsp
- engine-sound-modeling
- karplus-strong
relevance_score: 0.14
run_id: materialize-outputs
language_code: en
---

# Physics-Informed Neural Engine Sound Modeling with Differentiable Pulse-Train Synthesis

## Summary
This paper proposes the PTR (Pulse-Train-Resonator) model, which directly synthesizes the “pulse-based origin” of engine sound in a differentiable, physics-prior-driven way rather than only fitting the spectral result. Compared with the harmonic-plus-noise baseline, it achieves better reconstruction quality on three engine data subsets while also providing interpretable physical parameters.

## Problem
- Existing neural engine sound synthesis methods mostly fit the **heard spectrum** rather than modeling the true physical source of the sound: discrete exhaust pressure pulses occurring according to the firing order.
- Engine sounds have characteristics such as low fundamental frequency, strong nonstationarity, millisecond-scale transients, and acceleration/deceleration direction dependence, making traditional harmonic/noise modeling difficult to handle both timing precision and timbral evolution at the same time.
- This matters because models that better match the physical mechanism may not only improve reconstruction quality, but also produce interpretable control parameters corresponding to mechanical phenomena, which is useful for synthesis and analysis.

## Approach
- Proposes an end-to-end differentiable **PTR** architecture: RPM, torque, and their first- and second-order differences are used as inputs; pulse and noise parameters are first decoded, and then waveforms are synthesized at the audio rate.
- Uses a **parameterized pulse train** instead of direct harmonic modeling: each cylinder generates bipolar pressure pulses according to the firing rhythm, with physics priors such as harmonic decay, valve/pressure-release envelopes, and thermodynamic phase modulation.
- Uses explicit gating to model operating conditions: throttle-related combustion noise is activated under positive torque, while airflow noise under deceleration fuel cutoff (DFCO) is activated under negative torque, rather than relying entirely on the network to learn this implicitly.
- Sends multi-cylinder pulses into a **differentiable Karplus-Strong resonator** to simulate the exhaust system; by rewriting recursive feedback into an optimizable all-pole form and using Gumbel-Softmax to learn discrete delays, gradient-based training becomes possible.
- During training, combines multiresolution STFT loss with a harmonic loss based on engine-order harmonic trajectories to constrain both the overall spectrum and the speed-synchronized harmonic structure.

## Results
- Validated on 3 subsets (A/B/C) of the Procedural Engine Sounds Dataset, with a total duration of about **7.5 hours**, about **2.5 hours** per subset, using a 90/10 train/validation split.
- Compared with the structurally identical **HPN baseline**, PTR reduces average **harmonic loss** from **0.111** to **0.088**, which the paper describes as a **21% improvement in harmonic reconstruction**.
- Average **STFT loss** decreases from **1.899** to **1.807**; average **total loss** decreases from **1.006** to **0.949**, i.e. a **5.7%** reduction.
- Total loss by dataset: A from **0.944 → 0.872** (about **7.6%** improvement), B from **0.943 → 0.907** (about **3.8%**), C from **1.132 → 1.069** (about **5.6%**).
- The paper also claims that the model can produce more realistic perceptual behavior, such as RPM-dependent harmonic structure, transitions caused by gear shifting/clutch events, and different noise characteristics for throttle and DFCO, but this part is mainly qualitative description and does not provide numerical subjective listening scores.
- It additionally claims that even though the architecture includes a V8 firing-order prior, it can still generalize to the inline-four characteristics of dataset A, showing a certain degree of robustness.

## Link
- [http://arxiv.org/abs/2603.09391v1](http://arxiv.org/abs/2603.09391v1)
