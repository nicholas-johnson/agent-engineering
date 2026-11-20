# Social scripts

Short vertical videos that promote the course. Each clip is a web page built with [clip-deck](../clip-deck/). It puts your camera, an animation of the code and diagrams, and captions on one portrait stage, and records it straight from Chrome.

| Clip | Hook |
|------|------|
| 1. The square root: [script](01-square-root/script.md), [page](01-square-root/index.html) | "I'm going to explain MCP to you in ninety seconds." |
| 2. How an AI learns: [script](02-how-ai-learns/script.md), [page](02-how-ai-learns/index.html) | "I'm going to show you how an AI learns, in sixty seconds." |
| 3. Search by meaning: [script](03-search-by-meaning/script.md), [page](03-search-by-meaning/index.html) | "I'm going to explain embeddings to you in sixty seconds." |

## How a clip works

Each clip has five beats:

1. **The promise.** Say what they will learn and how fast: "I'm going to explain MCP to you in sixty seconds." It tells people why to keep watching. Make it a promise the clip can keep, in the time it says.
2. **The odd thing.** Then, in the style of Hannah Fry, show something surprising that happened, not a topic. Stop and let it land.
3. **The reveal.** Explain the mechanism in plain words. The technical term comes last.
4. **The payoff.** Keep the promise in one line they could repeat to a friend. Real-world examples make it concrete.
5. **The sign-off.** Full-face: "I'm Nicholas Johnson. I'm a principal dev working with AI. I'm doing a series on AI fundamentals. Follow if you'd like to know more." Then cut. The link to the course goes in the post text, not the video.

## Making a clip

Ask Claude Code for one. The [`social-clip` skill](../.claude/skills/social-clip/SKILL.md) walks it through the whole process. To do it by hand:

1. **Start it:** `pnpm social:new 02-slug` copies the template into `02-slug/`.
2. **Write `script.md` first,** and agree it before building anything.
3. **Build the frames** in `index.html`. The [clip-deck README](../clip-deck/README.md) lists the markers, the components and the stage's limits.
4. **Check it:** `pnpm social:check 02-slug` lists every caption, estimates the length, reports anything cut off, and saves a picture of every step to `output/02-slug/`.
5. **Record it,** as below.

## Recording a clip

Serve the pages from the repo root:

```bash
pnpm social
```

Then open the clip, for example <http://127.0.0.1:8765/01-square-root/>, in Chrome. Allow the camera and microphone, and press F for full screen.

1. Press **R**. Chrome asks what to share: choose **This tab**. A three-second countdown appears beside the stage.
2. The page opens on you, full-screen, with the first caption. Say it.
3. Press **space** for the next caption, then say it. The animation moves on with the captions. The script's **Captions and presses** table shows what happens on each press.
4. Press **R** again to stop. The take is saved to Downloads as an MP4, named after the clip and the time.

Press R again for another take: it starts again from the top.

- **A presentation clicker works.** It sends Page Down, and it lets you keep your eyes on the camera.
- **C switches camera,** for example to an iPhone through Continuity Camera.
- **Only the stage is recorded.** The status beside it is not.

## Filming

- **The captions are the script,** so say the words as written. If a line doesn't sound like you, change it in `index.html`.
- **Pause after the hook.** You can tighten a pause in CapCut, but you can't add one you didn't record.
- **Real numbers only:** every number and every line of output on the stage must come from a real run. Each script says where its material comes from.
