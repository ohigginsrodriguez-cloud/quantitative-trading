from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """Clase base para todas las estrategias"""
    
    def __init__(self, symbol, threshold=2.0, sl_pct=0.015, tp_pct=0.04, window=30):
        self.symbol = symbol
        self.threshold = threshold
        self.sl_pct = sl_pct
        self.tp_pct = tp_pct
        self.window = window
    
    @abstractmethod
    def analyze(self, df):
        """
        Analizar datos y retornar señal de entrada
        
        Returns:
            dict: {
                'signal': True/False,
                'entry_price': float,
                'tp': float,
                'sl': float,
                'confidence': float (0-1),
                'reason': str
            }
        """
        pass
    
    def calculate_tp_sl(self, entry_price):
        """Calcular TP y SL basado en porcentajes"""
        tp = entry_price * (1 + self.tp_pct)
        sl = entry_price * (1 - self.sl_pct)
        return tp, sl