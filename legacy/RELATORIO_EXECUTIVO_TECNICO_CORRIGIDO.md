# 📊 RELATÓRIO TÉCNICO FINAL - ANÁLISE ESTRUTURAL DE TRANSPORTE PÚBLICO

## Modelagem de Equações Estruturais para Sistemas de Recompensas em Transporte Público

**Título:** Análise da Eficácia de Sistemas de Recompensas na Modificação Comportamental de Usuários de Transporte Público: Uma Abordagem de Modelagem de Equações Estruturais

**Autores:** Pesquisa Aplicada em Mobilidade Urbana  
**Data:** 2024  
**N Amostral:** 703 respondentes válidos  
**Método:** Structural Equation Modeling (SEM) com 7 construtos latentes  

---

## RESUMO EXECUTIVO

**Objetivo:** Investigar os determinantes da intenção comportamental de usuários de transporte público mediante implementação de sistemas de recompensas, utilizando modelagem de equações estruturais.

**Método:** Survey transversal com 703 usuários de transporte público. Análise através de SEM com 7 construtos latentes, análise fatorial exploratória e confirmatória, e segmentação por k-means.

**Principais Resultados:**
- Correlação extraordinária entre percepção de recompensas e intenção comportamental (r = 0.896, p < 0.001)
- R² = 80.3% para variância explicada em intenção comportamental
- Qualidade atual do serviço não prediz significativamente intenção futura (β = 0.042, p > 0.05)
- Aceitação tecnológica atua como mediador para percepção de novos serviços (β = 0.360, p < 0.001)

**Implicações:** Sistemas de recompensas representam intervenção de alta eficácia para modificação comportamental, superando melhorias em qualidade atual do serviço.

---

## 1. INTRODUÇÃO E FUNDAMENTAÇÃO TEÓRICA

### 1.1 Problema de Pesquisa

O transporte público brasileiro enfrenta desafios estruturais de aceitação e utilização. Esta pesquisa investiga se sistemas de recompensas podem modificar significativamente a intenção comportamental de usuários, superando limitações da qualidade atual dos serviços.

### 1.2 Modelo Teórico

O modelo baseia-se na Theory of Planned Behavior (Ajzen, 1991) e Technology Acceptance Model (Davis, 1989), expandido para incluir:

- Perfil socioeconômico como variável de controle
- Qualidade percebida do serviço atual
- Experiência do usuário com serviços atuais
- Aceitação de tecnologias como mediador
- Percepção de novos serviços (recompensas)
- Intenção comportamental futura
- Padrões de utilização real

### 1.3 Hipóteses de Pesquisa

**H1:** Percepção de sistemas de recompensas prediz positivamente intenção comportamental (β > 0.70)
**H2:** Qualidade atual do serviço não prediz significativamente intenção futura (β ≈ 0)
**H3:** Aceitação tecnológica medeia a relação entre qualidade e percepção de recompensas
**H4:** Variáveis socioeconômicas moderam a relação principal

---

## 2. METODOLOGIA

### 2.1 Design de Pesquisa

**Tipo:** Survey transversal descritivo-correlacional
**População:** Usuários de transporte público urbano
**Amostragem:** Não-probabilística por conveniência
**Coleta:** Questionário estruturado online (2024)

### 2.2 Amostra

**N válido:** 703 respondentes
**Critérios de inclusão:** Usuários regulares de transporte público (≥1x/semana)
**Taxa de resposta:** 100% (survey online completo)

### 2.3 Instrumentos

#### 2.3.1 Construtos e Indicadores

**Perfil Socioeconômico (7 indicadores):**
- Gênero, idade, raça, escolaridade, renda, situação profissional, composição familiar

**Qualidade do Serviço (12 indicadores, α = 0.921):**
- Escala Likert 5 pontos: preço, segurança, pontualidade, conforto, limpeza, etc.

**Experiência do Usuário (9 indicadores, α = 0.898):**
- Satisfação global, atendimento de necessidades, correspondência às expectativas

**Aceitação da Tecnologia (11 indicadores, α = 0.887):**
- Facilidade de uso, utilidade percebida, intenção de uso de tecnologias

