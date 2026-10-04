from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.core.models import Asset, MarketData, NewsArticle, NewsSentiment, Prediction, ModelMetrics
from apps.ml_engine.trainer import MLTrainer
from apps.ml_engine.predictor import MLPredictor

class MLEngineTests(TestCase):

    def setUp(self):
        self.asset = Asset.objects.create(
            ticker='AAPL',
            name='Apple Inc.',
            asset_type=Asset.AssetType.STOCK
        )

        now = timezone.now()
        # Create 30 rows of market data to allow TimeSeriesSplit
        for i in range(30):
            MarketData.objects.create(
                asset=self.asset,
                timestamp=now - timedelta(days=30 - i),
                open_price=150.0 + (i * 0.5),
                high_price=152.0 + (i * 0.5),
                low_price=149.0 + (i * 0.5),
                close_price=151.0 + (i * 0.5),
                volume=1000000.0,
                rsi_14=50.0 + (i % 10),
                macd=0.1 * i,
                macd_signal=0.08 * i,
                sma_20=150.0,
                sma_50=145.0,
                volatility_20=0.015
            )

        # Create news article & sentiment
        article = NewsArticle.objects.create(
            asset=self.asset,
            title='Apple anuncia sólidas métricas operativas',
            summary='Positivo para inversores.',
            source='Reuters',
            url='https://example.com/aapl-test-ml',
            published_at=now - timedelta(days=15)
        )
        NewsSentiment.objects.create(
            article=article,
            sentiment_label=NewsSentiment.SentimentLabel.POSITIVE,
            sentiment_score=0.75,
            impact_score=0.85
        )

    def test_ml_trainer_execution(self):
        trainer = MLTrainer(version='test_v1.0')
        result = trainer.train_and_evaluate()
        self.assertEqual(result['status'], 'success')
        self.assertGreaterEqual(result['accuracy'], 0.0)
        self.assertGreaterEqual(result['f1_score'], 0.0)
        
        # Verify ModelMetrics created in DB
        metrics = ModelMetrics.objects.filter(model_version='test_v1.0').first()
        self.assertIsNotNone(metrics)

    def test_ml_predictor_execution(self):
        # Train first
        trainer = MLTrainer(version='test_v1.0')
        trainer.train_and_evaluate()

        # Predict
        predictor = MLPredictor(version='test_v1.0')
        pred = predictor.predict_asset(self.asset)

        self.assertIsNotNone(pred)
        self.assertIn(pred.predicted_class, ['SUBE', 'ESTABLE', 'BAJA'])
        self.assertAlmostEqual(pred.prob_sube + pred.prob_estable + pred.prob_baja, 1.0, places=4)
