from django.core.management.base import BaseCommand
from apps.ml_engine.trainer import MLTrainer

class Command(BaseCommand):
    help = 'Entrena y evalúa el modelo de Machine Learning con TimeSeriesSplit'

    def add_arguments(self, parser):
        parser.add_argument('--model-version', type=str, default='v1.0.0', help='Versión del modelo')

    def handle(self, *args, **options):
        version = options['model_version']
        self.stdout.write(self.style.NOTICE(f'Iniciando entrenamiento del modelo {version}...'))

        trainer = MLTrainer(version=version)
        result = trainer.train_and_evaluate()

        if result.get('status') == 'success':
            self.stdout.write(self.style.SUCCESS(
                f"Entrenamiento exitoso | Modelo {result['model_version']} | "
                f"Accuracy: {result['accuracy']:.2%} | F1-Score: {result['f1_score']:.2f} | "
                f"Muestras: {result['samples_trained']}"
            ))
        else:
            self.stdout.write(self.style.ERROR(f"Error en entrenamiento: {result.get('message')}"))
