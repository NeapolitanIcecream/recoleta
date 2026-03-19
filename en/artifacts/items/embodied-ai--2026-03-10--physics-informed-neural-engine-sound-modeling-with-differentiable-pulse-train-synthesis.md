---
source: arxiv
url: http://arxiv.org/abs/2603.09391v1
published_at: '2026-03-10T09:03:35'
authors:
- Robin Doerfler
- Lonce Wyse
topics:
- neural-audio-synthesis
- physics-informed-modeling
- differentiable-dsp
- engine-sound-synthesis
- karplus-strong
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Physics-Informed Neural Engine Sound Modeling with Differentiable Pulse-Train Synthesis

## Summary
This paper proposes PTR, a physics-informed neural architecture for engine sound synthesis that no longer only fits spectral outcomes, but directly models combustion pulse trains and their propagation through the exhaust system. It combines differentiable pulse generation with differentiable resonators, improving reconstruction quality while providing more interpretable physical parameters.

## Problem
- Existing neural engine-audio methods mostly fit the **heard harmonic spectrum**, rather than modeling the true cause: discrete exhaust pressure pulses occurring according to the firing order.
- Engine sounds simultaneously exhibit characteristics such as **low fundamental frequency, strong non-stationarity, rapid transients, and acceleration/deceleration direction dependence**, making traditional harmonic-plus-noise or general music-audio modeling assumptions a poor fit.
- This matters because models that better reflect the physical mechanism may achieve **better reconstruction, cross-condition generalization, and parameter interpretability**, which is useful for sound synthesis and interactive engine-audio applications.

## Approach
- Proposes **Pulse-Train-Resonator (PTR)**: RPM, torque, and their first/second-order differences are input and decoded by a neural network into pulse and noise parameters, then audio is synthesized directly in the time domain.
- Uses **pulse trains aligned with the firing cycle** to represent each cylinder’s exhaust events, and incorporates physically inspired pulse-shape components: harmonic decay, pressure-release envelopes, thermodynamic phase modulation, per-cylinder gain, and timing offsets.
- Uses **throttle/deceleration fuel cutoff (DFCO) gating** based on the sign of torque to control different noise sources, making noise behavior under propulsion and deceleration conditions more physically consistent.
- Uses **differentiable Karplus-Strong resonators** to simulate exhaust-system acoustics; the authors rewrite recursive delayed feedback into an all-pole form suitable for gradient optimization, and use Gumbel-Softmax to learn discrete delay lengths.
- During training, combines **multi-resolution STFT loss** with **harmonic loss** computed along engine-order trajectories, encouraging both overall spectral matching and RPM-synchronized harmonic structure.

## Results
- On the 3 subsets of the Procedural Engine Sounds Dataset (A/B/C, totaling **7.5 hours** of audio), PTR compared with an **HPN baseline** using the same encoder-decoder reduces the average **total validation loss from 1.006 to 0.949**, i.e. a **5.7% reduction**.
- Average **harmonic loss drops from 0.111 to 0.088**, which the authors describe as a **21% improvement in harmonic reconstruction**; average **STFT loss decreases from 1.899 to 1.807**.
- Per-dataset total loss: **A: 0.944 -> 0.872 (about 7.6%)**, **B: 0.943 -> 0.907 (about 3.8%)**, **C: 1.132 -> 1.069 (about 5.6%)**; PTR outperforms the baseline on all three engine types.
- On the hardest **Dataset C**, harmonic loss improves **0.166 -> 0.117**, indicating that directly modeling pulses rather than explicit harmonics can still better recover harmonic structure.
- Training settings include **16 kHz** audio, **100 epochs**, and about **45,000 steps**; the paper states that both models converge quickly within the first **10,000 steps**, but PTR maintains better performance afterward.
- At the perceptual level, the authors claim PTR can generate more realistic RPM-related harmonics, load-dependent noise, clutch/gearshift transitions, and DFCO acoustic behavior; however, this part is mainly qualitative and does not provide subjective listening-test numbers.

## Link
- [http://arxiv.org/abs/2603.09391v1](http://arxiv.org/abs/2603.09391v1)
