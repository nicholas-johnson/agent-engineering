# Social scripts

Scripts for short videos that promote the course. Each clip is a web page that puts you, an animation of the code and diagrams, and captions on one portrait stage, and records it straight from Chrome.

| Clip | Hook | Promotes |
|------|------|----------|
| 1. The square root: [script](01-square-root/script.md), [page](01-square-root/index.html) | "I'm going to explain MCP to you in sixty seconds." | Module 4: Tools |

## How a clip works

Each clip has five beats:

1. **The promise.** Say what they will learn and how fast: "I'm going to explain MCP to you in sixty seconds." It tells people why to keep watching. Make it a promise the clip can keep, in the time it says.
2. **The odd thing.** Then, in the style of Hannah Fry, show something surprising that happened, not a topic. Stop and let it land.
3. **The reveal.** Explain the mechanism in plain words. The technical term comes last.
4. **The payoff.** Keep the promise in one line they could repeat to a friend.
5. **The sign-off.** Full-face: "I'm Nicholas Johnson. I'm a principal dev working with AI. I'm doing a series on AI fundamentals. Follow if you'd like to know more." Then cut. The link to the course goes in the post text, not the video.

## Recording a clip

Serve the pages from the repo root. The camera and recording only work from a served page, not one opened as a file:

```bash
pnpm social
```

Then open <http://127.0.0.1:8765/01-square-root/> in Chrome, allow the camera and microphone, and press F for full screen.

1. Press **R**. Chrome asks what to share: choose **This tab**. A three-second countdown appears beside the stage.
2. The page opens on you, full-screen, with the first caption. Say it.
3. Press **space** for the next caption, then say it. The animation moves on with the captions. The script's **Captions and presses** table shows what happens on each press.
4. Press **R** again to stop. The take is saved to Downloads as an MP4, named after the clip and the time.

Press R again for another take: it starts again from the top.

| Key | Does |
|-----|------|
| Space, →, Page Down, Enter or a click | Next caption |
| ←, Page Up or Backspace | Back one |
| Home | Start again |
| R | Start or stop recording |
| C | Next camera, for example an iPhone through Continuity Camera |
| F | Full screen |

- **Only the stage is recorded.** The status beside it (recording time, camera and microphone, keys) is not.
- **The size comes from your screen.** The recording is the stage at its size on screen. Full screen on a Retina Mac gives about 1100×1960.
- **A presentation clicker works.** It sends Page Down, and it lets you keep your eyes on the camera.
- **The address ends `#frame.step`,** so reloading keeps your place.

## The stage

The stage is 1080×1920:

- **Your name and the course** sit at the top, between 136px and 240px, on every frame and over the camera too. Above them is left for the platform's own buttons.
- **The animation** sits between 270px and 1150px.
- **The camera box** is below the animation. The caption sits over the bottom of it.

On a frame marked `data-camera="full"`, the camera fills the stage.

`style.css` and `player.js` are shared by every clip, so a new clip needs only its own `index.html`. The top of `player.js` explains the markers that make things appear, change, type themselves out and become captions.

## Filming

- **The captions are the script,** so say the words as written. If a line doesn't sound like you, change it in `index.html`.
- **Pause after the hook.** You can tighten a pause in CapCut, but you can't add one you didn't record.
- **Big code:** code and terminal output on the stage need a very large font, 28pt or more.
- **Real numbers only:** every number and every line of output on the stage must come from a real run. Each script says where its material comes from.
