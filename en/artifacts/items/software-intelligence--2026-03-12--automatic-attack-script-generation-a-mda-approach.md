---
source: arxiv
url: http://arxiv.org/abs/2603.11861v1
published_at: '2026-03-12T12:34:49'
authors:
- Quentin Goux
- Nadira Lammari
topics:
- model-driven-architecture
- attack-script-generation
- cybersecurity-training
- tosca
- knowledge-graph
relevance_score: 0.55
run_id: materialize-outputs
language_code: en
---

# Automatic Attack Script Generation: a MDA Approach

## Summary
This paper proposes an automated method based on Model-Driven Architecture (MDA) that converts informal attack scenario descriptions into executable attack scripts and attack environments for cybersecurity teaching and training. Its core value is reducing the cost, error rate, and platform lock-in associated with manually building training exercises.

## Problem
- Attack scripts and environments in cybersecurity practical training usually need to be built **manually**, a process that is time-consuming, error-prone, and highly dependent on technical, programming, and modeling skills.
- Existing attack models and frameworks are **heterogeneous** in both syntax and semantics, and usually cannot describe attack steps and attack context in a unified way, making them difficult to reuse and hard to automatically implement.
- Training environments evolve quickly and attack techniques change rapidly, so manually built exercise content **easily becomes outdated** and is hard to migrate across platforms.

## Approach
- The authors organize the process using the **three-layer MDA abstraction**: a unified attack model serves as the CIM, TOSCA is used to build the PIM, and platform-specific PSMs are then generated.
- At the CIM layer, they use their previously proposed **unified attack model** and a formal language to describe attack operation paths and attack context, with user-interface-assisted input; the context can also be automatically inferred from attack steps.
- The CIM is stored in a **Neo4j knowledge graph**, and then a set of **12 transformation rules** is used to automatically generate an abstract infrastructure topology and abstract attack workflow in TOSCA YAML.
- To address TOSCA’s limited support for attack semantics, the authors make minimal extensions by introducing the `AttackTransitions` interface and the `HostSystem` type to express attack actions and host targets.
- For target inference, the authors propose two types of **reasoning hypotheses**, such as `iao` and `ig`, to automatically find from the knowledge graph the host that should execute each attack step; they then instantiate the PIM on the OpenTOSCA + Ansible platform to generate concrete execution scripts and environments.

## Results
- The paper mainly provides a **feasibility validation** of the method and does not report systematic quantitative experimental results such as accuracy, success rate, or time cost on standard benchmark datasets.
- In the **SnifAttack** example, formalization automatically derives **38 resources**, bringing the overall knowledge graph to **182 nodes and 1482 relationships**.
- In the PIM generation stage, the authors define **12 transformation rules** and successfully auto-generate the TOSCA topology and workflow; the workflow covers the example’s **6 attack steps**: Scanning, UseOfDefaults, Sniffing, Disclosure, Discovery, and Checkmate.
- For target inference, the `iao` hypothesis infers targets for the first **2** steps in the example and, after extension, additionally covers **2** more steps; the `ig` hypothesis infers the remaining **2** steps, thereby completing execution targets for all **6/6** steps.
- The generated TOSCA service template passes the syntax and semantic checks of **TOSCA Toolbox** and automatically produces UML diagrams, indicating that the generated results are verifiable at the standards level.
- At the PSM layer, the authors show a concrete implementation for their self-built platform: **OpenTOSCA** provides the infrastructure, **Ansible** executes the concrete scripts, and command-line output examples are included, but no direct numerical comparison is provided against manual methods or existing automation approaches.

## Link
- [http://arxiv.org/abs/2603.11861v1](http://arxiv.org/abs/2603.11861v1)
