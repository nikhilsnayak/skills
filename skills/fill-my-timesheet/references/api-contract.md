# CodeCraft Timesheet API — contract

Base: `https://timesheet.codecraft.in`. Backend is NestJS/Express behind Cloudflare;
interactive Swagger lives at `/api/` (spec embedded in `/api/swagger-ui-init.js`).
This file is the ground truth so you don't have to re-discover it. All of it is
**org-wide constant** — the same for every CodeCraft employee.

## Auth
Cookie-based. A request needs the `accessToken` (and `refreshToken`) cookies from a
logged-in browser session. Pass them via `TIMESHEET_COOKIE`. Cloudflare rejects a
default urllib/bot User-Agent with 403 — always send a browser UA (the bundled
script does). Tokens expire (~1 day for access); on 401/403 the user must re-copy them.

Check: `GET /api/v2/auth/isAuthenticated` → `{isAuthenticated, user:{payload:{id,email,role}}}`.
`payload.id` is your **resourceId / employeeId** — used everywhere below.

## Create a worklog  — `POST /api/v2/worklog/daily-log`
```json
{ "id": null,
  "date": "2026-04-02",                 // date ONLY. A full ISO timestamp is rejected.
  "projectId": "<uuid>",
  "taskId": "<uuid>",
  "loggedHours": "08:00",               // "HH:mm"
  "description": "IGZ-1234: ...",
  "location": "codecraftOffice" }       // enum: codecraftOffice | home
```
Returns 201 with the created record. **Gotchas that cost real debugging time:**
- `id` must be JSON `null` for a new entry. `""` → 400 "id must be a UUID"; a random
  UUID → 500 (server tries to *update* a non-existent row).
- Multiple entries on the same date are allowed (report sums their minutes). This skill
  collapses to one entry/day, but the API does not require it.
- Posting creates the entry already in `submitted` status → it routes to the manager for
  approval. Treat every write as outward-facing; confirm before bulk-posting.

## Update / delete
- `PUT /api/v2/worklog/daily-log/{id}` — update (same body, real `id`).
- `DELETE /api/v1/worklog/{worklogId}` → 200 "Successfully Deleted Work Log".
  Works even on `submitted` entries. This is how you clear an entry off a leave day.

## Reads
- `GET /api/v2/worklog/employeeReport/{resourceId}/{month}/{year}` — **authoritative
  calendar.** `data.resourcesWorklog[]` has one row per calendar day with
  `isWeekOff`, `isCompanyOff` (holiday), `isOnLeave`, `minutes`, `taskName`, `workLogStatus`.
  Use this for working days + holidays; never hard-code a calendar.
- `GET /api/v1/leaves` — your leave records: `fromDate`,`toDate`,`typeOfLeaveForFrom`
  (`fullDay`/half), `approver`. Cross-check before writing — **never log work on a leave day.**
- `GET /api/v2/worklog/list?dateFrom=<ISO>&dateTo=<ISO>` — worklogs (org-wide feed) with
  **ids**; filter client-side by `employeeId == resourceId` to get yours. Needed for edits
  and for idempotent dedup.
- `GET /api/v2/project/resource/{resourceId}` — projects assigned to you (name → projectId).
- `GET /api/v2/task/list/{projectId}` — tasks for a project (name → taskId).

## Mapping helpers (per team, cache in config)
Project/task names in a spreadsheet must be resolved to UUIDs via the two endpoints above.
For a stable team on one project, cache the ids in `config.json` to skip the lookup and the
"which task?" question.
