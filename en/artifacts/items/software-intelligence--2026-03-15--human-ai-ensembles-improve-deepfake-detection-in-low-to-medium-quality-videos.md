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
- distribution-shift
- video-forensics
- benchmarking
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Human-AI Ensembles Improve Deepfake Detection in Low-to-Medium Quality Videos

## Summary
This paper compares the performance of humans and a large set of deepfake detectors under realistic conditions, finding that humans clearly outperform AI on low-to-medium quality videos. The authors further show that humans and AI make different types of mistakes, so combining them into an ensemble system can significantly improve robustness and eliminate high-confidence catastrophic errors.

## Problem
- Existing deepfake detection is usually treated as a purely machine learning problem, but standard benchmarks mostly use high-quality, frontal-face videos captured under ideal conditions, which do not represent everyday real-world scenarios recorded on mobile phones.
- In practice, if detectors fail on low/medium-quality videos with occlusion, motion, zoom, or small faces, this would directly affect judicial processes, public-event forensics, and digital trust, making the problem highly important.
- The field lacks large-scale, head-to-head comparisons between humans and AI detectors under the same conditions, and it is also unclear whether the two can complement each other.

## Approach
- The authors evaluated **200 human participants** and **95 state-of-the-art AI detectors**, comparing performance on two datasets: the standard benchmark **DF40** and **CharadesDF**, a newly created dataset that is more representative of everyday mobile-phone videos.
- **CharadesDF** contains **1,000 videos** (500 real, 500 fake), recorded by participants at home using personal devices while performing everyday activities, then manipulated into deepfakes using public face-swapping tools; the DF40 test set also contains **1,000 videos** (500 real, 500 fake, 10 manipulation techniques).
- On the AI side, the authors trained **32 architectures**, producing **96 variants** based on **FaceForensics++**, **CelebDF-v2**, and the **DF40 training set**; one was excluded for compatibility reasons, leaving 95 detectors for comparison.
- On the human side, **100 people** were recruited for each dataset; each person watched **60 videos** selected at random and provided a 5-point confidence rating. The authors converted these ratings into probabilities and then computed accuracy, F1, and AUC.
- To test complementarity, the authors built a **quality-weighted ensemble**: they performed leave-one-out weighted aggregation within the “human group” and the “AI group” separately, then averaged the two group outputs equally to form a **hybrid human-AI ensemble**.

## Results
- On **DF40**, mean human accuracy was **0.743**, significantly higher than AI at **0.610** (t(193)=**6.970**, p<**.001**, d=**0.999**). On the more realistic **CharadesDF**, humans achieved **0.784**, while AI dropped to near-random performance at **0.537** (t(193)=**17.389**, p<**.001**, d=**2.491**).
- Ensembles significantly outperformed individuals: the human ensemble reached accuracies of **0.890/0.928** on **DF40/CharadesDF**, improving over individual humans by **+14.7/+14.4** percentage points; the AI ensemble reached **0.869** on **DF40** (**+25.8** percentage points over individual AI), but only **0.607** on **CharadesDF** (**+7.0** percentage points), showing that AI is more fragile under domain shift.
- The strongest model was the **hybrid ensemble**: on **DF40** it achieved accuracy **0.941**, F1 **0.941**, and AUC **0.988**; on **CharadesDF** it achieved accuracy **0.924**, F1 **0.924**, and AUC **0.979**, outperforming either the human-only or AI-only ensemble overall.
- For the high-confidence catastrophic error rate (CFR), individual humans scored **19.0%/17.1%**, and individual AI scored **27.9%/31.7%**; the human ensemble reduced this to **1.9%/1.0%**, the AI ensemble reduced it to **0.1%/0.9%**, and the **hybrid ensemble achieved CFR = 0.000 on both datasets**.
- Human and AI errors were nearly independent: catastrophic-failure overlap was **0**, and the phi coefficients on **DF40/CharadesDF** were **-0.004/-0.010**, respectively. Humans were more likely to classify high-quality deepfakes as real, while AI was more likely to falsely flag authentic videos as fake, which is the core reason the hybrid ensemble is effective.
- The paper also claims that among visual quality factors, **face size/visibility** is the most consistently important factor; AI is more affected than humans by low-level visual quality and distribution shift, while most demographic variables have limited predictive power for human detection ability.

## Link
- [http://arxiv.org/abs/2603.14658v1](http://arxiv.org/abs/2603.14658v1)
