---
name: goalswon
description: Use the GoalsWon CLI (@goalswon/cli, `goalswon` binary) to manage daily goals, targets, accountability check-ins, chat with a coach, and review progress. Trigger whenever the user mentions goalswon, daily goals, accountability coach, daily check-in, or asks to list/create/complete goals, send a chat to their coach, view targets, or check progress.
---

# GoalsWon CLI Skill

## Preflight

Before any GoalsWon task, run the install/auth check once:

```bash
bash "$(dirname "$0")/scripts/check.sh"
```

If it exits non-zero, follow the printed instructions and stop.

## Golden Rule: Always Use `--json`

Every command accepts `--json`. Always use it — stdout becomes machine-readable JSON, stderr carries status messages, and errors are `{"error": "message"}`. Pipe to `jq` for extraction.

```bash
goalswon goals list --today --json | jq '.[].title'
```

To make JSON permanent: `goalswon config set json true`

## Command Reference

### Auth & Health

| Command | Description |
|---------|-------------|
| `goalswon auth login <key>` | Save API key |
| `goalswon auth status` | Check who you're logged in as |
| `goalswon auth config` | Show config file path and API URL |
| `goalswon health` | Check API connectivity |

### Goals

| Command | Description |
|---------|-------------|
| `goalswon goals list --today` | Today's goals |
| `goalswon goals list --yesterday` | Yesterday's goals |
| `goalswon goals list --tomorrow` | Tomorrow's goals |
| `goalswon goals list --date YYYY-MM-DD` | Specific date |
| `goalswon goals list --status done` | Filter by status (`done`, `partial`, etc.) |
| `goalswon goals create "<title>" --today` | Create a goal for today |
| `goalswon goals create "<title>" --tomorrow` | Create for tomorrow |
| `goalswon goals create "<title>" --date YYYY-MM-DD` | Create for a specific date |
| `goalswon goals create "<title>" --today --tag <N>` | Create with a tag ID |
| `goalswon goals create "<title>" --today --status done` | Create already completed |
| `goalswon goals complete <id>` | Mark as done |
| `goalswon goals complete <id> --status partial` | Mark as partial |
| `goalswon goals complete <id> --date YYYY-MM-DD` | Complete on a specific date (recurring goals) |
| `goalswon goals delete <id>` | Delete a goal |
| `goalswon goals recurring` | List recurring goal templates |

### Days

| Command | Description |
|---------|-------------|
| `goalswon days list` | Recent days |
| `goalswon days list --from YYYY-MM-DD --to YYYY-MM-DD` | Date range |
| `goalswon days show --today` | Today's detail with goals |
| `goalswon days show --yesterday` | Yesterday's detail |
| `goalswon days show YYYYMMDD` | Specific date (compact format, e.g. `20260327`) |

### Targets

| Command | Description |
|---------|-------------|
| `goalswon targets list --month YYYYMM` | Monthly targets (e.g. `202603`) |
| `goalswon targets create "<title>" --month YYYYMM` | Create a target |

### Chat

| Command | Description |
|---------|-------------|
| `goalswon chat list` | Recent messages |
| `goalswon chat list --search "<query>"` | Search messages |
| `goalswon chat send "<message>" --client <id>` | Send message (coaches only) |

### Clients (Coaches Only)

| Command | Description |
|---------|-------------|
| `goalswon clients list` | All clients |
| `goalswon clients list --type premium` | Filter by type |
| `goalswon clients summary <id>` | Full client summary |

### Progress

| Command | Description |
|---------|-------------|
| `goalswon progress` | Last 30 days |
| `goalswon progress --from YYYY-MM-DD --to YYYY-MM-DD` | Custom date range |

### Config

| Command | Description |
|---------|-------------|
| `goalswon config set json true` | Always output JSON |
| `goalswon config set json false` | Back to human-readable |

## Date Formats

- `--date`, `--from`, `--to`: ISO format `YYYY-MM-DD` (e.g. `2026-03-27`)
- `days show` positional arg: compact `YYYYMMDD` (e.g. `20260327`)
- `--month` for targets: compact `YYYYMM` (e.g. `202603`)

Use `currentDate` from the session context for "today".

## Common Recipes

**What are my goals today?**
```bash
goalswon goals list --today --json
```

**Mark a goal as done by title** (never invent IDs — resolve first):
```bash
goalswon goals list --today --json | jq '.[] | select(.name | test("exercise"; "i")) | .id'
# then:
goalswon goals complete <id>
```

**Add a goal for tomorrow:**
```bash
goalswon goals create "Plan week" --tomorrow
```

**Recap yesterday:**
```bash
goalswon days show --yesterday --json
```

**How am I doing this month?**
```bash
goalswon progress --from 2026-05-01 --to 2026-05-27 --json
```

**Recent chat with coach:**
```bash
goalswon chat list --json | jq '.[:5]'
```

## Safety Rules

- **Never invent IDs.** Always `list --json` first, find the ID from the output, then act.
- **Confirm before deleting.** `goalswon goals delete <id>` is irreversible — ask the user to confirm.
- **API key handling.** If `auth status` fails, direct the user to `app.goalswon.com > Settings > API settings` and tell them to run `! goalswon auth login <YOUR_API_KEY>` themselves (the `!` prefix runs it in their terminal). Never ask them to paste the key into chat.
