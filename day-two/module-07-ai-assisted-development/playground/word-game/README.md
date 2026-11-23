# Word game

Build a two-player word game of your own design that runs in one HTML file: no install, no server, works on a phone. Games are a good test of an agent because the rules have to be exactly right, and you'll know at once when they're not. You'll design the rules, have Claude Code build them, then play it and argue with it about what's fair.

**Build it in:** Claude Code (or Cursor). **Time:** an afternoon. **Needs:** Claude Code and a browser.

## Start

Write your rules down first, in a file called `RULES.md`. A starting point:

> Each player gets seven letters. Players take turns to make a word from their letters, scoring one point a letter, two for each letter used from the other player's last word. Used letters are replaced from a shared bag. The game ends when the bag is empty.

Then start `claude` in that folder:

> Build the game in RULES.md as a single HTML file, index.html, for two players sharing one phone. Check words against a word list you include in the file. Keep score, show whose turn it is, and say clearly why a word was refused.

Open `index.html` in a browser and play a full game before you ask for anything else.

## Then

- "When I played, X happened. RULES.md says Y. Fix it, and tell me which rule you misread."
- "Add a pass button, and end the game when both players pass twice."
- "Make it look like a board game: wooden tiles, a felt table."
- "Add a computer player that's easy to beat."

## Watch for

- **The rules it changed.** Compare what it built with `RULES.md`, line by line. Ask it to list every place it had to make up a rule.
- **The word list.** Where did it come from, and how big is it? Can you play swear words? Should you?
- **One file.** Did it keep everything in `index.html`, or start adding files and libraries?

## Try this

1. Write a test page, `test.html`, that plays fifty random games and checks the score always adds up.
2. Change a rule in `RULES.md` and ask it to update the game and the tests together.
3. Make it a game for two phones, over the internet. What does it say you need now?
4. Give the same `RULES.md` to Lovable. Which version would you rather play?
5. Invent a second game, a different one, and ask for both behind a menu.

## Questions

For discussion. There are no right answers.

- Writing `RULES.md` first is a plan. Did it save time, or would you rather have played first and fixed things?
- Who designed this game: you, or the model?
- A computer player that's easy to beat is harder to build than one that always wins. Why might that be?
