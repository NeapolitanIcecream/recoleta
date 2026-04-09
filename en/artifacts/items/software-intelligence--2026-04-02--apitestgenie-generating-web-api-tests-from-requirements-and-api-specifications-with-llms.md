---
source: arxiv
url: http://arxiv.org/abs/2604.02039v1
published_at: '2026-04-02T13:43:56'
authors:
- "Andr\xE9 Pereira"
- Bruno Lima
- "Jo\xE3o Pascoal Faria"
topics:
- llm-test-generation
- api-testing
- openapi
- requirements-to-code
- retrieval-augmented-generation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# APITestGenie: Generating Web API Tests from Requirements and API Specifications with LLMs

## Summary
APITestGenie generates executable web API integration tests from natural-language business requirements plus OpenAPI specs. The paper shows that this requirement-driven setup can produce valid tests for most evaluated requirements, including large industrial APIs.

## Problem
- Writing API integration and acceptance tests is still manual, slow, and error-prone, especially when expected behavior is described in business requirements rather than low-level API calls.
- Existing API test tools often work from OpenAPI alone, so they miss requirement context and struggle to generate tests that check business behavior across multiple endpoints.
- This matters for modern systems that depend on many APIs and need tests that keep up with frequent changes and deployments.

## Approach
- APITestGenie takes two inputs: a business requirement in natural language and the API's OpenAPI specification, then asks an LLM to generate ready-to-run TypeScript tests using Axios and Jest.
- The system uses a structured prompt with task context, output quality criteria, and a required output format that includes requirement interpretation, endpoint selection, and executable test code.
- For large API specs, it preprocesses the OpenAPI file, splits it into chunks, embeds them in a vector database, expands the requirement into related queries, and retrieves the most relevant chunks with RAG.
- The workflow has three modules: test generation, optional test improvement using prior execution feedback, and test execution in a Jest/TypeScript environment.
- The evaluation used GPT-4-Turbo with three generation attempts per business requirement, then executed scripts and manually checked semantic validity.

## Results
- Evaluated on 10 real-world APIs and 25 business requirements, with 75 total generation attempts; 8 of the APIs came from an automotive industry partner and covered about 1,000 live endpoints.
- APITestGenie produced 52 valid test scripts out of 75 attempts, for a 69.3% success rate per attempt.
- 22 of 25 business requirements had at least one valid script within three attempts, for an 88.6% requirement-level success rate; the abstract rounds this to 89%.
- Low-complexity APIs reached 21 valid scripts out of 24 attempts, or 87.5%, and 8 of 8 requirements got at least one valid script. High-complexity APIs reached 31 of 51 attempts, or 60.8%, and 14 of 17 requirements got at least one valid script.
- Average generation time was 126 seconds and average cost was €0.37 per generation.
- Among the 52 valid scripts, 31 passed, 12 exposed API defects, 2 failed due to insufficient documentation, and 7 failed because of environment setup issues. The paper states that some generated tests found previously unknown defects, including cross-endpoint integration issues.

## Link
- [http://arxiv.org/abs/2604.02039v1](http://arxiv.org/abs/2604.02039v1)
