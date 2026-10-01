# Arquitectura del Sistema y Diseño Tecnológico

## 1. Visión General de la Arquitectura

El sistema adopta una **arquitectura por capas desacopladas**, compuesta por pipelines de ingesta (Scraping + APIs de Mercado), un motor de procesamiento NLP, un módulo de Feature Engineering & Machine Learning, una capa backend en **Django REST Framework** con **PostgreSQL** y una capa frontend en **Next.js**.

```mermaid
graph TD
    subgraph Ingestion_Layer["Capa de Ingesta & Extracción"]
        ScrapySpiders["Scrapy Spiders<br/>(Noticias Financieras)"]
        MarketAPI["Market Data Fetcher<br/>(yfinance / AlphaVantage / Binance)"]
    end

    subgraph Processing_Layer["Capa de NLP & Feature Engineering"]
        NLP_Engine["NLP Engine<br/>(VADER / TextBlob / FinBERT / Spacy)"]
        TechIndicators["Calculador de Indicadores<br/>(RSI, MACD, SMA, Volatilidad)"]
    end

    subgraph Data_Storage["Capa de Almacenamiento (Database)"]
        PostgreSQL[("PostgreSQL Database<br/>Django ORM")]
    end

    subgraph ML_Engine["Capa de Machine Learning"]
        DatasetBuilder["Dataset Builder<br/>(Alignment & Anti Data-Leakage)"]
        ML_Model["ML Predictor<br/>(RandomForest / XGBoost)"]
    end

    subgraph Backend_Layer["Capa Backend (API REST)"]
        DjangoDRF["Django REST Framework<br/>API Endpoints"]
    end

    subgraph Frontend_Layer["Capa Frontend (Dashboard Web)"]
        NextJS["Next.js / React Dashboard<br/>(Charts, Feeds & Signals)"]
    end

    ScrapySpiders -->|Noticias brutas| NLP_Engine
    NLP_Engine -->|Noticias + Sentimiento| PostgreSQL
    
    MarketAPI -->|Datos OHLCV| TechIndicators
    TechIndicators -->|Precios + Indicadores| PostgreSQL
    
    PostgreSQL -->|Sentimientos + Indicadores| DatasetBuilder
    DatasetBuilder -->|Dataset de Entrenar/Inferir| ML_Model
    ML_Model -->|Predicciones (SUBE/ESTABLE/BAJA)| PostgreSQL

    PostgreSQL <--> DjangoDRF
    DjangoDRF <-->|JSON REST HTTP| NextJS
```

---

## 2. Descripción de Capas

### 2.1. Capa de Extracción e Ingesta (Scrapy + APIs)
- **Scrapy Spiders:** Módulos encargados de rastrear sitios web de noticias financieras. Extraen título, cuerpo, fecha/hora, fuente y URL.
- **Market Data Collectors:** Integradores que consumen datos históricos y recientes de precios OHLCV y volumen desde APIs financieras confiables.

### 2.2. Capa de Procesamiento NLP e Indicadores Técnicos
- **NLP Sentiment Engine:** Normaliza texto, identifica los activos mencionados (Tickers / Nombres) y asigna un puntaje de sentimiento (Score $[-1.0, +1.0]$) y etiquetas de polaridad (Positivo, Neutro, Negativo).
- **Technical Analysis Module:** Utiliza librerías como `pandas` y `pandas_ta` / `TA-Lib` para calcular:
  - **RSI (14):** Relative Strength Index
  - **SMA / EMA (20, 50):** Medias Móviles Simples y Exponenciales
  - **MACD:** Moving Average Convergence Divergence
  - **Bollinger Bands:** Banda Superior, Media e Inferior
  - **Volatilidad Histórica:** Desviación estándar de los retornos

### 2.3. Capa de Almacenamiento (PostgreSQL & Django ORM)
Modelos ORM principales:
1. `Asset`: Metadatos del activo (Ticker, Nombre, Tipo: Acción/Crypto, Estado activo).
2. `NewsArticle`: Noticia extraída (Título, Resumen, Fuente, URL, Fecha de publicación, Ticker asociado).
3. `NewsSentiment`: Resultados del NLP (Score de sentimiento, Impacto estimado, Confianza).
4. `MarketData`: Serie temporal OHLCV (Fecha/Hora, Open, High, Low, Close, Volume, Indicadores calculados).
5. `Prediction`: Predicciones generadas (Asset, Fecha objetivo, Clase elegida: `SUBE`/`ESTABLE`/`BAJA`, Probabilidades $[P_{SUBE}, P_{ESTABLE}, P_{BAJA}]$, Versión del Modelo).
6. `ModelEvaluation`: Métricas de evaluación (Accuracy, F1-Score, Matriz de Confusión, Fecha de entrenamiento).

### 2.4. Capa de Machine Learning (ML Pipeline)
- **Data Merger & Prevención de Data Leakage:** Cruza las noticias agregadas en una ventana de tiempo $T$ con los indicadores de mercado acumulados hasta $T$, garantizando que no se usen precios futuros para predecir $T+k$.
- **Model Training & Evaluation:** Utiliza modelos de clasificación (Random Forest, XGBoost, Logistic Regression) evaluados mediante validación temporal (`TimeSeriesSplit`).
- **Inferencia:** Produce el vector de probabilidades y la clase final predicha para cada activo.

### 2.5. Capa Backend (Django REST Framework)
- **Endpoints REST API:**
  - `GET /api/v1/assets/`: Lista de activos monitoreados.
  - `GET /api/v1/news/?asset={ticker}`: Feed de noticias con sentimiento.
  - `GET /api/v1/market-data/?asset={ticker}`: Serie de tiempo e indicadores.
  - `GET /api/v1/predictions/latest/`: Últimas predicciones por activo.
  - `GET /api/v1/predictions/history/?asset={ticker}`: Histórico de predicciones vs resultado real.
  - `POST /api/v1/ml/train/`: Trigger de re-entrenamiento (admin/background).

### 2.6. Capa Frontend (Dashboard Web Next.js)
- **Next.js React Framework:** Renderizado dinámico y optimizado.
- **Componentes Clave:**
  - *Asset Selector & Header Card:* Resumen del activo seleccionado.
  - *Price & Technical Indicator Chart:* Gráfico interactivo de línea/velas con superposición de indicadores.
  - *Sentiment Gauge & News Feed:* Medidor visual de sentimiento de mercado y lista de noticias relevantes etiquetadas.
  - *Prediction Signal Badge:* Tarjeta destacada con la clase predicha (`SUBE`, `ESTABLE`, `BAJA`) y barras de porcentaje de probabilidad.
  - *Accuracy & Historical Backtest Widget:* Gráfico de efectividad del modelo a lo largo del tiempo.