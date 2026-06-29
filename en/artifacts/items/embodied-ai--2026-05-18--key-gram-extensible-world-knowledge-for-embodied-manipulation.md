---
source: arxiv
url: https://arxiv.org/abs/2605.18556v1
published_at: '2026-05-18T15:37:02'
authors:
- Jingjing Fan
- Siyuan Li
- Botao Ren
- Zhidong Deng
topics:
- vision-language-action
- robot-manipulation
- external-memory
- compositional-grounding
- world-knowledge
- real-world-robotics
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Key-Gram: Extensible World Knowledge for Embodied Manipulation

## Summary
Key-Gram adds an external language-memory module to VLA robot policies so reusable task knowledge can be retrieved by instruction phrases and injected into visual reasoning layers. It reports consistent success-rate gains on RoboTwin2.0, LIBERO-Plus, and real dual-arm manipulation.

## Problem
- VLA and world-action models often mix instruction knowledge and visual state reasoning in the same backbone, which can weaken instruction grounding in compositional manipulation.
- Updating the backbone to learn new objects, relations, or tasks can overwrite earlier knowledge, which matters for robots that must adapt after deployment.

## Approach
- A parser splits each instruction into a fixed set of short key-grams, such as object relations, task goals, and subgoals.
- Each key-gram is mapped through deterministic multi-head hashing to rows in an external embedding table, giving O(1) lookup by instruction-derived keys.
- Retrieved memory vectors are projected into selected Transformer layers, then a token-wise gate decides which visual tokens receive the retrieved language prior.
- A lightweight long-span convolution mixes the retrieved key-gram information before adding it as a residual update to the hidden states.
- The same memory-guided backbone feeds a future-vision latent head and a flow-matching action expert for trajectory prediction.

## Results
- On RoboTwin2.0 50-task averages, pi0-KG improved easy success from 65.9% to 80.3% (+21.9%) and hard success from 58.4% to 75.6% (+29.5%); pi0.5-KG improved easy from 82.7% to 89.0% (+7.6%) and hard from 76.8% to 84.4% (+9.9%).
- On LIBERO-Plus transfer from LIBERO without target-domain fine-tuning, pi0-KG improved 53.6% to 72.8% (+35.8%), and pi0.5-KG improved 83.9% to 87.7% (+4.5%).
- After LIBERO-Plus fine-tuning, pi0-KG reached 88.5% versus 84.0% for pi0 (+5.4%), and pi0.5-KG reached 92.6% versus 90.4% for pi0.5 (+2.4%).
- On real-world long-horizon dual-arm tasks, pi0-KG improved average success from 69.3% to 80.0% (+15.4%), and pi0.5-KG improved 82.0% to 88.7% (+8.1%).
- On real-world expansion tasks, pi0-KG improved average success from 72.4% to 81.6% (+12.7%), with unseen pairing gains of +34.6% and +41.7%; pi0.5-KG improved 80.0% to 86.8% (+8.5%), with unseen pairing gains of +18.8% and +21.2%.

## Link
- [https://arxiv.org/abs/2605.18556v1](https://arxiv.org/abs/2605.18556v1)
