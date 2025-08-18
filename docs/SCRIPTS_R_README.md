# 📊 SCRIPTS R - ANÁLISE DE TRANSPORTE PÚBLICO

## 🎯 **OBJETIVO**

Estes 5 scripts R são versões **totalmente fiéis** dos scripts Python originais que geraram o `RELATORIO_UNIFICADO_COMPLETO_FINAL.md`. Eles reproduzem **exatamente os mesmos resultados**, análises estatísticas e visualizações.

---

## 📂 **ESTRUTURA DOS SCRIPTS**

### **1. `dados_reais_final.R`**
**🔍 FUNÇÃO:** Análise demográfica completa e correlações básicas

**📈 RESULTADOS REPRODUZIDOS:**
- Total: 703 respondentes  
- Gênero: 61.5% mulheres
- Raça: 59.2% negros
- Médias de qualidade (1.65) e percepção (4.56)
- **Correlação principal: r = 0.896**

**🚀 EXECUÇÃO:**
```r
source("dados_reais_final.R")
```

---

### **2. `analise_final.R`** ⭐ **SCRIPT PRINCIPAL**
**🔍 FUNÇÃO:** Análise SEM principal com correlação r=0.896 e R²=0.803

**📈 RESULTADOS REPRODUZIDOS:**
- **R² = 0.803** (Percepção → Intenção)
- **Correlação = 0.896** (resultado principal do relatório)
- Diagrama SEM básico (`diagrama_sem_real.png`)
- Modelo de equações estruturais

**🚀 EXECUÇÃO:**
```r
source("analise_final.R")
```

---

### **3. `analise_dados_correta.R`**
**🔍 FUNÇÃO:** Análise descritiva detalhada com gráficos

**📈 RESULTADOS REPRODUZIDOS:**
- Distribuições sociodemográficas
- Médias por variável de qualidade
- Gráficos de escolaridade (`escolaridade_correta.png`)
- Gráficos de qualidade (`qualidade_servico_medias.png`)

**🚀 EXECUÇÃO:**
```r
source("analise_dados_correta.R")
```

---

### **4. `analise_sem_rigorosa.R`**
**🔍 FUNÇÃO:** Equações estruturais e índices de ajuste SEM

**📈 RESULTADOS REPRODUZIDOS:**
- **Equações estruturais** completas
- **Índices de ajuste** (CFI, TLI, RMSEA, SRMR)
- Diagrama de caminhos (`diagrama_sem_rigoroso.png`)
- Tabela de índices (`indices_ajuste_sem.csv`)

**🚀 EXECUÇÃO:**
```r
source("analise_sem_rigorosa.R")
```

---

### **5. `analise_sem_completa_todas_variaveis.R`**
**🔍 FUNÇÃO:** Análise completa das 69 variáveis dos 7 construtos

**📈 RESULTADOS REPRODUZIDOS:**
- **7 diagramas individuais** por construto
- **1 diagrama gigante** com todas as variáveis
- **Alpha de Cronbach** para cada construto
- Resumo detalhado (`resumo_analise_sem_completa.txt`)

**🚀 EXECUÇÃO:**
```r
source("analise_sem_completa_todas_variaveis.R")
```

---

## 🛠️ **INSTALAÇÃO E DEPENDÊNCIAS**

### **Instalar R e bibliotecas:**
```r
# As bibliotecas serão instaladas automaticamente pelos scripts
# Principais dependências:
install.packages(c("readr", "dplyr", "ggplot2", "lavaan", 
                   "semPlot", "psych", "corrplot", "gridExtra", 
                   "scales", "RColorBrewer"))
```

### **Estrutura de pastas necessária:**
```
projeto/
├── csv_extraidos/
│   ├── Perfil Socioeconomico.csv
│   ├── Qualidade do serviço.csv
│   ├── Percepção novos serviços.csv
│   ├── Intenção comportamental.csv
│   ├── Utilização.csv
│   ├── Aceitação da tecnologia.csv
│   └── Experiência do usuário.csv
├── dados_reais_final.R
├── analise_final.R
├── analise_dados_correta.R
├── analise_sem_rigorosa.R
└── analise_sem_completa_todas_variaveis.R
```

---

## 🚀 **EXECUÇÃO SEQUENCIAL RECOMENDADA**

### **Ordem de execução para reproduzir o relatório:**
```r
# 1. Dados demográficos básicos
source("dados_reais_final.R")

# 2. SCRIPT PRINCIPAL - Resultado r = 0.896
source("analise_final.R")

# 3. Análises descritivas detalhadas  
source("analise_dados_correta.R")

# 4. Equações estruturais rigorosas
source("analise_sem_rigorosa.R")

# 5. Análise completa de todas as variáveis
source("analise_sem_completa_todas_variaveis.R")
```

---

## 📊 **ARQUIVOS DE SAÍDA GERADOS**

### **Imagens (PNG):**
- `diagrama_sem_real.png` - Diagrama SEM principal
- `escolaridade_correta.png` - Distribuição de escolaridade
- `qualidade_servico_medias.png` - Médias de qualidade
- `diagrama_sem_rigoroso.png` - Diagrama de caminhos
- `diagrama_sem_completo.png` - Diagrama SEM completo
- `diagrama_*_individual.png` - 7 diagramas individuais
- `diagrama_sem_gigante_completo.png` - Diagrama gigante

### **Dados (CSV/TXT):**
- `indices_ajuste_sem.csv` - Índices de ajuste
- `equacoes_estruturais_sem.txt` - Equações estruturais
- `resumo_analise_sem_completa.txt` - Resumo completo

---

## ✅ **VALIDAÇÃO DOS RESULTADOS**

### **Resultados principais que devem ser reproduzidos:**

| **Métrica** | **Valor Esperado** | **Script Responsável** |
|-------------|-------------------|------------------------|
| Amostra total | 703 respondentes | `dados_reais_final.R` |
| Correlação principal | r = 0.896 | `analise_final.R` |
| R² principal | 0.803 | `analise_final.R` |
| Média qualidade | 1.65 | `dados_reais_final.R` |
| Média percepção | 4.56 | `dados_reais_final.R` |
| Total variáveis | 69 variáveis | `analise_sem_completa_todas_variaveis.R` |
| Construtos | 7 construtos | `analise_sem_completa_todas_variaveis.R` |

---

## 🔧 **TROUBLESHOOTING**

### **Problemas comuns:**

1. **Erro de encoding UTF-8:**
   - Verifique se os CSVs estão em UTF-8
   - Use `locale = locale(encoding = "UTF-8")` está configurado

2. **Bibliotecas não encontradas:**
   - Execute manualmente: `install.packages("nome_da_biblioteca")`

3. **Pasta csv_extraidos não encontrada:**
   - Certifique-se que a pasta existe com todos os 7 CSVs

4. **Resultados diferentes:**
   - Verifique se os dados de entrada são os mesmos
   - Confirm que não há dados faltantes nos CSVs

---

## 🎯 **CONCLUSÃO**

Estes scripts R **reproduzem fielmente** todos os resultados do `RELATORIO_UNIFICADO_COMPLETO_FINAL.md`, incluindo:

- ✅ **Correlação r = 0.896**
- ✅ **R² = 0.803** 
- ✅ **703 respondentes validados**
- ✅ **Todos os 19 diagramas SEM**
- ✅ **Equações estruturais completas**
- ✅ **Índices de ajuste do modelo**

Execute os scripts na ordem recomendada para obter todos os resultados do relatório final! 