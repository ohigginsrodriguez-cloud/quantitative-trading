import sys
sys.path.append('/home/pulpo/Documents/quantitative-trading')

from config import SYMBOL, TIMEFRAME, PERIOD, STRATEGY_NAME
from strategies.volatility_config import STRATEGY_PARAMS
from database import Database
from strategies.volatility import VolatilityStrategy
from src.quanttrading.data import prepare_data


class TradingBot:
    def __init__(self, db):
        self.db = db
        self.db.create_trades_table()


    def run(self):
        data = prepare_data(SYMBOL, PERIOD, TIMEFRAME)
        strategy = VolatilityStrategy(data, STRATEGY_PARAMS)
        result = strategy.analyze()
        signal = result['signal']

        if signal:
            self.db.insert_trade(
                entry_time=str(data.index[-1]),
                entry_price=data['Close'].iloc[-1],
                size_position=0.2,
                direction='LONG'
            )

if __name__ == '__main__':
    db = Database()
    bot = TradingBot(db)
    bot.run()