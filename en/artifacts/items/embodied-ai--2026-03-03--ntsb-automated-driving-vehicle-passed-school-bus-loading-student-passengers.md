---
source: hn
url: https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx
published_at: '2026-03-03T23:30:19'
authors:
- Animats
topics:
- automated-driving-safety
- school-bus-compliance
- remote-assistance
- ads-incident-investigation
- waymo
relevance_score: 0.14
run_id: materialize-outputs
language_code: en
---

# NTSB: Automated Driving Vehicle Passed School Bus Loading Student Passengers

## Summary
This is a preliminary NTSB investigative bulletin about a Waymo automated driving vehicle unlawfully passing a school bus in Texas while students were boarding or alighting. It reveals safety deficiencies in ADS recognition of school bus stopping signals and in the remote assistance decision chain, with direct safety implications for driverless deployment on public roads.

## Problem
- The issue highlighted by this event is: **an L4 automated driving vehicle failed to remain stopped as required by law and ultimately passed a school bus while its red lights were flashing and stop arm was extended**, directly endangering students boarding or exiting.
- This matters because school bus scenarios are high-risk traffic situations governed by strict rules; if an ADS fails in these rare but critical safety contexts, it indicates gaps in perception, rule understanding, or human-machine coordination.
- This is not a single isolated incident: Austin ISD reported that **multiple** similar incidents involving Waymo vehicles passing stopped school buses had occurred **since the start of the 2025/2026 school year**, prompting both the NTSB and NHTSA to open investigations and defect evaluations.

## Approach
- This is not an algorithm paper, but an **accident/incident investigative bulletin**; its core method is to reconstruct the event and identify possible failure points based on **video evidence, vehicle behavior records, and remote assistance interactions**.
- The event chain can be summarized as: the ADS vehicle first stopped in the opposing lane → the vehicle sent a prompt to remote assistance asking “**is this a school bus with active signals?**” → the remote assistance operator responded “**No**” → the vehicle resumed travel and passed the school bus while its stop arm was still extended.
- The bulletin specifically notes that the vehicle was operating **Waymo’s 5th-generation ADS (SAE L4)**, and that the vehicle was unoccupied at the time, indicating that the system was expected to independently handle driving and safety-critical decisions within its defined ODD.
- The NTSB’s goal is to continue investigating the **January 12 event and other similar incidents**, determine possible causes, and issue safety recommendations to prevent recurrence.

## Results
- The key confirmed finding is that at **7:55 a.m. on January 12, 2026**, a **2024 Jaguar I-Pace** equipped with Waymo’s 5th-generation ADS unlawfully passed a **2025 Thomas Built** school bus in Austin while students were boarding or alighting; **no collision occurred**.
- Scene conditions were: **35 mph** speed limit, **daylight, clear weather, and dry roadway**; the school bus had **flashing red lights and stop arms extended on both sides**, indicating that the environment was not adverse and the failure was not triggered by obvious weather or visibility problems.
- Video evidence shows that the ADS vehicle was initially the **first vehicle to stop**, but restarted after remote assistance replied “**No**”; ultimately, **a total of 6 vehicles** passed while the school bus was stopped, including the ADS vehicle and a passenger vehicle behind it.
- Austin ISD stated that **multiple** Waymo school-bus-passing incidents had occurred **since the start of the 2025/2026 school year**; the text explicitly mentions that in addition to the January 12 event, there was also a **January 14** incident involving a **2023 International** special-needs-route school bus.
- Specific regulatory developments include: NHTSA’s Office of Defects Investigation opened preliminary evaluation **PE25013** on **October 17, 2025**; on **December 10, 2025**, Waymo notified NHTSA of safety recall **25E-084**, involving a software update for **3,067 vehicles** equipped with its **5th-generation ADS**.
- The text **does not provide formal performance metrics, benchmark comparisons, or statistically significant results**; the strongest concrete claim is that the NTSB has identified repeated school-bus-passing incidents and is investigating their possible causes in order to develop safety recommendations.

## Link
- [https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx](https://www.ntsb.gov:443/investigations/Pages/HWY26FH007.aspx)
