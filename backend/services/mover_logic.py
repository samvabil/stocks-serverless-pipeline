def calculate_percent_change(open_price: float, close_price: float) -> float:
    """ Calculates percent change using formula """
    if open_price == 0:
        raise ValueError("Open price cannot be zero")

    return ((close_price - open_price) / open_price) * 100

def pick_top_mover(stock_results: list[dict]) -> dict:
    """ Returns stock with largest absolute movement """
    if not stock_results:
        raise ValueError("No stock results provided")

    return max(stock_results, key=lambda item: abs(item["percentChange"]))