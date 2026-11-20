// Clip 3's map at each step. Keys are "frame.step", as in the address bar.
// The passages and questions come from search.py, through map.js.

const { points, questions } = window.MAP;

new Space("#map", {
  points,
  box: { x: 56, y: 390, w: 968, h: 530 },
  groups: {
    royals: { colour: "#f87171", label: "the Queen and King", at: [-0.42, -0.25] },
    turtle: { colour: "#38bdf8", label: "the Mock Turtle" },
    tea: { colour: "#c084fc", label: "the tea party" },
    caterpillar: { colour: "#4ade80", label: "the Caterpillar" },
  },
}).script({
  // Every passage, squashed from 1,536 numbers onto a flat map
  "3.0": { show: true, note: "Each dot is a passage: 1,536 numbers, squashed to 2" },
  // Coloured by who the passage is mostly about
  "3.1": { tint: true, labels: true },
  // The question lands among the Queen's passages, and joins its closest one
  "3.2": { questions: { angry: { at: questions.angry.point, label: questions.angry.text } } },
  "3.3": { links: { angry: questions.angry.nearest } },
  "4.0": { hide: true },
});
