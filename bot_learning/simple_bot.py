import sys 
sys.path.append('/home/pulpo/Documents/quantitative-trading')
from src.quanttrading.data import prepare_data
from simple_database import Database
import pandas as pd


df_aapl = prepare_data('AAPL', '1mo', '4h')

window = 30
volatility = df_aapl['Return'].rolling(window).std().iloc[-1]
threshold = 1
entry_price = df_aapl['Close'].iloc[-1]
exit_price = entry_price * 1.05 # SIMULACION DE SUBIDA DE PRECIO

db = Database()

if volatility > threshold:
    print('TRADE ABIERTO')
    id_trade = db.insert_trade(
        entry_time     = str(df_aapl.index[-1]),
        entry_price    = 100 * 1.05,
        size_position  = 0.1,
        direction      = 'LONG'
    )
else:
    print(f'Volatilidad estable: {volatility: .3f}')

if id_trade:
    db.update_trade(
        id_trade    = id_trade,
        exit_time   = str(df_aapl.index[-1]),
        exit_price  = exit_price
    )

    db.get_trade_by_id(id_trade=id_trade)