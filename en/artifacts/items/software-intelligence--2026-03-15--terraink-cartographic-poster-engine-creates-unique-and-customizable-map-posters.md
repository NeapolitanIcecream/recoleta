---
source: hn
url: https://github.com/yousifamanuel/terraink
published_at: '2026-03-15T23:06:07'
authors:
- thunderbong
topics:
- map-poster-generation
- cartography
- geospatial-visualization
- openstreetmap
- react-typescript
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# TerraInk: Cartographic Poster Engine-creates unique and customizable map posters

## Summary
TerraInk is an open-source cartographic poster generator still under development, designed to turn any city or region into a customizable high-resolution map poster. It is built on OpenStreetMap data and a modern web technology stack, emphasizing theme styling, layer control, and export capabilities.

## Problem
- The problem it addresses is that ordinary users or design enthusiasts lack a simple tool to quickly turn real map data into printable, personalized city posters.
- This matters because map posters have both decorative and commemorative value, while also requiring a balance between geographic accuracy, visual customization, and export quality.
- The current description also suggests it aims to be an open-source implementation that is easy to extend and maintain, rather than just a one-off generation tool.

## Approach
- The core approach is to connect public geospatial data sources: Nominatim for geocoding, OpenStreetMap/OpenMapTiles/OpenFreeMap for map data, and MapLibre to render the visualized map.
- The frontend and application layer are built with Bun, React, and TypeScript, providing an interactive configuration interface where users can choose locations, themes, colors, labels, and export dimensions.
- Through a "theme system + per-layer style control" mechanism, users can adjust layers such as roads, water bodies, parks, and buildings separately to generate stylized posters.
- With typography controls and Google Fonts support, users can customize how city/country labels are displayed.
- It ultimately supports exporting high-resolution PNGs at arbitrary dimensions to meet printing needs.

## Results
- The text **does not provide formal paper-style quantitative experimental results**, nor does it give datasets, baseline methods, or metric comparisons.
- Specific functional claims include the ability to generate city map posters for "any location in the world" based on real OpenStreetMap data.
- It offers "dozens of curated themes," meaning dozens of preset themes, and also supports custom color schemes.
- It supports detailed layer control, including per-layer styling for elements such as roads, water bodies, parks, and building footprints.
- It supports high-resolution PNG export and can generate print-ready posters at user-defined dimensions.
- The project explicitly states it is "still in development," so at present it is more of an engineering project with improving functionality than a research result validated through benchmarks.

## Link
- [https://github.com/yousifamanuel/terraink](https://github.com/yousifamanuel/terraink)
