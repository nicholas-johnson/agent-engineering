// Clip 2's network at each step. Keys are "frame.step", as in the address bar.
// The neuron's numbers come from neuron.py; the next-word chances from Module 1's README.

const inputs = { "0.0": 1, "0.1": 1 };

new Network("#net").script({
  // One neuron, learning that dark clouds and a rain forecast mean "take an umbrella"
  "2.0": {
    layers: [2, 1],
    radius: 56,
    spacing: 300,
    pad: { left: 300, right: 290 },
    weights: { "0.0-0": -0.35, "0.1-0": -0.7 },
    showWeights: true,
  },
  "2.1": {
    pulse: "forward",
    labels: { "0.0": "dark clouds", "0.1": "rain forecast", "1.0": "umbrella?" },
    values: { ...inputs, "1.0": 0.26 },
    showValues: true,
  },
  "2.3": { pulse: "backward", weights: { "0.0-0": 0.39, "0.1-0": 0.04 } },
  "2.4": { pulse: "forward", values: { ...inputs, "1.0": 0.61 } },
  "2.5": {
    pulse: ["backward", "forward"],
    weights: { "0.0-0": 0.78, "0.1-0": 0.44 },
    values: { ...inputs, "1.0": 0.77 },
  },
  "2.6": {
    pulse: ["backward", "forward"],
    weights: { "0.0-0": 1.01, "0.1-0": 0.66 },
    values: { ...inputs, "1.0": 0.84 },
  },

  // Layers of neurons, and the error flowing back through them
  "3.0": {
    layers: [3, 6, 6, 5],
    radius: undefined,
    spacing: undefined,
    pad: {},
    weights: { random: 3 },
    values: {},
    labels: {},
    showValues: false,
    showWeights: false,
  },
  "3.1": { pulse: "forward", values: { random: 5 } },
  "3.2": { pulse: "backward", nudge: 0.45 },
  "3.3": { pulse: "forward", values: { random: 9 } },

  // A model like Module 1's: the last three tokens of "the queen said to" in, the next word's
  // chances out.
  "4.0": {
    layers: [3, 6, 5],
    pad: { left: 180, right: 470 },
    pulse: "forward",
    monoLabels: true,
    labels: { "0.0": "queen", "0.1": "said", "0.2": "to" },
    values: { random: 11, "0.0": 1, "0.1": 1, "0.2": 1, "2.0": 1, "2.1": 0.81, "2.2": 0.5, "2.3": 0.31, "2.4": 0.19 },
    // First the next word: Module 1's real output for this context.
    bars: {
      "2.0": { label: "the", value: 0.16 },
      "2.1": { label: "alice", value: 0.13 },
      "2.2": { label: '"', value: 0.08 },
      "2.3": { label: "herself", value: 0.05 },
      "2.4": { label: "this", value: 0.03 },
    },
  },

  // Then the same outputs as tokens: made up, with words cut into the pieces a tokeniser might use.
  "4.1": {
    bars: {
      "2.0": { label: "the", value: 0.16 },
      "2.1": { label: "al", value: 0.13 },
      "2.2": { label: '"', value: 0.08 },
      "2.3": { label: "her", value: 0.05 },
      "2.4": { label: "th", value: 0.03 },
    },
  },

  // Zoom right out
  "5.0": { zoom: 3, field: true },
  "5.1": { zoom: 90, zoomTime: 5000 },
});
