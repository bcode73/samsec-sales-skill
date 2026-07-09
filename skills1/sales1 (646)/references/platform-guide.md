# Verint CX Automation Platform Reference

## Platform overview

The **Verint CX Automation Platform** (verint.com/cx-automation; still marketed as the "Open Platform" / "Open CCaaS Platform" / "open ecosystem") is an enterprise CX automation platform that has pivoted from legacy workforce engagement management to AI-first customer experience automation. AI ARR ($372M, +21.2% YoY) now exceeds legacy ARR ($356M, down 5.6%) for the first time (Q2 FYE26). Total subscription ARR ~$728M. The combined entity is the market leader with 40%+ global WEM market share, serving ~85% of Fortune 500 and managing ~5M agents across 100+ countries.

**Transaction structure (corrected 2026-06-13)**: Thoma Bravo took Verint private in an all-cash transaction at an enterprise value of **$2B** ($20.50/share), announced Aug 25, 2025. Mechanically, **Calabrio acquired Verint — Verint became a wholly owned subsidiary of Calabrio** and was delisted from Nasdaq. The two were then "combined into one company," and on Feb 18, 2026 the combined organization announced it will move forward under a single corporate name: **Verint**. (The skill previously said "Verint acquired Calabrio," which is backwards.)

**Positioning**: Open, modular platform (vs NICE and Genesys suite-based approaches). Emphasizes hybrid cloud deployment, BYOT (Bring Your Own Telephony), and best-of-breed integrations.

**Target**: Large enterprises managing contact center operations across multiple industries — banking, insurance, public sector, retail, telecommunications.

## Da Vinci AI Bots

Verint Da Vinci combines commercial, open-source, and proprietary AI. All bots are powered by the best available AI models for their specific task. The current portfolio (verint.com/open-da-vinci-ai, verint.com/cx-automation) groups several agent-facing bots under the **Agent Copilot Bots** umbrella (real-time, in-call knowledge retrieval, coaching, and post-call wrap-up) and adds newer bots — **Genie Bot**, **PII Redaction Bot**, **Call Risk Scoring Bot**, and **Knowledge Creation Bot** — alongside the established ones below.

### Quality Bot
- Automates quality evaluations across up to 100% of interactions (vs typical 2-5% manual sampling)
- Uses generative AI to automatically write scoring rules for compliance, empathy, process adherence
- Increases supervisor capacity by ~33%
- Reduces supervisor costs

### Coaching Bot
- Real-time, non-disruptive agent guidance during live calls
- Next-best-action suggestions based on interaction context
- Trained on your specific interaction and agent data in the Verint Data Hub
- Gets smarter over time — learns from your organization's top performers
- Reduces call duration, increases sales conversions, boosts retention

### Wrap Up Bot
- Generative AI creates automatic call summaries at interaction end
- Cuts after-call work by up to 60 seconds per call
- Trains on your data to improve summary quality over time

### CX/EX Scoring Bot
- Measures conversation dynamics using unique AI models
- Predicts customer retention and loyalty drivers
- Scores both customer experience (CX) and employee experience (EX)

### TimeFlex Bot
- Agent-initiated schedule changes without supervisor approval
- Uses complex scheduling algorithms to ensure coverage while allowing flexibility
- Enables permissionless scheduling adjustments at scale

### Exact Transcription Bot
- Market-leading transcription accuracy
- 80+ languages and dialects
- Customized models per customer for domain-specific vocabulary

### Data Insights Bot
- Translates business intelligence into actionable insights
- AI surfaces anomalies, trends, and correlations automatically
- Reduces time spent manually analyzing dashboards

### Genie Bot (newer)
- Conversational analytics: analysts and supervisors ask questions about CX interaction data in plain (natural) language
- Generates insights/leadership reports from interaction data without requiring data-science expertise
- Connects with conversational-intelligence data; one of the four bots first extended to Calabrio customers (Mar 2026)

### Agent Copilot Bots (umbrella)
- Automate manual agent workflows in real time — in-call knowledge retrieval, coaching, and post-call wrap-up
- Groups the Coaching Bot and Wrap Up Bot functions into a single real-time agent assistant
- One of the four bot families first extended to Calabrio customers (Mar 2026)

