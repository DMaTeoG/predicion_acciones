from django.core.management.base import BaseCommand
from apps.core.models import Asset
from apps.ml_engine.predictor import MLPredictor

class Command(BaseCommand):
    help = 'Genera y almacena predicciones probabilísticas para todos los activos activos'

    def add_arguments(self, parser):
        parser.add_argument('--model-version', type=str, default='v1.0.0', help='Versión del modelo a usar')

    def handle(self, *args, **options):
        version = options['model_version']
        predictor = MLPredictor(version=version)
        assets = Asset.objects.filter(is_active=True)

        self.stdout.write(self.style.NOTICE(f'Generando predicciones con modelo {version} para {assets.count()} activos...'))

        for asset in assets:
            pred = predictor.predict_asset(asset)
            self.stdout.write(self.style.SUCCESS(
                f"[{asset.ticker}] Predicción: {pred.predicted_class} | "
                f"Prob Sube: {pred.prob_sube:.1%} | Prob Estable: {pred.prob_estable:.1%} | Prob Baja: {pred.prob_baja:.1%}"
            ))

        self.stdout.write(self.style.SUCCESS('Predicciones generadas y registradas con éxito.'))
