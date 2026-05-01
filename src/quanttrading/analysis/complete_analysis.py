from .visualization import plot_autocorrelation, plot_histogram, plot_rolling_statistics, plot_time_series
from .statistics import calculate_stats, get_percentiles, detect_outliers
import pandas as pd

def full_analysis(df, ticker, window, threshold=3):
    """
    Complte analysis of financial data.
    Calculates statistics, detects outliers, and plot visualizations.
    """

    # 1 - CALCULATE STATISTICS
    print("STATISTICS:")
    stats = calculate_stats(df['Return'])
    for key, value in stats.items():
        print(f' {key}: {value: .3f}')

    # 2. GET PERCENTILES
    print("\nPERCENTILES:")
    percentiles = get_percentiles(df['Return'])
    for key, value in percentiles.items():
        print(f"  {key}: {value:.3f}")

    # 3. DETECT OUTLIERS
    print("\nOUTLIERS:")
    outliers = detect_outliers(df['Return'], threshold=threshold)
    print(f"  Total data points: {len(df)}")
    print(f"  Outliers detected: {outliers.sum()}")
    print(f"  Percentage: {(outliers.sum() / len(df) * 100):.2f}%")

    # 4. PLOT HISTOGRAM
    print("\nPlotting histogram...")
    plot_histogram(df['Return'], title=f"{ticker} - Returns Distribution")
    
    # 5. PLOT TIME SERIES
    print("Plotting time series...")
    plot_time_series(df, title=f"{ticker} - Price Analysis")
    
    # 6. PLOT ROLLING STATISTICS
    print("Plotting rolling statistics...")
    plot_rolling_statistics(df, window=window)

    # 7. PLOT AUTOCORRELATION
    print("Plotting autocorrelation...")
    plot_autocorrelation(df['Return'])
 
    # 8. SHOW OUTLIERS
    if outliers.sum() > 0:
        print(f"\nOutlier details (top 10):")
        outlier_days = df[outliers][['Return']].copy()
        outlier_days['Distance (STD)'] = ((df['Return'] - stats['mean']).abs() / stats['std'])[outliers]
        print(outlier_days.head(10))
    
    print(f"\n{'='*60}\n")

    # Return results as dict
    return {
        'stats': stats,
        'percentiles': percentiles,
        'outliers': outliers,
        'outlier_count': outliers.sum()
    }