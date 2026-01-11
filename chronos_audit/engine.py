from sentence_transformers import CrossEncoder
from langchain_google_genai import ChatGoogleGenerativeAI

from chronos_audit.config import CONFIG
from chronos_audit.ingestion import load_local_books
from chronos_audit.indexing import build_indices
from chronos_audit.temporal import extract_time_scope
from chronos_audit.retrieval import retrieve_documents
from chronos_audit.judge import run_tabula_rasa_judge
from chronos_audit.utils import normalize_book_name


class ChronosAuditEngine:
    def __init__(self):
        print("[ENGINE] Initializing judge model...", flush=True)
        self.judge = ChatGoogleGenerativeAI(
            model=CONFIG["JUDGE_MODEL"],
            temperature=0
        )

        print("[ENGINE] Initializing reranker...", flush=True)
        self.reranker = CrossEncoder(CONFIG["RERANK_MODEL"])

        print("[ENGINE] Loading local books...", flush=True)
        books = load_local_books()
        print(f"[ENGINE] Loaded {len(books)} books", flush=True)

        print("[ENGINE] Building indices (this can take time)...", flush=True)
        self.indices = build_indices(books)
        print("[ENGINE] Indices built successfully", flush=True)

    def process_claim(
        self,
        claim: str,
        book_name: str,
        character: str,
        caption: str = "",
        row_id=None
    ):
        # ---------- Progress marker ----------
        if row_id is not None:
            print(f"[ENGINE] Processing claim ID={row_id}", flush=True)

        # ---------- Book routing ----------
        target = normalize_book_name(book_name)
        matched_book = next(
            (b for b in self.indices if target in normalize_book_name(b)),
            None
        )

        if not matched_book:
            return {
                "pred": 1,
                "rationale": "Book not found in index",
                "dossier": []
            }

        # ---------- Temporal scope ----------
        print("[ENGINE] Calling Gemini (temporal scope)...", flush=True)
        try:
            time_scope = extract_time_scope(claim, self.judge)
        except Exception as e:
            return {
                "pred": 1,
                "rationale": f"Temporal extraction failed: {str(e)}",
                "dossier": []
            }

        # ---------- Retrieval ----------
        query = f"{character} {time_scope} {caption} {claim}"
        docs = retrieve_documents(self.indices[matched_book], query)

        if not docs:
            return {
                "pred": 1,
                "rationale": "Silence is consistent",
                "dossier": []
            }

        # ---------- Reranking ----------
        pairs = [[query, d.page_content] for d in docs]
        scores = self.reranker.predict(pairs)

        top_docs = [
            d for d, _ in sorted(
                zip(docs, scores),
                key=lambda x: x[1],
                reverse=True
            )[:15]
        ]

        evidence = "\n---\n".join(d.page_content for d in top_docs)

        # ---------- Judge ----------
        print("[ENGINE] Calling Gemini (tabula-rasa judge)...", flush=True)
        result = run_tabula_rasa_judge(
            self.judge,
            claim,
            character,
            time_scope,
            evidence
        )

        # ---------- Grounding safeguard ----------
        if result["verdict"] == 0 and not result.get("dossier"):
            return {
                "pred": 1,
                "rationale": "No grounded contradiction",
                "dossier": []
            }

        return {
            "pred": result["verdict"],
            "rationale": result["rationale"],
            "dossier": result.get("dossier", [])
        }
