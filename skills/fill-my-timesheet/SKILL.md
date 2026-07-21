---
name: fill-my-timesheet
description: >-
  Populate the CodeCraft timesheet (timesheet.codecraft.in) from a worklog
  spreadsheet — creating the daily worklog entries over the API. Use this
  whenever the user wants to fill, backfill, or bulk-log their timesheet /
  worklog / daily-log for a month or date range, or import worklogs from an
  Excel/CSV/Google Sheet or pasted table into the timesheet, or reconcile
  logged days against leaves and holidays. Trigger it even when they don't name
  the API — "log my hours for June", "my timesheet is empty", "import my
  worklog sheet", "I forgot to fill timesheet for last 3 months" all qualify.
  Do NOT use for generic spreadsheet parsing, for leave applications, or for
  timesheets on any system other than timesheet.codecraft.in.
---

# Fill my timesheet

Turn a worklog spreadsheet into daily entries in the CodeCraft timesheet, safely.
The API and its rules are identical for every employee (that value is captured in
`references/api-contract.md` and `scripts/timesheet.py`); what varies per person/team
is the **auth token**, the **project/task**, and the **spreadsheet layout** — those are
inputs. Keep the engine fixed and adapt only the inputs.

Reusability boundary: the engine is org-wide; project/task ids and sheet layout are
team-level (`config.json`); the token and date range are per-run.

## Before you start — gather inputs

1. **Auth / cookie.** Ask the user for their live session cookie and export it in the terminal:
   `export TIMESHEET_COOKIE='accessToken=...; refreshToken=...'`.
   - In Chrome/Edge: open the signed-in timesheet page, press F12, go to Application/Storage → Cookies → `timesheet.codecraft.in`, and copy the `accessToken` and `refreshToken` values.
   - In Firefox: open DevTools → Storage → Cookies and copy the same values.
   - If they only have a cURL request from the browser, copy the `-b`/cookie header and use that exact value.
   - Verify immediately with `python scripts/timesheet.py whoami`. If it fails, the cookie is stale or incomplete — ask them to re-copy it.
   - Never write the cookie to a file in the repo, never paste it into config.json, and never echo it back in the terminal output.
2. **Config.** Prefer a private per-user config in the home directory, not in the repo. Create
   `~/.config/codecraft-timesheet/config.json` (or `~/.codecraft-timesheet/config.json`) if it
   does not already exist. If the home-directory config is missing, seed it from
   `assets/config.example.json` and confirm the project, task, and sheet layout with the user.
   If the user has a previous local config, reuse it rather than creating a new one. A stable team
   on one project should cache ids here so you don't ask "which task?" every run.
   - Keep the cookie out of this file and out of the repo entirely.
   - If the user wants a reusable local setup, create the hidden folder and any needed asset files
     there (for example `~/.config/codecraft-timesheet/`), and reference that location first.
   - Only use the repo's `assets/` and `references/` files as templates or fallbacks; do not
     overwrite them unless the user explicitly asks for a repo-level change.
3. **Period.** Confirm the exact month(s) or date range to fill. If the user says "last month" or "June",
   resolve it explicitly before planning entries.
4. **Actual worklog data.** Gather the real source rows the user wants to import.
   - If they have a spreadsheet, ask for the file path or paste the rows directly. Ask for the actual columns that matter: date/week, description/task, hours/days, and person name.
   - If they have a Google Sheet or Excel file, ask them to share the sheet link or upload the file and tell you which tab to use.
   - If they already have logged work in the timesheet, inspect it first with `python scripts/timesheet.py list <from> <to>` so you can reconcile existing entries instead of duplicating them.
   - For a team sheet, identify the target person and carry forward merged name cells; do not assume the same person is on every row.
   - If the data is incomplete or ambiguous, stop and ask for clarification rather than guessing.

## Workflow

Read `references/api-contract.md` once up front — it explains the payload quirks
(`id:null`, date-only, auto-submit) that are easy to get wrong.

