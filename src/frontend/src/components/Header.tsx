import React from 'react';
import { Activity, ShieldCheck, Cpu, Database } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="glass-panel sticky top-0 z-50 px-6 py-4 flex flex-wrap items-center justify-between border-b border-white/10 shadow-2xl">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-emerald-400 p-0.5 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <div className="w-full h-full bg-dark-900 rounded-[10px] flex items-center justify-center">
            <Activity className="w-5 h-5 text-emerald-400 animate-pulse" />
          </div>
        </div>
        <div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            Predicción Inteligente de Activos
          </h1>
          <p className="text-xs text-slate-400 flex items-center gap-1.5">
            NLP Noticias + Indicadores Técnicos + Machine Learning
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3 mt-2 sm:mt-0">
        <div className="px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Anti-Data Leakage</span>
        </div>
        <div className="px-3 py-1.5 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-medium flex items-center gap-1.5">
          <Cpu className="w-3.5 h-3.5" />
          <span>Scikit / XGBoost ML</span>
        </div>
        <div className="px-3 py-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-medium flex items-center gap-1.5">
          <Database className="w-3.5 h-3.5" />
          <span>API Django REST</span>
        </div>
      </div>
    </header>
  );
};
