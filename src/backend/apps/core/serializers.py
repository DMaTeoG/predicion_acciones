from rest_framework import serializers
from .models import Asset, NewsArticle, NewsSentiment, MarketData, Prediction, ModelMetrics

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class NewsSentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSentiment
        fields = ['sentiment_label', 'sentiment_score', 'impact_score', 'processed_at']

class NewsArticleSerializer(serializers.ModelSerializer):
    asset_ticker = serializers.CharField(source='asset.ticker', read_only=True)
    sentiment = NewsSentimentSerializer(read_only=True)

    class Meta:
        model = NewsArticle
        fields = ['id', 'asset', 'asset_ticker', 'title', 'summary', 'content', 'source', 'url', 'published_at', 'scraped_at', 'sentiment']

class MarketDataSerializer(serializers.ModelSerializer):
    asset_ticker = serializers.CharField(source='asset.ticker', read_only=True)

    class Meta:
        model = MarketData
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    asset_ticker = serializers.CharField(source='asset.ticker', read_only=True)
    asset_name = serializers.CharField(source='asset.name', read_only=True)

    class Meta:
        model = Prediction
        fields = '__all__'

class ModelMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelMetrics
        fields = '__all__'
