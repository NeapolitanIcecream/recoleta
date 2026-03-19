---
source: hn
url: https://github.com/yousifamanuel/terraink
published_at: '2026-03-15T23:06:07'
authors:
- thunderbong
topics:
- map-poster-generation
- cartography
- openstreetmap
- map-rendering
- design-tool
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# TerraInk: Cartographic Poster Engine-creates unique and customizable map posters

## Summary
TerraInk is an open-source map poster generator still in development, using real OpenStreetMap data to create customizable city map posters for any location in the world. It is better understood as an engineering product reimplementation and frontend application rather than a research paper proposing a new algorithm.

## Problem
- The problem it solves is enabling ordinary users to conveniently generate high-quality, customizable, printable map posters for any city or location without manually handling map data, styling, and export workflows.
- This matters because map poster creation typically involves geocoding, tile rendering, layer styling, font control, and high-resolution export, and the integration barrier across these steps is fairly high.
- Based on the provided content, the project is primarily aimed at design/visualization creation scenarios and is only weakly related to user-interest topics such as robotics, world models, or vision-language-action.

## Approach
- The core mechanism is straightforward: the user enters a city name, region name, or coordinates; the system geocodes the location and then renders the map using OpenStreetMap data and vector tiles.
- The frontend/application stack uses Bun, React, and TypeScript, implementing an interactive poster editor rather than training a model or learning a policy.
- Rendering uses MapLibre; data sources include OpenStreetMap, OpenMapTiles, and OpenFreeMap; geocoding uses Nominatim.
- Customization capabilities include a theme system, custom color palettes, layered styling for roads/water bodies/parks/buildings, and controls for city/country labels and Google Fonts.
- The output supports exporting high-resolution PNGs at specified dimensions for print-ready poster generation.

## Results
- The provided text **does not include any quantitative experimental results**, datasets, baselines, evaluation metrics, or comparison figures.
- The strongest concrete claim is at the functionality level: it supports generating custom city map posters for “any location in the world,” backed by real OpenStreetMap data.
- The listed features include searching for locations by name or coordinates, dozens of themes or custom palettes, layered map style controls, typography controls, and high-resolution PNG export.
- The project explicitly states it is “still in development,” indicating that its current status is closer to an open-source application under development than a completed, validated research result.

## Link
- [https://github.com/yousifamanuel/terraink](https://github.com/yousifamanuel/terraink)
