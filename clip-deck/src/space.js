// A small SVG engine for maps of meaning: one dot per embedded thing (a passage, a sentence),
// squashed from its many numbers down to two, coloured by group. Questions drop onto the map, and
// a line joins each to the dot it is closest to. A clip makes one in its scene.js and says what the
// map shows at each step:
//
//   new Space("#map", { points: [[0.1, -0.2, "royals"], …], groups: { royals: { colour: "#f87171", label: "the Queen" } } })
//     .script({
//       "3.0": { show: true },
//       "3.1": { tint: true, labels: true },
//       "3.2": { questions: { angry: { at: [-0.14, -0.17], label: "the angry queen" } } },
//       "3.3": { links: { angry: 105 } },
//     });
//
// Keys are "frame.step", as in the address bar. Each step's state is every entry up to it, so
// stepping back or reloading lands in the right place. See the clip-deck README for every field.

(() => {
  const NS = "http://www.w3.org/2000/svg";
  const STAGE = { width: 1080, height: 1920 };
  const BOX = { x: 56, y: 400, w: 968, h: 560 };
  const TIME = { appear: 500, spread: 900, move: 700, drop: 800, link: 600 };
  const COLOUR = { point: "#475569", question: "#fde047", link: "#fde047", ring: "#f8fafc", muted: "#94a3b8" };
  const RADIUS = { point: 9, chosen: 17, question: 15 };

  const still = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const clamp = (x, low = 0, high = 1) => Math.min(high, Math.max(low, x));
  const mix = (a, b, t) => a + (b - a) * t;
  const ease = (t) => (t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2);
  const land = (t) => 1 + 2.2 * (t - 1) ** 3 + 1.2 * (t - 1) ** 2; // overshoots a little, then settles

  function make(name, attributes = {}, parent = null) {
    const element = document.createElementNS(NS, name);
    for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
    parent?.append(element);
    return element;
  }

  // A repeatable number in [0, 1) for an index, so the dots appear in a scattered order.
  function scatter(i) {
    let h = Math.imul(i + 1, 2654435761);
    h = Math.imul(h ^ (h >>> 15), 2246822507);
    return ((h ^ (h >>> 13)) >>> 0) / 2 ** 32;
  }

  function mixColour(a, b, t) {
    const channels = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
    const [ca, cb] = [channels(a), channels(b)];
    return `rgb(${ca.map((c, i) => Math.round(mix(c, cb[i], t))).join(",")})`;
  }

  class Space {
    // options: points ([x, y, group] each, in any units), groups ({ name: { colour, label, at } },
    // where at is [x, y] for the label if the middle of the group isn't a good place), box (where the
    // map sits), stage, steps (the step keys, if there is no clip), and listen (follow the clip's
    // "clip:step" events: on by default).
    constructor(target, options = {}) {
      this.svg = typeof target === "string" ? document.querySelector(target) : target;
      this.stage = { ...STAGE, ...options.stage };
      this.box = { ...BOX, ...options.box };
      this.groups = options.groups ?? {};
      this.stepKeys = options.steps ?? null;
      this.svg.setAttribute("viewBox", `0 0 ${this.stage.width} ${this.stage.height}`);
      this.root = make("g", {}, this.svg);
      this.linkLayer = make("g", {}, this.root);
      this.pointLayer = make("g", {}, this.root);
      this.labelLayer = make("g", {}, this.root);
      this.questionLayer = make("g", {}, this.root);
      this.noteText = make("text", { "text-anchor": "end", class: "map-note", fill: COLOUR.muted }, this.root);

      const raw = options.points ?? [];
      this.fit(raw);
      this.points = raw.map(([x, y, group], i) => ({
        x,
        y,
        group,
        order: scatter(i),
        shown: 0,
        tint: 0,
        chosen: 0,
        circle: make("circle", { r: RADIUS.point }, this.pointLayer),
      }));
      this.labels = Object.entries(this.groups).map(([name, group]) => {
        const members = this.points.filter((point) => point.group === name);
        const middle = (key) => members.map((point) => point[key]).sort((a, b) => a - b)[Math.floor(members.length / 2)] ?? 0;
        const [x, y] = group.at ?? [middle("x"), middle("y")];
        const text = make("text", { "text-anchor": "middle", fill: group.colour }, this.labelLayer);
        text.textContent = group.label ?? name;
        return { name, x, y, text, shown: 0 };
      });
      this.questions = new Map();
      this.links = new Map();
      this.view = { opacity: 1, note: 0 };
      this.tweens = [];
      this.entries = new Map();
      this.tick = this.tick.bind(this);
      this.onStep = (event) => this.go(event.detail);
      if (options.listen !== false) document.addEventListener("clip:step", this.onStep);
    }

    destroy() {
      this.dead = true;
      document.removeEventListener("clip:step", this.onStep);
    }

    steps() {
      return this.stepKeys ?? window.clip.steps;
    }

    goTo(index, forward = false) {
      this.go({ key: this.steps()[index], index, forward });
    }

    script(entries) {
      this.entries = new Map(Object.entries(entries));
      return this;
    }

    // Everything up to and including a step, applied in order.
    stateAt(index) {
      const state = {};
      for (const key of this.steps().slice(0, index + 1)) Object.assign(state, this.entries.get(key));
      return state;
    }

    go({ index, forward }) {
      this.apply(this.stateAt(index), forward && !still());
    }

    // Scale the points' own units to fill the box, keeping their shape.
    fit(raw) {
      const xs = raw.map((p) => p[0]);
      const ys = raw.map((p) => p[1]);
      const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
      const scale = Math.min(this.box.w / (x1 - x0 || 1), this.box.h / (y1 - y0 || 1)) * 0.94;
      const cx = (x0 + x1) / 2;
      const cy = (y0 + y1) / 2;
      this.place = ([x, y]) => [this.box.x + this.box.w / 2 + (x - cx) * scale, this.box.y + this.box.h / 2 + (y - cy) * scale];
    }

    apply(state, animate) {
      const time = (ms) => (animate ? ms : 0);
      const chosen = new Set(Object.values(state.links ?? {}));

      for (const [i, point] of this.points.entries()) {
        const appear = state.show && !point.shown ? point.order * TIME.spread : 0;
        this.tween(point, "shown", state.show ? 1 : 0, time(TIME.appear), time(appear));
        this.tween(point, "tint", state.tint ? 1 : 0, time(TIME.move), time(point.order * 300));
        this.tween(point, "chosen", chosen.has(i) ? 1 : 0, time(TIME.move), time(chosen.has(i) ? TIME.link * 0.7 : 0));
      }

      const labelled = state.labels === true ? Object.keys(this.groups) : (state.labels ?? []);
      for (const label of this.labels) this.tween(label, "shown", labelled.includes(label.name) ? 1 : 0, time(TIME.move), time(300));

      const questions = state.questions ?? {};
      for (const [name, question] of this.questions) if (!(name in questions)) this.tween(question, "shown", 0, time(TIME.move));
      for (const [name, target] of Object.entries(questions)) {
        let question = this.questions.get(name);
        if (!question) question = this.addQuestion(name);
        question.label.textContent = target.label ?? "";
        [question.x, question.y] = target.at;
        question.side = target.side ?? "right";
        this.tween(question, "shown", 1, time(TIME.drop));
      }

      const links = state.links ?? {};
      for (const [name, link] of this.links) if (links[name] === undefined) this.tween(link, "drawn", 0, time(TIME.move));
      for (const [name, to] of Object.entries(links)) {
        let link = this.links.get(name);
        if (!link) link = this.addLink(name);
        link.to = to;
        this.tween(link, "drawn", 1, time(TIME.link));
      }

      this.noteText.textContent = state.note ?? "";
      this.tween(this.view, "note", state.note ? 1 : 0, time(TIME.move), time(TIME.spread));
      this.tween(this.view, "opacity", state.hide ? 0 : 1, time(TIME.move));
      this.start();
    }

    addQuestion(name) {
      const group = make("g", {}, this.questionLayer);
      const question = {
        shown: 0,
        group,
        halo: make("circle", { r: RADIUS.question * 2.2, fill: COLOUR.question, opacity: 0.18 }, group),
        dot: make("circle", { r: RADIUS.question, fill: COLOUR.question, stroke: "#020617", "stroke-width": 4 }, group),
        label: make("text", { "dominant-baseline": "central", class: "mono", fill: COLOUR.question }, group),
      };
      this.questions.set(name, question);
      return question;
    }

    addLink(name) {
      const link = { drawn: 0, line: make("line", { stroke: COLOUR.link, "stroke-width": 5, "stroke-linecap": "round" }, this.linkLayer) };
      this.links.set(name, link);
      return link;
    }

    tween(object, key, to, duration, delay = 0, curve = ease) {
      this.tweens = this.tweens.filter((tween) => !(tween.object === object && tween.key === key));
      if (!duration && !delay) {
        object[key] = to;
        return;
      }
      this.tweens.push({ object, key, from: object[key], to, start: performance.now() + delay, duration: Math.max(1, duration), curve });
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
        tween.object[tween.key] = mix(tween.from, tween.to, tween.curve(clamp(progress)));
        return progress < 1;
      });
      this.render();
      if (this.tweens.length) requestAnimationFrame(this.tick);
      else this.running = false;
    }

    render() {
      this.root.setAttribute("opacity", this.view.opacity);
      for (const point of this.points) {
        const [x, y] = this.place([point.x, point.y]);
        const colour = this.groups[point.group]?.colour ?? COLOUR.point;
        point.circle.setAttribute("cx", x);
        point.circle.setAttribute("cy", y);
        point.circle.setAttribute("r", mix(RADIUS.point, RADIUS.chosen, point.chosen) * point.shown);
        point.circle.setAttribute("fill", mixColour(COLOUR.point, colour, point.tint));
        point.circle.setAttribute("stroke", COLOUR.ring);
        point.circle.setAttribute("stroke-width", 5 * point.chosen);
        point.circle.setAttribute("opacity", point.shown * (0.75 + 0.25 * point.chosen));
      }

      for (const label of this.labels) {
        const [x, y] = this.place([label.x, label.y]);
        label.text.setAttribute("x", x);
        label.text.setAttribute("y", y - 34 + 10 * (1 - label.shown));
        label.text.setAttribute("opacity", label.shown);
      }

      for (const question of this.questions.values()) {
        const [x, y] = this.place([question.x, question.y]);
        // Drops in from above, overshooting a little as it lands.
        const fall = (1 - land(clamp(question.shown))) * 140;
        question.group.setAttribute("transform", `translate(${x} ${y - fall})`);
        question.group.setAttribute("opacity", clamp(question.shown * 3));
        const left = question.side === "left";
        question.label.setAttribute("text-anchor", left ? "end" : "start");
        question.label.setAttribute("x", (left ? -1 : 1) * (RADIUS.question + 18));
        question.label.setAttribute("y", 0);
      }

      for (const [name, link] of this.links) {
        const question = this.questions.get(name);
        const point = this.points[link.to];
        if (!question || !point) continue;
        const [x1, y1] = this.place([question.x, question.y]);
        const [x2, y2] = this.place([point.x, point.y]);
        const length = Math.hypot(x2 - x1, y2 - y1);
        link.line.setAttribute("x1", x1);
        link.line.setAttribute("y1", y1);
        link.line.setAttribute("x2", x2);
        link.line.setAttribute("y2", y2);
        link.line.setAttribute("stroke-dasharray", `${length} ${length}`);
        link.line.setAttribute("stroke-dashoffset", length * (1 - link.drawn));
        link.line.setAttribute("opacity", Math.min(1, link.drawn * 4) * question.shown);
      }

      this.noteText.setAttribute("x", this.box.x + this.box.w);
      this.noteText.setAttribute("y", this.box.y + this.box.h + 6);
      this.noteText.setAttribute("opacity", this.view.note);
    }
  }

  window.Space = Space;
})();
