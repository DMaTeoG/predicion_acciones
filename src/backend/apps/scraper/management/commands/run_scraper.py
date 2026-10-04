from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.core.models import Asset, NewsArticle, NewsSentiment
from apps.nlp.sentiment_engine import SentimentEngine

class Command(BaseCommand):
    help = 'Ejecuta la ingesta de noticias financieras y el pipeline NLP'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando ingesta de noticias y pipeline NLP...'))
        sentiment_engine = SentimentEngine()

        sample_news = [
            {
                'ticker': 'AAPL',
                'title': 'Apple alcanza ingresos récord impulsados por fuertes ventas de iPhone 15 y servicios',
                'summary': 'Los analistas destacan el crecimiento sostenido del margen bruto de la compañía tecnológica.',
                'source': 'Reuters',
                'url': 'https://news.example.com/aapl-record-revenue-2026',
                'sentiment': 'POSITIVE',
                'days_ago': 2
            },
            {
                'ticker': 'AAPL',
                'title': 'Preocupación por ralentización de entregas de la cadena de suministro en Asia para Apple',
                'summary': 'Retrasos en componentes de pantalla podrían afectar el volumen del próximo trimestre.',
                'source': 'Bloomberg',
                'url': 'https://news.example.com/aapl-supply-chain-delay-2026',
                'sentiment': 'NEGATIVE',
                'days_ago': 1
            },
            {
                'ticker': 'TSLA',
                'title': 'Tesla anuncia nueva super-fábrica y entregas récord de vehículos eléctricos',
                'summary': 'La optimización de baterías reduce costos de producción un 15 por ciento.',
                'source': 'Financial Times',
                'url': 'https://news.example.com/tsla-gigafactory-expansion-2026',
                'sentiment': 'POSITIVE',
                'days_ago': 2
            },
            {
                'ticker': 'TSLA',
                'title': 'Investigadores evalúan impacto de regulaciones de conducción autónoma en Tesla',
                'summary': 'Nuevas guías de transporte requerirán validación adicional para el sistema de piloto automático.',
                'source': 'Wall Street Journal',
                'url': 'https://news.example.com/tsla-regulatory-scrutiny-2026',
                'sentiment': 'NEUTRAL',
                'days_ago': 0
            },
            {
                'ticker': 'BTC-USD',
                'title': 'Bitcoin supera la resistencia de los 65.000 dólares tras entrada masiva en ETFs',
                'summary': 'La demanda institucional y el halving impulsan el precio del activo digital a nuevos máximos.',
                'source': 'CoinDesk',
                'url': 'https://news.example.com/btc-etf-rally-2026',
                'sentiment': 'POSITIVE',
                'days_ago': 1
            },
            {
                'ticker': 'ETH-USD',
                'title': 'La red Ethereum implementa actualización para reducir tarifas de gas significativamente',
                'summary': 'Desarrolladores reportan un incremento en las transacciones por segundo en Layer-2.',
                'source': 'Decrypt',
                'url': 'https://news.example.com/eth-upgrade-gas-fees-2026',
                'sentiment': 'POSITIVE',
                'days_ago': 0
            }
        ]

        count = 0
        now = timezone.now()

        for item in sample_news:
            try:
                asset = Asset.objects.get(ticker=item['ticker'])
            except Asset.DoesNotExist:
                continue

            pub_date = now - timedelta(days=item['days_ago'])

            article, created = NewsArticle.objects.get_or_create(
                url=item['url'],
                defaults={
                    'asset': asset,
                    'title': item['title'],
                    'summary': item['summary'],
                    'source': item['source'],
                    'published_at': pub_date
                }
            )

            if created or not hasattr(article, 'sentiment'):
                nlp_res = sentiment_engine.analyze_text(f"{item['title']} {item['summary']}")

                NewsSentiment.objects.update_or_create(
                    article=article,
                    defaults={
                        'sentiment_label': nlp_res['sentiment_label'],
                        'sentiment_score': nlp_res['sentiment_score'],
                        'impact_score': nlp_res['impact_score']
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Ingesta e inferencia NLP completadas. Noticias procesadas: {count}'))
