---
source: arxiv
url: https://arxiv.org/abs/2605.26379v1
published_at: '2026-05-25T22:56:26'
authors:
- David Klindt
- Yann LeCun
- Randall Balestriero
topics:
- world-models
- jepa
- linear-identifiability
- self-supervised-learning
- latent-planning
- robot-control
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# When Does LeJEPA Learn a World Model?

## Summary
This paper gives conditions under which LeJEPA learns a linear world model: with Gaussian latent variables and stationary additive-noise positive pairs, the optimum recovers the latents up to an orthogonal transform.

## Problem
- Nonlinear observations can hide the latent state needed for planning and compositional generalization.
- Existing JEPA work did not prove when the learned embedding recovers true latent variables, so linear probes and latent planning lacked an identifiability guarantee.
- The paper asks which latent distributions make LeJEPA linearly identifiable under independent stationary additive-noise transitions.

## Approach
- Model observations as `x = g(z)`, where `g` can be nonlinear, and train `h = f ∘ g` with LeJEPA alignment `E||h(z') - h(z)||²` plus Gaussian regularization `h(z) ~ N(0, I_n)`.
- For Gaussian latents, use the Ornstein-Uhlenbeck positive-pair transition `z' = ρz + sqrt(1 - ρ²)η`, with `η ~ N(0, I_n)`.
- Decompose learned functions into Hermite polynomial degrees. A degree-`d` term has correlation `ρ^d`, so nonlinear terms lose correlation compared with the linear degree-1 term.
- Use Sturm-Liouville analysis for the converse: under additive noise, requiring the first eigenfunction to be affine forces the latent density to be Gaussian.
- Connect orthogonal latent recovery to planning by showing that optimal finite-horizon control is preserved when costs are invariant under orthogonal transforms.

## Results
- Theorem 5.1: in the Gaussian world, any measurable `h` with `h(z) ~ N(0, I_n)` has loss `L(h) ≥ 2(1 - ρ)n`; equality holds exactly when `h(z) = Qz` for some orthogonal `Q ∈ O(n)`.
- At the optimum, the learned transition has the same form in representation space: `h(z') | h(z) ~ N(ρh(z), (1 - ρ²)I_n)`.
- Theorem 5.2: within independent, stationary, additive-noise worlds, Gaussian latents are the unique case where every whitened LeJEPA minimizer is linear.
- Theorem 5.3: approximate recovery is bounded by `E||h(z) - Qz||² ≤ D + (ε + D)²`, where `D = δ / (2ρ(1 - ρ))`, `δ` is alignment slack, and `ε` is whitening error.
- Theorem 5.4: if `h(z)=Qz`, latent-space planning gives the same optimal value and action sequence as planning in the true latent state for `O(n)`-invariant costs.
- The supplied excerpt claims experiments on 2D nonlinear mixings, distributional ablations, 1024-dimensional latents, approximate-bound tests, and pixel-based robotic control, but it does not include task-score tables or empirical metric values.

## Link
- [https://arxiv.org/abs/2605.26379v1](https://arxiv.org/abs/2605.26379v1)
