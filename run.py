import json
import pandas as pd
from pathlib import Path
from chronos_audit.engine import ChronosAuditEngine

def main():
    print("[RUN] Initializing Chronos-Audit engine...")
    engine = ChronosAuditEngine()

    ROOT = Path(__file__).resolve().parent
    input_csv = ROOT / "processed_test.csv"
    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)

    print("[RUN] Loading test data...")
    df = pd.read_csv(input_csv)

    results = []
    dossiers = []

    print(f"[RUN] Processing {len(df)} claims...")
    for _, row in df.iterrows():
        result = engine.process_claim(
            claim=row["content"],
            book_name=row["book_name"],
            character=str(row["char"]),
            caption=str(row.get("caption", "")),
            row_id=row["id"]
        )

        # === REQUIRED RESULTS FILE ===
        results.append({
            "Story ID": row["id"],
            "Prediction": result["pred"]
        })

        # === OPTIONAL BUT STRONGLY VALUED DOSSIER ===
        dossiers.append({
            "story_id": row["id"],
            "primary_claim": row["content"],
            "consistency_label": result["pred"],
            "evidence_rationale": result["dossier"]
        })

    # Save results.csv (REQUIRED)
    results_path = output_dir / "results.csv"
    pd.DataFrame(results).to_csv(results_path, index=False)

    # Save forensic dossier (OPTIONAL / Track A)
    dossier_path = output_dir / "forensic_dossier.jsonl"
    with open(dossier_path, "w", encoding="utf-8") as f:
        for d in dossiers:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print("[RUN] DONE")
    print(f"✔ results.csv → {results_path}")
    print(f"✔ forensic_dossier.jsonl → {dossier_path}")

if __name__ == "__main__":
    main()
