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
- world-model
- multi-agent-video-generation
- shared-world-modeling
- video-diffusion
- carla-simulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# ShareVerse: Multi-Agent Consistent Video Generation for Shared World Modeling

## Summary
ShareVerse proposes a video generation framework for multi-agent shared world modeling, allowing multiple independent agents to generate the same world consistently from their own perspectives. It combines a new dataset built with CARLA, four-view concatenation, and cross-agent attention to achieve both multi-view geometric consistency and cross-agent world consistency at the video level.

## Problem
- Existing video world models mostly handle only **single-agent/single-view** settings, making it difficult to ensure that multiple agents generate **the same shared physical world**.
- Multi-agent scenarios require satisfying both **multi-view geometric consistency within each agent** and **content consistency across different agents in overlapping regions, while also making reasonable inferences in non-overlapping regions**.
- This is important because shared world modeling is a foundational capability for systems such as **multi-robot collaboration, multiplayer games, and drone swarms**, yet current public datasets and methods are insufficient to support this task.

## Approach
- Build a large-scale synchronized two-agent dataset based on CARLA: each agent has four cameras (front/rear/left/right), covering multiple scenes, weather conditions, and six types of interaction trajectories, yielding **55,000 video pairs** in total, with long videos split into **49-frame** training clips.
- Perform **spatial concatenation** on the four video streams of each agent, effectively allowing the model to see the agent’s 360° environment at once, making it easier to maintain internal multi-view geometric consistency for that agent.
- Convert camera intrinsics and poses into **raymap embeddings** and use them as camera-trajectory conditioning inputs to the video diffusion model, so generation is controlled by camera motion rather than relying only on the first frame.
- Add **cross-agent attention** to the pretrained CogVideoX: concatenate the video features of the two agents and perform attention-based interaction so they can exchange spatiotemporal and positional information, thereby maintaining consistency in overlapping regions and generating reasonably in non-overlapping regions based on historical information.
- The overall model supports video generation at **49 frames, 480×720** resolution and is trained on top of **CogVideoX-5B-I2V**.

## Results
- On the authors’ validation set of unseen scenes, the method achieves **PSNR 20.76**, **SSIM 0.6656**, and **LPIPS 0.2791**, used to evaluate consistency with paired ground-truth frames and reconstruction quality.
- On **VBench**, the reported generation quality metrics are **Aesthetic 0.4480**, **Imaging 0.6468**, **Temporal Flickering 0.9490**, **Motion Smoothness 0.9745**, **Subject Consistency 0.8913**, and **Background Consistency 0.9312**.
- The paper does not provide a direct numerical comparison table against existing public baseline methods; the stronger concrete claim is that its method can simultaneously maintain **internal consistency across four views for a single agent** and **cross-agent scene consistency** in a **two-agent shared world**.
- Qualitative results claim that the model can accurately perceive the dynamic positions of other agents; when changing another agent’s trajectory or modifying map buildings, the generated results change accordingly, indicating cross-agent information sharing.
- The ablation study concludes that **four-view training outperforms single-view**, **raymap is better than directly using raw camera parameters**, and **cross-agent attention is crucial for interactive generation**, though the excerpted abstract does not provide the corresponding ablation numbers.

## Link
- [http://arxiv.org/abs/2603.02697v1](http://arxiv.org/abs/2603.02697v1)
