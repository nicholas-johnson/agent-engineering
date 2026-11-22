import { useCallback, useEffect, useRef, useState } from 'react';
import { InlineMarkdown } from './InlineMarkdown';

// The words are drawn on a 1200×400 stage, scaled to fit the slide.
const STAGE = { width: 1200, height: 400 };
const LINE = { left: 90, right: 1110, y: 200 };
const FONT = 30;
// A rough width for one letter, to keep labels from overlapping.
const LETTER = 0.56 * FONT;
const GAP = 16;
// Label heights, tried in this order: just above the line, just below, then further out.
const LEVELS = [-50, 50, -100, 100, -150, 150];

// The same keys SlideDeck uses to move between slides.
const NEXT_KEYS = ['ArrowRight', ' ', 'Enter'];
const BACK_KEYS = ['ArrowLeft', 'Backspace'];

const WORD_LINE_CSS = `
  .word-line .word,
  .word-line .leader,
  .word-line .label {
    transition: transform 900ms cubic-bezier(0.65, 0, 0.35, 1), opacity 400ms;
  }
  .word-line text {
    font-family: ui-sans-serif, system-ui, sans-serif;
    font-size: ${FONT}px;
    font-weight: 600;
    fill: #e2e8f0;
    paint-order: stroke;
    stroke: #0f172a;
    stroke-width: 8px;
    stroke-linejoin: round;
    transition: fill 400ms;
  }
  .word-line circle {
    fill: #94a3b8;
    transition: fill 400ms;
  }
  .word-line .axis {
    stroke: #64748b;
    stroke-width: 3px;
  }
  .word-line .leader line {
    stroke: #475569;
    stroke-width: 2px;
  }
  .word-line .lit text,
  .word-line .lit circle {
    fill: #fde047;
  }
  .word-line .dim {
    opacity: 0.3;
  }
  @media (prefers-reduced-motion: reduce) {
    .word-line * {
      transition: none !important;
    }
  }
`;

// Every word evenly spaced along the line, in alphabetical order.
function alphabetical(words) {
  const sorted = Object.keys(words).sort();
  const step = (LINE.right - LINE.left) / (sorted.length - 1);
  return Object.fromEntries(sorted.map((word, i) => [word, LINE.left + i * step]));
}

// Every word at its own number, the lowest at the left end and the highest at the right.
function byNumber(words) {
  const numbers = Object.values(words);
  const low = Math.min(...numbers);
  const high = Math.max(...numbers);
  return Object.fromEntries(
    Object.entries(words).map(([word, n]) => [
      word,
      LINE.left + ((n - low) / (high - low)) * (LINE.right - LINE.left),
    ]),
  );
}

// Each word's label goes on the first level where it clears the labels already there.
function levels(xs) {
  const ends = LEVELS.map(() => -Infinity);
  const placed = {};
  for (const [word, x] of Object.entries(xs).sort((a, b) => a[1] - b[1])) {
    const half = (word.length * LETTER) / 2;
    let level = ends.findIndex((end) => end + GAP < x - half);
    if (level === -1) level = ends.indexOf(Math.min(...ends));
    ends[level] = x + half;
    placed[word] = { x, dy: LEVELS[level] };
  }
  return placed;
}

// A slide that puts words on a line, one number each, and moves them as it steps. Each step has
// a caption. The right arrow (or space, or enter) plays the next step and the left arrow goes back
// one; on the last step, the right arrow moves on to the next slide. The dots show where you are,
// and click to jump to a step.
//
//   content: {
//     title,
//     words: { word: number, … },
//     steps: [{ caption, placed, highlight }],
//     note,      optional small print under the dots
//   }
//
// Until a step says `placed: true`, the words sit in alphabetical order. `highlight` lists the
// words to light up; the rest fade. Each step carries on from the one before.
export function WordLineSlide({ content }) {
  const { title, words, steps, note } = content;
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

  const { placed = false, highlight = [] } = Object.assign(
    {},
    ...steps.slice(0, index + 1),
  );
  const positions = levels(placed ? byNumber(words) : alphabetical(words));

  return (
    <div className="flex-1 min-h-0 flex flex-col items-center animate-fade-in px-8 pt-6 pb-4 w-full">
      <style>{WORD_LINE_CSS}</style>
      <h1 className="text-3xl md:text-4xl font-bold text-white text-center mb-2">
        {title}
      </h1>
      <div className="flex-1 min-h-0 w-full max-w-[1500px]">
        <svg
          viewBox={`0 0 ${STAGE.width} ${STAGE.height}`}
          className="word-line block w-full h-full"
          role="img"
          aria-label={title}
        >
          <line
            className="axis"
            x1={LINE.left - 40}
            x2={LINE.right + 40}
            y1={LINE.y}
            y2={LINE.y}
          />
          {/* Every leader, then every dot, then every label, so a label always covers the lines. */}
          {['leader', 'dot', 'label'].map((part) => (
            <g key={part}>
              {Object.keys(words).map((word) => {
                const { x, dy } = positions[word];
                const lit = highlight.includes(word);
                const dim = highlight.length > 0 && !lit;
                // The leader runs from the dot to just short of the label.
                const reach = dy - Math.sign(dy) * FONT * 0.6;
                return (
                  <g
                    key={word}
                    className={`word${lit ? ' lit' : ''}${dim ? ' dim' : ''}`}
                    style={{ transform: `translate(${x}px, ${LINE.y}px)` }}
                  >
                    {part === 'leader' && (
                      <g className="leader" style={{ transform: `scaleY(${reach})` }}>
                        <line
                          x1={0}
                          y1={0}
                          x2={0}
                          y2={1}
                          vectorEffect="non-scaling-stroke"
                        />
                      </g>
                    )}
                    {part === 'dot' && <circle r={9} />}
                    {part === 'label' && (
                      <g className="label" style={{ transform: `translateY(${dy}px)` }}>
                        <text textAnchor="middle" dominantBaseline="central">
                          {word}
                        </text>
                      </g>
                    )}
                  </g>
                );
              })}
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
