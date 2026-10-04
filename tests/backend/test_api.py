from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from apps.core.models import Asset, NewsArticle, NewsSentiment, MarketData, Prediction, ModelMetrics

class APIIntegrationTests(APITestCase):

    def setUp(self):
        self.asset = Asset.objects.create(
            ticker='AAPL',
            name='Apple Inc.',
            asset_type=Asset.AssetType.STOCK
        )

        now = timezone.now()
        self.article = NewsArticle.objects.create(
            asset=self.asset,
            title='Prueba Noticia API',
            summary='Resumen API',
            source='Reuters',
            url='https://example.com/api-news-1',
            published_at=now
        )
        self.sentiment = NewsSentiment.objects.create(
            article=self.article,
            sentiment_label=NewsSentiment.SentimentLabel.POSITIVE,
            sentiment_score=0.8,
            impact_score=0.9
        )
        self.market_data = MarketData.objects.create(
            asset=self.asset,
            timestamp=now,
            open_price=150.0,
            high_price=152.0,
            low_price=149.0,
            close_price=151.0,
            volume=1000000.0,
            rsi_14=55.0,
            macd=0.5,
            macd_signal=0.4,
            sma_20=150.0,
            sma_50=145.0,
            volatility_20=0.015
        )
        self.prediction = Prediction.objects.create(
            asset=self.asset,
            target_date=now,
            predicted_class=Prediction.PredictedClass.SUBE,
            prob_sube=0.70,
            prob_estable=0.20,
            prob_baja=0.10,
            model_version='v1.0.0'
        )
        self.metrics = ModelMetrics.objects.create(
            model_version='v1.0.0',
            accuracy=0.85,
            f1_score=0.82
        )

    def test_get_assets(self):
        response = self.client.get('/api/v1/assets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_news_by_asset(self):
        response = self.client.get('/api/v1/news/?asset=AAPL')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['asset_ticker'], 'AAPL')

    def test_get_market_data_by_asset(self):
        response = self.client.get('/api/v1/market-data/?asset=AAPL')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_latest_predictions(self):
        response = self.client.get('/api/v1/predictions/latest/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['asset_ticker'], 'AAPL')
        self.assertEqual(response.data[0]['predicted_class'], 'SUBE')

    def test_get_metrics(self):
        response = self.client.get('/api/v1/metrics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
