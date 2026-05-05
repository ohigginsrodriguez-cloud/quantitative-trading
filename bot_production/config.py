import os

# RUTA DEL PROYECTO
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_PATH, 'database', 'trades.db')
LOG_PATH = os.path.join(BASE_PATH, 'logs', 'bot.log')

SYMBOL = os.getenv('SYMBOL', 'AAPL')
TIMEFRAME = os.getenv('TIMEFRAME', '4h')
PERIOD = os.getenv('PERIOD', '1mo')

STRATEGY_NAME = os.getenv('STRATEGY', 'volatility')

SCHEDULER_HOURS = 1

DB_NAME = 'trades.db'

print(f"  Configuración cargada")
print(f"   Symbol: {SYMBOL}")
print(f"   Timeframe: {TIMEFRAME}")
print(f"   Strategy: {STRATEGY_NAME}")
print(f"   DB Path: {DB_PATH}")