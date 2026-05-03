import sys
sys.path.append('/home/pulpo/Documents/quantitative-trading')
sys.path.append('/home/pulpo/Documents/quantitative-trading/bot')

from src.quanttrading.data import prepare_data
from database import init_database, save_trade, close_trade, get_open_trades, get_statistics
from strategies.aapl_volatility import AAPLVolatilityStrategy
from strategies.msft_trend_following import MSFTTrendFollowingStrategy
import pandas as pd
from datetime import datetime
import schedule
import time
import logging

# SETUP LOGGING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pulpo/Documents/quantitative-trading/bot/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutomatedTradingBot:
    def __init__(self, strategies):
        """
        Bot automatizado que ejecuta múltiples estrategias
        
        Args:
            strategies: Lista de tuplas (strategy_instance, symbol)
        """
        self.strategies = strategies
        init_database()
        logger.info("Bot inicializado")
    
    def process_strategy(self, strategy):
        """Procesar una estrategia individual"""
        
        logger.info(f"\n{'='*70}")
        logger.info(f"EJECUTANDO: {strategy.__class__.__name__} ({strategy.symbol})")
        logger.info(f"{'='*70}")
        
        try:
            # Descargar datos
            df = prepare_data(strategy.symbol, '1mo', '4h')
            
            if len(df) < strategy.window:
                logger.warning(f"⚠️  {strategy.symbol}: No hay suficientes datos")
                return
            
            # Analizar con la estrategia
            analysis = self.process_analysis(strategy, df)
            
            # Gestionar trades abiertos
            self.manage_open_trades(strategy, df)
            
            # Log de estadísticas
            self.log_statistics()
            
        except Exception as e:
            logger.error(f"❌ Error en {strategy.symbol}: {e}", exc_info=True)
    
    def process_analysis(self, strategy, df):
        """Ejecutar análisis de la estrategia"""
        
        analysis = strategy.analyze(df)
        
        logger.info(f"📊 Análisis: {analysis['reason']}")
        logger.info(f"   Confianza: {analysis['confidence']:.1%}")
        
        # ⭐ NUEVO: Si ya hay trade abierto del mismo símbolo, NO entres
        open_trades = get_open_trades()
        if any(t[1] == strategy.symbol for t in open_trades):
            logger.info(f"⚠️  Ya hay trade abierto en {strategy.symbol}. Esperando cierre...")
            return analysis
        
        if analysis['signal']:
            logger.info(f"✅ SEÑAL DE ENTRADA")
            logger.info(f"   Entry Price: {analysis['entry_price']:.4f}")
            logger.info(f"   TP: {analysis['tp']:.4f}")
            logger.info(f"   SL: {analysis['sl']:.4f}")
            
            # Guardar trade
            trade_id = save_trade(
                symbol=strategy.symbol,
                entry_time=str(df.index[-1]),
                entry_price=analysis['entry_price'],
                rolling_std=analysis['confidence']
            )
            logger.info(f"   Trade #{trade_id} guardado en BD")
        else:
            logger.info(f"❌ Sin señal")
    
        return analysis
    
    def manage_open_trades(self, strategy, df):
        """Gestionar trades abiertos"""
        
        open_trades = get_open_trades()
        
        if not open_trades:
            return
        
        logger.info(f"📊 Trades abiertos: {len(open_trades)}")
        last_price = df['Close'].iloc[-1]
        
        for trade_id, symbol, entry_price in open_trades:
            if symbol != strategy.symbol:
                continue
            
            tp = entry_price * (1 + strategy.tp_pct)
            sl = entry_price * (1 - strategy.sl_pct)
            
            # Cierre por TP
            if last_price >= tp:
                logger.info(f"✅ CIERRE POR TP - Trade #{trade_id}")
                logger.info(f"   Entry: {entry_price:.4f} | Exit: {last_price:.4f}")
                close_trade(trade_id, str(df.index[-1]), last_price)
            
            # Cierre por SL
            elif last_price <= sl:
                logger.warning(f"❌ CIERRE POR SL - Trade #{trade_id}")
                logger.warning(f"   Entry: {entry_price:.4f} | Exit: {last_price:.4f}")
                close_trade(trade_id, str(df.index[-1]), last_price)
    
    def log_statistics(self):
        """Loguear estadísticas"""
        
        stats = get_statistics()
        
        logger.info(f"\n📈 ESTADÍSTICAS TOTALES:")
        logger.info(f"   Total trades: {stats['total_trades']}")
        logger.info(f"   Ganadores: {stats['winning_trades']}")
        logger.info(f"   Win Rate: {stats['win_rate']:.1f}%")
        logger.info(f"   Total Return: {stats['total_return']:+.2f}%")
        logger.info(f"   Avg Return: {stats['avg_return']:+.2f}%")
    
    def run_all_strategies(self):
        """Ejecutar todas las estrategias"""
        
        logger.info(f"\n\n{'#'*70}")
        logger.info(f"# CICLO DE EJECUCIÓN - {datetime.now()}")
        logger.info(f"{'#'*70}")
        
        for strategy in self.strategies:
            self.process_strategy(strategy)
        
        logger.info(f"\n✅ Ciclo completado\n")
    
    def schedule_hourly(self):
        """Programar ejecución cada hora"""
        
        logger.info("⏰ Bot programado para ejecutar cada hora")
        
        # Ejecutar ahora
        self.run_all_strategies()
        
        # Programar cada hora
        schedule.every().hour.at(":00").do(self.run_all_strategies)
        
        # Loop infinito
        while True:
            schedule.run_pending()
            time.sleep(60)  # Chequear cada minuto

if __name__ == '__main__':
    # CARGAR ESTRATEGIAS
    strategies = [
        AAPLVolatilityStrategy(symbol='AAPL', threshold=2.0),
        MSFTTrendFollowingStrategy(symbol='MSFT', ma_fast=10, ma_slow=20)
    ]
    
    # CREAR BOT
    bot = AutomatedTradingBot(strategies)
    
    # EJECUTAR EN LOOP (cada hora)
    bot.schedule_hourly()