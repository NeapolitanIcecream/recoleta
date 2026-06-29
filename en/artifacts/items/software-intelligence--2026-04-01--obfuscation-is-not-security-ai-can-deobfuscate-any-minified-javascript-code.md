---
source: hn
url: https://www.afterpack.dev/blog/claude-code-source-leak
published_at: '2026-04-01T23:25:29'
authors:
- rvz
topics:
- javascript-security
- code-deobfuscation
- llm-code-analysis
- software-supply-chain
- prompt-exposure
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Obfuscation is not security – AI can deobfuscate any minified JavaScript code

## Summary
This post argues that Anthropic's Claude Code source was already exposed through a public minified JavaScript bundle, and that modern LLMs can recover structure and sensitive details from such code with little effort. The main claim is that minification does not protect JavaScript against AI-assisted reverse engineering.

## Problem
- The paper targets a common security assumption: shipping minified JavaScript is treated as enough to hide prompts, logic, feature flags, and internal product details.
- This matters because JavaScript CLIs, web apps, Electron apps, and React Native apps ship client-visible code, and LLMs can read and restructure minified code far faster than manual reverse engineering.
- In the Claude Code case, the author argues that the source-map leak added comments and file structure, but the core logic, prompts, endpoints, and internal identifiers were already public in the npm bundle.

## Approach
- The author analyzes the public `@anthropic-ai/claude-code` npm package, focusing on the bundled `cli.js` file, described as a 13MB, 16,824-line minified JavaScript artifact.
- They use a simple AST-based extraction script to parse the bundle and pull out plaintext artifacts such as string literals, prompts, telemetry event names, environment variables, error messages, and endpoints.
- They then ask Claude itself to analyze and deobfuscate the minified bundle, with the claim that LLMs are strong at recovering readable structure from minified or transformed code.
- The post contrasts minification with stronger obfuscation techniques, then argues that even traditional JavaScript obfuscation is now weak against current AI models because many transforms are pattern-based and reversible.
- The final part presents AfterPack, the author's product, as an alternative based on irreversible or information-destroying transforms plus encrypted source maps for developer debugging.

## Results
- The AST parser processed the full 13MB `cli.js` bundle in **1.47 seconds**.
- From that file, the author reports extraction of **147,992 strings**, including **1,000+ system prompts**, **837 telemetry events**, **504 environment variables**, and **3,196 error messages**.
- The post says the npm bundle exposed hardcoded endpoints, OAuth URLs, a DataDog API key, and a full model catalog in plaintext, without needing the leaked source map.
- The leaked source map is described as covering an **1,884-file** project tree and exposing comments, file names, module boundaries, and internal experiment codenames.
- As external context, the author claims a clean-room Rust rewrite of Claude Code reached **50,000 GitHub stars in 2 hours** and later **100,000+ stars in about a day**, but these are ecosystem effects, not benchmark results for the deobfuscation method.
- The post gives no controlled benchmark against other reverse-engineering tools or models, so the quantitative evidence is a single case study plus extraction counts from one target bundle.

## Link
- [https://www.afterpack.dev/blog/claude-code-source-leak](https://www.afterpack.dev/blog/claude-code-source-leak)
