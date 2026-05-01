from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt
import pandas as pd

def plot_histogram(returns, title='Returns Distribution'):
    """Plot histogram of returns with statistical lines"""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.style.use('dark_background')
    
    # Histograma
    ax.hist(returns, bins=50, color='white', edgecolor='black', alpha=0.7)
    
    # Líneas de referencia
    mean = returns.mean()
    std = returns.std()
    
    ax.axvline(mean, color='red', linestyle='-', linewidth=2, label=f'Mean: {mean:.4f}')
    ax.axvline(mean + std, color='blue', linestyle='--', linewidth=1.5, label=f'+1 STD')
    ax.axvline(mean - std, color='blue', linestyle='--', linewidth=1.5, label=f'-1 STD')
    
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Returns (%)')
    ax.set_ylabel('Frequency')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.show()

def plot_time_series(df, title='Price Analysis'):
    """Plot price, returns, and volume with better spacing"""
    
    has_volume = 'Volume' in df.columns and df['Volume'].sum() > 0
    n_plots = 3 if has_volume else 2
    
    fig, axes = plt.subplots(n_plots, 1, figsize=(14, 12), sharex=True)
    
    # PRICE
    axes[0].plot(df.index, df['Close'], color='blue', linewidth=1)
    axes[0].set_title('Price Over Time', fontsize=12)
    axes[0].set_ylabel('Price')
    axes[0].grid(True, alpha=0.3)
    
    # RETURNS
    axes[1].bar(df.index, df['Return'], color='green', alpha=0.7, width=1)
    axes[1].axhline(y=0, color='red', linestyle='-', alpha=0.5)
    axes[1].set_title('Daily Returns', fontsize=12)
    axes[1].set_ylabel('Return (%)')
    axes[1].grid(True, alpha=0.3)
    
    # VOLUME
    if has_volume:
        axes[2].bar(df.index, df['Volume'], color='orange', alpha=0.6, width=1)
        axes[2].set_title('Volume', fontsize=12)
        axes[2].set_ylabel('Volume')
        axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_rolling_statistics(df, window=30):
    """Plot rolling volatility, mean, and skewness"""
    
    # Calcular rolling stats
    df_copy = df.copy()
    df_copy['std_rolling'] = df_copy['Return'].rolling(window).std()
    df_copy['mean_rolling'] = df_copy['Return'].rolling(window).mean()
    df_copy['skew_rolling'] = df_copy['Return'].rolling(window).skew()
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # VOLATILITY
    axes[0].plot(df_copy.index, df_copy['std_rolling'], color='red', linewidth=1, label=f'STD ({window}d)')
    axes[0].set_title(f'Rolling Volatility ({window} days)', fontsize=12)
    axes[0].set_ylabel('STD (%)')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # MEAN
    axes[1].plot(df_copy.index, df_copy['mean_rolling'], color='green', linewidth=1, label=f'Mean ({window}d)')
    axes[1].set_title(f'Rolling Mean Return ({window} days)', fontsize=12)
    axes[1].set_ylabel('Mean (%)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    # SKEWNESS
    axes[2].plot(df_copy.index, df_copy['skew_rolling'], color='blue', linewidth=1, label=f'Skew ({window}d)')
    axes[2].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[2].set_title(f'Rolling Skewness ({window} days)', fontsize=12)
    axes[2].set_ylabel('Skew')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()
    
    plt.tight_layout()
    plt.show()

def plot_autocorrelation(returns, nlags=50):
    """Plot autocorrelation of returns and absolute returns"""
    from statsmodels.graphics.tsaplots import plot_acf
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    
    # Returns autocorrelation
    plot_acf(returns.dropna(), lags=nlags, ax=axes[0], alpha=0.05)
    axes[0].set_title('Autocorrelation of Returns')
    axes[0].set_ylabel('Autocorrelation')
    axes[0].grid(True, alpha=0.3)
    
    # Absolute returns (volatility clustering)
    plot_acf(returns.abs().dropna(), lags=nlags, ax=axes[1], alpha=0.05)
    axes[1].set_title('Autocorrelation of Absolute Returns (Volatility Clustering)')
    axes[1].set_ylabel('Autocorrelation')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()