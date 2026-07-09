# BOOK BIBLE
### *Sales Blueprint: The Practical System for Attracting Customers, Closing More Sales and Building a Business People Trust*

**This document is the single source of truth for the entire manuscript.**
Every module, worksheet, diagram and line of front matter must be consistent with what is written here. If a later draft contradicts this document, the draft is wrong and must be corrected, not the other way round.

---

## 1. PROJECT IDENTITY

| Field | Detail |
|---|---|
| **Title** | Sales Blueprint |
| **Subtitle** | The Practical System for Attracting Customers, Closing More Sales and Building a Business People Trust |
| **Author** | Samuel Omobusuyi |
| **Publisher** | SSO Publishing |
| **Language** | British English |
| **Category** | Business / Sales / Entrepreneurship |
| **Target length** | 220 to 280 formatted pages |
| **Comparable shelf** | Sits beside *To Sell Is Human*, *The Challenger Sale*, *Never Split the Difference*, *Influence*: practical, structured, no-nonsense business craft rather than motivational content |

**SSO Publishing is the official publishing imprint of this entire project.** Every front-matter page, copyright notice, footer, export (DOCX/PDF/EPUB/print) and external reference to the book's publisher must read "SSO Publishing." No other imprint name is used anywhere in the manuscript, repository, or generated assets.

### Target audience

A business owner, founder, or sales professional who:

- Sells a considered purchase: the buyer needs more than one conversation to say yes
- Is good at their craft but has never had formal sales training
- Is tired of "sales tips" content and wants one coherent system
- Sells to both individual customers and business buyers, often within the same week
- Wants a repeatable process, not a personality transplant

### Mission

To give a business owner a single, complete, repeatable system for turning strangers into customers and customers into advocates, without resorting to pressure, manipulation or scripts that make them cringe.

### Vision

Sales Blueprint becomes the book people hand to a new hire on their first day and say: "Read this. This is how we sell here."

### Core promise

*Every sale is won or lost in nine moments. Master the nine, and selling stops being a mystery.*

### Brand personality

- **Direct.** Says the thing other business books dance around.
- **Grounded.** Every claim is followed by a mechanism ("here is why this works") and a method ("here is how you do it").
- **Respectful of the reader's intelligence.** Never dumbs down, never pads.
- **Quietly confident.** The authority comes from clarity, not from volume or exclamation marks.

### Writing philosophy

Teach first. Persuade second. A reader who finishes a chapter should be able to *do* something differently that afternoon, not just feel inspired. If a paragraph doesn't change what the reader thinks or does, it is cut.

---

## 2. VOICE GUIDE

Write as an experienced business owner explaining, over coffee, exactly how something works and why, to someone whose judgement they respect.

**The voice is:**

- An experienced entrepreneur who has actually closed deals, lost deals, and figured out why
- Someone who teaches through explanation and example, not through hype
- Confident enough to be plain: short sentences, real answers, no hedging

**The voice is never:**

- Academic (no citations-heavy tone, no "studies show" without a concrete, named mechanism)
- Artificial-sounding or AI-generated in cadence (no "in today's fast-paced business landscape," no rule-of-three padding, no inflated-significance phrasing, no em dashes or en dashes anywhere; see Section 13)
- A motivational speaker (no "you've got this," no manufactured urgency, no chapter-ending pep talks)
- Exaggerated (never "this will 10x your close rate"; instead, something like "reps using this approach report fewer stalled deals in the third meeting")
- Clickbait (never "the one trick top performers don't want you to know")

**Working test for every paragraph:** *Would a sharp, sceptical small-business owner nod, or would they roll their eyes?* If in doubt, cut the flourish and state the point plainly.

---

## 3. STYLE GUIDE

