import React from 'react';
import { Newspaper, ExternalLink, ThumbsUp, ThumbsDown, Minus } from 'lucide-react';

interface NewsItem {
  id: number;
  title: string;
  summary: string;
  source: string;
  url: string;
  published_at: string;
  sentiment?: {
    sentiment_label: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
    sentiment_score: number;
    impact_score: number;
  };
}

interface SentimentFeedProps {
  news: NewsItem[];
  ticker: string;
}

export const SentimentFeed: React.FC<SentimentFeedProps> = ({ news, ticker }) => {
  if (!news || news.length === 0) {
    return (
      <div className="glass-panel p-6 rounded-2xl flex items-center justify-center min-h-[300px]">
        <span className="text-slate-400 text-sm">No hay noticias procesadas recientemente para {ticker}.</span>
      </div>
    );
  }

  // Calculate Average Sentiment Score
  const validSentiments = news.filter((item) => item.sentiment);
  const avgScore = validSentiments.length > 0
    ? validSentiments.reduce((acc, curr) => acc + (curr.sentiment?.sentiment_score || 0), 0) / validSentiments.length
    : 0;

  const sentimentCategory = avgScore >= 0.1 ? 'Positivo' : avgScore <= -0.1 ? 'Negativo' : 'Neutro';
  const categoryColor = avgScore >= 0.1 ? 'text-emerald-400' : avgScore <= -0.1 ? 'text-rose-400' : 'text-amber-400';

  return (
    <div className="glass-panel p-6 rounded-2xl shadow-2xl flex flex-col justify-between h-full">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Newspaper className="w-5 h-5 text-blue-400" />
            <span>Feed de Noticias & Sentimiento NLP</span>
          </h3>
          <p className="text-xs text-slate-400">Titulares rastreados y clasificados en tiempo real</p>
        </div>

        <div className="text-right">
          <div className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">Sentimiento Promedio</div>
          <div className={`text-base font-black ${categoryColor} flex items-center justify-end gap-1`}>
            <span>{sentimentCategory}</span>
            <span className="text-xs font-mono">({avgScore > 0 ? `+${avgScore.toFixed(2)}` : avgScore.toFixed(2)})</span>
          </div>
        </div>
      </div>

      {/* News List */}
      <div className="space-y-3 max-h-[360px] overflow-y-auto pr-1">
        {news.map((item) => {
          const sent = item.sentiment;
          const label = sent?.sentiment_label || 'NEUTRAL';
          const score = sent?.sentiment_score || 0;

          const badgeConfig = {
            POSITIVE: { bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400', icon: ThumbsUp },
            NEUTRAL: { bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400', icon: Minus },
            NEGATIVE: { bg: 'bg-rose-500/10 border-rose-500/30 text-rose-400', icon: ThumbsDown },
          }[label];

          const IconComp = badgeConfig.icon;

          return (
            <div
              key={item.id || item.url}
              className="glass-card p-4 rounded-xl border border-white/5 hover:border-white/20 transition-all duration-200"
            >
              <div className="flex items-start justify-between gap-3 mb-1.5">
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs font-semibold text-slate-100 hover:text-blue-400 transition-colors line-clamp-2 flex items-center gap-1.5"
                >
                  <span>{item.title}</span>
                  <ExternalLink className="w-3 h-3 text-slate-400 flex-shrink-0" />
                </a>
                <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${badgeConfig.bg} flex items-center gap-1 flex-shrink-0`}>
                  <IconComp className="w-3 h-3" />
                  <span>{label}</span>
                </span>
              </div>

              {item.summary && (
                <p className="text-[11px] text-slate-400 line-clamp-2 mb-2">{item.summary}</p>
              )}

              <div className="flex items-center justify-between text-[10px] text-slate-400 pt-1 border-t border-white/5">
                <span>Fuente: <strong className="text-slate-300">{item.source}</strong></span>
                <span className="font-mono">Score: {score > 0 ? `+${score.toFixed(2)}` : score.toFixed(2)}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
