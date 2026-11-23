# Pub quiz

Build a quiz for a pub night, a classroom or a team social. The host runs it on a big screen; players join on their phones with a short code, answer against the clock, and watch a live leaderboard. It's a small app with three hard parts: sign-in for the host, players who don't sign in at all, and everyone's screen changing at the same moment.

**Build it in:** Lovable. **Time:** an evening. **Needs:** a Lovable account; the free plan's daily credits are enough for a first version.

## Start in Plan mode

> Build a quiz app for a pub quiz night. The host signs in, makes a quiz of picture and text questions, then runs it on a big screen. Players join on their phones with a four-letter code and a team name, with no account. Each question has a timer; when it runs out, the big screen shows the answer and a leaderboard.

Answer its questions, then read the plan before you approve it. Look for what it decided about players: can two teams have the same name? What happens if a phone loses signal?

## Then, one change at a time

- "The host can move to the next question early when every team has answered."
- "Score more points for answering quickly, up to double for an instant answer."
- "Add a picture round: the host uploads images, and players type what they show."
- "Make the phone screen work with one thumb: big buttons, nothing to scroll."

## Watch for

- **Live updates.** Open the game on two phones and the big screen. Does every screen change at the same moment? Lovable's built-in backend has realtime updates; ask it which parts use them.
- **Cheating.** Can a player see the answer before the timer ends? Ask in Chat mode: "Could a player find the answer by looking at the page's code?"
- **What it invented.** Rules you never gave it, such as negative marking or a maximum number of teams.

## Try this

1. Run a real quiz with friends or colleagues. Write down everything that went wrong, and fix it in one message each.
2. Add a round where teams draw on their phones, and the host picks the best drawing.
3. Let the host save a quiz and run it again next month with new teams.
4. Run the deep security scan. What does it say about players who have no account?
5. Sync the project to GitHub and open it in Claude Code or Cursor. Ask: "Explain how a player's answer gets from their phone to the leaderboard." Is it how you'd have built it?

## Questions

For discussion. There are no right answers.

- You described the game, not the screens. Which of the screens it made would you have designed differently, and does it matter?
- Players join with no account. What could go wrong, and how much would you care at a pub quiz? At a school?
- How would you know the app can handle 40 phones at once before the night itself?