- **British English** throughout: organise, colour, favourite, programme (unless referring to computer code), realise, licence (noun) / license (verb).
- **Short paragraphs.** Two to five sentences. One idea each.
- **Sentences favour clarity over rhythm.** If a sentence needs a second read, it is rewritten.
- **Examples are concrete and numeric where possible:** a price, a percentage, a number of days, not vague ("significantly improved") but specific ("cut the sales cycle from eleven weeks to seven").
- **Minimal jargon.** Where a technical sales term is unavoidable (e.g. "economic buyer"), it is defined in plain language the first time it appears and added to the Glossary.
- **No repetition of ideas across modules.** Each module owns its territory. Cross-references point back ("see Module 4") instead of re-explaining.
- **No filler transitions** ("Now that we've covered X, let's move on to Y" is replaced by a direct opening line that earns its place).
- **Second person ("you")** is the default address to the reader; the case study is narrated in third person.
- **Contractions are allowed** ("don't," "it's"): this is a conversation with a peer, not a legal document.

---

## 4. FORMATTING GUIDE

### Heading hierarchy

```
# Module Title (H1, one per module)
## Major section (H2)
### Subsection (H3)
#### Rare (only for deeply nested worksheet steps)
```

Headings use sentence case, not title case: "Building the value stack," not "Building The Value Stack."

### Callout boxes

Use blockquote-style callouts with a bold label so they are visually distinct and portable across Markdown renderers:

> **Tip:** A single, practical piece of advice that supports the main text.

> **Warning:** A common trap, framed as "watch for" rather than "don't."

> **Kestrel Office Interiors case study:** A continuation of the running story, clearly marked so the reader always knows they've moved into narrative.

> **Exercise:** A named, numbered practical task the reader does before continuing.

### Standard module elements (in order)

1. Learning objectives (bullet list, three to five items, each starting with an active verb)
2. Opening story (60 to 150 words, sets up the problem the module solves)
3. Core principles (H2 sections)
4. Kestrel Office Interiors case study thread (woven through or boxed)
5. Diagram(s) (Mermaid, referenced by filename in `/visuals/diagrams`)
6. Worksheet / exercise (referenced by filename in `/worksheets`)
7. Common mistakes (bullet list, framed as "watch for," not "never do")
8. Chapter summary (three to six bullet points)
9. Key takeaways (a single bolded sentence: the one line a reader should remember)

### Lists and tables

Use tables for anything comparative (before/after, option A vs option B, tier definitions). Use numbered lists for sequences the reader must follow in order. Use bullet lists for non-sequential collections. Avoid inline-header vertical lists where every bullet opens with a bolded label followed by a colon and a sentence that just restates the label; write the point as a sentence instead.

### Diagram formatting

All in-manuscript diagrams are Mermaid, stored in `/visuals/diagrams/`, referenced from the module text with a caption line directly beneath:

```
*Figure 3.1: The Trust Pyramid*
```

Figure numbers follow `{module number}.{sequence within module}`.

---

## 5. TERMINOLOGY

Defined once, used consistently everywhere. Full definitions live in the Glossary (`manuscript/appendices/glossary.md`); this is the working reference during drafting.

| Term | Definition |
|---|---|
| **The Blueprint Framework** | The book's central nine-stage system for winning and keeping a customer (see Section 6). |
| **Considered purchase** | A purchase the buyer will not make on impulse: it involves risk, cost, or more than one decision-maker. |
| **Budget holder** | The person who controls or releases the money for a purchase. Not always the decision-maker. |
| **Champion** | A person inside the buying organisation who wants you to win and will advocate internally, even when not in the room. |
| **Economic buyer** | The person whose approval is ultimately required because they own the budget outcome. |
| **Trust deficit** | The gap between how much confidence a buyer needs to say yes and how much they currently have. |
| **Value stack** | The visible, itemised list of outcomes a customer gets, arranged so the price feels small next to the pile. |
| **Objection** | A signal of unresolved doubt, not a rejection. Distinguished throughout from a **decline** (a genuine no). |
| **Multithreading** | Building relationships with more than one stakeholder in a buying decision, so the deal does not depend on a single contact. |
| **Nurture** | Deliberate, scheduled contact with a customer or prospect that is not a sales pitch. |
| **Advocate** | A past customer who proactively refers, reviews, or defends the business without being asked each time. |
| **The 30-Day Sales Blueprint** | The book's closing implementation plan: a day-by-day rollout of the framework for a real business. |

