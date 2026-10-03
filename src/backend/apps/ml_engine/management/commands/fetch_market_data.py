from django.core.management.base import BaseCommand
from apps.core.models import Asset
from apps.ml_engine.market_fetcher import MarketFetcher

class Command(BaseCommand):
    help = 'Sincroniza precios e indicadores técnicos de mercado para los activos activos'

    def handle(self, *args, **options):
        fetcher = MarketFetcher()
        assets = Asset.objects.filter(is_active=True)
        total_records = 0

        self.stdout.write(self.style.NOTICE(f'Iniciando sincronización para {assets.count()} activos...'))

        for asset in assets:
            count = fetcher.sync_asset_market_data(asset)
            total_records += count
            self.stdout.write(self.style.SUCCESS(f'[{asset.ticker}] Registros procesados: {count}'))

        self.stdout.write(self.style.SUCCESS(f'Sincronización completa. Total de registros procesados: {total_records}'))
