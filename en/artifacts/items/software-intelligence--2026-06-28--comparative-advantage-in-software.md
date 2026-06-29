---
source: hn
url: https://achad4.substack.com/p/comparative-advantage-in-software
published_at: '2026-06-28T22:19:35'
authors:
- achad4
topics:
- ai-software-products
- coding-agents
- llm-applications
- product-strategy
- agent-workflows
- restaurant-erp
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Comparative Advantage in Software

## Summary
The essay argues that AI-generated code makes software valuable only when a product reduces token cost or raises task correctness better than a customer can do with a general model. It is a business and product strategy piece, with Kintow restaurant operations examples rather than experimental research.

## Problem
- Coding agents lower the cost of building software, so buyers need a clearer reason to pay for products they might recreate with Claude or another LLM.
- Thin AI wrappers can lose value when they add little beyond model calls.
- Complex operational software still matters when it maintains state, enforces workflows, and prevents errors that would cost users time or money.

## Approach
- The method is a cost model: compare a product with direct LLM use by asking how many tokens the task takes and how correct those tokens are.
- Products create value by reducing the amount of model reasoning needed through workflows, domain models, typed data, and deterministic steps.
- Products also create value by improving correctness through context engineering, evaluations, persistent state, and error-correcting workflows.
- Kintow applies this to restaurant ERP tasks such as inventory, waste, recipes, labor, automated procurement, and invoice parsing.

## Results
- The excerpt reports no experiments, datasets, baselines, or accuracy metrics.
- It claims 2 product levers: lower the number of tokens needed for a task and increase the correctness of each token produced.
- Automated procurement needs precise state and approval controls because purchasing can affect about 30% of a restaurant’s revenue.
- Invoice parsing works on a single document with Claude, but repeated runs can vary and fail to sync with a catalog; the claimed fix is evaluations, context engineering, and correction workflows.
- The strongest concrete claim is that customers with spreadsheets, incumbent tools, or home-built systems may still buy specialized software when maintenance and reliability costs exceed the cost of the product.

## Link
- [https://achad4.substack.com/p/comparative-advantage-in-software](https://achad4.substack.com/p/comparative-advantage-in-software)
