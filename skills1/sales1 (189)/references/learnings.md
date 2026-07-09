# FreshLearn Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-27**: Research baseline — platform docs, REST API (`https://api.freshlearn.com/v1`, `api-key` header from Settings → User → API Key, cursor pagination `{data, pageInfo}` with `limit` 1–200/default 50 and Unix-second date filters, sections Members/Courses/Product Enrollments/Payments/Assessments), native webhooks + Zapier (6 triggers / 9 actions), pricing, and the affiliate program captured from live sources on this date. Re-verify before relying. Key facts: **API + unlimited workflows are No Brainer+ ($89)-gated; Zapier + community + certificates + branding removal are No Brainer ($46)-gated; Pro is courses + email + checkout only**. 0% transaction fees + unlimited learners on all paid tiers. Exact REST endpoint paths are JS-rendered in the doc (operation surface verified via Zapier/Make; example paths in the api-reference are best-effort and marked). No GitHub org / MCP server found. Differentiators: heavy AI Studio + no caps on students/storage. Known complaints: limited page builder (header/footer per page), no-refund policy, billing/cancellation friction, occasional glitches.
