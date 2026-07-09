---
name: sales-third-party
description: "Browses and install third-party marketing, research, and creative skills. Use when: 'install skills', 'available skills', 'third party skills', 'marketing skills', 'opc skills', 'what skills are available', 'list skills', 'browse skills', 'show me skills'. Do NOT use for routing a specific sales objective to the right skill (use /sales-do) or requesting a brand-new skill that doesn't exist yet (use /sales-request-skill)."
argument-hint: "[optional: a category or keyword to filter the catalog, e.g. 'research' or 'cold email']"
license: MIT
version: 1.0.0
tags: [sales, catalog, third-party, skill-discovery]
---
You are a skill catalog browser. When invoked, present the user with the full catalog of third-party skills available for this repo and help them install what they need.

## How to use this catalog

Each skill below can be installed individually or in bulk. Once installed, invoke it directly (e.g., `/cold-email <request>`) or use `/sales-do` to get routed automatically.

---
## Marketing & GTM Skills

> 33 skills from [`coreyhaines31/marketingskills`](https://skills.sh/coreyhaines31/marketingskills)

### Bulk install (all 33)

```bash
npx skills add coreyhaines31/marketingskills
```

### Install one

```bash
npx skills add coreyhaines31/marketingskills --skill <skill-name>
```

### SEO & Content

| Skill | What it does |
|---|---|
| `/ai-seo` | Optimize content for AI search engines and LLM citations |
| `/content-strategy` | Plan content strategy and identify topics to cover |
| `/copywriting` | Write marketing copy for homepages, landing pages, and sites |
| `/copy-editing` | Edit, review, and improve existing marketing copy |
| `/programmatic-seo` | Generate SEO pages at scale using templates |
| `/schema-markup` | Add and optimize structured data markup |
| `/seo-audit` | Audit and diagnose technical and on-page SEO issues |
| `/site-architecture` | Plan website hierarchy, navigation, and URL structure |
| `/social-content` | Create and schedule social media content |

### Conversion & Growth

| Skill | What it does |
|---|---|
| `/ab-test-setup` | Plan, design, and implement A/B tests and experiments |
| `/form-cro` | Optimize lead capture and contact forms |
| `/onboarding-cro` | Optimize post-signup activation and time-to-value |
| `/page-cro` | Increase conversions on marketing and landing pages |
| `/paywall-upgrade-cro` | Optimize in-app paywalls and upsell modals |
| `/popup-cro` | Create and optimize popups, modals, and overlays |
| `/signup-flow-cro` | Optimize signup, registration, and trial activation |

### Acquisition & Campaigns

| Skill | What it does |
|---|---|
| `/ad-creative` | Generate and scale ad headlines, descriptions, and full ads |
| `/cold-email` | Write B2B cold outreach and follow-up sequences |
| `/email-sequence` | Create automated email flows and drip campaigns |
| `/free-tool-strategy` | Plan and build free marketing tools for lead generation |
| `/lead-magnets` | Create and optimize lead magnets for email capture |
| `/paid-ads` | Manage Google, Meta, LinkedIn, and Twitter ad campaigns |

### Strategy & Positioning

| Skill | What it does |
|---|---|
| `/competitor-alternatives` | Create competitor comparison and alternative pages |
| `/launch-strategy` | Plan product launches and feature announcements |
| `/marketing-ideas` | Generate marketing inspiration and SaaS strategies |
| `/marketing-psychology` | Apply behavioral science and mental models to marketing |
| `/pricing-strategy` | Determine pricing, packaging, and monetization decisions |
| `/product-marketing-context` | Create foundational product marketing documentation |

### Retention & Revenue

| Skill | What it does |
|---|---|
| `/churn-prevention` | Reduce churn through cancellation flows and save offers |
| `/referral-program` | Build and optimize referral and affiliate programs |
| `/revops` | Manage lead lifecycle and marketing-to-sales handoff |
| `/sales-enablement` | Create pitch decks, one-pagers, and objection handling docs |

### Analytics

| Skill | What it does |
|---|---|
| `/analytics-tracking` | Set up and audit analytics measurement and event tracking |

---
## Research & Data Skills

> 10 skills from [`resciencelab/opc-skills`](https://skills.sh/resciencelab/opc-skills)

### Bulk install (all 10)

```bash
npx skills add resciencelab/opc-skills
```

### Install one

```bash
npx skills add resciencelab/opc-skills --skill <skill-name>
```

### Research

| Skill | What it does |
|---|---|
| `/producthunt` | Search and retrieve Product Hunt posts, topics, and collections |
| `/reddit` | Search and retrieve Reddit posts, comments, and subreddit info |
| `/requesthunt` | Collect and analyze user feedback from Reddit, X, and GitHub |
| `/twitter` | Search and retrieve tweets, user profiles, and trends from X |

### Creative & Design

| Skill | What it does |
|---|---|
| `/banner-creator` | Generate professional banners for GitHub, Twitter, and websites |
| `/logo-creator` | Generate professional logos with AI through iterative design |
| `/nanobanana` | Generate and edit images using AI (Gemini image model) |

### SEO & Domains

| Skill | What it does |
|---|---|
| `/seo-geo` | Optimize for AI search engines (GEO) and traditional search |
| `/domain-hunter` | Find domain names with availability checks and price comparison |

### Utilities

| Skill | What it does |
|---|---|
| `/archive` | Capture, index, and reuse project knowledge across sessions |

---
## More Third-Party Skills

### SEO & Backlinks

> From [`aaron-he-zhu/seo-geo-claude-skills`](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)

| Skill | What it does |
|---|---|
| `/backlink-analyzer` | Analyze backlink profiles with toxic link detection and competitor benchmarking |

```bash
npx skills add aaron-he-zhu/seo-geo-claude-skills --skill backlink-analyzer
```

### Presentations

> From [`jimliu/baoyu-skills`](https://skills.sh/jimliu/baoyu-skills)

| Skill | What it does |
|---|---|
| `/baoyu-slide-deck` | Transform content into professional presentation decks with customizable styles |

```bash
npx skills add jimliu/baoyu-skills --skill baoyu-slide-deck
```

### Marketing & Standardization

> From [`supercent-io/skills-template`](https://skills.sh/supercent-io/skills-template)

| Skill | What it does |
|---|---|
| `/marketing-skills-collection` | Generate marketing deliverables across CRO, copywriting, SEO, analytics, and growth |
| `/marketing-automation` | Marketing automation with 23 sub-skills across CRO, copywriting, SEO, analytics, and growth |
| `/skill-standardization` | Validate and standardize SKILL.md files against the Agent Skills spec |

```bash
npx skills add supercent-io/skills-template --skill <skill-name>
```

### Competitive Analysis

> From [`wshobson/agents`](https://skills.sh/wshobson/agents)

| Skill | What it does |
|---|---|
| `/competitive-landscape` | Analyze competitive dynamics with Porter's Five Forces, Blue Ocean Strategy, and positioning maps |

```bash
npx skills add wshobson/agents --skill competitive-landscape
```

### Link Building

> From [`calm-north/seojuice-skills`](https://skills.sh/calm-north/seojuice-skills)

| Skill | What it does |
|---|---|
| `/build-links` | Design link acquisition campaigns with prospect scoring and outreach strategy |

```bash
npx skills add calm-north/seojuice-skills --skill build-links
```

### Skill Development

> From [`starchild-ai-agent/official-skills`](https://skills.sh/starchild-ai-agent/official-skills)

| Skill | What it does |
|---|---|
| `/skill-creator` | Scaffold new skills with validated directory structure, frontmatter, and progressive disclosure |

```bash
npx skills add starchild-ai-agent/official-skills --skill skill-creator
```

### Lead Generation

> From [`apify/agent-skills`](https://skills.sh/apify/agent-skills)

| Skill | What it does |
|---|---|
| `/apify-lead-generation` | Multi-platform lead scraping from Google Maps, social media, websites, and search engines |

```bash
npx skills add apify/agent-skills --skill apify-lead-generation
```

### Launch & Growth

> From [`inferen-sh/skills`](https://skills.sh/inferen-sh/skills)

| Skill | What it does |
|---|---|
| `/product-hunt-launch` | Optimize Product Hunt launches with research, gallery strategy, and timing guidance |

```bash
npx skills add inferen-sh/skills --skill product-hunt-launch
```

## Examples

### Example 1: Browse the full catalog

**User says**: "What third-party skills are available?"

**Skill does**:
1. Presents the catalog grouped by source — Marketing & GTM (33 from `coreyhaines31/marketingskills`), Research & Data (10 from `resciencelab/opc-skills`), and the "More Third-Party Skills" sources (backlinks, presentations, competitive analysis, link building, skill development, lead generation, launch).
2. Surfaces the category headings (SEO & Content, Conversion & Growth, Acquisition & Campaigns, etc.) so the user can scan by intent.
3. Notes each skill can be installed in bulk per source or one at a time with `--skill <skill-name>`.

**Result**: The user sees every available skill with a one-line description and knows exactly how to install whichever they want.

### Example 2: Filter to a keyword and install one skill

**User says**: "I need a skill for writing cold outreach."

**Skill does**:
1. Filters the catalog to matching entries — here `/cold-email` ("Write B2B cold outreach and follow-up sequences") under Acquisition & Campaigns.
2. Identifies the source repo for that skill (`coreyhaines31/marketingskills`).
3. Hands back the single-skill install command: `npx skills add coreyhaines31/marketingskills --skill cold-email`.

**Result**: The user installs just the cold-email skill and invokes it with `/cold-email <request>`.

### Example 3: Bulk-install a whole source

**User says**: "Install all the research skills."

**Skill does**:
1. Identifies the Research & Data group sourced from `resciencelab/opc-skills` (10 skills including `/reddit`, `/twitter`, `/producthunt`, `/requesthunt`).
2. Provides the bulk install command: `npx skills add resciencelab/opc-skills`.
3. Lists what gets pulled in so the user knows the full set before running it.

**Result**: All 10 skills from that source are installed at once and each is invocable directly.

## Troubleshooting

### A skill doesn't appear after running the install command

**Cause**: The skill was installed into a different agent, or the install targeted the bulk source without the specific `--skill` flag the user expected.

**Solution**: Re-run the install for the exact source shown in the catalog, adding `--skill <skill-name>` for a single skill. Confirm the source slug matches the one listed under that skill's section (e.g., `coreyhaines31/marketingskills` vs `resciencelab/opc-skills`).

### Unsure which source a skill comes from

**Cause**: Skill names are listed under category headings, but the install command depends on the source repo, which is shown per section rather than per row.

**Solution**: Find the skill's section, then use the `> From [...]` source link and code block directly above or below that table. The Marketing & GTM and Research & Data groups each have a single shared source; the "More Third-Party Skills" entries each list their own source and command.

### Want a skill that isn't in the catalog

**Cause**: This catalog only covers vetted third-party skills already curated for the repo; it does not create new skills or route sales objectives.

**Solution**: To request a brand-new skill, use `/sales-request-skill`. To get routed to the best existing skill for a specific sales objective, use `/sales-do`.

## Related skills

- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`
