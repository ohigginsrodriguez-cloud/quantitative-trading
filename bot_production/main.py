import sys
sys.path.append('/home/pulpo/Documents/quantitative-trading')

import schedule
import time
import logging
from database import Database
from bot import TradingBot
from strategies.volatility import VolatilityStrategy
from strategies.volatility_config import STRATEGY_PARAMS


# SETUP LOGGING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


TRADING_CONFIG = [
    {
        'symbol': 'AAPL',
        'timeframe': '4h',
        'strategy': VolatilityStrategy,
        'params': STRATEGY_PARAMS
    },
    { #LO MISMO PORQUE AUN NO TENEMOS ESTRATEGIA
        'symbol': 'NVDA',
        'timeframe': '4h',
        'strategy': VolatilityStrategy,
        'params': STRATEGY_PARAMS
    },
    { #LO MISMO PORQUE AUN NO TENEMOS ESTRATEGIA
        'symbol': 'MSFT',
        'timeframe': '4h',
        'strategy': VolatilityStrategy,
        'params': STRATEGY_PARAMS
    }
]

def run_bots():
    logger.info('INICIANDO CICLO DE EJECUCION')
    db = Database()

    for config in TRADING_CONFIG:
        logger.info(f"Ejecutando {config['symbol']}")
        try:
            bot = TradingBot(db)
            bot.run(config)
        except Exception as e:
            logger.error(f"ERROR EN {config['symbol']}: {e}")

    logger.info('CICLO COMPLETADO\n')

if __name__ == '__main__':
    logger.info('BOT INICIADO - EJECUTANDO CADA HORA')
    schedule.every().hours.do(run_bots)
    while True:
        schedule.run_pending()
        time.sleep(60)