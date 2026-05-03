import sys
sys.path.append('/home/pulpo/Documents/quantitative-trading')
sys.path.append('/home/pulpo/Documents/quantitative-trading/bot')

from src.quanttrading.data import prepare_data
from database import init_database, save_trade, close_trade, get_open_trades, get_statistics
from strategies.aapl_volatility import AAPLVolatilityStrategy
import pandas as pd
from datetime import datetime

class TradingBot:
    def __init__(self, strategy):
        """
        Bot genérico que carga cualquier estrategia
        
        Args:
            strategy: Instancia de BaseStrategy
        """
        self.strategy = strategy
        init_database()
    
    def run(self):
        """Ejecutar bot con la estrategia cargada"""
        
        print(f"\n{'='*70}")
        print(f"BOT INICIADO - {datetime.now()}")
        print(f"Estrategia: {self.strategy.__class__.__name__}")
        print(f"Símbolo: {self.strategy.symbol}")
        print(f"{'='*70}\n")
        
        # Descargar datos
        try:
            df = prepare_data(self.strategy.symbol, '1mo', '4h')
        except Exception as e:
            print(f"❌ Error descargando datos: {e}")
            return
        
        if len(df) < self.strategy.window:
            print("⚠️ No hay suficientes datos")
            return
        
        # ANALIZAR CON LA ESTRATEGIA
        analysis = self.strategy.analyze(df)
        
        print(f"📊 ANÁLISIS:")
        print(f"   Razón: {analysis['reason']}")
        print(f"   Confianza: {analysis['confidence']:.1%}\n")
        
        # SI HAY SEÑAL
        if analysis['signal']:
            print(f"✅ SEÑAL DE ENTRADA DETECTADA")
            print(f"   Entry Price: {analysis['entry_price']:.4f}")
            print(f"   TP: {analysis['tp']:.4f}")
            print(f"   SL: {analysis['sl']:.4f}")
            print(f"   Confianza: {analysis['confidence']:.1%}\n")
            
            # Guardar en BD
            trade_id = save_trade(
                symbol=self.strategy.symbol,
                entry_time=str(df.index[-1]),
                entry_price=analysis['entry_price'],
                rolling_std=analysis['confidence']
            )
        else:
            print(f"❌ SIN SEÑAL DE ENTRADA\n")
        
        # GESTIONAR TRADES ABIERTOS
        open_trades = get_open_trades()
        
        if open_trades:
            print(f"📊 Trades abiertos: {len(open_trades)}")
            last_price = df['Close'].iloc[-1]
            
            for trade_id, symbol, entry_price in open_trades:
                tp = entry_price * (1 + self.strategy.tp_pct)
                sl = entry_price * (1 - self.strategy.sl_pct)
                
                # Cierre por TP
                if last_price >= tp:
                    print(f"\n✅ CIERRE POR TP (Trade #{trade_id})")
                    close_trade(trade_id, str(df.index[-1]), last_price)
                
                # Cierre por SL
                elif last_price <= sl:
                    print(f"\n❌ CIERRE POR SL (Trade #{trade_id})")
                    close_trade(trade_id, str(df.index[-1]), last_price)
        
        # ESTADÍSTICAS
        stats = get_statistics()
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   Total trades: {stats['total_trades']}")
        print(f"   Ganadores: {stats['winning_trades']}")
        print(f"   Win Rate: {stats['win_rate']:.1f}%")
        print(f"   Total Return: {stats['total_return']:+.2f}%")
        print(f"   Avg Return: {stats['avg_return']:+.2f}%")
        print(f"\n{'='*70}\n")

if __name__ == '__main__':
    # CARGAR LA ESTRATEGIA
    strategy = AAPLVolatilityStrategy(
        symbol='AAPL',
        threshold=2.0,
        sl_pct=0.015,
        tp_pct=0.04,
        window=30
    )
    
    # CREAR BOT CON LA ESTRATEGIA
    bot = TradingBot(strategy)
    
    # EJECUTAR
    bot.run()