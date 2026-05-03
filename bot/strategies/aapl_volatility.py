import pandas as pd
from base_strategy import BaseStrategy

class AAPLVolatilityStrategy(BaseStrategy):
    """
    Estrategia: Entra cuando volatility (rolling std) > threshold
    
    Análisis:
    - AAPL tiene kurtosis alta (2.3)
    - Sesgo positivo (+0.53)
    - Perfecto para mean reversion en volatilidad alta
    """
    
    def __init__(self, symbol='AAPL', threshold=2.0, sl_pct=0.015, tp_pct=0.04, window=30):
        super().__init__(symbol, threshold, sl_pct, tp_pct, window)
    
    def analyze(self, df):
        """
        Lógica de entrada:
        1. Calcular rolling std del precio
        2. Si rolling_std > threshold → SEÑAL
        3. Retornar entrada con TP/SL
        """
        
        # Calcular rolling volatilidad
        rolling_std = df['Close'].rolling(self.window).std()
        
        last_std = rolling_std.iloc[-1]
        last_price = df['Close'].iloc[-1]
        last_time = df.index[-1]
        
        # LÓGICA DE ENTRADA
        if last_std > self.threshold:
            tp, sl = self.calculate_tp_sl(last_price)
            
            return {
                'signal': True,
                'entry_price': last_price,
                'tp': tp,
                'sl': sl,
                'confidence': min(last_std / self.threshold, 1.0),  # 0-1
                'reason': f'Volatilidad alta: {last_std:.4f} > {self.threshold}'
            }
        
        return {
            'signal': False,
            'entry_price': None,
            'tp': None,
            'sl': None,
            'confidence': 0.0,
            'reason': f'Volatilidad baja: {last_std:.4f} < {self.threshold}'
        }