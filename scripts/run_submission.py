import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import json
import pandas as pd
from chronos_audit.engine import ChronosAuditEngine
from chronos_audit.config import CONFIG

def main():
    engine = ChronosAuditEngine()

    input_csv = CONFIG["PROCESSED_DATA_DIR"] / "processed_test.csv"
    output_dir = CONFIG["OUTPUT_DIR"]
    output_dir.mkdir(exist_ok=True)

    df = pd.read_csv(input_csv)
    submissions, dossiers = [], []

    for _, row in df.iterrows():
        result = engine.process_claim(
            claim=row["content"],
            book_name=row["book_name"],
            character=str(row["char"]),
            caption=str(row.get("caption", "")),
            row_id=row["id"]
        )

        submissions.append({
            "Story ID": row["id"],
            "Prediction": result["pred"],
            "Rationale": result["rationale"]
        })

        dossiers.append({
            "story_id": row["id"],
            "claim": row["content"],
            "prediction": result["pred"],
            "evidence_rationale": result["dossier"]
        })

    pd.DataFrame(submissions).to_csv(output_dir / "submission.csv", index=False)
    with open(output_dir / "forensic_dossier.jsonl", "w") as f:
        for d in dossiers:
            f.write(json.dumps(d) + "\n")

if __name__ == "__main__":
    main()
