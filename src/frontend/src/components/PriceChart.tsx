import React, { useState } from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';

interface MarketDataPoint {
  timestamp: string;
  close_price: number;
  open_price: number;
  high_price: number;
  low_price: number;
  volume: number;
  rsi_14: number;
  macd: number;
  macd_signal: number;
  sma_20: number;
  sma_50: number;
}

interface PriceChartProps {
  data: MarketDataPoint[];
  ticker: string;
}

export const PriceChart: React.FC<PriceChartProps> = ({ data, ticker }) => {
  const [activeTab, setActiveTab] = useState<'price' | 'rsi' | 'macd'>('price');

  if (!data || data.length === 0) {
    return (
      <div className="glass-panel p-6 rounded-2xl flex items-center justify-center min-h-[350px]">
        <span className="text-slate-400 text-sm">Cargando serie histórica de precios e indicadores...</span>
      </div>
    );
  }

  const formattedData = data.slice(-30).map((item) => ({
    ...item,
    dateStr: new Date(item.timestamp).toLocaleDateString('es-ES', { month: 'short', day: 'numeric' }),
    closeFormatted: Number(item.close_price.toFixed(2)),
    sma20Formatted: Number(item.sma_20.toFixed(2)),
    sma50Formatted: Number(item.sma_50.toFixed(2)),
    rsiFormatted: Number(item.rsi_14.toFixed(1)),
    macdFormatted: Number(item.macd.toFixed(3)),
    macdSignalFormatted: Number(item.macd_signal.toFixed(3)),
  }));

  return (
    <div className="glass-panel p-6 rounded-2xl shadow-2xl flex flex-col justify-between">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <span>Serie Temporal de Precios e Indicadores</span>
            <span className="text-xs font-mono text-blue-400 px-2 py-0.5 rounded bg-blue-500/10 border border-blue-500/20">
              {ticker}
            </span>
          </h3>
          <p className="text-xs text-slate-400">Precios OHLCV e indicadores técnicos calculados</p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center gap-1.5 p-1 bg-dark-900 rounded-xl border border-white/5">
          <button
            onClick={() => setActiveTab('price')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'price'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Precio & SMA
          </button>
          <button
            onClick={() => setActiveTab('rsi')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'rsi'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            RSI (14)
          </button>
          <button
            onClick={() => setActiveTab('macd')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'macd'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            MACD
          </button>
        </div>
      </div>

      {/* Chart Area */}
      <div className="h-[280px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          {activeTab === 'price' ? (
            <ComposedChart data={formattedData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#252f45" opacity={0.5} />
              <XAxis dataKey="dateStr" stroke="#64748b" fontSize={11} />
              <YAxis domain={['auto', 'auto']} stroke="#64748b" fontSize={11} orientation="right" />
              <Tooltip
                contentStyle={{ backgroundColor: '#121722', borderColor: '#252f45', borderRadius: '12px', fontSize: '12px' }}
                itemStyle={{ color: '#fff' }}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '8px' }} />
              <Line type="monotone" dataKey="closeFormatted" name="Precio Cierre ($)" stroke="#3b82f6" strokeWidth={2.5} dot={false} />
              <Line type="monotone" dataKey="sma20Formatted" name="SMA 20" stroke="#10b981" strokeWidth={1.5} dot={false} strokeDasharray="4 4" />
              <Line type="monotone" dataKey="sma50Formatted" name="SMA 50" stroke="#f59e0b" strokeWidth={1.5} dot={false} strokeDasharray="4 4" />
            </ComposedChart>
          ) : activeTab === 'rsi' ? (
            <ComposedChart data={formattedData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#252f45" opacity={0.5} />
              <XAxis dataKey="dateStr" stroke="#64748b" fontSize={11} />
              <YAxis domain={[0, 100]} stroke="#64748b" fontSize={11} orientation="right" />
              <Tooltip
                contentStyle={{ backgroundColor: '#121722', borderColor: '#252f45', borderRadius: '12px', fontSize: '12px' }}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '8px' }} />
              <Line type="monotone" dataKey="rsiFormatted" name="RSI (14)" stroke="#8b5cf6" strokeWidth={2} dot={false} />
            </ComposedChart>
          ) : (
            <ComposedChart data={formattedData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#252f45" opacity={0.5} />
              <XAxis dataKey="dateStr" stroke="#64748b" fontSize={11} />
              <YAxis domain={['auto', 'auto']} stroke="#64748b" fontSize={11} orientation="right" />
              <Tooltip
                contentStyle={{ backgroundColor: '#121722', borderColor: '#252f45', borderRadius: '12px', fontSize: '12px' }}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '8px' }} />
              <Line type="monotone" dataKey="macdFormatted" name="MACD" stroke="#3b82f6" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="macdSignalFormatted" name="Señal MACD" stroke="#ef4444" strokeWidth={1.5} dot={false} />
            </ComposedChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
};
