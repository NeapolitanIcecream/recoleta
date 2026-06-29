---
source: arxiv
url: https://arxiv.org/abs/2606.13601v1
published_at: '2026-06-11T17:20:15'
authors:
- Haosen Yang
- Guowu Wei
topics:
- dexterous-manipulation
- musculoskeletal-hand
- anatomical-priors
- tendon-actuation
- robot-hand-design
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# MCR-Bionic Hand: Anatomical Structural Priors for Dexterous Manipulation

## Summary
MCR-Bionic Hand builds a biomimetic robot hand around anatomical hand structures that shape grasping before control and modulate contact after grasp. The paper claims these structures reduce the burden on active control by encoding useful motion, stability, and coordination in hardware.

## Problem
- Dexterous robot hands often rely on high-DOF control while simplifying the wrist, tendons, ligaments, and extensor hood that help human hands pre-shape and stabilize grasps.
- That simplification pushes grasp formation, distal coordination, and post-contact adjustment into the controller, even when anatomy could supply part of that function.
- The paper asks which anatomical structures change the relation between input, motion, contact, and stability in ways that matter for manipulation.

## Approach
- It builds MCR-Bionic as a 1:1 musculoskeletal hand with 23 bones, 61 wrist ligaments, more than 103 soft-tissue limit structures, 46 muscle units, and a 3-DOF wrist.
- It reconstructs three anatomical mappings: wrist-finger tenodesis for pre-shaping, extensor-hood routing for PIP-DIP coordination, and intrinsic-plus pathways for MCP control and distal stability.
- It uses closed hydraulic artificial muscles for local in-hand activation of each tendon pathway.
- It tests the hand with grasping and manipulation tasks such as chess-piece grasping, coin rotation, dorsal coin transfer, pen transfer, pen swinging, cube pushing, and dorsal coin flipping.
- It pairs the experiments with geometric mechanical models of the extensor hood, wrist-finger coupling, and intrinsic-plus behavior.

## Results
- The hand prototype contains 23 bones, 61 wrist ligaments, more than 103 soft-tissue constraints, 46 muscle units, and 24 simplified DOF; counting small rotations and palmar deformation, movable DOF exceeds 45.
- Estimated output is about 1.8 Nm at the MCP, 1.2 Nm at the PIP, and 0.5 Nm at the DIP for long fingers, with about 20 N fingertip force per finger.
- The thumb reaches about 1.4 Nm at the MCP, 0.8 Nm at the PIP, 0.5 Nm at the DIP, and about 20 N fingertip force.
- Wrist motion range is reported as -53° to 18° flexion/extension, -29° to 19° radial/ulnar deviation, and -60° to 50° axial rotation.
- Experiments show wrist extension can trigger passive index and thumb closing for pinch and lifting, and the reconstructed extensor hood makes DIP motion follow PIP posture.
- The paper does not report comparative task success rates or benchmark numbers against other robot hands; its strongest quantitative claims are the structural counts, torque estimates, force estimates, and wrist ranges.

## Link
- [https://arxiv.org/abs/2606.13601v1](https://arxiv.org/abs/2606.13601v1)
