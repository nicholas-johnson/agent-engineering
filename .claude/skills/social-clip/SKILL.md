---
name: social-clip
description: Make a new short vertical video (a "social clip") that promotes the Agent Engineering course. Use when asked to make, script, build or change a social clip, reel, short or TikTok in social-scripts/.
---

# Making a social clip

A social clip is a 60-to-90-second vertical video that teaches one useful idea from the course. Nicholas records it himself: a web page shows his camera, an animation and captions on one stage, and he presses space to move through it. You write the script and build the page.

Read these first:

- `social-scripts/README.md`: the five beats, and how a clip is recorded
- `social-scripts/01-square-root/`: a finished clip. Copy its patterns.
- `clip-deck/README.md`: the markers, the components and the stage's limits

## The shape of every clip

1. **The promise**, full-face: "I'm going to explain *X* to you in sixty seconds." It must be useful, and the clip must keep it in that time.
2. **The odd thing:** something surprising that really happened, shown before it is explained. A real demo from the course is best.
3. **The reveal:** how it works, in plain words. The technical term comes last.
4. **The payoff:** one line they could repeat to a friend, plus a real-world example or two.
5. **The sign-off**, full-face, word for word: "I'm Nicholas Johnson. I'm a principal dev working with AI. I'm doing a series on AI fundamentals. Follow if you'd like to know more."

## Steps

1. **Agree the idea first.** Propose to Nicholas the promise, the odd thing (which demo, and what output), the reveal and the payoff, in a few lines. Wait for a yes before building.
2. **Find the real material.** Use output from a module's README, or run the demo. Never invent output or numbers. For any real-world claim (a product, a server, a feature), check a primary source and note it with the date.
3. **Start the clip:** `pnpm social:new NN-slug`, numbered after the last clip in `social-scripts/`.
4. **Write `script.md`:** the five beats, what's on screen, the captions table, the post text, notes, and a table saying where each piece of material came from.
5. **Build `index.html`:** one `<section class="frame">` per screen. Write each spoken sentence as a `<p class="cue">`, which is both the autocue and the caption. Make things appear with `data-in`, and use the components in the clip-deck README. Set the byline's module name. For a neural network diagram, use `network.js` with a `scene.js`, as in clip 2; for a map of embeddings, `space.js`, as in clip 3. Don't hand-draw SVG.
6. **Watch the motion.** The check's pictures show only where each step ends up. Open the clip in Chrome and step through it, to see that the animations read well.
7. **Check it:** `pnpm social:check NN-slug`. Fix every problem it reports, then look at `social-scripts/output/NN-slug/sheet.png`, which shows every step. Read the estimated length: if the part before the sign-off runs over the promise, cut lines.
8. **Update `social-scripts/README.md`:** add the clip to the table.
9. **Hand over:** tell Nicholas to run `pnpm social`, open the clip in Chrome and press R. Commit only when asked.

## Rules

- **Captions:** one short sentence each, two lines at most (about 80 characters). Use `<em>` for the one word that matters; it shows in yellow.
- **Code on screen:** it must be the real code, squeezed to fit. Wrap at about 45 characters, and say in the notes what you changed.
- **Never fill a gap with made-up output.** If a demo can't run, say so and ask.
- **Writing:** British English, plain words, short sentences.
- **New components** go in `clip-deck/src/style.css`, and must be added to the table in the clip-deck README, so every clip can use them.
