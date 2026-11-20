# Clip 2 — How an AI learns

> A promise to show how an AI learns in sixty seconds. One neuron gets a question wrong, and we nudge its weights until it's nearly right. Then layers of neurons, with the error flowing backwards through them: backpropagation. Train one on a book and it predicts the next word. Then zoom out: this little one has 48 weights to nudge, and the big ones have billions.

- **Length:** about 140 spoken words to explain it, then about 25 for the sign-off. `pnpm social:check` estimates about 65 seconds in all, so time your first take.
- **Ending:** the sign-off, full-face: "Follow if you'd like to know more." Cut straight after it.
- **Recording:** [`index.html`](index.html), with the network drawn by `clip-deck`'s `network.js` from [`scene.js`](scene.js). Run `pnpm social`, open <http://127.0.0.1:8765/02-how-ai-learns/> in Chrome and press R.

## The script

### 1. The promise

To camera, full-screen:

> "I'm going to show you how an AI learns, in sixty seconds."

### 2. The odd thing

> "Every AI starts out knowing nothing. Here's one neuron. Should I take an umbrella? It says 0.26. The right answer is 1."

**Screen:** one neuron. Two inputs, *dark clouds* and *rain forecast*, both 1, joined to one output, *umbrella?*. Its two weights start random: −0.35 and −0.70. Data travels along them, and the answer comes out at 0.26.

### 3. The reveal

> "So we nudge each weight a little, towards the right answer. Try again: 0.61. Nudge, and try again: 0.77. And again: 0.84. That's learning."

**Screen:** the error travels back in red, and each weight counts to its new value. Then the data goes forward again and the answer climbs.

> "Real networks have layers of these. Data flows forwards, and the answer's wrong. The error flows backwards, and every weight gets a nudge. That's backpropagation. Then do it again. And again."

**Screen:** the neuron grows into four layers. White dots go forwards, red dots come back, and every weight shifts.

### 4. The payoff

> "Train one on a book, and it learns to predict the next word… or the next part of a word, which we call a token. It gives every possible next word a chance."

**Screen:** a model like Module 1's, after "the queen said to". Its inputs are the last three tokens, *queen*, *said* and *to*. Its outputs start as the five likeliest next words: *the* 16%, *alice* 13%, *"* 8%, *herself* 5%, *this* 3%. On "token", the same bars become tokens, and the words shorten to the pieces a tokeniser might cut them into: *the*, *al*, *"*, *her*, *th*. The tokens are illustrative: see the notes.

> "This little one has 48 weights to nudge. The big ones have billions. Same trick: be wrong, nudge, repeat."

**Screen:** the camera pulls back, and the little network turns out to be a tiny part of one vast network, with more layers on either side and more neurons above and below. By the end the whole vast network is on screen, with the little one a bright speck at its centre.

### 5. Sign-off

Full-face again:

> "I'm Nicholas Johnson. I'm a principal dev working with AI. I'm doing a series on AI fundamentals. Follow if you'd like to know more."

## Captions and presses

The captions are the `<p class="cue">` lines in `index.html`, and the network's changes are in `scene.js`, keyed by the same steps. Words in italics show in yellow.

