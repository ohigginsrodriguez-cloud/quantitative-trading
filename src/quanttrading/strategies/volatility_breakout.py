"""
Lógica: Esta estrategia se basa en que la volatilidad es cíclica. 
Cuando el mercado está muy "quieto" (volatilidad baja), suele ser 
la calma antes de una gran tormenta. 
Compramos cuando el precio rompe esa calma con fuerza.
"""


def strategy_volatility_breakout(df, window=20, breakout_mult=1.5):
    """
    Breakout_mult: Qué tanto debe 'explotar' el precio respecto al rango normal.
    """
    # 1. Medimos el rango típico (High - Low) o simplemente usamos la Std Dev
    df['rolling_std'] = df['Return'].rolling(window).std()
    
    # 2. La señal ocurre cuando el retorno de hoy es mucho mayor a la volatilidad reciente
    # Es decir, el precio 'despertó' de golpe.
    df['Signal'] = df['Return'] > (df['rolling_std'].shift(1) * breakout_mult)
    
    df['Next_Day_Return'] = df['Return'].shift(-1)
    
    return df[df['Signal'] == True]