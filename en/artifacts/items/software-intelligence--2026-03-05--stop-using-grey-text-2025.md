---
source: hn
url: https://catskull.net/stop-using-grey-text.html
published_at: '2026-03-05T23:15:57'
authors:
- catskull
topics:
- web-accessibility
- ui-design
- readability
- css
- human-ai-interaction
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Stop using grey text (2025)

## Summary
This is a short essay about web readability and accessibility, whose central argument is that body text should not be set in low-contrast gray on a light background. The author argues that this common design choice directly harms the reading experience, and that it is actually easy to avoid through higher contrast or support for `prefers-contrast`.

## Problem
- The article criticizes the common web design practice of using “gray text on a grayish-white background,” which significantly reduces body-text readability.
- This affects a much broader set of users, not just people with explicit visual impairments, because low-contrast text makes reading more effortful even for ordinary readers.
- This matters because designers, in pursuit of so-called “design-y” aesthetics, deliberately override the default text color and end up sacrificing information delivery and accessibility.

## Approach
- The core approach is simple: do not set body text in low-contrast gray, especially not on an off-white background.
- If low-contrast colors must be used for stylistic reasons, sites should at least support the CSS `prefers-contrast` media query so users who need higher contrast can recover a readable style.
- The author explains the issue in the most direct terms: low contrast makes textual information feel like it has been compressed and degraded, reducing “information density” and content fidelity.
- The piece also uses a side-by-side “demo” to show the obvious difference in reading experience between high-contrast and low-contrast text.

## Results
- The article **does not provide formal experiments, datasets, or quantitative metrics**, so there are no precise numerical results to report.
- Its strongest concrete claim is that increasing contrast makes content “higher fidelity,” improves information density, and improves the reading experience for everyone, not only users with visual impairments.
- The article also offers a clear engineering recommendation: use the `prefers-contrast` media query as a fallback, indicating that the cost of fixing the issue is low and “easy” to implement.
- Compared with the design baseline of “gray text + grayish-white background,” the author asserts that default or higher-contrast text rendering is significantly more readable, though no quantitative comparison is given.

## Link
- [https://catskull.net/stop-using-grey-text.html](https://catskull.net/stop-using-grey-text.html)
