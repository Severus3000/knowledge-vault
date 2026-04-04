import os
from pathlib import Path

VAULT_PATH = Path(os.environ.get("VAULT_PATH", "./vault")).resolve()
RAW_DIR = VAULT_PATH / "raw"
WIKI_DIR = VAULT_PATH / "wiki"
OUTPUTS_DIR = VAULT_PATH / "outputs"
ASSETS_DIR = RAW_DIR / "assets"
INDEX_FILE = WIKI_DIR / "_index.md"
GRAPH_FILE = WIKI_DIR / "_graph.json"
COMPILED_FILE = WIKI_DIR / "_compiled.json"
