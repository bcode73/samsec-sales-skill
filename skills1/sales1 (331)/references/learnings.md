# Maximizer Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, Octopus API surface (base `https://api.maximizer.com/octopus`, POST-RPC: `/Authenticate`, `/Read`, `/Create`, `/Update`, `/Delete`, `/Validate`, `/BinaryUpload`, `/WorkflowStart`…), Read query syntax (Scope/Criteria/GroupBy/OrderBy + `Configuration.Drivers` searchers), base64 composite record `Key`s, per-edition rate limits (Core 30/10s, Business/Financial 90/30s), Webhooks API (`https://api.maximizer.com/webhooks`, `/v1/targets` + `/v1/subscriptions`, 2-second/3-attempt delivery, no HMAC), editions/pricing, and GitHub (`github.com/maximizercrm`: octopus-api, webhooks, ferret-api) captured from live sources on this date. Request/response JSON examples are verbatim from the official Postman collection and OpenAPI spec. Re-verify specifics against current docs before relying on them.
