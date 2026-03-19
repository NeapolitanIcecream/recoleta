---
source: hn
url: https://kawasakirobotics.com/in/blog/202511_kaleido/
published_at: '2026-03-05T23:34:17'
authors:
- hhs
topics:
- humanoid-robotics
- bipedal-locomotion
- robot-control
- human-robot-interaction
- robot-hardware
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Humanoid robot: The evolution of Kawasaki’s challenge

## Summary
This article reviews the evolution of Kawasaki’s multiple generations of humanoid robots **Kaleido/Friends** from 2015 to 2023, focusing on how it transferred industrial robot expertise to a bipedal, dual-arm humanoid platform capable of coexisting with people. Its core value lies in improving humanoid robots’ autonomous operation, stable walking, and human-robot interaction capabilities for hazardous work, service, and remote-operation scenarios.

## Problem
- To replace or assist human work in human-centered environments, a general-purpose humanoid form capable of **bipedal walking and dual-arm manipulation** is needed.
- But industrial robot technology cannot be transferred directly to humanoid robots: humanoids must be **lightweight, self-supporting, resistant to falls, and fast-controlled**, while also moving stably in confined, unstructured environments.
- This matters because it determines whether robots can enter scenarios that traditional automation struggles to cover, such as **hazardous operations, disaster response, and care/daily assistance**.

## Approach
- In terms of design philosophy, the team did not mechanically replicate the human body. Instead, it **extracted key human functions** and reconstructed them using motors and mechanical structures to achieve more practical bipedal motion.
- On the hardware side, it continuously pursued **lightweighting and integration**: moving from external controllers to more compact controllers and dedicated humanoid controllers, using **magnesium-alloy structural components** and **3D-printed resin shells**, and integrating the battery and electronic systems into the body to enable untethered autonomous operation.
- For sensing and gait control, to handle impact conditions such as stepping and jumping, the team developed its own **6-axis force/torque sensor**, replacing commercial products that were too heavy, expensive, and vulnerable to impact damage.
- In control, it continuously improved gait stability, especially by adding **real-time footstep adjustment** in 2023 to correct landing points under disturbance and reduce fall risk.
- In interaction, the Friends series introduced **AI dialogue + synchronized gestures** to explore more natural human-robot communication and service-oriented humanoid design.

## Results
- At iREX 2017, Kaleido was publicly demonstrated for the first time, performing actions such as **standing up and pull-ups**; at the time its specs were **175 cm, 85 kg, externally powered**.
- The early control system had clear bottlenecks: even by the third generation it still used the industrial robot **E-controller**, whose control cycle was too slow for humanoid applications and required **4 independent units**; after switching to the F-controller it became more compact, but was still about **30 kg**, making in-body integration unsuitable.
- In 2019, the first demonstration of **onboard battery-powered, fully untethered bipedal walking** was achieved; at that time Kaleido was **178 cm, 85 kg**, and the control and electrical systems were integrated into the body without increasing total weight.
- To improve gait capability, the team developed a custom **6-axis force/torque sensor** for humanoid walking; the article gives qualitative advantages that it is better suited to **lightweight and impact-resistant** requirements, but **does not provide specific accuracy, weight, or cost figures**.
- In 2021, Friends demonstrated **AI question answering and synchronized gesture interaction**, and conducted live Q&A with children at a science museum event; the article only provides qualitative descriptions such as “the audience responded positively and it could provoke laughter,” with **no quantitative evaluation metrics**.
- In 2023, through software and hardware upgrades and **real-time footstep adjustment**, the company claimed to **significantly reduce fall risk and improve robustness**, but **did not report specific success rates, speed, disturbance magnitude, or comparative baseline data**.

## Link
- [https://kawasakirobotics.com/in/blog/202511_kaleido/](https://kawasakirobotics.com/in/blog/202511_kaleido/)
