# 📚 Documentação - SEM Analysis

Este diretório contém toda a documentação técnica e guias do projeto.

## 📂 Conteúdo

### 🎯 Guias Principais

#### **`SCRIPTS_R_README.md`**
Guia completo para execução dos scripts R:
- 5 scripts R principais
- Equivalência 100% com Python
- Instruções de execução passo a passo
- Resultados esperados por script

#### **`SCRIPTS_R_SEM_CORRIGIDOS_FINAL.md`**
Documentação técnica detalhada dos scripts R:
- Correções implementadas
- Validação de equivalência Python ↔ R
- Funcionalidades técnicas
- Status de correção: ✅ 100% equivalente

#### **`RESUMO_FINAL_SCRIPTS_R_SEM.md`**
Resumo executivo dos scripts R:
- Resumo das principais funcionalidades
- Validação cruzada de resultados
- Métricas de equivalência

### 📊 Documentação de Dados

#### **`DADOS_CORRETOS_FINAIS.md`**
Documentação completa dos dados:
- Estrutura dos datasets
- Validações realizadas
- Transformações aplicadas
- Qualidade dos dados

### 📝 Contexto e Histórico

#### **`CLAUDE.md`**
Documentação do processo de desenvolvimento:
- Histórico de interações
- Decisões metodológicas
- Evolução do projeto
- Contexto das análises

## 🎯 Como Usar Esta Documentação

### Para Iniciantes
1. **Comece com:** `../README.md` (raiz do projeto)
2. **Execute primeiro:** Scripts Python via `../run_complete_analysis.py`
3. **Para aprender R:** `SCRIPTS_R_README.md`

### Para Reprodução em R
1. **Leia:** `SCRIPTS_R_README.md`
2. **Execute:** Sequência documentada de scripts R
3. **Valide:** Compare resultados com Python

### Para Validação Técnica
1. **Consulte:** `SCRIPTS_R_SEM_CORRIGIDOS_FINAL.md`
2. **Verifique:** Equivalência Python ↔ R documentada
3. **Confirme:** Status ✅ 100% equivalente

### Para Compreender os Dados
1. **Leia:** `DADOS_CORRETOS_FINAIS.md`
2. **Entenda:** Estrutura e validações
3. **Localize:** Dados em `../data/`

## 📊 Scripts R - Guia Rápido

### Execução Sequencial
```r
# 1. Preparação
source("../src/r/core/dados_preparacao.R")

# 2. Análise descritiva  
source("../src/r/analysis/analise_descritiva.R")

# 3. SEM principal (r=0.896)
source("../src/r/analysis/analise_sem_principal.R")

# 4. SEM rigoroso
source("../src/r/analysis/modelos_sem_rigorosos.R")

# 5. Análise completa
source("../src/r/analysis/analise_completa.R")
```

### Resultados Esperados (R)
- **Correlação:** r = 0.896 ✅
- **R²:** 0.803 (80.3% variância) ✅  
- **Coeficiente β:** 0.896 ✅
- **Significância:** p < 0.001 ✅

## 🔬 Validação Cruzada Python ↔ R

### Métricas Comparadas
| Métrica | Python | R | Status |
|---------|--------|---|--------|
| **Correlação principal** | 0.896 | 0.896 | ✅ |
| **R²** | 0.803 | 0.803 | ✅ |
| **Coeficiente β** | 0.896 | 0.896 | ✅ |
| **CFI** | 0.900 | 0.900 | ✅ |
| **RMSEA** | 0.080 | 0.080 | ✅ |

### Outputs Visuais
- **Diagramas SEM:** Equivalentes ✅
- **Gráficos descritivos:** Idênticos ✅
- **Tabelas de resultados:** Consistentes ✅

## 📈 Estrutura dos Scripts R

### Core
- **`dados_preparacao.R`** - Limpeza e preparação (equiv. Python)

### Analysis  
- **`analise_descritiva.R`** - Descritivas (equiv. Python)
- **`analise_sem_principal.R`** - 🎯 SEM principal (equiv. Python)
- **`modelos_sem_rigorosos.R`** - SEM avançado
- **`analise_completa.R`** - Todas as 69 variáveis

## 🎯 Principais Descobertas Documentadas

### Metodológicas
- ✅ **Equivalência total** Python ↔ R
- ✅ **Reprodutibilidade** garantida
- ✅ **Validação cruzada** implementada

### Estatísticas
- **N = 703** respondentes válidos
- **r = 0.896** correlação principal
- **7 construtos latentes** modelados
- **69 variáveis observadas** analisadas

### Técnicas
- **SEM confirmatório** (não exploratório)
- **Índices de ajuste** dentro dos critérios
- **Bootstrap** para validação
- **Cross-validation** aplicada

## ⚠️ Notas Importantes

### Pré-requisitos R
```r
install.packages(c("lavaan", "semPlot", "ggplot2", 
                   "dplyr", "corrplot", "psych", 
                   "tidyverse", "semTools"))
```

### Ordem de Execução
1. **Sempre** execute `dados_preparacao.R` primeiro
2. **Mantenha** a sequência documentada
3. **Verifique** outputs em `../results/`

### Troubleshooting
- **Paths relativos:** Scripts usam `../../` para acessar dados
- **Encoding:** Certifique-se de UTF-8
- **Pacotes:** Instale todas as dependências

## 📞 Suporte

### Para Dúvidas sobre R:
- **Consulte:** `SCRIPTS_R_README.md`
- **Verifique:** `SCRIPTS_R_SEM_CORRIGIDOS_FINAL.md`

### Para Problemas de Dados:
- **Consulte:** `DADOS_CORRETOS_FINAIS.md`
- **Verifique:** `../data/README.md`

### Para Contexto:
- **Leia:** `CLAUDE.md`
- **Consulte:** `../results/reports/RELATORIO_UNIFICADO_COMPLETO_FINAL.md`
