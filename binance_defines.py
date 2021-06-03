class OHLC_enum:
    TIME_OPENNING = 0
    PRICE_OPENNING = 1
    PRICE_HIGHEST = 2
    PRICE_LOWEST = 3
    PRICE_CLOSING = 4
    VOLUME = 5
    TIME_CLOSING = 6
    QUOTE_VOLUME = 7
    NUM_OF_TRADES = 8
    TAKER_BASE_VOLUME = 9
    TAKER_QUOTE_VOLUME = 10
    SPARE = 11

class OHLC_Values:
    def __init__(self, openning_price, highest_price, lowest_price, closing_price, openning_time):
        self.price_openning = openning_price
        self.price_closing = closing_price
        self.price_highest = highest_price
        self.lowest_price = lowest_price
        self.time_opening = openning_time

