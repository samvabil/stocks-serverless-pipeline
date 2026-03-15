import json
from datetime import datetime, timezone

from backend.services.stock_api import get_daily_open_close
from backend.services.mover_logic import calculate_percent_change, pick_top_mover
from backend.services.db import save_winner

WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]

def get_target_date(event: dict) -> str:
    """
    Allows manual testing/backfilling
        serverless invoke -f ingest --data '{"date":"YYYY-MM-DD"}'
    Otherwise, defaults to today's date 
    """
    if event and event.get("date"):
        return event["date"]

    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def handler(event, context):
    try:
        target_date = get_target_date(event or {})
        stock_results = []

        for ticker in WATCHLIST:
            try:
                data = get_daily_open_close(ticker, target_date)

                percent_change = calculate_percent_change(
                    data["open"],
                    data["close"]
                )

                stock_results.append({
                    "date": target_date,
                    "ticker": data["ticker"],
                    "percentChange": round(percent_change, 2),
                    "closingPrice": round(data["close"], 2)
                })

            except Exception as ticker_error:
                print(f"Skipping {ticker}: {ticker_error}")

        if not stock_results:
            raise ValueError("No stock data processed")

        winner = pick_top_mover(stock_results)

        save_winner(winner)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Daily ingestion successful",
                "winner": winner
            })
        }

    except Exception as error:
        print(f"Ingestion failed: {error}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Ingestion failed",
                "error": str(error)
            })
        }