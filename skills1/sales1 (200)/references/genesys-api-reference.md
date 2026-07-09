<!-- Source: https://developer.genesys.cloud/platform/api/ and https://all.docs.genesys.com/Developer/APIbyService -->
<!-- Note: Developer Center is fully JS-rendered — API docs could not be fetched verbatim via WebFetch. This reference is compiled from WebSearch results, help center articles, and status pages. Refresh by visiting https://developer.genesys.cloud/ directly. -->

# Genesys Cloud Platform API Reference

## Authentication

OAuth 2.0 required for all API access. Two grant types:

### Client Credentials
Single-step authentication for non-user applications (services, cron jobs, integrations).
- Client app provides OAuth client credentials → receives access token
- No user context — actions are performed as the OAuth client

### Code Authorization
Two-step authentication for user-facing applications.
1. User authenticates via sign-in form at `/oauth/authorize`
2. Application exchanges authorization code for access token at `/oauth/token`

### Creating OAuth clients
Menu > Admin > Integrations > OAuth > Add Client
- Configure grant type, redirect URIs, scope
- **Note (verified 2026-06-13)**: The Token Implicit Grant (Browser) option is being deprecated in two stages — **May 25, 2026** the option is no longer available for *creating* new OAuth clients (existing clients keep working and remain editable), and **May 24, 2027** it is removed completely. Genesys recommends migrating to **PKCE** (Proof Key for Code Exchange, an extension of the authorization code flow for public clients), per OAuth 2.0 Security Best Practice. Source: https://help.genesys.cloud/announcements/deprecation-token-implicit-grant-browser-option-for-oauth-authorization/

## Regional API Base URLs

| Region | API Base URL |
|---|---|
| US East | `https://api.mypurecloud.com` |
| US East 2 (FedRAMP / GovCloud) | `https://api.use2.us-gov-pure.cloud` |
| US West | `https://api.usw2.pure.cloud` |
| Canada | `https://api.cac1.pure.cloud` |
| Mexico (Central) | `https://api.mxc1.pure.cloud` |
| São Paulo | `https://api.sae1.pure.cloud` |
| Dublin | `https://api.mypurecloud.ie` |
| Frankfurt | `https://api.mypurecloud.de` |
| London | `https://api.euw2.pure.cloud` |
| Zurich | `https://api.euc2.pure.cloud` |
| Mumbai | `https://api.aps1.pure.cloud` |
| Seoul | `https://api.apne2.pure.cloud` |
| Sydney | `https://api.mypurecloud.com.au` |
| Osaka | `https://api.apne3.pure.cloud` |
| Tokyo | `https://api.mypurecloud.jp` |
| UAE | `https://api.mec1.pure.cloud` |

All endpoints follow pattern: `{base_url}/api/v2/{resource}`

> Region note (verified 2026-06-13): Mexico Central (`mxc1.pure.cloud`, AWS `mx-central-1`) is a newer core region. The OpenAPI/Swagger definition for any region is at `{base_url}/api/v2/docs/swagger`. Source: https://help.genesys.cloud/articles/aws-regions-for-genesys-cloud-deployment/

## Platform Client SDKs

| Language | Package |
|---|---|
| JavaScript | CJS, AMD, ES6 modules |
| Java / Android | Maven |
| Python | pip |
| .NET | NuGet |
| Go | go get |
| iOS | Swift/Objective-C |

## API Resource Categories

### Digital Messaging & Engagement
- Alerting
- External Contacts
- Open Messaging
- WebChat
- Web Messaging
- Widgets
- Predictive Engagement

### Inbound
- Analytics
- Callback
- Conversations
- Engagement
- Fax
- Flows
- Recording
- Routing

### Outbound
- CX Contact
- Outbound campaigns and contact lists

### Workforce Engagement Management
- Quality Management (evaluations, scoring)
- Workforce Management (forecasting, scheduling, adherence)
- Interaction Analytics

### Self-Service & Automation
- Architect (flows, prompts, grammars)
- CLI tools

### Unified Communications
- Content Management
- Geolocation
- Locations
- Notifications (WebSocket-based)

### Open Platform
- Authorization (roles, permissions, scopes)
- Billing
- GDPR (data subject requests)
- Groups
- Identity Provider (SSO)
- Integrations
- OAuth
- Organization
- Users
- Workspace

### Telecom
- Telephony
- SIP management

## Event Streaming & Notifications (verified 2026-06-13)

Genesys Cloud does **not** use traditional HMAC-signed outbound webhooks. Real-time events are delivered two ways:

### Notifications API (WebSocket — pull/subscribe model)
- `GET /api/v2/notifications/availabletopics` — list subscribable topics (categories of events: conversations, agent presence, routing, analytics, etc.)
- `POST /api/v2/notifications/channels` — create a notification channel (returns a WebSocket connect URI)
- `POST|PUT /api/v2/notifications/channels/{channelId}/subscriptions` — add/replace topic subscriptions on a channel
- Limits: up to **20 channels per user + application**; up to **1000 topics per WebSocket connection**. Messages arrive as JSON with `topicName`, `eventBody`, and metadata.
- Source: https://developer.genesys.cloud/notificationsalerts/notifications/ , https://developer.genesys.cloud/notificationsalerts/notifications/available-topics

### Amazon EventBridge integration (push model)
For scalable, near-real-time backend integrations, Genesys Cloud streams events to an AWS partner event source via the **Amazon EventBridge** integration. Configure in Admin with the AWS account ID, region, and event source suffix; matching notification events begin flowing within ~5 minutes of activation. Commonly used for Analytics Detail Events and Conversation Events into Lambda/data pipelines. Source: https://help.genesys.cloud/articles/about-the-amazon-eventbridge-integration/ , https://help.genesys.cloud/articles/configure-the-amazon-eventbridge-integration/

## Developer Tools

- **API Explorer**: Browser-based docs + inline request testing at developer.genesys.cloud
- **Platform API CLI (`gc`)**: Command-line interface for scripting and automation
- **Archy**: YAML-based Architect flow authoring for CI/CD pipelines
- **Notifications API**: WebSocket-based subscribe/topic event streaming (see Event Streaming section above)

## Rate Limits

**Default: 300 requests per minute, applied per OAuth token (client credential)** — not per organization or per user (verified 2026-06-13). Each client credential gets its own independent 300/min allowance, so creating additional OAuth clients is the supported way to raise effective throughput; limits can also be raised by opening a Genesys support case with justification. Exceeding the limit returns HTTP `429 Too Many Requests`. Some individual services/endpoints (e.g. Outbound, Data Actions in Architect flows) impose their own narrower limits. Full rate-limit docs at developer.genesys.cloud/platform/api/rate-limits (JS-rendered — header/Retry-After details could not be fetched verbatim). Monitor via the API Usage Report in the admin console. Sources: https://developer.genesys.cloud/platform/api/rate-limits , https://community.genesys.com/discussion/api-limits

## Scopes

Genesys Cloud uses scopes to control API endpoint access. Scope categories include:
- routing, conversations, analytics, users, groups
- architect, quality, workforce-management
- recording, telephony, integrations
- authorization, organization, gdpr, billing

Configure scopes per OAuth client based on required functionality.

## Status Monitoring

- Service status: https://status.mypurecloud.com/
- API status: https://status.mypurecloud.com/api
- Status history shows incident frequency and duration
