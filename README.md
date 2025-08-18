# 🚀 SEM-Analysis: Análise de Estruturas de Equações (SEM) para Transporte Público

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![R](https://img.shields.io/badge/R-4.0+-blue.svg)](https://r-project.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Visão Geral

Este projeto contém uma análise completa de **Structural Equation Modeling (SEM)** aplicada ao estudo de comportamento dos usuários de transporte público e sistemas de recompensas. O objetivo é identificar fatores que influenciam a intenção comportamental dos usuários e propor estratégias baseadas em evidências para melhorar a utilização do transporte público urbano.

### 🎯 Descobertas Principais

- **Correlação r = 0.896** entre percepção de recompensas e intenção comportamental
- **R² = 80.3%** da variância na intenção comportamental é explicada por sistemas de recompensas
- **61.5%** dos usuários são mulheres, indicando maior dependência feminina
- **82.2%** dos usuários têm ensino médio ou superior (perfil mais educado que esperado)

## 🎯 GUIA COMPLETO PARA REPRODUZIR OS RESULTADOS

### 📊 **RELATÓRIO PRINCIPAL QUE SERÁ REPRODUZIDO:**
- **Arquivo:** `results/reports/Relatório.md` (1,986 linhas de análise completa)
- **Conteúdo:** Análise SEM com r=0.896, perfil socioeconômico, machine learning, clustering
- **Figuras:** 58 imagens e diagramas profissionais
- **Dados:** 703 respondentes, 69 variáveis, 7 construtos

---

## 🚀 PASSO A PASSO COMPLETO - DO ZERO AO RESULTADO

### **ETAPA 1: INSTALAÇÃO DAS FERRAMENTAS BÁSICAS**

#### 🐍 **1.1 Instalando Python (Obrigatório)**

**Windows:**
1. Vá para [python.org/downloads](https://python.org/downloads)
2. Clique em "Download Python 3.11.x" (versão mais recente)
3. ✅ **IMPORTANTE:** Marque "Add Python to PATH" durante a instalação
4. Execute o instalador e clique "Install Now"
5. Teste no CMD/PowerShell: `python --version`

**macOS:**
```bash
# Instalar via Homebrew (recomendado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### 📊 **1.2 Instalando R (Obrigatório)**

**Windows:**
1. Vá para [r-project.org](https://www.r-project.org/)
2. Clique "CRAN" → Escolha um mirror brasileiro
3. Clique "Download R for Windows" → "base" → "Download R"
4. Execute o instalador

**macOS:**
```bash
brew install r
```

**Linux:**
```bash
sudo apt install r-base r-base-dev
```

#### 💻 **1.3 Instalando uma IDE (Recomendado - VSCode)**

**VSCode (Recomendado para iniciantes):**
1. Vá para [code.visualstudio.com](https://code.visualstudio.com)
2. Baixe e instale para seu sistema operacional
3. Instale as extensões:
   - **Python** (Microsoft)
   - **R** (REditorSupport)
   - **Jupyter** (Microsoft)

**Alternativas:**
- **PyCharm Community** (Mais avançado para Python)
- **RStudio** (Especializado em R)

#### ⚡ **1.4 Instalando o Gerenciador UV (Obrigatório)**

**Windows (PowerShell como Administrador):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verificar instalação:**
```bash
uv --version
```

---

### **ETAPA 2: BAIXANDO E CONFIGURANDO O PROJETO**

#### 📥 **2.1 Baixando o Projeto**

**Opção A - Git (se tiver Git instalado):**
```bash
git clone [URL_DO_REPOSITORIO]
cd SEM-Analysis
```

**Opção B - Download Direto:**
1. Baixe o arquivo ZIP do projeto
2. Extraia para uma pasta (ex: `C:\Projetos\SEM-Analysis`)
3. Abra o terminal nessa pasta

#### 🔧 **2.2 Configurando o Ambiente Python**

```bash
# 1. Navegar para a pasta do projeto
cd SEM-Analysis

# 2. Instalar dependências automaticamente
uv sync

# 3. Verificar se funcionou
uv run python --version
```

#### 📊 **2.3 Configurando o R**

Abra o R ou RStudio e execute:

```r
# Instalar pacotes necessários
install.packages(c(
  "lavaan",        # SEM Analysis
  "semPlot",       # SEM Plots
  "ggplot2",       # Gráficos
  "dplyr",         # Manipulação de dados
  "corrplot",      # Matriz de correlação
  "psych",         # Análise psicométrica
  "tidyverse",     # Pacotes essenciais
  "semTools",      # Ferramentas SEM
  "VIM",           # Dados faltantes
  "mice",          # Imputação
  "readxl",        # Ler Excel
  "writexl"        # Escrever Excel
))
```

---

### **ETAPA 3: REPRODUZINDO OS RESULTADOS DO RELATÓRIO**

#### 🎯 **3.1 Execução Completa (Método Mais Fácil)**

```bash
# Este comando executa TUDO e reproduz o relatório completo
uv run run_complete_analysis.py
```

**⏱️ Tempo estimado:** 15-30 minutos
**📊 Resultado:** Gera todas as análises do `Relatório.md`

#### 🐍 **3.2 Execução Passo a Passo - Python**

**Passo 1: Preparação dos Dados**
```bash
cd src/python/core/
uv run dados_preparacao.py
uv run dados_reais_final.py
```

**Passo 2: Análises Estatísticas**
```bash
cd ../analysis/
uv run analise_demografica.py      # Perfil socioeconômico
uv run analise_descritiva.py       # Estatísticas descritivas  
uv run analise_sem_principal.py    # 🎯 SEM principal (r=0.896)
uv run modelos_sem.py              # Modelos SEM avançados
uv run machine_learning.py         # Random Forest & Clustering
```

**Passo 3: Visualizações**
```bash
cd ../visualization/
uv run diagramas_sem.py            # Diagramas SEM completos
uv run diagramas_profissionais.py  # Diagramas para publicação
```

**Passo 4: Consolidação**
```bash
cd ../core/
uv run analise_final.py            # Resultado final consolidado
```

#### 📊 **3.3 Execução Passo a Passo - R**

Abra o R/RStudio e execute:

```r
# 1. Preparação
source("src/r/core/dados_preparacao.R")

# 2. Análises principais
source("src/r/analysis/analise_descritiva.R")
source("src/r/analysis/analise_sem_principal.R")    # 🎯 SEM principal
source("src/r/analysis/modelos_sem_rigorosos.R")
source("src/r/analysis/analise_completa.R")
```

---

### **ETAPA 4: VERIFICANDO OS RESULTADOS**

#### 📋 **4.1 Relatórios Gerados**

Após a execução, verifique estes arquivos:

- ✅ **`results/reports/Relatório.md`** - Relatório principal (1,986 linhas)
- ✅ **`results/reports/RELATORIO_UNIFICADO_COMPLETO_FINAL.md`** - Relatório secundário
- ✅ **`results/images/`** - 58 imagens e diagramas
- ✅ **`results/outputs/`** - Dados e análises detalhadas

#### 🎯 **4.2 Principais Descobertas Esperadas**

Você deve encontrar estas descobertas no relatório:

- **Correlação r = 0.896** entre recompensas e intenção comportamental
- **R² = 80.3%** de variância explicada
- **61.5%** dos usuários são mulheres
- **82.2%** têm ensino médio ou superior
- **4 clusters** comportamentais identificados

#### 📊 **4.3 Principais Figuras Geradas**

- `diagrama_sem_real.png` - Diagrama SEM principal
- `correlacoes_dimensoes.png` - Mapa de correlações
- `dashboard_socioeconomico_completo.png` - Dashboard executivo

---

## 📁 Estrutura do Projeto

```
SEM-Analysis/
├── 📊 src/                          # Código fonte organizado
│   ├── python/                      # Scripts Python (50 arquivos)
│   │   ├── core/                    # 🔑 Módulos principais
│   │   │   ├── dados_preparacao.py  # Preparação e limpeza
│   │   │   ├── dados_reais_final.py # Processamento final
│   │   │   └── analise_final.py     # Consolidação
│   │   ├── analysis/                # 📈 Análises estatísticas
│   │   │   ├── analise_sem_principal.py   # 🎯 SEM r=0.896
│   │   │   ├── modelos_sem.py             # Modelos avançados
│   │   │   ├── machine_learning.py        # Random Forest
│   │   │   └── analise_wtp.py             # Willingness-to-Pay
│   │   └── visualization/           # 🎨 Visualizações
│   │       ├── diagramas_sem.py           # Diagramas SEM
│   │       └── diagramas_profissionais.py # Para publicação
│   └── r/                           # Scripts R equivalentes (13 arquivos)
│
├── 💾 data/                         # Dados organizados
│   ├── raw/csv_extraidos/           # 🎯 CSVs por construto (7 arquivos)
│   └── processed/                   # Dados processados (28 arquivos)
│
├── 📈 results/                      # Todos os resultados
│   ├── reports/                     # 📋 Relatórios principais
│   │   └── Relatório.md            # 🎯 RELATÓRIO PRINCIPAL
│   ├── images/                      # 🖼️ 58 imagens organizadas
│   └── outputs/                     # 📊 Outputs detalhados
│
├── 📚 docs/                         # Documentação completa
├── ⚙️ config/                       # Configurações
│   ├── requirements.txt            # Dependências Python
│   └── pyproject.toml              # Configuração UV
│
└── 🏃‍♂️ run_complete_analysis.py     # 🎯 SCRIPT PRINCIPAL
```

---

## ❗ SOLUÇÃO DE PROBLEMAS COMUNS

### 🐍 **Problemas com Python**

**"Python não foi encontrado":**
```bash
# Windows: Reinstalar Python marcando "Add to PATH"
# Ou usar Python via Windows Store
python --version
```

**"uv não foi encontrado":**
```bash
# Reiniciar terminal após instalação
# Ou instalar manualmente:
pip install uv
```

**"Erro de permissão":**
```bash
# Windows: Executar PowerShell como Administrador
# Linux/Mac: Usar sudo apenas se necessário
```

### 📊 **Problemas com R**

**"Pacote não pode ser instalado":**
```r
# Tentar com mirror diferente
install.packages("lavaan", repos="https://cran.rstudio.com/")

# Ou instalar dependências do sistema (Linux):
# sudo apt-get install libcurl4-openssl-dev libssl-dev libxml2-dev
```

**"Erro de compilação":**
```r
# Instalar versão binária
install.packages("lavaan", type="binary")
```

### 💻 **Problemas Gerais**

**"Erro de memória":**
- Feche outras aplicações
- Execute os scripts um por vez ao invés do script completo

**"Dados não encontrados":**
- Verifique se está na pasta correta do projeto
- Execute `ls` (Linux/Mac) ou `dir` (Windows) para ver os arquivos

**"Demora muito para executar":**
- Normal: O script completo pode levar 15-30 minutos
- Execute por partes para testar

---

## 📊 PRINCIPAIS RESULTADOS ESPERADOS

### 🎯 **Modelo SEM Principal**
- **Correlação:** r = 0.896 (Percepção ↔ Intenção Comportamental)
- **R² = 80.3%** da variância explicada por recompensas
- **Coeficiente β = 0.896** (efeito dominante)
- **Significância:** p < 0.001 (altamente significativo)

### 👥 **Perfil dos Usuários (N=703)**
- **Gênero:** 61.5% mulheres, 38.3% homens
- **Educação:** 82.2% com ensino médio ou superior
- **Etnia:** 59.2% negros, 40.0% brancos
- **Dependência:** 70.3% usam transporte público como principal

### 🎁 **Sistema de Recompensas (Preferências)**
1. **Uso ilimitado** (4.57/5.0) - Mais desejado
2. **Descontos comerciais** (4.52/5.0)
3. **Passagens gratuitas** (4.51/5.0)
4. **Créditos diretos** (4.48/5.0)

### 🤖 **Machine Learning (4 Clusters)**
1. **"Satisfeitos Engajados"** (28.0%) - Base leal
2. **"Críticos Esperançosos"** (24.6%) - Alto potencial
3. **"Resignados Céticos"** (22.5%) - Desafiadores
4. **"Neutros Potenciais"** (24.9%) - Influenciáveis

---

## 📋 ARQUIVOS PRINCIPAIS GERADOS

### 📊 **Relatórios**
- **`results/reports/Relatório.md`** - 📋 PRINCIPAL (1,986 linhas)
- **`results/reports/RELATORIO_UNIFICADO_COMPLETO_FINAL.md`** - Secundário
- **Formatos:** Markdown, PDF, DOCX disponíveis

### 🖼️ **Figuras Principais (58 total)**
- **`diagrama_sem_real.png`** - Diagrama SEM principal (r=0.896)
- **`correlacoes_dimensoes.png`** - Mapa de correlações completo
- **`dashboard_socioeconomico_completo.png`** - Dashboard executivo
- **`modelo_sem_global.png`** - Modelo global com 7 construtos

### 📈 **Dados Processados**
- **`results/outputs/resultados_sem_fixed/`** - Resultados SEM corrigidos
- **`results/outputs/resultados_wtp/`** - Análises Willingness-to-Pay
- **`results/outputs/visualizacoes/`** - Todas as visualizações por categoria

---

## 🔬 METODOLOGIA CIENTÍFICA

### **Análise SEM (Structural Equation Modeling)**
- **Software:** Python (semopy) + R (lavaan)
- **Construtos:** 7 variáveis latentes
- **Indicadores:** 69 variáveis observadas
- **Método:** Máxima verossimilhança com bootstrap
- **Validação:** CFI, TLI, RMSEA, SRMR

### **Machine Learning**
- **Random Forest:** 86.7% de acurácia preditiva
- **K-Means Clustering:** 4 segmentos comportamentais
- **PCA:** Redução dimensional (62.8% variância)

### **Análise Descritiva**
- **Amostra:** N = 703 respondentes válidos
- **Escalas:** Likert 5 pontos
- **Testes:** Qui-quadrado, ANOVA, correlações

---

## 🎯 COMO USAR OS RESULTADOS

### **Para Pesquisadores:**
1. **Consulte:** `results/reports/Relatório.md` para metodologia completa
2. **Analise:** Diagramas SEM em `results/images/`
3. **Replique:** Use os scripts em `src/python/` e `src/r/`

### **Para Gestores Públicos:**
1. **Leia:** Seção "Insights Estratégicos" do relatório
2. **Foque:** Correlação r=0.896 (recompensas → intenção)
3. **Implemente:** Sistemas de recompensas como prioridade

### **Para Desenvolvedores:**
1. **Execute:** `run_complete_analysis.py` para reprodução completa
2. **Modifique:** Scripts em `src/` para novas análises
3. **Valide:** Use `final_verification_report.py` para verificação

---

## 📞 SUPORTE E RECURSOS ADICIONAIS

### 📚 **Documentação Técnica**
- **`docs/SCRIPTS_R_SEM_CORRIGIDOS_FINAL.md`** - Metodologia SEM em R
- **`docs/DADOS_CORRETOS_FINAIS.md`** - Estrutura dos dados
- **`docs/PROJETO_REORGANIZADO_FINAL.md`** - Visão geral da organização

### 🔍 **Para Troubleshooting:**
1. **Execute:** `python final_verification_report.py` para diagnóstico
2. **Verifique:** Logs em `results/outputs/` 
3. **Consulte:** Seção "Solução de Problemas" acima

### 🤝 **Contribuições**
Este projeto segue as melhores práticas de engenharia de software:
- ✅ **Estrutura modular** por funcionalidade
- ✅ **Reprodutibilidade** garantida (Python + R)
- ✅ **Documentação** completa e didática
- ✅ **Validação** automatizada de resultados

---

## 📄 LICENÇA E CITAÇÃO

**Licença:** MIT License - Veja [LICENSE](LICENSE) para detalhes

**Para citar este trabalho:**
```
SEM-Analysis: Análise de Estruturas de Equações para Transporte Público
Correlação r=0.896 entre percepção de recompensas e intenção comportamental
N=703 respondentes, 69 variáveis, 7 construtos latentes
```

---

## 🚀 INÍCIO RÁPIDO

### **Para Reprodução Completa (Recomendado):**
```bash
# 1. Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clonar projeto
cd SEM-Analysis

# 3. Configurar ambiente
uv sync

# 4. Reproduzir TUDO
uv run run_complete_analysis.py
```

### **Para Verificar Resultados:**
```bash
# Verificar se tudo foi gerado corretamente
uv run final_verification_report.py
```

### **Para Consultar Resultados:**
1. 📋 **Relatório Principal:** `results/reports/Relatório.md`
2. 🖼️ **Figuras:** Pasta `results/images/`
3. 📊 **Dados:** Pasta `results/outputs/`

---

**🎯 OBJETIVO:** Reproduzir 100% dos resultados científicos do projeto SEM-Analysis

**📋 RESULTADO:** Relatório completo com r=0.896 e 58 visualizações profissionais

**⏱️ TEMPO:** 15-30 minutos para execução completa
