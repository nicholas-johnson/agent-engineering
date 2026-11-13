// Plays a clip: steps through its frames, puts your camera on the stage, captions what you
// say, and records the stage with your voice.
//
// Keys: Space, →, Page Down or Enter: next. ←, Page Up or Backspace: back. Home: start again.
//       R: start or stop recording. C: next camera. F: full screen.
//
// Inside a frame:
//   data-camera="full"  the camera fills the stage on this frame
//   <p class="cue">     what to say, one per step, in order. It is your autocue and the
//                       viewer's caption. A frame has at least as many steps as it has cues.
//   data-in="n"         appears at step n (0: as the frame arrives)
//   data-out="n"        disappears at step n
//   data-at="n"         gets the class "reached" at step n (for effects such as the red digits)
//   class="type"        types itself out, one character at a time (monospace text only)
//   class="stream"      appears word by word, like a streamed reply

const KEYWORDS = new Set([
  "and", "as", "async", "await", "class", "def", "elif", "else", "for", "from",
  "if", "import", "in", "is", "lambda", "not", "or", "pass", "return", "while",
  "with", "None", "True", "False",
]);
const BUILTINS = new Set(["bool", "dict", "float", "int", "list", "print", "str"]);
const TOKEN = /(#.*)|("""|"[^"]*"|'[^']*')|(@[\w.]+)|([A-Za-z_]\w*)|(\d[\d_.]*)/g;

const NEXT = [" ", "ArrowRight", "ArrowDown", "PageDown", "Enter"];
const BACK = ["ArrowLeft", "ArrowUp", "PageUp", "Backspace"];
const CAMERA = { width: { ideal: 1920 }, height: { ideal: 1080 }, frameRate: { ideal: 30 } };
const RECORDING_TYPES = [
  "video/mp4;codecs=avc1.640033,mp4a.40.2",
  "video/mp4;codecs=avc1,mp4a.40.2",
  "video/mp4",
  "video/webm;codecs=vp9,opus",
  "video/webm",
];

function escape(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function span(kind, text) {
  return `<span class="${kind}">${escape(text)}</span>`;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Colour one line of Python, remembering whether we are inside a """docstring""".
function highlightLine(line, state) {
  let out = "";
  let start = 0;
  if (state.inDocstring) {
    const end = line.indexOf('"""');
    if (end === -1) return span("str", line);
    state.inDocstring = false;
    out += span("str", line.slice(0, end + 3));
    start = end + 3;
  }

  TOKEN.lastIndex = start;
  let last = start;
  let match;
  while ((match = TOKEN.exec(line))) {
    const [token, comment, string, decorator, name, number] = match;
    out += escape(line.slice(last, match.index));
    if (comment) out += span("comment", token);
    else if (string === '"""') {
      const end = line.indexOf('"""', TOKEN.lastIndex);
      if (end === -1) {
        state.inDocstring = true;
        return out + span("str", line.slice(match.index));
      }
      out += span("str", line.slice(match.index, end + 3));
      TOKEN.lastIndex = end + 3;
    } else if (string) out += span("str", token);
    else if (decorator) out += span("deco", token);
    else if (name && KEYWORDS.has(name)) out += span("kw", token);
    else if (name && BUILTINS.has(name)) out += span("builtin", token);
    else if (name && line[TOKEN.lastIndex] === "(") out += span("fn", token);
    else if (number) out += span("num", token);
    else out += escape(token);
    last = TOKEN.lastIndex;
  }
  return out + escape(line.slice(last));
}

// Code: lines starting "+ " (or a lone "+") are added lines.
for (const code of document.querySelectorAll(".code")) {
  const lines = code.textContent.replace(/^\n+|\s+$/g, "").split("\n");
  const state = { inDocstring: false };
  code.innerHTML = lines
    .map((line) => {
      const added = line === "+" || line.startsWith("+ ");
      const text = added ? line.slice(2) : line;
      const classes = ["line", added && "added", !text.trim() && "blank"].filter(Boolean).join(" ");
      return `<span class="${classes}">${highlightLine(text, state) || " "}</span>`;
    })
    .join("");
}

// Answers: wrap the digits where each one stops matching the right answer.
for (const answers of document.querySelectorAll(".answers")) {
  const right = answers.querySelector(".right .number").textContent;
  for (const number of answers.querySelectorAll(".answer:not(.right) .number")) {
    const text = number.textContent;
    let same = 0;
    while (same < text.length && text[same] === right[same]) same++;
    number.innerHTML = `${escape(text.slice(0, same))}<span class="drift">${escape(text.slice(same))}</span>`;
  }
}

for (const element of document.querySelectorAll(".type")) {
  element.style.setProperty("--chars", element.textContent.length);
  element.innerHTML = `<span class="typed">${element.innerHTML}</span>`;
}

for (const element of document.querySelectorAll(".stream")) {
  element.innerHTML = element.textContent
    .split(" ")
    .map((word, i) => `<span class="word" style="--i: ${i}">${escape(word)}</span>`)
    .join(" ");
}

// Frames, steps and captions

const root = document.documentElement;
const stage = document.querySelector(".stage");
const frames = [...stage.querySelectorAll(".frame")];

// Each frame's cues, one per step, moved out of the frame into the caption.
const cues = frames.map((frame) => {
  const found = [...frame.querySelectorAll(".cue")];
  for (const cue of found) cue.remove();
  return found.map((cue) => cue.innerHTML);
});

const lastStep = frames.map((frame, f) =>
  Math.max(
    cues[f].length - 1,
    ...[...frame.querySelectorAll("[data-in], [data-out], [data-at]")].flatMap((element) =>
      [element.dataset.in, element.dataset.out, element.dataset.at].filter(Boolean).map(Number),
    ),
  ),
);

const caption = document.createElement("p");
caption.className = "caption";
stage.append(caption);

// Outside the stage, so it is never recorded.
const statusLine = document.createElement("aside");
statusLine.className = "status";
document.body.append(statusLine);

let current = 0;
let step = 0;

function show() {
  frames.forEach((frame, i) => {
    frame.classList.toggle("current", i === current);
    frame.classList.toggle("past", i < current);
    const at = i < current ? lastStep[i] : i === current ? step : -1;
    for (const element of frame.querySelectorAll("[data-in]")) element.classList.toggle("shown", at >= element.dataset.in);
    for (const element of frame.querySelectorAll("[data-out]")) element.classList.toggle("gone", at >= element.dataset.out);
    for (const element of frame.querySelectorAll("[data-at]")) element.classList.toggle("reached", at >= element.dataset.at);
  });
  stage.classList.toggle("camera-full", frames[current].dataset.camera === "full");

  const words = cues[current][step] ?? "";
  if (caption.innerHTML !== words) {
    caption.innerHTML = words;
    caption.animate(
      [
        { opacity: 0, transform: "translate(-50%, 12px)" },
        { opacity: 1, transform: "translate(-50%, 0)" },
      ],
      { duration: 200, easing: "ease-out" },
    );
  }
  caption.hidden = !words;
  history.replaceState(null, "", `#${current + 1}.${step}`);
}

function next() {
  if (step < lastStep[current]) step++;
  else if (current < frames.length - 1) {
    current++;
    step = 0;
  }
}

function back() {
  if (step > 0) step--;
  else if (current > 0) {
    current--;
    step = lastStep[current];
  }
}

// The stage is always 1080×1920, scaled to fit the window. The status goes in the space beside it.
function fit() {
  const scale = Math.min(innerHeight / 1920, innerWidth / 1080);
  root.style.setProperty("--scale", scale);
  root.classList.toggle("narrow", (innerWidth - 1080 * scale) / 2 < 240);
}

// Camera and microphone

const cameraBox = document.createElement("div");
cameraBox.className = "camera";
cameraBox.innerHTML = "<video muted playsinline autoplay></video><span>Camera</span>";
stage.append(cameraBox);
const video = cameraBox.querySelector("video");

let mic = null;
let cameraName = "";
let micName = "";
let note = "";

function useCamera(stream) {
  video.srcObject?.getTracks().forEach((track) => track.stop());
  video.srcObject = stream;
  cameraName = stream.getVideoTracks()[0].label;
  stage.classList.add("has-camera");
  renderStatus();
}

async function startMedia() {
  if (!navigator.mediaDevices) {
    note = "Open this page with pnpm social to use the camera and record.";
    renderStatus();
    return;
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: CAMERA, audio: { echoCancellation: false } });
    mic = new MediaStream(stream.getAudioTracks());
    micName = mic.getAudioTracks()[0]?.label ?? "";
    useCamera(new MediaStream(stream.getVideoTracks()));
  } catch (error) {
    note = `No camera or microphone: ${error.message}`;
    renderStatus();
  }
}

async function nextCamera() {
  const cameras = (await navigator.mediaDevices.enumerateDevices()).filter((device) => device.kind === "videoinput");
  if (cameras.length < 2) return;
  const now = video.srcObject?.getVideoTracks()[0].getSettings().deviceId;
  const chosen = cameras[(cameras.findIndex((camera) => camera.deviceId === now) + 1) % cameras.length];
  useCamera(await navigator.mediaDevices.getUserMedia({ video: { ...CAMERA, deviceId: { exact: chosen.deviceId } } }));
}

// Recording: capture this tab, cropped to the stage, plus the microphone.

let tab = null;
let recorder = null;
let countdown = 0;
let startedAt = 0;

async function captureStage() {
  if (tab?.active) return;
  tab = await navigator.mediaDevices.getDisplayMedia({
    video: { frameRate: 30, width: { ideal: 4096 }, height: { ideal: 4096 } },
    audio: false,
    preferCurrentTab: true,
    selfBrowserSurface: "include",
    surfaceSwitching: "exclude",
  });
  const [track] = tab.getVideoTracks();
  if (!track.cropTo) {
    tab.getTracks().forEach((t) => t.stop());
    tab = null;
    throw new Error("choose “This tab” when Chrome asks what to share.");
  }
  track.addEventListener("ended", () => recorder?.stop());
  await track.cropTo(await CropTarget.fromElement(stage));
}

async function record() {
  if (recorder) {
    recorder.stop();
    return;
  }
  if (countdown) return;
  try {
    await captureStage();
  } catch (error) {
    note = `Not recording: ${error.message}`;
    renderStatus();
    return;
  }

  current = step = 0;
  show();
  for (countdown = 3; countdown > 0; countdown--) {
    renderStatus();
    await sleep(1000);
  }

  const type = RECORDING_TYPES.find((candidate) => MediaRecorder.isTypeSupported(candidate));
  const tracks = [...tab.getVideoTracks(), ...(mic?.getAudioTracks() ?? [])];
  const chunks = [];
  recorder = new MediaRecorder(new MediaStream(tracks), { mimeType: type, videoBitsPerSecond: 16_000_000 });
  recorder.addEventListener("dataavailable", (event) => chunks.push(event.data));
  recorder.addEventListener("stop", () => {
    save(new Blob(chunks, { type }), type);
    recorder = null;
    renderStatus();
  });
  recorder.start(1000);
  startedAt = Date.now();
  note = "";
  renderStatus();
}

function save(blob, type) {
  const time = new Date().toTimeString().slice(0, 8).replace(/:/g, "-");
  const name = `${document.body.dataset.clip}-${time}.${type.includes("mp4") ? "mp4" : "webm"}`;
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = name;
  link.click();
  setTimeout(() => URL.revokeObjectURL(link.href), 60_000);
  note = `Saved ${name} to Downloads.`;
}

function clock(ms) {
  const seconds = Math.floor(ms / 1000);
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
}

function renderStatus() {
  const state = countdown
    ? `<strong class="rec">Recording in ${countdown}…</strong>`
    : recorder
      ? `<strong class="rec">● Recording ${clock(Date.now() - startedAt)}</strong> · R to stop`
      : "<strong>R to record</strong>";
  const devices = [cameraName, micName].filter(Boolean).map(escape).join(" · ") || "No camera yet";
  const keys = "Space next · ← back · Home start<br />R record · C camera · F full screen";
  statusLine.innerHTML = [state, devices, note && escape(note), keys].filter(Boolean).join("<br />");
}

setInterval(() => recorder && renderStatus(), 250);

// Keys

document.addEventListener("keydown", (event) => {
  if (event.repeat || event.metaKey || event.ctrlKey) return;
  const key = event.key.length === 1 ? event.key.toLowerCase() : event.key;
  if (NEXT.includes(key)) next();
  else if (BACK.includes(key)) back();
  else if (key === "Home") current = step = 0;
  else if (key === "r") record();
  else if (key === "c") nextCamera();
  else if (key === "f") root.requestFullscreen();
  else return;
  event.preventDefault();
  show();
});

stage.addEventListener("click", () => {
  next();
  show();
});

addEventListener("resize", fit);
fit();

// Reloading keeps your place: the address ends #frame.step
const [frame, at] = location.hash.slice(1).split(".").map(Number);
if (frame >= 1 && frame <= frames.length) {
  current = frame - 1;
  step = Math.min(at || 0, lastStep[current]);
}
show();
renderStatus();
startMedia();
