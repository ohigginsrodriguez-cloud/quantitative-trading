import pandas as pd

def calculate_stats(series):
    """Calculate statistical masures of a series"""
    mean = series.mean()
    std = series.std()
    skew = series.skew()
    kurt = series.kurt()
    return{'mean': mean, 'std': std, 'skew': skew, 'kurt': kurt}

def get_percentiles(series):
    """Calculate percentiles of a series"""
    p05 = series.quantile(0.05)
    p25 = series.quantile(0.25)
    p75 = series.quantile(0.75)
    p95 = series.quantile(0.95)
    return {'p05': p05, 'p25': p25, 'p75': p75, 'p95': p95}

def detect_outliers(series, threshold=3):
    """
    Detect outliers using standard deviation method.
    Returns boolean series where True = outlier
    """
    mean = series.mean()
    std = series.std()
    distance = (series - mean).abs() /std
    return distance > tereshold