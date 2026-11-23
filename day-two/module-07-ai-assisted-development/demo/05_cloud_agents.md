# Run sheet: cloud agents

The live demo for section 5. A cloud agent takes a task, works on its own computer in the cloud, and hands back a branch or a pull request. Start the tasks before the session: each takes from a few minutes to half an hour, and you can't speed it up on stage.

You need the project in a GitHub repository, and an account with each service you show. Checked against each service's documentation on 23 November 2026.

## Set up

Put the project on GitHub, as a private repository, with the tickets as issues. From the module folder:

```bash
MODULE="$PWD"
cp -R data/project ~/dormouse-dashboard && cd ~/dormouse-dashboard && git init -q && git add . && git commit -qm "Start"
gh repo create dormouse-dashboard --private --source . --push
for ticket in DOR-232 DOR-233 DOR-234; do
  gh issue create --title "$(head -1 "$MODULE/data/tickets/$ticket.md" | sed 's/^# //')" --body-file "$MODULE/data/tickets/$ticket.md"
done
```

## 1. Claude Code on the web

1. Open claude.ai/code (or the Code tab in the Claude app), choose the `dormouse-dashboard` repository, and paste the DOR-232 issue.
2. Close the tab. Come back when it's done: it pushed a branch. Read the diff in the changes card, then **Create PR**.
3. From a terminal, the same thing: `claude --cloud "Fix the bug in issue DOR-234"`. To carry on with a cloud session on your own machine: `claude --teleport`.

Point out: it read the repository's `CLAUDE.md`, as it does in the terminal. It runs in a fresh machine with limited internet unless you allow more.

## 2. Copilot in the cloud

1. On github.com, open the DOR-233 issue and assign it to **Copilot**.
2. Copilot opens a pull request and works on it. When it asks for review, read the diff.
3. Leave a review comment starting `@copilot` asking for one change, and watch it push again.

Point out: the task starts where the work already is, in an issue, and ends where it is already reviewed, in a pull request. It reads `AGENTS.md` and `CLAUDE.md` too.

## 3. Codex cloud

1. In Codex (the web or desktop app), choose **Work in → Cloud**, pick the repository, and paste DOR-234.
2. When it finishes, read the diff and the test output it shows, then open a pull request.

Point out: each task gets its own machine, and the agent has no internet while it works unless you turn it on.

## 4. Cursor Cloud Agents

1. At cursor.com/agents (or **Cloud** in the dropdown under Cursor's agent input), pick the repository and paste DOR-232.
2. It works on a branch and comes back with a pull request, with screenshots and logs.

## 5. A review nobody has to start

1. In Claude Code, in `~/dormouse-dashboard`, run `/install-github-app` and follow the steps. It adds the `anthropics/claude-code-action` workflow to the repository.
2. On one of the pull requests above, comment: `@claude Review this against the issue it fixes.`

Point out: a cloud agent wrote the change, and another agent reviews it. A person still decides whether to merge.
