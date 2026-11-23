# Photo tidy

Build a script that tidies a folder of photos: rename each one by the date it was taken, move them into a folder per month, and list the likely duplicates. It's the kind of job Claude Code is best at, files and folders on your own computer, and the kind where a mistake is expensive. So you'll also make it safe: a dry run first, nothing ever deleted, and a hook that stops the agent running a delete command at all.

**Build it in:** Claude Code. **Time:** an afternoon. **Needs:** Claude Code, and a copy of some photos you don't mind losing. Never point it at the only copy.

## Start in plan mode

Make a folder, put twenty or so photos in `test-photos/` (copies), start `claude` there, and press Shift+Tab until it says plan mode:

> Write a script that renames the photos in a folder by the date they were taken (from the photo's own data, not the file's date), moves them into a folder per month like 2026-06/, and lists likely duplicates. It must never delete anything. It prints what it would do, and only does it when I add --apply. Test it on test-photos/.

Read the plan. Which language did it choose, and does it need anything installed? What does it do with a photo that has no date inside it?

## Then

- "Run it on test-photos/ without --apply, and show me what it would do."
- "Two photos taken in the same second get the same name. What happens? Fix it."
- "Write tests, using a few tiny made-up image files, for the dates, the names and the duplicates."
- "Add --undo, which puts everything back where it was, from a log the script writes."

## Make it safe

Add a hook so Claude Code can't run a delete command, whatever it decides. Ask Claude Code to write it:

> Add a PreToolUse hook to .claude/settings.json that blocks any Bash command containing rm, and tells you to ask me instead.

Then ask it to "clean up the test files", and watch the hook stop it.

## Watch for

- **Dry run first.** Did it really print without moving anything? Check the folder.
- **Permission prompts.** Which commands did it ask before running? Which mode were you in?
- **Duplicates.** Same file, or same picture? Ask it how it decides.

## Try this

1. Add an agent file, `.claude/agents/safety-check.md`, that reads the script and lists every line that could lose a file. Ask Claude to run it after every change.
2. Handle videos too, with the date from inside the file.
3. Make it find near-duplicates: the same shot taken three times in a row. Keep the sharpest.
4. Turn it into a skill, `.claude/skills/tidy-photos/SKILL.md`, so "tidy my photos" in any folder runs it.
5. Run it on your real photo library, on a copy, with `--apply`. Then `--undo`. Did everything come back?

## Questions

For discussion. There are no right answers.

- The hook blocks a command whatever the model decides. What else on your computer would you want guarded that way?
- "It must never delete anything" was in the prompt. Was that enough on its own? How would you know?
- You didn't read every line of the script. What did you check instead, and is that enough for your photos?
