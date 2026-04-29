"""
(Para mercados con "Inercia")

Cuándo usarla: 
Cuando el Expectancy de los últimos 6 meses es positivo y la Media es claramente superior a 0. 
El precio tiene fuerza para seguir subiendo.
"""

def strategy_momentum(df, window=20, threshold=1.0):
    """
    threshold: Multiplicador de fuerza
    """
    df['rolling_std'] = df['Return'].rolling(window).std()
    
    # Señal: El retorno es positivo y supera la volatilidad normal
    df['Signal'] = df['Return'] > (df['rolling_std'] * threshold)
    
    df['Next_Day_Return'] = df['Return'].shift(-1)
    
    return df[df['Signal'] == True]