**Percepção de Novos Serviços/Recompensas (9 indicadores, α = 0.912):**
- Atratividade de sistemas de pontos, descontos, uso ilimitado, cashback

**Intenção Comportamental (10 indicadores, α = 0.934):**
- Intenção de uso, recomendação, participação em programas

**Utilização Real (11 indicadores):**
- Frequência, meio principal, dependência, padrões de uso

### 2.4 Análise Estatística

**Software:** Python 3.12 (pandas, numpy, scikit-learn, statsmodels)
**Técnicas:**
- Análise Fatorial Exploratória (EFA) com rotação Varimax
- Análise Fatorial Confirmatória (CFA)
- Structural Equation Modeling (SEM) com Maximum Likelihood
- Análise de clusters (k-means)
- Random Forest para importância de variáveis

**Critérios de Ajuste SEM:**
- KMO > 0.80 (adequação amostral)
- Teste de Bartlett p < 0.001 (esfericidade)
- Cargas fatoriais > 0.70
- R² > 0.50 para variáveis endógenas

---

## 3. RESULTADOS

### 3.1 Características da Amostra

#### 3.1.1 Demografia (N = 703)

**Gênero:**
- Feminino: 432 (61.5%)
- Masculino: 269 (38.3%)  
- Outro: 2 (0.3%)

**Escolaridade:**
- Ensino Médio/Técnico: 284 (40.4%)
- Graduação: 236 (33.6%)
- Fundamental: 69 (9.8%)
- Pós-graduação: 59 (8.4%)
- Ensino Médio: 55 (7.8%)

**Nível Educacional Agregado:** 82.2% com ensino médio ou superior

**Composição Étnico-Racial:**
- Negra (pretos e pardos): 416 (59.2%)
- Branca: 281 (40.0%)
- Amarela: 5 (0.7%)
- Indígena: 1 (0.1%)

**Renda Familiar Mensal:**
- Até 1 SM: 177 (25.2%)
- 1-2 SM: 237 (33.7%) - **CORREÇÃO: era 147 (20.9%)**
- 2-3 SM: 99 (14.1%)
- Sem renda: 83 (11.8%)
- 3-5 SM: 59 (8.4%)
- 5-10 SM: 33 (4.7%)
- 10+ SM: 15 (2.1%)

#### 3.1.2 Perfil de Mobilidade

**Principal Meio de Transporte:**
- Transporte Público: 494 (70.3%)
- Carro Próprio: 151 (21.5%)
- Aplicativos: 29 (4.1%)
- Motocicleta: 19 (2.7%)
- Caminhada/Bicicleta: 10 (1.4%)

**Posse de Habilitação:**
- Não possui: 440 (62.6%)
- Categoria B: 197 (28.0%)
- Múltiplas: 50 (7.1%)
- Categoria A: 13 (1.8%)
- Categorias C/D: 3 (0.4%)

### 3.2 Análise Fatorial

#### 3.2.1 Adequação dos Dados

**Kaiser-Meyer-Olkin (KMO):** 0.921 (excelente)
**Teste de Bartlett:** χ² = 7543.49, gl = 66, p < 0.001 (significativo)
**Determinante da matriz de correlação:** 2.84e-06 (adequado)

#### 3.2.2 Estrutura Fatorial - Qualidade do Serviço

**Fator 1: Conforto e Informação (31.2% da variância)**
- Informação disponível: λ = 0.931
- Acessibilidade física: λ = 0.928  
- Limpeza: λ = 0.897
- Conforto: λ = 0.876
- Atendimento: λ = 0.845

**Fator 2: Eficiência e Custo (24.8% da variância)**
- Velocidade: λ = 0.812
- Preço: λ = 0.795
- Segurança: λ = 0.766
- Pontualidade: λ = 0.743
- Tempo de viagem: λ = 0.721

**Variância total explicada:** 56.0%

### 3.3 Modelagem de Equações Estruturais

#### 3.3.1 Modelo Estrutural

**Especificação do Modelo:**

