from database import get_all_trades, get_statistics
import pandas as pd

def view_database():
    """Ver todos los trades en la BD"""
    print("\n" + "="*80)
    print("TRADES EN LA BASE DE DATOS")
    print("="*80 + "\n")
    
    trades = get_all_trades()
    
    if not trades:
        print("No hay trades aún")
        return
    
    # Convertir a DataFrame para mostrar bonito
    columns = ['ID', 'Symbol', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price', 'PnL', 'Return %', 'Status', 'Rolling STD', 'Created']
    df = pd.DataFrame(trades, columns=columns)
    
    print(df.to_string(index=False))
    
    # Estadísticas
    print("\n" + "="*80)
    print("ESTADÍSTICAS")
    print("="*80)
    stats = get_statistics()
    
    print(f"\nTotal trades cerrados: {stats['total_trades']}")
    print(f"Trades ganadores: {stats['winning_trades']}")
    print(f"Win Rate: {stats['win_rate']:.1f}%")
    print(f"Total Return: {stats['total_return']:+.2f}%")
    print(f"Avg Return/Trade: {stats['avg_return']:+.2f}%")

if __name__ == '__main__':
    view_database()