// A small SVG engine for neural network diagrams on the stage: neurons and weights, data and
// error travelling through them, probability bars, and a camera that can zoom right out over a
// field of copies. A clip makes one in its scene.js and says what it looks like at each step:
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
      const id = this.svg.id || "network";

      const defs = make("defs", {}, this.svg);
      this.pattern = make("pattern", { id: `${id}-field`, patternUnits: "userSpaceOnUse" }, defs);
      this.copy = make("use", { href: `#${id}-body` }, this.pattern);
      this.root = make("g", {}, this.svg);
      this.field = make("rect", { x: -3e5, y: -3e5, width: 6e5, height: 6e5, fill: `url(#${id}-field)` }, this.root);
      this.body = make("g", { id: `${id}-body` }, this.root);
      this.edgeLayer = make("g", {}, this.body);
      this.nodeLayer = make("g", {}, this.body);
      this.overlay = make("g", {}, this.root);
      this.pulseLayer = make("g", {}, this.root);

      this.nodes = new Map();
      this.edges = new Map();
      this.bars = new Map();
      this.pulses = [];
      this.tweens = [];
      this.view = { zoom: 0, cx: this.stage.width / 2, cy: this.stage.height / 2, field: 0, opacity: 1 };
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
      layers.forEach((count, l) => {
        const x = box.x + pad.left + (layers.length === 1 ? width / 2 : (width * l) / (layers.length - 1));
        for (let i = 0; i < count; i++) {
          const y = box.y + pad.top + height / 2 + (i - (count - 1) / 2) * gap;
          nodes.push({ id: `${l}.${i}`, layer: l, index: i, x, y, r });
          if (l + 1 < layers.length) {
            for (let j = 0; j < layers[l + 1]; j++) edges.push({ id: `${l}.${i}-${j}`, from: `${l}.${i}`, to: `${l + 1}.${j}`, layer: l });
          }
        }
      });
      return { nodes, edges };
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
      const { nodes, edges } = this.layout(layers, box, { ...this.defaultPad, ...state.pad }, state.radius, state.spacing);
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
      this.pattern.setAttribute("x", box.x);
      this.pattern.setAttribute("y", box.y);
      this.pattern.setAttribute("width", box.w);
      this.pattern.setAttribute("height", box.h);
      this.copy.setAttribute("x", -box.x);
      this.copy.setAttribute("y", -box.y);
      this.tween(this.view, "zoom", Math.log2(state.zoom ?? 1), time(state.zoomTime ?? TIME.zoom));
      this.tween(this.view, "cx", box.x + box.w / 2, time(TIME.move));
      this.tween(this.view, "cy", box.y + box.h / 2, time(TIME.move));
      this.tween(this.view, "field", state.field ? 1 : 0, time(TIME.move));
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
      this.svg.setAttribute(
        "viewBox",
        `${cx - (cx * scale)} ${cy - (cy * scale)} ${this.stage.width * scale} ${this.stage.height * scale}`,
      );
      this.field.setAttribute("opacity", this.view.field * 0.5);
      this.root.setAttribute("opacity", this.view.opacity);
    }

    *all() {
      for (const maps of [this.nodes, this.edges, this.bars]) for (const [id, thing] of maps) yield [maps, id, thing];
    }
  }

  window.Network = Network;
})();
