# Module guide

How a module of the Agent Engineering course is put together. **Module 1, `day-one/module-01-intro-to-language-models/`, is the reference example.** When in doubt, look at how it does it.

## Where modules live

```text
day-one/
  README.md                          ← table of the day's modules
  module-01-intro-to-language-models/
  module-02-.../
day-two/
  module-05-.../
```

- Each day folder is `day-<word>` and holds four modules.
- Module numbers run across the whole course, not per day: Day Two starts at module 05. This keeps commands like `pnpm slides:05` unique.
- Module folders are `module-NN-short-slug`.
- Update the day's `README.md` table when you add a module.

## What goes in a module

```text
module-NN-slug/
  README.md          ← the full written explanation
  slides/            ← the slide deck (Vite + React, uses ../../../slide-deck)
  demo/              ← numbered demo scripts, one per section
    output/          ← written by the demos, gitignored
  data/              ← corpora and other input files, plus any script that builds them
  playground/        ← things to play with between exercises
  further-reading/   ← the final exercise: papers, books and extension projects
```

## How a module is designed

**Agree the outline first.** The course is built step by step with Nicholas. Before building anything, propose the module's sections and what each demo will show, point out problems with the plan, and wait for agreement.

**Tell a story.** A module is a sequence of steps, each one a working idea with a weakness that motivates the next step. Module 1 goes: count word pairs → too little context → a bigger window → too many contexts → letters → too little meaning per step → tokens → still too many contexts → a neural network that generalises.

**Don't spoil the story.**

- No "the plan" slide listing every section up front.
- Each section shows its demo **before** explaining why it breaks.
- Results go on slides _after_ the demo that produces them.

**Small, then large.** Where a demo runs on data, run it on something small first, then something larger (Module 1: chapter 1 of _Alice_, then the whole book). The contrast is usually the lesson.

**One thread through every demo.** Use the same prompt, input or task in every demo so learners can compare the steps directly (Module 1 completes _"alice was beginning to get"_ in all five).

## Demos

Demos are teaching scripts, not reusable code. Keep them clean and simple.

- Named `demo/NN_short_name.py`, one per section, numbered in order.
- **Plain Python, standard library only**, unless a dependency has been agreed.
- Settings are module-level constants (`WINDOW = 5`). **No optional parameters, no command-line flags, no configuration.**
- A few small functions and top-level script flow. No classes unless they are the point.
- Short comments only where a line isn't obvious. No big comment blocks.
- Duplicate a small helper between demos rather than sharing a module. Each demo should read on its own.
- **Write what was built to a file** in `demo/output/` (gitignored), in a form people can open, look through and search: indented JSON, or one item per line of text.
- **Print only the payoff.** In Module 1 that is a heading per corpus and three sentence completions. No statistics, top-five lists or diagnostics; those belong in the README and slides.
- **End with the thing the module is about**, visibly working: in Module 1, completing a sentence.
- If a demo takes more than a few seconds, show a single progress line that updates in place (`print(..., end="\r")`) so it doesn't look frozen.
- Paths are relative to the script (`Path(__file__).parent`), so demos run from any folder.
- Run with `uv run python demo/NN_name.py` from the module folder. The system `python3` is too old.

### Demos that call an API

Module 2 is the reference for these.

- Use OpenAI's **Responses API** (`client.responses.create`, `output_text`, `input=` and `instructions=`). The older Chat Completions API is mentioned once, on one slide in Module 2, and nowhere else.
- Call `load_dotenv()` at the top; the key lives in `.env` at the repo root. Never print or commit a key.
- `MODEL = "gpt-6-luna"` as a constant, with `reasoning={"effort": "none"}` unless the demo is about reasoning. `temperature`, `top_p` and log probabilities only work when reasoning effort is `"none"`.
- Interactive demos read from `input()` and stop on an empty line. Write the transcript to `demo/output/`.
- Check a model or parameter against OpenAI's documentation, and with a real call, before relying on it. Model names and supported parameters change.
- Test interactive scripts by piping input in: `printf 'Hello\n\n' | uv run python demo/02_chat_loop.py`.

## The module README

Written for someone reading on their own after the session. In order:

1. `# Module N — Title`, then a one-paragraph `>` summary of the whole story.
2. **Learning goals**: bullet points, key terms in bold.
3. **The core idea** in plain language.
4. **The data**: a table of the files in `data/`, with sources and licences.
5. **Running the demos**: the `uv run` command, a table of what each demo writes to `demo/output/`, and a note that output is random where it is.
6. **One section per step**, `## N. Title`, each with:
   - `**Demo:** \`demo/NN_name.py\``
   - the idea, with the few lines of code that matter
   - real output, quoted
   - real numbers, usually in a table comparing the small and large data
   - why it breaks, leading into the next section
