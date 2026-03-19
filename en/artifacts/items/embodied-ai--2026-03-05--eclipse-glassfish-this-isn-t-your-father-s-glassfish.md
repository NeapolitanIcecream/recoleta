---
source: hn
url: https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/
published_at: '2026-03-05T23:18:57'
authors:
- henk53
topics:
- java-application-server
- jakarta-ee
- microprofile
- enterprise-java
- glassfish
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Eclipse GlassFish: This Isn't Your Father's GlassFish

## Summary
This is an article introducing the modern evolution of Eclipse GlassFish, with the core aim of refuting the old impression that it is “slow, unsupported, and only suitable for development environments.” The article emphasizes that since GlassFish 7.0, the platform has become an enterprise-grade application server with commercial support, compatibility with modern Java standards, and lightweight deployment capabilities.

## Problem
- The problem the article addresses is that developers and enterprises still view GlassFish, based on experiences with older versions, as an application server that is **unsuitable for production, lacks support, and lags in performance**.
- This matters because such perceptions can prevent organizations from upgrading to or adopting what is actually a mature Java/Jakarta EE platform, affecting production deployment, standards compatibility, and modernization decisions.
- The article also implicitly highlights a comparison issue: the capability gap between old Oracle GlassFish / early Eclipse GlassFish and modern Eclipse GlassFish is often overlooked.

## Approach
- The core mechanism is straightforward: through **version demarcation (especially after 7.0) + a feature list + an explanation of support capabilities**, the author argues that modern Eclipse GlassFish is significantly different from older versions.
- Specific measures include emphasizing that **OmniFish has provided commercial support since 2022**, covering 24×7 support, SLA, supported builds, bug fixes, hot patches, and consulting services, to address doubts that it is “unsupported and unusable in production.”
- The article also uses **standards compliance and platform capability upgrades** as evidence, such as being the first to pass the Jakarta EE 11 Web Profile and Platform TCK, and supporting multiple MicroProfile APIs (Health, Config, REST Client, JWT).
- Another key point is the transformation of **Embedded GlassFish** from more of a development tool into a lightweight, observable, production-ready runtime suitable for command-line microservices and cloud containers.
- It also emphasizes performance and security improvements, including faster startup, better JDBC connection pool throughput, improved resource management, support up to Java 25, a default shift to PKCS12 keystore, and fixes for critical vulnerabilities.

## Results
- The clearest quantifiable time markers in the article are: **since 2022 and with GlassFish 7.0**, the author claims the platform has transformed into a “production-ready, enterprise-grade platform.”
- The article claims Eclipse GlassFish was **the first to pass the Jakarta EE 11 Web Profile and Jakarta EE 11 Platform TCK**, which is one of its strongest technical endorsements, but it **does not provide specific test scores, durations, or numerical comparisons with other servers**.
- In terms of support capabilities, it specifies clear service offerings: **24×7 support**, strict **SLA**, secure tested builds, bug fixes, hot patches, and expert consulting, but it does not disclose customer counts, recovery times, or support benchmark data.
- On compatibility, the article explicitly states support for **up to Java 25**, and support for multiple MicroProfile APIs; this is concrete progress at the version level.
- In terms of performance, the author claims **faster startup times, improved JDBC pool throughput, and better resource management**, but the excerpt **does not provide any benchmark figures, datasets, baselines, or percentage improvements**.
- Therefore, the article’s “breakthrough results” are mainly **a change in platform positioning and ecosystem maturity**, rather than strict paper-style experimental results.

## Link
- [https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/](https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/)
