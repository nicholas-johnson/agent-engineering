import { useCallback, useEffect, useRef, useState } from 'react';
import { InlineMarkdown } from './InlineMarkdown';

// The same keys SlideDeck uses to move between slides.
const NEXT_KEYS = ['ArrowRight', ' ', 'Enter'];
const BACK_KEYS = ['ArrowLeft', 'Backspace'];

// What lights up in the loop diagram at each kind of step.
const LIT = {
  ask: { nodes: ['question', 'model'], edges: ['ask'] },
  call: { nodes: ['model', 'decision'], edges: ['think'] },
  run: { nodes: ['decision', 'run'], edges: ['yes'] },
  back: { nodes: ['run', 'model'], edges: ['back'] },
  answer: { nodes: ['model', 'decision', 'answer'], edges: ['think', 'no'] },
};

// Steps where the whole conversation goes to the model.
const SENT = ['ask', 'back'];

// The clip deck's colours, typing and streaming (clip-deck/src/style.css), scoped to this slide.
const TOOL_LOOP_CSS = `
  .tool-loop {
    --card: rgba(30, 41, 59, 0.6);
    --border: #334155;
    --muted: #94a3b8;
    --primary: #0ea5e9;
    --secondary: #c084fc;
    --python: #4ade80;
  }
  .tool-loop .node rect, .tool-loop .node polygon {
    fill: rgba(30, 41, 59, 0.6);
    stroke: var(--border);
    stroke-width: 3;
    transition: fill 0.4s ease, stroke 0.4s ease;
  }
  .tool-loop .node text {
    fill: var(--muted);
    font: 600 26px ui-sans-serif, system-ui, sans-serif;
    text-anchor: middle;
    dominant-baseline: central;
    transition: fill 0.4s ease;
  }
  .tool-loop .node.lit text { fill: #fff; }
  .tool-loop .node.lit rect, .tool-loop .node.lit polygon {
    stroke: var(--colour);
    fill: color-mix(in srgb, var(--colour) 18%, transparent);
  }
  .tool-loop .edge {
    fill: none;
    stroke: var(--border);
    stroke-width: 3;
    transition: stroke 0.4s ease;
  }
  .tool-loop .edge.lit {
    stroke: var(--primary);
    stroke-dasharray: 12 8;
    animation: tool-loop-march 0.6s linear infinite;
  }
  .tool-loop .edge-label {
    fill: var(--muted);
    font: 600 22px ui-sans-serif, system-ui, sans-serif;
  }
  @keyframes tool-loop-march { to { stroke-dashoffset: -20; } }

  .tool-loop .conversation {
    border: 2px dashed transparent;
    border-radius: 24px;
    transition: border-color 0.4s ease;
  }
  .tool-loop .conversation.sent { border-color: var(--primary); }
  .tool-loop .sent-label {
    color: var(--primary);
    opacity: 0;
    transition: opacity 0.4s ease;
  }
  .tool-loop .conversation.sent .sent-label { opacity: 1; }

  .tool-loop .message { animation: tool-loop-in 0.45s ease both; }
  .tool-loop .bubble { padding: 0.9em 1.1em; border-radius: 22px; line-height: 1.3; }
  .tool-loop .bubble.you {
    align-self: flex-end;
    max-width: 85%;
    background: var(--primary);
    border-bottom-right-radius: 6px;
  }
  .tool-loop .bubble.answer {
    max-width: 92%;
    background: var(--card);
    border: 2px solid var(--secondary);
    border-bottom-left-radius: 6px;
  }
  .tool-loop .card {
    padding: 0.8em 1.1em;
    border-radius: 20px;
    background: var(--card);
    border: 2px solid var(--border);
    border-top-width: 7px;
  }
  .tool-loop .card.call { border-top-color: var(--secondary); }
  .tool-loop .card.result { border-top-color: var(--python); }
  .tool-loop .who { color: var(--muted); font-weight: 700; font-size: 0.8em; margin-bottom: 0.3em; }
  .tool-loop .mono { font-family: Menlo, "SF Mono", Consolas, monospace; }

  .tool-loop .typed {
    display: inline-block;
    vertical-align: top;
    overflow: hidden;
    white-space: nowrap;
    width: calc(var(--chars) * 1ch);
    animation: tool-loop-type calc(var(--chars) * 40ms) steps(var(--chars), end) 0.3s both;
  }
  .tool-loop .word { animation: tool-loop-word 0.15s ease both; animation-delay: calc(0.4s + var(--i) * 80ms); }
  @keyframes tool-loop-in { from { opacity: 0; transform: translateY(24px); } }
  @keyframes tool-loop-type { from { width: 0; } }
  @keyframes tool-loop-word { from { opacity: 0; } }

  .tool-loop.still .edge.lit, .tool-loop.still .message, .tool-loop.still .typed, .tool-loop.still .word,
  .tool-loop .message.settled, .tool-loop .settled .typed, .tool-loop .settled .word {
    animation: none;
  }
`;

function Node({ id, lit, colour, children }) {
  return (
    <g className={`node ${lit.includes(id) ? 'lit' : ''}`} style={{ '--colour': colour }}>
      {children}
    </g>
  );
}

