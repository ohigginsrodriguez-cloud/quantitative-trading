from .base import Strategy
import pandas as pd

class VolatilityStrategy(Strategy):
    
    def __init__(self, data, params):
        super().__init__(data, params)

    def analyze(self):
        volatility = self.data['Return'].rolling(self.params['window']).std().iloc[-1]
        
        if volatility > self.params['threshold']:
            return {'signal': True, 'reason': f'Volatilidad alta: {volatility:.3f} > {self.params["threshold"]}'}
        else:
            return {'signal': False, 'reason': f'Volatilidad baja: {volatility:.3f} < {self.params["threshold"]}'}