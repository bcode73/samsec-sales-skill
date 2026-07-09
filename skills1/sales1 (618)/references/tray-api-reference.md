# Tray.ai API Reference

<!-- Source: https://tray.ai/documentation/developer/openapi/embeddedapi/tag/overview/, https://tray.ai/documentation/developer/openapi/embeddedapi/tag/solutionInstances/, https://tray.ai/documentation/developer/getting-started/prerequisites/master-and-user-tokens, https://tray.ai/documentation/developer/developer-portal/getting-started/troubleshooting/rate-limiting-tray/. Re-verified against live docs 2026-06-13. Note: developer.tray.ai now 301-redirects to tray.ai/documentation/developer/. Some schema detail is only fully visible in the Postman/Insomnia collections. -->

> **Token requirement note (re-verified 2026-06-13)**: Tray's current docs assign Solution Instance lifecycle mutations to the **User token**, not the Master token. `createSolutionInstance`, `updateSolutionInstance`, `upgradeSolutionInstance`, and `removeSolutionInstance` are all titled "(user token)" in the official reference. Master token is used for org-wide setup (managing end users, creating user tokens, fetching connectors/operation schemas). See the mutation table below.

## API type

**GraphQL** — backend-only API.

> "The Tray GraphQL API is a backend API only and calls must be invoked server-side."

Client-side JavaScript calls are blocked by CORS. All API usage must originate from a server. This applies to both Tray Embedded and Intelligent iPaaS API consumers.

## Base URLs (regional)

| Region | Base URL |
|---|---|
| US | `https://tray.io/graphql` |
| EU | `https://eu1.tray.io/graphql` |
| APAC | `https://ap1.tray.io/graphql` |

Use the base URL that matches your Tray org's region. Querying the wrong region returns empty results without an obvious error.

## Authentication

Bearer token in `Authorization` header:

```
Authorization: Bearer <your-token>
```

Tray uses **two token types**. Per current docs: "All endpoints require either a master token or a user token passed as a bearer." "When using a Master token, you are the one taking actions (getting connectors, getting operation schemas etc.). When using a user token, your end users are performing the actions (creating an auth, calling a connector etc.)."

### Master Token
- **Scope**: Entire org workspace (the Embedded account owner/admin acts)
- **Obtained from**: Tray Embedded UI (workspace admin settings) — an admin/owner of the Embedded account creates it
- **Used for**: Org-wide setup — managing end users (`Get Users` / create / update / delete external users), creating user tokens (`authorize`), fetching connectors and operation schemas
- **Lifecycle**: Long-lived; rotate if compromised

### User Token
- **Scope**: Single end user (the end user acts)
- **Obtained via**: the "Create user token" mutation — underlying operation is **`authorize`** (takes `userId: ID!`, returns `accessToken`). Requires a Master Token to mint.
- **Used for**: Per-end-user operations — creating auths, calling connectors, and the **Solution Instance lifecycle** (`createSolutionInstance`, `updateSolutionInstance`, `upgradeSolutionInstance`, `removeSolutionInstance`)
- **Lifecycle**: Shorter-lived per-user session tokens

### Endpoints accepting both
Some operations accept either token, with results filtered by scope. `Get Solution Instances` (`get-solution-instances`) is titled "(user/master token)" — a master token returns instances org-wide, a user token returns only that end user's. Using a master token gives all auths in your org workspace while a user token only gives auths owned by that end user.

## OAuth redirect URLs

- **Default**: `auth.tray.io/oauth2/token`
- **Whitelabel**: `<your_org_name>.integration-authentication.com/oauth2/token`

For embedded deployments, configure your OAuth app in the external system (Salesforce, HubSpot, etc.) to redirect to the whitelabel URL matching your Tray org.

## Key API resources

- **Users** — end users of your embedded integration
- **Authentications** — stored OAuth/API-key credentials per user
- **Solutions** — reusable workflow templates
- **Solution Instances** — per-end-user copies of a Solution
- **Projects** — workspace organization
- **Workflows** — automation units within Solutions / Solution Instances
- **Call Connector operations** — programmatic connector invocation

## Key mutations / queries (Tray Embedded)

Operation names below use the friendly title and (in parentheses) the underlying GraphQL operation id from the official reference. Param types reflect the live schema as of 2026-06-13.

### End-user management (Master token)

| Operation | GraphQL op | Params | Returns | Token |
|---|---|---|---|---|
| Get users | query | — (paginated) | `name`, `id`, `externalUserId` | Master |
| Create new user | `createExternalUser` | `name: String!`, `externalUserId: String!` | created user | Master |
| Update user | `updateExternalUser` | `userId: ID!`, `isTestUser: Boolean` | updated user | Master |
| Delete user | `removeExternalUser` | `userId` | — | Master |
| Create user token | `authorize` | `userId: ID!` | `accessToken` | Master |
| Create Auth/Config dialog auth code | `generateAuthorizationCode` | `userId: ID!` | `authorizationCode` | Master |

`createUserAuthentication` returns an `authenticationId` which is then passed (with the external user ID) into `createSolutionInstance` when activating a Solution for an end user.

### Solution Instances

> All four Solution Instance mutations require a **User token** in current docs. `get-solution-instances` accepts user **or** master token.

