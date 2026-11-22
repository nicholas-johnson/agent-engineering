import { Fragment } from 'react';
import Markdown from 'markdown-to-jsx/react';

const OPTIONS = {
  wrapper: Fragment,
  disableAutoLink: true,
  disableParsingRawHTML: true,
  overrides: {
    strong: { props: { className: 'font-bold text-white' } },
    em: { props: { className: 'italic' } },
    code: {
      props: {
        className:
          'bg-slate-700 text-amber-300 px-1.5 py-0.5 rounded text-[0.9em] font-mono',
      },
    },
  },
};

// A bullet such as "1. Keep the words" is text, not a one-item list.
function escapeBlockStart(text) {
  return text.replace(/^(\d+)([.)])(?=\s)/, '$1\\$2').replace(/^([-+*>#])(?=\s)/, '\\$1');
}

// A template literal keeps its source indentation, and four spaces would make a code block.
function dedent(text) {
  const [first, ...rest] = text.split('\n');
  const indent = Math.min(
    ...rest.filter((line) => line.trim()).map((line) => line.search(/\S/)),
  );
  return [first, ...rest.map((line) => line.slice(indent))].join('\n');
}

export function InlineMarkdown({ text }) {
  if (typeof text !== 'string') return text;
  return (
    <Markdown options={{ ...OPTIONS, forceInline: true }}>
      {escapeBlockStart(text)}
    </Markdown>
  );
}

export function BlockMarkdown({ text }) {
  if (typeof text !== 'string') return text;
  return <Markdown options={{ ...OPTIONS, forceBlock: true }}>{dedent(text)}</Markdown>;
}
