---
source: hn
url: https://tomjohnell.com/pike-solving-the-should-we-stop-here-or-gamble-on-the-next-exit-problem/
published_at: '2026-03-04T23:46:47'
authors:
- tjohnell
topics:
- route-planning
- map-data
- poi-recommendation
- osm
- osrm
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Pike – Solving the "should we stop here or gamble on the next exit" problem

## Summary
Pike is a location-selection app for long-distance highway driving that solves the decision problem of “should we get off at this exit or gamble on the next one being better?” Its core idea is to precompute, offline, the interstate exit sequence and the real driving time from each exit to POIs, enabling recommendations that better reflect actual detour cost.

## Problem
- The existing “Add Stop” experience in navigation apps is not holistic enough, often offering scattered and unreliable candidates, and even missing key categories such as rest areas.
- What drivers actually care about is not places that are “close in straight-line distance,” but options at the next several exits that are only about 1–5 minutes of driving from the exit; this directly affects en-route decisions around food, gas, charging, rest, and more.
- Relying only on directional heuristics, radial search, or real-time graph traversal can easily produce bad recommendations because of road curvature, bidirectional reachability, messy OSM data, and transfer/interchange exits. So while the problem looks simple, it is actually easy to get wrong.

## Approach
- The problem was reframed from “finding points on a map graph in real time” to “pre-organizing the highway exit sequence”: the author ultimately canonicalized exit data into an ordered structure (similar to a linked list) rather than relying on complex runtime graph traversal.
- The early approach went through 5 versions: v1 used a heuristic for “POIs in the forward direction”; v2 used an undirected interstate graph + Dijkstra; v3 switched to a bidirectional directed graph; v4 precomputed exit sequences; v5 then added real driving-time search.
- The core mechanism is to import OSM data into OSRM and offline precompute driving distance and driving time from “every interstate exit in the continental US” to POIs such as restaurants, gas stations, EV charging stations, rest areas, and hotels.
- The recommendation rule is very straightforward: if a POI cannot be reached from a given exit within 5 minutes of driving, it is not recommended; the system therefore operates on “actual detour time” rather than a straight-line radius.
- The author explicitly summarizes the lesson learned: map problems should not rely on heuristics; instead, the data should be corrected/normalized and modeled rigorously at the level of reachability and travel time.

## Results
- The paper/article does not provide standard academic benchmarks, A/B tests, or user studies, so there are **no formal quantitative metrics** such as accuracy, recall, or satisfaction.
- The strongest quantitative facts are that the system limits recommendations to POIs **within 5 minutes of driving after an exit**, and that it precomputed driving distance and time for exit-POI pairs **across the continental US**.
- In terms of compute resources, the author says this offline precomputation required an AWS instance with **200+ GB of memory**, costing about **$1000+/month**, but the computation itself took only **a few hours**.
- Compared with the earlier versions, v5 is claimed to have significantly improved recommendation quality by avoiding errors such as direction misclassification caused by road curvature, reverse-exit recommendations caused by undirected graphs, and cases where “the exit actually only leads to another interstate and cannot reach the POI at all.”
- The author’s core conclusion is that Pike is currently driven by “exit sequences + precomputed real driving time,” which makes its recommendations “more accurate”; however, the article does not provide a formal numerical comparison with Google/Apple Maps.

## Link
- [https://tomjohnell.com/pike-solving-the-should-we-stop-here-or-gamble-on-the-next-exit-problem/](https://tomjohnell.com/pike-solving-the-should-we-stop-here-or-gamble-on-the-next-exit-problem/)
