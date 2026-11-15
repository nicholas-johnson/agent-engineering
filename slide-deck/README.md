# Slide Deck

Shared slide deck component for the React course. Each module can use this to create their own slide presentations.

## Usage

In your module's slides folder:

```jsx
// main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { SlideDeck } from "slide-deck";
import { slides } from "./slides";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <SlideDeck slides={slides} />
  </React.StrictMode>,
);
```

## Slide Types

### Title Slide

```js
{
  type: 'title',
  content: {
    title: 'Main Title',
    subtitle: 'Subtitle text',
    icon: 'IconName' // Lucide icon name
  }
}
```

### Standard Slide (bullet points)

```js
{
  type: 'standard',
  content: {
    title: 'Slide Title',
    points: ['Point 1', 'Point 2', 'Point 3'],
    emoji: 'IconName'
  }
}
```

### Code Slide

```js
{
  type: 'code',
  content: {
    title: 'Code Example',
    code: `const x = 1;`,
    highlights: ['Key point 1', 'Key point 2']
  }
}
```

### Credits

`standard`, `code`, `description`, `equation` and `image` slides accept an optional
`credit` string, rendered as small grey text under the slide body. Use it to cite a
paper behind the idea on the slide:

```js
{
  type: 'standard',
  content: {
    title: 'Consensus and conflict resolution',
    points: ['Voting', 'Ranked choice'],
    credit: 'Wang et al. (2022). "Self-Consistency Improves Chain of Thought Reasoning in Language Models." arXiv:2203.11171'
  }
}
```

### Network Slide (an animated neural network)

Draws a network with the clip deck's `network.js`, and plays it one step at a time. The right
arrow, space or enter plays the next step; the left arrow goes back one. On the last step, the
right arrow moves on to the next slide. The dots under the diagram show where you are, and click to
jump to a step. In the PDF export, the slide shows its last step.

```js
{
  type: 'network',
  content: {
    title: 'Learning',
    note: 'Optional small print',
    steps: [
      // Each step: a caption, and what the network looks like from here on.
      { caption: 'One neuron', layers: [2, 1], weights: { '0.0-0': -0.35, '0.1-0': -0.7 }, showWeights: true },
      { caption: 'It says **0.26**', pulse: 'forward', values: { '0.0': 1, '0.1': 1, '1.0': 0.26 }, showValues: true },
      { caption: 'Nudge the weights', pulse: 'backward', weights: { '0.0-0': 0.39, '0.1-0': 0.04 } },
    ],
  },
}
```

A step takes the same fields as a clip's `scene.js` (layers, weights, values, labels, bars, pulse,
nudge…): see the Networks section of the [clip-deck README](../clip-deck/README.md#networks). Each
step carries on from the one before. The drawing is 1300×700 by default; `stage` and `box` change
that.

### Comparison Slide (with bullet points)

```js
{
  type: 'comparison',
  content: {
    title: 'Compare Two Things',
    left: {
      label: 'Option A',
      items: ['Item 1', 'Item 2']
    },
    right: {
      label: 'Option B',
      items: ['Item 1', 'Item 2']
    }
  }
}
```

### Comparison Slide (with code blocks)

```js
{
  type: 'comparison',
  content: {
    title: 'Compare Code',
    left: {
      label: 'Before',
      code: `const x = 1;`
    },
    right: {
      label: 'After',
      code: `const x = 2;`
    }
  }
}
```

### Rules Slide (cards grid)

```js
{
  type: 'rules',
  content: {
    title: 'Key Rules',
    rules: [
      { rule: 'Rule Name', example: 'Example text', icon: 'IconName' }
    ]
  }
}
```

### Welcome Slide (centered list)

```js
{
  type: 'welcome',
  content: {
    title: 'Welcome Title',
    points: ['Point 1', 'Point 2', 'Point 3']
  }
}
```

### Modules Slide (grid of module cards)

```js
{
  type: 'modules',
  content: {
    title: 'Course Overview',
    modules: [
      { num: '1-2', name: 'Module Name', icon: 'IconName' }
    ]
  }
}
```

## Requirements

Each module's slides folder needs:

- Tailwind CSS configured with the custom `primary` and `secondary` colors
- `react-router-dom` installed
- The `animate-float` and `animate-fade-in` animations in tailwind.config.js
