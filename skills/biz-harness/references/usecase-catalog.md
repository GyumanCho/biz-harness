# Business Use Case Catalog

Standard use case templates organized by domain. Each template provides a
starting point — customize steps, actors, and outcomes for your specific context.

## How to Use This Catalog

1. Identify your domain (or closest match)
2. Review candidate use cases
3. Select 1-5 use cases for your harness
4. Customize actors, steps, and outcomes as needed

---

## Domain: SaaS Product

### UC-SAAS-01: User Onboarding Automation

```yaml
id: UC-SAAS-01
name: User Onboarding Automation
domain: SaaS Product
business_goal: "Increase new user activation rate within first 7 days"
actors: [New User, System, CS Team]
steps:
  - trigger: "User completes signup"
  - action: "Analyze user profile and intent"
  - action: "Generate personalized onboarding guide"
  - action: "Deliver step-by-step tutorials"
  - action: "Check activation at day 3 — trigger retention action if inactive"
  - outcome: "User engages core feature at least once within 7 days"
recommended_pattern: Pipeline
agent_roles: [Profile-Analyzer, Guide-Generator, Tutorial-Deliverer, Activation-Tracker]
qa_criteria:
  - "All steps execute sequentially without gaps"
  - "Inactive user detection accuracy"
  - "Generated guide is domain-appropriate"
```

### UC-SAAS-02: Subscription & Billing Management

```yaml
id: UC-SAAS-02
name: Subscription & Billing Management
domain: SaaS Product
business_goal: "Reduce involuntary churn from billing failures"
actors: [Subscriber, Payment Gateway, Finance Team]
steps:
  - trigger: "Subscription renewal date approaches"
  - action: "Validate payment method status"
  - action: "Process renewal charge"
  - action: "Handle failure — retry with backoff, notify user"
  - action: "Escalate persistent failures to finance team"
  - outcome: "95%+ successful renewal rate"
recommended_pattern: Pipeline
agent_roles: [Payment-Validator, Charge-Processor, Retry-Handler, Escalation-Agent]
qa_criteria:
  - "Payment validation catches expired methods before charge"
  - "Retry logic follows correct backoff schedule"
  - "Escalation triggers at correct threshold"
```

### UC-SAAS-03: Customer Support Ticket Processing

```yaml
id: UC-SAAS-03
name: Customer Support Ticket Processing
domain: SaaS Product
business_goal: "Resolve 60% of tickets without human intervention"
actors: [Customer, Support System, Support Agent]
steps:
  - trigger: "Customer submits support ticket"
  - action: "Classify ticket category and urgency"
  - action: "Search knowledge base for matching solutions"
  - action: "Generate response draft"
  - action: "Route to human agent if confidence < threshold"
  - outcome: "Response within 5 minutes, 60% auto-resolution rate"
recommended_pattern: Fan-out/Fan-in
agent_roles: [Ticket-Classifier, KB-Searcher, Response-Generator, Router]
qa_criteria:
  - "Classification accuracy across ticket types"
  - "KB search relevance score"
  - "Human routing triggers at correct confidence threshold"
```

### UC-SAAS-04: Product Analytics Report Generation

```yaml
id: UC-SAAS-04
name: Product Analytics Report Generation
domain: SaaS Product
business_goal: "Deliver actionable weekly product insights to stakeholders"
actors: [Data Source, Product Team, Stakeholders]
steps:
  - trigger: "Weekly schedule or on-demand request"
  - action: "Collect metrics from data sources"
  - action: "Analyze trends, anomalies, and correlations"
  - action: "Generate narrative report with visualizations"
  - action: "Distribute to stakeholders via configured channels"
  - outcome: "Stakeholders receive report with 3+ actionable insights"
recommended_pattern: Pipeline
agent_roles: [Data-Collector, Trend-Analyzer, Report-Writer, Distributor]
qa_criteria:
  - "All required metrics are collected"
  - "Anomaly detection sensitivity"
  - "Report readability and actionability"
```

---

## Domain: E-Commerce

### UC-ECOM-01: Product Listing Pipeline

```yaml
id: UC-ECOM-01
name: Product Listing Pipeline
domain: E-Commerce
business_goal: "Reduce product listing time from hours to minutes"
actors: [Seller, Product Catalog, QA Reviewer]
steps:
  - trigger: "Seller uploads raw product data"
  - action: "Validate and normalize product attributes"
  - action: "Generate optimized title, description, and tags"
  - action: "Auto-categorize into taxonomy"
  - action: "Quality check — flag issues for review"
  - outcome: "Listing published in < 10 minutes with 95% accuracy"
recommended_pattern: Pipeline
agent_roles: [Data-Normalizer, Content-Generator, Categorizer, QA-Checker]
qa_criteria:
  - "Attribute validation catches all required fields"
  - "Generated content meets SEO standards"
  - "Category accuracy across product types"
```

