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
- notification-system
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Show HN: I mapped 954K addresses because AI hallucinated my trash day

## Summary
This is a trash collection lookup and reminder service for residents. Its core is combining municipal open data with community-submitted reports to provide a real-time, address-based collection calendar. It is not a paper about software foundation models, but it demonstrates a practical urban information system driven by data integration, map visualization, and community validation.

## Problem
- It addresses the problem of residents not knowing their trash, recycling, and organics collection dates, especially when holiday delay rules make schedules more confusing.
- This problem matters because missing collection creates real-world inconvenience, while official information is often fragmented, hard to search, and lacks a good address-level lookup experience.
- The text also implicitly points out that general-purpose AI can hallucinate on this kind of local, fine-grained, and highly time-sensitive information, so a verifiable data system is needed instead of purely generative answers.

## Approach
- Uses **address lookup** as the entry point: users enter a street address, and the system looks up the corresponding trash, recycling, and organics collection dates from a community database in real time.
- Combines **municipal open data** with **community reports**, and improves accuracy through neighbor verification, forming a sustainably scalable address-level database.
- Provides an **interactive map**: San Diego addresses are color-coded by collection day, with support for zooming, filtering by day, and searching by address.
- Builds in **holiday delay rules**, automatically adjusting collection schedules rather than only returning a static calendar.
- Uses **reminders, leaderboards, and contribution incentives** to encourage residents to report and maintain data, supporting city-by-city expansion.

## Results
- The system claims to cover **San Diego** and **Austin**, and supports ongoing “city by city” expansion, but does not provide more complete coverage metrics.
- The page title claims the author “mapped **954K addresses**,” which is the strongest quantitative scale signal in the text, but the excerpt does not provide the data source, mapping success rate, or error bounds.
- At the feature level, it supports lookup for **3 types** of collection: Trash, Organics, and Recycling. Trash and Organics are collected **weekly**, while Recycling is collected **every other week** (using San Diego’s three-bin system as the example).
- It supports the **2026 holiday schedule** delay rule: starting on a holiday, subsequent collections that week are **shifted forward by 1 day**.
- It does not provide standard research-style experimental results such as accuracy, recall, response time, or quantitative comparisons with official systems or other tools; the most concrete outcome is that it is already live and usable, with real-time lookup, map display, and email reminder capabilities.

## Link
- [https://trashalert.io](https://trashalert.io)
