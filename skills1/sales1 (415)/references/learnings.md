# PhantomBuster — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the API docs (hub.phantombuster.com/docs/api + /reference), support center (Using the API, webhooks, plans), and pricing/review articles.

- **Category:** code-free **web/LinkedIn automation + scraping + lead-gen**. **Phantoms** = pre-built automations (LinkedIn Search Export, Profile/Company Scraper, Auto-Connect/Message, Email Finder, …); **Flows/Workflows** chain them; **AI Agents** add LLM steps; **LinkedIn Leads database** stores results. Cloud-run. Audience: growth hackers, solo founders, small B2B SaaS sales teams, agencies — strong fit.
- **API:** base **`https://phantombuster.com/api/v2/<path>`** (v2 = ms timestamps; v1 = seconds). Auth **`X-Phantombuster-Key-1`** header (or `key` query param); key from **Workspace settings**, **shown once on creation**. Anyone with the key can launch agents → keep server-side, rotate if leaked. Responses are **JSend** (`{status:"success",data}` / `{status:"error",message}`).
- **Endpoint groups:** **Agents** (`/agents/fetch-all`, `/agent/{id}`, **`/agent/{id}/launch`**, `/agent/{id}/fetch-output`), **Containers** (`/containers/fetch`, **`/containers/fetch-result-object`**), **Storage** (LinkedIn Leads DB — delete leads, manage lists, sync). Full per-endpoint detail at `/reference`.
- **Async model (key!):** **Agent ID** = a Phantom (persistent); **Container ID** = one run. `POST /agent/{id}/launch` **queues** a run and returns a **containerId** — data isn't ready until that container finishes; then read **`/containers/fetch-result-object`**. The **`output`** launch param controls what you get. People's #1 confusion: expecting results in the launch response.
- **Webhooks:** set **per agent** (setup → **Advanced Notification Settings**). **Auth = a `secret` via query param** (webhooks **cannot send custom headers** → verify the secret, not a header signature). **11-second timeout** — exceed it → cancelled + treated as server error. So **return 200 fast, process async**.
- **Limits:** **execution time** (monthly run-hours: 20/80/300 by tier), **Phantom slots** (concurrency: 5/15/50), **email credits** (500/2,500/10,000). **API on all paid plans** + unlimited CSV/JSON exports + up to 100 workspace members.
- **Pricing:** Start ~$56–69/mo, Grow (mid), Scale ~$439/mo; annual saves ~19–20%. Verify.
- **Risk/compliance:** Phantoms run **as your account** via your **session cookie** (LinkedIn `li_at`) — aggressive volumes can get the account restricted; cookies expire (refresh). Scraping LinkedIn/sites is a **ToS/legal gray area** — use responsibly. Account-safety strategy → `/sales-linkedin`.
- **Competitive set:** Clay (data canvas), **TexAu**, Captain Data, Bardeen, Evaboot, Waalaxy, Dux-Soup. PhantomBuster's angle: huge Phantom catalog + API + cloud execution.

⚠️ **Fetch note for future runs:** the marketing homepage is JS-rendered (thin to WebFetch); use **hub.phantombuster.com/docs/api** + `/reference` (fetchable) for API detail, and **support.phantombuster.com** for plans/limits. Confirmed: base URL + auth header + JSend + Agents/Containers/Storage groups + launch→container→result flow + webhook secret/11s. Gaps: exact Storage paths, per-endpoint JSON, current exact prices.
