import pandas as pd
import numpy as np
from datetime import timedelta
from apps.core.models import Asset, MarketData, NewsArticle, NewsSentiment

class DatasetBuilder:
    def __init__(self, asset: Asset):
        self.asset = asset

    def build_dataset(self, forward_days: int = 1, threshold_pct: float = 0.005) -> pd.DataFrame:
        """
        Construye el dataset alineado temporalmente y libre de Data Leakage.
        Features en T:
          - Precios e indicadores OHLCV en T (close_price, volume, rsi_14, macd, macd_signal, sma_20, sma_50, volatility_20)
          - Sentimiento agregado de noticias publicadas en [T-3 días, T] (t <= T)
        Target en T+forward_days:
          - SUBE (cambio > +threshold_pct)
          - BAJA (cambio < -threshold_pct)
          - ESTABLE (cambio dentro de [-threshold_pct, +threshold_pct])
        """
        market_qs = MarketData.objects.filter(asset=self.asset).order_by('timestamp')
        if not market_qs.exists():
            return pd.DataFrame()

        m_data = list(market_qs.values(
            'timestamp', 'open_price', 'high_price', 'low_price', 'close_price', 'volume',
            'rsi_14', 'macd', 'macd_signal', 'sma_20', 'sma_50', 'volatility_20'
        ))
        df_market = pd.DataFrame(m_data)

        # Cargar todas las noticias del activo con su sentimiento
        news_qs = NewsArticle.objects.filter(asset=self.asset).select_related('sentiment')
        news_list = []
        for article in news_qs:
            if hasattr(article, 'sentiment'):
                news_list.append({
                    'published_at': article.published_at,
                    'score': article.sentiment.sentiment_score,
                    'impact': article.sentiment.impact_score
                })
        df_news = pd.DataFrame(news_list)

        rows = []
        for i in range(len(df_market)):
            current_row = df_market.iloc[i]
            current_time = current_row['timestamp']

            # ANTI DATA LEAKAGE: Filtrar noticias estrictamente <= current_time
            if not df_news.empty:
                window_start = current_time - timedelta(days=3)
                relevant_news = df_news[
                    (df_news['published_at'] <= current_time) &
                    (df_news['published_at'] >= window_start)
                ]
                if not relevant_news.empty:
                    mean_sentiment = float(relevant_news['score'].mean())
                    mean_impact = float(relevant_news['impact'].mean())
                    news_count = len(relevant_news)
                else:
                    mean_sentiment = 0.0
                    mean_impact = 0.5
                    news_count = 0
            else:
                mean_sentiment = 0.0
                mean_impact = 0.5
                news_count = 0

            # Calcular Target Y_t+forward_days (solo para datos que tengan futuro)
            target_label = None
            if i + forward_days < len(df_market):
                future_close = df_market.iloc[i + forward_days]['close_price']
                price_change = (future_close - current_row['close_price']) / current_row['close_price']

                if price_change > threshold_pct:
                    target_label = 'SUBE'
                elif price_change < -threshold_pct:
                    target_label = 'BAJA'
                else:
                    target_label = 'ESTABLE'

            row_dict = {
                'timestamp': current_time,
                'open_price': current_row['open_price'],
                'high_price': current_row['high_price'],
                'low_price': current_row['low_price'],
                'close_price': current_row['close_price'],
                'volume': current_row['volume'],
                'rsi_14': current_row['rsi_14'] or 50.0,
                'macd': current_row['macd'] or 0.0,
                'macd_signal': current_row['macd_signal'] or 0.0,
                'sma_20': current_row['sma_20'] or current_row['close_price'],
                'sma_50': current_row['sma_50'] or current_row['close_price'],
                'volatility_20': current_row['volatility_20'] or 0.01,
                'news_sentiment_score': mean_sentiment,
                'news_impact_score': mean_impact,
                'news_count': news_count,
                'target': target_label
            }
            rows.append(row_dict)

        return pd.DataFrame(rows)
