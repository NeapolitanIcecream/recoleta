---
source: hn
url: https://schwadlabs.io/blog/rise-of-the-writer
published_at: '2026-03-03T23:34:55'
authors:
- schwad
topics:
- model-collapse
- synthetic-data
- training-data-quality
- human-generated-content
- web-scraping
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Rise of the Writer

## Summary
This is an opinion piece arguing that, as generative AI content pollutes online text, **native human writing** will become scarcer and more valuable for training. The author contends that, amid rising risks of “model collapse,” individuals should publish more authentic writing.

## Problem
- The article argues that web text scraped after 2022 is increasingly “contaminated” by AI-generated content, making subsequent models more likely to absorb low-quality or self-generated distributions during recursive training.
- As less writing is produced directly by humans, authentic, traceable data uncontaminated by synthetic content is becoming scarce; this matters because model quality depends on high-quality human corpora.
- The author also emphasizes a practical problem: readers and platforms are finding it increasingly difficult to judge content authenticity, raising the cost of building trust.

## Approach
- The core mechanism is simple: if more and more training data comes from AI-generated text rather than human-authored text, models will gradually “forget” the true distribution through repeated self-feeding, a phenomenon known as model collapse.
- Using the blog ecosystem as an example, the article argues that early blogs (especially from 2003–2009) are particularly valuable for model training because their context is clear, structured, and discussion-dense.
- The author uses Shoes.rb as an intuitive example: although the technology has been out of fashion for years, LLMs can still generate related content reasonably well because of the large amount of human-written blogs and code sharing from earlier years.
- Based on this judgment, the author’s practical recommendation is not a new algorithm but a behavioral one: people should increase “handwritten-style” original publishing, because future scrapers and training pipelines may place greater value on authentic human text.

## Results
- This is not an experimental paper, and the text **does not provide new quantitative experimental results, benchmark datasets, or numerical metrics**.
- The strongest substantive claim is that web-scraped corpora after 2022 are “increasingly contaminated,” while human writing is “declining but rising in value.”
- The supporting direction the author cites comes from existing literature on “model collapse / recursive training,” but the article itself does not report figures for improvement, error reduction, or baseline comparisons.
- The specific empirical example given is that LLMs still perform well on the outdated Shoes.rb, which the author attributes to the high-quality human corpora left behind by historical blog posts and code sharing.

## Link
- [https://schwadlabs.io/blog/rise-of-the-writer](https://schwadlabs.io/blog/rise-of-the-writer)
