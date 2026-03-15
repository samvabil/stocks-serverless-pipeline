import os
import time
import requests

BASE_URL = "https://api.massive.com" 
API_KEY = os.environ["STOCK_API_KEY"]

def get_daily_open_close(ticker: str, date_str: str, max_retries: int = 2) -> dict:
    """
    Fetch daily open/close data for a ticker on specified date from Massive
    Docs endpoint: GET /v1/open-close/{ticker}/{date}
    """
    url = f"{BASE_URL}/v1/open-close/{ticker}/{date_str}"
    params = {"apiKey": API_KEY}

    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 429:
                last_error = f"Rate limited with status 429 on attempt {attempt}"
                time.sleep(attempt)
                continue

            response.raise_for_status()
            data = response.json()

            if data.get("status") != "OK":
                last_error = f"Massive returned non-OK status: {data}"
                raise ValueError(f"Massive returned non-OK status for {ticker}: {data}")

            if "open" not in data or "close" not in data:
                last_error = f"Missing open/close data: {data}"
                raise ValueError(f"Missing open/close for {ticker} on {date_str}: {data}")

            return {
                "ticker": data.get("symbol", ticker),
                "date": data.get("from", date_str),
                "open": float(data["open"]),
                "close": float(data["close"]),
            }

        except requests.RequestException as exc:
            last_error = str(exc)
            if attempt < max_retries:
                time.sleep(attempt)
                continue
            raise

        except Exception as exc:
            last_error = str(exc)
            raise

    raise RuntimeError(f"Failed to fetch {ticker} for {date_str}: {last_error}")