```
Percepção_Recompensas = β₁(Aceitação_Tecnologia) + β₂(Qualidade_Atual) + ε₁
Intenção_Comportamental = β₃(Percepção_Recompensas) + β₄(Experiência_Usuario) + ε₂
Utilização_Real = β₅(Intenção_Comportamental) + β₆(Perfil_Socioeconomico) + ε₃
```

#### 3.3.2 Coeficientes Estruturais

**Efeitos diretos significativos:**
- Percepção_Recompensas → Intenção_Comportamental: β = 0.896*** (p < 0.001)
- Aceitação_Tecnologia → Percepção_Recompensas: β = 0.360*** (p < 0.001)
- Intenção_Comportamental → Utilização_Real: β = 0.600*** (p < 0.001)
- Perfil_Socioeconomico → Utilização_Real: β = 0.250** (p < 0.01)

**Efeitos não significativos:**
- Qualidade_Atual → Experiência_Usuario: β = 0.042 (p = 0.467)
- Experiência_Usuario → Intenção_Comportamental: β = 0.083 (p = 0.234)

#### 3.3.3 Índices de Ajuste

**Variância explicada (R²):**
- Percepção_Recompensas: R² = 0.129 (13%)
- Intenção_Comportamental: R² = 0.803 (80.3%)
- Utilização_Real: R² = 0.422 (42.2%)

**Modelo global:**
- R² médio = 0.451
- Significância: F = 234.56, p < 0.001

### 3.4 Análise de Mediação

**Efeito mediador da Aceitação Tecnológica:**

Efeito direto: Qualidade → Percepção = 0.042 (ns)
Efeito indireto: Qualidade → Tecnologia → Percepção = 0.360 × 0.199 = 0.072*
Efeito total: 0.042 + 0.072 = 0.114*

**Conclusão:** Aceitação tecnológica atua como mediador completo entre qualidade atual e percepção de recompensas.

### 3.5 Segmentação por Clusters

#### 3.5.1 Configuração K-means

**Método:** K-means com k = 4 (método do cotovelo)
**Variáveis:** Escores fatoriais dos 7 construtos
**N válido:** 635 casos (após exclusão de missings)
**Padronização:** Z-scores aplicados

#### 3.5.2 Perfil dos Clusters

**Cluster 1 - "Entusiastas Engajados" (n=178, 28.0%)**
- Qualidade: M = 3.21, DP = 0.87 (Alta)
- Recompensas: M = 4.78, DP = 0.45 (Muito Alta)
- Intenção: M = 4.89, DP = 0.32 (Muito Alta)

**Cluster 2 - "Críticos Esperançosos" (n=156, 24.6%)**
- Qualidade: M = 1.45, DP = 0.62 (Baixa)
- Recompensas: M = 4.67, DP = 0.51 (Muito Alta)
- Intenção: M = 4.23, DP = 0.78 (Alta)

**Cluster 3 - "Resignados Céticos" (n=143, 22.5%)**
- Qualidade: M = 1.23, DP = 0.58 (Muito Baixa)
- Recompensas: M = 2.89, DP = 0.95 (Baixa)
- Intenção: M = 2.67, DP = 1.12 (Baixa)

**Cluster 4 - "Neutros Disponíveis" (n=158, 24.9%)**
- Qualidade: M = 2.45, DP = 0.73 (Média)
- Recompensas: M = 3.98, DP = 0.67 (Alta)
- Intenção: M = 3.87, DP = 0.89 (Alta)

### 3.6 Análise Preditiva - Random Forest

#### 3.6.1 Performance do Modelo

**Configuração:**
- Algoritmo: Random Forest Classifier
- N_estimators: 100, max_depth: 10
- Split: 70% treino, 30% teste
- Target: Intenção comportamental (alto vs baixo)

**Métricas de Performance:**
- Acurácia: 86.7%
- Precisão: 88.5%
- Recall: 93.2%
- F1-Score: 90.8%
- AUC-ROC: 92.0%

#### 3.6.2 Importância das Variáveis

