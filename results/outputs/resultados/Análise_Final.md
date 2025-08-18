# Análise Final dos Modelos de Equações Estruturais para Transporte Público

## Resumo Executivo

Esta análise examina as relações entre percepções, experiências e disposições dos usuários de transporte público, utilizando Modelagem de Equações Estruturais (SEM). Foram implementados seis modelos específicos e um modelo global integrado, além de análises adicionais que incluem modelagem Mixed Logit e fatores sociodemográficos.

Os resultados indicam que a qualidade percebida do transporte público influencia significativamente a experiência geral dos usuários (coef. 0.85), enquanto o valor percebido das recompensas e a experiência geral influenciam a disposição a aceitar incentivos (coef. 0.26 e 0.12, respectivamente). Este conhecimento oferece importantes direcionamentos para políticas públicas de transporte que visem aumentar a satisfação e o uso do transporte coletivo.

## Modelos Individuais Implementados

### 1. Qualidade do Serviço

- **Ajuste**: RMSEA = 0.23, o que indica um ajuste insatisfatório
- **Carga mais alta**: Informação sobre linhas (coef. 9.68) e locais atendidos (coef. 8.78)
- **Insight**: A informação sobre as linhas e a abrangência do sistema são aspectos cruciais da qualidade percebida

### 2. Utilização do Transporte

- **Ajuste**: RMSEA = 0.14, indicando ajuste marginal
- **Carga mais alta**: Tempo gasto com transporte (-2.13) - relacionamento negativo com motivação
- **Insight**: Quanto maior o tempo gasto no transporte, menor a motivação para uso

### 3. Percepção sobre Recompensas

- **Ajuste**: RMSEA = 0.28, indicando ajuste inadequado
- **Construtos**: ValorRecompensas e PreferenciaPassesIlimitados são distintos mas correlacionados (0.38)
- **Insight**: Os usuários distinguem entre recompensas diretas (cashback, pontos) e passes ilimitados

### 4. Intenção de Uso

- **Ajuste**: RMSEA = 0.41, indicando ajuste inadequado
- **Carga mais alta**: Desconto fora do horário de pico (1.68) para recompensas
- **Insight**: Descontos fora do horário de pico têm forte potencial para influenciar comportamento

### 5. Disposição a Participar

- **Ajuste**: RMSEA = 0.29, indicando ajuste inadequado
- **Carga mais alta**: Pagar diariamente (1.50) na disposição para pagamento diário
- **Insight**: Usuários mais dispostos a pagamentos diários têm preferência por valores mais altos

### 6. Experiência e Facilidade de Pagamento

- **Ajuste**: RMSEA = 0.10, indicando ajuste aceitável
- **Carga mais alta**: QR code (8.64) e aplicativos (6.41) na facilidade de pagamento
- **Insight**: Métodos digitais de pagamento são valorizados como facilitadores

## Modelo Global

O modelo global integra as variáveis-chave dos modelos individuais e fornece insights sobre as relações estruturais:

### Relações Estruturais:

- **QualidadePercebida → ExperienciaGeral**: 0.85
- **ValorRecompensas → DisposicaoAceitar**: 0.26
- **ExperienciaGeral → DisposicaoAceitar**: 0.12

### Principais Indicadores:

- **QualidadePercebida**: Confiabilidade de horários (1.16), segurança (1.10)
- **ExperienciaGeral**: Necessidades atendidas (1.07), correspondência às expectativas (1.01)
- **ValorRecompensas**: Pontos/créditos (1.00), cashback por km (0.96)
- **DisposicaoAceitar**: Recompensa por km (0.99), desconto fora pico (0.89)

### Ajuste do Modelo:

- RMSEA = 0.10, indicando ajuste marginal

## Análise Mixed Logit

A análise Mixed Logit examinou três disposições específicas:

### 1. Disposição a Pagar Diariamente (até R$10):

