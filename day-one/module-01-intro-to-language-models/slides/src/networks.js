// The animated networks in the slides. Each step is a clip-deck network state (see the Networks
// section of clip-deck/README.md) with a caption. They are taken from the "How an AI learns"
// clip, social-scripts/02-how-ai-learns/scene.js, where you can see them in motion with the
// clip's script. Every step carries on from the step before.

// A sketch of Module 1's model: the last three tokens in, chances for the next one out.
// The real model has 3 × 16 inputs, 32 hidden neurons and 500 outputs. The percentages are its
// real output after "the queen said to" (Module 1 README, section 5).
export const networkDiagram = {
  title: 'A network of neurons',
  note: 'A simplified sketch of Module 1\'s model: the real one has 500 outputs. The percentages are its real output after "the queen said to".',
  steps: [
    {
      caption: 'A neural network is **neurons**, in layers.',
      layers: [3, 6, 5],
      pad: { left: 180, right: 480 },
      monoLabels: true,
      labels: { '0.0': 'queen', 0.1: 'said', 0.2: 'to' },
      weights: { random: 3 },
    },
    {
      caption:
        'Each line is a **weight**. Blue pushes up, violet pushes down, and thicker means stronger.',
    },
    {
      caption: 'Numbers go in on the left, and flow **forwards**, layer by layer.',
      pulse: 'forward',
      values: {
        random: 11,
        '0.0': 1,
        0.1: 1,
        0.2: 1,
        '2.0': 1,
        2.1: 0.81,
        2.2: 0.5,
        2.3: 0.31,
        2.4: 0.19,
      },
    },
    {
      caption: 'Out come **chances** for the next word.',
      bars: {
        '2.0': { label: 'the', value: 0.16 },
        2.1: { label: 'alice', value: 0.13 },
        2.2: { label: '"', value: 0.08 },
        2.3: { label: 'herself', value: 0.05 },
        2.4: { label: 'this', value: 0.03 },
      },
    },
  ],
};

// One neuron, learning that dark clouds and a rain forecast mean "take an umbrella". The numbers
// are real: social-scripts/02-how-ai-learns/neuron.py (sigmoid, learning rate 1.0).
const inputs = { '0.0': 1, 0.1: 1 };

export const networkLearning = {
  title: 'Learning: wrong, nudge, repeat',
  note: 'Each nudge: weight += error × input. These are the real numbers from a one-neuron example.',
  steps: [
    {
      caption: 'One neuron, with two **weights**. It starts out knowing nothing.',
      layers: [2, 1],
      radius: 64,
      spacing: 320,
      pad: { left: 400, right: 380 },
      weights: { '0.0-0': -0.35, '0.1-0': -0.7 },
      showWeights: true,
    },
    {
      caption:
        'Should I take an umbrella? Dark clouds and a rain forecast go in. It says **0.26**.',
      pulse: 'forward',
      labels: { '0.0': 'dark clouds', 0.1: 'rain forecast', '1.0': 'umbrella?' },
      values: { ...inputs, '1.0': 0.26 },
      showValues: true,
    },
    {
      caption: 'The right answer is **1**: take an umbrella. So it is wrong.',
    },
    {
      caption: 'So we nudge each weight a little, towards the right answer.',
      pulse: 'backward',
      weights: { '0.0-0': 0.39, '0.1-0': 0.04 },
    },
    {
      caption: 'Try again: **0.61**.',
      pulse: 'forward',
      values: { ...inputs, '1.0': 0.61 },
    },
    {
      caption: 'Nudge, and try again: **0.77**.',
      pulse: ['backward', 'forward'],
      weights: { '0.0-0': 0.78, '0.1-0': 0.44 },
      values: { ...inputs, '1.0': 0.77 },
    },
    {
      caption: 'And again: **0.84**. That is **learning**.',
      pulse: ['backward', 'forward'],
      weights: { '0.0-0': 1.01, '0.1-0': 0.66 },
      values: { ...inputs, '1.0': 0.84 },
    },
  ],
};

// Layers of neurons, and the error flowing back through them. The weights, activations and
// nudges here are made up to show the shape of it, not the numbers of a trained network.
export const networkBackprop = {
  title: 'Backpropagation',
  note: 'Illustration: the numbers are made up, to show the shape of it.',
  steps: [
    {
      caption: 'Real networks have **layers** of neurons.',
      layers: [3, 6, 6, 5],
      weights: { random: 3 },
    },
    {
      caption: 'Data flows **forwards**, and the answer is wrong.',
      pulse: 'forward',
      values: { random: 5 },
    },
    {
      caption: 'The error flows **backwards**, and every weight gets a nudge.',
      pulse: 'backward',
      nudge: 0.45,
    },
    {
      caption: "That's **backpropagation**. Then do it again. And again.",
      pulse: 'forward',
      values: { random: 9 },
    },
  ],
};
