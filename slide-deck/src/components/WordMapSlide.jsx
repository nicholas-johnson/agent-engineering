import { useCallback, useEffect, useRef, useState } from 'react';
import { InlineMarkdown } from './InlineMarkdown';

// The map is drawn on a 1200×680 stage, scaled to fit the slide. The middle of the map is the
// centre of the stage, and the circle the words move out to has this radius.
const STAGE = { width: 1200, height: 680 };
const MIDDLE = { x: 600, y: 340 };
const RADIUS = 230;
const FONT = 26;
// A rough width for one letter, to keep labels from overlapping.
const LETTER = 0.56 * FONT;
const COLOURS = ['#38bdf8', '#fbbf24', '#f472b6', '#4ade80', '#c084fc'];
const LIT = '#fde047';
const SUM = '#f8fafc';
const ARC = 80;
// A sentence's arrows are added on one at a time, this far apart.
const BEAT = 450;

// The same keys SlideDeck uses to move between slides.
const NEXT_KEYS = ['ArrowRight', ' ', 'Enter'];
const BACK_KEYS = ['ArrowLeft', 'Backspace'];

const WORD_MAP_CSS = `
  .word-map .dot,
  .word-map .arrow,
  .word-map .leader,
  .word-map .label {
    transition: transform 900ms cubic-bezier(0.65, 0, 0.35, 1), opacity 400ms;
  }
  .word-map text {
    font-family: ui-sans-serif, system-ui, sans-serif;
    font-size: ${FONT}px;
    font-weight: 600;
    fill: #e2e8f0;
    paint-order: stroke;
    stroke: #0f172a;
    stroke-width: 7px;
    stroke-linejoin: round;
    transition: fill 400ms;
  }
  .word-map .dot circle {
    fill: #94a3b8;
    transition: fill 400ms;
  }
  .word-map .arrow line {
    stroke: #64748b;
    stroke-width: 2px;
    transition: stroke 400ms;
  }
  .word-map .leader line {
    stroke: #475569;
    stroke-width: 1.5px;
  }
  .word-map .ring {
    fill: none;
    stroke: #64748b;
    stroke-width: 2px;
    stroke-dasharray: 8 8;
    transition: opacity 600ms;
  }
  .word-map .middle {
    fill: #e2e8f0;
  }
  .word-map .angle path {
    fill: none;
    stroke: ${LIT};
    stroke-width: 4px;
  }
  .word-map .angle text {
    fill: ${LIT};
  }
  .word-map .step line {
    stroke-width: 4px;
  }
  .word-map .sum line {
    stroke: ${SUM};
    stroke-width: 6px;
  }
  .word-map .tip circle {
    fill: ${SUM};
  }
  .word-map .sentence text {
    fill: ${SUM};
    font-style: italic;
  }
  .word-map .dim {
    opacity: 0.25;
  }
  .word-map .appear {
    animation: word-map-appear 500ms both;
  }
  .word-map .grow {
    animation: word-map-grow 600ms cubic-bezier(0.65, 0, 0.35, 1) backwards;
  }
  .word-map .fade {
    animation: word-map-appear 400ms backwards;
  }
  @keyframes word-map-appear {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  @keyframes word-map-grow {
    from { transform: var(--from); }
  }
  @media (prefers-reduced-motion: reduce) {
    .word-map * {
      transition: none !important;
      animation: none !important;
    }
  }
`;

// How far one unit of the map reaches on the stage: the farthest word sits well inside the circle.
function scaleOf(words) {
  const far = Math.max(...Object.values(words).map(([x, y]) => Math.hypot(x, y)));
  return (0.85 * RADIUS) / far;
}

// Where each word's dot goes on the stage: at its own two numbers, or pushed out along its
// direction to the circle itself.
function spots(words, onCircle) {
  const scale = scaleOf(words);
  return Object.fromEntries(
    Object.entries(words).map(([word, [x, y]]) => {
      const length = Math.hypot(x, y) || 1;
      const reach = onCircle ? RADIUS / length : scale;
      return [word, [MIDDLE.x + x * reach, MIDDLE.y - y * reach]];
    }),
  );
}

function overlaps(a, b) {
  return a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3];
}

