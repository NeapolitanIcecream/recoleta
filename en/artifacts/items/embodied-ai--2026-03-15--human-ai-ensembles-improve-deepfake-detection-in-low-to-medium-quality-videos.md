---
source: arxiv
url: http://arxiv.org/abs/2603.14658v1
published_at: '2026-03-15T23:25:34'
authors:
- Marco Postiglione
- Isabel Gortner
- V. S. Subrahmanian
topics:
- deepfake-detection
- human-ai-ensemble
- benchmarking
- domain-shift
- video-forensics
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Human-AI Ensembles Improve Deepfake Detection in Low-to-Medium Quality Videos

## Summary
This paper systematically compares the real-world performance of humans and AI in deepfake video detection, finding that humans clearly outperform existing AI detectors in low- to medium-quality settings. The study also shows that human–AI ensembles can substantially reduce high-confidence misclassifications, indicating that real-world applications are better suited to collaborative detection rather than relying on algorithms alone.

## Problem
- Existing deepfake detection is mostly evaluated using machine learning benchmarks, but standard datasets often favor high-quality, front-facing, well-lit videos and are difficult to treat as representative of real user-generated content captured on mobile phones.
- The field lacks large-scale, direct comparisons between humans and multiple state-of-the-art AI detectors across different video conditions, so it remains unclear which is more reliable under real-world conditions.
- This matters because videos in judicial, journalistic, and public-event contexts are often of only moderate quality; if detectors fail in these scenarios, digital trust and accountability are directly affected.

## Approach
- The authors evaluated **200 human participants** and **95 state-of-the-art AI detectors**, comparing them on two test sets: the standard benchmark **DF40** and **CharadesDF**, a newly constructed dataset intended to better reflect real mobile-phone home-recording scenarios.
- On the AI side, they used **32 architectures**, trained on **FaceForensics++、CelebDF-v2、DF40 training set** respectively, forming **96 variants**; one was excluded due to architectural incompatibility, leaving 95 detectors in the final evaluation.
- The new dataset **CharadesDF** contains **1,000 videos** (500 real, 500 fake), covering more realistic conditions such as everyday activities, camera motion, occlusion, smaller faces, and lower visual quality.
- Human participants provided real/fake judgments and 5-point confidence ratings for videos; the study also analyzed accuracy, AUC, F1, and the “catastrophic failure rate” (CFR), defined as the proportion of severe errors made with high confidence.
- To test complementarity, the authors built **quality-weighted voting** human ensembles, AI ensembles, and a **hybrid ensemble** that first aggregates the human and AI groups separately and then combines them with equal weights.

## Results
- **Humans significantly outperform AI.** On **DF40**, mean human accuracy was **0.743**, versus **0.610** for AI (t=6.970, p<.001, d=0.999); on **CharadesDF**, humans reached **0.784**, while AI dropped to near chance at **0.537** (t=17.389, p<.001, d=2.491).
- **Ensembling significantly improves performance.** Human ensembles reached **0.890 / 0.928** on DF40 / CharadesDF; AI ensembles reached **0.869 / 0.607**; hybrid ensembles performed best at **0.941 / 0.924**, with corresponding AUC values of **0.988 / 0.979**.
- **High-confidence misclassifications drop sharply.** Individual humans had CFRs of **19.0% / 17.1%**, while individual AI had **27.9% / 31.7%**; human ensembles reduced this to **1.9% / 1.0%**, AI ensembles to **0.1% / 0.9%**, and the **hybrid ensemble achieved CFR = 0.000** on both datasets.
- **Human and AI error patterns are complementary and nearly independent.** Catastrophic failure overlap was zero; failure correlation φ was **-0.004 / -0.010** on DF40 / CharadesDF respectively, with Fisher tests showing **p=1.000** in both cases.
- **The error types differ.** When only humans made severe errors, they usually classified deepfakes as real: **14/19 (74%)** in DF40 and **8/8 (100%)** in CharadesDF; when only AI made severe errors, it usually classified real videos as fake: **1/1 (100%)** in DF40 and **7/7 (100%)** in CharadesDF.
- **Out-of-domain real-world conditions are more damaging for AI.** Relative to individual models, AI ensembles improved by **+25.8 percentage points** on DF40, but only **+7.0 percentage points** on CharadesDF; based on this, the authors argue that current AI deepfake detection is highly fragile to distribution shift in real low-/medium-quality videos.

## Link
- [http://arxiv.org/abs/2603.14658v1](http://arxiv.org/abs/2603.14658v1)
