// A slow, subtle 3D backdrop for the stage: the glowing rim of a planet just above the camera
// box, a perspective grid drifting across its surface, and faint stars in the sky above.
// WebGL2. Without it the stage keeps its plain CSS background.

const VERTEX = `#version 300 es
in vec2 corner;
void main() {
  gl_Position = vec4(corner, 0.0, 1.0);
}`;

const FRAGMENT = `#version 300 es
precision highp float;

uniform float time;
out vec4 colour;

const vec2 SIZE = vec2(1080.0, 1920.0);
const float HORIZON = 1120.0;  // top of the planet's rim, just above the camera box
const float RADIUS = 1200.0;
const vec3 TOP = vec3(0.059, 0.090, 0.165);     // the slides' slate-900
const vec3 DEEP = vec3(0.008, 0.024, 0.090);    // slate-950
const vec3 SKY = vec3(0.055, 0.647, 0.914);     // primary
const vec3 VIOLET = vec3(0.753, 0.518, 0.988);  // secondary

float hash(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}

void main() {
  vec2 p = vec2(gl_FragCoord.x, SIZE.y - gl_FragCoord.y);  // pixels from the top left
  vec3 tint = mix(SKY, VIOLET, smoothstep(0.0, SIZE.x, p.x));
  vec2 centre = vec2(SIZE.x / 2.0, HORIZON + RADIUS);
  float d = length(p - centre) - RADIUS;  // distance from the rim, negative inside the planet

  // The grid, worked out everywhere because fwidth needs its neighbours.
  float below = max(p.y - HORIZON, 1.0);
  vec2 g = vec2((p.x - SIZE.x / 2.0) / below * 2.2, 520.0 / below + time * 0.08);
  vec2 a = abs(fract(g - 0.5) - 0.5) / fwidth(g);
  float line = 1.0 - min(min(a.x, a.y), 1.0);

  vec3 c;
  if (d < 0.0) {
    c = mix(DEEP, TOP, 0.35) * 0.8;
    c += tint * 0.2 * line * smoothstep(0.0, 140.0, -d) * smoothstep(0.0, 90.0, below);
    c += tint * 0.18 * exp(d / 50.0);
  } else {
    c = mix(TOP, DEEP, smoothstep(0.0, SIZE.y, p.y));
    c += SKY * 0.16 * smoothstep(850.0, 0.0, length(p - vec2(160.0, 150.0)));
    c += VIOLET * 0.1 * smoothstep(850.0, 0.0, length(p - vec2(970.0, 670.0)));

    vec2 cell = floor(p / 36.0);
    float star = hash(cell);
    if (star > 0.94) {
      vec2 at = (cell + 0.2 + 0.6 * vec2(hash(cell + 7.0), hash(cell + 13.0))) * 36.0;
      float twinkle = 0.5 + 0.5 * sin(time * (0.6 + star) + star * 40.0);
      c += vec3(0.8, 0.85, 1.0) * 0.35 * twinkle * smoothstep(1.6, 0.0, length(p - at));
    }

    float breathe = 0.85 + 0.15 * sin(time * 0.5);
    c += tint * 0.22 * breathe * exp(-d / 120.0);
    c += tint * 0.07 * breathe * exp(-d / 500.0);
  }

  // The rim itself, with a light that travels along it.
  float sweep = exp(-pow((p.x - (mod(time * 90.0, 1800.0) - 360.0)) / 160.0, 2.0));
  c += tint * exp(-abs(d) / 2.5) * (0.6 + 0.9 * sweep);

  c += (hash(p + fract(time)) - 0.5) / 255.0;  // dither, so the gradients don't band
  colour = vec4(c, 1.0);
}`;

function compile(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(shader));
  return shader;
}

function startBackdrop() {
  const canvas = document.createElement("canvas");
  canvas.className = "backdrop";
  canvas.width = 1080;
  canvas.height = 1920;
  const gl = canvas.getContext("webgl2");
  if (!gl) return;

  const program = gl.createProgram();
  gl.attachShader(program, compile(gl, gl.VERTEX_SHADER, VERTEX));
  gl.attachShader(program, compile(gl, gl.FRAGMENT_SHADER, FRAGMENT));
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
  gl.useProgram(program);

  // One triangle that covers the whole canvas.
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const corner = gl.getAttribLocation(program, "corner");
  gl.enableVertexAttribArray(corner);
  gl.vertexAttribPointer(corner, 2, gl.FLOAT, false, 0, 0);
  const time = gl.getUniformLocation(program, "time");

  document.querySelector(".stage").prepend(canvas);

  function draw(ms) {
    gl.uniform1f(time, ms / 1000);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);
}

try {
  startBackdrop();
} catch (error) {
  console.error("Backdrop off:", error.message);
}
