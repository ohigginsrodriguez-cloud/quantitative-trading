"""
(Para mercados de "Rango")

Cuándo usarla: 

Cuando el Skew es cercano a 0 y la Kurtosis no es demasiado extrema. 
El precio rebota como un elástico.
"""

def strategy_mean_reversion(df, window=20, std_mult=1.5):
    """
    df: DataFrame con columna 'Return'
    window: Ventana para la volatilidad móvil
    std_mult: Qué tan 'excesiva' debe ser la caída (1.5 o 2 desviaciones)
    """
    # 1. Calculamos la volatilidad dinámica (Rolling)
    df['rolling_std'] = df['Return'].rolling(window).std()
    
    # 2. Generamos la Señal (Comprar si el retorno cae más que la volatilidad actual)
    # Usamos -df['rolling_std'] para detectar caídas
    df['Signal'] = df['Return'] < -(df['rolling_std'] * std_mult)
    
    # 3. Resultado de "Mañana"
    df['Next_Day_Return'] = df['Return'].shift(-1)
    
    return df[df['Signal'] == True]