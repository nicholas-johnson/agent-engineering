import { useCallback, useEffect, useId, useRef, useState } from 'react';
// The animated network engine from the clip deck. It adds `Network` to the window.
import 'clip-deck/src/network.js';
import { InlineMarkdown } from './InlineMarkdown';

// The network is drawn on a 1300×700 stage, scaled to fit the slide. These are the clip deck's
// own network colours and fonts, sized for this stage.
const STAGE = { width: 1300, height: 700 };
const BOX = { x: 20, y: 20, w: 1260, h: 660 };

// The same keys SlideDeck uses to move between slides.
const NEXT_KEYS = ['ArrowRight', ' ', 'Enter'];
const BACK_KEYS = ['ArrowLeft', 'Backspace'];

const NETWORK_CSS = `
  .network-slide text {
    font-family: ui-sans-serif, system-ui, sans-serif;
    font-size: 30px;
    font-weight: 600;
    paint-order: stroke;
    stroke: rgba(15, 23, 42, 0.9);
    stroke-width: 8px;
    stroke-linejoin: round;
  }
  .network-slide .mono {
    font-family: ui-monospace, Menlo, Consolas, monospace;
    font-weight: 400;
  }
  .network-slide .weight {
    font-family: ui-monospace, Menlo, Consolas, monospace;
    font-size: 26px;
    font-weight: 700;
  }
`;

// A slide with an animated network. Each step has a caption. The right arrow (or space, or
// enter) plays the next step and the left arrow goes back one; on the last step, the right arrow
// moves on to the next slide. The dots show where you are, and click to jump to a step.
//
//   content: {
//     title,
//     steps: [{ caption, ...what the network looks like from this step on }],
//     note,      optional small print under the dots
//     stage, box optional: the drawing's size, and where the network sits in it
//   }
//
// Each step takes the fields in the clip-deck README's Networks section (layers, weights, values,
// pulse, bars, labels…), and carries on from the step before.
export function NetworkSlide({ content }) {
  const { title, steps, note } = content;
  // The PDF export prints every slide at once: show the last step, still.
  const printing =
    typeof window !== 'undefined' && window.location.pathname.endsWith('/print');

  const svgRef = useRef(null);
  const networkRef = useRef(null);
  const id = `network-${useId().replace(/:/g, '')}`;
  const [index, setIndex] = useState(printing ? steps.length - 1 : 0);
  // The step on show, and the one the network last drew, kept outside React's render.
  const indexRef = useRef(index);
  const drawnRef = useRef(-1);

  const show = useCallback(
    (to) => {
      const forward = !printing && to === drawnRef.current + 1;
      networkRef.current?.goTo(to, forward);
      drawnRef.current = to;
      indexRef.current = to;
      setIndex(to);
    },
    [printing],
  );

  useEffect(() => {
    const svg = svgRef.current;
    const network = new window.Network(svg, {
      stage: content.stage ?? STAGE,
      box: content.box ?? BOX,
      listen: false,
      steps: steps.map((_, i) => String(i)),
    });
    network.script(
      Object.fromEntries(
        steps.map(({ caption: _caption, ...entry }, i) => [String(i), entry]),
      ),
    );
    networkRef.current = network;
    // Draw the step on show, without effects: the index in state is already right.
    network.goTo(indexRef.current, false);
    drawnRef.current = indexRef.current;
    return () => {
      network.destroy();
      svg.replaceChildren();
      networkRef.current = null;
    };
  }, [content, steps]);

  // The arrow keys step through the animation. On the first or last step they carry on to the
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

  return (
    <div className="flex-1 min-h-0 flex flex-col items-center animate-fade-in px-8 pt-6 pb-4 w-full">
      <style>{NETWORK_CSS}</style>
      <h1 className="text-3xl md:text-4xl font-bold text-white text-center mb-2">
        {title}
      </h1>
      <div className="flex-1 min-h-0 w-full max-w-[1700px]">
        <svg
          ref={svgRef}
          id={id}
          className="network-slide block w-full h-full"
          role="img"
          aria-label={title}
        />
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
