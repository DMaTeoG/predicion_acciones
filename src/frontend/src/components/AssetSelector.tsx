import React from 'react';
import { TrendingUp, Coins } from 'lucide-react';

interface Asset {
  ticker: string;
  name: string;
  asset_type: string;
}

interface AssetSelectorProps {
  assets: Asset[];
  selectedTicker: string;
  onSelect: (ticker: string) => void;
}

export const AssetSelector: React.FC<AssetSelectorProps> = ({ assets, selectedTicker, onSelect }) => {
  return (
    <div className="glass-panel p-4 rounded-2xl flex flex-wrap items-center justify-between gap-3 shadow-xl">
      <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">
        Activos Monitoreados:
      </span>
      <div className="flex flex-wrap items-center gap-2">
        {assets.map((asset) => {
          const isSelected = asset.ticker === selectedTicker;
          const isCrypto = asset.asset_type === 'CRYPTO';

          return (
            <button
              key={asset.ticker}
              onClick={() => onSelect(asset.ticker)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all duration-200 flex items-center gap-2 ${
                isSelected
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/30 scale-105 border border-blue-400/30'
                  : 'glass-card text-slate-300 hover:text-white hover:bg-white/10'
              }`}
            >
              {isCrypto ? (
                <Coins className={`w-3.5 h-3.5 ${isSelected ? 'text-amber-300' : 'text-amber-400'}`} />
              ) : (
                <TrendingUp className={`w-3.5 h-3.5 ${isSelected ? 'text-emerald-300' : 'text-emerald-400'}`} />
              )}
              <span>{asset.ticker}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
