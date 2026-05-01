import matplotlib.pyplot as plt
import pandas as pd

def plot_histogram(returns, title='Returns Distribution'):

    plt.figure(figsize=(12, 6))
    plt.style.use('dark_background')
    plt.hist(returns, bins=50, color='white', edgecolor='black')
    plt.axvline(0, color='red', linestyle='-', linewidth=2)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_time_series(df, title='Price Analysis'):
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    #PRICE
    axes[0].plot(df. index, df['Close'], color='blue', linewidth=1)
    axes[0].set_title('Pice over time')
    axes[0].set_ylabel('Price')

    #RETURNS
    axes[1].bar(df.index, df['Return'], color='green', alpha=1, linewidth=0.02)
    axes[1].axhline(y=0, color='red', linestyle='-', alpha=0.5)
    axes[1].set_title('Daily Returns')
    axes[1].set_ylabel('Returns (%)')
    axes[1].grid(True, alpha=0.3)

    #VOLUME
    axes[2].bar(df.index, df['Volume'], color='orange', alpha=0.6, linewidth=0.02)
    axes[2].grid(True, alpha=0.3)
    axes[2].set_ylabel('Volume')
    axes[2].set_title('Volume')

    plt.tight_layout()
    plt.shoow()

def plot_rolling_statistics(df, window):
    df['std_30'] = df['Return'].rolling(window).std()
    df['mean_30'] = df['Return'].rolling(window).mean()
    df['skew_30'] = df['Return'].rolling(window).skew()

    +