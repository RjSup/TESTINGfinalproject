class Config:
    FEATURES = [
        'return_1w',
        'return_4w',
        'return_12w',
        'sma_cross',
        'rsi',
        'macd_signal',
        'volatility'
    ]
    RISK_LEVELS = {
        'HIGH': {'stocks': 4},
        'MEDIUM': {'stocks': 6},
        'LOW': {'stocks': 8}
    }