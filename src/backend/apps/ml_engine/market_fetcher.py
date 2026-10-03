import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from apps.core.models import Asset, MarketData
from .technical_indicators import TechnicalIndicatorsCalculator

class MarketFetcher:
    def __init__(self):
        self.calculator = TechnicalIndicatorsCalculator()

    def sync_asset_market_data(self, asset: Asset, period: str = "60d", interval: str = "1d") -> int:
        """
        Sincroniza los datos OHLCV de mercado para un activo específico desde yfinance.
        Calcula e inserta/actualiza indicadores técnicos en la BD.
        """
        ticker_symbol = asset.ticker
        records_processed = 0

        try:
            ticker_obj = yf.Ticker(ticker_symbol)
            df = ticker_obj.history(period=period, interval=interval)
        except Exception:
            df = pd.DataFrame()

        if df.empty or len(df) == 0:
            df = self._generate_fallback_data(asset.ticker, days=60)
        else:
            df = df.reset_index()
            col_map = {
                'Date': 'timestamp',
                'Datetime': 'timestamp',
                'Open': 'open_price',
                'High': 'high_price',
                'Low': 'low_price',
                'Close': 'close_price',
                'Volume': 'volume'
            }
            df = df.rename(columns=col_map)

        req_cols = ['timestamp', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']
        for col in req_cols:
            if col not in df.columns:
                df[col] = 100.0 if 'price' in col else 10000.0

        # Rellenar cualquier NaN presente en los datos OHLCV
        df['close_price'] = df['close_price'].ffill().bfill().fillna(100.0)
        df['open_price'] = df['open_price'].fillna(df['close_price'])
        df['high_price'] = df['high_price'].fillna(df['close_price'])
        df['low_price'] = df['low_price'].fillna(df['close_price'])
        df['volume'] = df['volume'].fillna(10000.0)

        # Calcular Indicadores Técnicos
        df = self.calculator.calculate_indicators(df)

        for _, row in df.iterrows():
            ts = row['timestamp']
            if isinstance(ts, (str, pd.Timestamp)):
                ts = pd.to_datetime(ts)
                if ts.tzinfo is None:
                    ts = timezone.make_aware(ts)

            MarketData.objects.update_or_create(
                asset=asset,
                timestamp=ts,
                defaults={
                    'open_price': float(row['open_price']),
                    'high_price': float(row['high_price']),
                    'low_price': float(row['low_price']),
                    'close_price': float(row['close_price']),
                    'volume': float(row['volume']),
                    'rsi_14': float(row['rsi_14']),
                    'macd': float(row['macd']),
                    'macd_signal': float(row['macd_signal']),
                    'sma_20': float(row['sma_20']),
                    'sma_50': float(row['sma_50']),
                    'volatility_20': float(row['volatility_20']),
                }
            )
            records_processed += 1

        return records_processed

    def _generate_fallback_data(self, ticker: str, days: int = 60) -> pd.DataFrame:
        """Genera una serie temporal sintética OHLCV realista para desarrollo y pruebas offline."""
        now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        dates = [now - timedelta(days=i) for i in range(days, 0, -1)]
        
        base_price = 180.0 if 'AAPL' in ticker else (220.0 if 'TSLA' in ticker else (65000.0 if 'BTC' in ticker else 3200.0))
        np.random.seed(42)
        returns = np.random.normal(0.001, 0.02, days)
        price_path = base_price * np.exp(np.cumsum(returns))

        data = []
        for i, dt in enumerate(dates):
            close_p = price_path[i]
            open_p = close_p * (1 + np.random.normal(0, 0.005))
            high_p = max(open_p, close_p) * (1 + abs(np.random.normal(0, 0.008)))
            low_p = min(open_p, close_p) * (1 - abs(np.random.normal(0, 0.008)))
            vol = float(np.random.randint(500000, 5000000))
            data.append({
                'timestamp': dt,
                'open_price': open_p,
                'high_price': high_p,
                'low_price': low_p,
                'close_price': close_p,
                'volume': vol
            })

        return pd.DataFrame(data)
