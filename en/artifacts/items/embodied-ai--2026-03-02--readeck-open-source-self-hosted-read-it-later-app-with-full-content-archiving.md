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
- privacy
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Readeck – open-source, self-hosted read-it-later app with full content archiving

## Summary
Readeck is an open-source, self-hosted read-it-later and bookmark archiving app focused on fully saving the readable content of web pages, along with images and other resources, locally for long-term access. It is more like a lightweight archiving system oriented toward privacy and long-term preservation than a novel algorithmic method from research papers.

## Problem
- It addresses the problem that bookmarked web content can become unavailable, lose images, go offline, or otherwise become inaccessible over time. This matters because ordinary bookmarks usually save only links, and the original text and resources may be gone a few years later.
- It also addresses the privacy concern that users do not want to depend on third-party cloud services to read their personal saved content, especially in reading, archiving, and full-text search scenarios.
- Based on the provided material, this is not work in robotics or foundation models, so it has relatively low direct relevance to the user's focus topics.

## Approach
- The core mechanism is simple: after a user saves a link, the system immediately fetches and stores the readable content of the web page along with resources such as images, preventing losses caused by future changes to or disappearance of the original page.
- Each bookmark is saved as an **immutable single ZIP file** containing HTML, images, and other content; the application serves this content on demand directly or converts it into a web page / e-book (EPUB).
- The system identifies page types (articles, images, videos) and handles them accordingly; except for videos, the browser side generally no longer makes requests to external websites, improving privacy.
- In engineering terms, it uses a relatively simple stack: a Go backend, server-side rendering, Stimulus/Turbo for enhanced interactivity, and a simple database schema, with SQLite recommended. Most installations can be done via a single binary or a container.
- At the product feature level, it supports labels, favorites, archives, highlights, collections, browser extensions, full-text search, EPUB export, and OPDS access.

## Results
- The provided text **does not include formal quantitative evaluation results**; there are no datasets, baseline methods, or comparable figures such as accuracy, recall, or latency.
- The only explicit numerical information is mainly the code composition: **Go 74.9%**, **HTML 13.3%**, **JavaScript 6.5%**, **SCSS 3.3%**, **Python 1%**, **Other 1%**.
- There is one concrete runtime example for deployment: by default it can be accessed via **`http://localhost:8000/`**, and the container example maps port **8000:8000**.
- The strongest concrete claims are that the system stores text and images in the local instance as soon as a link is saved; **except for videos, it does not send requests from the browser to external websites**; and it claims that its simple stack enables “**very quick response times**” and a smooth experience, though no benchmark numbers or comparison baselines are provided.

## Link
- [https://codeberg.org/readeck/readeck](https://codeberg.org/readeck/readeck)