7. **Summary**: a table of the steps and the problem each one has.
8. **Playground** and **Further reading and extensions**: a sentence each, with links.
9. **Slides**: the `pnpm slides:NN` command.

**Every quoted output and number must come from actually running the code.** Never make up example output. If the code changes, rerun it and update the quotes.

## Slides

The deck is `slides/src/slides.js`, an array of slide objects rendered by the shared `slide-deck` package. See `slide-deck/README.md` for the slide types, but note that `standard` slides take `icon`, not `emoji`. Icons must be names from `slide-deck/src/components/SlideIcon.jsx`.

Structure:

1. Course title slide (`Agent Engineering`, `Nicholas Johnson`), then the module title slide.
2. A few intro slides: the core question, and the data. No plan slide.
3. For each section:
   - a `title` slide: `N. Section name` with a short subtitle
   - two or three explanation slides (`standard`, `code`, `comparison`, `equation`, `description`)
   - a demo handoff: a `title` slide, `Demo — Section name`, subtitle `Switch to terminal: python demo/NN_name.py`, icon `rocket`
   - after the demo: a `Why this breaks` slide (`description`, icon `warning`) quoting real output, or a results slide
4. Wrap-up: a `Wrap-up` title slide, a comparison or summary, `What we learned`, and a closing `Final exercise: further reading` slide.

Setting up a new deck:

- Copy `slides/` from Module 1 and change the `package.json` name to `@agent-engineering/module-NN-slides`, its description, and the `<title>` in `index.html`.
- Keep the `@source "../../../../slide-deck/src/**/*.jsx";` line in `src/index.css`; the path depends on the folder depth.
- Add `"slides:NN": "pnpm --filter @agent-engineering/module-NN-slides dev"` to the root `package.json`.
- Install the latest React, Vite and Tailwind with `pnpm --filter ... add`. Don't pin old versions.

## Playground

Things for delegates to play with between exercises. It should **build on what the module covered without repeating it**.

- `playground/README.md`: a table of the folders, what each is about, and whether the demos must be run first.
- One folder per idea, short and descriptive (`temperature`, `tokenizer-lab`). Usually six or seven.
- Each folder has `play.py` (or two scripts where that's clearer, like `train.py` and `complete.py`) and a `README.md` containing:
  - what it shows and why it's interesting, in a paragraph
  - how to run it, and whether demos must be run first
  - real example output
  - **Things to notice** (optional)
  - **Try this**: five or six numbered ideas for extending it, from easy to hard
- Same code style as demos. Where possible, load the files the demos wrote to `demo/output/` instead of rebuilding them.
- Output goes in `output/` inside the folder (gitignored).
- Good playgrounds turn a hidden setting into something you can change (temperature, window size, vocabulary size), run the model a different way (scoring instead of generating), or point it at different data.

## Further reading (the final exercise)

`further-reading/README.md`:

1. **The exercise**: pick a paper (⭐ marks good starting points), read the part that matters, write two or three sentences connecting it to a demo, then start an extension.
2. **Reading list**, grouped by the module's sections, plus "Where it went next". Each entry has:
   - a full citation in bold: authors, year, title, venue, volume and pages
   - a link where one exists (arXiv preferred)
   - a short paragraph: what the paper did, **which part to look for**, and **which demo or playground it connects to**
3. **Books, videos and posts**, with links.
4. **Extensions**: bigger projects than the playground, rated ★ (an afternoon) to ★★★ (a weekend). They must not repeat the playground's "Try this" ideas.

Check every link resolves and every arXiv ID matches its title before committing. Say which citations you could not check.

## Data

- Prefer public-domain text (Project Gutenberg). Strip the Gutenberg header and footer, and replace curly quotes and dashes with plain ASCII.
- Ask before downloading anything new, saying what and from where.
- Commit the cleaned files. Record the source in the module README's data table.
- Any script that builds data (like `data/build_tokens.py`) lives in `data/` and its output is committed.

## Writing style

- British English: _neighbouring_, _generalise_, _memorise_.
- Plain language, short sentences. Explain a term the first time you use it, and put it in **bold**.
- Be honest about weaknesses: if output is rough, say so and say why.

## Before you say a module is done

- Run every demo and every playground script. Check the output files are written and readable.
- Check every quote and number in the README and slides matches a real run.
- `npx prettier --check` on the slides, then `pnpm --filter @agent-engineering/module-NN-slides build`, and delete the `dist/` folder it creates.
- Look at the slides in a browser: titles fit, code blocks don't overflow.
- Make sure `output/` folders and `dist/` are not staged.
