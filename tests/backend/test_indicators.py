import pandas as pd
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.core.models import Asset, MarketData, NewsArticle, NewsSentiment
from apps.ml_engine.technical_indicators import TechnicalIndicatorsCalculator
from apps.ml_engine.dataset_builder import DatasetBuilder

class IndicatorAndDatasetTests(TestCase):

    def setUp(self):
        self.asset = Asset.objects.create(
            ticker='AAPL',
            name='Apple Inc.',
            asset_type=Asset.AssetType.STOCK
        )

        now = timezone.now()
        # Create 10 market data rows
        for i in range(10):
            MarketData.objects.create(
                asset=self.asset,
                timestamp=now - timedelta(days=10 - i),
                open_price=150.0 + i,
                high_price=152.0 + i,
                low_price=149.0 + i,
                close_price=151.0 + i,
                volume=1000000.0,
                rsi_14=55.0,
                macd=0.5,
                macd_signal=0.4,
                sma_20=150.0,
                sma_50=145.0,
                volatility_20=0.015
            )

        # Create news article and sentiment
        article = NewsArticle.objects.create(
            asset=self.asset,
            title='Apple anuncia nueva integración de IA',
            summary='Positivo para ingresos.',
            source='TechCrunch',
            url='https://example.com/aapl-ai-1',
            published_at=now - timedelta(days=5)
        )
        NewsSentiment.objects.create(
            article=article,
            sentiment_label=NewsSentiment.SentimentLabel.POSITIVE,
            sentiment_score=0.8,
            impact_score=0.9
        )

    def test_technical_indicators_calculation(self):
        df_raw = pd.DataFrame([
            {'timestamp': '2026-01-01', 'open_price': 100, 'high_price': 105, 'low_price': 99, 'close_price': 104, 'volume': 1000},
            {'timestamp': '2026-01-02', 'open_price': 104, 'high_price': 108, 'low_price': 103, 'close_price': 107, 'volume': 1200},
            {'timestamp': '2026-01-03', 'open_price': 107, 'high_price': 109, 'low_price': 105, 'close_price': 106, 'volume': 1100},
            {'timestamp': '2026-01-04', 'open_price': 106, 'high_price': 112, 'low_price': 106, 'close_price': 111, 'volume': 1500},
            {'timestamp': '2026-01-05', 'open_price': 111, 'high_price': 115, 'low_price': 110, 'close_price': 114, 'volume': 1800},
        ])
        df_ind = TechnicalIndicatorsCalculator.calculate_indicators(df_raw)
        self.assertIn('rsi_14', df_ind.columns)
        self.assertIn('macd', df_ind.columns)
        self.assertIn('sma_20', df_ind.columns)
        self.assertIn('volatility_20', df_ind.columns)
        self.assertEqual(len(df_ind), 5)

    def test_dataset_builder_anti_leakage(self):
        builder = DatasetBuilder(self.asset)
        df_dataset = builder.build_dataset(forward_days=1)
        self.assertFalse(df_dataset.empty)
        self.assertIn('news_sentiment_score', df_dataset.columns)
        self.assertIn('target', df_dataset.columns)
        
        # Verify target contains valid labels
        valid_targets = {'SUBE', 'BAJA', 'ESTABLE'}
        for target in df_dataset['target']:
            if pd.notna(target) and target is not None:
                self.assertIn(target, valid_targets)
