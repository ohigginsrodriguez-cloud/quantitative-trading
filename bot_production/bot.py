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


    def run(self, config):
        symbol = config['symbol']
        timeframe = config['timeframe']
        period = config.get('period', '1mo')
        strategy_class = config['strategy']
        params = config['params']

        data = prepare_data(symbol, period, timeframe)
        strategy = VolatilityStrategy(data, params)
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