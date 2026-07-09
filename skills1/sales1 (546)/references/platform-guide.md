# Solidroad Platform Reference

## Platform overview

Solidroad is an AI-powered quality management and training platform for CX teams. Founded in 2023 (YC W25), headquartered in Dublin with offices in San Francisco. 6-person team led by CEO Mark Hughes (ex-Intercom) and CTO Patrick Finlay (ex-Intercom, Monaru S19). Raised $6.5M seed + $25M Series A (April 2026, led by Hedosophia). SOC 2 + ISO 27001 certified.

Solidroad's key differentiator is the **closed-loop between QA and training**: automated quality scoring surfaces skill gaps, which automatically generate targeted training simulations. Most QA tools stop at scoring — Solidroad connects scoring to remediation.

## Key modules

### Interaction Review (Automated QA)
- Scores **100% of conversations** across phone, live chat, video, and email — no sampling
- AI applies custom quality rubrics uniformly, avoiding subjective human interpretation
- Each org defines its own criteria: tone, policy compliance, interaction standards
- Conversations analyzed in **80+ languages**
- Up to **90% reduction** in manual review hours, **20x increase** in coverage

### AI Training Simulations
- Generates **custom practice scenarios** from real conversation patterns and discovered skill gaps
- Multi-channel: phone, email, chat, video simulations
- Each simulation scored against custom scorecards with instant coaching feedback
- **SCORE methodology**: Scenario-based training framework for structured practice
- Reps practice in risk-free environment before engaging real customers

### Performance Analytics
- **IQS framework**: Internal Quality Score tracking across agents and teams
- Custom scorecards with weighted criteria
- Team-wide and individual agent dashboards
- Tracks improvement over time: ramp time, resolution speed, quality scores

### Unified QA for Human + AI Agents
- Single, consistent quality view across human agents AND AI agents (chatbots, virtual agents)
- Same rubrics applied to both — identifies where AI agents fail and where humans struggle
- This is Solidroad's positioning against tools that only monitor human agents

## Pricing and limits

**Custom pricing only (re-verified 2026-06-13).** Solidroad does **not** publish per-user pricing, named tiers, or a self-serve plan on its website. The official positioning is *"Custom pricing only — no self-serve tier or published pricing for smaller teams to evaluate independently."* Pricing is quote-based and obtained by contacting sales / booking a demo.

- No public per-user dollar figures. (Earlier versions of this guide cited ~$10 / ~$20-30 / ~$50 per-user tiers; those came from third-party aggregators like SaaSworthy, were never published on solidroad.com, and are no longer reflected anywhere official — do not quote them as Solidroad's pricing.)
- Enterprise-oriented: expect a custom annual contract, dedicated CSM, SSO, and custom rubrics.
- SOC 2 Type 2 + ISO 27001 certified.
- For a current quote, contact Solidroad sales / book a demo.

> **Unverified:** whether a 14-day free trial is still offered. Older notes mentioned a 14-day trial with "Growth-tier" features, but Growth is not a named tier on the current site and the trial could not be confirmed against live docs on 2026-06-13. Confirm with sales.

## Integrations

### Helpdesk / Service Platforms (native connectors)
Per the official site (re-verified 2026-06-13), native connectors are:
- **Zendesk** — native connector
- **Intercom** — native connector
- **Gladly** — native connector
- **Gorgias** — native connector
- **ServiceNow** — native connector
- **Help Scout** — native connector (listed on the ecommerce-QA resource page)

> Official quote: *"Integrate with Zendesk, Intercom, Gladly, Gorgias, and ServiceNow via native connectors."* The `/quality` page summarizes it as *"Plug into Intercom, Zendesk, and more."*
>
> **Salesforce Service Cloud is NOT currently listed** as a native connector anywhere on solidroad.com (checked the homepage, /quality, and the call-center-QA + ecommerce-QA resource pages on 2026-06-13). Earlier versions of this guide listed it; treat a Salesforce integration as unconfirmed — verify with Solidroad sales before relying on it.

### Other integrations / broader CX stack
- **Gong**, **Guru**, **Front** — listed among "leading tools" Solidroad integrates with on the homepage
- Solidroad is "building native integrations to connect to your sales stack to automatically score your live calls"
- Works within existing CX tech stack; legacy telephony/CCaaS targets (Genesys, Avaya, Cisco, Five9) are not named on the current site — confirm during evaluation

### API
- **No public API documented.** SaaSworthy lists API support as "NA."
- All integrations through native connectors or custom integration via Solidroad team
- No known webhook support

## Key results (case studies)

| Customer | Result |
|---|---|
| Podium Corp | 800K+ conversations/mo processed, 33% faster issue resolution |
| Tech Mahindra | 50% reduction in onboarding time |
| Crypto.com | Go-live CSAT improved by 3% (above 90%) |
| General | Up to 90% reduction in manual review hours, 20x increase in QA coverage |

## Workflow setup

### Setting up Automated QA (Week 1-2)

1. **Connect your channels**: Link Solidroad to your CRM/CCaaS via native connectors
2. **Define scoring criteria**: Start with 3-5 binary, observable criteria (not subjective)
3. **Configure custom rubrics**: Weight criteria by importance (compliance vs tone vs resolution)
4. **Run parallel scoring**: Compare AI scores against manual supervisor scores for 2-4 weeks
5. **Calibrate**: Adjust criteria and weights based on calibration results
6. **Go live**: Enable automated scoring on 100% of conversations

### Setting up AI Training (Week 3-4)

1. **Review QA gaps**: Identify the top 3-5 skill gaps from automated scoring data
2. **Generate simulations**: Solidroad creates practice scenarios targeting those specific gaps
3. **Configure channels**: Set up phone, chat, and/or email practice as needed
4. **Assign to agents**: Route simulations to agents with relevant skill gaps
5. **Track improvement**: Monitor quality scores post-training to measure impact

### Closed-Loop Coaching Workflow

```
QA scores conversations → Gaps identified → AI generates targeted simulations
→ Agent practices → Re-scored on real conversations → Improvement measured
→ New gaps surface → New simulations generated → Continuous improvement
```

## Competitive positioning

| Platform | Focus | QA | Training | Real-time coaching | Pricing |
|---|---|---|---|---|---|
| **Solidroad** | QA + Training closed-loop | 100% automated | AI simulations | No | Custom (quote-based) |
| Observe.AI | Enterprise QA + virtual agents | 100% automated | No | Agent Copilot | ~$100-500/user/mo |
| Balto | Real-time guidance | 100% automated | No | Yes (<200ms) | ~$100-150/agent/mo |
| Cresta | Enterprise AI stack | 100% automated | No | Yes | $60K-$150K/yr |
| MaestroQA | Structured QA workflows | Sampling-based | No | No | ~$19/user/mo+ |
| Enthu.AI | Affordable QA | 100% automated | No | No | ~$15-69/user/mo |

**When to choose Solidroad:**
- You want QA AND training in one platform (closed-loop)
- You're a BPO or mid-large contact center (50+ agents)
- You need multi-channel training (not just phone)
- You want to measure training impact directly through QA scores

**When to choose something else:**
- You need real-time coaching during calls → Balto or Cresta
- You need pure QA without training → Observe.AI, MaestroQA, or Enthu.AI
- You need AI virtual agents → Observe.AI or Cresta
- You have <20 agents and need affordability → Enthu.AI

## Partner program

Solidroad runs a PartnerStack affiliate program:
- $100 per lead, $500 per closed-won deal
- 90-day cookie (resets on re-click)
- Signup: https://solidroad.partnerstack.com/
