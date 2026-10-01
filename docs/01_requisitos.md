# Especificación de Requisitos y Alcance del Sistema

## 1. Contexto y Definición del Problema
Los mercados financieros (acciones) y de criptomonedas se caracterizan por una alta volatilidad impulsada tanto por datos cuantitativos (precios históricos, volumen) como por datos cualitativos (noticias, eventos macroeconómicos, declaraciones corporativas). 

Analizar manualmente ambas fuentes de información es ineficiente y propenso a sesgos humanos. Se propone desarrollar un **Sistema Inteligente para la Predicción del Comportamiento de Activos Financieros mediante Análisis de Noticias y Machine Learning**, capaz de automatizar la ingesta de noticias, el análisis de sentimiento NLP, el procesamiento de indicadores de mercado y la generación de predicciones probabilísticas.

---

## 2. Objetivo General
Desarrollar una plataforma web completa que recopile noticias financieras mediante scraping, las procese con técnicas de NLP para extraer sentimiento e impacto, las combine con indicadores técnicos y precios históricos del mercado, y entrene modelos de Machine Learning para predecir la tendencia probabilística (`SUBE`, `ESTABLE`, `BAJA`) de activos seleccionados, mostrando los resultados en un Dashboard web interactivo.

---

## 3. Alcance del Sistema

### 3.1. Extracción e Ingesta de Noticias
- **Recolección Automática:** Implementación de *spiders* en **Scrapy** para la extracción periódica de titular, cuerpo, fecha de publicación, fuente y URL de noticias financieras.
- **Mapeo e Identificación de Activos:** Identificación y vinculación automática de noticias a activos financieros específicos (ej. `AAPL`, `TSLA`, `BTC`, `ETH`) mediante coincidencia de entidades y palabras clave (Ticker / Named Entity Recognition).

### 3.2. Procesamiento de Lenguaje Natural (NLP)
- **Análisis de Sentimiento:** Clasificación del tono de cada noticia en categorías (Positivo, Neutro, Negativo) y generación de un puntaje numérico continuo de sentimiento (score de -1.0 a +1.0).
- **Estimación de Impacto:** Ponderación del impacto probable de la noticia según su relevancia o fuente.

### 3.3. Ingesta de Datos Financieros e Indicadores
- **Datos Históricos del Mercado:** Obtención de datos OHLCV (Open, High, Low, Close, Volume) a través de APIs de mercado (ej. `yfinance`, Alpha Vantage, Binance).
- **Cálculo de Indicadores Técnicos:** Generación de indicadores clave como RSI (Índice de Fuerza Relativa), Medias Móviles (SMA 20/50, EMA), MACD, Bandas de Bollinger y Volatilidad.

### 3.4. Motor de Machine Learning y Data Pipeline
- **Construcción del Dataset:** Alineación temporal precisa entre publicaciones de noticias (agregado de sentimientos) e intervalos de precios históricos de mercado.
- **Prevención de Data Leakage:** Garantía estricta de ordenamiento temporal (Time-Series Split) para asegurar que las predicciones para el tiempo $T$ utilicen únicamente información generada en $t \le T$.
- **Modelos Predictivos:** Entrenamiento y evaluación de clasificadores supervised (ej. Random Forest, XGBoost, Logistic Regression) para predecir la etiqueta de mercado en la siguiente ventana de tiempo ($T+k$): `SUBE`, `ESTABLE`, `BAJA`.
- **Inferencia y Probabilidades:** Emisión de probabilidades asignadas a cada categoría de clase.

### 3.5. Backend API y Dashboard Frontend
- **Backend REST API (Django DRF):** Endpoints para consultar activos, feeds de noticias procesadas, indicadores de mercado, historial de predicciones y métricas del modelo.
- **Dashboard Web (Next.js):** Interfaz gráfica intuitiva con visualización de gráficos de precios, medidores de sentimiento, señales probabilísticas de predicción y rendimiento histórico del modelo.

---

## 4. Requisitos Funcionales (RF)

| ID | Requisito Funcional | Descripción |
|---|---|---|
| **RF-01** | Ingesta de Noticias | El sistema debe ejecutar scrapers automáticos para obtener noticias financieras de portales seleccionados. |
| **RF-02** | Etiquetado de Activo | El sistema debe vincular cada noticia extraída a uno o más activos de la lista administrada. |
| **RF-03** | Análisis NLP | El sistema debe calcular el sentimiento (score de -1 a 1) y clasificar el impacto de cada noticia. |
| **RF-04** | Descarga de Datos OHLCV | El sistema debe sincronizar diariamente o por periodo los precios y volumen de los activos configurados. |
| **RF-05** | Cálculo de Indicadores | El sistema debe calcular RSI, MACD, Medias Móviles y Volatilidad sobre la serie de precios. |
| **RF-06** | Generación de Dataset | El sistema debe cruzar en ventanas temporales los sentimientos NLP con las métricas del mercado. |
| **RF-07** | Entrenamiento y Validación | El sistema debe permitir entrenar y evaluar modelos de ML sin incurrir en Data Leakage. |
| **RF-08** | Inferencia Predictiva | El sistema debe generar predicciones probabilísticas de la clase (`SUBE`, `ESTABLE`, `BAJA`) para un activo dado. |
| **RF-09** | API REST | El sistema debe exponer endpoints HTTP JSON protegidos/estructurados para el Dashboard. |
| **RF-10** | Visualización en Dashboard | El Dashboard debe mostrar gráficos de precio/volumen, lista de noticias con sentimiento y la predicción probabilística actual. |
| **RF-11** | Historial y Métricas | El sistema debe registrar las predicciones pasadas y contrastarlas con el resultado real del mercado para calcular el acierto (Accuracy/F1-Score). |

---

## 5. Requisitos No Funcionales (RNF)

- **RNF-01 (Tolerancia a Fallos y Scraping):** El pipeline de ingesta debe gestionar reintentos, time-outs y cambios estructurales menores en los sitios web sin detener la aplicación principal.
- **RNF-02 (Rigor Metodológico de ML):** La división de conjuntos de datos de entrenamiento y prueba debe basarse estrictamente en series temporales para evitar *Data Leakage*.
- **RNF-03 (Modularidad y Desacoplamiento):** Los módulos de Scraping, NLP, Mercado, ML Engine y Web Dashboard deben estar claramente desacoplados en sus capas correspondientes.
- **RNF-04 (Rendimiento de la API):** Los endpoints REST deben responder en menos de 500 ms para consultas estándar del Dashboard.
- **RNF-05 (Estética y UX del Frontend):** El dashboard debe contar con una interfaz moderna, responsiva, con visualización de datos dinámica (charts) y un diseño profesional de nivel producción.

---

## 6. Limitaciones Reconocidas del Proyecto

1. **Carácter Académico y Experimental:** El sistema se desarrolla con fines académicos/experimentales; **no** ejecuta órdenes reales de trading ni maneja dinero real.
2. **Naturaleza Estocástica del Mercado:** Ningún modelo predictivo garantiza rentabilidad o aciertos del 100% debido a factores exógenos e impredecibles del mercado.
3. **Limitaciones de Scraping y APIs externas:** Dependencia de la estabilidad de fuentes públicas web y límites de cuota (rate limits) de las APIs financieras.
4. **Desafíos de NLP Financiero:** El procesamiento de noticias puede presentar ambigüedades en ironías, jerga financiera específica o noticias duplicadas entre agencias.
5. **Alcance Acotado de Activos:** Inicialmente el sistema trabajará sobre un portafolio acotado de activos representativos (acciones tecnológicas líderes y criptomonedas principales) para garantizar control metodológico.