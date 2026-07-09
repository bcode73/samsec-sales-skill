# Personadeck Platform Reference

<!-- Source: personadeck.io / app.personadeck.io (homepage 404s to the app at research 2026-07);
assembled from third-party listings: capterra.com, appsumo.com/products/personadeck, getapp.com,
softwarefinder.com, creati.ai. Pricing in EUR. -->

## Overview

Personadeck (personadeck.io, app at `app.personadeck.io`) is an AI **customer-persona generator** aimed
at marketers, marketing agencies, product managers, and founders who want a buyer/user persona in
minutes without manual research. You pick a **persona type**, describe your audience or product, and it
returns a **professionally-styled persona card** using machine-learning / NLP over your description. Its
differentiator vs a generic chatbot is the **persona-type choice** (User vs Negative), a styled card
layout with **editable labels**, **personality-trait predictions**, and a **multilingual** interface. It
is a **UI-only web app** — there is no documented public API. (The homepage often 404s straight to the
app; treat all specifics as best-effort and verify live.)

## Persona types (chosen first)

| Type | What it models | Use it to |
|---|---|---|
| **User Persona** | The audience you *want* — the ideal customer/user | Align product, positioning, and messaging with the people you're building for |
| **Negative Persona** | The skeptic / non-buyer / poor-fit customer | Decide who to **screen out** of targeting, or which objections to deliberately convert |

Building **both** gives a real audience map (who to chase, who to disqualify). A single blended persona
hides the disqualifiers.

## Capabilities & automation surface

| Module | What it produces | Automation surface |
|---|---|---|
| **Persona generator** | A styled persona card: demographics, behaviors, motivations/preferences, preferred channels, and **personality-trait predictions** (practical-vs-emotional, introvert-vs-extrovert, etc.), derived from your audience/product description | UI-only |
| **Persona-type selector** | User Persona vs Negative Persona (choose before generating) | UI-only |
| **Editable card labels** | Rename/adjust the persona card's field labels after generation | UI-only |
| **Multilingual** | UI in English, French, German, Spanish; **persona generation in any language** on higher plans | UI-only |
| **PDF export** | Download the finished persona as a PDF (the only export format) | UI-only, PDF only |
| **Storage** | Save personas in-app (unlimited storage on paid tiers) | UI-only |

*Everything is UI-only. There are no documented webhooks, no Zapier/Make modules, and no MCP server. The
persona is static and can only leave the tool as a PDF.*

## Persona field set (typical output)

A generated Personadeck card typically includes:

- **Demographics** — age, location, occupation, and similar attributes inferred from your description
- **Behaviors & preferences** — how the persona acts and what they favor
- **Motivations / goals** — what they're trying to achieve
- **Preferred channels** — where to reach them
- **Personality-trait predictions** — directional axes such as **practical vs emotional** and
  **introvert vs extrovert** (framing, not measured psychometrics)

Field labels are **editable**, so trim or rename anything the model over-asserted before exporting.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — assembled from third-party listings; the app pricing page was
unreachable (503) at research. Prices in EUR and may be stale. Confirm at app.personadeck.io/en/pricing.*

| Plan | Price (approx.) | Notes |
|---|---|---|
| **Free** | €0 | Try persona generation with restrictions/limits |
| **Basic** | ~€4 / month | Entry paid tier |
| **Medium** | ~€9.90 / month | Adds generation in any language (per listings) |
| **Pro** | ~€42 / month | ~**45 personas / month**, unlimited storage, editable labels |

- Also sold as an **AppSumo lifetime deal** (lifetime Pro access; code redemption within 60 days,
  non-stackable, 60-day money-back guarantee) — figures and availability move.
- **Freemium model**: start free, upgrade when ready.
- **No API tier** — there is no developer/API plan because there is no public API. There is therefore no
  rate-limit or overage behavior to design an integration around.

## Getting a useful persona (input quality)

Reviewers fault Personadeck for **repackaging thin input**, so input depth is the whole game:

1. Name a **specific customer**, not a category ("rotating-shift ICU nurse," not "healthcare workers").
2. State the **exact problem** they hit and **when**.
3. Say how your product **differs** from how they solve it today.
4. Give the **stage/context** (pre-launch, first customers, scaling).
5. Generate a **User Persona** and a **Negative Persona**, then **re-run variants** and compare.
6. **Edit the labels** to cut anything the model over-asserted before exporting the PDF.

Then **validate against real people** — interview a handful about the last time they hit the problem and
watch what they actually do. A generated persona is a hypothesis, not a finding.

## No public API — automation workaround

Personadeck has **no public API, no webhooks, no Zapier/Make, and no MCP server**. For programmatic or
batch persona generation, call an LLM API directly with your own persona prompt instead of trying to
integrate against Personadeck.

**cURL (Anthropic Messages API):**

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": "Generate a customer persona for this product. Return demographics, behaviors, motivations, preferred channels, and two personality-trait axes (practical-vs-emotional, introvert-vs-extrovert). Product: a meal-prep subscription for rotating-shift nurses who skip meals on night shifts."
    }]
  }'
```

**Python (batch over many segments):**

```python
import os, anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

segments = [
    "rotating-shift ICU nurses who skip meals on night shifts",
    "gig-economy drivers who eat fast food between rides",
    # ... 30 more
]

PROMPT = (
    "Generate a customer persona for the audience below. Return JSON with keys: "
    "demographics, behaviors, motivations, preferred_channels, personality_traits "
    "(practical_vs_emotional, introvert_vs_extrovert). Audience: {seg}"
)

for seg in segments:
    msg = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[{"role": "user", "content": PROMPT.format(seg=seg)}],
    )
    print(seg, "→", msg.content[0].text)
```

This gives you the batch/scripted generation Personadeck itself can't — and the output is structured
data you can pipe into a CRM or deck, unlike Personadeck's static PDF. Still validate any generated
persona against real customers before acting on it.
