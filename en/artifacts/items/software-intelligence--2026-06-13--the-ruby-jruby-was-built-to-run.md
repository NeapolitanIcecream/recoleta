---
source: hn
url: https://intertwingly.net/blog/2026/06/11/The-Ruby-JRuby-Was-Built-to-Run.html
published_at: '2026-06-13T22:31:40'
authors:
- mooreds
topics:
- rails
- jruby
- partial-evaluation
- program-compilation
- benchmarking
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# The Ruby JRuby Was Built to Run

## Summary
The post argues that Roundhouse can turn a Rails app into simpler Ruby code that JRuby can run much faster than stock Rails. It matters because it shows a path to both higher throughput and wider deployment for existing Rails apps.

## Problem
- Rails apps spend each request redoing work that does not change between requests, such as route resolution, SQL string building, template lookup, and type casting.
- JRuby already speeds up standard Rails in some cases, but it still runs the original metaprogrammed framework code.
- The question is whether compiling the app itself, instead of only changing the runtime, gives a larger gain.

## Approach
- Roundhouse reads a Rails app and makes request-invariant decisions at transpile time.
- It emits standalone projects in multiple languages, including Ruby, so the generated app can run on JRuby without changing the app logic.
- The generated Ruby keeps only the parts that vary per request, such as request format, flash state, and actual database contents.
- A compare gate checks emitted output against Rails output to keep behavior equivalent on the measured endpoints.
- The benchmark compares stock Rails and emitted Ruby on CRuby+YJIT and JRuby, using the same small Rails 8 blog app.

## Results
- On the HTML index endpoint, stock Rails does 481 req/sec on CRuby+YJIT and 1,057 req/sec on JRuby, a 2.2× throughput gain from JRuby alone.
- On the same endpoint, the emitted app is 11× faster than Rails on CRuby+YJIT and 25× faster than Rails on JRuby.
- On the JSON endpoint, stock Rails is roughly tied across runtimes: 1,272 req/sec on CRuby+YJIT vs 1,080 req/sec on JRuby.
- On the JSON endpoint, the emitted app is 6× faster than Rails on CRuby+YJIT and 43× faster than Rails on JRuby.
- The full diagonal comparison reaches 54× from emitted Ruby on JRuby versus stock Rails on CRuby+YJIT.
- The post also reports higher memory use on JRuby, around 1–1.5 GB RSS versus 135–416 MB on CRuby.

## Link
- [https://intertwingly.net/blog/2026/06/11/The-Ruby-JRuby-Was-Built-to-Run.html](https://intertwingly.net/blog/2026/06/11/The-Ruby-JRuby-Was-Built-to-Run.html)
