import React from 'react';
import { TrendingUp, TrendingDown, Minus, BrainCircuit } from 'lucide-react';

interface Prediction {
  asset_ticker: string;
  predicted_class: 'SUBE' | 'ESTABLE' | 'BAJA';
  prob_sube: number;
  prob_estable: number;
  prob_baja: number;
  model_version: string;
  target_date: string;
}

interface PredictionCardProps {
  prediction: Prediction | null;
  assetName: string;
}

export const PredictionCard: React.FC<PredictionCardProps> = ({ prediction, assetName }) => {
  if (!prediction) {
    return (
      <div className="glass-panel p-6 rounded-2xl flex items-center justify-center min-h-[220px]">
        <span className="text-slate-400 text-sm">Cargando señal de predicción ML...</span>
      </div>
    );
  }

  const { predicted_class, prob_sube, prob_estable, prob_baja, model_version } = prediction;

  const config = {
    SUBE: {
      color: 'from-emerald-500 to-teal-600',
      border: 'border-emerald-500/40',
      shadow: 'shadow-emerald-500/20',
      text: 'text-emerald-400',
      icon: TrendingUp,
      label: 'PREDICCIÓN: SUBE 📈'
    },
    ESTABLE: {
      color: 'from-amber-500 to-yellow-600',
      border: 'border-amber-500/40',
      shadow: 'shadow-amber-500/20',
      text: 'text-amber-400',
      icon: Minus,
      label: 'PREDICCIÓN: ESTABLE ➖'
    },
    BAJA: {
      color: 'from-rose-500 to-red-600',
      border: 'border-rose-500/40',
      shadow: 'shadow-rose-500/20',
      text: 'text-rose-400',
      icon: TrendingDown,
      label: 'PREDICCIÓN: BAJA 📉'
    }
  }[predicted_class] || {
    color: 'from-blue-500 to-indigo-600',
    border: 'border-blue-500/40',
    shadow: 'shadow-blue-500/20',
    text: 'text-blue-400',
    icon: BrainCircuit,
    label: predicted_class
  };

  const IconComp = config.icon;
  const maxProb = Math.max(prob_sube, prob_estable, prob_baja);

  return (
    <div className={`glass-panel p-6 rounded-2xl border ${config.border} shadow-2xl relative overflow-hidden`}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">
            Señal Probabilística ML
          </span>
          <h2 className="text-lg font-bold text-white mt-0.5">{assetName} ({prediction.asset_ticker})</h2>
        </div>
        <div className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[11px] text-slate-300 font-mono">
          Modelo: {model_version}
        </div>
      </div>

      {/* Hero Badge */}
      <div className={`p-4 rounded-xl bg-gradient-to-r ${config.color} ${config.shadow} shadow-lg flex items-center justify-between mb-6`}>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-black/20 flex items-center justify-center">
            <IconComp className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="text-xs text-white/80 font-medium">Predicción de Tendencia (24h)</div>
            <div className="text-xl font-extrabold text-white tracking-wide">{config.label}</div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-white/80">Confianza Máxima</div>
          <div className="text-2xl font-black text-white">{ (maxProb * 100).toFixed(1) }%</div>
        </div>
      </div>

      {/* Probabilities Breakdown */}
      <div className="space-y-3">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
          Distribución de Probabilidades:
        </span>

        {/* SUBE bar */}
        <div>
          <div className="flex justify-between text-xs font-medium mb-1">
            <span className="text-emerald-400 font-semibold">Probabilidad SUBE</span>
            <span className="text-emerald-300 font-mono">{(prob_sube * 100).toFixed(1)}%</span>
          </div>
          <div className="w-full h-2.5 rounded-full bg-dark-900 overflow-hidden p-0.5 border border-white/5">
            <div
              className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-500"
              style={{ width: `${Math.max(2, prob_sube * 100)}%` }}
            />
          </div>
        </div>

        {/* ESTABLE bar */}
        <div>
          <div className="flex justify-between text-xs font-medium mb-1">
            <span className="text-amber-400 font-semibold">Probabilidad ESTABLE</span>
            <span className="text-amber-300 font-mono">{(prob_estable * 100).toFixed(1)}%</span>
          </div>
          <div className="w-full h-2.5 rounded-full bg-dark-900 overflow-hidden p-0.5 border border-white/5">
            <div
              className="h-full rounded-full bg-gradient-to-r from-amber-500 to-yellow-400 transition-all duration-500"
              style={{ width: `${Math.max(2, prob_estable * 100)}%` }}
            />
          </div>
        </div>

        {/* BAJA bar */}
        <div>
          <div className="flex justify-between text-xs font-medium mb-1">
            <span className="text-rose-400 font-semibold">Probabilidad BAJA</span>
            <span className="text-rose-300 font-mono">{(prob_baja * 100).toFixed(1)}%</span>
          </div>
          <div className="w-full h-2.5 rounded-full bg-dark-900 overflow-hidden p-0.5 border border-white/5">
            <div
              className="h-full rounded-full bg-gradient-to-r from-rose-500 to-red-400 transition-all duration-500"
              style={{ width: `${Math.max(2, prob_baja * 100)}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
