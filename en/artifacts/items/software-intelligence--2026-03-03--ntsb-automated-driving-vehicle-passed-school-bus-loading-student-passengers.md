---
source: hn
url: https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx
published_at: '2026-03-03T23:30:19'
authors:
- Animats
topics:
- autonomous-driving-safety
- ads-failure-analysis
- remote-assistance
- school-bus-compliance
- transportation-investigation
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# NTSB: Automated Driving Vehicle Passed School Bus Loading Student Passengers

## Summary
This is not a research paper, but rather an NTSB preliminary investigation bulletin on an incident in which a Waymo automated driving vehicle unlawfully passed a school bus while it was stopped to load or unload students. Its core value lies in revealing safety deficiencies in the ADS’s school-bus scenario recognition and remote-assistance decision chain.

## Problem
- The issue highlighted in this bulletin is: **the automated driving system failed to remain stopped and ultimately unlawfully passed while a school bus had its red lights activated, stop arm extended, and was loading or unloading students**, directly threatening the safety of child passengers.
- This is important because the vehicle was an **unoccupied, SAE Level 4** system, which should have been able to independently handle safety-critical scenarios within its operational design domain; if it fails in a high-risk school-bus scenario, that suggests the system boundaries and safety safeguards may be inadequate.
- The incident also exposed a **remote-assistance misjudgment** problem: the vehicle proactively asked, “is this a school bus with active signals?”, the remote-assistance operator answered “No,” and the vehicle then resumed travel and passed the school bus.

## Approach
- The “method” of this document is not to propose a new algorithm, but to **reconstruct the incident based on accident investigation**: using descriptions of the vehicle and roadway environment, video evidence, school-bus exterior camera recordings, and operator information to analyze system behavior.
- The investigation focuses on the decision chain of **ADS perception → stopping → requesting remote assistance → remote response → resuming travel**, identifying weak points in the system’s compliance with school-bus laws and handling of unusual scenarios.
- The bulletin also places this single incident within a **broader pattern**: Austin ISD reported that multiple Waymo vehicles passing stopped school buses had occurred since the start of the 2025/2026 school year, indicating this may not be an isolated failure.
- Related regulatory actions include **NHTSA defect preliminary evaluation (PE25013)** and Waymo’s **software recall (25E-084) for 3,067 vehicles equipped with the 5th-generation ADS**, indicating that the issue has entered systematic safety review.

## Results
- At **7:55 a.m. CST on January 12, 2026**, an unoccupied **2024 Jaguar I-Pace** equipped with Waymo’s **5th-generation ADS** passed a school bus that was loading or unloading students on **East Oltorf Street** in Austin, Texas; at the time, the school bus’s **red lights were flashing and its stop arm was extended**.
- Video shows that the ADS-equipped vehicle was initially the **first vehicle to stop**, but after requesting remote assistance and receiving a “**No**” response, it **resumed travel and passed** the school bus **while the stop arm was still extended**.
- In total, **6 vehicles** passed during the school-bus stop, including the ADS-equipped vehicle and a passenger vehicle behind it; **no collision occurred**.
- Austin ISD reported that **multiple** incidents involving Waymo ADS-equipped vehicles passing stopped school buses had occurred since the **start of the 2025/2026 school year**; the text explicitly mentions that in addition to the January 12 incident, there was another incident on **January 14, 2026** involving a special-needs-route school bus.
- On **December 10, 2025**, Waymo notified NHTSA of a software recall update covering **3,067 vehicles** equipped with its **5th-generation ADS**; NHTSA’s Office of Defects Investigation opened preliminary evaluation **PE25013** on **October 17, 2025**.
- This text **does not provide academic benchmarks, experimental data, or performance metrics**; the strongest concrete conclusion is that a real-world safety incident occurred in which the **ADS + remote-assistance chain failed to correctly recognize and/or comply with school-bus stopping laws**, and this has already triggered a federal investigation and software recall.

## Link
- [https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx](https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx)
