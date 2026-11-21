# Copies Module 6's Dormouse documentation into data/docs/: all 275 documents, for customers and for staff.
# Run from the module folder: uv run python data/copy_docs.py

import shutil
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE.parents[1] / "module-06-rag-and-proprietary-knowledge" / "data" / "docs"
DOCS = HERE / "docs"

shutil.rmtree(DOCS, ignore_errors=True)
shutil.copytree(SOURCE, DOCS)
print(f"Copied {len(list(DOCS.glob('*.md')))} documents to data/docs/")
