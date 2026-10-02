from rest_framework.routers import DefaultRouter
from .views import AssetViewSet, NewsArticleViewSet, MarketDataViewSet, PredictionViewSet, ModelMetricsViewSet

router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'news', NewsArticleViewSet, basename='news')
router.register(r'market-data', MarketDataViewSet, basename='market-data')
router.register(r'predictions', PredictionViewSet, basename='prediction')
router.register(r'metrics', ModelMetricsViewSet, basename='metrics')

urlpatterns = router.urls
