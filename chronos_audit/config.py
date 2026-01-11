from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]

CONFIG = {
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),

    # DATA LOCATIONS (MATCH YOUR ACTUAL FILES)
    "PROCESSED_DATA_DIR": ROOT_DIR,   # <-- important
    "OUTPUT_DIR": ROOT_DIR / "outputs",

    # MODELS
    "JUDGE_MODEL": "gemini-2.5-flash",
    "EMBED_MODEL": "all-MiniLM-L6-v2",
    "RERANK_MODEL": "cross-encoder/ms-marco-MiniLM-L-6-v2",

    # CHUNKING
    "CHUNK_SIZE": 1200,
    "CHUNK_OVERLAP": 200,
}
