# Other languages — search the English documentation in French, German, Spanish, Polish and Japanese.
# Run from the module folder: uv run python playground/other-languages/play.py
#                         or: source ../../.venv/bin/activate && python playground/other-languages/play.py
#
# To play: add a language or a question to QUESTIONS (a language you speak is best),
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
DOCS = HERE.parent.parent / "data" / "docs"
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

EMBEDDING_MODEL = "text-embedding-3-small"
BATCH = 100
TOP = 5
K1 = 1.5
B = 0.75

# Four questions from data/questions.json, each in six languages. The documentation is all in English.
QUESTIONS = [
    {
        "expected": ["understand-warm-wake", "thermostat-shows-the-sunrise-symbol"],
        "English": "Why is the heating already on before my alarm goes off?",
        "French": "Pourquoi le chauffage est-il déjà allumé avant que mon réveil sonne ?",
        "German": "Warum ist die Heizung schon an, bevor mein Wecker klingelt?",
        "Spanish": "¿Por qué la calefacción ya está encendida antes de que suene mi despertador?",
        "Polish": "Dlaczego ogrzewanie jest już włączone, zanim zadzwoni mój budzik?",
        "Japanese": "目覚ましが鳴る前なのに、なぜもう暖房がついているのですか？",
    },
    {
        "expected": [
            "reset-your-dormouse-account-password",
            "use-a-password-reset-link",
            "sign-in-to-the-dormouse-app-and-web-dashboard",
            "android-app-sign-in-screen-guide",
            "ios-app-sign-in-screen-guide",
            "web-dashboard-sign-in-screen-guide",
        ],
        "English": "I forgot my password and can't get into the app",
        "French": "J'ai oublié mon mot de passe et je n'arrive plus à accéder à l'appli",
        "German": "Ich habe mein Passwort vergessen und komme nicht mehr in die App",
        "Spanish": "He olvidado mi contraseña y no puedo entrar en la app",
        "Polish": "Zapomniałem hasła i nie mogę wejść do aplikacji",
        "Japanese": "パスワードを忘れてしまって、アプリにログインできません",
    },
    {
        "expected": [
            "thermostat-shows-the-wrong-room-temperature",
            "understand-thermostat-temperature-accuracy",
            "thermostat-placement-and-room-temperature-sensing",
        ],
        "English": "It says 21 degrees but the room feels freezing",
        "French": "Il affiche 21 degrés, mais on gèle dans la pièce",
        "German": "Da steht 21 Grad, aber im Zimmer ist es eiskalt",
        "Spanish": "Marca 21 grados, pero la habitación está helada",
        "Polish": "Pokazuje 21 stopni, a w pokoju jest lodowato",
        "Japanese": "21度と表示されているのに、部屋がすごく寒いです",
    },
    {
        "expected": ["connect-dormouse-to-a-voice-assistant"],
        "English": "Can I ask Alexa to turn the heating up?",
        "French": "Est-ce que je peux demander à Alexa de monter le chauffage ?",
        "German": "Kann ich Alexa bitten, die Heizung höher zu stellen?",
        "Spanish": "¿Puedo pedirle a Alexa que suba la calefacción?",
        "Polish": "Czy mogę poprosić Alexę, żeby podkręciła ogrzewanie?",
        "Japanese": "Alexaに暖房の温度を上げるように頼めますか？",
    },
]
LANGUAGES = ["English", "French", "German", "Spanish", "Polish", "Japanese"]

client = OpenAI()


def read_documents():
    documents = []
    for path in sorted(DOCS.glob("*.md")):
        _, header, text = path.read_text().split("---", 2)
        title = re.search(r"^title: (.+)$", header, re.MULTILINE)[1]
        documents.append({"id": path.stem, "title": title, "text": text.strip()})
    return documents


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


documents = read_documents()
titles = {d["id"]: d["title"] for d in documents}
word_counts = [Counter(words(d["text"])) for d in documents]
average_length = sum(c.total() for c in word_counts) / len(word_counts)
appears_in = Counter(w for c in word_counts for w in c)


def bm25(question, counts):
    score = 0
    for word in set(words(question)):
        if word not in counts:
            continue
        rarity = math.log(1 + (len(documents) - appears_in[word] + 0.5) / (appears_in[word] + 0.5))
        count = counts[word]
        score += rarity * count * (K1 + 1) / (count + K1 * (1 - B + B * counts.total() / average_length))
    return score


def rank_of_right_document(scores, expected):
    # 1 + how many documents score higher than the best right one. None if it scored nothing at all.
    best = max(scores[id] for id in expected)
    if best <= 0:
        return None
    return 1 + sum(score > best for score in scores.values())


def top_three(scores):
    found = [id for id in sorted(scores, key=scores.get, reverse=True) if scores[id] > 0]
    return [titles[id] for id in found[:3]]


vectors = embed([d["text"] for d in documents])

results = []
hits = Counter()
for q in QUESTIONS:
    question_vectors = embed([q[language] for language in LANGUAGES])
    print(f"\n{q['English']}")
    print(f"  {'':<10}{'keyword':>9}{'vector':>8}")
    for language, question_vector in zip(LANGUAGES, question_vectors):
        keyword_scores = {d["id"]: bm25(q[language], c) for d, c in zip(documents, word_counts)}
        vector_scores = {d["id"]: cosine_similarity(question_vector, v) for d, v in zip(documents, vectors)}
        keyword = rank_of_right_document(keyword_scores, q["expected"])
        vector = rank_of_right_document(vector_scores, q["expected"])
        hits["keyword"] += keyword is not None and keyword <= TOP
        hits["vector"] += vector is not None and vector <= TOP
        print(f"  {language:<10}{keyword or '-':>9}{vector or '-':>8}")
        results.append(
            {
                "language": language,
                "question": q[language],
                "expected": q["expected"],
                "keyword": {"rank": keyword, "top": top_three(keyword_scores)},
                "vector": {"rank": vector, "top": top_three(vector_scores)},
            }
        )

print(f"\nA right document in the top {TOP}, of {len(results)} searches:")
print(f"  keyword {hits['keyword']}, vector {hits['vector']}")
print("(- means no right document shares a word with the question.)")

(OUTPUT / "ranks.json").write_text(json.dumps({"hits": hits, "searches": results}, indent=2, ensure_ascii=False))
