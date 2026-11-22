# Run from the module folder: uv run python demo/03_word_map.py

import json
import math
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
GUIDE = HERE.parent / "data" / "docs" / "user-guide.md"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

WINDOW = 3
MIN_COUNT = 2
PICKED = [
    "sunrise", "wake", "warm", "early", "heat", "frost", "temperature", "schedule",
    "boiler", "radiator", "router", "app", "phone", "email", "account", "password",
]
GROUPS = 3
STEPS = 1000
WORDS = ["warm", "password"]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cosine_similarity(a, b):
    return dot(a, b) / math.sqrt(dot(a, a) * dot(b, b))


def unit(vector):
    length = math.sqrt(dot(vector, vector))
    return [x / length for x in vector]


def angle(point):
    return math.degrees(math.atan2(point[1], point[0])) % 360


def apart(a, b):
    gap = abs(angle(a) - angle(b))
    return min(gap, 360 - gap)


def count_vectors():
    # Count every word's neighbours, exactly as demo 2 does.
    text = GUIDE.read_text().split("---", 2)[2]
    words = re.findall(r"[a-z0-9]+", text.lower())
    counts = Counter(words)
    vocabulary = sorted(w for w, c in counts.items() if c >= MIN_COUNT)
    index = {w: i for i, w in enumerate(vocabulary)}
    tokens = [index[w] for w in words if w in index]
    vectors = [[0] * len(vocabulary) for _ in vocabulary]
    for i, word in enumerate(tokens):
        for j in range(max(0, i - WINDOW), min(len(tokens), i + WINDOW + 1)):
            if j != i:
                vectors[word][tokens[j]] += 1
    return {w: vectors[i] for w, i in index.items()}


def two_numbers(words, vectors, name):
    # How alike each pair of words is: the cosine similarity of their rows.
    rows = [vectors[w] for w in words]
    similar = [[0 if i == j else cosine_similarity(a, b) for j, b in enumerate(rows)] for i, a in enumerate(rows)]
    pull = [sum(row) for row in similar]

    def halfway(positions):
        # Move each word halfway towards the average position of the others, weighted by how alike they are.
        return [(p + dot(s, positions) / total) / 2 for p, s, total in zip(positions, similar, pull)]

    def centre(positions):
        middle = dot(pull, positions) / sum(pull)
        return [p - middle for p in positions]

    # Two lines this time, started anywhere.
    xs = [float(i) for i in range(len(words))]
    ys = [float(i * i) for i in range(len(words))]
    for step in range(STEPS):
        xs, ys = centre(halfway(xs)), centre(halfway(ys))
        # Keep the second line at right angles to the first, or both would end up the same line.
        overlap = sum(w * x * y for w, x, y in zip(pull, xs, ys)) / sum(w * x * x for w, x in zip(pull, xs))
        ys = [y - overlap * x for x, y in zip(xs, ys)]
        xs, ys = unit(xs), unit(ys)
        print(f"  {name}: round {step + 1} of {STEPS}", end="\r")
    print(" " * 60, end="\r")

    # Warm on the left and password above, every time.
    if xs[words.index("warm")] > 0:
        xs = [-x for x in xs]
    if ys[words.index("password")] < 0:
        ys = [-y for y in ys]
    return {w: [x, y] for w, x, y in zip(words, xs, ys)}


def find_groups(points):
    # Push every word out to the circle: only its direction counts.
    directions = {w: unit(p) for w, p in points.items()}
    # Where k-means starts changes where it settles, so start 12 times and keep the tightest groups.
    best = None
    for start in range(0, 120, 10):
        # Centres evenly spaced round the circle.
        centres = [[math.cos(math.radians(start + 360 * g / GROUPS)), math.sin(math.radians(start + 360 * g / GROUPS))] for g in range(GROUPS)]
        for _ in range(100):
            # Give each word to the centre with the highest cosine similarity: the smallest angle.
            group = {w: max(range(GROUPS), key=lambda g: dot(d, centres[g])) for w, d in directions.items()}
            # Move each centre to the middle of its words.
            for g in range(GROUPS):
                members = [directions[w] for w in group if group[w] == g]
                if members:
                    centres[g] = unit([sum(d[0] for d in members), sum(d[1] for d in members)])
        tightness = sum(dot(directions[w], centres[group[w]]) for w in group)
        if best is None or tightness > best[0]:
            best = (tightness, group, centres)
    _, group, centres = best
    # Number the groups by the direction they point in.
    order = sorted(range(GROUPS), key=lambda g: angle(centres[g]))
    return {w: order.index(g) + 1 for w, g in group.items()}


def written(points, group=None):
    return {
        w: {
            "x": round(p[0], 3),
            "y": round(p[1], 3),
            "length": round(math.hypot(*p), 3),
            "angle": round(angle(p)),
            **({"group": group[w]} if group else {}),
        }
        for w, p in sorted(points.items(), key=lambda item: angle(item[1]))
    }


vectors = count_vectors()

picked = two_numbers(PICKED, vectors, "16 words")
group = find_groups(picked)
print("\n=== 16 words we picked: two numbers each ===")
for g in range(1, GROUPS + 1):
    members = sorted((w for w in picked if group[w] == g), key=lambda w: angle(picked[w]))
    print(f"  group {g}    {', '.join(members)}")
for other in ["wake", "password"]:
    print(f"  warm and {other:<9} {apart(picked['warm'], picked[other]):3.0f}° apart")

everything = two_numbers(sorted(vectors), vectors, "All 235 words")
print(f"\n=== All {len(everything)} words: two numbers each ===")
for word in WORDS:
    closest = sorted((apart(everything[word], p), w) for w, p in everything.items() if w != word)
    print(f"  {word:<10} {', '.join(w for _, w in closest[:5])}")

(OUTPUT / "03_word_map.json").write_text(
    json.dumps({"picked": written(picked, group), "all": written(everything)}, indent=2)
)
