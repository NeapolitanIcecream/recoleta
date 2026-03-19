---
source: hn
url: https://codeberg.org/readeck/readeck
published_at: '2026-03-02T23:54:23'
authors:
- Curiositry
topics:
- self-hosted-app
- read-it-later
- web-archiving
- bookmark-manager
- privacy-first
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# Readeck – open-source, self-hosted read-it-later app with full content archiving

## Summary
Readeck is an open-source, self-hosted “read-it-later/bookmark archiving” web application focused on preserving the readable content of web pages and their related resources completely, privately, and for the long term. It is not a research-model paper, but a software system emphasizing simple architecture, fast response, and long-term archival capability.

## Problem
- Existing read-it-later or bookmark tools often **cannot fully preserve web page content**, especially related resources such as images, which leads to missing content when revisiting later.
- Web content is **ephemeral**: an article online today may be deleted, redesigned, or become unavailable in the future, so long-term preservation matters.
- Many modern web applications depend on complex frontend-backend separation and heavy deployment stacks, increasing the **barriers to installation, maintenance, and contribution**.

## Approach
- The core mechanism is simple: after a user saves a link, Readeck immediately fetches and stores the page’s **readable content and resources**; it also adapts its processing for image and video pages.
- Each bookmark is stored as an **immutable single ZIP file** containing HTML, images, and other content; the application serves this content directly on demand or converts it into a web page/EPUB.
- The system uses a **simple database model**, with SQLite recommended, to reduce deployment and maintenance complexity.
- The tech stack chooses **Go + server-side rendering**, with small amounts of interactivity provided by Stimulus/Turbo, avoiding heavyweight single-page applications and complex background processes.
- In its privacy design, except for videos, once content is saved, the browser **does not need to make further requests to external websites** when reading it, supporting private reading and long-term archival.

## Results
- It delivers clear functional outcomes: support for a complete reading and archiving workflow including **full-text search, labels, favorites, archives, highlights, collections, browser extension, EPUB export, and OPDS access**.
- Architecturally, it provides concrete implementation signals: the codebase is primarily **Go 74.9%**, supplemented by **HTML 13.3%**, **JavaScript 6.5%**, **SCSS 3.3%**, and **Python 1%**.
- Deployment is straightforward: it can run on port **8000** via a single container command, and it also supports startup as a **single binary**, lowering installation cost.
- The text does not provide rigorous benchmarks, datasets, or quantitative comparisons with competitors, so there are **no verifiable performance numbers**; the strongest concrete claims are “fast response,” “smooth experience,” and “long-term, private, complete archiving.”

## Link
- [https://codeberg.org/readeck/readeck](https://codeberg.org/readeck/readeck)
