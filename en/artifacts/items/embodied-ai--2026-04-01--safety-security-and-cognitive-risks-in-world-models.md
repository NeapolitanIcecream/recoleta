---
source: arxiv
url: http://arxiv.org/abs/2604.01346v2
published_at: '2026-04-01T19:57:33'
authors:
- Manoj Parmar
topics:
- world-models
- ai-safety
- adversarial-robustness
- threat-modeling
- alignment
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# Safety, Security, and Cognitive Risks in World Models

## Summary
This paper surveys safety, security, and human-trust risks in world models and adds a threat model plus proof-of-concept attack metrics. Its main claim is that world models create failure modes that persist across imagined rollouts, so they need stronger evaluation and controls in safety-critical systems.

## Problem
- The paper studies risks that arise when world models predict future states for planning in robotics, driving, and agentic AI.
- A small input perturbation or poisoned model state can carry through many rollout steps, which can make planning fail in ways that are hard to detect.
- The authors also argue that world-model-equipped agents raise alignment risks such as goal misgeneralisation and reward hacking, and human users may over-trust model forecasts.

## Approach
- The paper is mainly a survey and threat-modeling paper, not a new world-model training method.
- It defines **trajectory persistence** with an amplification ratio $\mathcal{A}_k$ that compares how much an attack grows inside a recurrent world model versus a single-step encoder.
- It defines **representational risk** $\mathcal{R}(\theta,\mathcal{D})$ as the gap between true environment dynamics and learned dynamics on a deployment distribution, with practical proxies such as ensemble disagreement and latent OOD scores.
- It builds a five-profile attacker taxonomy: white-box, grey-box, black-box, insider, and supply-chain, and maps threats onto world-model system layers and existing security references such as MITRE ATLAS and the OWASP LLM Top 10.
- It includes proof-of-concept experiments on GRU/RSSM-style models and checkpoint probing on DreamerV3 to test whether adversarial effects persist through rollouts.

## Results
- The paper reports a **trajectory-persistent adversarial attack** on a **GRU-based RSSM** with **$\mathcal{A}_1 = 2.26\times$**, meaning the attack error at step 1 is more than twice the single-step baseline.
- Under **adversarial fine-tuning**, the reported attack effect is reduced by **59.5%** on the GRU-based setup.
- In a **stochastic RSSM proxy**, the reported amplification drops to **$\mathcal{A}_1 = 0.65\times$**, which the authors use to argue that vulnerability depends on architecture.
- For a **real DreamerV3 checkpoint**, the paper reports **non-zero action drift** from checkpoint-level probing, but the excerpt gives no full end-to-end task metric, benchmark score, or failure-rate number.
- The paper cites prior context rather than new task performance gains, including **DreamerV3 on 150+ tasks** and a prior driving attack result with **up to 67% attack success rate**, but these are background references, not the paper's own headline experiment.
- The authors state that their empirical results are **proof of concept** on proxy models, and that claims about deployed large-scale systems rely on theory and literature synthesis rather than full system measurements.

## Link
- [http://arxiv.org/abs/2604.01346v2](http://arxiv.org/abs/2604.01346v2)
