---
source: hn
url: https://cheekypint.substack.com/p/garrett-langley-of-flock-safety-on
published_at: '2026-03-06T23:56:28'
authors:
- hhs
topics:
- public-safety
- computer-vision
- real-time-systems
- sensor-fusion
- drone-systems
relevance_score: 0.22
run_id: materialize-outputs
language_code: en
---

# Garrett Langley of Flock Safety on building technology to solve crime

## Summary
This is an interview about how Flock Safety integrates license plate recognition, cross-agency data sharing, real-time 911 access, video search, and drones into a public safety operating system, rather than a strictly academic paper. The core value proposition is to transform originally inefficient, fragmented, and reactive law enforcement workflows into a more real-time, collaborative, and searchable system, thereby improving case clearance and apprehension efficiency.

## Problem
- Many crimes are opportunistic and occur across communities/cities, while traditional security systems often can only **record that a crime happened** but struggle to **quickly identify suspects and coordinate pursuit**.
- The US law enforcement system is highly localized, and agencies have historically relied on phone calls, fax, CSV/FTP, and similar methods to exchange information, resulting in poor real-time collaboration and delayed tracking, especially for cross-jurisdiction cases.
- Data sources such as city 911 systems, video surveillance, license plate data, and drones are fragmented from one another. Manual distribution and retrieval are costly, and many leads turn into cold cases because of time delays.

## Approach
- Centered on a **community/city-scale public safety operating system** rather than single-home security: first using self-powered, 5G-backhauled cameras to capture vehicles/license plates at roadsides, then expanding to the integration of multiple types of citywide video and event streams.
- Build real-time data pipelines: connect to the FBI's NCIC hot list, local "hot list," 911 call streams, and third-party/private cameras, so the system can immediately perform coordinated searches when an incident occurs.
- Use simple computer vision and retrieval capabilities for "actionable lead extraction": for example, searching by license plate, vehicle appearance, anomalous license plate matches, or clothing descriptions (such as white Converse shoes), rather than merely doing passive archiving.
- Use FlockOS to place multiple agencies, states, and departments on the same collaboration layer, and distribute results to frontline officers and drone systems, creating a closed loop from report to location, tracking, and arrest.
- On the hardware side, emphasize infrastructure-independent deployment: solar power, 5G, and limited edge compute design, to suit roadside locations that lack power or fiber.

## Results
- The interview claims that **in the past year it helped "clear" more than 1 million crimes**, and says this accounts for about **7% of reported crime in the US**; here, "help clear" is defined as participating in the case-solving/arrest process rather than independently completing all law enforcement work.
- In terms of deployment scale, it claims coverage of **6000+ cities** and **more than 50% of the US population**; the company's business reportedly grew from 0 to about **$500 million ARR (within 7 years)**.
- In a real-time response case, the speaker gives a specific figure: in a serious incident in an undisclosed city, it took about **17 minutes from the 911 call to the suspect's arrest**, relying on real-time 911 access, video retrieval, and appearance-based search.
- In a cross-agency coordination case, it is claimed that in a human trafficking operation spanning **4 states**, **76 people were arrested**, with multiple local police departments, state agencies, and federal agencies coordinating on Flock.
- In missing-person scenarios, it is claimed that in the past year the system helped handle **1000+ Amber/Silver Alert** cases.
- These results all come from the founder's oral account and case descriptions, and **do not provide reproducible experimental setups, public benchmark datasets, or rigorous comparative evaluations against academic/industry baselines**. The strongest related claim is that it can compress cases that originally required weeks/months or even could not be solved into minute-level response and real-time cross-agency collaboration.

## Link
- [https://cheekypint.substack.com/p/garrett-langley-of-flock-safety-on](https://cheekypint.substack.com/p/garrett-langley-of-flock-safety-on)
