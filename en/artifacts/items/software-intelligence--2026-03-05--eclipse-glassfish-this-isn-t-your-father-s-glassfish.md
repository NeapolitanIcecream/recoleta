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
- cloud-runtime
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# Eclipse GlassFish: This Isn't Your Father's GlassFish

## Summary
This article is not an academic paper, but a product/technology promotional piece. Its core purpose is to correct the old impression that “GlassFish is outdated, slow, and only suitable for development environments,” emphasizing that Eclipse GlassFish after 7.0 has become a production-deployable, continuously evolving enterprise-grade Java application server.

## Problem
- The problem it aims to solve is that developers and enterprises still apply negative perceptions of Oracle GlassFish / early Eclipse GlassFish versions to modern Eclipse GlassFish.
- This matters because that perception can prevent teams from adopting a Java platform that already supports new Jakarta EE, microservice deployment, and commercial support.
- The article explicitly addresses doubts such as “not suitable for production, lacking support, insufficient performance and security, and outdated for modern lightweight deployment.”

## Approach
- The core mechanism is simple: by comparing older versions with Eclipse GlassFish after 7.0+, it explains the platform’s modernization in support model, standards compatibility, embedded runtime, performance, and security.
- It emphasizes commercial support capabilities: since 2022, OmniFish has provided 24×7 support, SLAs, supported builds, patches, security fixes, and consulting services, turning a “community project” into an “enterprise-ready platform.”
- It highlights standards and ecosystem updates: claiming to be the first to pass the Jakarta EE 11 Web Profile and Platform TCKs, and to add support for APIs such as MicroProfile Health, Config, REST Client, and JWT.
- It highlights runtime-form upgrades: transforming Embedded GlassFish from a development tool into a lightweight, observable production runtime suitable for command-line microservices and cloud containers, with JMX monitoring support.
- It highlights engineering improvements: support up to Java 25, default adoption of PKCS12 keystore, and continued improvements in startup speed, JDBC connection pool throughput, and resource management.

## Results
- The clearest timeline stated in the article is **since 2022 and GlassFish 7.0**, when its positioning shifted from “non-production” to a “production-ready, enterprise-grade platform.”
- It claims to have **been the first to pass the Jakarta EE 11 Web Profile TCK and Jakarta EE 11 Platform TCK**; however, it provides no specific test scores, timing, or numerical comparisons with other servers.
- It claims support for multiple **MicroProfile APIs**—Health, Config, REST Client, JWT—for building microservices; no coverage or performance data is provided.
- It claims performance improvements such as **faster startup time, higher JDBC pool throughput, and better resource management**, and support for **up to Java 25**; however, it provides no benchmark figures, datasets, or baseline comparisons.
- On security, it claims a default switch to **PKCS12 keystore** and fixes for critical vulnerabilities; it does not list CVE IDs, number of fixes, or compliance metrics.
- Overall, the article’s main “breakthrough results” are product capability and standards-certification claims, while **reproducible quantitative experimental results are lacking**.

## Link
- [https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/](https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/)
