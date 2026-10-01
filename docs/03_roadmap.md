# Roadmap de Desarrollo por Fases

## Fase 1: Arquitectura Base, Entorno y Modelado ORM (Django + Database)
- [ ] **1.1. Inicialización del proyecto Backend Django**
  - Configurar entorno virtual (`venv` / `poetry`), instalar `Django`, `djangorestframework`, `django-cors-headers`, `psycopg2` / `sqlite3`.
- [ ] **1.2. Definición del Modelo de Datos ORM (`core` app)**
  - `Asset` (Ticker, Name, AssetType: STOCK/CRYPTO, IsActive).
  - `NewsArticle` (Title, Summary, Content, Source, URL, PublishedAt, Asset FK).
  - `NewsSentiment` (Article OneToOne, SentimentLabel: POS/NEU/NEG, Score [-1 a 1], ImpactScore).
  - `MarketData` (Asset FK, Timestamp, Open, High, Low, Close, Volume, RSI, MACD, SMA20, SMA50, Volatility).
  - `Prediction` (Asset FK, Timestamp, TargetTimestamp, PredictedClass: SUBE/ESTABLE/BAJA, Probabilities JSON, ModelVersion).
  - `ModelMetrics` (ModelVersion, TrainedAt, Accuracy, F1Score, ConfusionMatrix JSON).
- [ ] **1.3. Migraciones y Semilla de Datos Iniciales**
  - Crear e integrar scripts de *seeding* inicial para activos principales (ej. `AAPL`, `TSLA`, `BTC-USD`, `ETH-USD`).

---

## Fase 2: Ingesta de Noticias (Scrapy) & Engine NLP
- [ ] **2.1. Scrapy Project Setup & Spiders**
  - Estructurar el proyecto Scrapy para extracción de sitios de noticias financieras.
  - Diseñar spiders con selectores CSS/XPath robustos y manejo de User-Agents y pipelines.
- [ ] **2.2. Entity Matcher (Reconocimiento de Activos)**
  - Implementar pipeline de Scrapy/Python para mapear titulares/texto a activos específicos (`Asset`).
- [ ] **2.3. Pipeline NLP de Sentimiento**
  - Integrar módulo de NLP (ej. `VADER` / `FinBERT` / `TextBlob`) para calcular polaridad y score numérico.
  - Guardar automáticamente en las tablas `NewsArticle` y `NewsSentiment`.

---

## Fase 3: Ingesta de Mercado, Indicadores Técnicos & Data Pipeline
- [ ] **3.1. Extractor de Precios de Mercado**
  - Implementar script/servicio para descargar datos OHLCV históricos y en tiempo real usando `yfinance` o APIs de exchanges.
- [ ] **3.2. Calculador de Indicadores Técnicos**
  - Desarrollar módulo `technical_indicators.py` para calcular RSI, MACD, Medias Móviles y Volatilidad usando `pandas`/`pandas_ta`.
  - Guardar registros estructurados en `MarketData`.
- [ ] **3.3. Construcción del Feature Store (Dataset Aligned)**
  - Implementar script para sincronizar temporalmente la agregación de sentimiento diario/horario de noticias con los indicadores OHLCV.
  - **Mecanismo Anti-Data Leakage:** Garantizar que la muestra en $T$ solo consulte noticias publicadas en $\le T$.

---

## Fase 4: Core de Machine Learning (Entrenamiento, Validación e Inferencia)
- [ ] **4.1. Preprocesamiento de Features y Definición de Target**
  - Generar la variable objetivo $Y_{t+k}$ en 3 clases (`SUBE`: cambio $> +\epsilon$, `BAJA`: cambio $< -\epsilon$, `ESTABLE`: dentro de $[-\epsilon, +\epsilon]$).
- [ ] **4.2. Entrenamiento y Validación de Modelos**
  - Entrenar clasificadores (`RandomForestClassifier`, `XGBClassifier`, `LogisticRegression`).
  - Utilizar `TimeSeriesSplit` para evaluación realista (Accuracy, Precision, Recall, F1-Score).
  - Serializar el modelo entrenado (`.joblib` / `.pkl`).
- [ ] **4.3. Pipeline de Inferencia Automática**
  - Generar script de inferencia diaria que consuma los últimos datos, aplique el modelo guardado y almacene el resultado en `Prediction`.

---

## Fase 5: API REST Backend (Django DRF)
- [ ] **5.1. Serializadores y ViewSets de DRF**
  - Exponer endpoints `/api/v1/assets/`, `/api/v1/news/`, `/api/v1/market-data/`, `/api/v1/predictions/latest/` y `/api/v1/predictions/history/`.
- [ ] **5.2. Filtros, Paginación y CORS**
  - Configurar filtrado por Ticker/Asset, rango de fechas y paginación.
  - Habilitar CORS para permitir conexión con Next.js.

---

## Fase 6: Dashboard Web Frontend (Next.js & UI)
- [ ] **6.1. Configuración de Next.js y Design System**
  - Inicializar aplicación Next.js React en Frontend.
  - Diseñar interfaz con estética moderna, tema oscuro/elegante, paleta de colores financieros sofisticados.
- [ ] **6.2. Componentes del Dashboard**
  - *Header & Asset Selector Bar*: Selección del activo activo.
  - *Financial Price Chart Component*: Gráfico dinámico de serie de precios e indicadores.
  - *Sentiment Gauge & News Feed Component*: Indicador de sentimiento del activo y feed de titulares recientes con badge de polaridad.
  - *Prediction Card Component*: Visualizador de señal (`SUBE` / `ESTABLE` / `BAJA`) con barras de probabilidad ($P_{SUBE}, P_{ESTABLE}, P_{BAJA}$).
  - *Model Accuracy & Historical Performance Component*: Medidor de rendimiento histórico del modelo.

---

## Fase 7: Integración, Pruebas y Documentación
- [ ] **7.1. Pruebas Unitarias e Integración (`/tests`)**
  - Pruebas de modelos Django, scrapers, calculadores de indicadores, evaluadores de ML y endpoints API.
- [ ] **7.2. Verificación End-to-End**
  - Ejecutar flujo completo: Ingesta $\to$ NLP $\to$ Indicadores $\to$ Dataset ML $\to$ Inferencia $\to$ API $\to$ Dashboard Frontend.
- [ ] **7.3. Documentación Final del Sistema**