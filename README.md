# 🧠 HITL Lab

**Multi-cloud AI demos · Cobertura ISO 27001 / 42001 / 22301**

*Por Adrián Álvarez Martínez · [hitl.mx](https://hitl.mx)*

---

## ⚡ Arranque en 3 comandos

```bash
# 1. Clona o descarga el proyecto
git clone https://github.com/hitlmx/hitl-lab
cd hitl-lab

# 2. Configura tu proveedor AI
cp .env.example .env
# Edita .env y pon tu API key del proveedor que quieras usar

# 3. Levanta el lab
docker-compose up
```

Abre tu browser en: **http://localhost:8888**
Token: `hitllab2026`

---

## 🌩️ Montaje en nubes (5 minutos)

### IBM TechZone
```bash
# En Watson Studio — abre una terminal y ejecuta:
git clone https://github.com/hitlmx/hitl-lab
cd hitl-lab && pip install -r requirements.txt
# Abre notebooks/ desde JupyterLab
```

### AWS SageMaker Studio Lab
```bash
# En el terminal de SageMaker:
git clone https://github.com/hitlmx/hitl-lab
cd hitl-lab && pip install -r requirements.txt
```

### Google Vertex AI Workbench
```bash
git clone https://github.com/hitlmx/hitl-lab
cd hitl-lab && pip install -r requirements.txt
```

### Local (sin Docker)
```bash
pip install -r requirements.txt
cp .env.example .env  # edita con tu API key
jupyter lab --notebook-dir=notebooks/
```

---

## 🗂️ Notebooks disponibles

| Notebook | Escenario | ISO cubierta |
|----------|-----------|--------------|
| `01_mary_credito.ipynb` | La Mary pide un microcrédito | 27001 · 42001 · 22301 |
| `06_copo_listas.ipynb` | CoPo detecta listas negras | 27001 · 42001 |
| `10_pipeline_modelo.ipynb` | Pipeline de entrenamiento AI | 42001 |

---

## 🔄 Cambiar de nube

Edita una sola línea en `.env`:

```bash
PROVIDER=claude     # Anthropic Claude
PROVIDER=watsonx    # IBM WatsonX (TechZone)
PROVIDER=bedrock    # AWS Bedrock (SageMaker)
PROVIDER=gemini     # Google Gemini (Vertex)
PROVIDER=openai     # OpenAI
```

El notebook no cambia. Solo cambia el modelo que responde.

---

## 📋 ISO Controls

Cada notebook incluye:

- **ISO 27001** — Datos sintéticos, secrets en variables de entorno, sin PII real
- **ISO 42001** — Prompts versionados, audit log automático, revisión humana (HITL)
- **ISO 22301** — Fallback automático si el modelo no responde, RTO documentado

---

## 🏗️ Estructura del proyecto

```
hitl-lab/
├── docker-compose.yml     ← levanta todo
├── Dockerfile
├── requirements.txt
├── .env.example           ← copia como .env
├── adapters/
│   ├── __init__.py
│   └── base.py            ← adapter multi-nube
├── notebooks/
│   └── 01_mary_credito.ipynb
├── iso_controls/
│   ├── 27001_checklist.md
│   ├── 42001_checklist.md
│   └── 22301_checklist.md
└── data/
    ├── synthetic/         ← datos de prueba
    └── audit.jsonl        ← generado automáticamente
```

---

*HITL Lab es un proyecto de [HITL — Human In The Loop](https://hitl.mx)*
*Skills-Depot · IBM Partner · AWS Partner*









@"
# HITL Lab

**Multi-cloud AI demos · ISO 27001 / 42001 / 22301**

*Adrian Alvarez Martinez · [hitl.mx](https://hitl.mx) · IBM Partner · AWS Partner*

---

## Arranque en 3 comandos

```bash
git clone https://github.com/sdadrianalvarez/hitl-lab
cd hitl-lab
cp .env.example .env   # agrega tu API key
docker-compose up
```

Abre: http://localhost:8888 · Token: hitllab2026

---

## Notebooks

| # | Escenario | Tecnicas | ISO |
|---|-----------|----------|-----|
| 01 | La Mary pide microcredito | Chain of Thought, HITL review | 27001 · 42001 · 22301 |
| 06 | CoPo detecta listas negras | Multi-source reasoning, scorecard | 27001 · 42001 |
| 10 | Pipeline RAG y evaluacion | RAG, dataset sintetico, rating AI | 42001 · 22301 |

---

## Cambia de nube en 1 linea

```bash
PROVIDER=claude     # Anthropic
PROVIDER=watsonx    # IBM TechZone
PROVIDER=bedrock    # AWS SageMaker
PROVIDER=gemini     # Google Vertex AI
PROVIDER=openai     # OpenAI
```

---

## Montaje en nubes (5 minutos)

### IBM TechZone / Watson Studio
```bash
git clone https://github.com/sdadrianalvarez/hitl-lab
pip install -r requirements.txt
# Abre notebooks/ desde JupyterLab
```

### AWS SageMaker Studio Lab
```bash
git clone https://github.com/sdadrianalvarez/hitl-lab
pip install -r requirements.txt
```

### Google Vertex AI Workbench
```bash
git clone https://github.com/sdadrianalvarez/hitl-lab
pip install -r requirements.txt
```

---

## Estructura

hitl-lab/

├── adapters/

│   ├── init.py

│   └── base.py              # adapter multi-nube con ISO controls

├── notebooks/

│   ├── 01_mary_credito.ipynb

│   ├── 06_copo_listas_negras.ipynb

│   └── 10_pipeline_modelo.ipynb

├── iso_controls/

│   ├── 27001_checklist.md

│   ├── 42001_checklist.md

│   └── 22301_checklist.md

├── docker-compose.yml

├── Dockerfile

├── requirements.txt

└── .env.example



---

*HITL Lab es un proyecto de [HITL — Human In The Loop](https://hitl.mx)*
"@ | Out-File -Encoding utf8 README.md

git add README.md
git commit -m "docs: update README with all notebooks and cloud setup"
git push