### UC-ECOM-02: Order Fulfillment & Tracking

```yaml
id: UC-ECOM-02
name: Order Fulfillment & Tracking
domain: E-Commerce
business_goal: "Achieve 99% order accuracy and real-time tracking visibility"
actors: [Customer, Warehouse, Shipping Carrier]
steps:
  - trigger: "Order placed and payment confirmed"
  - action: "Verify inventory availability"
  - action: "Generate pick/pack instructions"
  - action: "Assign shipping carrier and generate label"
  - action: "Track shipment and update customer"
  - outcome: "Customer receives accurate delivery ETA, 99% order accuracy"
recommended_pattern: Pipeline
agent_roles: [Inventory-Checker, Fulfillment-Planner, Shipping-Coordinator, Tracking-Updater]
qa_criteria:
  - "Inventory sync accuracy"
  - "Carrier selection optimality (cost vs speed)"
  - "Tracking update timeliness"
```

### UC-ECOM-03: Customer Review Analysis & Response

```yaml
id: UC-ECOM-03
name: Customer Review Analysis & Response
domain: E-Commerce
business_goal: "Respond to all reviews within 24h, extract product improvement signals"
actors: [Customer, Product Team, CS Team]
steps:
  - trigger: "New customer review posted"
  - action: "Analyze sentiment and extract key themes"
  - action: "Classify as praise, complaint, question, or suggestion"
  - action: "Generate appropriate response draft"
  - action: "Aggregate insights for product team weekly digest"
  - outcome: "100% review response rate, weekly insight report"
recommended_pattern: Fan-out/Fan-in
agent_roles: [Sentiment-Analyzer, Classifier, Response-Drafter, Insight-Aggregator]
qa_criteria:
  - "Sentiment analysis accuracy"
  - "Response tone appropriateness"
  - "Insight extraction relevance"
```

### UC-ECOM-04: Promotion Campaign Execution

```yaml
id: UC-ECOM-04
name: Promotion Campaign Execution
domain: E-Commerce
business_goal: "Execute targeted promotions that increase conversion by 15%+"
actors: [Marketing Team, Customer Segments, Analytics]
steps:
  - trigger: "Campaign brief submitted by marketing team"
  - action: "Segment target audience based on criteria"
  - action: "Generate personalized campaign content"
  - action: "Schedule and deploy across channels"
  - action: "Monitor performance and auto-optimize"
  - outcome: "Campaign delivered to target segments with real-time optimization"
recommended_pattern: Pipeline
agent_roles: [Audience-Segmenter, Content-Creator, Campaign-Deployer, Performance-Monitor]
qa_criteria:
  - "Segmentation precision"
  - "Content personalization quality"
  - "Real-time optimization responsiveness"
```

---

## Domain: Fintech

### UC-FIN-01: KYC/AML Screening Automation

```yaml
id: UC-FIN-01
name: KYC/AML Screening Automation
domain: Fintech
business_goal: "Complete customer verification in < 5 minutes with 99.5% compliance"
actors: [Applicant, Compliance System, Compliance Officer]
steps:
  - trigger: "New customer application submitted"
  - action: "Extract and validate identity documents"
  - action: "Screen against sanctions and PEP lists"
  - action: "Calculate risk score"
  - action: "Auto-approve low-risk, escalate high-risk to officer"
  - outcome: "Verified customer onboarded or flagged for manual review"
recommended_pattern: Pipeline
agent_roles: [Document-Extractor, Screening-Agent, Risk-Scorer, Decision-Router]
qa_criteria:
  - "Document extraction accuracy"
  - "Sanctions list matching precision/recall"
  - "Risk score calibration"
```

### UC-FIN-02: Transaction Monitoring & Anomaly Detection

```yaml
id: UC-FIN-02
name: Transaction Monitoring & Anomaly Detection
domain: Fintech
business_goal: "Detect suspicious transactions in real-time with < 1% false positive rate"
actors: [Customer, Transaction System, Fraud Team]
steps:
  - trigger: "Transaction initiated"
  - action: "Evaluate against customer behavior profile"
  - action: "Run rule-based and pattern-based anomaly checks"
  - action: "Score transaction risk"
  - action: "Block/flag high-risk, alert fraud team"
  - outcome: "Suspicious transactions caught in real-time"
recommended_pattern: Fan-out/Fan-in
agent_roles: [Profile-Matcher, Rule-Engine, Pattern-Detector, Alert-Manager]
qa_criteria:
  - "Detection sensitivity vs false positive balance"
  - "Alert routing accuracy"
  - "Response latency"
```

### UC-FIN-03: Regulatory Report Generation