---

## 6. FRAMEWORK DEFINITIONS: THE BLUEPRINT FRAMEWORK

This is the intellectual property of the book. Every module in Part Two exists to teach one letter in depth; every other part of the book refers back to it. The framework describes the *sequence a buyer moves through emotionally and practically*, whether that sequence takes ten minutes or ten months.

```
B: Build Trust
L: Learn the Customer
U: Understand the Problem
E: Establish Value
P: Present the Offer
R: Remove Doubt
I: Inspire Action
N: Nurture Relationships
T: Turn Customers into Advocates
```

| Letter | Stage | One-line definition | Fails when... |
|---|---|---|---|
| **B** | Build Trust | Earn the right to be listened to before you try to sell anything. | The seller pitches before the buyer feels safe. |
| **L** | Learn the Customer | Understand who the buyer actually is: their role, pressures, and how they buy. | The seller assumes instead of asking. |
| **U** | Understand the Problem | Diagnose the real cost and cause of the buyer's problem, not the surface symptom. | The seller solves the wrong problem well. |
| **E** | Establish Value | Connect the solution to a specific, believable outcome the buyer cares about. | Value is asserted ("we're the best") instead of demonstrated. |
| **P** | Present the Offer | Package the solution so the decision is easy to say yes to. | The offer is confusing, over-optioned, or price-led. |
| **R** | Remove Doubt | Address the specific, named hesitations standing between interest and commitment. | Objections are argued with instead of resolved. |
| **I** | Inspire Action | Give the buyer a clear, low-friction next step and a reason to take it now. | The seller waits for the buyer to chase them. |
| **N** | Nurture Relationships | Keep the relationship alive and valuable after the sale closes. | Contact stops the day the invoice is paid. |
| **T** | Turn Customers into Advocates | Turn satisfaction into active, repeatable referral. | The business hopes for referrals instead of building a system for them. |

**Design rule:** the framework is not strictly linear in real selling. A seller often loops back (a new stakeholder joins mid-deal and Learn/Build Trust restart for them). Part Two teaches each stage as a discipline; Module 13 ("Sales Systems") teaches how the loop actually runs in practice.

Every module in Part Two must:
1. Open by naming which letter it covers and why it sits where it does in the sequence.
2. Show what happens when a seller skips straight past this letter (a concrete failure mode).
3. Give at least one exercise the reader can complete using their own, real business.
4. Advance the Kestrel Office Interiors story by exactly one stage.

---

## 7. VISUAL STYLE

**Aesthetic:** Minimal, premium, business-consulting. Think McKinsey deck crossed with a well-designed product manual, never a clip-art motivational poster.

**Principles:**

- One accent colour per diagram family; restrained palette overall (ink/charcoal text, a single accent, deep teal, for emphasis, white/cream background)
- Generous whitespace; diagrams must survive being read at a glance
- Every diagram earns its place by teaching something a paragraph would say more slowly; it is never decorative
- Consistent shape language: pyramids for hierarchy/priority, funnels for narrowing processes, cycles for recurring loops, flowcharts for decisions, timelines for sequences
- Typography in generated graphics: clean sans-serif, sentence case (not ALL CAPS), no drop shadows or gradients

**In-manuscript diagrams** are built in Mermaid (version-controlled, renders in Markdown/GitHub, free to update). **Premium cover/marketing/full-page graphics** are specified as detailed generation prompts in `/visuals/prompts/` for external image generation. Each prompt file states purpose, exact placement in the manuscript, the caption to run beneath it, and the full generation prompt.

---

## 8. RUNNING CASE STUDY

**One fictional business. Same story, start to finish. Every module advances it by one stage.**

### Business: Kestrel Office Interiors

**Founder:** Priya Shah, 34. Trained as an interior designer; started the business eight years ago after fitting out a friend's start-up office as a favour.

**What they do:** Design and fit out offices for growing companies (15 to 200 staff) who have outgrown their space or are moving to a new one. Typical project value: £18,000 to £140,000. Sales cycle: three to fourteen weeks.

