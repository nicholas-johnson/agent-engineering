# Module 2 — Building a Chatbot

> In Module 1 we built a language model that could just about finish a sentence. Now we use a real one. Through OpenAI's API, a vastly bigger model does the same job — predict the next token — and we turn it into a chatbot in five steps: ask it one question, put it in a loop, discover it forgets everything, give it a memory, stream its replies as they are written, and finally show it pictures. Our chatbot is the Cheshire Cat.

## Learning goals

- Call a large language model through the **OpenAI Responses API**, and read the **response object** that comes back.
- Shape a model's behaviour with **instructions** (often called the system prompt).
- Build a **chat loop**, and explain why the API is **stateless**: the model only knows what you send it.
- Give a chatbot **memory** by sending the conversation history, and see what that costs in **tokens**.
- **Stream** a reply token by token as it is generated.
- Send **images** as well as text: a **multimodal** model.

---

## From our model to theirs

At the end of Module 1, our 26,000-parameter model completed *"alice was beginning to get"* with *"alice was beginning to getve had would meill it."*

Here is a real model, `gpt-6-luna`, given the same start and asked for the probabilities of its next few tokens:

```text
'very'      -> 'very' 77%, 'rather' 15%, 'b' 5%, 't' 4%
' tired'    -> ' tired' 100%
' of'       -> ' of' 100%
' sitting'  -> ' sitting' 100%
```

It carries on *"very tired of sitting by her sister on the bank, and of having nothing to do"*: the first line of the book, word for word, just like our five-word model in Module 1. It has read *Alice* too, and it does exactly what our models did: produce a vector of probabilities for the next token. It is just enormously better at it. (The `logprobs` playground lets you look at these probabilities yourself.)

## Setting up

