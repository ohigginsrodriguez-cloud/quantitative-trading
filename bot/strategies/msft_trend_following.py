import pandas as pd
from strategies.base_strategy import BaseStrategy

class MSFTTrendFollowingStrategy(BaseStrategy):
    """
    Estrategia: Trend Following con Moving Average Crossover
    
    Análisis MSFT:
    - Sesgo negativo (-1.27) = NO es good para mean reversion
    - Kurtosis alta (8.3) = hay eventos extremos
    - Mejor: Seguir tendencias con MA cruce
    """
    
    def __init__(self, symbol='MSFT', ma_fast=10, ma_slow=20, sl_pct=0.02, tp_pct=0.05, window=30):
        super().__init__(symbol, threshold=None, sl_pct=sl_pct, tp_pct=tp_pct, window=window)
        self.ma_fast = ma_fast
        self.ma_slow = ma_slow
    
    def analyze(self, df):
        """
        Lógica: Entra si MA rápida cruza arriba de MA lenta
        """
        
        close = df['Close']
        
        # Calcular medias móviles
        ma_f = close.rolling(self.ma_fast).mean()
        ma_s = close.rolling(self.ma_slow).mean()
        
        last_price = close.iloc[-1]
        
        # CRUCE ALCISTA
        if ma_f.iloc[-1] > ma_s.iloc[-1] and ma_f.iloc[-2] <= ma_s.iloc[-2]:
            tp, sl = self.calculate_tp_sl(last_price)
            
            return {
                'signal': True,
                'entry_price': last_price,
                'tp': tp,
                'sl': sl,
                'confidence': 0.8,
                'reason': f'Cruce alcista: MA{self.ma_fast} ({ma_f.iloc[-1]:.2f}) > MA{self.ma_slow} ({ma_s.iloc[-1]:.2f})'
            }
        
        return {
            'signal': False,
            'entry_price': None,
            'tp': None,
            'sl': None,
            'confidence': 0.0,
            'reason': f'Sin cruce: MA{self.ma_fast} < MA{self.ma_slow}'
        }