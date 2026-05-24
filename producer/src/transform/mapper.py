def map_binance_trade(payload: dict) -> dict:
    return {
        "event_type":     payload["e"],
        "event_time":     payload["E"],
        "symbol":         payload["s"],
        "trade_id":       payload["t"],
        "price":          payload["p"],
        "quantity":       payload["q"],
        "trade_time":     payload["T"],
        "is_buyer_maker": payload["m"],
    }
