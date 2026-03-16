import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


def load_dotenv() -> None:
    """Loads simple KEY=VALUE pairs from the project .env file."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


load_dotenv()
os.environ.setdefault("MOVERS_TABLE", "stock-movers-dev")
BACKFILL_TIMEZONE = os.environ.setdefault("BACKFILL_TIMEZONE", "America/Chicago")

from backend.handlers.ingest import handler as ingest_handler


def get_recent_business_days(count: int) -> list[str]:
    """Returns the most recent local business days in YYYY-MM-DD format."""
    dates: list[str] = []
    current = datetime.now(ZoneInfo(BACKFILL_TIMEZONE)).date()

    while len(dates) < count:
        if current.weekday() < 5:
            dates.append(current.strftime("%Y-%m-%d"))
        current -= timedelta(days=1)

    dates.sort()
    return dates


def main() -> None:
    for date_str in get_recent_business_days(8):
        print(f"Backfilling {date_str}")
        result = ingest_handler({"date": date_str}, None)
        print(result)


if __name__ == "__main__":
    main()
