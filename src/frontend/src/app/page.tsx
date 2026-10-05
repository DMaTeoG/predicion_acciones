'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '../components/Header';
import { AssetSelector } from '../components/AssetSelector';
import { PredictionCard } from '../components/PredictionCard';
import { PriceChart } from '../components/PriceChart';
import { SentimentFeed } from '../components/SentimentFeed';
import { ModelPerformance } from '../components/ModelPerformance';

const API_BASE = 'http://127.0.0.1:8000/api/v1';

export default function Home() {
  const [assets, setAssets] = useState<any[]>([
    { ticker: 'AAPL', name: 'Apple Inc.', asset_type: 'STOCK' },
    { ticker: 'TSLA', name: 'Tesla, Inc.', asset_type: 'STOCK' },
    { ticker: 'MSFT', name: 'Microsoft Corporation', asset_type: 'STOCK' },
    { ticker: 'NVDA', name: 'NVIDIA Corporation', asset_type: 'STOCK' },
    { ticker: 'BTC-USD', name: 'Bitcoin USD', asset_type: 'CRYPTO' },
    { ticker: 'ETH-USD', name: 'Ethereum USD', asset_type: 'CRYPTO' },
  ]);
  const [selectedTicker, setSelectedTicker] = useState<string>('AAPL');
  const [prediction, setPrediction] = useState<any>(null);
  const [marketData, setMarketData] = useState<any[]>([]);
  const [news, setNews] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Fetch Assets list
  useEffect(() => {
    fetch(`${API_BASE}/assets/`)
      .then((res) => res.json())
      .then((data) => {
        if (data.results && data.results.length > 0) {
          setAssets(data.results);
        }
      })
      .catch(() => {});
  }, []);

  // Fetch Data for selected Ticker
  useEffect(() => {
    setLoading(true);

    // 1. Fetch Latest Predictions
    fetch(`${API_BASE}/predictions/latest/`)
      .then((res) => res.json())
      .then((preds) => {
        if (Array.isArray(preds)) {
          const matched = preds.find((p: any) => p.asset_ticker === selectedTicker);
          if (matched) {
            setPrediction(matched);
          } else {
            setPrediction(getDefaultPrediction(selectedTicker));
          }
        }
      })
      .catch(() => {
        setPrediction(getDefaultPrediction(selectedTicker));
      });

    // 2. Fetch Market Data OHLCV & Indicators
    fetch(`${API_BASE}/market-data/?asset=${selectedTicker}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.results && data.results.length > 0) {
          setMarketData(data.results);
        } else {
          setMarketData(getDefaultMarketData(selectedTicker));
        }
      })
      .catch(() => {
        setMarketData(getDefaultMarketData(selectedTicker));
      });

    // 3. Fetch News & Sentiment
    fetch(`${API_BASE}/news/?asset=${selectedTicker}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.results && data.results.length > 0) {
          setNews(data.results);
        } else {
          setNews(getDefaultNews(selectedTicker));
        }
      })
      .catch(() => {
        setNews(getDefaultNews(selectedTicker));
      });

    // 4. Fetch Model Metrics
    fetch(`${API_BASE}/metrics/`)
      .then((res) => res.json())
      .then((data) => {
        if (data.results && data.results.length > 0) {
          setMetrics(data.results[0]);
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [selectedTicker]);

  const currentAsset = assets.find((a) => a.ticker === selectedTicker) || {
    ticker: selectedTicker,
    name: selectedTicker,
  };

  return (
    <div className="min-h-screen bg-dark-900 flex flex-col font-sans">
      <Header />

      <main className="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full space-y-6">
        {/* Asset Selector */}
        <AssetSelector
          assets={assets}
          selectedTicker={selectedTicker}
          onSelect={(ticker) => setSelectedTicker(ticker)}
        />

        {/* Prediction Card & Performance Metric */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <PredictionCard prediction={prediction} assetName={currentAsset.name} />
          </div>
          <div className="lg:col-span-1">
            <ModelPerformance metrics={metrics} />
          </div>
        </div>

        {/* Charts & News Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <PriceChart data={marketData} ticker={selectedTicker} />
          <SentimentFeed news={news} ticker={selectedTicker} />
        </div>
      </main>

      <footer className="glass-panel py-4 px-6 text-center text-xs text-slate-500 border-t border-white/5">
        Sistema Inteligente para la Predicción del Comportamiento de Activos Financieros • Fines Académicos y Experimentales
      </footer>
    </div>
  );
}

// Fallback Mock Generators for offline preview
function getDefaultPrediction(ticker: string) {
  const isUp = ticker === 'NVDA' || ticker === 'BTC-USD';
  return {
    asset_ticker: ticker,
    predicted_class: isUp ? 'SUBE' : ticker === 'TSLA' ? 'BAJA' : 'ESTABLE',
    prob_sube: isUp ? 0.65 : 0.25,
    prob_estable: isUp ? 0.25 : 0.50,
    prob_baja: isUp ? 0.10 : 0.25,
    model_version: 'v1.0.0',
    target_date: new Date().toISOString(),
  };
}

function getDefaultMarketData(ticker: string) {
  const basePrice = ticker === 'BTC-USD' ? 64000 : ticker === 'ETH-USD' ? 3200 : ticker === 'NVDA' ? 125 : 185;
  const list = [];
  const now = new Date();
  for (let i = 30; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    const p = basePrice + Math.sin(i / 3) * (basePrice * 0.04);
    list.push({
      timestamp: d.toISOString(),
      close_price: p,
      open_price: p * 0.99,
      high_price: p * 1.02,
      low_price: p * 0.98,
      volume: 1500000,
      rsi_14: 50 + Math.sin(i / 2) * 15,
      macd: Math.sin(i / 4) * 1.5,
      macd_signal: Math.sin((i - 1) / 4) * 1.2,
      sma_20: p * 0.98,
      sma_50: p * 0.95,
    });
  }
  return list;
}

function getDefaultNews(ticker: string) {
  return [
    {
      id: 1,
      title: `${ticker} reporta sólida aceleración operacional e innovación tecnológica`,
      summary: 'Analistas del mercado destacan el impulso positivo en ingresos y margen bruto.',
      source: 'Financial Times',
      url: 'https://finance.yahoo.com',
      published_at: new Date().toISOString(),
      sentiment: { sentiment_label: 'POSITIVE', sentiment_score: 0.75, impact_score: 0.85 },
    },
    {
      id: 2,
      title: `Inversores monitorean condiciones macroeconómicas globales para ${ticker}`,
      summary: 'La tasa de interés e inflación influyen en la valuación sectorial.',
      source: 'Bloomberg',
      url: 'https://bloomberg.com',
      published_at: new Date().toISOString(),
      sentiment: { sentiment_label: 'NEUTRAL', sentiment_score: 0.05, impact_score: 0.40 },
    },
  ];
}
