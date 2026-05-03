import sqlite3
import os
from datetime import datetime

# Ruta de la BD
DB_PATH = '/home/pulpo/Documents/quantitative-trading/bot/trades.db'

def init_database():
    """Crear tabla de trades si no existe"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            entry_time DATETIME NOT NULL,
            entry_price REAL NOT NULL,
            exit_time DATETIME,
            exit_price REAL,
            pnl REAL,
            return_pct REAL,
            status TEXT DEFAULT 'OPEN',
            rolling_std REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada")

def save_trade(symbol, entry_time, entry_price, rolling_std):
    """Guardar nuevo trade ABIERTO"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO trades (symbol, entry_time, entry_price, rolling_std, status)
        VALUES (?, ?, ?, ?, 'OPEN')
    ''', (symbol, entry_time, entry_price, rolling_std))
    
    trade_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Trade #{trade_id} guardado: {symbol} @ {entry_price}")
    return trade_id

def close_trade(trade_id, exit_time, exit_price):
    """Cerrar un trade y calcular PnL"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener entry_price
    cursor.execute('SELECT entry_price FROM trades WHERE id = ?', (trade_id,))
    entry_price = cursor.fetchone()[0]
    
    # Calcular PnL
    pnl = exit_price - entry_price
    return_pct = (pnl / entry_price) * 100
    
    cursor.execute('''
        UPDATE trades 
        SET exit_time = ?, exit_price = ?, pnl = ?, return_pct = ?, status = 'CLOSED'
        WHERE id = ?
    ''', (exit_time, exit_price, pnl, return_pct, trade_id))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Trade #{trade_id} cerrado: PnL {pnl:.4f} ({return_pct:+.2f}%)")

def get_open_trades():
    """Obtener trades abiertos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, symbol, entry_price FROM trades WHERE status = "OPEN"')
    trades = cursor.fetchall()
    conn.close()
    
    return trades

def get_all_trades():
    """Obtener todos los trades para análisis"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM trades ORDER BY entry_time DESC')
    trades = cursor.fetchall()
    conn.close()
    
    return trades

def get_statistics():
    """Obtener estadísticas de trading"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM trades WHERE status = "CLOSED"')
    total_trades = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM trades WHERE status = "CLOSED" AND return_pct > 0')
    winning_trades = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(return_pct) FROM trades WHERE status = "CLOSED"')
    total_return = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT AVG(return_pct) FROM trades WHERE status = "CLOSED"')
    avg_return = cursor.fetchone()[0] or 0
    
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    conn.close()
    
    return {
        'total_trades': total_trades,
        'winning_trades': winning_trades,
        'win_rate': win_rate,
        'total_return': total_return,
        'avg_return': avg_return
    }

if __name__ == '__main__':
    init_database()