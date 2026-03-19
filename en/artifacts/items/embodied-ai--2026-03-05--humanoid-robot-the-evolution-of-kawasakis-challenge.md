---
source: hn
url: https://kawasakirobotics.com/in/blog/202511_kaleido/
published_at: '2026-03-05T23:34:17'
authors:
- hhs
topics:
- humanoid-robot
- bipedal-locomotion
- robot-engineering
- human-robot-interaction
- remote-operation
relevance_score: 0.41
run_id: materialize-outputs
language_code: en
---

# Humanoid robot: The evolution of Kawasaki’s challenge

## Summary
This article reviews the evolution of Kawasaki’s 8 generations of humanoid robots, Kaleido/Friends, since 2015, focusing on how industrial robot expertise was translated into a humanoid platform that can walk bipedally, work with two arms, and coexist with people. It reads more like an R&D history and engineering retrospective than an academic paper proposing a new algorithm with standard benchmark evaluations.

## Problem
- The problem to solve is how to build a humanoid robot that can **move and perform tasks in environments designed for humans**, because a bipedal + dual-arm form is better suited to replacing humans in dangerous, dirty, exhausting work, or tasks that require access to existing facilities.
- The difficulty is that, unlike industrial robots, a humanoid must achieve **stable bipedal locomotion, fall resistance, onboard power, compact control, and perception/interaction capabilities** under strict self-weight constraints.
- This matters because if humanoids can also be combined with teleoperation, they could be used for **disaster response and hazardous-site operations**, reducing the need to expose people to high-risk environments.

## Approach
- The core idea is not to mechanically replicate the human body in full, but to **extract the key functions humans need to perform tasks** and then implement them with motors and mechanisms, thereby achieving stable bipedal walking.
- Across multiple prototype generations, they continuously worked on **lightweighting and system integration**: replacing external controllers with compact amplifiers/drivers, using magnesium-alloy structural parts and 3D-printed resin shells, and integrating batteries and electronics into the body to enable untethered standalone operation.
- To support walking control, they developed **custom 6-axis force/torque sensors**, because commercial ankle sensors, while highly accurate, are too heavy, too expensive, and insufficiently impact-resistant for a humanoid platform that may step, jump, and fall.
- On the control side, later versions added **real-time footstep adjustment**, correcting foot landing positions online when balance is disturbed, reducing fall risk and improving walking robustness.
- For human-robot interaction, the Friends series combined AI with work conducted in collaboration with Osaka University to enable **dialogue plus synchronized gestures**, exploring how to make humanoid robots better suited for care and daily assistance scenarios.

## Results
- In 2017, Kaleido was first publicly demonstrated at **iREX 2017**, where it could **stand up and do pull-ups**; at the time the code/system was still quite fragile, but the team ultimately completed the full demo. Publicly disclosed specs: **height 175 cm, weight 85 kg, externally powered**.
- By 2019, Kaleido achieved its first **fully autonomous bipedal walking demonstration with an onboard battery**; disclosed specs: **height 178 cm, weight 85 kg**. Control and power electronics were integrated into the body **without increasing total weight**.
- The article explicitly notes that the early F-controller still weighed about **30 kg**, making it too heavy to be built in; this bottleneck was later addressed through more compact amplifiers, motor drivers, and dedicated controller solutions.
- In 2023, through hardware/software upgrades and **real-time footstep adjustment**, it claims to have **significantly reduced fall risk and improved robustness**; however, **the article provides no quantitative metrics** (such as fall rate, speed, endurance, energy consumption, or benchmark comparisons).
- In 2021, Friends introduced **AI dialogue and gesture-synchronized interaction**, and at an event at Miraikan in Japan it demonstrated Q&A with children. The article reports on-site feedback (large audiences and good interaction effects), but **does not provide standardized evaluation data**.
- Overall, the strongest concrete claim is that Kawasaki has progressed from early prototypes to a multi-generation humanoid robot platform that can be **publicly demonstrated, run independently on onboard batteries, walk more stably, and support human-robot interaction**; however, this article **does not include rigorous academic benchmark results or quantitative comparisons with SOTA systems**.

## Link
- [https://kawasakirobotics.com/in/blog/202511_kaleido/](https://kawasakirobotics.com/in/blog/202511_kaleido/)