### Knowledge Automation Bot
- Single search bar across all knowledge sources
- AI summarizes results into curated answers
- Delivers appropriate knowledge at optimal times during interactions

### Knowledge Creation Bot (newer)
- GenAI authoring/maintenance of knowledge content to keep the knowledge base current

### PII Redaction Bot (newer)
- Automatically detects and redacts personally identifiable information in interactions/transcripts

### Call Risk Scoring Bot (newer)
- Scores interactions for risk (compliance/fraud signals) to prioritize review

### Intelligent Virtual Assistant (IVA)
- Powered by Voice and Digital Containment Bots; uses agentic AI
- Autonomously resolves customer interactions across voice, digital, and messaging channels
- Reduces inbound volume while maintaining satisfaction scores
- One of the four bot families first extended to Calabrio customers (Mar 2026)

## Workforce Management

- Forecasting — multi-algorithm forecasting with historical pattern recognition
- Scheduling — automated schedule generation with constraint handling
- Real-time adherence — monitors agent activity against schedule, alerts on deviations
- Intraday management — reforecast and adjust throughout the day
- Agent self-service — shift swaps, time-off requests, preference setting

## Quality Management

- Automated evaluations using Quality Bot (100% coverage possible)
- Evaluation forms and scorecards
- Calibration workflows for scoring consistency
- Coaching workflows triggered by evaluation results
- Compliance monitoring (Financial, HIPAA, PCI)

## CX Analytics / Speech & Text Analytics

- Speech analytics across voice interactions
- Text analytics across digital channels (chat, email, social)
- Sentiment analysis
- Topic detection and trending
- Root cause analysis
- Customer effort scoring

## Knowledge Automation

- Unified knowledge base across all sources
- AI-powered search and summarization
- Context-aware knowledge delivery to agents during interactions
- Self-service knowledge for customers

## Financial Compliance

- Trade reconstruction
- Communications surveillance
- Compliance recording
- Regulatory reporting

## Fraud & Security

- Authentication solutions
- Fraud detection
- Voice biometrics

## Pricing and limits

**No public pricing.** Enterprise custom pricing — "contact sales" model.

Estimated ranges (from industry research):
- WFM module: starts ~$100-500/user/month depending on deployment and modules
- Full platform: significantly higher, custom negotiated
- Calabrio ONE (midmarket positioning): ~$50-120/agent/month

**Pricing model**: Typically per-named-user for SaaS deployments. Can also be based on monthly page views and API calls for some products. On-premises options available.

**Contract terms**: Annual or multi-year. Highly negotiable — get feature lists in writing.

## Integrations

**500+ adaptors across 300+ vendors.**

**BYOT (Bring Your Own Telephony)**: Connect any major ACD system — cloud or on-premises. Multiple ACDs can connect simultaneously.

**Supported ACD/CCaaS**:
- Amazon Connect
- Genesys Cloud CX
- NICE CXone
- Five9
- Cisco
- Avaya
- Mitel
- Twilio Flex
- And more

**CRM integration**:
- Salesforce — via EliteConnect (makes recordings searchable by Salesforce fields, playback within Salesforce) and Verint WFM Professional for Service/Sales Cloud
- Other CRMs via adaptor library

**Verint Marketplace**: 350+ listings including extensions, Da Vinci Services, and partner innovations.

**Google Cloud**: WFM deployment partnership.

## API and developer resources

**Developer Portal**: One-stop shop for Verint APIs — behind authentication (not publicly browsable). Verint Customer Engagement Platform customers access it to discover APIs and use cases.

**Authentication (corrected 2026-06-13)**:
- **Platform identity / SSO**: the Verint Customer Engagement Platform supports **SAML 2.0**, **OpenID Connect (OIDC)**, and native username/password (per the Technical Architecture Overview). APIs are exposed as "developer-friendly open APIs (OAS)."
- **Da Vinci / Coaching APIs**: use **OAuth 2.0 — `client_credentials` grant**. You request API activation via your CSM/Program Manager, receive `client_id` and `client_secret` (sent encrypted), exchange them for a bearer access token, and use it on subsequent requests. All requests must use HTTPS over TLS. **Basic Auth is deprecated** in favor of OAuth 2.0 client credentials (Verint Coaching API docs, developers.cogitocorp.com).
- The skill previously said "API key-based authentication." Verint Community (the separate Telligent forum product) does use OAuth 2.0 / legacy API keys / PKCE, but that is a different product from the CX/WEM platform — do not conflate the two.

