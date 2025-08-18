# 📊 Código Fonte - SEM Analysis

Este diretório contém todo o código fonte necessário para reproduzir as análises do projeto.

## 🐍 Python (`python/`)

### 📦 Core (`python/core/`)
Scripts fundamentais para preparação e consolidação dos dados:

- **`dados_preparacao.py`** - Limpeza e preparação inicial dos dados
- **`dados_reais_final.py`** - Processamento final dos dados reais  
- **`analise_final.py`** - Consolidação e síntese dos resultados

### 🔬 Analysis (`python/analysis/`)
Scripts de análises estatísticas e modelagem:

- **`analise_demografica.py`** - Análise do perfil socioeconômico
- **`analise_descritiva.py`** - Estatísticas descritivas completas
- **`analise_sem_principal.py`** - 🎯 **SEM PRINCIPAL** (r=0.896)
- **`modelos_sem.py`** - Modelos SEM avançados (7 construtos)
- **`machine_learning.py`** - Random Forest e K-Means Clustering
- **`analise_wtp.py`** - Análise Willingness-to-Pay

### 🎨 Visualization (`python/visualization/`)
Scripts para geração de gráficos e diagramas:

- **`diagramas_sem.py`** - Diagramas SEM completos
- **`diagramas_simples.py`** - Versões simplificadas
- **`diagramas_profissionais.py`** - Diagramas para publicação
- **`diagramas_storytelling.py`** - Diagramas narrativos

## 📊 R (`r/`)

Scripts R equivalentes aos Python, garantindo reprodutibilidade cruzada:

### 📦 Core (`r/core/`)
- **`dados_preparacao.R`** - Preparação de dados (equivalente Python)

### 🔬 Analysis (`r/analysis/`)
- **`analise_descritiva.R`** - Descritivas (equiv. Python)
- **`analise_sem_principal.R`** - 🎯 **SEM PRINCIPAL** (equiv. Python)
- **`modelos_sem_rigorosos.R`** - SEM rigorosos
- **`analise_completa.R`** - Análise completa com todas as variáveis

## 🚀 Como Executar

### Sequência Python Completa
```bash
# Core
cd python/core/
uv run dados_preparacao.py
uv run dados_reais_final.py

# Analysis  
cd ../analysis/
uv run analise_demografica.py
uv run analise_descritiva.py
uv run analise_sem_principal.py    # 🎯 Principal
uv run modelos_sem.py
uv run machine_learning.py
uv run analise_wtp.py

# Visualization
cd ../visualization/
uv run diagramas_sem.py
uv run diagramas_profissionais.py

# Consolidação
cd ../core/
uv run analise_final.py
```

### Sequência R Completa
```r
# Core
source("r/core/dados_preparacao.R")

# Analysis
source("r/analysis/analise_descritiva.R")
source("r/analysis/analise_sem_principal.R")    # 🎯 Principal
source("r/analysis/modelos_sem_rigorosos.R")
source("r/analysis/analise_completa.R")
```

## 📈 Outputs Gerados

Cada script gera outputs específicos em `../../results/`:

- **Imagens:** `../../results/images/`
- **Relatórios:** `../../results/reports/`
- **Dados processados:** `../../results/outputs/`

## 🔗 Dependências

### Python
- pandas, numpy, scipy
- matplotlib, seaborn
- scikit-learn
- semopy (SEM)
- factor-analyzer

### R  
- lavaan (SEM)
- ggplot2, dplyr
- psych, corrplot
- semPlot, semTools

## ⚠️ Importantes

1. **Ordem de execução:** Siga a sequência core → analysis → visualization
2. **Caminhos relativos:** Scripts usam caminhos relativos (`../../data/`, `../../results/`)
3. **Equivalência:** Scripts Python e R produzem os mesmos resultados
4. **Principal descoberta:** `analise_sem_principal.py/R` contém o resultado r=0.896
