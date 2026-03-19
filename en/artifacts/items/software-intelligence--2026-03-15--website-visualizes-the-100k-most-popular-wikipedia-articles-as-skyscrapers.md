---
source: hn
url: https://wikicity.app/
published_at: '2026-03-15T22:25:27'
authors:
- mykowebhn
topics:
- information-visualization
- 3d-interface
- wikipedia
- interactive-exploration
- gamification
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# Website visualizes the 100k most popular Wikipedia articles as skyscrapers

## Summary
This is an interactive visualization project that maps the 100,000 most-viewed Wikipedia articles from the past 12 months into a 3D “city of skyscrapers,” using a gamified approach to help users explore the information space. It is more like an information visualization and interactive experience for the general public than a research paper presenting a new algorithm or system evaluation.

## Problem
- The problem it aims to solve is that Wikipedia’s most popular content is large in scale, list-based presentation is dull, and users find it hard to intuitively understand article popularity, relative ranking, and distribution relationships.
- This matters because turning abstract traffic and ranking data into a spatial metaphor can lower the barrier to exploration and improve knowledge discovery, educational presentation, and public engagement.
- From the provided content, it mainly focuses on “explorability and playability,” rather than serious information retrieval, knowledge reasoning, or software productivity problems.

## Approach
- The core mechanism is simple: each of Wikipedia’s 100,000 most popular articles is represented as a building, and users browse them in a 3D city.
- Building attributes are tied to article metrics; the interface explicitly shows **Views (12mo)**, **Words**, **View Rank**, **Floors**, and **Views relative to #1**, indicating that visual encodings such as building height/floor count carry information about popularity and scale.
- The interaction offers two main modes: **Explore** for roaming and clicking buildings to view entries and nearby buildings; **Fly & Destroy** for piloting a plane, shooting, and launching missiles, using game-like mechanics to enhance engagement and exploration.
- It also provides features such as random jumps, speed/altitude status, nearby building recommendations, and links to the original Wikipedia pages, forming a loop of “visualization + navigation + external reading.”

## Results
- The clearest result in terms of scale is that the system visualizes **100,000** “most-viewed Wikipedia articles.”
- The data window is **12 months of page views**, and it supports displaying the page-view ratio relative to the **#1** entry, as well as attributes such as **view rank / words / floors**.
- The provided excerpt **does not provide** any formal experiments, user studies, A/B tests, or benchmark comparisons, so there are no reportable figures for accuracy, recall, efficiency gains, or statistical significance.
- The strongest concrete claim is that the project implements an interactive 3D knowledge city that supports orbital exploration, click-based discovery of nearby entries, and a flight mode with shooting/missile mechanics to make exploration more fun.

## Link
- [https://wikicity.app/](https://wikicity.app/)