#### Get solution instances (`get-solution-instances`) — user/master token
- **Parameters**: `ownerId: String!`
- **Returns**: collection of instances with `id`, `name`, `enabled`, `owner`, `created`, `workflows`, `authValues`, `configValues`

#### Create solution instance (`create-solution-instance`) — **User token**
- **Parameters**: `solutionId: ID!`, `instanceName: String!` (plus `authenticationId` from `createUserAuthentication` when activating for an end user)
- **Returns**: `id`, `name`, `enabled`, `created`, `workflows` (each workflow has its own trigger URL)

#### Update solution instance (`update-solution-instance`) — **User token**
- **Parameters**: `solutionInstanceId: ID!`, `instanceName: String!`, `enabled: Boolean!`
- **Returns**: `id`, `name`, `enabled`, `created`
- **Note**: This is the mutation used to **enable** an instance (set `enabled: true`) and rename it — it is the final step in activating an instance for an end user. (Config/auth values are set via `upgradeSolutionInstance`, not here.)

#### Upgrade solution instance (`upgrade-solution-instance`) — **User token**
- **Parameters**: `solutionInstanceId: ID!`, `configValues: [ConfigValue!]`, `authValues: [AuthValue!]`
- **Returns**: `id`, `configValues`, `authValues`, `enabled`, `created`
- Used to apply updated config/auth values and/or move to a newer Solution version.

#### Delete solution instance (`delete-solution-instance`) — **User token**
- **Parameters**: `solutionInstanceId: ID!`
- **Returns**: `clientMutationId`

### Activation timing gotcha
After an instance is **created**, if you auto-enable it for the end user, delay the enable call by **at least 2 seconds**. After an instance is **enabled**, wait **at least 2 seconds** before calling the Solution Instance's webhook/trigger URL. Skipping these delays causes intermittent failures.

## Rate limits

> "30 requests per second or 1800 requests per minute" across all Embedded APIs / Connectivity APIs **except** Call Connector.

**Burst**: "up to 50 requests per second" for momentary spikes, provided the overall window rate is not broken.

**Call Connector endpoint**: Concurrency-limited, not rate-limited. "1000 requests can be active at any given time." Increases available via CSM.

**Event delivery (Trigger API)**: Not rate-limited. Tray implements exponential backoff for downstream endpoints that rate-limit.

**HTTP response codes when rate-limited**: Not specified in public docs. Monitor for rate-limit error messages in GraphQL `errors` responses and implement exponential backoff.

## Error handling

GraphQL responses return **HTTP 200** even when the server encounters an error. Always inspect the `errors` array in the response body:

```json
{
  "data": null,
  "errors": [
    {
      "message": "...",
      "extensions": { "code": "..." }
    }
  ]
}
```

Do not rely on HTTP status codes alone.

## Testing tools

- **Postman collection** — official Postman workspace (check Tray docs for current link)
- **Insomnia GraphQL collection** — available for Insomnia users
- **GraphQL playground** — interactive query builder in the Tray Developer Portal

## Reference implementations

- **Official sample app**: `github.com/trayio/embedded-edition-sample-app` — Apollo GraphQL based, actively maintained (21 stars, last updated Feb 2026). Shows end-to-end Tray Embedded integration pattern in a Node.js/React app.
- **CDK examples**: `github.com/trayio/CDK-examples-public` — examples for building custom connectors with falafel.
- **Connector tester**: `github.com/trayio/connector-tester-public` — tooling for testing custom connectors.
- **Embedded custom JS**: `github.com/trayio/embedded-customjs-public` — patterns for custom JavaScript in embedded deployments.
- **falafel framework**: `github.com/trayio/falafel` — Node.js framework for building Tray connectors.

## Developer portal

- **Root**: `https://tray.ai/documentation/`
- **Embedded API overview**: `https://tray.ai/documentation/developer/openapi/embeddedapi/tag/overview/`
- **Solution Instances API**: `https://tray.ai/documentation/developer/openapi/embeddedapi/tag/solutionInstances/`
- **Master & user tokens**: `https://tray.ai/documentation/developer/getting-started/prerequisites/master-and-user-tokens`
- **Rate limiting**: `https://tray.ai/documentation/developer/developer-portal/getting-started/troubleshooting/rate-limiting-tray/`
- Note: `developer.tray.ai/...` URLs 301-redirect to `tray.ai/documentation/developer/...`.

## Agent Gateway for MCP (governance layer, current)

Separate from the Embedded GraphQL API, Tray now ships **Agent Gateway for MCP** — an enterprise control layer to spin up, version, publish, and deprecate **MCP Servers** on a governed path (700+ MCP servers derived from the connector library). It adds composite-tool consolidation to cut token usage (one customer cited 500+ → ~20 MCP tools), centralized RBAC over which agents/teams access which MCP tools, per-call tracing (user/agent/purpose), and dynamic OAuth within composite tools. Agents are managed as APIs and connected via MCP or A2A. See `https://tray.ai/platform/agent-gateway/`.

## Known gaps in public docs

- Specific HTTP response codes when rate limits are exceeded are not documented.
- Full OpenAPI/GraphQL schema is not published publicly; access via developer portal after auth.
- Partner / affiliate commission structure is not documented publicly.
- Exact per-tier task quotas on Pro/Team are not published consistently across sources.
