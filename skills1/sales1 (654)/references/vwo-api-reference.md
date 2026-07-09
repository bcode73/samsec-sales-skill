<!-- Source: https://developers.wingify.com/reference/introduction-1, https://developers.wingify.com/v2/docs/fme-rest-apis, https://developers.wingify.com/reference/api-rate-limits-1, https://developers.wingify.com/v2/docs/fme-configure-webhooks, https://help.vwo.com/hc/en-us/articles/360020559993 -->
<!-- Re-verified 2026-06-13. NOTE: the developer docs moved — developers.vwo.com now 301-redirects to developers.wingify.com. -->

# VWO API Reference

## Overview

VWO API is organized around REST and encodes data in JSON. API access is available on the **Enterprise plan only** (confirmed by the VWO Help Center: "This feature is only available in our Enterprise plan"). For questions or new app development, contact api@vwo.com.

Developer docs live at **developers.wingify.com** (the old `developers.vwo.com` URLs 301-redirect there).

## Authentication

Generate API tokens at: `https://app.vwo.com/#/developers/tokens`

Select the appropriate permission level for your use case. The token is passed in the request header — official docs state "Each API request is authenticated by a token in the request header." Tokens do **not** expire: "A user authentication token authorized to your application is not time-bound and is valid indefinitely without requiring you to re-authorize." Tokens can be revoked from the Control Panel.

## Rate limits

Per official docs (developers.wingify.com/reference/api-rate-limits-1): **"We rate limit 1 request per second for every token."** The limit is applied to the token, not the application — "Applications are not rate limited, though the limit is applied upon the token generated for an account." Organizations needing higher limits should contact VWO support. (Separately, VWO's pricing page lists an FME "API Access" allowance of 60,000 calls/month per the feature table.)

## SDKs (Feature Management & Experimentation)

VWO FME SDKs are available for multiple languages, all hosted on GitHub under the Wingify organization (Apache 2.0 license):

| Language | Package | GitHub |
|---|---|---|
| Node.js / Browser JS | `vwo-fme-node-sdk` | github.com/wingify/vwo-fme-node-sdk |
| Python | `vwo-fme-python-sdk` | github.com/wingify/vwo-fme-python-sdk |
| Java | `vwo-fme-java-sdk` | github.com/wingify/vwo-fme-java-sdk |
| PHP | `vwo-fme-php-sdk` | github.com/wingify/vwo-fme-php-sdk |
| Ruby | `vwo-fme-ruby-sdk` | github.com/wingify/vwo-fme-ruby-sdk |
| Go | `vwo-fme-go-sdk` | github.com/wingify/vwo-fme-go-sdk |
| .NET | `vwo-fme-dotnet-sdk` | github.com/wingify/vwo-fme-dotnet-sdk |
| React (web) | `vwo-fme-react-sdk` | github.com/wingify/vwo-fme-react-sdk |
| Flutter | `vwo-fme-flutter-sdk` | github.com/wingify/vwo-fme-flutter-sdk |
| React Native | `vwo-fme-react-native-sdk` | github.com/wingify/vwo-fme-react-native-sdk |
| Android | `vwo-fme-android-sdk` | github.com/wingify/vwo-fme-android-sdk |
| iOS | `vwo-fme-ios-sdk` | github.com/wingify/vwo-fme-ios-sdk |

### OpenFeature Providers

| Language | GitHub |
|---|---|
| Node.js | github.com/wingify/vwo-openfeature-provider-node |
| Python | github.com/wingify/vwo-openfeature-provider-python |
| Java | github.com/wingify/vwo-openfeature-provider-java |
| Go | github.com/wingify/vwo-openfeature-provider-go |
| PHP | github.com/wingify/vwo-openfeature-provider-php |
| .NET | github.com/wingify/vwo-openfeature-provider-dotnet |

### MCP Server

`vwo-fme-mcp` — Model Context Protocol server for AI agent integration with VWO feature flags. GitHub: github.com/wingify/vwo-fme-mcp

### GitHub Action

`vwo-fme-github-action` — Evaluate feature flags in CI/CD pipelines. GitHub: github.com/wingify/vwo-fme-github-action

## FME REST APIs (Enterprise only)

### Feature Flag APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | Get All Feature Flags of a Workspace | Retrieve all feature flags configured within a workspace |
| GET | Get Details of a Specific Feature Flag | Fetch detailed information about a specific feature flag using its ID |
| POST | Create a Feature Flag | Create a new feature flag by specifying name, key, and configurations |
| PATCH | Update a Feature Flag | Modify existing flag attributes (name, description, tags, key) |

### Feature Flag Rules APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | Get Feature Flag Projects and Environments | Fetch the list of projects and environments a flag is assigned to |
| GET | Get All Feature Flag Rules | List all rules configured for a given feature flag |
| GET | Get Details of a Specific Feature Flag Rule | Access complete rule configuration details |
| POST | Create a Feature Flag Rule | Create a new rule with targeting conditions |
| PATCH | Update a Feature Flag Rule | Modify audience conditions, variations, or strategy |
| PATCH | Toggle Feature Flag Rule Status | Enable or disable rules without deletion |
| PATCH | Toggle Feature Flag Status for an Environment | Control flag activation per environment |
| DELETE | Delete a Feature Flag Rule | Permanently remove a rule from a flag |

## FME Webhooks

VWO Feature Experimentation can push **outbound webhooks** when SDK-relevant settings change (e.g. a feature flag is modified in the control panel). Source: developers.wingify.com/v2/docs/fme-configure-webhooks.

- **Trigger**: an event in the source system, e.g. a feature flag is modified.
- **Delivery**: HTTP POST to a configured Webhook URL.
- **Payload fields**:
  - `timestamp` — Unix timestamp of the change
  - `event` — currently always `settings_changed` for SDK-related updates
  - `action` — specific change indicator (e.g. `campaign_settings_changed`, `feature_flag_updated`)
  - `triggered_by` — usually `vwo`
- **Authentication**: API-key based, **not HMAC**. VWO "supports API key-based authentication using a secret key" and includes it in the request header as `x-vwo-auth: YOUR_SECRET_KEY`. Validate inbound webhooks by comparing this header to the secret you generated.
- **Configuration**: Configurations → Website and Apps → select the Default Project → enable the Webhook option in the Environment(s) section → provide the endpoint URL in the `Webhook URL` field → generate and securely store the secret key.

> The FME server-side SDKs also accept an optional `webhook_auth_key` so they can validate the `settings_changed` webhook and refetch settings.

## VWO Engage API

VWO Engage (web push notifications) has a separate API. See VWO Help Center for Engage-specific API key generation and endpoints.

## Segment Integration

Forward VWO experiment impressions to Segment using `@segment/analytics-next`. Package: `vwo-segment-analytics-next` on GitHub.

## Support

- API questions: api@vwo.com
- General support: support@vwo.com
- Developer docs: https://developers.wingify.com (old https://developers.vwo.com URLs redirect here)
- Help center: https://help.vwo.com
