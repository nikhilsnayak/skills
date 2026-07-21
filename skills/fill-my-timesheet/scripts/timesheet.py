#!/usr/bin/env python3
"""Reusable engine for the CodeCraft timesheet API (timesheet.codecraft.in).

This handles the *mechanical* parts safely and deterministically: auth, the
authoritative calendar, leave records, listing your entries with their ids,
idempotent posting, deletion, and verification. The *judgement* parts
(parsing an arbitrary spreadsheet, deciding how to distribute hours) live in
SKILL.md and stay with the model, because they vary per person/team.

Auth (never hard-code): set the session cookie in the environment.
    export TIMESHEET_COOKIE='accessToken=...; refreshToken=...'
Grab it from the browser DevTools (Application > Cookies) or by copying any
authenticated request as cURL and lifting the `-b`/cookie value.

Usage:
    python timesheet.py whoami
    python timesheet.py calendar <month> <year>
    python timesheet.py leaves
    python timesheet.py list <YYYY-MM-DD> <YYYY-MM-DD>
    python timesheet.py post <entries.json> [--dry-run] [--limit N] [--force]
    python timesheet.py delete <worklogId>
    python timesheet.py verify <month> <year>

entries.json is an array of objects:
    {"date":"2026-04-02","loggedHours":"08:00","description":"...",
     "projectId":"<uuid>","taskId":"<uuid>","location":"codecraftOffice"}
`id` is omitted/None for new entries. `post` skips any date that already has
one of *your* entries (idempotent) unless --force, so re-runs never duplicate.
"""
import json, os, sys, time, urllib.request, urllib.error

BASE = os.environ.get("TIMESHEET_BASE", "https://timesheet.codecraft.in")
COOKIE = os.environ.get("TIMESHEET_COOKIE", "")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36")  # non-bot UA: Cloudflare 403s urllib's default