### 1. Establish the real calendar (don't guess it)
For each month run `python scripts/timesheet.py calendar <month> <year>`. It returns the
**working days**, **holidays** (`isCompanyOff`), and **approved leaves**. This is the source
of truth — never hand-compute weekends/holidays, and never place work on a holiday or leave day.
The whole point of pulling this is that the system already knows the user's real off-days.

### 2. Parse the source into normalized rows
Adapt to whatever the sheet looks like (use the `sheetLayout` hint in config). Normalize to a
per-period list of `{description, amount}` where amount is either **hours** or **days**
(1 day = 8h). For a team sheet, filter to the target person and carry forward merged
Name/Days cells. Preserve the source's own week/day structure if it has one — it tells you
which dates the work belongs to.

If the sheet is organized by week (date-ranged tabs), distribute **within each week**. If it's a
flat monthly list of tickets+days with no dates, distribute across the month's working days in order.

### 3. Map descriptions to a task
Resolve project/task names to UUIDs from `config.json` (or via
`GET /api/v2/project/resource/{id}` and `GET /api/v2/task/list/{projectId}`). The common case is
one default task for everything. If a description clearly belongs to a different task and there's
no obvious mapping, ask rather than guess — it's the user's official record.

### 4. Distribute to days → one entry per working day
Fill the period's working days to `hoursPerDay` (8:00), in source order:
- Walk the normalized items, packing each working day to 8h; an item spanning >8h continues to
  the next working day, and a day may combine several items (join their descriptions with ` | `).
- **Skip weekends, holidays, and leave days** from step 1 entirely.
- If a period has fewer hours than working days, leave trailing working days empty — those are
  genuine gaps (usually leave). Do **not** invent hours to fill them.
- Emit one object per day: `{date, loggedHours:"HH:mm", description, projectId, taskId, location}`
  into `entries.json`. Almost every day is `08:00`; a remainder day may be shorter.

### 5. Dry-run and get approval
Show the user the full day-by-day plan (`python scripts/timesheet.py post entries.json --dry-run`,
or a table). Posting auto-submits to their manager, so this approval gate is mandatory — never
bulk-write without it.

### 6. Post: test one, then the rest
- `post` is **idempotent**: it skips any date that already has one of the user's entries, so
  re-runs never duplicate.
- First post a single entry to confirm the payload works end-to-end:
  `python scripts/timesheet.py post entries.json --limit 1`, then `verify` (below).
- Then post the remainder: `python scripts/timesheet.py post entries.json`.

### 7. Verify
`python scripts/timesheet.py verify <month> <year>` reports logged days, total hours, and — 
critically — flags any work sitting on a leave day. Confirm totals match the source.

## Corrections (leaves, shifting)

Users often review and correct after the first pass. Common cases:
- **"I was on leave on day X"** → find the entry (`list <from> <to>`), `delete <id>`. If that work
  should still count, move it to an open working day that week (create a new entry there). If no
  open day exists, tell the user it will be dropped and let them decide.
- **"The work is on the wrong days / shift it"** → the source's week/day structure is authoritative.
  Delete the misplaced entries and recreate them on the correct working days.
- **Conflict between the user and the system** (e.g. they say "not on leave" but there's an approved
  leave record) → surface the evidence and let them decide before writing. Don't silently override
  either side.

## Non-negotiables (these are where it goes wrong)
- Confirm before every write; each post submits to a manager.
- Calendar + leaves come from the API, not from computation.
- Never log work on a holiday or leave day.
- Idempotency via `post`'s skip — don't disable `--force` unless you truly intend to duplicate.
- The token is a secret: runtime env only, never committed, never logged.

## Files
- `scripts/timesheet.py` — the engine: `whoami`, `calendar`, `leaves`, `list`, `post`
  (`--dry-run`/`--limit`/`--force`), `delete`, `verify`. Reads `TIMESHEET_COOKIE`.
- `references/api-contract.md` — endpoints, payload contract, and the debugging gotchas.
- `assets/config.example.json` — team config template (project/task ids, sheet layout).
