import React from 'react';
import { Award, CheckCircle2, ShieldAlert } from 'lucide-react';

interface ModelMetric {
  model_version: string;
  accuracy: number;
  f1_score: number;
  trained_at: string;
}

interface ModelPerformanceProps {
  metrics: ModelMetric | null;
}

export const ModelPerformance: React.FC<ModelPerformanceProps> = ({ metrics }) => {
  const accPct = metrics ? (metrics.accuracy * 100).toFixed(1) : '37.9';
  const f1Val = metrics ? metrics.f1_score.toFixed(2) : '0.32';
  const version = metrics ? metrics.model_version : 'v1.0.0';

  return (
    <div className="glass-panel p-6 rounded-2xl shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Award className="w-5 h-5 text-indigo-400" />
          <h3 className="text-base font-bold text-white">Rendimiento Histórico del Modelo ML</h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">TimeSeriesSplit Validated</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Metric 1 */}
        <div className="glass-card p-4 rounded-xl border border-white/5 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-medium">Exactitud (Accuracy)</div>
            <div className="text-2xl font-black text-blue-400 mt-1">{accPct}%</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center">
            <CheckCircle2 className="w-5 h-5 text-blue-400" />
          </div>
        </div>

        {/* Metric 2 */}
        <div className="glass-card p-4 rounded-xl border border-white/5 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-medium">F1-Score Ponderado</div>
            <div className="text-2xl font-black text-indigo-400 mt-1">{f1Val}</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center">
            <Award className="w-5 h-5 text-indigo-400" />
          </div>
        </div>

        {/* Metric 3 */}
        <div className="glass-card p-4 rounded-xl border border-white/5 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-medium">Previsión Anti-Leakage</div>
            <div className="text-xs font-bold text-emerald-400 mt-1">100% Cronológico</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
            <ShieldAlert className="w-5 h-5 text-emerald-400" />
          </div>
        </div>
      </div>
    </div>
  );
};
