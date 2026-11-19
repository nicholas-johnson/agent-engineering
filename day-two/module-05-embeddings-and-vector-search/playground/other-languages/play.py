# Other languages — search the English library in French, German, Spanish, Polish and Japanese.
# Run from the module folder: uv run python playground/other-languages/play.py
#                         or: source ../../.venv/bin/activate && python playground/other-languages/play.py
#
# To play: add a language or a request to REQUESTS (a language you speak is best),
# or try slang, typos and abbreviations in English. Vectors are cached in output/.

import json
import math
import re
import sqlite3
import struct
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5
K1 = 1.5
B = 0.75

# Four requests, each in six languages. The library itself is all in English.
REQUESTS = [
    {
        "platform": "android",
        "expected": ["TS-1042"],
        "English": "Customers can't sign in after resetting their password",
        "French": "Les clients ne peuvent pas se connecter après avoir réinitialisé leur mot de passe",
        "German": "Kunden können sich nach dem Zurücksetzen ihres Passworts nicht anmelden",
        "Spanish": "Los clientes no pueden iniciar sesión después de restablecer su contraseña",
        "Polish": "Klienci nie mogą się zalogować po zresetowaniu hasła",
        "Japanese": "パスワードをリセットした後、お客様がサインインできません",
    },
    {
        "platform": "ios",
        "expected": ["TS-1558"],
        "English": "The same thermostat shows up twice in the home after adding it again",
        "French": "Le même thermostat apparaît deux fois dans la maison après l'avoir ajouté à nouveau",
        "German": "Derselbe Thermostat erscheint zweimal im Zuhause, nachdem er erneut hinzugefügt wurde",
        "Spanish": "El mismo termostato aparece dos veces en la casa después de volver a añadirlo",
        "Polish": "Ten sam termostat pojawia się dwa razy w domu po ponownym dodaniu",
        "Japanese": "同じサーモスタットをもう一度追加したら、ホームに2回表示される",
    },
    {
        "platform": "device",
        "expected": ["TS-1465"],
        "English": "The thermostat says 21 but the room feels colder. Is its reading accurate?",
        "French": "Le thermostat indique 21, mais la pièce semble plus froide. Sa mesure est-elle exacte ?",
        "German": "Der Thermostat zeigt 21 an, aber der Raum fühlt sich kälter an. Ist seine Messung genau?",
        "Spanish": "El termostato marca 21, pero la habitación se nota más fría. ¿Su lectura es precisa?",
        "Polish": "Termostat pokazuje 21, ale w pokoju wydaje się chłodniej. Czy jego odczyt jest dokładny?",
        "Japanese": "サーモスタットは21度と表示しているが、部屋はもっと寒く感じる。表示は正確か？",
    },
    {
        "platform": "device",
        "expected": ["TS-1026", "TS-1488", "TS-1702", "TS-1769"],
        "English": "E-104 came up while setting up a new thermostat",
        "French": "E-104 s'est affiché pendant l'installation d'un nouveau thermostat",
        "German": "Beim Einrichten eines neuen Thermostats wurde E-104 angezeigt",
        "Spanish": "Apareció E-104 al configurar un termostato nuevo",
        "Polish": "Podczas konfigurowania nowego termostatu pojawił się E-104",
        "Japanese": "新しいサーモスタットの設定中にE-104が表示された",
    },
]
LANGUAGES = ["English", "French", "German", "Spanish", "Polish", "Japanese"]

client = OpenAI()


def script_text(script):
    return " ".join([script["title"], script["preconditions"], *script["steps"], script["expected"]])


def what_it_tests(script):
    return f"{script['title']}. {script['expected']}"


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def embed(texts):
    # Vectors are kept in output/vectors.db by their text, so a rerun only embeds new text.
    cache = sqlite3.connect(OUTPUT / "vectors.db")
    cache.execute("create table if not exists vectors (text text primary key, vector blob)")
    stored = dict(cache.execute("select text, vector from vectors"))
    missing = list(dict.fromkeys(t for t in texts if t not in stored))
    for start in range(0, len(missing), BATCH):
        batch = missing[start : start + BATCH]
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        for text, item in zip(batch, response.data):
            stored[text] = struct.pack(f"{len(item.embedding)}f", *item.embedding)
            cache.execute("insert into vectors values (?, ?)", (text, stored[text]))
        cache.commit()
        print(f"  Embedding: {start + len(batch):,}/{len(missing):,}", end="\r")
    print(" " * 40, end="\r")
    return [struct.unpack(f"{len(stored[t]) // 4}f", stored[t]) for t in texts]


def cosine_similarity(a, b):
    return math.sumprod(a, b) / (math.sqrt(math.sumprod(a, a)) * math.sqrt(math.sumprod(b, b)))


scripts = json.loads((DATA / "test-scripts.json").read_text())
titles = {s["id"]: s["title"] for s in scripts}
documents = [Counter(words(script_text(s))) for s in scripts]
average_length = sum(d.total() for d in documents) / len(documents)
appears_in = Counter(w for d in documents for w in d)


def bm25(request, document):
    score = 0
    for word in set(words(request)):
        if word not in document:
            continue
        rarity = math.log(1 + (len(documents) - appears_in[word] + 0.5) / (appears_in[word] + 0.5))
        count = document[word]
        score += rarity * count * (K1 + 1) / (count + K1 * (1 - B + B * document.total() / average_length))
    return score


def rank_of_right_script(scores, expected):
    # 1 + how many scripts score higher than the best right one. None if it scored nothing at all.
    best = max(scores[id] for id in expected)
    if best <= 0:
        return None
    return 1 + sum(score > best for score in scores.values())


def top_three(scores):
    found = [id for id in sorted(scores, key=scores.get, reverse=True) if scores[id] > 0]
    return [f"{id}  {titles[id]}" for id in found[:3]]


vectors = embed([what_it_tests(s) for s in scripts])

results = []
hits = Counter()
for r in REQUESTS:
    # Search only the request's platform, as the module's search tool does.
    on_platform = [(s, d, v) for s, d, v in zip(scripts, documents, vectors) if s["platform"] == r["platform"]]
    request_vectors = embed([r[language] for language in LANGUAGES])
    print(f"\n{r['English']} ({r['platform']})")
    print(f"  {'':<10}{'keyword':>9}{'vector':>8}")
    for language, request_vector in zip(LANGUAGES, request_vectors):
        keyword_scores = {s["id"]: bm25(r[language], d) for s, d, _ in on_platform}
        vector_scores = {s["id"]: cosine_similarity(request_vector, v) for s, _, v in on_platform}
        keyword = rank_of_right_script(keyword_scores, r["expected"])
        vector = rank_of_right_script(vector_scores, r["expected"])
        hits["keyword"] += keyword is not None and keyword <= TOP
        hits["vector"] += vector is not None and vector <= TOP
        print(f"  {language:<10}{keyword or '-':>9}{vector or '-':>8}")
        results.append(
            {
                "language": language,
                "request": r[language],
                "expected": r["expected"],
                "keyword": {"rank": keyword, "top": top_three(keyword_scores)},
                "vector": {"rank": vector, "top": top_three(vector_scores)},
            }
        )

print(f"\nA right script in the top {TOP}, of {len(results)} searches:")
print(f"  keyword {hits['keyword']}, vector {hits['vector']}")
print("(- means the right script shares no word with the request.)")

(OUTPUT / "ranks.json").write_text(json.dumps({"hits": hits, "searches": results}, indent=2, ensure_ascii=False))