```yaml
id: UC-FIN-03
name: Regulatory Report Generation
domain: Fintech
business_goal: "Generate compliant regulatory reports with zero manual intervention"
actors: [Data Systems, Compliance Team, Regulator]
steps:
  - trigger: "Reporting period closes or ad-hoc request"
  - action: "Aggregate data from required sources"
  - action: "Apply regulatory formatting rules"
  - action: "Validate completeness and accuracy"
  - action: "Generate report and submit for review"
  - outcome: "Compliant report ready for filing"
recommended_pattern: Pipeline
agent_roles: [Data-Aggregator, Format-Applier, Compliance-Validator, Report-Assembler]
qa_criteria:
  - "Data completeness across all required fields"
  - "Format compliance with regulatory specifications"
  - "Validation catch rate for errors"
```

### UC-FIN-04: Portfolio Analysis & Advisory

```yaml
id: UC-FIN-04
name: Portfolio Analysis & Advisory
domain: Fintech
business_goal: "Provide personalized investment insights to improve portfolio returns"
actors: [Customer, Market Data, Advisory Team]
steps:
  - trigger: "Customer requests portfolio review or scheduled analysis"
  - action: "Collect current portfolio holdings and market data"
  - action: "Analyze risk exposure and diversification"
  - action: "Generate rebalancing recommendations"
  - action: "Present insights with rationale to customer"
  - outcome: "Customer receives actionable portfolio advice"
recommended_pattern: Expert Pool
agent_roles: [Data-Fetcher, Risk-Analyzer, Rebalance-Advisor, Report-Presenter]
qa_criteria:
  - "Market data freshness"
  - "Risk calculation accuracy"
  - "Recommendation suitability for customer profile"
```

---

## Domain: Content & Media

### UC-MEDIA-01: Content Production Pipeline

```yaml
id: UC-MEDIA-01
name: Content Production Pipeline
domain: Content & Media
business_goal: "Produce 3x more content with consistent quality"
actors: [Content Team, Editor, Publisher]
steps:
  - trigger: "Content brief submitted"
  - action: "Research topic and gather source materials"
  - action: "Generate draft content"
  - action: "Edit for style, accuracy, and brand voice"
  - action: "Prepare for publishing (format, metadata, assets)"
  - outcome: "Publish-ready content in half the time"
recommended_pattern: Pipeline
agent_roles: [Researcher, Draft-Writer, Editor, Publisher-Prep]
qa_criteria:
  - "Research depth and source quality"
  - "Draft adherence to content brief"
  - "Brand voice consistency"
```

### UC-MEDIA-02: Multi-Channel Distribution

```yaml
id: UC-MEDIA-02
name: Multi-Channel Distribution
domain: Content & Media
business_goal: "Distribute content to all channels simultaneously with platform optimization"
actors: [Content, Platform APIs, Analytics]
steps:
  - trigger: "Content approved for publishing"
  - action: "Adapt content format for each platform"
  - action: "Optimize metadata (titles, descriptions, tags) per platform"
  - action: "Schedule and publish across channels"
  - action: "Monitor initial performance metrics"
  - outcome: "Content live on all platforms within 1 hour"
recommended_pattern: Fan-out/Fan-in
agent_roles: [Format-Adapter, SEO-Optimizer, Scheduler, Performance-Watcher]
qa_criteria:
  - "Platform-specific format compliance"
  - "Metadata optimization quality"
  - "Publishing timing accuracy"
```

### UC-MEDIA-03: Performance Analysis & Optimization

```yaml
id: UC-MEDIA-03
name: Performance Analysis & Optimization
domain: Content & Media
business_goal: "Increase content engagement by 20% through data-driven optimization"
actors: [Analytics Platforms, Content Team, Strategy Team]
steps:
  - trigger: "Weekly analysis cycle or performance threshold breach"
  - action: "Collect engagement metrics across platforms"
  - action: "Identify top/bottom performers and patterns"
  - action: "Generate optimization recommendations"
  - action: "Apply A/B test suggestions for next content cycle"
  - outcome: "Actionable optimization playbook updated weekly"
recommended_pattern: Pipeline
agent_roles: [Metrics-Collector, Pattern-Analyzer, Optimization-Advisor, Test-Planner]
qa_criteria:
  - "Metric collection completeness"
  - "Pattern identification accuracy"
  - "Recommendation actionability"
```

### UC-MEDIA-04: Copyright & Compliance Review

```yaml
id: UC-MEDIA-04
name: Copyright & Compliance Review
domain: Content & Media
business_goal: "Zero copyright violations, 100% compliance with content policies"
actors: [Content, Legal Team, Compliance Database]
steps:
  - trigger: "Content enters review stage"
  - action: "Scan for potential copyright issues (text, images, music)"
  - action: "Check against content policies and guidelines"
  - action: "Flag issues with specific locations and severity"
  - action: "Suggest compliant alternatives where possible"
  - outcome: "Content cleared for publishing or issues resolved"
recommended_pattern: Producer-Reviewer
agent_roles: [Copyright-Scanner, Policy-Checker, Issue-Flagger, Alternative-Suggester]
qa_criteria:
  - "Copyright detection sensitivity"
  - "Policy rule coverage"
  - "Alternative suggestion quality"
```

