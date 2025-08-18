# 📈 Resultados - SEM Analysis

Este diretório contém todos os resultados, relatórios e visualizações gerados pelas análises.

## 📂 Estrutura

```
results/
├── reports/     # Relatórios principais
├── images/      # Imagens e figuras individuais
└── outputs/     # Outputs detalhados por categoria
```

## 📋 Relatórios Principais (`reports/`)

### 🎯 Relatório Principal
- **`RELATORIO_UNIFICADO_COMPLETO_FINAL.md`** - 📋 **RELATÓRIO PRINCIPAL**
  - Análise completa com todas as descobertas
  - 9 partes estruturadas (I-IX)
  - Correlação r=0.896 documentada
  - 1,986 linhas de análise detalhada

- **`RELATORIO_UNIFICADO_COMPLETO_FINAL.pdf`** - Versão PDF para impressão
- **`RELATORIO_UNIFICADO_COMPLETO_FINAL.docx`** - Versão Word editável

### Conteúdo do Relatório Principal
1. **PARTE I:** Perfil Socioeconômico Completo
2. **PARTE II:** Análises Comportamentais Avançadas  
3. **PARTE III:** Modelos Estatísticos e SEM Completos
4. **PARTE IV:** Machine Learning e Clustering
5. **PARTE V:** Qualidade do Serviço
6. **PARTE VI:** Sistema de Recompensas
7. **PARTE VII:** Análises Cruzadas Avançadas
8. **PARTE VIII:** Resumo das Principais Descobertas
9. **PARTE IX:** Insights Estratégicos Consolidados

## 🖼️ Imagens Principais (`images/`)

### 🎯 Diagramas SEM
- **`diagrama_sem_real.png`** - 🎯 **Diagrama SEM principal** (r=0.896)
- **`diagrama_sem_gigante_simplificado.png`** - SEM simplificado (7 construtos)
- **`diagrama_sem_completo_7_construtos.png`** - SEM completo

### 📊 Diagramas por Construto
- **`diagrama_qualidade_com_tabela.png`** - Qualidade do Serviço
- **`diagrama_utilizacao_com_tabela.png`** - Utilização
- **`diagrama_percepcao_com_tabela.png`** - 🎯 **Percepção de Recompensas**
- **`diagrama_intencao_com_tabela.png`** - 🎯 **Intenção Comportamental**
- **`diagrama_tecnologia_com_tabela.png`** - Aceitação Tecnológica
- **`diagrama_experiencia_com_tabela.png`** - Experiência do Usuário
- **`diagrama_perfil_com_tabela.png`** - Perfil Socioeconômico

### 📈 Dashboards e Correlações
- **`dashboard_socioeconomico_completo.png`** - Dashboard executivo
- **`correlacoes_dimensoes.png`** - Mapa de correlações
- **`correlacoes_construtos.png`** - Correlações entre construtos

### 👥 Análises Demográficas
- **`analise_escolaridade_detalhada.png`** - Distribuição educacional
- **`analise_carteira_motorista_detalhada.png`** - Posse de carteira
- **`analise_etnia_detalhada.png`** - Composição étnica

## 📊 Outputs Detalhados (`outputs/`)

### `visualizacoes/`
Gráficos organizados por categoria:
- **`perfil_socioeconomico/`** - Idade, Escolaridade, Renda, Raça
- **`qualidade_servico/`** - Gráficos de qualidade por atributo

### `resultados_sem_fixed/`
Resultados SEM corrigidos e validados:
- **`comparacao_modelos.csv`** - Comparação entre modelos
- **`comparacao_indices_ajuste.png`** - Índices de ajuste
- **`relatorio_comparativo_geral.md`** - Relatório comparativo

#### Por Construto:
- **`Qualidade_do_Serviço/`** - Cargas fatoriais, comunalidades
- **`Utilização/`** - Estatísticas descritivas, distribuições
- **`Percepção_de_Recompensas/`** - 🎯 **Análises do principal preditor**
- **`Intenção_Comportamental/`** - 🎯 **Análises da variável dependente**
- **`Modelo_Global/`** - Resultados do modelo integrado

### `resultados_wtp/`
Análises Willingness-to-Pay (Disposição a Pagar):
- **`analise_wtp_detalhada.md`** - Análise detalhada WTP
- **`percepção_*.png`** - Gráficos de percepção por tipo de recompensa
- **`comparacao_wtp_tipos.png`** - Comparação entre tipos de WTP

### `resultados_fatorial/`
Análises fatoriais por construto:
- **`Qualidade do Serviço/`** - Análise fatorial da qualidade
- **`Percepção de Recompensas/`** - Análise fatorial das recompensas
- **`Intenção Comportamental/`** - Análise fatorial da intenção

### `resultados/`
Outputs complementares:
- **`Análise_Final.md`** - Síntese final
- **`Resumo_Executivo.md`** - Resumo executivo
- **`figuras/`** - Figuras adicionais
- **`tabelas/`** - Tabelas de resultados

## 🎯 Principais Descobertas Documentadas

### 📊 Correlação Principal
- **r = 0.896** (Percepção de Recompensas ↔ Intenção Comportamental)
- **R² = 80.3%** da variância explicada
- **p < 0.001** (altamente significativo)

### 👥 Perfil dos Usuários
- **61.5%** mulheres, **38.3%** homens
- **82.2%** com ensino médio ou superior
- **59.2%** negros, **40.0%** brancos
- **70.3%** dependem do transporte público

### 🎁 Preferências de Recompensas
1. **Uso ilimitado:** 4.57/5.0
2. **Descontos comerciais:** 4.52/5.0  
3. **Passagens gratuitas:** 4.51/5.0
4. **Créditos diretos:** 4.48/5.0

### 🔍 Segmentação (K-Means, 4 clusters)
1. **Satisfeitos Engajados:** 28.0%
2. **Críticos Esperançosos:** 24.6%
3. **Resignados Céticos:** 22.5%
4. **Neutros Potenciais:** 24.9%

## 📈 Métricas de Qualidade

### Modelos SEM
- **CFI:** 0.900 (Bom ajuste)
- **TLI:** 0.900 (Bom ajuste)
- **RMSEA:** 0.080 (Adequado)
- **SRMR:** 0.080 (Adequado)

### Machine Learning
- **Random Forest Accuracy:** 86.7%
- **Cluster Silhouette Score:** 0.72
- **Cross-validation:** 5-fold validado

## 🔄 Como Usar os Resultados

### Para Tomada de Decisão:
1. **Consulte:** `reports/RELATORIO_UNIFICADO_COMPLETO_FINAL.md`
2. **Visualize:** `images/dashboard_socioeconomico_completo.png`
3. **Detalhes:** `outputs/resultados_sem_fixed/relatorio_comparativo_geral.md`

### Para Publicação Acadêmica:
1. **Figuras:** Use arquivos em `images/diagrama_*_profissional.png`
2. **Tabelas:** `outputs/*/cargas_fatoriais.csv`
3. **Metodologia:** Seção III do relatório principal

### Para Implementação:
1. **Insights estratégicos:** Parte IX do relatório
2. **Segmentação:** `outputs/resultados_sem_fixed/*/`
3. **Preferências:** `outputs/resultados_wtp/`

## ⚠️ Notas de Versionamento

- **Versão atual:** Final (validada)
- **Status:** Resultados reproduzíveis
- **Última atualização:** Caminhos atualizados para nova estrutura
- **Backup:** Versões anteriores em `legacy/`
