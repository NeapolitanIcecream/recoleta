---
source: hn
url: https://trashalert.io
published_at: '2026-03-05T23:23:29'
authors:
- hudtaylor
topics:
- civic-tech
- geospatial-data
- community-sourcing
- address-lookup
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: I mapped 954K addresses because AI hallucinated my trash day

## Summary
TrashAlert is a resident-facing trash collection lookup and reminder website that helps users quickly find their trash, recycling, and organics pickup days, while using community contributions to fill in missing data. Its core value is integrating scattered municipal open data and neighbor-submitted reports into an address-level service that is searchable, reminder-enabled, and visualized.

## Problem
- It solves the problem of residents not knowing their household trash pickup dates, dealing with complex holiday delay rules, and easily missing the time to take out the trash.
- Municipal information is often scattered, hard to search, or not detailed enough at the address level, creating a high barrier to practical use.
- Community reporting helps fill in missing areas and updated information, which is important for both coverage expansion and data accuracy.

## Approach
- Users enter a street address, and the system uses **municipal open data** and **community reports** to look up that address’s collection schedule in real time.
- It provides address-level results showing trash, recycling, and organics pickup days, and automatically accounts for holiday delays.
- It uses an interactive map to color-code addresses by pickup day, with support for zooming, filtering by day, and address search, making it easier to inspect an entire street or neighborhood.
- It uses a community-building mechanism: users can report their own pickup day, help neighbors complete the database, and are incentivized to participate through a leaderboard.
- It states that address lookups are processed in real time and that it does **not store** users’ search contents, reducing privacy concerns.

## Results
- The most specific scale figure is the title’s claim that it “mapped **954K addresses**,” indicating that it has built a large-scale address-level mapping.
- It currently explicitly supports **2** cities: **San Diego** and **Austin**, and says it plans to expand city by city.
- In San Diego, it describes the **three-bin system**: black and green bins are collected **weekly**, while blue bins are collected **every other week**; black and green bin pickup days span **Mon-Fri**.
- It provides the **2026 holiday schedule** rule: no collection on designated holidays, and starting from the holiday, the remaining pickups that week are **shifted forward by 1 day**.
- The text does not provide strict paper-style evaluation metrics, comparison baselines, or quantitative experimental results such as accuracy/F1/recall; its strongest concrete claims are large-scale address mapping, real-time lookup, automatic holiday adjustment, and a community-verified data-building process.

## Link
- [https://trashalert.io](https://trashalert.io)
