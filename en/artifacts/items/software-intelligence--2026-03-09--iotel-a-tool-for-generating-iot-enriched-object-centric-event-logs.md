---
source: arxiv
url: http://arxiv.org/abs/2603.07906v1
published_at: '2026-03-09T02:59:22'
authors:
- Jia Wei
- Xin Su
- Chun Ouyang
topics:
- process-mining
- internet-of-things
- event-logs
- object-centric-process-mining
- data-integration
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# IOTEL: A Tool for Generating IoT-enriched Object-Centric Event Logs

## Summary
This paper presents IOTEL, a semi-automatic tool for systematically integrating process-relevant IoT data into object-centric event logs (OCEL). Its goal is to enable analysis of IoT-enhanced processes while directly reusing existing OCEL and process mining toolchains, without introducing proprietary log schemas.

## Problem
- To analyze IoT-enhanced business processes, low-level sensor/actuator data must be combined with high-level business event logs, but this is difficult because they differ in abstraction level and come from separate data sources.
- If raw IoT data is inserted directly into event logs, the log size and semantic complexity increase significantly, and substantial preprocessing is still required afterward, reducing usability for process analysis.
- Existing tools either focus on extracting event logs from sensor streams or rely on specific proprietary schemas (such as CORE), lacking a general-purpose tool for integrating “process-relevant IoT data” into existing OCEL logs.

## Approach
- IOTEL uses **OCEL 2.0** as the target log schema and adds IoT data as object attributes or event attributes without changing the basic OCEL structure, thereby remaining compatible with existing process mining tools.
- The tool first performs **pre-integration filtering**: it derives a smaller sub-schema from SOSA/SSN, retaining only concepts useful for process analysis and avoiding importing all raw IoT semantics and data volume into the log at once.
- It provides three core functions: IoT data processing, OCEL log exploration, and IoT-OCEL integration; users can configure device types, interaction patterns, attribute mappings, relationship qualifiers, and aggregation/filtering strategies (such as min/max/avg/median).
- The central mechanism is simple: it first determines whether an IoT device describes “a specific activity” or “a business object,” and then writes the corresponding data as an **event attribute** or an **object attribute**; for data with continuous effects or effects spanning objects, domain knowledge is used to determine the attachment point.
- In terms of system implementation, it uses DuckDB + Parquet for intermediate analysis and processing, ultimately writing to an OCEL 2.0-compliant SQLite database, and adopts non-destructive incremental extension to store newly added IoT attributes and relationships.

## Results
- The paper’s main contribution is a **tool and prototype implementation**, not a paper on algorithmic accuracy improvements; it **does not report quantitative comparison results such as performance, accuracy, F1, or benchmarks against baseline methods**.
- To validate the applicability of the sub-schema, the authors analyzed and mapped **69** public IoT datasets, claiming that the core semantics of these datasets can all be represented consistently by their derived schema.
- The tool implements **3** core functional modules: IoT data processing, OCEL log exploration, and IoT data integration, and provides an interactive GUI prototype along with GitHub and demo video resources.
- In a real industrial scenario, the authors applied IOTEL to a port freight pickup process, integrating **GPS** and **weight sensor** data with OCEL logs from the port management system to support analysis of anomalous weight manipulation/fraud; however, the paper does not provide quantified benefits such as improved detection rate or reduced analysis time.
- Compared with approaches that rely on proprietary schemas, IOTEL’s strongest concrete claim is that it performs structured IoT enrichment directly based on **OCEL**, reducing the need for custom data pipelines and improving compatibility with existing object-centric process mining tools.

## Link
- [http://arxiv.org/abs/2603.07906v1](http://arxiv.org/abs/2603.07906v1)
