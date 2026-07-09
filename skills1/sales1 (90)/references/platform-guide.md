# Celigo Platform Reference

## Platform overview

Celigo is a mid-market iPaaS (Integration Platform-as-a-Service) that unifies data, applications, and AI workflows. Named 2025 Gartner Customers' Choice for iPaaS. Positioned as the simpler, faster, more affordable alternative to MuleSoft/Boomi/Workato, with particular depth in NetSuite integrations. Target audience: mid-market organizations with 10-50 SaaS apps seeking faster time-to-value than enterprise iPaaS platforms. Strong in ecommerce, finance, and NetSuite-centric companies.

## Key modules

### Integration Marketplace
- 1,000+ pre-built connectors for popular business systems
- **Integration Apps**: fully managed, end-to-end solutions bundling multiple flows, mappings, and configs into one package (e.g., Shopify-NetSuite Integration App)
- **Integration Templates**: pre-built workflows with predefined data flows and mappings — ready-to-use but customizable
- **Universal Connectors**: for REST/SOAP APIs not in the marketplace — connect any API-accessible system

### AI-Powered Error Management
- ML + NLP + automation to classify, analyze, and resolve errors
- Claims 95% auto-resolution rate for integration errors
- Automatic resolution of duplicate errors and retries for transient issues
- Error classification: transient (timeouts, rate limits → auto-retry) vs persistent (bad data, wrong mapping → manual fix)
- Error investigation tools: Errors page, request/response details, AFE (Adaptive Flow Engine) input replay, debug logs

### API Management (APIM)
- Build, publish, and secure APIs from the APIM console
- Create and manage API plans, applications, and subscriptions
- Centralized API governance and access control
- Share data securely across business units, customers, partners

### B2B Manager for EDI
- Trading partner management and document exchange
- Standard formats: X12, EDIFACT, and others
- Automated document processing and validation

### OEM & Embedded Integrations
- White-label integration solutions
- Embed Celigo's integration capabilities into your SaaS product
- End users get pre-built integrations without seeing Celigo's UI

### Celigo Private Cloud
- Dedicated cloud infrastructure deployment
- Enterprise security and compliance requirements
- Isolated environment for sensitive data

### Celigo Ora, Agent Builder & MCP Server (Agentic Automation)
Launched 31 Mar 2026. Available across all platform editions, free until June 2026.
- **Celigo Ora**: conversational natural-language AI copilot with direct access to the whole platform — design integrations, troubleshoot errors, and manage operations in plain language. Powered by a network of specialized agents with full business context; built-in governance with human-in-the-loop approvals and full auditability. **Beta** at launch. Also provides AI-powered error analysis directly from the Errors page (plain-language explanations + recommended next steps).
- **Agent Builder**: low-code environment for building AI-driven automations that reason through tasks and act across systems, with configurable guardrails. **Generally available.**
- **MCP Server**: Celigo's Enterprise Model Context Protocol server — a standard for secure, real-time, auditable AI connectivity to enterprise systems, letting teams run the full spectrum of automation (rules-based logic → adaptive AI agents) on one platform. Supports MCP prompt templates (discover/use prompts, map required inputs/arguments in Celigo). **Generally available.**

## Pricing and limits

Celigo uses **endpoint + flow pricing** — you pay based on the number of connected apps (endpoints) and data flows, NOT per transaction or per record. This means volume spikes don't cause overages (unlike Workato's task-based billing).

Celigo's official pricing page (celigo.com/platform/pricing, re-verified 2026-06-13) lists **three editions** — Standard, Professional, and Enterprise — plus a 30-day unlimited free trial. (Older third-party guides reference Free/Basic/Premium tier names; the current official naming is below.)

| Edition | Endpoints | Key features (per official pricing page) | Support |
|---|---|---|---|
| Standard | Tiered (contact sales) | Performance matched to app API limits; MFA + role-based access controls, optional SSO add-on | Standard SLAs at no extra cost |
| Professional | Tiered (contact sales) | Adds **API Builder** + **Lookup Cache**; SSO included; role-based access with auditability; includes a **sandbox** dev environment | Enhanced support package with SLAs |
| Enterprise | **Unlimited** | Maximum performance; governance, security, and auditability for compliance | Best support package, fastest SLAs |

