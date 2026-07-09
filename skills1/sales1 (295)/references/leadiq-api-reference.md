<!-- Source: https://developer.leadiq.com/ , https://github.com/leadiq/dataiq-api-specs (apiary.apib), and the LeadIQ Public API Guide. Re-verified against live official docs 2026-06-13. -->
# LeadIQ GraphQL API Reference

## Endpoint

```
https://api.leadiq.com/graphql
```

## Authentication

HTTP Basic Authentication. Use your API key as the username with an empty password.

```
Authorization: Basic base64(api_key:)
```

API keys are found in: Settings → API Keys within your LeadIQ account.

## Rate Limits

- Free plans: 10 requests/minute
- Paid plans: 60 requests/minute

## Queries

### searchPeople
Find individuals by name, company, LinkedIn profile, email, or phone.

**Input filters**: name, company name, domain, LinkedIn URL, email address, phone number.

**Profile filters**: HasWorkEmail, HasVerifiedWorkPhone (filter by available contact info type).

**Returns**: Person records with name, LinkedIn details, current positions, verified emails (with status: verified/unverified/catchAll), phone numbers (with type: mobile/direct/work), education, social profiles.

### searchCompany
Find companies by name, domain, country, or LinkedIn URL.

**Returns**: Company profiles with technology stacks, funding information, revenue ranges, hierarchies, and employment trend analytics.

### flatAdvancedSearch
Advanced contact search returning a flat list of people.

**Filters**: job title, seniority level, role/function, company size, geography, technologies, funding status, industry classification.

**Sort options**: name, seniority, title, update date.

### groupedAdvancedSearch
Same as flatAdvancedSearch but results grouped by company.

### account
Retrieve current user account details, subscription plans, and usage statistics.

**Returns**: billable usage statistics, trial limits, subscription status.

> The official spec also exposes a `usage` meta query (`usage { planUsage { name usageType units cap } trialUsage { ... } subscription { status } }`) for tracking billable/trial usage and caps per period. The `planUsage` field accepts an optional `from` parameter (defaults to the current billing period).

### prospect
Retrieve a specific prospect by ID. Argument: `id: ID!`. Returns a `Prospect`.

### list
Retrieve a single list by ID. Argument: `id: ID!`. Returns a `List`.

### lists
Retrieve multiple lists with pagination. Arguments: `limit: Int` (default 25), `cursor: ID`. Returns a `ListConnection`.

### workatoToken
Generate authentication tokens for Workato integration.

## Mutations

### submitPersonFeedback
Report data corrections for contact information (mark a contact's email/phone as valid or invalid).

**This is a GraphQL mutation**, not a REST endpoint. It is sent as a POST to the same `https://api.leadiq.com/graphql` endpoint. Returns `ID!`. Argument: `input: ApiPersonFeedback!`.

`ApiPersonFeedback` fields include: `personId`, `linkedinUrl`, `linkedinId`, `name`, `companyId`, `companyName`, `companyDomain`, `title`, `value`, `status` (`ContactInfoStatus`: Correct/Invalid), `invalidReason` (`InvalidReason` enum), `type` (`ContactInfoType`: WorkEmail/PersonalEmail/WorkPhone/WorkMobile/etc.), `lastSeen`.

> The published apiary spec also documents an equivalent `markAsInvalid(input: MarkAsInvalidInput!)` GraphQL mutation that takes `workEmails`/`workPhones` arrays and returns a boolean. Either way, feedback flows through `/graphql` — there is **no** REST `/v1/feedback` endpoint.

### addProspectToList
Add a prospect to a list. Arguments: `listId: ID!`, `input: CreateProspectInput!`. Returns a `Prospect`.

### createList
Create a new list. Argument: `input: CreateListInput!`. Returns a `List`.

## Error Handling

**The API always returns HTTP 200.** You cannot rely on HTTP status codes to detect errors — instead, examine the `errors` array within the JSON response body.

- **Request-level errors** affect the entire request and appear in `extensions > response > status`.
- **Data-level errors** affect individual records and appear in `extensions > status`.
- A **`429 Too Many Requests`** value can appear in the `errors` array when too many requests are made with the same API key in a short window — this is **not** an HTTP status code, it is part of the response body. Retry later with exponential backoff.

(Some individual REST-style operation examples in the apiary blueprint show a `400` response with an `{ "error": "..." }` body for malformed requests, but the general GraphQL error contract is the HTTP-200-with-`errors`-array model above.)

## Premium Features

- **MobilePhone add-on**: Request premium personal mobile phones by passing `premiumDataAddOns: ["MobilePhone"]` on the search input (e.g. `searchPeople`); adds numbers to the `personalPhones` field. Costs extra credits (10 per phone reveal). Premium usage is disabled for trial accounts by default — contact LeadIQ to enable.
- **MCP access**: LeadIQ ships an official MCP (Model Context Protocol) Connector that connects AI platforms — Claude (Free/Pro/Teams), ChatGPT (Plus/Team/Enterprise), Cursor, and other MCP-compatible clients — directly to your LeadIQ account using natural language for contact enrichment, company enrichment, and advanced prospecting. Exposed tools include Get Account Details (plans, billing cycle, credit usage), Get Contact Tracking Balance, and Get Usage Statistics. See the LeadIQ help center "Using the LeadIQ MCP Connector" article for setup.

## Contact

API support: api@leadiq.com
Terms: https://leadiq.com/legal/terms-of-use
Developer portal: https://developer.leadiq.com/