**Where they are:** A market town in the English Midlands; clients across a 90-minute radius plus a growing number of remote-first clients found online.

**Team at the start of the book:** Priya, one designer, one project manager, a small fitting crew subcontracted per job. No dedicated salesperson: Priya does all the selling herself, on top of running projects.

**The buying committee Kestrel sells into (used to teach multithreading):**
- **Office Manager / Operations Lead:** day-to-day contact, feels the pain first, rarely controls budget alone
- **Finance Director:** controls the budget, is sceptical of "nice to have" spend
- **Managing Director / CEO:** cares about what the space says about the company and how disruptive the work will be

**The problem at the start of the book:** Priya's work is excellent. She has a strong portfolio and happy past clients, but her win rate on quotes is under one in four. She competes on price against national fit-out chains, discounts to try to win, and gets referrals by luck rather than by design. She believes she is "just not a salesperson."

**The arc across the book:** Module by module, Priya installs one stage of the Blueprint Framework into how Kestrel sells. By Module 14 (The 30-Day Sales Blueprint), Kestrel has a repeatable, documented sales system, a rising win rate, a small multithreaded pipeline of enterprise-style deals, and a functioning referral engine, all without Priya becoming a different person.

**Continuity rules:**
- Every fact stated about Kestrel in an earlier module remains true in every later module (name, numbers, team, location, client types).
- Numbers move in one direction across the book (win rate, average deal size, referral rate) unless a module explicitly explains a setback and how it was addressed.
- Priya is never turned into a flawless case study. She still makes mistakes; the book shows her correcting them, which is where the teaching lives.
- Dialogue and scenes are original in every module. Never copy a scene from an earlier module; only reference outcomes ("Since Module 6, Priya's opening question had changed...").

---

## 9. QUALITY STANDARD: THE FIVE QUESTIONS

Every chapter must visibly answer, in this order:

1. **What?** Name the concept precisely.
2. **Why?** Explain the mechanism: why does this work, psychologically or commercially?
3. **How?** Give the concrete method or steps.
4. **How do I apply this today?** A specific action the reader can take within 24 hours.
5. **How do I measure success?** A concrete metric or signal that tells the reader it worked.

A module that cannot answer all five is not finished.

---

## 10. EDITORIAL RULES

