import json
from datetime import datetime, timezone

from backend.services.stock_api import get_daily_open_close
from backend.services.mover_logic import calculate_percent_change, pick_top_mover
from backend.services.db import save_winner

WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

def get_target_date(event: dict) -> str:
    """
    Allows manual testing/backfilling
        serverless invoke -f ingest --data '{"date":"YYYY-MM-DD"}'
    Otherwise, defaults to today's date 
    """
    if event and event.get("date"):
        date_str = event["date"]
        try:
            parsed = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date must be in YYYY-MM-DD format")
        return parsed.strftime("%Y-%m-%d")

    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def handler(event, context):
    try:
        target_date = get_target_date(event or {})
        stock_results = []
        errors = []

        for ticker in WATCHLIST:
            try:
                print(f"Fetching {ticker} for {target_date}")
                data = get_daily_open_close(ticker, target_date)
                print(f"Received data for {ticker}: {data}")

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
                errors.append({
                    "ticker": ticker,
                    "error": str(ticker_error)
                })

        if not stock_results:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "No stock data processed",
                    "date": target_date,
                    "errors": errors
                })
            }

        winner = pick_top_mover(stock_results)
        save_winner(winner)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Daily ingestion successful",
                "winner": winner,
                "errors": errors
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