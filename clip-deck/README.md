# Clip Deck

The engine for the course's short vertical videos. A clip is one HTML page. It puts your camera, an animation of code and diagrams, and captions on a single 1080×1920 stage. You step through it with the space bar and record it straight from Chrome.

The clips themselves live in [`social-scripts/`](../social-scripts/). From the repo root:

```bash
pnpm social
```

```bash
pnpm social:new 02-embeddings
```

```bash
pnpm social:check 02-embeddings
```

| Command | Does |
|---------|------|
| `pnpm social` | Serves the clips at <http://127.0.0.1:8765/>. The camera and recording only work from a served page. |
| `pnpm social:new 02-slug` | Starts a clip from [`template/`](template/): an `index.html` and a `script.md`. |
| `pnpm social:check 02-slug` | Steps through the clip in Chrome with a fake camera. It lists every caption, reports anything cut off, and saves a picture of every step to `social-scripts/output/02-slug/`. `sheet.png` there shows them all at once. Leave out the slug to check every clip. |

## What's in it

| File | Does |
|------|------|
| `src/player.js` | Steps through the frames, shows the captions, runs the camera, and records the stage |
| `src/backdrop.js` | The slow WebGL horizon behind everything |
| `src/style.css` | The stage layout and every component below |
| `template/` | The starting point for a new clip |
| `cli.mjs` | The `serve`, `new` and `check` commands |

## A clip page

```html
<body data-clip="02-embeddings">
  <main class="stage">
    <header class="byline">
      <p class="name">Nicholas Johnson</p>
      <p class="brand">Agent Engineering · Embeddings</p>
    </header>

    <section class="frame" data-camera="full">
      <p class="cue">I'm going to explain <em>embeddings</em> to you in sixty seconds.</p>
    </section>

    <section class="frame">
      <p class="cue">First caption on this frame.</p>
      <p class="cue">Second caption: the card appears.</p>
      <h1>A heading</h1>
      <div class="card ai" data-in="1">…</div>
    </section>
  </main>
</body>
```

- **The `<head>`** links `/clip-deck/style.css` and loads `/clip-deck/backdrop.js` and `/clip-deck/player.js` with `defer`. The template already does this.
- **`data-clip`** on the body names the recordings: `02-embeddings-14-32-05.mp4`.
- **Each `<section class="frame">`** is one screen. Frames play in order.
- **A frame's steps:** each press of space moves one step. A frame has one step per caption, or more if its builds need them.

## Markers

| Marker | Does |
|--------|------|
| `<p class="cue">` | One caption per step, in order. It is both the autocue and the viewer's subtitle. `<em>` shows in yellow. |
| `data-camera="full"` on a frame | The camera fills the stage. Use it for the promise and the sign-off. |
| `data-in="n"` | Appears at step n. `0` means as the frame arrives, which is useful with a `--delay`. |
| `data-out="n"` | Disappears at step n. |
| `data-at="n"` | Gets the class `reached` at step n. It drives the effects below. |
| `style="--delay: 0.8s"` | Holds back an appearance, for example to stagger three rows. |
| `class="type"` | Types itself out, one character at a time. Monospace text only. |
| `class="stream"` | Appears word by word, like a streamed AI reply. |
| `<div class="swap">` | Stacks its children in one place, for a heading that changes: one with `data-out="n"`, the next with `data-in="n"`. |

## Components

| Component | Looks like |
|-----------|------------|
| `<h1>` | A big white heading. Two short lines at most. |
| `<div class="bubble you">` | Your question: a blue chat bubble on the right |
| `<div class="bubble ai">` | The AI's reply: an outlined bubble on the left |
| `<div class="card ai\|python\|gmail\|calendar">` with `<p class="who">` and `<p class="says">` | A labelled card with a coloured top edge |
| `<div class="servers">` holding `.card`s with `<h2>` and `<p>` | A stack of named cards |
| `<div class="compare">` holding two `.card`s with `<h2>` and `<ul>` of `<li class="yes\|no">` | Two cards side by side, with ticks and crosses |
| `<div class="answers">` holding `.answer` rows of `<span>label</span><span class="number type">` | Numbers stacked to compare. Mark one row `.right`. With `data-at`, the digits where the others leave the right one turn red. |
| `<pre class="code">` | Python, coloured automatically |
| `<pre class="code grow" data-at="n">` | Lines starting `+ ` (or a lone `+`) stay folded away, then open up in green at step n |
| `<p class="result">`, `<p class="note">` | A line of output, or a muted sentence |
| `<div class="arrow">↓</div>` | A down arrow between cards |

## The stage

The stage is 1080×1920. Keep within these limits; `pnpm social:check` reports anything cut off.

- **0–136px:** left for the platform's own buttons.
- **136–240px:** your name and the course, on every frame.
- **270–1150px:** the frame. That's 880px tall, and frames are centred in it. A frame that is too tall runs into the camera box.
- **1180–1780px:** the camera box. The caption sits over its bottom edge.
- **Code is 32px Menlo,** so about 45 characters fit on a line. Wrap anything longer.
- **Captions are 46px bold,** so about 40 characters fit on a line. Keep each caption to two lines: one short sentence.

## Recording

Open the clip in Chrome, press **F** for full screen, then **R**. Chrome asks what to share: choose **This tab**. After a three-second countdown, you're recording.

| Key | Does |
|-----|------|
| Space, →, Page Down, Enter or a click | Next step |
| ←, Page Up or Backspace | Back one |
| Home | Start again |
| R | Start or stop recording |
| C | Next camera |
| F | Full screen |

Press R again to stop. The take is saved to Downloads as an MP4 of just the stage, with your microphone. On a Retina Mac it comes out at about 1100×1960. The address ends `#frame.step`, so reloading keeps your place.
