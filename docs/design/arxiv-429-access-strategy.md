# arXiv 429 Access Strategy

Date: 2026-05-13

## Scope

This note records a low-impact check of arXiv paper retrieval paths and the
policy constraints that shape Recoleta's behavior when arXiv returns HTTP 429.
It does not document or recommend bypassing arXiv rate limits.

## Official Constraints

- arXiv API Terms of Use say clients must respect API rate limits and must not
  attempt to circumvent them. If a use case needs a higher request rate, arXiv
  asks developers to contact support:
  https://info.arxiv.org/help/api/tou.html
- The legacy APIs, including OAI-PMH, RSS, and the arXiv API, are limited to no
  more than one request every three seconds and a single connection at a time:
  https://info.arxiv.org/help/api/tou.html#rate-limits
- The API manual asks production clients to cache results because repeated
  calls for the same query are normally unnecessary within a day:
  https://info.arxiv.org/help/api/user-manual.html
- The main `arxiv.org` robots policy allows `/abs`, `/pdf`, and `/html` for the
  default user agent, but declares a `Crawl-delay: 15` and disallows automated
  access to paths such as `/e-print` and `/src`:
  https://arxiv.org/robots.txt
- For bulk full-text use, arXiv points to Kaggle and Amazon S3 instead of
  programmatic crawling of the main site:
  https://info.arxiv.org/help/bulk_data.html

## Low-Impact Probe

Using an honest project User-Agent and no browser impersonation:

- `GET https://arxiv.org/html/1706.03762` returned HTTP 200 with
  `content-type: text/html; charset=utf-8` and `content-length: 182419`.
- `GET https://export.arxiv.org/api/query?id_list=1706.03762&max_results=1`
  returned HTTP 200 with `content-type: application/atom+xml; charset=utf-8`.

These checks show that single-paper HTML retrieval and metadata retrieval work
from the current environment when performed politely. They do not show that
browser-like automation can or should bypass 429.

## Recommended Behavior

- Do not use fake browser headers, extra machines, proxies, or automated browser
  sessions to get around 429.
- Prefer the arXiv API or OAI-PMH for metadata. Keep those clients single
  connection and at least three seconds apart.
- For Recoleta's `html_document` enrichment path, treat `/html/{id}` as a
  main-site crawl path: default to serial fetches and about one request every
  15 seconds.
- Cache stored article content and avoid refetching content already present in
  the local database.
- When arXiv returns 429 with `Retry-After`, wait according to that header before
  retrying. If the item still fails, let the pipeline mark it retryable instead
  of immediately hammering the endpoint.
- For large backfills or full-text corpus work, use the published S3 or Kaggle
  bulk data paths rather than crawling arXiv pages.
