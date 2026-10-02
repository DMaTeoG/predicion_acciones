from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Asset, NewsArticle, NewsSentiment, MarketData, Prediction, ModelMetrics
from .serializers import (
    AssetSerializer, NewsArticleSerializer, MarketDataSerializer,
    PredictionSerializer, ModelMetricsSerializer
)

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.filter(is_active=True)
    serializer_class = AssetSerializer

class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.select_related('asset', 'sentiment').all()
    serializer_class = NewsArticleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        ticker = self.request.query_params.get('asset', None)
        if ticker:
            queryset = queryset.filter(asset__ticker__iexact=ticker)
        return queryset

class MarketDataViewSet(viewsets.ModelViewSet):
    queryset = MarketData.objects.select_related('asset').all()
    serializer_class = MarketDataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        ticker = self.request.query_params.get('asset', None)
        if ticker:
            queryset = queryset.filter(asset__ticker__iexact=ticker)
        return queryset

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.select_related('asset').all()
    serializer_class = PredictionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        ticker = self.request.query_params.get('asset', None)
        if ticker:
            queryset = queryset.filter(asset__ticker__iexact=ticker)
        return queryset

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Devuelve la predicción más reciente para cada activo activo."""
        assets = Asset.objects.filter(is_active=True)
        latest_predictions = []
        for asset in assets:
            pred = Prediction.objects.filter(asset=asset).order_by('-prediction_date').first()
            if pred:
                latest_predictions.append(pred)
        serializer = self.get_serializer(latest_predictions, many=True)
        return Response(serializer.data)

class ModelMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelMetrics.objects.all()
    serializer_class = ModelMetricsSerializer
