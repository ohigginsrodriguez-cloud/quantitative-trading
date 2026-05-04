import sqlite3
from datetime import datetime

def format_datetime(dt):
    """CONVERTIR DATETIME A STRING LIMPIO"""
    if isinstance(dt, str):
        # SI YA ES STRING, LIMPIA LA ZONA HORARIA
        return dt.split('+')[0] # QUITA "+00:00"
    #SI ES DATETIME, CONVERTIR A STRING
    return dt.fstring('%Y-%m-%d %H:%M:%S')

def format_price(price):
    """REDONDEAR EL PRECIO A 3 DECIMALES"""
    return round(price, 3)

def format_size(size):
    return round(size, 4)

DB_PATH = '/home/pulpo/Documents/quantitative-trading/bot_learning/database/trades.db'

class Database:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    def connect(self):
        """DEVUELVE CONEXION
        CONEXION A LA BD, SI NO EXISTE LA CREA"""
        return sqlite3.connect(self.db_name)
    
    def create_trades_table(self):
        """CREAR TABLA SI NO EXISTE
        BUENA PRACTICA MANEJAR ERRORES"""
        try:
            """USO with PORQUE ES BUENA PRACTICA Y 
            AUTOMATIZA EL USO DE commit y close"""
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS trades (
                    id_trade  INTEGER PRIMARY KEY AUTOINCREMENT,
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
                conn.commit()
                print('TRADES TABLE CREATED')
        except sqlite3.Error as e:
            print(f'Error: {e}')

    def insert_trade(self, entry_time, entry_price, size_position, direction):
        """INSERTAR TRADES EN LA TABLA"""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO trades (entry_time, entry_price, size_position, direction) 
                    VALUES (?, ?, ?, ?)
                    """, (
                        format_datetime(entry_time), 
                        format_price(entry_price), 
                        format_size(size_position), 
                        direction)
                )
                conn.commit()
                print('TRADE INSERTED')

                id_trade = cursor.lastrowid #RETORNO EL ID DE LA ULTIMA FILA INSERTADA
                return id_trade
                
        except sqlite3.Error as e:
            print(f'Error: {e}')
            return None

    def get_all_trades(self):
        """MUESTRA TODOS LOS TRADES"""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT * FROM trades ORDER BY id_trade""")
                trades = cursor.fetchall() # DEVUELVE TODOS LOS DATOS SELECCIONADOS
                for fila in trades:
                    print(fila)
                return trades
        except sqlite3.Error as e:
            print(f'Error: {e}')

    def update_trade(self, id_trade, exit_time, exit_price):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """UPDATE trades 
                    SET exit_time = ?,
                    exit_price = ?,
                    pnl = (? - entry_price) * size_position
                    WHERE id_trade = ?
                    """, (
                        format_datetime(exit_time), 
                        format_price(exit_price), 
                        format_price(exit_price), 
                        id_trade)
                )
                conn.commit()
                print(f'TRADE #{id_trade} UPDATED')
                return 
        except sqlite3.Error as e:
            print(f'Error: {e}')


    def get_trade_by_id(self, id_trade):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT * FROM trades WHERE id_trade = ?""",
                    (id_trade,) # COMA AL FINAL SI ES SOLO UNA (TUPLA)
                    )
                trade = cursor.fetchone() # DEVUELVE VALOR SELECCIONADO
                if trade:
                    print(f'TRADE FOUNDED: {trade}')
                    return trade
                else:
                    print(f'DOESN EXISTS ID TRADE: {id_trade}')
                return None
            
        except sqlite3.Error as e:
            print(f'Error: {e}')
            return None


if __name__ =='__main__':
    db = Database()
    db.create_trades_table()
    db.insert_trade(
        entry_time='2026-05-03 10:30:00',
        entry_price=280.15,
        size_position=0.1,
        direction='LONG'
    )
    db.get_all_trades()
    db.update_trade(
        id_trade=1,
        exit_time='2026-05-03 10:35:00',
        exit_price=295.15
    )
    db.get_all_trades()
    db.get_trade_by_id(id_trade=2)