- No idea is explained twice across modules: if it recurs, it is referenced, not restated.
- No generic advice ("build relationships," "listen to your customer") without an immediate, specific mechanism for how to do it.
- No motivational filler: no chapter may end on inspiration alone; it must end on the summary and key takeaway.
- Every paragraph must earn its place: if deleting it loses no instruction, example, or narrative progress, delete it.
- Source material (the repository's SKILL.md library) is research only. Principles are extracted and resynthesised into original explanations, analogies, exercises, diagrams and the Kestrel story. No wording is copied or closely paraphrased from source files or from any other published author.
- Every module is reviewed against this Book Bible and against all previously completed modules before being marked final.
- Every module must pass the Humanizer Pass (Section 13) before being marked final.

---

## 11. BOOK STRUCTURE (REFERENCE)

**Front Matter:** Copyright · Disclaimer · Dedication · Preface · Table of Contents · How to Use This Book · Introduction · The Blueprint Framework (overview)

**Part One: Foundations**
Module 1: The Truth About Sales
Module 2: How Customers Really Buy

**Part Two: The Blueprint Framework**
Module 3: Build Trust
Module 4: Learn the Customer
Module 5: Understand the Problem
Module 6: Establish Value
Module 7: Present the Offer
Module 8: Remove Doubt
Module 9: Inspire Action
Module 10: Nurture Relationships
Module 11: Turn Customers into Advocates

**Part Three: Modern Selling**
Module 12: Digital Selling
Module 13: Sales Systems

**Part Four: Implementation**
Module 14: The 30-Day Sales Blueprint

**Appendices:** Worksheets · Templates · Checklists · Glossary · References

---

## 12. COPYRIGHT PAGE (STANDING TEXT)

This exact text is used verbatim on the copyright page in front matter:

> Copyright © 2026 Samuel Omobusuyi. All rights reserved.
>
> No part of this publication may be reproduced, stored in a retrieval system or transmitted in any form or by any means, electronic, mechanical, photocopying, recording or otherwise, without prior written permission from the copyright holder, except for brief quotations used in reviews or other uses permitted by applicable copyright law.
>
> Published by SSO Publishing.
>
> First Edition, 2026.
>
> The information in this book is provided for educational and informational purposes only. It does not constitute legal, financial or professional advice. The author and publisher make no representations or warranties as to the accuracy or completeness of the contents and disclaim any liability arising from its use. Kestrel Office Interiors and all characters depicted are fictional and any resemblance to real businesses or persons is coincidental.

---

## 13. HUMANIZER PASS (MANDATORY WRITING QUALITY GATE)

Every piece of manuscript text, meaning front matter, every module, every worksheet, template, and checklist, must pass a Humanizer review before it is marked Final in `PROJECT_ROADMAP.md`. The reference standard is the `humanizer` skill stored at the repository root (`SKILL (1).md`), which catalogues the recurring tells of AI-generated prose. This section states the constraints from that skill that apply directly to this book; the root skill file is the fuller reference when a judgement call is needed.

### Hard constraints (no exceptions)

- **No em dashes (—) or en dashes (–) anywhere in the manuscript.** Use a period, comma, colon, parentheses, or a restructured sentence instead. Number ranges use a plain hyphen ("three to fourteen weeks" or "3-14 weeks"), never an en dash.
- **No curly quotation marks.** Straight quotes only.
- **No emojis.**
- **Sentence case in headings**, never title case.
- **No inline-header vertical lists** (bulleted items that open with a bolded label and colon, then just restate the label in sentence form).

### Patterns to catch on every pass

- **Inflated significance:** phrases like "stands as a testament," "marks a pivotal moment," "underscores its importance." State what happened; skip the ceremony.
- **Promotional language:** "vibrant," "boasts," "nestled," "must-read," "game-changing." Kestrel Office Interiors is a real-feeling business, not a tourist brochure.
- **Vague attribution:** "experts agree," "industry reports suggest," without a named, specific source. If there's no source, cut the claim or make it concrete.
- **AI vocabulary words:** delve, tapestry, testament, underscore, pivotal, crucial (overused), foster, garner, intricate, landscape (as an abstract noun), showcase, robust, seamless, leverage (as a verb), align with. None of these are banned outright, but a paragraph that leans on more than one of them reads as machine-written.
- **Rule-of-three padding:** forcing every list into exactly three items to sound thorough. Use however many items the point actually needs.
- **Copula avoidance:** "serves as," "stands as," "functions as" where "is" would do the job.
- **Negative parallelisms:** "It's not just X, it's Y." Say what it is.
- **Generic upbeat endings:** "the future looks bright," "exciting times ahead." End on the chapter summary and key takeaway instead (Section 4).
- **Signposting:** "Let's dive in," "here's what you need to know." Start with the content itself.
- **Sycophantic tone:** this book never addresses the reader as if it were a chatbot ("great question!"). It has no reason to; it is a book, not a conversation.
- **Excessive hedging:** "it could potentially possibly be argued." Say the thing directly, with an honest qualifier only where real uncertainty exists.

### What this section does not ban

Formal vocabulary used precisely, correct grammar, clear structure, and the occasional short sentence for emphasis are not AI tells on their own. The test is always whether a sharp, sceptical reader would sense a machine behind the page, not whether the prose is polished. See the "Detection guidance" section of `SKILL (1).md` for the fuller list of false positives.

### Process for every module

1. Write the draft against this Book Bible.
2. Read it back and mark every hit against the patterns above.
3. Revise into a final version with no em dashes, no en dashes, and no more than one instance of any single AI vocabulary word per module.
4. Only then update its status to Final in `PROJECT_ROADMAP.md`.

---

*This Book Bible is a living document during drafting. Any change to it after Phase 1 approval must be logged and cross-checked against all modules already written.*
