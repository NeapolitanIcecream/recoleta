---
source: hn
url: https://en.wikipedia.org/wiki/Leap_second
published_at: '2026-03-09T23:53:16'
authors:
- pinkmuffinere
topics:
- timekeeping
- utc
- leap-second
- atomic-time
- earth-rotation
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Leap Second

## Summary
A leap second is a mechanism that occasionally adds, or theoretically removes, 1 second from UTC to keep atomic-clock time close to solar time as defined by Earth's rotation. This article outlines the principles, history, implementation process, engineering issues, and international progress toward gradually discontinuing leap seconds by 2035.

## Problem
- The problem it solves is: **UTC is based on highly precise atomic time, while UT1, defined by Earth's rotation, is not uniform**. Without correction, civil time would gradually drift away from astronomical solar time.
- This matters because UTC is the standard time for global civil use and digital systems; if its deviation from UT1 becomes too large, it would undermine the traditional time semantics of “noon being close to the Sun's highest point.”
- But leap seconds themselves also create engineering problems: they are irregular, can only be announced about 6 months in advance, and are implemented inconsistently across systems, causing anomalies in computing, networks, satellite navigation, and trading systems.

## Approach
- The core mechanism is very simple: **when the deviation between UTC and UT1 approaches the threshold, insert or delete 1 second in UTC** so that the two become close again.
- At present, IERS typically decides whether to make an adjustment, with the goal of keeping the **UTC−UT1 difference within ±0.9 seconds**; historically, only positive leap seconds have actually occurred, adding `23:59:60` at the end of a day.
- UTC therefore serves as a compromise timescale: it runs continuously according to SI atomic seconds under normal conditions, and is then realigned with Earth's rotation through leap seconds when necessary.
- The article also introduces alternative approaches: using TAI/GPS directly as machine time, using smear to spread out the 1 second, or in the future canceling frequent leap seconds and relaxing the allowed deviation between UT1 and UTC.

## Results
- Since the introduction of leap seconds in **1972**, up to the latest status given in the article, **27 leap seconds have been added**; the most recent occurred on **2016-12-31**.
- As of **2024**, **TAI and UTC differ by 37 seconds**, calculated as the initial **10 seconds** plus the subsequent **27 leap seconds**.
- Between **1972–2020**, leap seconds occurred on average about **once every 21 months**, but the distribution was highly irregular; for example, there were **6 consecutive years without a leap second** from **1999-01-01 to 2004-12-31**, while there were **9 leap seconds in the 8 years** from **1972–1979**.
- The long-term trend in the length of Earth's mean solar day is an increase of about **1.4–1.7 milliseconds per century**; the article also cites a model giving a main trend of **1.70 ± 0.05 ms/century**, with an additional variation of about **4 ms** and a period of about **1500 years**.
- The article states that leap seconds are clearly disruptive to modern systems, and cites actual software/network failure cases in years such as **2012** and **2015**; however, this is not a single experimental paper, so there is **no unified benchmark dataset or SOTA-style performance metric**.
- At the international level, **the 27th CGPM meeting in 2022 adopted Resolution 4**, deciding that by **2035 or earlier** the allowed maximum **UT1−UTC** difference would be increased, effectively paving the way to stop frequent leap-second insertions in the future; **WRC-23 in 2023** has formally endorsed this direction.

## Link
- [https://en.wikipedia.org/wiki/Leap_second](https://en.wikipedia.org/wiki/Leap_second)
