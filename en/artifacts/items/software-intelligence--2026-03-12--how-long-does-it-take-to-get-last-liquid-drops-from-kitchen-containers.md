---
source: hn
url: https://www.brown.edu/news/2026-03-04/kitchen-fluid-dynamics
published_at: '2026-03-12T22:51:04'
authors:
- hhs
topics:
- fluid-dynamics
- thin-film-flow
- navier-stokes
- kitchen-physics
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# How long does it take to get last liquid drops from kitchen containers?

## Summary
This study uses the physics model of thin liquid film flow to answer an everyday but common question: after tilting a container, how long does it take for those last drops of liquid to finally run out? By combining the Navier-Stokes equations with simple experiments, the authors estimated draining times for liquids of different viscosities in kitchen scenarios.

## Problem
- The study aims to solve: how long it takes for a **thin liquid film** on the surface of a tilted container to drain most of its liquid, and when the residual water film after washing a pan will gather enough to be poured off again.
- This question matters because thin liquid film flow appears not only in the kitchen, but also widely in biophysics and surface-fluid research, making it a real-world example of a broader fluid mechanics problem.
- The difficulty is that drainage time changes significantly with liquid viscosity, so it is hard to judge the waiting time accurately by intuition alone.

## Approach
- The core method uses the **viscous-regime approximation of the Navier-Stokes equations** to describe the slow gravity-driven flow of a thin liquid film on an inclined surface.
- The authors simplified the problem to “liquid flowing on a surface tilted at 45°,” and used that to predict how long liquids of different viscosities would take to reach a given drainage fraction.
- They conducted corresponding experiments: letting liquid flow down a plate inclined at 45° and using weighing to determine when **90%** of the liquid had been drained (decanted).
- For the washed iron pan/wok question, the authors further performed computer simulations to estimate the optimal waiting time for the residual water film to gather at the bottom and become suitable for pouring off again.

## Results
- The experiments and theoretical calculations were **generally consistent**, showing that this thin liquid film flow model can predict kitchen-container drainage waiting times fairly well.
- At a **45° tilt angle**, a lower-viscosity liquid like milk takes about **30 seconds** to drain **90%** of the liquid in the thin film.
- For more viscous liquids, such as olive oil, reaching a **90% recovery rate** takes **more than 9 minutes**.
- Water reaches **90% decanting** in just **a few seconds**.
- Cold maple syrup may require **several hours** to reach the same **90%** drainage level.
- For the residual water film after washing a pan, the simulation gave an optimal waiting time of about **15 minutes** before pouring again; the researchers had previously typically waited only **1–2 minutes**.

## Link
- [https://www.brown.edu/news/2026-03-04/kitchen-fluid-dynamics](https://www.brown.edu/news/2026-03-04/kitchen-fluid-dynamics)
