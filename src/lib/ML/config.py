class Config:
    FEATURES = [
        'return_1m', 'return_3m', 'return_6m',
        'sma3_cross', 'sma6_cross', 'rsi',
        'macd_signal', 'volatility', 'volume_ratio'
    ]
    RISK_LEVELS = {
        'HIGH': {'stocks': 4},
        'MEDIUM': {'stocks': 6},
        'LOW': {'stocks': 8}
    }