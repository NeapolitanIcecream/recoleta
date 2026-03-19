---
source: arxiv
url: http://arxiv.org/abs/2603.09455v1
published_at: '2026-03-10T10:11:09'
authors:
- Ezio Bartocci
- Alessio Gambi
- Felix Gigler
- Cristinel Mateis
- "Dejan Ni\u010Dkovi\u0107"
topics:
- autonomous-driving
- scenario-testing
- openscenario-dsl
- answer-set-programming
- runtime-monitoring
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Declarative Scenario-based Testing with RoadLogic

## Summary
This paper presents **RoadLogic**, which automatically converts declarative OpenSCENARIO DSL (OS2) into executable autonomous driving simulations for systematic scenario-based testing. Its core value is connecting “what scenario to test” with “how to concretely execute the simulation,” while also providing an open-source implementation.

## Problem
- Existing autonomous driving scenario testing mostly relies on imperative/operational scenario definitions, requiring developers to manually enumerate a large number of variants, resulting in poor coverage and high cost.
- Declarative languages such as OS2 can express scenario intent at a high level, but there is a lack of systematic, open-source methods to automatically instantiate specifications into concrete, executable simulations.
- This matters because exhaustive testing on real roads is both expensive and dangerous, while simulation testing requires large numbers of **specification-compliant and diverse** concrete scenario instances.

## Approach
- First, the OS2 scenario specification is translated into a **symbolic automaton**, representing sequencing, parallelism, branching, and spatial/relational constraints as states and transition conditions.
- The automaton is then encoded as an **Answer Set Programming (ASP)** planning problem, and a solver generates high-level discrete plans that satisfy the constraints.
- Next, the high-level plans are refined into waypoints/goals for each vehicle and passed to the **FrenetiX** motion planner to generate physically feasible, collision-free trajectories in **CommonRoad**.
- Finally, **runtime monitoring** derived from the symbolic automaton is used to check whether the generated execution traces satisfy the original OS2 specification, retaining only compliant simulations.
- In simple terms: first “logically come up with a traffic script that satisfies the conditions,” then “drive it out using motion planning,” and finally “automatically verify whether it truly matches the original script.”

## Results
- The paper claims that **RoadLogic is the first open-source framework** capable of automatically instantiating declarative OS2 specifications into realistic, specification-compliant simulations; the paper excerpt does not provide verifiable numerical comparisons against similar open-source baselines.
- It evaluates multiple representative/diverse OS2 logical scenarios in the **CommonRoad** framework, combining **clingo** and **FrenetiX** to complete end-to-end generation and verification.
- Qualitative results state that the system can reliably produce **realistic, specification-satisfying** simulation executions within **minutes**.
- Through **parameter sampling**, the system can cover **diverse behavioral variants** under the same abstract scenario; the excerpt does not provide specific numbers for variant counts or coverage.
- The excerpt **does not provide detailed quantitative metrics** (such as success rate, average generation time, percentage improvement over baselines, dataset size, etc.); the strongest concrete claims are end-to-end automation, specification compliance, open-source availability, and the ability to generate diverse scenario instances within minutes.

## Link
- [http://arxiv.org/abs/2603.09455v1](http://arxiv.org/abs/2603.09455v1)