You need an OpenAI API key. Create one at [platform.openai.com](https://platform.openai.com/api-keys), then copy `.env.example` at the root of the repository to `.env` and put your key in it:

```text
OPENAI_API_KEY=sk-...
```

`.env` is ignored by git, so your key won't be committed. Every demo calls `load_dotenv()`, which reads it.

This module adds the course's first two packages, `openai` and `python-dotenv`. `uv` installs them the first time you run anything.

## The data

| File | What | Source |
|------|------|--------|
| `data/mad-tea-party.png` | John Tenniel's illustration of the Mad Tea Party | [Project Gutenberg #114](https://www.gutenberg.org/ebooks/114), public domain |

## Running the demos

From this folder:

```bash
uv run python demo/01_one_response.py
```

Demos 2–5 are chats: type a message and press Enter, and press Enter on an empty line to stop. Each demo writes what happened to `demo/output/`:

| Demo | Writes |
|------|--------|
| `01_one_response.py` | `01_response.json`: the whole response object |
| `02_chat_loop.py` | `02_chat_loop.txt`: the conversation |
| `03_conversation.py` | `03_conversation.txt`: the conversation, with tokens used per turn |
| `04_streaming.py` | `04_streaming.txt`: the conversation |
| `05_images.py` | `05_images.txt`: the conversation |

Replies are random, so yours will differ from the examples below.

All the demos use `gpt-6-luna`, OpenAI's fast, low-cost GPT-6 model, with **reasoning effort** set to `"none"`. Reasoning models can "think" before they answer, which is slower and costs more tokens. For a chatbot we want quick replies.

---

## 1. One response

**Demo:** `demo/01_one_response.py`

One call to the API:

```python
client = OpenAI()

response = client.responses.create(
    model="gpt-6-luna",
    reasoning={"effort": "none"},
    instructions=INSTRUCTIONS,
    input="Would you tell me, please, which way I ought to go from here?",
)
print(response.output_text)
```

- `input` is what you say.
- `instructions` tell the model who to be and how to behave. Ours makes it the Cheshire Cat, mischievous but helpful, and keeps it to two or three sentences. Instructions are often called the **system prompt**.
- `output_text` is the reply.

The question is the one Alice asks the Cat in the book. The reply:

> That depends a good deal on where you want to get to. If you don't much care where, then any way will do—but if you have a destination in mind, tell me, and we'll find the path.

The first sentence is Carroll's own, from the book. The model knows its *Alice*.

Open `demo/output/01_response.json` to see the whole **response object**. Among other things it has an `id`, the `model` that answered, the `instructions` we sent, the `output` (a list, because a response can contain more than one item), and `usage`: how many tokens went in and how many came out. You pay for both.

You will also meet the older **Chat Completions API** (`client.chat.completions.create`) in other code and tutorials. It is still supported, but OpenAI recommends the Responses API for new code, and that's what this course uses.

**Why this breaks:** it answers one question, then stops. To ask another, you have to run it again.

## 2. A chat loop

**Demo:** `demo/02_chat_loop.py`

Put the call in a loop:

```python
while True:
    question = input("You: ")
    if not question:
        break
    response = client.responses.create(..., input=question)
    print(f"Cat: {response.output_text}")
```

That's a chatbot. Until you try this:

> **You:** Hello! My name is Nick.
> **Cat:** Hello, Nick! I'd grin and say, "Names are useful things—especially when someone wants to find you again." Shall I call you Nick?
>
> **You:** What is my name?
> **Cat:** I don't know your name—you haven't told me. But names are curious things, aren't they? A cat can vanish without one.

**Why this breaks:** the API is **stateless**. Each call is completely separate, and the model only sees what you send in that call. This is the context window from Module 1 again: the model predicts from the context it is given, and nothing else. It has no memory of its own.

## 3. Memory

**Demo:** `demo/03_conversation.py`

If the model only knows what we send, we send it everything. Keep a list of the conversation and send the whole list every time:

```python
messages.append({"role": "user", "content": question})
response = client.responses.create(..., input=messages)
messages.append({"role": "assistant", "content": response.output_text})
```

Each message has a **role**: `user` for what you said, `assistant` for what the model said. The model reads the whole conversation and predicts what the assistant says next.

> **You:** Hello! My name is Nick.
> **Cat:** Well, hello, Nick! Names are curious things—they tell us what to call you, but not where you're going.
>
> **You:** What is my name?
> **Cat:** Your name is Nick—unless you've wandered into a very convincing disguise.

It remembers. (The API can also store the conversation for you: pass `previous_response_id=response.id` instead of the list. But the model still reads the whole conversation every time, and you still pay for it.)

**Why this breaks:** two things.

- **You wait.** Nothing appears until the whole reply has been written.
- **Every turn costs more.** `demo/output/03_conversation.txt` records the tokens used by each turn:

| Turn | Input tokens | Output tokens |
|------|-------------:|--------------:|
| 1 | 56 | 29 |
| 2 | 96 | 19 |
| 3 | 127 | 34 |

The input grows every turn, because every turn resends everything before it. A long conversation gets slow and expensive, and eventually won't fit in the context window at all. (The `cost-of-memory` playground explores this.)

## 4. Streaming

**Demo:** `demo/04_streaming.py`

Instead of waiting for the finished reply, ask for it as a **stream** of events, and print each piece of text as it arrives:

```python
stream = client.responses.create(..., input=messages, stream=True)
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
```

Now the reply appears a few characters at a time. This is not a special effect. The model really does produce its reply one token at a time, each one predicted from everything before it, exactly like the generation loop in every Module 1 demo. Streaming just lets you watch.

There are other event types too, such as `response.created` and `response.completed`. We only need the text.

**Why this breaks:** it can only read text.

## 5. Images

**Demo:** `demo/05_images.py`

`gpt-6-luna` is **multimodal**: it accepts images as well as text. A message's content can be a list of parts, some text and some images:

```python
image = base64.b64encode(Path("mad-tea-party.png").read_bytes()).decode()
messages = [{
    "role": "user",
    "content": [
        {"type": "input_text", "text": "What is going on in this picture?"},
        {"type": "input_image", "image_url": f"data:image/png;base64,{image}"},
    ],
}]
```

The image is sent inside the request, encoded as text (**base64**). You can also give it the URL of an image on the web.

The demo shows the Cat Tenniel's illustration of the Mad Tea Party, then carries on chatting:

> **You:** What is going on in this picture?
> **Cat:** Alice has stumbled upon the Mad Hatter's tea party: she sits at a crowded table with the Hatter, the March Hare, and the Dormouse. They're surrounded by teacups and a very untidy spread—though whether it's teatime or nonsense time is anyone's guess.
>
> **You:** Who is the one with the big hat?
> **Cat:** That's the Mad Hatter—the one wearing the enormous hat marked "In this style 10/6." A hat that large is hard to mistake, even in Wonderland.

It read the price ticket in the Hatter's hat.

How does a language model see? OpenAI doesn't publish the details, but the usual approach is to cut the image into small square patches and turn each patch into a vector, just like a token's embedding. To the model, the picture becomes more tokens in the context, and you pay for them as input tokens.

---

## Summary

| Step | What we added | What was wrong |
|------|---------------|----------------|
| 1. One response | A single API call, with instructions | One question, then it stops |
| 2. A chat loop | `input()` in a loop | It forgets everything: the API is stateless |
| 3. Memory | Send the whole conversation every time | Slow to reply, and every turn costs more |
| 4. Streaming | Print the reply as it is generated | It can only read text |
| 5. Images | Send pictures as well as text | — |

## Playground

[`playground/`](playground/) has seven things to play with between exercises: a chatbot with every setting exposed, personas, temperature, a model shootout, the cost of memory, a real model's next-token probabilities, and vision. Each comes with ideas for taking it further.

## Further reading and extensions

The final exercise is in [`further-reading/`](further-reading/): papers on how chat models are trained to follow instructions, how they see images, and how they cope with long conversations, plus extension projects to take home.

## Slides

```bash
pnpm slides:02
```