function LoopDiagram({ at }) {
  const { nodes, edges } = LIT[at] ?? { nodes: [], edges: [] };
  const edge = (id) => `edge ${edges.includes(id) ? 'lit' : ''}`;
  const arrow = (id) => `url(#tool-loop-arrow${edges.includes(id) ? '-lit' : ''})`;
  return (
    <svg viewBox="0 0 620 600" className="block w-full h-full" role="img" aria-label="The tool loop">
      <defs>
        {[
          ['tool-loop-arrow', '#334155'],
          ['tool-loop-arrow-lit', '#0ea5e9'],
        ].map(([id, fill]) => (
          <marker key={id} id={id} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill={fill} />
          </marker>
        ))}
      </defs>

      <path className={edge('ask')} d="M170,90 V156" markerEnd={arrow('ask')} />
      <path className={edge('think')} d="M170,230 V276" markerEnd={arrow('think')} />
      <path className={edge('yes')} d="M300,340 H376" markerEnd={arrow('yes')} />
      <path className={edge('back')} d="M490,305 V195 H304" markerEnd={arrow('back')} />
      <path className={edge('no')} d="M170,400 V496" markerEnd={arrow('no')} />
      <text className="edge-label" x="316" y="326">yes</text>
      <text className="edge-label" x="184" y="456">no</text>

      <Node id="question" lit={nodes} colour="#0ea5e9">
        <rect x="40" y="20" width="260" height="70" rx="16" />
        <text x="170" y="55">Question</text>
      </Node>
      <Node id="model" lit={nodes} colour="#c084fc">
        <rect x="40" y="160" width="260" height="70" rx="16" />
        <text x="170" y="195">Model</text>
      </Node>
      <Node id="decision" lit={nodes} colour="#0ea5e9">
        <polygon points="40,340 170,280 300,340 170,400" />
        <text x="170" y="340">Tool call?</text>
      </Node>
      <Node id="run" lit={nodes} colour="#4ade80">
        <rect x="380" y="305" width="220" height="70" rx="16" />
        <text x="490" y="340">Run the tool</text>
      </Node>
      <Node id="answer" lit={nodes} colour="#c084fc">
        <rect x="40" y="500" width="260" height="70" rx="16" />
        <text x="170" y="535">Answer</text>
      </Node>
    </svg>
  );
}

function Typed({ text }) {
  return (
    <span className="typed mono" style={{ '--chars': text.length }}>
      {text}
    </span>
  );
}

function Streamed({ text }) {
  return text.split(' ').map((word, i) => (
    <span key={i} className="word" style={{ '--i': i }}>
      {i > 0 ? ' ' : ''}
      {word}
    </span>
  ));
}

// Only the newest message animates, so jumping ahead with the dots shows the rest as they ended.
function Message({ kind, label, text, settled }) {
  const settle = settled ? 'settled' : '';
  if (kind === 'you') return <div className={`message bubble you ${settle}`}>{text}</div>;
  if (kind === 'answer')
    return (
      <div className={`message bubble answer ${settle}`}>
        <Streamed text={text} />
      </div>
    );
  return (
    <div className={`message card ${kind} ${settle}`}>
      {label && <p className="who">{label}</p>}
      <Typed text={text} />
    </div>
  );
}

// One run of the tool loop, a step at a time: the loop diagram lights up on the left, and the
// conversation builds up on the right, in the clip deck's style. Keys and dots work as in
// NetworkSlide; in the PDF export, the slide shows its last step.
//
//   content: {
//     title,
//     steps: [{
//       caption,
//       at,       where the loop is: 'ask', 'call', 'run', 'back' or 'answer'
//       message,  optional, added to the conversation: { kind: 'you' | 'call' | 'result' | 'answer', label, text }
//     }],
//   }
export function ToolLoopSlide({ content }) {
  const { title, steps } = content;
  const printing =
    typeof window !== 'undefined' && window.location.pathname.endsWith('/print');

  const [index, setIndex] = useState(printing ? steps.length - 1 : 0);
  const indexRef = useRef(index);

  const show = useCallback((to) => {
    indexRef.current = to;
    setIndex(to);
  }, []);

  // As in NetworkSlide: the arrow keys step through, and carry on to the neighbouring slide at
  // either end. Listening in the capture phase keeps the deck's own handler from seeing them.
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

  const step = steps[index];
  const messages = steps
    .slice(0, index + 1)
    .map((s, i) => s.message && <Message key={i} {...s.message} settled={i < index} />)
    .filter(Boolean);

  return (
    <div
      className={`tool-loop ${printing ? 'still' : ''} flex-1 min-h-0 flex flex-col items-center animate-fade-in px-8 pt-6 pb-4 w-full`}
    >
      <style>{TOOL_LOOP_CSS}</style>
      <h1 className="text-3xl md:text-4xl font-bold text-white text-center mb-4">{title}</h1>
      <div className="flex-1 min-h-0 w-full max-w-[1700px] grid grid-cols-[2fr_3fr] grid-rows-[minmax(0,1fr)] gap-10 items-center">
        <div className="h-full min-h-0 flex items-center">
          <LoopDiagram at={step.at} />
        </div>
        <div
          className={`conversation ${SENT.includes(step.at) ? 'sent' : ''} max-h-full overflow-hidden flex flex-col gap-[0.6em] p-[0.8em] text-white`}
          style={{ fontSize: 'clamp(14px, 2.5vh, 30px)' }}
        >
          <p className="sent-label text-[0.7em] font-semibold -mb-[0.3em]">
            The whole conversation goes to the model
          </p>
          {messages}
        </div>
      </div>
      <p className="text-2xl md:text-3xl text-gray-200 text-center min-h-[2.5em] max-w-5xl mt-2">
        <InlineMarkdown text={step.caption} />
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
    </div>
  );
}
