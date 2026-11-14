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
| `src/network.js` | An SVG engine for neural network diagrams: see [Networks](#networks) |
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
| `<section class="frame top">` | A frame whose content sits at the top, leaving the space below for a graphic such as a network |

## Networks

`src/network.js` draws neural networks on the stage and animates them: neurons and weights, data travelling forwards, error travelling backwards, probability bars, and a camera that zooms out over a field of copies. [Clip 2](../social-scripts/02-how-ai-learns/) uses it throughout.

Three things go on the page:

```html
<script src="/clip-deck/network.js" defer></script>
<script src="scene.js" defer></script>      <!-- before player.js -->
<script src="/clip-deck/player.js" defer></script>
…
<main class="stage">
  <svg class="network" id="net"></svg>
```

`scene.js` says what the network looks like at each step it changes. Keys are `"frame.step"`, as in the address bar:

```js
new Network("#net").script({
  "2.0": { layers: [2, 1], weights: { "0.0-0": -0.35, "0.1-0": -0.7 }, showWeights: true },
  "2.1": { pulse: "forward", values: { "0.0": 1, "0.1": 1, "1.0": 0.26 }, showValues: true },
  "2.3": { pulse: "backward", weights: { "0.0-0": 0.39, "0.1-0": 0.04 } },
});
```

A step's state is every entry up to it, so later entries only say what changes. Set a field to `undefined` to put it back to its default. Pressing back, or reloading, jumps straight to the right state. Effects such as pulses play only when you step forward. Neurons are named `"layer.index"` and weights `"layer.from-to"`, counting from 0, so `"0.1-0"` joins the second input to the first neuron in the next layer.

| Field | Does |
|-------|------|
| `layers: [3, 6, 5]` | Neurons in each layer. Changing it grows or shrinks the network, and anything that stays moves into place. |
| `box: { x, y, w, h }` | Where the network sits on the stage. Default: `{ x: 56, y: 480, w: 968, h: 660 }`, under a `frame top` heading. |
| `pad: { top, right, bottom, left }` | Room inside the box, for labels on the left and bars on the right |
| `radius`, `spacing` | Neuron size, and the gap between neurons in a layer. Worked out from the box if left out. |
| `weights: { "0.0-0": -0.35, random: 3, spread: 1 }` | Weights by name. Any not named are random, from the seed in `random`. Positive weights are blue, negative violet, and stronger ones thicker. |
| `nudge: 0.4` | Nudges every weight by a random amount up to this much, as if after backpropagation |
| `values: { "1.0": 0.26, random: 5 }` | How lit each neuron is, from 0 to 1. Any not named are 0, or random with a seed in `random`. |
| `showValues`, `showWeights` | Write the numbers inside neurons and along weights |
| `labels: { "0.0": "dark clouds" }`, `monoLabels` | Text beside a neuron: left of the inputs, right of the outputs, above the rest. `monoLabels` sets them in Menlo, for tokens. |
| `bars: { "2.0": { label: "the", value: 0.16 } }` | A labelled probability bar beside an output neuron, scaled to the biggest || `pulse: "forward"`, `"backward"`, or a list | Dots travel through the network, layer by layer: data forwards in white, error backwards in red. Neurons light up as the data reaches them, and weights change as the error passes. |
| `zoom: 90`, `zoomTime: 5000`, `field: true` | Pull the camera back that many times, around the network's box, over that many milliseconds. `field` fills the space with copies of the network. |
| `show: false` | Hide the network |

`pnpm social:check` runs with reduced motion, so the network jumps straight to each step's final state for the pictures.

The engine follows the player through `window.clip.steps`, which lists every step's key in order. It also listens for the `clip:step` event, which fires on `document` with `{ key, index, forward }`. Any other script can follow along the same way.

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
