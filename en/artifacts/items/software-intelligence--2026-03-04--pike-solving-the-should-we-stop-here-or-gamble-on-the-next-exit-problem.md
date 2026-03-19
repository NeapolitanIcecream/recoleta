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
- geospatial-computing
- driving-time-search
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Pike – Solving the "should we stop here or gamble on the next exit" problem

## Summary
Pike is an app for highway driving scenarios that helps solve the decision problem of “should we stop at this exit, or gamble that the next one is better.” By precomputing exit sequences and the actual driving time from exits to points of interest, it provides recommendations that better match road-trip decision habits than typical map apps.

## Problem
- Existing map features like **Add Stop** or radial search are not well suited to highway drivers: users care about “what can I reach within a 1–5 minute detour from the next few exits,” not places that are close in straight-line distance on the map but require a long real-world detour.
- Simple methods based on direction or real-time graph traversal can recommend incorrect or unreachable exits because of road curvature, bidirectional travel constraints, messy OSM data, and connected-component issues.
- This problem matters because choosing where to eat, refuel, charge, stop at a rest area, or stay at a hotel is a frequent and essential need during long-distance driving. Missing the right exit can mean having no ideal option for hundreds of miles, directly affecting the travel experience.

## Approach
- The problem is reframed from “guessing available options ahead in real time” to “pre-organizing highway exit sequences,” structuring exits along each route into a normalized ordered form, similar to a linked list, instead of doing complex graph searches while driving.
- Early attempts included: finding POIs based on current travel direction, building an undirected highway graph from OSM and using Dijkstra to find exits, and then moving to a bidirectional directed graph; these approaches all failed or were unstable because of reachability or data-boundary issues.
- The final core mechanism is to import OSM data into OSRM and offline precompute the driving time and distance from “every interstate highway exit to every POI,” rather than performing radius searches.
- The recommendation logic is very straightforward: a restaurant, gas station, EV charger, rest area, or hotel appears on an exit card only if it is reachable within **5 minutes of driving** from that exit; otherwise, it is not recommended.
- In the product UI, users can swipe through cards for the next several exits, mimicking the blue highway logo signs, to reduce decision burden while driving.

## Results
- The article **does not provide formal benchmarks, offline evaluation data, or user-study metrics**, so there is no verifiable accuracy, recall, or quantitative comparison with Google Maps or Apple Maps.
- The author claims the system already covers the **continental United States**, with precomputed driving time and distance for “every interstate exit × every restaurant/gas station/EV charger/rest area/hotel.”
- To compute these full road-network and POI relationships, the system used an AWS instance with **more than 200 GB of memory**, costing **over $1000 per month**, though in practice it only needed to run for **a few hours** to complete the precomputation.
- The key threshold in the current product is **5 minutes of driving time**: **if it takes more than 5 minutes, it is not recommended**. The author presents this as the main source of the app’s accuracy and practicality, and plans to make it configurable in the future.
- Compared with earlier versions, the author’s strongest concrete conclusion is that using exit sequences plus real driving-time search avoids the erroneous recommendations caused by directional heuristics, real-time traversal of undirected/directed graphs, and cases where “an exit cannot actually be used to leave the highway.”

## Link
- [https://tomjohnell.com/pike-solving-the-should-we-stop-here-or-gamble-on-the-next-exit-problem/](https://tomjohnell.com/pike-solving-the-should-we-stop-here-or-gamble-on-the-next-exit-problem/)
