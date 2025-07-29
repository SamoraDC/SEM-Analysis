# 📊 ANÁLISE ESTRUTURADA - TRANSPORTE PÚBLICO E RECOMPENSAS

## 🎯 OBJETIVO

Este diretório contém uma versão reorganizada e estruturada de todos os scripts de análise necessários para reproduzir o **RELATORIO_UNIFICADO_COMPLETO_FINAL.md**. 

A estrutura foi criada para:
- ✅ Organizar os scripts por fase de análise
- ✅ Facilitar a execução sequencial
- ✅ Permitir verificação de resultados
- ✅ Garantir reprodutibilidade

## 📁 ESTRUTURA DE DIRETÓRIOS

```
analise_estruturada/
├── 01_preparacao/              # Fase 1: Preparação e validação dos dados
│   └── dados_reais_final.py    # Carregamento e validação dos CSVs
├── 02_descritiva/              # Fase 2: Análise descritiva e perfil
│   ├── analise_expandida_completa.py      # Perfil socioeconômico completo
│   └── analise_completa_corrigida.py      # Análise base com codificação
├── 03_sem_modelos/             # Fase 3: Modelos de Equações Estruturais
│   ├── fix_sem_models.py       # Análise fatorial e SEM
│   └── analise_sem_corrigida.py # Modelo Percepção → Intenção
├── 04_machine_learning/        # Fase 4: ML e análises avançadas
│   ├── analise_estatistica_avancada.py   # Random Forest, clustering
│   └── fix_wtp_analysis.py     # Análise de disposição a pagar
├── 05_visualizacoes/           # Fase 5: Criação de diagramas
│   ├── criar_diagrama_sem_storytelling.py
│   ├── criar_diagrama_sem_profissional.py
│   ├── criar_diagrama_sem_completo_simples.py
│   └── criar_diagrama_sem_completo.py
├── 06_consolidacao/            # Fase 6: Consolidação final
│   └── analise_final.py        # Síntese e validação cruzada
├── outputs/                    # Diretório de saídas
│   ├── dados_processados/      # Dados tratados e codificados
│   ├── visualizacoes/          # Gráficos e figuras
│   ├── resultados_sem/         # Resultados dos modelos SEM
│   ├── diagramas/              # Diagramas estruturais
│   └── relatorios/             # Relatórios gerados
├── executar_analise_completa.py # SCRIPT PRINCIPAL
├── requirements.txt            # Dependências Python
└── README.md                   # Esta documentação
```

## 🚀 COMO EXECUTAR

### Pré-requisitos
1. **Dados de entrada:** Certifique-se que o diretório `../csv_extraidos/` contém os 7 arquivos CSV
2. **Dependências:** Instale as bibliotecas necessárias

```bash
# Instalar dependências
pip install -r requirements.txt

# OU usando uv (recomendado)
uv add pandas numpy matplotlib seaborn scikit-learn factor-analyzer semopy scipy statsmodels networkx
```

### Execução Completa (RECOMENDADO)
```bash
# Executar toda a análise de uma vez
python executar_analise_completa.py
```

### Execução Manual por Fases
```bash
# Fase 1: Preparação
python 01_preparacao/dados_reais_final.py

# Fase 2: Análise Descritiva
python 02_descritiva/analise_expandida_completa.py
python 02_descritiva/analise_completa_corrigida.py

# Fase 3: Modelos SEM
python 03_sem_modelos/fix_sem_models.py
python 03_sem_modelos/analise_sem_corrigida.py

# Fase 4: Machine Learning
python 04_machine_learning/analise_estatistica_avancada.py
python 04_machine_learning/fix_wtp_analysis.py

# Fase 5: Visualizações
python 05_visualizacoes/criar_diagrama_sem_storytelling.py
python 05_visualizacoes/criar_diagrama_sem_profissional.py
python 05_visualizacoes/criar_diagrama_sem_completo_simples.py
python 05_visualizacoes/criar_diagrama_sem_completo.py

# Fase 6: Consolidação
python 06_consolidacao/analise_final.py
```

## 📊 PRINCIPAIS RESULTADOS ESPERADOS