*Endpoint/flow counts per tier are not published on the official page (contact sales). Dollar amounts below are best-effort from third-party sources (ERPPeers, Vendr, G2) and may be stale — confirm with Celigo. Older third-party estimates: Standard ~$12,800-$25,500/yr, Professional ~$16,500-$50,000/yr, Enterprise $50,000+/yr; average ~$17,000/yr.*

**Key pricing notes**:
- Each connected app = 1 endpoint (not each flow)
- Flows can run on schedules or in real-time
- AI capabilities (Celigo Ora, Agent Builder, MCP Server) available across all editions, free until June 2026
- The 30-day free trial gives unlimited platform access; there is no standing "Free" paid tier on the current pricing page
- Additional implementation and training costs may apply

## Integrations

### Pre-built connectors
Major platforms: Salesforce, Microsoft Dynamics 365, Oracle NetSuite, SAP, Walmart, Amazon, Shopify, Snowflake, Acumatica, HubSpot, and 1,000+ more.

### NetSuite (flagship integration)
- Deepest NetSuite integration of any iPaaS
- Pre-built Integration Apps for Shopify-NetSuite, Salesforce-NetSuite, and more
- NetSuite RESTlet proxying with custom headers (Integrator-NetSuite-ScriptId, Integrator-NetSuite-DeployId)
- Common workflows: order-to-cash, procure-to-pay, inventory sync, financial close

### Zapier / Make
No native Zapier/Make connector. Use webhooks or REST API for bidirectional communication.

## Data model (API)

The Celigo integrator.io API is RESTful, uses JSON, and requires Bearer token authentication.

**Base URLs**:
- North America: `https://api.integrator.io/v1/`
- EU: `https://api.eu.integrator.io/v1/`
- Browser: `https://integrator.io/api/`

**Key resources**:

| Resource | Purpose |
|---|---|
| Connection | Store credentials and auth info for integrated apps |
| Export | Extract data from source applications |
| Import | Insert/update data into destination applications |
| Flow | Compose exports + imports for data movement |
| Integration | Group flows with shared permissions and stats |
| State | Store arbitrary JSON data with custom keys |
| Job | Track flow execution state and final statistics |

**Rate limits**: Leaky bucket — 1,000 token bucket, 300 tokens/sec fill rate, ~1,080,000 requests/hour.

## Solution categories

**By business function**: Commerce & Retail, Customer Support, Data Warehouse & Analytics, Finance, IT, PeopleOps, Product, RevOps, Supply Chain.

**Common workflows**:
- **Order-to-cash**: Shopify/Amazon → NetSuite (orders, inventory, fulfillment)
- **Procure-to-pay**: Procurement → ERP → AP automation
- **Financial close**: Multi-system reconciliation → NetSuite/SAP
- **Employee onboarding**: HRIS → IT provisioning → payroll
- **Customer 360**: CRM + support + billing → unified view
- **3PL fulfillment**: Ecommerce → 3PL → shipping → tracking updates
- **Returns management**: Returns portal → ERP → refund/credit processing

## Competitive positioning

| Factor | Celigo | Workato | Boomi | MuleSoft |
|---|---|---|---|---|
| Pricing model | Endpoints + flows | Task-based | Per-connection | vCore-based |
| Best for | Mid-market, NetSuite-heavy | Business process automation | Hybrid cloud/on-prem | Enterprise API-led |
| Learning curve | Weeks | Weeks | Months | Months-years |
| Connector count | 1,000+ | 1,200+ | 1,000+ | 450+ |
| AI capabilities | Ora copilot, Agent Builder, MCP Server, AI error management | LLM flow generation | AgentStudio | Einstein AI Gateway |
| Surprise costs | Low (no per-transaction) | High (task overages) | Medium (connection creep) | High (vCore sizing) |
| NetSuite depth | Deepest | Good | Good | Limited |
| Target team size | Small IT (2-5 people) | Small-medium IT | Medium-large IT | Large IT (certified devs) |

## Error debugging workflow

1. **Errors page** → expand failed record → check request/response details
2. **AFE input** → copy retry data → replay with visible data to isolate the issue
3. **Debug logs** → enable on HTTP connectors for full API request/response traces
4. **Run console** → check flow execution history, timing, record counts
5. **Dashboard** → high-level view of all flows, error trends, success rates
6. **Diagnostics** → system-level health checks
7. **2026.1.1 enhancement** → connection debug logs now show underlying API calls during connection establishment
