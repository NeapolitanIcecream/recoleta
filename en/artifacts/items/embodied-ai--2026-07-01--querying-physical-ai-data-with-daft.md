---
source: hn
url: https://www.eventual.ai/blog/egodex-scenario-search
published_at: '2026-07-01T22:45:06'
authors:
- DISCURSIVE
topics:
- robot-data-scaling
- dexterous-manipulation
- multimodal-search
- egocentric-video
- hand-pose-geometry
relevance_score: 0.7
run_id: materialize-outputs
language_code: en
---

# Querying Physical AI Data with Daft

## Summary
Daft is used to search Apple EgoDex videos by hand geometry and text semantics in one per-frame table. The main value is faster retrieval of unlabeled robot-manipulation clips for audit, failure mining, and fine-tuning.

## Problem
- Robotics teams collect long egocentric videos and hand-pose streams, but task-level labels hide fine events such as twisting, tight grips, and object-specific grasps.
- Failure mining and retraining need exact moments instead of whole episodes, especially when data arrives continuously.
- Text search alone misses hand pose and action details that are stored in sensor geometry.

## Approach
- The system adds native HDF5 support to Daft and reads each EgoDex HDF5/MP4 pair into a per-frame DataFrame with episode, frame, task, video, and pose fields.
- It encodes video frames at 1 fps with Google SigLIP-2 into 768D vectors using a stateful GPU UDF. A text query is encoded with the same model and ranked by cosine similarity.
- It computes geometric columns from EgoDex hand data: 48 wrist/fingertip pose values and 204 skeleton values across 68 joints.
- It derives per-frame and temporal features such as fingertip distance, curl, pinch, palm orientation, aperture, wrist position, wrist velocity, curl velocity, and forearm roll.
- A query filters frames with pose/action predicates, ranks matches by optional text similarity, groups by episode, and returns navigable [start, end] matching segments.

## Results
- No precision, recall, latency, throughput, or full dataset-scale benchmark is reported.
- The implemented pipeline stores 1 fps SigLIP embeddings with 768 dimensions alongside geometric features computed from 48 pose values and 204 skeleton values.
- An open-palm query filters frames in the 0.9 to 1.0 openness band and returns the top 5 matching episodes.
- In k=2 examples, hammer grip + "stapler" returns the actual stapler-in-hand episode at rank 1; the second match is a false positive involving a small black case.
- A lifting query on the "Assemble soft legos into a tower" episode finds 12 separate [start, end] segments, with the UI showing the first 5 as distinct block lifts.
- The post claims geometry-only queries separate open versus closed palms and writing grips, while combined queries such as grasping + "shirt" retrieve two t-shirt-folding episodes.

## Link
- [https://www.eventual.ai/blog/egodex-scenario-search](https://www.eventual.ai/blog/egodex-scenario-search)
