---
source: arxiv
url: http://arxiv.org/abs/2603.02697v1
published_at: '2026-03-03T07:41:12'
authors:
- Jiayi Zhu
- Jianing Zhang
- Yiying Yang
- Wei Cheng
- Xiaoyun Yuan
topics:
- multi-agent-video-generation
- shared-world-modeling
- world-models
- video-diffusion
- carla-simulation
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# ShareVerse: Multi-Agent Consistent Video Generation for Shared World Modeling

## Summary
ShareVerse proposes a video generation framework for multi-agent shared world modeling, enabling multiple independent agents to generate videos of the same world that are consistent with one another. It combines large video models, a CARLA simulation dataset, multi-view stitching, and cross-agent attention to support collaborative generation over a relatively large spatial-temporal range.

## Problem
- Existing world models and video generation methods are mostly designed for **single-agent or single-view** settings, making it difficult to ensure that multiple agents generate **the same consistent physical world**.
- Multi-agent scenarios must simultaneously satisfy: **multi-view geometric consistency within each individual agent**, as well as **world consistency across agents in overlapping regions** and reasonable completion in non-overlapping regions.
- This is important because shared world modeling is a foundational capability for applications such as **multiplayer games, multi-robot collaboration, and drone swarm systems**.

## Approach
- Builds a large-scale multi-agent interaction dataset based on **CARLA**: two agents, 4 camera views per agent (front/rear/left/right), 3 weather conditions, more than 10 scenes, and 6 types of interaction trajectories, resulting in **55,000 video pairs**.
- Applies **spatial stitching** to the 4-view videos of each agent, allowing the model to see a more complete 360° environment for that agent at once, making it easier to maintain multi-view geometric consistency within the agent.
- Converts camera intrinsics and poses into **raymap embeddings**, which are injected into the video diffusion model as trajectory/action conditions so that generation is controlled by camera motion.
- Adds **cross-agent attention** to the pretrained CogVideoX: the spatiotemporal features of the two agents are concatenated and then used for attention interaction, allowing them to exchange positional and scene information to maintain shared world consistency.
- The framework supports first-frame-conditioned generation of **49-frame** future videos, and jointly trains the base model with the newly added modules.

## Results
- On reconstruction metrics related to shared world consistency, the method achieves: **PSNR 20.76, SSIM 0.6656, LPIPS 0.2791**; the paper does not provide a numerical comparison table against specific baseline methods, so relative improvement percentages cannot be reported.
- On **VBench**, the generation quality scores are: **Aesthetic 0.4480, Imaging 0.6468, Temporal Flickering 0.9490, Motion Smoothness 0.9745, Subject Consistency 0.8913, Background Consistency 0.9312**.
- In terms of data and generation scale: the dataset contains **55,000 video pairs**; the original videos are about **250 frames**, split into **49-frame** segments for training; the generation resolution is **480×720**; the model supports **49-frame large-scale video generation**.
- The qualitative results claim that the model can simultaneously maintain **internal consistency across an individual agent’s four views** and **shared world consistency between two agents**, while also perceiving and generating the dynamic positions of other agents relatively accurately.
- Ablation experiments claim that **four-view training outperforms single-view**, **raymap is better than directly using raw camera values**, and **cross-agent attention is crucial for interactive generation**; however, the excerpt does not provide the specific numbers for these ablations.

## Link
- [http://arxiv.org/abs/2603.02697v1](http://arxiv.org/abs/2603.02697v1)
