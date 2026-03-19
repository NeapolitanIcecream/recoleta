---
source: hn
url: https://en.wikipedia.org/wiki/Leap_second
published_at: '2026-03-09T23:53:16'
authors:
- pinkmuffinere
topics:
- timekeeping
- leap-second
- utc
- distributed-systems
- clock-synchronization
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# Leap Second

## Summary
A leap second is a 1-second correction mechanism introduced to keep UTC, which is based on atomic clocks, closely aligned with solar time defined by the Earth's rotation. This article systematically explains the physical causes of leap seconds, the implementation rules, the engineering problems they create, and the international progress toward gradually abolishing leap seconds by around 2035.

## Problem
- It is necessary to address the continuously accumulating offset between **atomic time (TAI)** and **Earth-rotation time (UT1)**; otherwise, civil time UTC would gradually drift away from solar time.
- Although leap seconds keep the difference between UTC and UT1 within about **±0.9 seconds**, their **irregular nature and announcement only about 6 months in advance** create implementation complexity and failure risks for computing, network synchronization, navigation, and trading systems.
- Different systems handle leap seconds inconsistently (repeated second, 23:59:60, freeze, smear, etc.), leading to inconsistent timestamps across systems and affecting precise ordering, continuous timekeeping, and interoperability.

## Approach
- The core mechanism is simple: when **UTC is about to deviate too far from UT1**, the **IERS** announces the insertion, or theoretically deletion, of **1 second** at the end of a month, pulling UTC back close to UT1.
- Since **1972**, UTC has run on strict SI seconds, but inserts a positive leap second at **23:59:60** when needed; negative leap seconds are theoretically possible, but the text notes that **none has yet occurred**.
- In terms of rules, the IERS usually decides to act when the offset approaches **0.6 seconds**, to ensure that **UTC-UT1 does not exceed ±0.9 seconds**; announcements are typically issued every **6 months**, with implementation preferably at the end of **June or December**.
- The text also discusses alternatives: using **TAI** as the internal time standard, adopting **leap smear** for gradual adjustment, or in the future replacing frequent leap seconds with less common **leap minute / leap hour**.
- At the international standards level, **2022年CGPM Resolution 4** decided to relax the allowable UT1-UTC difference by **2035年或之前**, effectively paving the way for ending routine leap seconds while preserving UTC's long-term link to Earth's rotation.

## Results
- Since **1972**, UTC has had **27 positive leap seconds** added; the most recent occurred on **2016-12-31**. As of **2024**, **TAI and UTC differ by 37 seconds** (the initial 10 seconds + 27 leap seconds).
- During **1972–2020**, leap seconds occurred on average about once every **21 months**, but the distribution was highly irregular: for example, there were **6 years** with no leap second between **1999-01-01 and 2004-12-31**, while there were **9** leap seconds in the **8 years** from **1972–1979**.
- The Earth's average day length has increased by about **1.4–1.7 milliseconds per century** over the past several centuries; tidal friction alone contributes about **2.3 milliseconds/century**, but redistribution of mass inside and on the surface of the Earth offsets part of that.
- The text gives an extreme observation: **2022-06-29** was the shortest day on record, **1.59 milliseconds** shorter than 24 hours; **2020** saw **28** of the shortest days since 1960, prompting discussion of **negative leap seconds** and alternatives.
- In terms of international decisions, the **2022** CGPM had already passed a resolution to raise the UT1-UTC limit by **2035年或之前**, and **2023年WRC-23** formally endorsed that direction; the text does not provide unified benchmark metrics like a research paper experiment, but instead uses historical statistics, institutional thresholds, and many engineering incident cases as the main “results.”

## Link
- [https://en.wikipedia.org/wiki/Leap_second](https://en.wikipedia.org/wiki/Leap_second)
