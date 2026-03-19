---
source: hn
url: https://catskull.net/stop-using-grey-text.html
published_at: '2026-03-05T23:15:57'
authors:
- catskull
topics:
- web-accessibility
- color-contrast
- ui-design
- css
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Stop using grey text (2025)

## Summary
This is not a robotics or machine learning research paper, but a short essay about web readability and accessibility. The author strongly opposes using gray body text on light backgrounds, arguing that it significantly degrades the reading experience and excludes some users.

## Problem
- The problem the article addresses is that many websites deliberately use low-contrast gray text on light gray/off-white backgrounds, making content hard to read.
- This matters because low contrast harms accessibility, increases the reading burden for both typical users and users with visual impairments, and directly shrinks the potential audience.
- The author also points out that this practice is usually caused by manually overriding the default text color, meaning the issue is not a technical limitation but a design choice.

## Approach
- The core approach is very simple: **stop using low-contrast gray text**, and prioritize high-contrast body text colors.
- If a design insists on using a low-contrast scheme, the author suggests at minimum supporting CSS's `prefers-contrast` media query so that users who need higher contrast can get a more readable version.
- The article illustrates the readability problem by directly criticizing designers, giving a simple CSS direction, and showing a “contrast demo.”
- The essential mechanism is to increase the luminance/color contrast between foreground text and background, thereby improving clarity of information delivery and reading comfort.

## Results
- The text **does not provide formal experiments, datasets, metrics, or quantitative results**, so there are no numerical breakthrough results to report.
- The strongest concrete claim is that gray text on a light background can make users wonder whether their “eyesight is getting worse,” indicating a clear increase in subjective reading burden.
- The author argues that increasing contrast helps everyone and can improve the “information density” and “fidelity” of content.
- The only actionable technical recommendation given is to support `prefers-contrast`, but no A/B tests, accessibility score improvements, or user study numbers are provided.

## Link
- [https://catskull.net/stop-using-grey-text.html](https://catskull.net/stop-using-grey-text.html)
