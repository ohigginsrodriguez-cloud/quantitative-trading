import sqlite3
from config import DB_PATH

class Database:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)
    
    def create_trades_table(self):
        try:
            with sqlite3.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CRREATE TABLE IF NOT EXISTS trades (
                    id_trades INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_time TEXT NOT NULL,
                    exit_time TEXT,
                    entry_price REAL NOT NULL,
                    exit_price REAL,
                    size_position REAL NOT NULL,
                    direction TEXT NOT NULL,
                    pnl REAL
                    )
                    """
                )
                print('TABLA TRADES CREADA')

        except sqlite3.Error as e:
            print(f'ERROR: {e}')

    def insert_trade(self, entry_time, entry_price, size_position, direction):
        try:
            with sqlite3.connect() as conn:
                cursor = conn.cursor(
                    """
                    INSERT INTO trades (entry_time, entry_price, size_position, direction)
                    VALUES (?, ?, ?, ?)
                    """,(
                        format_datetime(entry_price),
                        format_price(entry_price),
                        format_size(size_position),
                        direction
                    )
                )
                print('TRADE INSERTADO')
                id_trade = cursor.lastrowid
                return id_trade
            
        except sqlite3.Error as e:
            print(f'ERROR: {e}')
            return None
        
    def get_all_trades(self):
        try:
            with sqlite3.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT * FROM trades""")
                trades = cursor.fetchall()
                return trades

        except sqlite3.Error as e:
            print(f'ERROR: {e}')
            return None
        
    def update_trade(self, id_trade, exit_time, exit_price):
        try:
            with sqlite3.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE trades
                    SET exit_time = ?,
                    exit_price = ?,
                    pnl = (? - entry_price) * size_position
                    WHERE id_trade = ?
                    """, (
                        format_datetime(exit_time),
                        format_price(exit_price),
                        id_trade
                    )
                )
                print(f'TRADE #{id_trade} UPDATED')

        except sqlite3.Error as e:
            print(f'ERROR: {e}')

    def get_trade_by_id(self, id_trade):
        try:
            with sqlite3.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT * FROM trades WHERE id_trade = ?""", 
                    (id_trade,)
                )
                trade = cursor.fetchone()
                if trade:
                    print(f'TRADE ENCONTRADO {trade}')
                    return trade
                else:
                    print('TRADE NO ENCONTRADO')
        except sqlite3.Error as e:
            print(f'ERROR: {e}')
            return None






def format_datetime(dt):
    if isinstance(dt, str):
        # SI YA ES STRING, LIMPIA LA ZONA HORARIA
        return dt.split('+')[0]
    #SI ES DATETIME, CONVERTIR A STRING
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def format_price(price):
    return round(price, 3)

def format_size(size):
    return round(size, 4)