import json
import subprocess
import sys
import time
from datetime import datetime, timedelta


def get_last_business_days(reference_date: str | None = None, count: int = 7) -> list[str]:
    """
    Returns the last `count` business days before the reference date.
    Excludes the reference date itself.
    """
    if reference_date:
        start = datetime.strptime(reference_date, "%Y-%m-%d").date()
    else:
        start = datetime.today().date()

    results = []
    current = start - timedelta(days=1)

    while len(results) < count:
        if current.weekday() < 5:  # Monday=0, Friday=4
            results.append(current.strftime("%Y-%m-%d"))
        current -= timedelta(days=1)

    return results


def invoke_ingest(stage: str, date_str: str) -> None:
    payload = json.dumps({"date": date_str})

    cmd = [
        "serverless",
        "invoke",
        "-f",
        "ingest",
        "--stage",
        stage,
        "--data",
        payload,
    ]

    print(f"\nInvoking ingest for {date_str}...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        raise RuntimeError(f"Invoke failed for {date_str}")


def main():
    """
    Usage:
      python3 scripts/backfill.py
      python3 scripts/backfill.py 2026-03-16
      python3 scripts/backfill.py 2026-03-16 dev
      python3 scripts/backfill.py 2026-03-16 dev 65
    """
    reference_date = sys.argv[1] if len(sys.argv) > 1 else None
    stage = sys.argv[2] if len(sys.argv) > 2 else "dev"
    pause_seconds = int(sys.argv[3]) if len(sys.argv) > 3 else 65

    if reference_date:
        try:
            datetime.strptime(reference_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("reference date must be in YYYY-MM-DD format")

    dates = get_last_business_days(reference_date=reference_date, count=7)

    print("Backfilling these dates:")
    for d in dates:
        print(f"  - {d}")

    for index, d in enumerate(dates):
        invoke_ingest(stage=stage, date_str=d)

        if index < len(dates) - 1:
            print(f"\nWaiting {pause_seconds} seconds to stay within rate limits...")
            time.sleep(pause_seconds)

    print("\nBackfill complete.")


if __name__ == "__main__":
    main()