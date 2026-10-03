import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import timedelta
from django.utils import timezone
from apps.core.models import Asset, Prediction
from .dataset_builder import DatasetBuilder
from .trainer import ARTIFACTS_DIR, MLTrainer

class MLPredictor:
    def __init__(self, version: str = "v1.0.0"):
        self.version = version
        self.model_file = ARTIFACTS_DIR / f'model_{version}.joblib'
        self.artifact = None

    def _load_model(self):
        if self.model_file.exists():
            self.artifact = joblib.load(self.model_file)
            return True
        return False

    def predict_asset(self, asset: Asset) -> Prediction:
        """
        Genera la predicción probabilística (SUBE, ESTABLE, BAJA) para un activo específico
        utilizando las últimas métricas disponibles en T.
        """
        builder = DatasetBuilder(asset)
        df_asset = builder.build_dataset(forward_days=1)

        if df_asset.empty:
            # Fallback a distribución uniforme si no hay datos de mercado aún
            return self._save_prediction(asset, 'ESTABLE', 0.33, 0.34, 0.33)

        # Tomar la última muestra disponible en T
        latest_row = df_asset.iloc[-1]
        feature_cols = MLTrainer.FEATURE_COLS
        X_sample = pd.DataFrame([latest_row[feature_cols]]).fillna(0.0)

        if self._load_model() and self.artifact:
            model = self.artifact['model']
            classes = list(model.classes_)
            probs = model.predict_proba(X_sample)[0]

            prob_map = {cls: float(p) for cls, p in zip(classes, probs)}
            p_sube = prob_map.get('SUBE', 0.0)
            p_estable = prob_map.get('ESTABLE', 0.0)
            p_baja = prob_map.get('BAJA', 0.0)

            # Normalizar probabilidades para asegurar suma = 1.0
            total_p = p_sube + p_estable + p_baja
            if total_p > 0:
                p_sube /= total_p
                p_estable /= total_p
                p_baja /= total_p

            predicted_class = max(prob_map, key=prob_map.get)
        else:
            # Regla heurística basada en RSI y Sentimiento si el modelo no ha sido entrenado aún
            rsi = latest_row['rsi_14']
            sentiment = latest_row['news_sentiment_score']

            if rsi > 60 or sentiment > 0.3:
                predicted_class = 'SUBE'
                p_sube, p_estable, p_baja = 0.65, 0.25, 0.10
            elif rsi < 40 or sentiment < -0.3:
                predicted_class = 'BAJA'
                p_sube, p_estable, p_baja = 0.10, 0.25, 0.65
            else:
                predicted_class = 'ESTABLE'
                p_sube, p_estable, p_baja = 0.20, 0.60, 0.20

        return self._save_prediction(asset, predicted_class, p_sube, p_estable, p_baja)

    def _save_prediction(self, asset: Asset, pred_class: str, p_sube: float, p_est: float, p_baja: float) -> Prediction:
        now = timezone.now()
        target_date = now + timedelta(days=1)

        prediction = Prediction.objects.create(
            asset=asset,
            target_date=target_date,
            predicted_class=pred_class,
            prob_sube=float(p_sube),
            prob_estable=float(p_est),
            prob_baja=float(p_baja),
            model_version=self.version
        )
        return prediction