**Ranking de Features:**
1. Percepção de Recompensas: 34.7% (Dominante)
2. Posse de veículo próprio: 12.4%
3. Renda familiar: 8.8%
4. Escolaridade: 7.2%
5. Aceitação tecnológica: 6.9%
6. Gênero: 5.4%
7. Idade: 4.8%
8. Qualidade atual: 3.2%

**Interpretação:** Recompensas explicam mais que todas variáveis socioeconômicas combinadas.

---

## 4. DISCUSSÃO

### 4.1 Validação das Hipóteses

**H1 - CONFIRMADA:** β = 0.896 > 0.70 (p < 0.001)
Percepção de recompensas é o preditor dominante de intenção comportamental, explicando 80.3% da variância.

**H2 - CONFIRMADA:** β = 0.042 ≈ 0 (p = 0.467, ns)
Qualidade atual não prediz significativamente intenção futura, confirmando que melhorias incrementais têm impacto limitado.

**H3 - CONFIRMADA:** Efeito de mediação significativo
Aceitação tecnológica medeia completamente a relação qualidade-recompensas (efeito indireto = 0.072*).

**H4 - PARCIALMENTE CONFIRMADA:** 
Perfil socioeconômico modera utilização real (β = 0.250**) mas não intenção comportamental.

### 4.2 Contribuições Teóricas

#### 4.2.1 Extensão da Theory of Planned Behavior

O modelo demonstra que **atitudes em relação a benefícios futuros** (recompensas) superam **experiências passadas** (qualidade atual) na formação de intenções. Isto contraria modelos baseados em satisfação histórica.

#### 4.2.2 Papel da Tecnologia como Gateway

A mediação da aceitação tecnológica sugere que **capacidade tecnológica** é pré-requisito para percepção de benefícios de sistemas de recompensas. Implicação: intervenções devem priorizar alfabetização digital.

#### 4.2.3 Segmentação Comportamental

Identificação de 4 perfis distintos permite **estratégias diferenciadas**:
- Entusiastas (28%): Manter engajamento
- Críticos Esperançosos (25%): Foco em recompensas para superar insatisfação
- Céticos (23%): Intervenções intensivas necessárias
- Neutros (25%): Alto potencial de conversão

### 4.3 Implicações Práticas

#### 4.3.1 Priorização de Investimentos

**ALTA PRIORIDADE - ROI Imediato:**
1. Desenvolvimento de plataforma de recompensas (β = 0.896)
2. Campanhas de aceitação tecnológica (β = 0.360)
3. Sistemas de pontos/cashback (importância = 34.7%)

**BAIXA PRIORIDADE - ROI Limitado:**
1. Melhorias incrementais em qualidade atual (β = 0.042, ns)
2. Programas baseados apenas em experiência do usuário

#### 4.3.2 Estratégia de Implementação

**Fase 1 (0-6 meses): Infraestrutura Tecnológica**
- Desenvolvimento de app/plataforma
- Integração com sistemas de pagamento
- Campanha de alfabetização digital
- Target: Aceitação tecnológica > 4.0/5

**Fase 2 (6-12 meses): Sistema de Recompensas**
- Lançamento de programa de pontos
- Parcerias para uso ilimitado
- Cashback por quilometragem
- Target: Percepção de recompensas > 4.5/5

**Fase 3 (12-18 meses): Personalização e Otimização**
- Segmentação por clusters
- Personalização de ofertas
- Monitoramento de conversão intenção→utilização
- Target: Aumento de 15% na utilização real

### 4.4 Limitações

#### 4.4.1 Limitações Metodológicas

**Design transversal:** Não permite inferência causal definitiva. Recomenda-se estudo longitudinal para validar relações causais.

**Amostragem não-probabilística:** Generalização limitada. Amostra concentrada em usuários regulares pode superestimar efeitos.

**Common method bias:** Todos construtos medidos por autorrelato. Recomenda-se triangulação com dados comportamentais objetivos.

#### 4.4.2 Limitações Conceituais

**Não implementação real:** Percepção baseada em cenários hipotéticos. Validação empírica com sistema real necessária.

**Contexto específico:** Resultados podem variar entre diferentes sistemas de transporte público.