**API capabilities** (per Technical Architecture Overview — verbatim use cases):
- Provisioning new and existing users
- Enriching interactions during the time of live calls
- Exporting enriched interactions
- Retrieving adherence data for employees in the Verint Workforce Management application
- Adding, updating, and retrieving schedules
- Transcribing audio files via the Verint Da Vinci Speech Transcription API Service
- Managing and retrieving Performance Management KPIs
- Webhooks for event notification

**SDKs**:
- Community REST SDK (.NET)
- Sitecore SDK
- Various integrations/samples on GitHub (verint-resources org — but minimal)

**API management**: Uses Gravitee for API management infrastructure.

**Note**: Unlike NICE CXone or Genesys which have publicly browsable API docs, Verint's API documentation requires developer portal access. This makes evaluation harder before purchase.

## Verint + Calabrio merger

**Structure (corrected 2026-06-13)**: Thoma Bravo entered a definitive agreement to take Verint private for an enterprise value of **$2B** ($20.50/share, all-cash), announced **Aug 25, 2025**. Mechanically, **Calabrio acquired Verint — Verint became a wholly owned subsidiary of Calabrio** and was delisted from Nasdaq. The two were then combined into one company. On **Feb 18, 2026** the combined organization announced a single corporate name: **Verint**. Calabrio solutions "will be supported and enhanced as part of the Verint CX Automation Platform."

**Market impact**: 40%+ global WEM market share, ~85% of Fortune 500, ~5M agents, 100+ countries.

**Brand positioning**:
- **Verint CX Automation Platform** (Open Platform / Open CCaaS Platform): Enterprise (large contact centers, complex requirements)
- **Calabrio ONE**: Midmarket (simpler deployment, faster time-to-value)

**For existing Calabrio customers**: Continue using Calabrio ONE. Verint AI bots are being expanded to Calabrio customers — the first four extended (announced **Mar 10, 2026**) are the **Genie Bot**, **TimeFlex Bot**, **Agent Copilot Bots**, and **IVA** (integrating into Calabrio WFM and CX Automation Platform). First joint event: Verint Engage 2026.

**Thoma Bravo**: Private equity firm that financed the $2B take-private, likely driving margin optimization.

## Workflow setup

### Setting up Quality Bot for 100% QA
1. Access Quality Management module
2. Create evaluation form with criteria (compliance, empathy, process)
3. Enable Quality Bot — configure scoring rules using generative AI
4. Set scope — which queues/teams/interaction types to evaluate
5. Publish rules (draft rules don't execute)
6. Monitor scoring accuracy and refine rules based on false positives/negatives

### Setting up Coaching Bot
1. Enable Coaching Bot for target agent groups
2. Configure knowledge sources in Data Hub
3. Set up trigger conditions (e.g., specific topics, compliance violations)
4. Customize guidance style (non-disruptive by default)
5. Monitor agent acceptance/rejection rates
6. Iterate based on which suggestions agents find helpful

### Connecting to your CCaaS (BYOT)
1. Identify your ACD/CCaaS platform
2. Use pre-built adaptor from the Verint Marketplace
3. Configure data flow — interaction data, agent states, queue metrics
4. Set up real-time adherence if using WFM
5. Test with subset of agents before full rollout
6. For multi-ACD environments, configure each adaptor independently

## Deep dives

### Verint vs NICE vs Genesys — architectural differences
- **Verint**: Open, modular. Deploy individual components without buying the full suite. Connect to any ACD.
- **NICE CXone**: Integrated suite. Strongest built-in WFM. Tighter coupling between modules.
- **Genesys Cloud CX**: Platform play with AppFoundry marketplace. Strong routing engine. WFM in CX 3+ tiers.

Verint's advantage is flexibility — you can layer Verint WFM on top of Genesys routing, or add Quality Bot to a NICE CXone deployment. The trade-off is more integration work and potentially higher total cost.

### Partner program
Verint Partners receive referral fees and software discounts. Partner Corner on Verint Connect provides self-serve resources for training, sales, technical, and marketing materials. Contact Verint's "Become a Partner" page to inquire.