def req(method, path, body=None):
    if not COOKIE:
        sys.exit("ERROR: set TIMESHEET_COOKIE (see script header).")
    url = path if path.startswith("http") else BASE + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "cookie": COOKIE, "user-agent": UA,
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "referer": f"{BASE}/dashboard/tracker", "origin": BASE,
    })
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, json.loads(resp.read() or "{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or "{}")
        except Exception: return e.code, {"error": str(e)}


def me():
    st, d = req("GET", "/api/v2/auth/isAuthenticated")
    if not d.get("isAuthenticated"):
        sys.exit(f"Not authenticated ({st}). Refresh TIMESHEET_COOKIE. {d}")
    return d["user"]["payload"]  # {id, email, role}


def my_entries(frm, to):
    """Your worklog entries in [frm,to] (YYYY-MM-DD), with ids."""
    uid = me()["id"]
    st, d = req("GET", f"/api/v2/worklog/list?dateFrom={frm}T00:00:00.000Z&dateTo={to}T23:59:59.999Z")
    return uid, [r for r in d.get("data", []) if r.get("employeeId") == uid]


def cmd_whoami():
    print(json.dumps(me(), indent=2))


def cmd_calendar(month, year):
    uid = me()["id"]
    st, d = req("GET", f"/api/v2/worklog/employeeReport/{uid}/{month}/{year}")
    rows = d["data"]["resourcesWorklog"]
    work, holiday, weekoff = [], [], []
    for r in rows:
        day = r["workDate"][:10]
        if r.get("isWeekOff"): weekoff.append(day)
        elif r.get("isCompanyOff"): holiday.append(day)
        else: work.append(day)
    st, l = req("GET", "/api/v1/leaves")
    pref = f"{int(year):04d}-{int(month):02d}"
    leaves = []
    for lv in l.get("data", []):
        fr, to = lv["fromDate"][:10], lv["toDate"][:10]
        if fr.startswith(pref) or to.startswith(pref):
            leaves.append({"from": fr, "to": to, "type": lv.get("typeOfLeaveForFrom")})
    out = {"working_days": work, "holidays": holiday, "leaves": leaves}
    print(json.dumps(out, indent=2))


def cmd_leaves():
    st, d = req("GET", "/api/v1/leaves")
    for lv in d.get("data", []):
        print(f"{lv['fromDate'][:10]} -> {lv['toDate'][:10]}  {lv.get('typeOfLeaveForFrom')}  "
              f"approver={lv.get('approver') or '(pending)'}")


def cmd_list(frm, to):
    uid, mine = my_entries(frm, to)
    for r in sorted(mine, key=lambda x: x["workDate"]):
        print(f"{r['workDate'][:10]}  {r['minutes']:>4}m  leave={str(r.get('isOnLeave')):5}  "
              f"id={r['id']}  {r.get('description','')[:55]}")
    print(f"# {len(mine)} entries")


def cmd_delete(wid):
    st, d = req("DELETE", f"/api/v1/worklog/{wid}")
    print(st, json.dumps(d)[:200])


def cmd_post(path, dry_run=False, limit=None, force=False):
    entries = json.load(open(path))
    if not entries:
        sys.exit("no entries")
    dates = [e["date"] for e in entries]
    frm, to = min(dates), max(dates)
    uid, existing = my_entries(frm, to)
    have = {r["workDate"][:10] for r in existing}
    todo = entries if force else [e for e in entries if e["date"] not in have]
    if limit is not None:
        todo = todo[:limit]
    skipped = len(entries) - len(todo)
    print(f"{'DRY-RUN ' if dry_run else ''}posting {len(todo)} (skipping {skipped} already-logged/over-limit)")
    ok, fail = 0, []
    for e in todo:
        payload = {"id": e.get("id"), "date": e["date"], "projectId": e["projectId"],
                   "taskId": e["taskId"], "description": e["description"],
                   "loggedHours": e["loggedHours"], "location": e.get("location", "codecraftOffice")}
        if dry_run:
            print(f"  WOULD POST {e['date']}  {e['loggedHours']}  {e['description'][:55]}")
            continue
        st, d = req("POST", "/api/v2/worklog/daily-log", payload)
        if st in (200, 201):
            ok += 1; print(f"  OK  {e['date']}  {e['loggedHours']}  {e['description'][:50]}")
        else:
            fail.append((e["date"], st, d)); print(f"  ERR {st} {e['date']}  {json.dumps(d)[:120]}")
        time.sleep(0.35)
    if not dry_run:
        print(f"posted {ok}/{len(todo)}")
        for d_, s_, b_ in fail: print(f"  FAIL {d_} {s_} {b_}")


def cmd_verify(month, year):
    uid = me()["id"]
    st, d = req("GET", f"/api/v2/worklog/employeeReport/{uid}/{month}/{year}")
    data = d["data"]
    logged = [r for r in data["resourcesWorklog"] if r["minutes"] > 0]
    mins = sum(r["minutes"] for r in logged)
    leave = [r["workDate"][:10] for r in data["resourcesWorklog"] if r.get("isOnLeave")]
    print(f"{data.get('resourceName')}  {month}/{year}: work_days={len(logged)}  "
          f"hours={mins/60:.2f}  totalDays={data.get('totalDays')}")
    if leave: print(f"  work logged on LEAVE days (fix these): {leave}")


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    c = a[0]
    if c == "whoami": cmd_whoami()
    elif c == "calendar": cmd_calendar(a[1], a[2])
    elif c == "leaves": cmd_leaves()
    elif c == "list": cmd_list(a[1], a[2])
    elif c == "delete": cmd_delete(a[1])
    elif c == "verify": cmd_verify(a[1], a[2])
    elif c == "post":
        cmd_post(a[1], dry_run="--dry-run" in a, force="--force" in a,
                 limit=(int(a[a.index("--limit")+1]) if "--limit" in a else None))
    else: sys.exit(f"unknown command {c}\n{__doc__}")


if __name__ == "__main__":
    main()
