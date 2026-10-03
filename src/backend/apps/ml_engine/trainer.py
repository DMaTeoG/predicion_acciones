import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from django.utils import timezone
from apps.core.models import Asset, ModelMetrics
from .dataset_builder import DatasetBuilder

# Directoria de artefactos para modelos entrenados
ARTIFACTS_DIR = Path(__file__).resolve().parent / 'artifacts'
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

class MLTrainer:
    FEATURE_COLS = [
        'close_price', 'volume', 'rsi_14', 'macd', 'macd_signal',
        'sma_20', 'sma_50', 'volatility_20',
        'news_sentiment_score', 'news_impact_score', 'news_count'
    ]

    def __init__(self, version: str = "v1.0.0"):
        self.version = version

    def train_and_evaluate(self) -> dict:
        """
        Consolida datasets de todos los activos activos, aplica TimeSeriesSplit,
        entrena un RandomForestClassifier y serializa el artefacto.
        """
        all_dfs = []
        assets = Asset.objects.filter(is_active=True)

        for asset in assets:
            builder = DatasetBuilder(asset)
            df_asset = builder.build_dataset(forward_days=1)
            if not df_asset.empty:
                # Filtrar filas que tengan target válido
                df_asset = df_asset.dropna(subset=['target'])
                all_dfs.append(df_asset)

        if not all_dfs:
            return {'status': 'error', 'message': 'Sin datos para entrenamiento'}

        df_full = pd.concat(all_dfs, ignore_index=True)
        df_full = df_full.sort_values('timestamp').reset_index(drop=True)

        if len(df_full) < 10:
            return {'status': 'error', 'message': 'Insuficientes muestras (< 10) para entrenamiento'}

        X = df_full[self.FEATURE_COLS].fillna(0.0)
        y = df_full['target']

        # Validación Cruzada Temporal Anti Data-Leakage
        tscv = TimeSeriesSplit(n_splits=min(3, len(df_full) // 5 or 2))
        acc_scores, f1_scores = [], []

        for train_idx, val_idx in tscv.split(X):
            X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]

            clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
            clf.fit(X_tr, y_tr)
            preds = clf.predict(X_val)

            acc_scores.append(accuracy_score(y_val, preds))
            f1_scores.append(f1_score(y_val, preds, average='weighted', zero_division=0))

        # Entrenamiento en dataset completo para modelo final
        final_model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
        final_model.fit(X, y)
        final_preds = final_model.predict(X)

        avg_acc = float(np.mean(acc_scores) if acc_scores else accuracy_score(y, final_preds))
        avg_f1 = float(np.mean(f1_scores) if f1_scores else f1_score(y, final_preds, average='weighted', zero_division=0))
        cm = confusion_matrix(y, final_preds, labels=['SUBE', 'ESTABLE', 'BAJA']).tolist()

        # Guardar artefacto .joblib
        model_path = ARTIFACTS_DIR / f'model_{self.version}.joblib'
        joblib.dump({
            'model': final_model,
            'features': self.FEATURE_COLS,
            'classes': list(final_model.classes_)
        }, model_path)

        # Registrar en la BD
        metrics, _ = ModelMetrics.objects.update_or_create(
            model_version=self.version,
            defaults={
                'accuracy': avg_acc,
                'f1_score': avg_f1,
                'confusion_matrix': cm,
                'features_used': self.FEATURE_COLS
            }
        )

        return {
            'status': 'success',
            'model_version': self.version,
            'accuracy': avg_acc,
            'f1_score': avg_f1,
            'samples_trained': len(df_full),
            'model_file': str(model_path)
        }