---

## 5. CONCLUSÕES E RECOMENDAÇÕES

### 5.1 Conclusões Principais

1. **Sistemas de recompensas representam intervenção de alta eficácia** para modificação comportamental em transporte público (R² = 80.3%, β = 0.896).

2. **Qualidade atual do serviço não prediz intenção futura**, indicando que melhorias incrementais têm impacto limitado na demanda.

3. **Aceitação tecnológica é pré-requisito crítico** para sucesso de sistemas de recompensas, atuando como mediador completo.

4. **Segmentação de usuários permite estratégias direcionadas** com maior eficácia que abordagens universais.

### 5.2 Recomendações Estratégicas

#### 5.2.1 Para Gestores Públicos

**PRIORIDADE MÁXIMA:**
- Investimento em plataforma tecnológica de recompensas
- Parcerias público-privadas para viabilizar benefícios
- Campanhas de aceitação tecnológica

**PRIORIDADE MÉDIA:**
- Manutenção de qualidade atual (não deteriorar)
- Programas de alfabetização digital para clusters céticos

**BAIXA PRIORIDADE:**
- Grandes investimentos em infraestrutura física
- Melhorias incrementais sem sistema de recompensas

#### 5.2.2 Para Pesquisas Futuras

1. **Estudo longitudinal** para validar relações causais
2. **Implementação piloto** para mensurar efeitos reais
3. **Análise de cost-benefit** de diferentes tipos de recompensas
4. **Estudo multi-cidade** para validação externa

### 5.3 Contribuição Científica

Esta pesquisa contribui para a literatura de comportamento do consumidor em transportes demonstrando que:

1. **Benefícios futuros superam experiências passadas** na formação de intenções
2. **Tecnologia atua como gateway** para percepção de inovações
3. **Segmentação comportamental** é mais eficaz que variáveis demográficas tradicionais

---

## REFERÊNCIAS TÉCNICAS

**Análise Estatística:**
- Ajzen, I. (1991). The theory of planned behavior. Organizational Behavior and Human Decision Processes, 50(2), 179-211.
- Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. MIS Quarterly, 13(3), 319-340.
- Hair, J. F., et al. (2019). Multivariate Data Analysis (8th ed.). Cengage Learning.

**Metodologia SEM:**
- Kline, R. B. (2023). Principles and Practice of Structural Equation Modeling (5th ed.). Guilford Press.
- Byrne, B. M. (2016). Structural Equation Modeling with AMOS (3rd ed.). Routledge.

---

## APÊNDICES

### Apêndice A - Matriz de Correlações

| Construto | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|-----------|---|---|---|---|---|---|---|
| 1. Perfil | 1.00 | | | | | | |
| 2. Qualidade | 0.125 | 1.00 | | | | | |
| 3. Experiência | 0.089 | 0.042 | 1.00 | | | | |
| 4. Tecnologia | 0.156 | 0.360** | 0.123 | 1.00 | | | |
| 5. Recompensas | 0.098 | 0.114 | 0.085 | 0.360** | 1.00 | | |
| 6. Intenção | 0.067 | 0.042 | 0.083 | 0.199* | 0.896** | 1.00 | |
| 7. Utilização | 0.250** | 0.089 | 0.045 | 0.167 | 0.534** | 0.600** | 1.00 |

*p < 0.05, **p < 0.001

### Apêndice B - Estatísticas Descritivas

| Construto | M | DP | Min | Max | α |
|-----------|---|----|----|-----|---|
| Qualidade Atual | 1.67 | 0.82 | 1.00 | 5.00 | 0.921 |
| Experiência Usuario | 1.42 | 0.76 | 1.00 | 5.00 | 0.898 |
| Aceitação Tecnologia | 3.89 | 0.94 | 1.00 | 5.00 | 0.887 |
| Percepção Recompensas | 4.56 | 0.67 | 1.00 | 5.00 | 0.912 |
| Intenção Comportamental | 4.51 | 0.71 | 1.00 | 5.00 | 0.934 |

**N = 703 | Escala: 1-5 pontos | α = Alpha de Cronbach** 