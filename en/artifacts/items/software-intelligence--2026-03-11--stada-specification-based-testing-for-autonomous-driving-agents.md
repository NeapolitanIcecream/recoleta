---
source: arxiv
url: http://arxiv.org/abs/2603.10940v1
published_at: '2026-03-11T16:26:20'
authors:
- Joy Saha
- Trey Woodlief
- Sebastian Elbaum
- Matthew B. Dwyer
topics:
- autonomous-driving
- specification-based-testing
- temporal-logic
- scenario-generation
- simulation-testing
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# STADA: Specification-based Testing for Autonomous Driving Agents

## Summary
STADA is a specification-based test generation framework for autonomous driving agents that systematically generates simulation scenarios satisfying preconditions directly from formal temporal-logic specifications. Its goal is to cover the behavior space related to safety rules more comprehensively and efficiently than template-based, manual, or random methods.

## Problem
- Existing autonomous driving simulation testing typically relies on template-based, manually authored, or randomly generated scenarios, making it difficult to **systematically** cover all critical prerequisite situations for a given safety specification.
- When validating formal safety requirements, if tests do not actually trigger the specification’s preconditions, they cannot effectively check whether the agent complies with the corresponding rule.
- Autonomous driving rules involve both **spatial relationships** and **temporal evolution**, and there are many possible ways they can be satisfied; manually enumerating them is costly and prone to missing important boundary behaviors.

## Approach
- STADA takes SceneFlow specifications as input and expresses safety rules as **LTLf temporal logic + RFOL spatial relations**, so that “which scenarios are relevant” can be read directly from the specification.
- It first analyzes the preconditions, decomposing disjunctions and temporal structure in the formulas into a set of distinct **relational graphs (RGs)**, where each RG represents one structured scenario configuration satisfying the preconditions.
- It then automatically constructs initial static scenes from the RGs and generates feasible paths for the ego vehicle and NPCs on the simulation map that are consistent with the RGs; it uses k-shortest paths plus greedy diversification to retain more differentiated trajectories.
- During simulation execution, the ego vehicle is controlled by the autonomous driving system under test, NPCs are controlled by autonomous driving scripts, and dynamic speed adjustment based on longitudinal distance is used to increase the probability of triggering the specification’s preconditions.
- Finally, it evaluates trajectories with a specification monitor and uses 3 coverage metrics (fine-grained configuration coverage, oneflip coverage, and binary coverage) to measure whether the tests truly cover the behavior space defined by the specification.

## Results
- The paper evaluates STADA on multiple **LTLf** specifications formalized in SceneFlow and compares it using **3 complementary coverage criteria**.
- On the **finest-grained coverage metric**, STADA achieves **more than 2×** the coverage of the best baseline.
- On the **coarsest-grained coverage metric**, STADA achieves a **75% coverage improvement** over the best baseline.
- To reach the **same coverage** as the best baseline, STADA requires **6× fewer simulations**.
- At the implementation level, STADA uses **Scenic** to generate initial scenes, **Python/CARLA** to generate and execute simulations, and is compared against **three baseline methods** on **two different driving agents**.
- The abstract and excerpt do not provide finer-grained absolute values (such as exact coverage percentages or per-dataset/per-specification scores), but the core quantitative claim is higher coverage and significantly lower simulation cost.

## Link
- [http://arxiv.org/abs/2603.10940v1](http://arxiv.org/abs/2603.10940v1)
