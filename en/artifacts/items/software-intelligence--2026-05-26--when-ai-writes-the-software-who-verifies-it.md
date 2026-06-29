---
source: hn
url: https://leodemoura.github.io/blog/2026-2-28-when-ai-writes-the-worlds-software-who-verifies-it/
published_at: '2026-05-26T22:57:02'
authors:
- fagnerbrack
topics:
- formal-verification
- ai-generated-code
- lean-theorem-proving
- code-intelligence
- software-foundation-models
- verified-software
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# When AI Writes the Software, Who Verifies It?

## Summary
The article argues that AI-generated software needs machine-checked proofs because review and testing cannot keep pace with code generation. It proposes Lean as the main platform and cites early AI-assisted verification results on zlib, distributed protocols, and mathematics.

## Problem
- AI is generating a large share of new code: Google and Microsoft report 25–30% AI-generated new code, AWS used AI to modernize 40 million lines of COBOL for Toyota, and Microsoft’s CTO predicts 95% AI-generated code by 2030.
- Human review weakens when models produce code that looks plausible. The article cites Karpathy’s “Accept All” pattern and says nearly half of AI-generated code fails basic security tests.
- Testing and review missed bugs such as Heartbleed for years. At AI code-generation speed, similar defects and supply-chain attacks can spread through critical infrastructure faster than current verification practices can check them.

## Approach
- Use formal specifications to define what correct behavior means before accepting AI-generated code.
- Have AI generate code, proofs, and proof steps in Lean; a small trusted kernel checks every proof mechanically.
- Keep the verifier independent from the AI generator, so trust rests on the proof checker rather than the model or vendor.
- Use simple, obviously correct models as specifications when possible. The AI then writes a faster implementation and proves that both versions behave the same.
- Use Lean’s tactic feedback, Mathlib, and domain-specific extensions so AI agents can build proofs step by step instead of relying only on black-box solver results.

## Results
- Anthropic reportedly built a 100,000-line C compiler with parallel AI agents in two weeks for under $20,000; it boots Linux and compiles SQLite, PostgreSQL, Redis, and Lua, but the article says it is not formally verified.
- A Claude-based experiment converted zlib, including DEFLATE, to Lean with minimal human guidance and no special theorem-proving tooling. The claimed theorem proves `decompressSingle (compress data level) = .ok data` for every compression level, with a `data.size < 1024 * 1024 * 1024` precondition.
- Lean’s Mathlib is cited as having over 200,000 formalized theorems and 750 contributors.
- Lean adoption claims include over 8,000 GitHub repositories, over 200,000 programming-environment installs, and more than 700 daily active users in Lean Zulip.
- Veil, a Lean-based distributed protocol verifier, is reported to verify Rabia agreement and validity for any number of nodes and to have found an inconsistency in a prior Rabia verification across two separate tools.
- A single mathematician working with an AI agent formalized the Prime Number Theorem in Lean in three weeks, producing 25,000 lines and over 1,000 theorems; the article says the previous formalization took over a year and dozens of contributors.

## Link
- [https://leodemoura.github.io/blog/2026-2-28-when-ai-writes-the-worlds-software-who-verifies-it/](https://leodemoura.github.io/blog/2026-2-28-when-ai-writes-the-worlds-software-who-verifies-it/)
