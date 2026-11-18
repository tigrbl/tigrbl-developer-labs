from pathlib import Path
import httpx, json, time

root = Path(__file__).parent
results = []
with httpx.Client(
    base_url="http://127.0.0.1:8782", timeout=20
) as c:
    for n in range(1, 25):
        r = c.post(f"/lab/run/{n}")
        data = r.json()
        results.append(
            {
                "lesson": n,
                "status": r.status_code,
                "passed": data.get("passed", False),
                "error": data.get("error"),
                "assertions": len(data.get("checks", [])),
            }
        )
        print(
            n,
            r.status_code,
            data.get("passed"),
            data.get("error", ""),
            flush=True,
        )
(root / "verification.json").write_text(
    json.dumps(
        {
            "results": results,
            "passed": sum(r["passed"] for r in results),
            "total": 24,
            "verified_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        },
        indent=2,
    ),
    "utf-8",
)
assert all(r["passed"] for r in results), (
    "Some labs failed; inspect evidence/*-failure.json"
)