### Descobertas Chave a Reproduzir:
- **Correlação Percepção → Intenção:** r = 0.896
- **Variância Explicada:** 80.3% da intenção comportamental  
- **Perfil Educacional:** 82.2% com ensino médio ou superior
- **Predominância Feminina:** 61.5% dos usuários
- **População Negra:** 59.2% dos usuários
- **Usuários de TP:** 70.3% como principal meio
- **Qualidade Média:** 1.64/5 (baixa)
- **Percepção Recompensas:** 4.51/5 (alta)
- **Intenção Comportamental:** 4.55/5 (alta)

### Visualizações Geradas:
- `diagrama_sem_storytelling_limpo.png` - Diagrama com narrativa visual
- `diagrama_executivo_simples.png` - Versão para apresentações
- `modelo_sem_global.png` - Modelo estrutural completo
- Gráficos de distribuição socioeconômica
- Mapas de correlação entre variáveis

## 🔍 VERIFICAÇÃO DE RESULTADOS

Após a execução, verifique:

1. **Relatório de Verificação:** `outputs/relatorios/RELATORIO_VERIFICACAO_ANALISE.md`
2. **Log de Execução:** Saída do console com timestamps
3. **Arquivos Gerados:** Conte os arquivos em cada subdiretório de `outputs/`

### Checklist de Conformidade:
- [ ] 703 respondentes processados
- [ ] 7 datasets carregados com sucesso
- [ ] Modelo SEM com R² ≈ 0.80
- [ ] Correlação Percepção-Intenção ≈ 0.896
- [ ] Diagramas SEM gerados
- [ ] Visualizações salvas

## ⚠️ TROUBLESHOOTING

### Problemas Comuns:

**1. Erro "Arquivo não encontrado"**
```
Solução: Verifique se ../csv_extraidos/ contém todos os 7 arquivos CSV
```

**2. Erro de dependências**
```bash
# Instalar dependências específicas
pip install pandas==1.3.0 numpy==1.20.0 matplotlib==3.4.0
```

**3. Timeout na execução**
```
Solução: Execute as fases manualmente uma por vez
```

**4. Erro de memória**
```
Solução: Feche outros programas e execute apenas as fases obrigatórias
```

## 📈 ARQUIVOS DE ENTRADA NECESSÁRIOS

### Localização: `../csv_extraidos/`
1. `Qualidade do serviço.csv` (705 linhas)
2. `Utilização.csv` (708 linhas)  
3. `Percepção novos serviços.csv` (705 linhas)
4. `Intenção comportamental.csv` (705 linhas)
5. `Aceitação da tecnologia.csv` (705 linhas)
6. `Experiência do usuário.csv` (705 linhas)
7. `Perfil Socioeconomico.csv` (706 linhas)

## 🎯 COMPARAÇÃO COM RELATÓRIO ORIGINAL

Este projeto visa **reproduzir exatamente** os resultados do `RELATORIO_UNIFICADO_COMPLETO_FINAL.md`:

### Seções Reproduzidas:
- ✅ **Parte I:** Perfil Socioeconômico Completo
- ✅ **Parte II:** Análises Comportamentais Avançadas  
- ✅ **Parte III:** Modelos Estatísticos e SEM
- ✅ **Parte IV:** Machine Learning e Clustering
- ✅ **Parte V:** Qualidade do Serviço
- ✅ **Parte VI:** Sistema de Recompensas
- ✅ **Parte VII:** Insights Estratégicos Consolidados

### Figuras Reproduzidas:
- Figura 1.1-1.4: Distribuições demográficas
- Figura 4.1-4.2: Diagramas SEM com storytelling
- Figura 7.1-7.4: Avaliações de qualidade
- Dashboards comparativos

---

## 📞 SUPORTE

Em caso de problemas:
1. Verifique o log de execução
2. Consulte o arquivo `RELATORIO_VERIFICACAO_ANALISE.md`
3. Execute as fases manualmente para isolar erros
4. Verifique se todos os arquivos CSV estão presentes

---

**Versão:** 1.0  
**Data:** Junho 2025  
**Objetivo:** Verificação e reprodução do RELATORIO_UNIFICADO_COMPLETO_FINAL.md 