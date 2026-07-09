<!-- Source: https://developer.monday.com/api-reference/reference/notetaker.md -->
<!-- Source: https://developer.monday.com/api-reference/reference/notetaker-other-types.md -->
<!-- Source: https://developer.monday.com/api-reference/docs/get-notetaker-meetings.md -->
<!-- Source: https://developer.monday.com/api-reference/docs/authentication.md -->
<!-- Source: https://developer.monday.com/api-reference/docs/rate-limits.md -->
<!-- Re-verified against live official docs 2026-06-13 -->

# monday.com Notetaker API Reference

## Authentication

- **Type**: API token in `Authorization` header
- **Eligible users**: Admins and Members have access to their own API tokens. Guests must use OAuth or shortLivedToken.
- **Viewers, deactivated users, and student accounts** cannot use the API.

## Base URL & Request Format

- **Endpoint**: `https://api.monday.com/v2`
- **Method**: All requests must be POST
- **Content-Type**: `application/json`
- **API version**: Notetaker queries require version **2026-04 or later**

## API Playground

Interactive testing: `https://monday.com/developers/v2/try-it-yourself`

---

## Query: `notetaker.meetings`

The top-level `notetaker` field returns a `NotetakerQueries` object. The `meetings` query on that namespace retrieves paginated meetings that have completed recordings.

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `limit` | `Int` | Maximum number of meetings to return. Default: `10`. Allowed range: 1–100. |
| `cursor` | `String` | Pagination cursor from the previous response's `page_info.cursor`. |
| `filters` | `MeetingsFilterInput` | Optional. Filter by meeting IDs, search text, or access level. |

### Return Type

`MeetingsResponse` — includes a `meetings` array and `page_info` for cursor-based pagination.

### Example Query

```graphql
query {
  notetaker {
    meetings(limit: 10, filters: { access: ALL }) {
      meetings {
        title
        start_time
        end_time
        recording_duration
        summary
        access_type
        meeting_link
        participants { email }
        topics {
          title
          talking_points { content }
        }
        action_items {
          content
          is_completed
          owner
          due_date
        }
      }
      page_info {
        has_next_page
        cursor
      }
    }
  }
}
```

---

## Meeting Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | `String` | Meeting title. |
| `start_time` | `String` | Meeting start time. |
| `end_time` | `String` | Meeting end time. |
| `recording_duration` | `Int` | Recording length in milliseconds. |
| `summary` | `String` | Meeting summary (markdown). |
| `access_type` | `MeetingAccess` | How the current user relates to the meeting. |
| `meeting_link` | `String` | Link to the meeting. |
| `participants` | `[Participant]` | People associated with the meeting. |
| `topics` | `[Topic]` | Discussion topics and talking points. |
| `action_items` | `[ActionItem]` | Action items captured from the meeting. |
| `transcript` | `[TranscriptEntry]` | Transcript segments with timing and speaker metadata. |

---

## Nested Types

### Participant

| Field | Type |
|-------|------|
| `email` | `String` |

### Topic

| Field | Type |
|-------|------|
| `title` | `String` |
| `talking_points` | `[TalkingPoint]` |

### TalkingPoint

| Field | Type | Notes |
|-------|------|-------|
| `content` | `String` | Content only — no `start_time` field available. |

### ActionItem

| Field | Type |
|-------|------|
| `content` | `String` |
| `is_completed` | `Boolean` |
| `owner` | `String` |
| `due_date` | `String` |

### TranscriptEntry

Transcript segments with timing and speaker metadata. Fields (per official `notetaker-other-types` docs):

| Field | Type | Notes |
|-------|------|-------|
| `text` | `String` | Transcript segment text. |
| `start_time` | `Float` | Segment start time. |
| `end_time` | `Float` | Segment end time. |
| `speaker` | `String` | Speaker label or name. |
| `language` | `String` | Language code or label for the segment. |

### MeetingsFilterInput

| Field | Type | Description |
|-------|------|-------------|
| `ids` | `[ID!]` | Filter by specific meeting IDs. |
| `search` | `String` | Filter by search text (matches title, participant name, or email). |
| `access` | `MeetingAccessFilter` | Filter by how the meeting is shared/owned relative to the current user. |

### MeetingAccess / MeetingAccessFilter enum

| Value | Meaning |
|-------|---------|
| `OWN` | Meeting owned by the current user (default for the MCP tool). |
| `SHARED_WITH_ME` | Shared directly with the user. |
| `SHARED_WITH_ACCOUNT` | Shared at the account level. |
| `ALL` | All meetings the user can access. |

### MeetingsResponse

| Field | Type |
|-------|------|
| `meetings` | `[Meeting]` |
| `page_info` | `PageInfo` |

### PageInfo

| Field | Type |
|-------|------|
| `has_next_page` | `Boolean` |
| `cursor` | `String` |

---

## Platform MCP: Get Notetaker Meetings

monday.com also exposes the notetaker through its **Platform MCP** server via a `Get Notetaker Meetings` tool (no separate GraphQL-only access required). Parameters:

| Param | Type | Notes |
|-------|------|-------|
| `ids` | array | Filter by specific meeting IDs. |
| `access` | string | `OWN` (default), `SHARED_WITH_ME`, `SHARED_WITH_ACCOUNT`, or `ALL`. |
| `search` | string | Search by title, participant name, or email. |
| `include_summary` | boolean | Adds the AI-generated summary. |
| `include_topics` | boolean | Adds discussion topics and talking points. |
| `include_action_items` | boolean | Adds action items. |
| `include_transcript` | boolean | Adds full transcript (can be very large). |
| `limit` | number | Results per page, 1–100. Default `25`. |
| `cursor` | string | Pass the `cursor` from the prior response's `page_info` for the next page. |

By default the response includes only `title`, `participants`, `start_time`, `end_time`, `meeting_link`, and metadata; transcript/summary/topics/action items are opt-in via the `include_*` flags. Source: https://developer.monday.com/api-reference/docs/get-notetaker-meetings.md

## Rate Limits

monday.com enforces account-wide rate limits on all API calls (no notetaker-specific override). Live limits as of 2026-06-13 (source: https://developer.monday.com/api-reference/docs/rate-limits.md):

- **Complexity**: single query capped at 5,000,000 (5M) complexity points. Per-minute complexity budget — app tokens 5M reads + 5M writes per minute; personal tokens 10M/min (1M/min for trial, NGO, and free accounts).
- **Requests per minute**: Enterprise 5,000 · Pro 2,500 · other tiers 1,000. Some endpoints have their own caps (e.g. board creation 40/min, group duplication 40/min, portfolio connections 15/min).
- **Daily calls** (reset midnight UTC): Free/Basic/Standard 1,000 · Pro 10,000 (soft) · Enterprise 25,000 (soft).
- **Concurrency**: Enterprise 250 · Pro 100 · other 40 simultaneous requests.
- **Per-IP**: 5,000 requests per 10 seconds.
- **Headers**: `RateLimit-Policy` (declared maximums) and `RateLimit` (current state — remaining quota `r`, reset time `t`).

## Supported Products

The monday.com API supports: monday work management, dev product, sales CRM, and service product. Workforms are not yet supported.