| Press | Caption: what you say | What else happens |
|-------|-----------------------|-------------------|
| — | I'm going to show you how an AI *learns*, in sixty seconds. | You, full-screen |
| 1 | Every AI starts out knowing nothing. | You shrink into the box. One neuron appears, with random weights −0.35 and −0.70. |
| 2 | Here's one neuron. Should I take an umbrella? | Both inputs light up at 1, data travels forwards, and the answer counts up to 0.26 |
| 3 | It says 0.26. The right answer is 1. | "The right answer: 1, take an umbrella" |
| 4 | So we nudge each weight a little, towards the right answer. | The error travels back in red; the weights change to +0.39 and +0.04 |
| 5 | Try again: 0.61. | Forwards again: 0.61 |
| 6 | Nudge, and try again: 0.77. | Back and forwards: weights +0.78 and +0.44, answer 0.77 |
| 7 | And again: 0.84. That's *learning*. | Weights +1.01 and +0.66, answer 0.84; the heading becomes "Wrong. Nudge. Repeat." |
| 8 | Real networks have layers of these. | The neuron grows into four layers |
| 9 | Data flows forwards, and the answer's wrong. | White dots travel forwards, lighting each layer |
| 10 | The error flows backwards, and every weight gets a nudge. | Red dots travel back, and every weight shifts |
| 11 | That's *backpropagation*. Then do it again. And again. | Forwards again; the heading becomes "Backpropagation" |
| 12 | Train one on a book, and it learns to predict the next word… | A model like Module 1's: *queen*, *said*, *to* in, and bars for the next word out: *the*, *alice*, *"*, *herself*, *this* |
| 13 | …or the next part of a word, which we call a *token*. | The heading becomes "The next token", and the outputs shorten to tokens: *the*, *al*, *"*, *her*, *th* |
| 14 | It gives every possible next word a chance. | — |
| 15 | This little one has 48 weights to nudge. | The labels and bars fade, and the camera pulls back three times as the network extends into a vast one around it |
| 16 | The big ones have *billions*. | It keeps pulling back, to 24 times, over five seconds, until the whole vast network is on screen; the heading becomes "Billions" |
| 17 | Same trick: be wrong, nudge, repeat. | — |
| 18 | I'm Nicholas Johnson. I'm a principal dev working with AI. | You, full-screen again |
| 19 | I'm doing a series on *AI fundamentals*. | — |
| 20 | Follow if you'd like to know more. | — |

Then press R to stop.

## Post text

For the description under the video, not on it. Repeat the promise, then the course plug:

> How an AI learns, in sixty seconds: it's wrong, so you nudge every weight a little towards the right answer. Then repeat.

## Notes

- **The neuron isn't a classic perceptron.** A perceptron answers only 0 or 1, so it's never "a bit wrong". This neuron has a smooth output (a sigmoid), so it can be a bit wrong and be nudged a little. That's why the captions say "neuron".
- **The neuron learns from a single example.** Real training uses many different examples. One is enough to show the nudge.
- **The neuron's starting weights are random,** from seed 7, which was chosen so it starts out clearly wrong. Any seed learns the same way.
- **The layered network is a diagram.** Its weights and lit neurons are made up, so you can see the shape. They're not from a trained model.
- **The words are real; the tokens are illustrative.** "The next word" shows Module 1's real output after "the queen said to": *the* 16%, *alice* 13%, *"* 8%, *herself* 5%, *this* 3%. On "token", the same bars are relabelled with made-up word pieces (*al*, *her*, *th*), to show that a token is often part of a word. Module 1's own tokeniser actually keeps these particular words whole, because its 500-token vocabulary happens to include them.
- **Module 1's model is squeezed to fit.** It really has 48 inputs (three tokens of 16 numbers each), 32 hidden neurons and 500 outputs. The diagram shows three tokens, six hidden neurons and five outputs.
- **The vast network is illustrative.** It's about 93 layers of 261 neurons, each joined to the seven nearest in the next layer, to give a sense of scale. Real large models are far bigger, and connected differently.
- **If the explanation runs over sixty seconds,** drop "It gives every possible next word a chance." first. It has no change on screen, so nothing else needs to move.

## Where the material comes from

| On screen | Source |
|-----------|--------|
| The neuron's weights and answers: −0.35, −0.70 → 0.26; then 0.61, 0.77, 0.84 | [`neuron.py`](neuron.py), run 13 November 2026: `uv run python social-scripts/02-how-ai-learns/neuron.py` |
| The context "the queen said to" | Module 1 README, section 5, "The result" (`day-one/module-01-intro-to-language-models/demo/05_neural_model.py`) |
| The next-word chances: *the* 16%, *alice* 13%, *"* 8%, *herself* 5%, *this* 3% | Module 1 README, section 5, "The result" |
| The tokens *the*, *al*, *"*, *her*, *th* | Made up: the same bars, relabelled with word pieces. See the notes. |
| The inputs *queen*, *said*, *to* | The context split with Module 1's tokens (`data/tokens.json`) is *the*, *queen*, *said*, *to*; the model reads the last three |
| 48 weights to nudge | The network on screen: 3 inputs × 6 hidden + 6 hidden × 5 outputs = 48 connections |
| The big ones have billions | Module 1 README, section 5, "From here to a real language model": "billions to trillions" |
