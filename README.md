# claude-skill-goalswon

A [Claude Code](https://claude.ai/code) skill for the [GoalsWon CLI](https://www.npmjs.com/package/@goalswon/cli) — manage daily goals, targets, accountability check-ins, and coach chat from the terminal.

## What This Skill Does

Teaches Claude how to:
- List, create, complete, and delete goals
- Browse daily summaries and progress
- Manage monthly targets
- Read and send coach chat
- Always use `--json` output for reliable parsing

## Prerequisites

```bash
npm install -g @goalswon/cli
goalswon auth login <YOUR_API_KEY>
```

Get your API key at [app.goalswon.com](https://app.goalswon.com) → Settings → API Access.

## Install

Clone this repo into your skills directory:

```bash
# Personal config
git clone git@github.com:liamkirsh/claude-skill-goalswon.git ~/.claude-personal/skills/goalswon

# Or standard Claude config
git clone git@github.com:liamkirsh/claude-skill-goalswon.git ~/.claude/skills/goalswon
```

Claude Code will automatically load the skill when you mention GoalsWon, daily goals, or accountability coaching.

## Usage

Once installed, just talk to Claude naturally:

- "What are my goals today?"
- "Mark 'Exercise' as done"
- "Add a goal for tomorrow: review PRs"
- "How did yesterday go?"
- "Show my progress this month"

## Files

- `SKILL.md` — the skill instructions loaded by Claude
- `scripts/check.sh` — verifies the CLI is installed and authenticated

## License

MIT — same as the upstream [`@goalswon/cli`](https://www.npmjs.com/package/@goalswon/cli) package.
