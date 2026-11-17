// A small SVG engine for neural network diagrams on the stage: neurons and weights, data and
// error travelling through them, probability bars, and a camera that can zoom right out while
// the network extends into one vast network around it (drawn with WebGL, as SVG can't draw that
// many). A clip makes one in its scene.js and says what it looks like at each step:
//
//   new Network("#net").script({
//     "2.0": { layers: [2, 1], weights: { "0.0-0": -0.35 } },
//     "2.1": { pulse: "forward", values: { "0.0": 1, "1.0": 0.26 } },
//   });
//
// Keys are "frame.step", as in the address bar. Each step's state is every entry up to it, so
// stepping back or reloading lands in the right place. See the clip-deck README for every field.
//
// Outside a clip (the slide decks use it), pass options and drive it yourself:
//
//   const net = new Network(svg, { stage: { width: 1600, height: 700 }, listen: false, steps: ["0", "1"] });
//   net.script({ "0": { layers: [3, 6, 5] }, "1": { pulse: "forward" } });
//   net.goTo(1, true);   // show step 1; true plays its effects
//   net.destroy();       // when done

(() => {
  const NS = "http://www.w3.org/2000/svg";
  const STAGE = { width: 1080, height: 1920 };
  const BOX = { x: 56, y: 480, w: 968, h: 660 };
  const PAD = { top: 30, right: 60, bottom: 30, left: 60 };
  const TIME = { move: 900, value: 500, pulse: 450, zoom: 2500 };
  const COLOUR = {
    positive: "#38bdf8",
    negative: "#c084fc",
    data: "#e0f2fe",
    error: "#f87171",
    node: "#0b1222",
    lit: "#0ea5e9",
    ring: "#475569",
    text: "#f1f5f9",
    muted: "#94a3b8",
    bar: "#0ea5e9",
  };

  const still = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const clamp = (x, low = 0, high = 1) => Math.min(high, Math.max(low, x));
  const mix = (a, b, t) => a + (b - a) * t;
  const ease = (t) => (t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2);

  function make(name, attributes = {}, parent = null) {
    const element = document.createElementNS(NS, name);
    for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
    parent?.append(element);
    return element;
  }

  // A repeatable number in [-1, 1) for a seed and a name.
  function noise(seed, key) {
    let h = 2166136261 ^ seed;
    for (const character of key) h = Math.imul(h ^ character.charCodeAt(0), 16777619);
    h = Math.imul(h ^ (h >>> 15), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    return ((h ^ (h >>> 16)) >>> 0) / 2 ** 31 - 1;
  }

  function hash(text) {
    return Math.abs(Math.round(noise(7, text) * 1e6));
  }

  function mixColour(a, b, t) {
    const channels = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
    const [ca, cb] = [channels(a), channels(b)];
    return `rgb(${ca.map((c, i) => Math.round(mix(c, cb[i], t))).join(",")})`;
  }

  function signed(x) {
    return `${x < 0 ? "−" : "+"}${Math.abs(x).toFixed(2)}`;
  }

  function plain(x) {
    return Number.isInteger(Math.round(x * 100) / 100) ? String(Math.round(x)) : x.toFixed(2);
  }

  class Network {
    // options: stage { width, height } (default: the 1080×1920 clip stage), box (where the network
    // sits by default), pad, steps (the step keys, if there is no clip), and listen (follow the
    // clip's "clip:step" events: on by default).
    constructor(target, options = {}) {
      this.svg = typeof target === "string" ? document.querySelector(target) : target;
      this.stage = { ...STAGE, ...options.stage };
      this.defaultBox = { ...BOX, ...options.box };
      this.defaultPad = { ...PAD, ...options.pad };
      this.stepKeys = options.steps ?? null;
      this.svg.setAttribute("viewBox", `0 0 ${this.stage.width} ${this.stage.height}`);
      this.root = make("g", {}, this.svg);
      this.body = make("g", {}, this.root);
      this.edgeLayer = make("g", {}, this.body);
      this.nodeLayer = make("g", {}, this.body);
      this.overlay = make("g", {}, this.root);
      this.pulseLayer = make("g", {}, this.root);

      this.nodes = new Map();
      this.edges = new Map();
      this.bars = new Map();
      this.pulses = [];
      this.tweens = [];
      this.view = { zoom: 0, cx: this.stage.width / 2, cy: this.stage.height / 2, extend: 0, opacity: 1 };
      this.extension = null;
      this.box = { ...this.defaultBox };
      this.entries = new Map();
      this.tick = this.tick.bind(this);
      this.onStep = (event) => this.go(event.detail);
      if (options.listen !== false) document.addEventListener("clip:step", this.onStep);
    }

    // Stop following the clip and stop animating. The caller removes the SVG's contents.
    destroy() {
      this.dead = true;
      document.removeEventListener("clip:step", this.onStep);
      this.extension?.remove();
    }

    // Every step's key, in order: the clip's, or the ones this network was given.
    steps() {
      return this.stepKeys ?? window.clip.steps;
    }

    // Show a step by its place in the list. Pass true when it is one step on, to play its effects.
    goTo(index, forward = false) {
      this.go({ key: this.steps()[index], index, forward });
    }

    script(entries) {
      this.entries = new Map(Object.entries(entries));
      return this;
    }

    // Everything up to and including a step, applied in order.
    stateAt(index) {
      const state = { layers: [], nudges: [] };
      for (const key of this.steps().slice(0, index + 1)) {
        const entry = this.entries.get(key);
        if (!entry) continue;
        for (const [name, value] of Object.entries(entry)) {
          if (name === "nudge") state.nudges.push({ seed: hash(key), amount: value });
          else if (name !== "pulse") state[name] = value;
        }
      }
      return state;
    }

    go({ key, index, forward }) {
      const animate = forward && !still();
      const pulses = animate ? [].concat(this.entries.get(key)?.pulse ?? []) : [];
      this.apply(this.stateAt(index), animate, pulses);
    }

    // Where every neuron and weight goes for some layers in a box.
    layout(layers, box, pad, radius, spacing) {
      const nodes = [];
      const edges = [];
      const width = box.w - pad.left - pad.right;
      const height = box.h - pad.top - pad.bottom;
      const gap = spacing ?? Math.min(height / Math.max(1, ...layers), 170);
      const r = radius ?? Math.min(48, gap * 0.3);
      const centre = box.y + pad.top + height / 2;
      layers.forEach((count, l) => {
        const x = box.x + pad.left + (layers.length === 1 ? width / 2 : (width * l) / (layers.length - 1));
        for (let i = 0; i < count; i++) {
          const y = centre + (i - (count - 1) / 2) * gap;
          nodes.push({ id: `${l}.${i}`, layer: l, index: i, x, y, r });
          if (l + 1 < layers.length) {
            for (let j = 0; j < layers[l + 1]; j++) edges.push({ id: `${l}.${i}-${j}`, from: `${l}.${i}`, to: `${l + 1}.${j}`, layer: l });
          }
        }
      });
      // The grid these neurons sit on, for the vast network that extends from them. A layer with an
      // even number of neurons sits half a gap off the centre line, so layers alternate.
      const lattice = {
        x: box.x + pad.left,
        layerGap: layers.length > 1 ? width / (layers.length - 1) : gap * 1.6,
        y: centre,
        gap,
        r,
        phase: ((layers[0] ?? 1) - 1) % 2 ? 0.5 : 0,
      };
      return { nodes, edges, lattice };
    }

    weightOf(state, id) {
      const given = state.weights ?? {};
      let weight = given[id] ?? noise(given.random ?? 1, id) * (given.spread ?? 1);
      for (const nudge of state.nudges) weight += noise(nudge.seed, id) * nudge.amount;
      return weight;
    }

    valueOf(state, id) {
      const given = state.values ?? {};
      return given[id] ?? (given.random ? (noise(given.random, id) + 1) / 2 : 0);
    }

    apply(state, animate, pulses) {
      const layers = state.layers;
      const box = { ...this.defaultBox, ...state.box };
      const { nodes, edges, lattice } = this.layout(layers, box, { ...this.defaultPad, ...state.pad }, state.radius, state.spacing);
      const time = (ms) => (animate ? ms : 0);
      const steps = Math.max(1, layers.length - 1);

      // When each layer lights up or learns: as the data or the error reaches it.
      let clock = 0;
      let forwardAt = null;
      let backwardAt = null;
      for (const direction of pulses) {
        if (direction === "forward") forwardAt ??= clock;
        else backwardAt ??= clock;
        this.pulse(direction, clock, edges, steps);
        clock += steps * TIME.pulse;
      }
      const lightAt = (layer) => (forwardAt === null ? 0 : forwardAt + layer * TIME.pulse);
      const learnAt = (layer) => (backwardAt === null ? 0 : backwardAt + (steps - layer) * TIME.pulse);

      const keepNodes = new Set(nodes.map((node) => node.id));
      for (const [id, node] of this.nodes) if (!keepNodes.has(id)) this.retire(node, time(TIME.move));
      for (const target of nodes) {
        let node = this.nodes.get(target.id);
        if (!node || node.dying) node = this.addNode(target);
        node.layer = target.layer;
        node.last = target.layer === layers.length - 1;
        node.first = target.layer === 0;
        this.tween(node, "x", target.x, time(TIME.move));
        this.tween(node, "y", target.y, time(TIME.move));
        this.tween(node, "r", target.r, time(TIME.move));
        this.tween(node, "opacity", 1, time(TIME.move));
        this.tween(node, "value", this.valueOf(state, target.id), time(TIME.value), time(lightAt(target.layer)));
        this.tween(node, "showValue", state.showValues ? 1 : 0, time(TIME.value));
        const label = state.labels?.[target.id] ?? "";
        if (label) node.labelText.textContent = label;
        node.labelText.classList.toggle("mono", Boolean(state.monoLabels));
        this.tween(node, "showLabel", label ? 1 : 0, time(TIME.value));
      }

      const keepEdges = new Set(edges.map((edge) => edge.id));
      for (const [id, edge] of this.edges) if (!keepEdges.has(id)) this.retire(edge, time(TIME.move));
      for (const target of edges) {
        let edge = this.edges.get(target.id);
        const weight = this.weightOf(state, target.id);
        if (!edge || edge.dying) edge = this.addEdge(target, weight);
        this.tween(edge, "opacity", 1, time(TIME.move));
        this.tween(edge, "weight", weight, time(TIME.value), time(learnAt(target.layer)));
        this.tween(edge, "showValue", state.showWeights ? 1 : 0, time(TIME.value));
      }

      const bars = state.bars ?? {};
      const biggest = Math.max(0.0001, ...Object.values(bars).map((bar) => bar.value));
      for (const [id, bar] of this.bars) if (!(id in bars)) this.retire(bar, time(TIME.value));
      for (const [id, target] of Object.entries(bars)) {
        let bar = this.bars.get(id);
        if (!bar || bar.dying) bar = this.addBar(id);
        bar.label.textContent = target.label;
        bar.of = biggest;
        this.tween(bar, "opacity", 1, time(TIME.value), time(lightAt(layers.length - 1)));
        this.tween(bar, "value", target.value, time(TIME.move), time(lightAt(layers.length - 1)));
      }

      this.box = box;
      this.lattice = lattice;
      if (state.extend) {
        this.extension ??= Extension.create(this.svg, this.stage);
        this.span = { layers: [-45, 47], neurons: [-130, 130], ...(state.extend === true ? {} : state.extend) };
      }
      this.tween(this.view, "zoom", Math.log2(state.zoom ?? 1), time(state.zoomTime ?? TIME.zoom));
      this.tween(this.view, "cx", box.x + box.w / 2, time(TIME.move));
      this.tween(this.view, "cy", box.y + box.h / 2, time(TIME.move));
      this.tween(this.view, "extend", state.extend ? 1 : 0, time(TIME.move));
      this.tween(this.view, "opacity", state.show === false ? 0 : 1, time(TIME.move));
      this.start();
    }

    addNode(target) {
      const group = make("g", {}, this.nodeLayer);
      const node = {
        ...target,
        r: 0,
        value: 0,
        opacity: 0,
        showValue: 0,
        showLabel: 0,
        group,
        circle: make("circle", { "stroke-width": 3 }, group),
        valueText: make("text", { "text-anchor": "middle", "dominant-baseline": "central", fill: COLOUR.text }, group),
        labelText: make("text", { "dominant-baseline": "central", fill: COLOUR.text }, this.overlay),
      };
      this.nodes.set(target.id, node);
      return node;
    }

    addEdge(target, weight) {
      const edge = {
        ...target,
        weight,
        opacity: 0,
        showValue: 0,
        line: make("line", { "stroke-linecap": "round" }, this.edgeLayer),
        valueText: make("text", { "text-anchor": "middle", "dominant-baseline": "central", class: "weight" }, this.overlay),
      };
      this.edges.set(target.id, edge);
      return edge;
    }

    addBar(id) {
      const group = make("g", {}, this.overlay);
      const bar = {
        id,
        value: 0,
        opacity: 0,
        of: 1,
        group,
        label: make("text", { "dominant-baseline": "central", class: "mono", fill: COLOUR.text }, group),
        rect: make("rect", { rx: 6, fill: COLOUR.bar }, group),
        percent: make("text", { "dominant-baseline": "central", fill: COLOUR.muted }, group),
      };
      this.bars.set(id, bar);
      return bar;
    }

    retire(thing, duration) {
      thing.dying = true;
      this.tween(thing, "opacity", 0, duration);
      if (thing.r !== undefined) this.tween(thing, "r", 0, duration);
    }

    // Dots that travel along every weight, layer by layer: data forwards, error backwards.
    pulse(direction, delay, edges, steps) {
      const now = performance.now();
      for (const edge of edges) {
        const layer = direction === "forward" ? edge.layer : steps - 1 - edge.layer;
        const colour = direction === "forward" ? COLOUR.data : COLOUR.error;
        const group = make("g", { opacity: 0 }, this.pulseLayer);
        make("circle", { r: 16, fill: colour, opacity: 0.25 }, group);
        make("circle", { r: 7, fill: colour }, group);
        this.pulses.push({
          edge: edge.id,
          forward: direction === "forward",
          start: now + delay + layer * TIME.pulse,
          group,
        });
      }
    }

    tween(object, key, to, duration, delay = 0) {
      this.tweens = this.tweens.filter((tween) => !(tween.object === object && tween.key === key));
      if (!duration && !delay) {
        object[key] = to;
        return;
      }
      this.tweens.push({ object, key, from: object[key], to, start: performance.now() + delay, duration: Math.max(1, duration) });
    }

    start() {
      this.render();
      if (!this.running) {
        this.running = true;
        requestAnimationFrame(this.tick);
      }
    }

    tick(now) {
      if (this.dead) {
        this.running = false;
        return;
      }
      this.tweens = this.tweens.filter((tween) => {
        const progress = (now - tween.start) / tween.duration;
        if (progress < 0) return true;
        tween.object[tween.key] = mix(tween.from, tween.to, ease(clamp(progress)));
        return progress < 1;
      });
      this.render(now);
      if (this.tweens.length || this.pulses.length) requestAnimationFrame(this.tick);
      else this.running = false;
    }

    render(now = performance.now()) {
      for (const [maps, id, thing] of this.all()) {
        if (thing.dying && thing.opacity <= 0.001 && !this.tweens.some((tween) => tween.object === thing)) {
          (thing.group ?? thing.line)?.remove();
          thing.labelText?.remove();
          thing.valueText?.remove();
          maps.delete(id);
        }
      }

      for (const node of this.nodes.values()) {
        node.group.setAttribute("opacity", node.opacity);
        node.circle.setAttribute("cx", node.x);
        node.circle.setAttribute("cy", node.y);
        node.circle.setAttribute("r", Math.max(0, node.r));
        node.circle.setAttribute("fill", mixColour(COLOUR.node, COLOUR.lit, clamp(node.value)));
        node.circle.setAttribute("stroke", mixColour(COLOUR.ring, COLOUR.positive, clamp(node.value)));
        node.valueText.setAttribute("x", node.x);
        node.valueText.setAttribute("y", node.y);
        node.valueText.style.fontSize = `${Math.max(1, node.r * 0.62)}px`;
        node.valueText.setAttribute("opacity", node.showValue);
        node.valueText.textContent = plain(node.value);
        const side = node.first ? -1 : node.last ? 1 : 0;
        node.labelText.setAttribute("text-anchor", side < 0 ? "end" : side > 0 ? "start" : "middle");
        node.labelText.setAttribute("x", node.x + side * (node.r + 20));
        node.labelText.setAttribute("y", side ? node.y : node.y - node.r - 26);
        node.labelText.setAttribute("opacity", node.opacity * node.showLabel);
      }

      for (const edge of this.edges.values()) {
        const from = this.nodes.get(edge.from);
        const to = this.nodes.get(edge.to);
        if (!from || !to) continue;
        const strength = Math.min(Math.abs(edge.weight), 1.5);
        const colour = edge.weight >= 0 ? COLOUR.positive : COLOUR.negative;
        edge.line.setAttribute("x1", from.x);
        edge.line.setAttribute("y1", from.y);
        edge.line.setAttribute("x2", to.x);
        edge.line.setAttribute("y2", to.y);
        edge.line.setAttribute("stroke", colour);
        edge.line.setAttribute("stroke-width", 1.5 + strength * 4);
        edge.line.setAttribute("opacity", edge.opacity * Math.min(from.opacity, to.opacity) * (0.3 + 0.45 * strength));
        edge.valueText.setAttribute("x", mix(from.x, to.x, 0.42));
        edge.valueText.setAttribute("y", mix(from.y, to.y, 0.42) + (from.y <= to.y ? -32 : 32));
        edge.valueText.setAttribute("fill", colour);
        edge.valueText.setAttribute("opacity", edge.opacity * edge.showValue);
        edge.valueText.textContent = signed(edge.weight);
      }

      for (const bar of this.bars.values()) {
        const node = this.nodes.get(bar.id);
        if (!node) continue;
        const left = node.x + node.r + 22;
        const width = Math.max(0, (bar.value / bar.of) * 190);
        bar.group.setAttribute("opacity", bar.opacity * node.opacity);
        bar.label.setAttribute("x", left);
        bar.label.setAttribute("y", node.y);
        bar.rect.setAttribute("x", left + 150);
        bar.rect.setAttribute("y", node.y - 16);
        bar.rect.setAttribute("width", width);
        bar.rect.setAttribute("height", 32);
        bar.percent.setAttribute("x", left + 150 + width + 14);
        bar.percent.setAttribute("y", node.y);
        bar.percent.textContent = `${Math.round(bar.value * 100)}%`;
      }

      this.pulses = this.pulses.filter((pulse) => {
        const edge = this.edges.get(pulse.edge);
        const progress = (now - pulse.start) / TIME.pulse;
        if (!edge || progress >= 1) {
          pulse.group.remove();
          return false;
        }
        const [a, b] = [this.nodes.get(edge.from), this.nodes.get(edge.to)];
        const t = pulse.forward ? clamp(progress) : 1 - clamp(progress);
        pulse.group.setAttribute("transform", `translate(${mix(a.x, b.x, t)} ${mix(a.y, b.y, t)})`);
        pulse.group.setAttribute("opacity", progress < 0 ? 0 : Math.sin(Math.PI * clamp(progress)) * 0.6 + 0.4);
        return true;
      });

      // The camera: zoom out around the network's box, keeping it where it is on the stage.
      const scale = 2 ** this.view.zoom;
      const { cx, cy } = this.view;
      const viewBox = [cx - cx * scale, cy - cy * scale, this.stage.width * scale, this.stage.height * scale];
      this.svg.setAttribute("viewBox", viewBox.join(" "));
      this.root.setAttribute("opacity", this.view.opacity);
      // Dimmer than the network on the stage, so that one still stands out.
      this.extension?.draw(viewBox, this.lattice, this.span, 0.6 * this.view.extend * this.view.opacity);
    }

    *all() {
      for (const maps of [this.nodes, this.edges, this.bars]) for (const [id, thing] of maps) yield [maps, id, thing];
    }
  }

  // The vast network that the one on the stage extends into. It sits on the same grid as the
  // stage's neurons, so they look like part of it. Far too many neurons for SVG, so a WebGL shader
  // works out each pixel from the grid instead: sharp at any zoom, and a soft glow when the lines
  // get finer than a pixel.
  const EXTENSION_VERTEX = `#version 300 es
in vec2 corner;
void main() {
  gl_Position = vec4(corner, 0.0, 1.0);
}`;

  const EXTENSION_FRAGMENT = `#version 300 es
precision highp float;

uniform vec2 size;      // the canvas, in pixels: the same as the stage
uniform vec4 view;      // the camera: x, y, width and height, on the stage
uniform vec4 lattice;   // x of the first layer, gap between layers, y of the centre line, gap between neurons
uniform float radius;
uniform float phase;    // 0, or 0.5 if the first layer sits half a gap off the centre line
uniform vec4 span;      // first and last layer, first and last neuron, counted from the stage's network
uniform float opacity;
out vec4 colour;

const int REACH = 3;  // each neuron connects to the seven nearest in the next layer
const vec3 POSITIVE = vec3(0.220, 0.741, 0.973);
const vec3 NEGATIVE = vec3(0.753, 0.518, 0.988);
const vec3 NODE = vec3(0.043, 0.071, 0.133);
const vec3 LIT = vec3(0.055, 0.647, 0.914);
const vec3 RING = vec3(0.278, 0.333, 0.412);

float hash(vec3 p) {
  p = fract(p * vec3(0.1031, 0.1030, 0.0973));
  p += dot(p, p.yxz + 33.33);
  return fract((p.x + p.y) * p.z);
}

// How far a layer's neurons sit off the centre line, in neuron gaps. Layers alternate.
float offset(float layer) {
  return mod(phase + 0.5 * layer, 1.0);
}

void main() {
  vec2 p = view.xy + vec2(gl_FragCoord.x, size.y - gl_FragCoord.y) / size * view.zw;
  float pixel = view.z / size.x;
  float layerGap = lattice.y;
  float gap = lattice.w;
  float column = (p.x - lattice.x) / layerGap;
  vec4 paint = vec4(0.0);

  // The weights between this layer and the next.
  float c = floor(column);
  float t = column - c;
  if (c >= span.x && c < span.y) {
    float shift = offset(c + 1.0) - offset(c);
    for (int k = -REACH; k <= REACH; k++) {
      float rise = float(k) + shift;
      float row = floor((p.y - lattice.z - t * rise * gap) / gap - offset(c) + 0.5);
      float target = row + float(k);
      if (row < span.z || row > span.w || target < span.z || target > span.w) continue;
      float y = lattice.z + (row + offset(c) + t * rise) * gap;
      float slope = rise * gap / layerGap;
      float distance = abs(p.y - y) / sqrt(1.0 + slope * slope);
      float weight = hash(vec3(c, row, float(k))) * 2.0 - 1.0;
      float width = 1.5 + abs(weight) * 4.0;
      float drawn = max(width, pixel);
      float cover = smoothstep(drawn * 0.5 + pixel * 0.5, drawn * 0.5 - pixel * 0.5, distance) * width / drawn;
      vec3 tint = weight >= 0.0 ? POSITIVE : NEGATIVE;
      paint += vec4(tint, 1.0) * cover * (0.3 + 0.45 * abs(weight)) * (1.0 - paint.a);
    }
  }

  // The neurons, over the weights.
  float layer = floor(column + 0.5);
  if (layer >= span.x && layer <= span.y) {
    float row = floor((p.y - lattice.z) / gap - offset(layer) + 0.5);
    if (row >= span.z && row <= span.w) {
      vec2 centre = vec2(lattice.x + layer * layerGap, lattice.z + (row + offset(layer)) * gap);
      float distance = length(p - centre);
      float lit = hash(vec3(layer, row, 9.0));
      float fill = smoothstep(radius + pixel, radius - pixel, distance);
      float ring = smoothstep(1.5 + pixel, max(0.0, 1.5 - pixel), abs(distance - radius)) * min(1.0, 3.0 / pixel);
      paint = vec4(mix(NODE, LIT, lit * lit), 1.0) * fill + paint * (1.0 - fill);
      paint = vec4(mix(RING, POSITIVE, lit), 1.0) * ring + paint * (1.0 - ring);
    }
  }

  // From far away the lines are finer than a pixel and shimmer, so fade to their average glow.
  vec2 low = vec2(lattice.x + span.x * layerGap, lattice.z + (span.z - 0.5) * gap);
  vec2 high = vec2(lattice.x + span.y * layerGap, lattice.z + (span.w + 1.0) * gap);
  float inside = step(low.x, p.x) * step(p.x, high.x) * step(low.y, p.y) * step(p.y, high.y);
  vec4 glow = vec4(mix(POSITIVE, NEGATIVE, 0.35), 1.0) * 0.2 * inside;
  float detail = smoothstep(1.5, 5.0, gap / pixel);
  colour = mix(glow, paint, detail) * opacity;
}`;

  class Extension {
    // A canvas just behind the SVG, or null if there's no WebGL (the zoom still works without it).
    static create(svg, stage) {
      const canvas = document.createElement("canvas");
      canvas.className = "network-extension";
      canvas.width = stage.width;
      canvas.height = stage.height;
      const gl = canvas.getContext("webgl2");
      if (!gl) return null;
      try {
        return new Extension(svg, canvas, gl);
      } catch (error) {
        console.error("Network extension off:", error.message);
        return null;
      }
    }

    constructor(svg, canvas, gl) {
      const compile = (type, source) => {
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(shader));
        return shader;
      };
      const program = gl.createProgram();
      gl.attachShader(program, compile(gl.VERTEX_SHADER, EXTENSION_VERTEX));
      gl.attachShader(program, compile(gl.FRAGMENT_SHADER, EXTENSION_FRAGMENT));
      gl.linkProgram(program);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
      gl.useProgram(program);

      gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
      const corner = gl.getAttribLocation(program, "corner");
      gl.enableVertexAttribArray(corner);
      gl.vertexAttribPointer(corner, 2, gl.FLOAT, false, 0, 0);

      this.uniforms = Object.fromEntries(
        ["size", "view", "lattice", "radius", "phase", "span", "opacity"].map((name) => [name, gl.getUniformLocation(program, name)]),
      );
      this.canvas = canvas;
      this.gl = gl;
      this.shown = false;
      svg.before(canvas);
    }

    draw(view, lattice, span, opacity) {
      const { gl, uniforms } = this;
      if (opacity <= 0.001 || !lattice || !span) {
        if (this.shown) gl.clear(gl.COLOR_BUFFER_BIT);
        this.shown = false;
        return;
      }
      this.shown = true;
      gl.viewport(0, 0, this.canvas.width, this.canvas.height);
      gl.uniform2f(uniforms.size, this.canvas.width, this.canvas.height);
      gl.uniform4f(uniforms.view, ...view);
      gl.uniform4f(uniforms.lattice, lattice.x, lattice.layerGap, lattice.y, lattice.gap);
      gl.uniform1f(uniforms.radius, lattice.r);
      gl.uniform1f(uniforms.phase, lattice.phase);
      gl.uniform4f(uniforms.span, span.layers[0], span.layers[1], span.neurons[0], span.neurons[1]);
      gl.uniform1f(uniforms.opacity, opacity);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }

    remove() {
      this.canvas.remove();
    }
  }

  window.Network = Network;
})();
