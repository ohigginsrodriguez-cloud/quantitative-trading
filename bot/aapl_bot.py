import sys
sys.path.append('/home/pulpo/Documents/quantitative-trading')

from src.quanttrading.data import prepare_data
from database import init_database, save_trade, close_trade, get_open_trades, get_statistics
import pandas as pd
from datetime import datetime

class AAPLBot:
    def __init__(self):
        self.symbol = 'AAPL'
        self.threshold = 2.0
        self.sl_pct = 0.015
        self.tp_pct = 0.04
        self.window = 30
        
        init_database()
    
    def run(self):
        """Ejecutar bot: descargar datos, evaluar, ejecutar trades"""
        print(f"\n{'='*60}")
        print(f"BOT INICIADO - {datetime.now()}")
        print(f"{'='*60}\n")
        
        # Descargar últimas 100 velas de AAPL 4h
        df = prepare_data(self.symbol, '1mo', '4h')
        
        if len(df) < self.window:
            print("⚠️ No hay suficientes datos")
            return
        
        # Calcular rolling std
        df['rolling_std'] = df['Close'].rolling(self.window).std()
        
        # Último precio y volatilidad
        last_price = df['Close'].iloc[-1]
        last_std = df['rolling_std'].iloc[-1]
        last_time = df.index[-1]
        
        print(f"Símbolo: {self.symbol}")
        print(f"Precio actual: {last_price:.2f}")
        print(f"Rolling STD: {last_std:.4f}")
        print(f"Threshold: {self.threshold}")
        print(f"Hora: {last_time}\n")
        
        # LÓGICA: Entra si volatilidad > threshold
        if last_std > self.threshold:
            print(f"✅ SEÑAL DE ENTRADA DETECTADA")
            print(f"   Volatilidad {last_std:.4f} > Threshold {self.threshold}")
            
            # Guardar trade en BD
            trade_id = save_trade(
                symbol=self.symbol,
                entry_time=str(last_time),  # ← Convertir a string
                entry_price=last_price,
                rolling_std=last_std
            )
            
            # Calcular TP y SL
            tp = last_price * (1 + self.tp_pct)
            sl = last_price * (1 - self.sl_pct)
            
            print(f"\n   Entry Price: {last_price:.4f}")
            print(f"   TP: {tp:.4f} (+{self.tp_pct*100:.1f}%)")
            print(f"   SL: {sl:.4f} (-{self.sl_pct*100:.1f}%)")
        
        else:
            print(f"❌ SIN SEÑAL")
            print(f"   Volatilidad {last_std:.4f} < Threshold {self.threshold}")
        
        # GESTIONAR TRADES ABIERTOS
        open_trades = get_open_trades()
        
        if open_trades:
            print(f"\n📊 Trades abiertos: {len(open_trades)}")
            for trade_id, symbol, entry_price in open_trades:
                # Simulación simple: si subió 2%, cerrar con ganancia
                if last_price > entry_price * 1.02:
                    print(f"\n✅ CIERRE CON GANANCIA (Trade #{trade_id})")
                    close_trade(trade_id, str(last_time), last_price)  # ← Convertir a string
        
        # ESTADÍSTICAS
        stats = get_statistics()
        print(f"\n📈 ESTADÍSTICAS TOTALES:")
        print(f"   Total trades: {stats['total_trades']}")
        print(f"   Ganadores: {stats['winning_trades']}")
        print(f"   Win Rate: {stats['win_rate']:.1f}%")
        print(f"   Total Return: {stats['total_return']:+.2f}%")
        print(f"   Avg Return: {stats['avg_return']:+.2f}%")

if __name__ == '__main__':
    bot = AAPLBot()
    bot.run()