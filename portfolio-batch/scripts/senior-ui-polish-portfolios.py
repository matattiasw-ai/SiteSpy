from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATOR_PATH = ROOT / "portfolio-batch" / "scripts" / "rebuild-beautiful-portfolios.py"
REPORT_PATH = ROOT / "portfolio-batch" / "senior-ui-polish-report.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("sitespy_portfolio_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load generator at {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    generator = load_generator()
    active_items = generator.active_items()
    assignments = generator.ASSIGNMENTS

    missing = [item["studentName"] for item in active_items if item["studentName"] not in assignments]
    if missing:
        raise RuntimeError(f"Missing portfolio assignment(s): {', '.join(missing)}")

    layout_ids = [assignments[item["studentName"]][0] for item in active_items]
    distinct_layouts = sorted(set(layout_ids))
    if len(active_items) != 17:
        raise RuntimeError(f"Expected 17 active portfolios, found {len(active_items)}")
    if len(distinct_layouts) < 14:
        raise RuntimeError(f"Expected at least 14 distinct layout families, found {len(distinct_layouts)}")

    print("[senior-ui] Reference benchmark: D:\\Documents\\Jobs\\Morning\\Programming\\FletPortfolio")
    print("[senior-ui] Generating static GitHub Pages portfolios under each site/ folder")
    generator.main()

    rows = []
    for item in active_items:
        assignment = assignments[item["studentName"]]
        rows.append(
            {
                "studentName": item["studentName"],
                "githubUsername": item["githubUsername"],
                "repoName": item["repoName"],
                "layoutFamily": assignment[0],
                "role": assignment[1],
                "sitePath": str((Path(item["portfolioPath"]) / "site").relative_to(ROOT)),
            }
        )

    REPORT_PATH.write_text(
        json.dumps(
            {
                "portfoliosProcessed": len(rows),
                "distinctLayoutFamilies": len(distinct_layouts),
                "referencePortfolio": "D:/Documents/Jobs/Morning/Programming/FletPortfolio",
                "specialAttention": {
                    "Washington Matattias": "Redesigned as GitHub contribution profile",
                    "Tjatindi Michael Kazundire": "Redesigned as modern SaaS product portfolio",
                },
                "rows": rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[senior-ui] Wrote {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
