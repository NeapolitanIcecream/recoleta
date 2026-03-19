---
source: hn
url: https://github.com/azaddjan/aipatternmanager
published_at: '2026-03-02T23:21:13'
authors:
- azaddjan
topics:
- enterprise-architecture
- neo4j
- architecture-patterns
- llm-tooling
- knowledge-graph
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# AI Architecture Pattern Manager – Togaf ABB/SBB/PBC with Neo4J

## Summary
This is a pattern management platform for enterprise AI architecture governance that combines TOGAF's ABB/SBB with Gartner's PBC into a Neo4j-based visual and analyzable catalog. It primarily addresses cross-abstraction-layer pattern modeling, relationship tracking, AI-assisted completion, and the export of governance artifacts.

## Problem
- Enterprise AI architecture patterns are often scattered across documents, whiteboards, and team experience, making it difficult to manage multiple layers of abstraction uniformly, from enterprise blueprints to vendor implementations.
- There is a lack of visualization, traceability, and change impact analysis for relationships among ABB, SBB, PBC, and technology products, resulting in low efficiency in architecture governance and reuse.
- Purely manual maintenance of a pattern library is costly, and it is also difficult to discover missing patterns, content quality issues, and capability coverage gaps, which affects the consistency and delivery speed of enterprise AI system design.

## Approach
- Use a graph-database-driven platform to centrally manage multi-layer objects: Architecture Blueprints, ABB, SBB, PBC, and Technologies, and explicitly model the relationships among them.
- Provide structured Pattern CRUD to store typed fields such as intent, problem, solution, interfaces, and invariants for each pattern, forming a governable pattern catalog.
- On the frontend, use interactive graph browsing, search, filtering, and double-click navigation to inspect cross-layer dependencies; on the backend, combine Neo4j queries with health scoring to evaluate completeness, relationships, coverage, and problems.
- Integrate multiple LLM providers (Anthropic, OpenAI, AWS Bedrock, Ollama) for AI authoring, missing-pattern discovery, single-pattern advising, and full-library deep semantic analysis across 9 dimensions.
- Support RBAC/JWT, team ownership, import/restore, and multi-format export to HTML/PPTX/DOCX/JSON, making it both a knowledge base and an enterprise architecture governance workbench.

## Results
- The text does not provide quantitative experimental results based on public datasets or standard benchmarks, so there are **no academically verifiable performance figures**.
- It explicitly claims support for **5 core architecture layers/entities**: AB, ABB, SBB, PBC, and Technologies, covering multiple categories such as Core AI/LLM, Integration, Agents, and Knowledge & Retrieval.
- The platform provides **4 health-scoring dimensions**: Completeness, Relationships, Coverage, and Problems, and generates a weighted overall score, drill-down, and trend tracking, but does not provide numeric results demonstrating the effectiveness of the scoring formula.
- AI deep analysis covers **9 analysis areas**, including architecture coherence, ABB↔SBB alignment, interface consistency, business capability gaps, vendor risk, content quality, pattern overlap, PBC composition, and a maturity roadmap.
- The export capability gives relatively specific output specifications: **30-slide PowerPoint**, self-contained HTML for offline viewing, structured Word documents, and full JSON backup/restore.
- At the engineering level, it provides directly runnable Docker image versions **backend:0.9.0** and **frontend:0.9.0**, and claims that the first launch automatically creates constraints, indexes, built-in categories, and an administrator account.

## Link
- [https://github.com/azaddjan/aipatternmanager](https://github.com/azaddjan/aipatternmanager)
