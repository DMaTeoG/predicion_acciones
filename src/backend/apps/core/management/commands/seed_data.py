from django.core.management.base import BaseCommand
from apps.core.models import Asset

class Command(BaseCommand):
    help = 'Crea los activos financieros iniciales (Acciones y Criptomonedas)'

    def handle(self, *args, **options):
        initial_assets = [
            {'ticker': 'AAPL', 'name': 'Apple Inc.', 'asset_type': Asset.AssetType.STOCK},
            {'ticker': 'TSLA', 'name': 'Tesla, Inc.', 'asset_type': Asset.AssetType.STOCK},
            {'ticker': 'MSFT', 'name': 'Microsoft Corporation', 'asset_type': Asset.AssetType.STOCK},
            {'ticker': 'NVDA', 'name': 'NVIDIA Corporation', 'asset_type': Asset.AssetType.STOCK},
            {'ticker': 'BTC-USD', 'name': 'Bitcoin USD', 'asset_type': Asset.AssetType.CRYPTO},
            {'ticker': 'ETH-USD', 'name': 'Ethereum USD', 'asset_type': Asset.AssetType.CRYPTO},
        ]

        created_count = 0
        for data in initial_assets:
            asset, created = Asset.objects.get_or_create(
                ticker=data['ticker'],
                defaults={'name': data['name'], 'asset_type': data['asset_type'], 'is_active': True}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Activo creado: {asset.ticker} ({asset.name})'))
            else:
                self.stdout.write(f'Activo ya existente: {asset.ticker}')

        self.stdout.write(self.style.SUCCESS(f'Sembrado finalizado. Activos nuevos creados: {created_count}'))