---

## Domain: DevTools & Platform

### UC-DEV-01: CI/CD Pipeline Management

```yaml
id: UC-DEV-01
name: CI/CD Pipeline Management
domain: DevTools & Platform
business_goal: "Reduce deployment failures by 80% with intelligent pipeline management"
actors: [Developer, CI System, Infrastructure]
steps:
  - trigger: "Code pushed to main branch or PR merged"
  - action: "Analyze changes and determine affected services"
  - action: "Run targeted test suites"
  - action: "Validate deployment prerequisites"
  - action: "Execute staged rollout with monitoring"
  - outcome: "Zero-downtime deployment with automatic rollback on failure"
recommended_pattern: Pipeline
agent_roles: [Change-Analyzer, Test-Runner, Deploy-Validator, Rollout-Manager]
qa_criteria:
  - "Change impact analysis accuracy"
  - "Test selection relevance"
  - "Rollback trigger reliability"
```

### UC-DEV-02: Incident Response Automation

```yaml
id: UC-DEV-02
name: Incident Response Automation
domain: DevTools & Platform
business_goal: "Reduce MTTR by 50% through automated triage and response"
actors: [Monitoring System, On-Call Engineer, Stakeholders]
steps:
  - trigger: "Alert fired from monitoring system"
  - action: "Correlate alert with recent changes and known issues"
  - action: "Assess severity and blast radius"
  - action: "Execute automated remediation for known patterns"
  - action: "Escalate and notify stakeholders for unknown issues"
  - outcome: "Incident triaged in < 2 minutes, known issues auto-resolved"
recommended_pattern: Fan-out/Fan-in
agent_roles: [Alert-Correlator, Severity-Assessor, Auto-Remediator, Escalation-Agent]
qa_criteria:
  - "Alert correlation accuracy"
  - "Severity assessment reliability"
  - "Remediation success rate for known patterns"
```

### UC-DEV-03: Code Review & Quality Gate

```yaml
id: UC-DEV-03
name: Code Review & Quality Gate
domain: DevTools & Platform
business_goal: "Catch 90% of defects before human review, reduce review time by 60%"
actors: [Developer, Reviewer, CI System]
steps:
  - trigger: "Pull request opened"
  - action: "Analyze code changes for patterns, security, and style"
  - action: "Run automated quality checks"
  - action: "Generate review summary with prioritized findings"
  - action: "Suggest fixes for critical issues"
  - outcome: "PR arrives at human reviewer pre-screened with actionable feedback"
recommended_pattern: Fan-out/Fan-in
agent_roles: [Pattern-Analyzer, Security-Scanner, Style-Checker, Review-Synthesizer]
qa_criteria:
  - "Defect detection precision/recall"
  - "False positive rate"
  - "Fix suggestion applicability"
```

### UC-DEV-04: Documentation Auto-Generation

```yaml
id: UC-DEV-04
name: Documentation Auto-Generation
domain: DevTools & Platform
business_goal: "Keep documentation in sync with code, eliminate doc-debt"
actors: [Codebase, Technical Writer, Developer]
steps:
  - trigger: "Code change merged or documentation review scheduled"
  - action: "Detect documentation gaps from code changes"
  - action: "Generate or update documentation drafts"
  - action: "Validate accuracy against current codebase"
  - action: "Submit for review with change context"
  - outcome: "Documentation stays within 1 sprint of code changes"
recommended_pattern: Pipeline
agent_roles: [Gap-Detector, Doc-Generator, Accuracy-Validator, Review-Submitter]
qa_criteria:
  - "Gap detection completeness"
  - "Generated doc accuracy"
  - "Technical language appropriateness"
```

---

## Custom Domain Template

For domains not covered above, use this template:

```yaml
id: UC-CUSTOM-01
name: "{Use Case Name}"
domain: "{Your Domain}"
business_goal: "{Measurable business outcome}"
actors: [Actor1, Actor2, ...]
steps:
  - trigger: "{What initiates this use case}"
  - action: "{Step 1}"
  - action: "{Step 2}"
  - action: "{Step N}"
  - outcome: "{Observable success criteria}"
recommended_pattern: "{Pipeline | Fan-out/Fan-in | Expert Pool | Producer-Reviewer | Supervisor | Hierarchical}"
agent_roles: [Role1, Role2, ...]
qa_criteria:
  - "{Criterion 1}"
  - "{Criterion 2}"
  - "{Criterion 3}"
```
