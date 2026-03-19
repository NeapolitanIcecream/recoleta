---
source: arxiv
url: http://arxiv.org/abs/2603.11861v1
published_at: '2026-03-12T12:34:49'
authors:
- Quentin Goux
- Nadira Lammari
topics:
- cybersecurity-training
- attack-script-generation
- model-driven-architecture
- tosca
- knowledge-graph
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Automatic Attack Script Generation: a MDA Approach

## Summary
This paper proposes an MDA (Model-Driven Architecture)-based method for automatically generating attack scripts, which gradually transforms informal attack scenario descriptions into executable scripts and attack environments for cybersecurity teaching and training. Its core value is reducing the time, errors, and skill barriers involved in manually building exercise environments, while improving cross-platform reusability.

## Problem
- Attack scripts and environments in cybersecurity practical training usually require manual configuration, which is costly, time-consuming, and error-prone.
- Existing attack models and frameworks are heterogeneous in syntax and semantics, and most cannot uniformly describe both the attack process and the attack context, making automatic script generation difficult.
- Manually implemented training scenarios quickly become outdated and are also hard to migrate across different platforms, limiting the updating and reuse of teaching and training content.

## Approach
- Proposes a unified attack model as the CIM (Computation Independent Model), using a formal language to describe attack steps, preconditions and postconditions, as well as the involved IT resources/context, with input guided through a user interface.
- Stores the formalized attack scenarios and context in a knowledge graph/property graph database (Neo4j), and automatically derives the required resources and environment from attack operation patterns.
- At the PIM (Platform Independent Model) layer, uses TOSCA Simple Profile 1.3 YAML service templates to represent abstract infrastructure and abstract attack scripts; the authors introduced minimal extensions for attack scenarios, such as `AttackTransitions` and `HostSystem`.
- Designs 12 automatic transformation rules from CIM to PIM, mapping resources to topology nodes/ports, mapping attack paths to workflow steps, and inferring the target host for each step through reasoning assumptions (such as `iao` and `ig`).
- At the PSM (Platform Specific Model) layer, instantiates the abstract model on concrete platforms; the paper demonstrates an implementation flow using OpenTOSCA to provide infrastructure and Ansible to execute automated scripts.

## Results
- The paper’s main contribution is proposing and demonstrating an end-to-end automated pipeline: from informal attack descriptions to CIM, then to TOSCA PIM, and finally to executable PSM and command-line execution.
- In the example “SnifAttack,” the system automatically derives **38 resources**, and the resulting overall knowledge graph reaches **182 nodes and 1482 relationships**.
- For PIM generation, the authors implemented **12 transformation rules** and automatically assigned target hosts to attack steps based on two types of reasoning assumptions; among the **6 steps** of SnifAttack, `iao` inferred the targets for the first **2 steps**, after extension covered another **2 steps**, and `ig` inferred the remaining **2 steps**.
- The generated PIM is represented in **TOSCA Simple Profile v1.3** YAML and is checked for syntax and semantics using **TOSCA Toolbox**, after which the corresponding UML diagrams are automatically produced.
- The paper does not provide systematic quantitative evaluation such as standard benchmark comparisons with existing methods, accuracy, generation success rate, or percentage of time saved; the strongest empirical evidence is the automatic generation of the SnifAttack case and its executable demonstration on the OpenTOSCA+Ansible platform.

## Link
- [http://arxiv.org/abs/2603.11861v1](http://arxiv.org/abs/2603.11861v1)
