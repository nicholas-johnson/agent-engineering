# Browser extension

Build a small extension for Chrome or Edge that changes the pages you visit. The first one adds a reading time to the top of any article. Extensions are a good project for a coding agent: a handful of files, a format with strict rules (the manifest), and a result you can try in your own browser in seconds.

**Build it in:** Claude Code or Cursor. **Time:** an afternoon. **Needs:** Claude Code or Cursor, and Chrome or Edge.

## Start

In an empty folder:

> Build a Chrome extension, using the current manifest version, that adds a small "6 min read" label at the top of any page that looks like an article, based on its word count at 230 words a minute. Ask for as few permissions as possible, and explain each one you ask for. Then tell me exactly how to load it into Chrome.

Load it (Chrome's extensions page, developer mode, "Load unpacked") and try it on a few news sites and a few pages that aren't articles.

## Then

- "It shows on search results too. Only show it on pages with one main article."
- "Add a button that copies the article as Markdown, with its title and link."
- "Let me set my own reading speed in the extension's options."
- "Add a progress bar along the top as I scroll."

## Watch for

- **Permissions.** Read the manifest. Does it ask to read every website? Does it need to? Ask it to justify each one again.
- **Pages it breaks.** Try a few complicated sites. Does the label ever cover something?
- **Out-of-date advice.** Extension rules change. Did it use the current manifest version without being reminded?

## Try this

1. Make a second extension: a word counter under any text box you type in.
2. Add a page in the extension that lists the last twenty articles you read, with their reading times, stored only in your browser.
3. Make it work in Firefox too. What did it have to change?
4. Write an agent file, `.claude/agents/permissions-check.md`, that reviews the manifest after every change and argues for fewer permissions.
5. Read the store's rules for publishing an extension, and ask what you'd need to change to publish it.

## Questions

For discussion. There are no right answers.

- An extension can read every page you visit. How would you decide whether to install one someone else built with AI?
- You asked for "as few permissions as possible". How do you know it did?
- Which small annoyance in your own browsing would you build an extension for?