- **Fatores significativos**:
  - Renda (coef. 0.31, p=0.001)
  - Idade (coef. -0.23, p=0.011)
- **Pseudo-R²**: 0.046

### 2. Disposição a Pagar Mensalmente (R$150-200):

- **Fatores significativos**:
  - Gênero (coef. 0.67, p=0.034)
- **Pseudo-R²**: 0.027

### 3. Disposição a Aceitar Recompensa por KM:

- **Fatores significativos**:
  - Renda (coef. 0.49, p<0.001)
  - Idade (coef. -0.26, p=0.021)
  - Gênero (coef. 1.36, p=0.001)
- **Pseudo-R²**: 0.117

## Análise Sociodemográfica

As análises de variáveis-chave por fatores sociodemográficos (gênero, idade, escolaridade e renda) revelaram tendências importantes:

1. **Gênero**: Mulheres demonstraram maior sensibilidade à segurança e maior disposição a aceitar recompensas
2. **Idade**: Pessoas mais jovens mostraram maior disposição a participar de programas de recompensa
3. **Escolaridade**: Maior escolaridade associada a maior exigência de qualidade e confiabilidade
4. **Renda**: Faixas de renda mais altas mostram maior disposição a pagar por serviços premium (passes mensais e anuais)

## Conclusões e Recomendações

### Principais Insights:

1. A qualidade percebida do transporte é o principal determinante da experiência geral
2. Recompensas e experiência positiva aumentam a disposição a pagar/aceitar incentivos
3. Confiabilidade de horários e segurança são os indicadores mais importantes de qualidade
4. Programas de recompensa devem considerar a segmentação por perfil sociodemográfico

### Recomendações:

1. **Melhoria de Qualidade**: Investir prioritariamente em confiabilidade de horários e segurança
2. **Programas de Recompensas**: Desenvolver sistemas que ofereçam múltiplas opções (cashback por km, descontos fora do pico)
3. **Segmentação**: Customizar ofertas considerando perfil demográfico (idade, renda e gênero)
4. **Métodos de Pagamento**: Investir em sistemas de pagamento digital (QR code, aplicativos)
5. **Gerenciamento de Picos**: Implementar descontos em horários fora de pico para redistribuir demanda

## Alinhamento com Escopo e Entrega

O estudo cumpriu os requisitos especificados no escopo, implementando:

- Seis modelos SEM específicos para diferentes dimensões
- Um modelo global integrando as relações principais
- Análise Mixed Logit para disposições específicas
- Análise sociodemográfica detalhada
- Visualizações de resultados por fatores sociodemográficos

Os resultados oferecem direcionamentos concretos para políticas públicas de transporte, incluindo:

1. Priorização de investimentos baseados no impacto na experiência do usuário
2. Desenvolvimento de programas de incentivo personalizados
3. Estratégias para aumento do uso do transporte público

## Limitações e Pesquisas Futuras

### Limitações:

- Ajuste insatisfatório de alguns modelos individuais
- Ausência do graphviz para visualização completa dos modelos
- Possível viés de amostragem (análise da representatividade populacional)

### Pesquisas Futuras:

1. Refinar os modelos com ajustes inadequados
2. Investigar mais profundamente o impacto das características operacionais (frequência, tempo de viagem)
3. Realizar análises longitudinais para verificar mudanças comportamentais após implementação de programas de recompensa
4. Expandir o modelo para incluir impactos ambientais e de sustentabilidade

## Contribuição para Políticas de Transporte

Os resultados fornecem evidências para formulação de políticas baseadas em dados, destacando a importância de:

1. Investimentos em qualidade como prioridade máxima
2. Programas de incentivo personalizados como catalisadores de mudança comportamental
3. Segmentação demográfica na concepção de serviços
4. Tecnologias de pagamento como facilitadoras da experiência do usuário

Esta análise integrada oferece uma base sólida para decisões estratégicas e operacionais no setor de transporte público, alinhadas com expectativas dos usuários e sustentabilidade do sistema.