// Each label sits just outside its dot, away from the middle. If that spot is taken (by another
// label, another word's dot, or the edge of the stage), it tries to either side, then further
// out. A label that had to move gets a thin line back to its dot. `taken` starts with boxes
// already in use. With `centre`, a label that can't fit beside its dot is centred on it instead.
function labels(points, { taken = [], centre = false } = {}) {
  const placed = {};
  const dots = Object.fromEntries(
    Object.entries(points).map(([word, [x, y]]) => [
      word,
      [x - 10, y - 10, x + 10, y + 10],
    ]),
  );
  const around = (word) =>
    Math.atan2(points[word][1] - MIDDLE.y, points[word][0] - MIDDLE.x);
  for (const word of Object.keys(points).sort((a, b) => around(a) - around(b))) {
    const [px, py] = points[word];
    const distance = Math.hypot(px - MIDDLE.x, py - MIDDLE.y);
    const [ux, uy] =
      distance > 1 ? [(px - MIDDLE.x) / distance, (py - MIDDLE.y) / distance] : [1, 0];
    const facing = ux > 0.35 ? 'start' : ux < -0.35 ? 'end' : 'middle';
    const anchors = centre && facing !== 'middle' ? [facing, 'middle'] : [facing];
    const width = word.length * LETTER;
    const others = Object.entries(dots).filter(([other]) => other !== word);
    let best = null;
    for (const anchor of anchors) {
      const gap = 14 + (anchor === 'middle' ? FONT * 0.5 : 0);
      // Above or below the middle, a sideways move must clear a whole word, not just a line.
      const sideways = anchor === 'middle' ? width / 2 + 10 : FONT + 4;
      for (const out of [0, 24, 48, 72]) {
        for (const side of [0, 1, -1, 2, -2]) {
          const x = px + ux * (gap + out) - uy * side * sideways;
          const y = py + uy * (gap + out) + ux * side * sideways;
          const left =
            anchor === 'start' ? x : anchor === 'end' ? x - width : x - width / 2;
          const box = [left - 3, y - FONT / 2 - 2, left + width + 3, y + FONT / 2 + 2];
          const outside =
            box[0] < 0 || box[1] < 0 || box[2] > STAGE.width || box[3] > STAGE.height;
          const hits =
            taken.filter((other) => overlaps(other, box)).length +
            others.filter(([, dot]) => overlaps(dot, box)).length +
            (outside ? 1 : 0);
          if (!best || hits < best.hits)
            best = { x, y, box, hits, anchor, moved: out > 0 || side !== 0 };
          if (hits === 0) break;
        }
        if (best.hits === 0) break;
      }
      if (best.hits === 0) break;
    }
    taken.push(best.box);
    // The point on the label nearest its dot, for the line back to it.
    const edge = [
      Math.min(Math.max(px, best.box[0]), best.box[2]),
      Math.min(Math.max(py, best.box[1]), best.box[3]),
    ];
    placed[word] = {
      x: best.x,
      y: best.y,
      anchor: best.anchor,
      moved: best.moved,
      edge,
      box: best.box,
    };
  }
  return placed;
}

// The transform that turns a line from (0, 0) to (1, 0) into a line between two stage points.
function along([x1, y1], [x2, y2], length = Math.hypot(x2 - x1, y2 - y1)) {
  const turn = (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI;
  return `translate(${x1}px, ${y1}px) rotate(${turn}deg) scaleX(${length})`;
}

// A sentence's words, arrow after arrow, tip to tail from the middle: where each one starts and
// ends on the stage. The last one ends at the sum of them all.
function chain(list, words, scale) {
  let [x, y] = [0, 0];
  return list.map((word) => {
    const from = [MIDDLE.x + x * scale, MIDDLE.y - y * scale];
    x += words[word][0];
    y += words[word][1];
    return { word, from, to: [MIDDLE.x + x * scale, MIDDLE.y - y * scale] };
  });
}

// The arc between two words' directions, the short way round, and how many degrees it spans.
// Its label sits just outside the arc. If that spot is in `taken` (a label or a dot), the arc and
// its label move further out, but no further than `reach`, the shorter of the two arrows.
function arc(words, [a, b], { taken = [], reach = Infinity } = {}) {
  const from = Math.atan2(words[a][1], words[a][0]);
  const to = Math.atan2(words[b][1], words[b][0]);
  const turn = ((to - from + 3 * Math.PI) % (2 * Math.PI)) - Math.PI;
  const at = (angle, r) => [
    MIDDLE.x + r * Math.cos(angle),
    MIDDLE.y - r * Math.sin(angle),
  ];
  const text = `${Math.round((Math.abs(turn) * 180) / Math.PI)}°`;
  const width = text.length * LETTER;
  const free = (r) => {
    const [x, y] = at(from + turn / 2, r + 34);
    const box = [
      x - width / 2 - 3,
      y - FONT / 2 - 2,
      x + width / 2 + 3,
      y + FONT / 2 + 2,
    ];
    return !taken.some((other) => overlaps(other, box));
  };
  const tries = [ARC, ARC + 40, ARC + 80, ARC + 120, ARC + 160].filter(
    (r) => r === ARC || r + 34 < reach,
  );
  const radius = tries.find(free) ?? ARC;
  const [sx, sy] = at(from, radius);
  const [ex, ey] = at(from + turn, radius);
  const [lx, ly] = at(from + turn / 2, radius + 34);
  return {
    path: `M ${sx} ${sy} A ${radius} ${radius} 0 0 ${turn > 0 ? 0 : 1} ${ex} ${ey}`,
    label: { x: lx, y: ly, text },
  };
}

// A slide that draws words as points on a map, two numbers each, around a middle point, and
// steps through it. Each step has a caption. The right arrow (or space, or enter) plays the next
// step and the left arrow goes back one; on the last step, the right arrow moves on to the next
// slide. The dots show where you are, and click to jump to a step.
//
//   content: {
//     title,
//     words: { word: [x, y], … },       the middle of the map is [0, 0]
//     groups: { word: 1, … },           optional: which group each word is in
//     sentences: { name: [word, …] },   optional: words to add up into one arrow
//     steps: [{ caption, arrows, circle, grouped, highlight, angle, sentences, average }],
//     note,                              optional small print under the dots
//   }
//
// `arrows` draws a line from the middle to every word, `circle` pushes every word out to a
// circle along its own direction, `grouped` colours the words by group, `highlight` lights up some
// words and fades the rest, and `angle: [a, b]` draws the angle between two words or sentences.
// A step's `sentences` lists the sentences to draw: each word's arrow added on, tip to tail, then
// one arrow for the sum. `average` shrinks each sum to the average: the same direction. Draw
// sentences without `circle`, since they need the words' real lengths. Each step carries on from
// the one before.
export function WordMapSlide({ content }) {
  const { title, words, groups = {}, sentences = {}, steps, note } = content;
  // The PDF export prints every slide at once: show the last step, still.
  const printing =
    typeof window !== 'undefined' && window.location.pathname.endsWith('/print');

  const [index, setIndex] = useState(printing ? steps.length - 1 : 0);
  const indexRef = useRef(index);

  const show = useCallback((to) => {
    indexRef.current = to;
    setIndex(to);
  }, []);

  // The arrow keys step through the slide. On the first or last step they carry on to the
  // neighbouring slide as usual. This listens in the capture phase and stops the key there when
  // it uses it, so the deck's own handler never sees it.
  useEffect(() => {
    if (printing) return undefined;
    const onKey = (event) => {
      if (event.metaKey || event.ctrlKey || event.altKey) return;
      const at = indexRef.current;
      let to = null;
      if (NEXT_KEYS.includes(event.key) && at < steps.length - 1) to = at + 1;
      else if (BACK_KEYS.includes(event.key) && at > 0) to = at - 1;
      if (to === null) return;
      event.preventDefault();
      event.stopImmediatePropagation();
      show(to);
    };
    window.addEventListener('keydown', onKey, true);
    return () => window.removeEventListener('keydown', onKey, true);
  }, [printing, steps.length, show]);

  const {
    arrows = false,
    circle = false,
    grouped = false,
    highlight = [],
    angle = null,
    sentences: drawn = [],
    average = false,
  } = Object.assign({}, ...steps.slice(0, index + 1));
  const points = spots(words, circle);
  const placed = labels(points);
  const scale = scaleOf(words);
  const chains = Object.fromEntries(
    drawn.map((name) => [name, chain(sentences[name], words, scale)]),
  );
  // Each sum's own two numbers (for its angle), and where its tip goes on the stage.
  const sums = Object.fromEntries(
    drawn.map((name) => {
      const [ex, ey] = chains[name].at(-1).to;
      return [name, [(ex - MIDDLE.x) / scale, (MIDDLE.y - ey) / scale]];
    }),
  );
  const tips = Object.fromEntries(
    drawn.map((name) => {
      const shrink = average ? sentences[name].length : 1;
      const [x, y] = sums[name];
      return [name, [MIDDLE.x + (x * scale) / shrink, MIDDLE.y - (y * scale) / shrink]];
    }),
  );
  // Sentence labels go wherever the words' labels and dots aren't.
  const said = labels(tips, {
    taken: [
      ...Object.values(placed).map((label) => label.box),
      ...Object.values(points).map(([x, y]) => [x - 10, y - 10, x + 10, y + 10]),
    ],
    centre: true,
  });
  const ends = { ...words, ...sums };
  const shown =
    angle &&
    arc(ends, angle, {
      taken: [
        ...Object.values(placed).map((label) => label.box),
        ...Object.values(said).map((label) => label.box),
        ...Object.values({ ...points, ...tips }).map(([x, y]) => [
          x - 10,
          y - 10,
          x + 10,
          y + 10,
        ]),
      ],
      reach: circle
        ? RADIUS
        : Math.min(...angle.map((name) => Math.hypot(...ends[name]) * scale)),
    });
  // The PDF export can't wait for animations, so it draws everything at once.
  const animate = (name) => (printing ? '' : ` ${name}`);
  const delay = (beats, extra = 0) =>
    printing ? undefined : `${beats * BEAT + extra}ms`;

  const colour = (word) => {
    if (grouped && groups[word]) return COLOURS[(groups[word] - 1) % COLOURS.length];
    if (highlight.includes(word)) return LIT;
    return undefined;
  };
  const dim = (word) => highlight.length > 0 && !highlight.includes(word);

  return (
    <div className="flex-1 min-h-0 flex flex-col items-center animate-fade-in px-8 pt-6 pb-4 w-full">
      <style>{WORD_MAP_CSS}</style>
      <h1 className="text-3xl md:text-4xl font-bold text-white text-center mb-2">
        {title}
      </h1>
      <div className="flex-1 min-h-0 w-full max-w-[1500px]">
        <svg
          viewBox={`0 0 ${STAGE.width} ${STAGE.height}`}
          className="word-map block w-full h-full"
          role="img"
          aria-label={title}
        >
          <circle
            className="ring"
            cx={MIDDLE.x}
            cy={MIDDLE.y}
            r={RADIUS}
            style={{ opacity: circle ? 1 : 0 }}
          />
          {/* Every arrow, then every dot, then every label, so a label always covers the lines. */}
          {Object.keys(words).map((word) => {
            const [px, py] = points[word];
            const turn = (Math.atan2(py - MIDDLE.y, px - MIDDLE.x) * 180) / Math.PI;
            const length = Math.hypot(px - MIDDLE.x, py - MIDDLE.y);
            return (
              <g
                key={word}
                className="arrow"
                style={{
                  transform: `translate(${MIDDLE.x}px, ${MIDDLE.y}px) rotate(${turn}deg) scaleX(${length})`,
                  opacity: arrows ? (dim(word) ? 0.25 : 1) : 0,
                }}
              >
                <line
                  x1={0}
                  y1={0}
                  x2={1}
                  y2={0}
                  vectorEffect="non-scaling-stroke"
                  style={{ stroke: colour(word) }}
                />
              </g>
            );
          })}
          {Object.keys(words).map((word) => {
            const [px, py] = points[word];
            const [ex, ey] = placed[word].edge;
            const turn = (Math.atan2(ey - py, ex - px) * 180) / Math.PI;
            const length = Math.hypot(ex - px, ey - py);
            return (
              <g
                key={word}
                className="leader"
                style={{
                  transform: `translate(${px}px, ${py}px) rotate(${turn}deg) scaleX(${length})`,
                  opacity: placed[word].moved ? (dim(word) ? 0.25 : 1) : 0,
                }}
              >
                <line x1={0} y1={0} x2={1} y2={0} vectorEffect="non-scaling-stroke" />
              </g>
            );
          })}
          {/* Each sentence: its words' arrows tip to tail, then one arrow for the sum. */}
          {drawn.map((name) =>
            chains[name].map(({ word, from, to }, beat) => (
              <g
                key={`${name}-${beat}`}
                className={`arrow step${animate('grow')}`}
                style={{
                  '--from': along(from, to, 0),
                  transform: along(from, to),
                  animationDelay: delay(beat),
                  opacity: average ? 0 : 1,
                }}
              >
                <line
                  x1={0}
                  y1={0}
                  x2={1}
                  y2={0}
                  vectorEffect="non-scaling-stroke"
                  style={{ stroke: colour(word) ?? LIT }}
                />
              </g>
            )),
          )}
          {drawn.map((name) => (
            <g
              key={name}
              className={`arrow sum${animate('grow')}`}
              style={{
                '--from': along([MIDDLE.x, MIDDLE.y], tips[name], 0),
                transform: along([MIDDLE.x, MIDDLE.y], tips[name]),
                animationDelay: delay(sentences[name].length),
              }}
            >
              <line x1={0} y1={0} x2={1} y2={0} vectorEffect="non-scaling-stroke" />
            </g>
          ))}
          {shown && (
            <g key={angle.join('-')} className="angle appear">
              <path d={shown.path} />
              <text
                x={shown.label.x}
                y={shown.label.y}
                textAnchor="middle"
                dominantBaseline="central"
              >
                {shown.label.text}
              </text>
            </g>
          )}
          <circle className="middle" cx={MIDDLE.x} cy={MIDDLE.y} r={6} />
          {Object.keys(words).map((word) => (
            <g
              key={word}
              className={`dot${dim(word) ? ' dim' : ''}`}
              style={{
                transform: `translate(${points[word][0]}px, ${points[word][1]}px)`,
              }}
            >
              <circle r={8} style={{ fill: colour(word) }} />
            </g>
          ))}
          {drawn.map((name) => (
            <g
              key={name}
              className={`dot tip${animate('fade')}`}
              style={{
                transform: `translate(${tips[name][0]}px, ${tips[name][1]}px)`,
                animationDelay: delay(sentences[name].length, 400),
              }}
            >
              <circle r={10} />
            </g>
          ))}
          {Object.keys(words).map((word) => (
            <g
              key={word}
              className={`label${dim(word) ? ' dim' : ''}`}
              style={{ transform: `translate(${placed[word].x}px, ${placed[word].y}px)` }}
            >
              <text
                textAnchor={placed[word].anchor}
                dominantBaseline="central"
                style={{ fill: colour(word) }}
              >
                {word}
              </text>
            </g>
          ))}
          {drawn.map((name) => (
            <g
              key={name}
              className={`label sentence${animate('fade')}`}
              style={{
                transform: `translate(${said[name].x}px, ${said[name].y}px)`,
                animationDelay: delay(sentences[name].length, 400),
              }}
            >
              <text textAnchor={said[name].anchor} dominantBaseline="central">
                {name}
              </text>
            </g>
          ))}
        </svg>
      </div>
      <p className="text-2xl md:text-3xl text-gray-200 text-center min-h-[4.5rem] max-w-5xl">
        <InlineMarkdown text={steps[index].caption} />
      </p>
      {!printing && (
        <div className="flex gap-3 mt-2">
          {steps.map((_, i) => (
            <button
              key={i}
              onClick={() => show(i)}
              className={`w-3 h-3 rounded-full transition-colors ${i === index ? 'bg-primary' : 'bg-slate-600 hover:bg-slate-500'}`}
              aria-label={`Step ${i + 1} of ${steps.length}`}
            />
          ))}
        </div>
      )}
      {note && (
        <p className="text-sm md:text-base text-gray-400 text-center max-w-4xl mt-3">
          {note}
        </p>
      )}
    </div>
  );
}
