# 💾 Dados - SEM Analysis

Este diretório contém todos os dados do projeto, organizados em dados brutos e processados.

## 📂 Estrutura

```
data/
├── raw/           # Dados brutos originais
└── processed/    # Dados limpos e processados
```

## 🔍 Dados Brutos (`raw/`)

### `dados/`
Dados originais em formato Excel:
- **`BDTransportepublico.xlsx`** - Base de dados principal
- **`BDTransportepublicosegmentada.xlsx`** - Base segmentada

### `csv_extraidos/`
CSVs extraídos da base principal por construto:
- **`Aceitação da tecnologia.csv`** (N=703) - Construto tecnológico
- **`Experiência do usuário.csv`** (N=703) - Experiência atual
- **`Intenção comportamental.csv`** (N=703) - 🎯 **Variável dependente**
- **`Percepção de recompensas.csv`** (N=703) - 🎯 **Principal preditor**
- **`Perfil Socioeconomico.csv`** (N=703) - Demografia
- **`Qualidade do serviço.csv`** (N=703) - Qualidade percebida
- **`Utilização.csv`** (N=703) - Padrões de uso

### `csv_segmentados/`
Dados segmentados para análises específicas:
- **`BDTP.csv`** - Base principal segmentada
- **`segmentada - *.csv`** - Bases por critérios específicos

## 🔬 Dados Processados (`processed/`)

### `dados_processados/`
Dados limpos e preparados para análise:
- **`aceitacao_codificado.csv`** - Aceitação tecnológica codificada
- **`aceitacao_tratado.csv`** - Aceitação tratada
- **`base_unificada.csv`** - 🎯 **Base principal unificada**
- **`construtos_principais.csv`** - Construtos SEM finais
- **`intencao_codificado.csv`** - Intenção comportamental codificada
- **`percepcao_codificado.csv`** - Percepção de recompensas codificada
- **`perfil_codificado.csv`** - Perfil socioeconômico codificado
- **`qualidade_codificado.csv`** - Qualidade do serviço codificada

### `dados_analise_estruturada/`
Dados específicos para análise SEM estruturada:
- Mesmos arquivos dos `csv_extraidos` mas validados e limpos
- Usados pelos scripts de análise SEM

## 📊 Características dos Dados

### Amostra Principal
- **N = 703** respondentes válidos
- **Taxa de resposta:** 100% (após limpeza)
- **Missing data:** < 5% por variável

### Variáveis por Construto

| Construto | Variáveis | Descrição |
|-----------|-----------|-----------|
| **Qualidade do Serviço** | 12 | Avaliação da qualidade atual (1-5) |
| **Utilização** | 11 | Padrões de uso do transporte |
| **Aceitação Tecnológica** | 11 | Abertura para soluções digitais |
| **Experiência do Usuário** | 9 | Experiência subjetiva atual |
| **Perfil Socioeconômico** | 8 | Características demográficas |
| **Percepção de Recompensas** | 9 | 🎯 **Principal preditor** (1-5) |
| **Intenção Comportamental** | 10 | 🎯 **Variável dependente** (1-5) |

### Escalas de Medição
- **Likert 5 pontos:** 1 (Discordo totalmente) - 5 (Concordo totalmente)
- **Frequência:** 1 (Nunca) - 5 (Sempre)
- **Satisfação:** 1 (Muito insatisfeito) - 5 (Muito satisfeito)

## 🎯 Dados Principais para Replicação

### Para reproduzir o resultado r=0.896:
1. **`csv_extraidos/Percepção de recompensas.csv`**
2. **`csv_extraidos/Intenção comportamental.csv`**

### Para análise SEM completa (7 construtos):
- **Todos os arquivos** em `csv_extraidos/`
- **Base unificada:** `processed/dados_processados/base_unificada.csv`

## 🔄 Pipeline de Processamento

```
1. Excel → CSV (extração manual)
2. CSV → Codificação (scripts/core/dados_preparacao.py)
3. Codificado → Validação (limpeza de missing)
4. Validado → Base unificada (merge dos construtos)
5. Unificada → Análise SEM (entrada para modelos)
```

## 📈 Qualidade dos Dados

### Validações Realizadas
- ✅ **Completude:** < 5% missing por variável
- ✅ **Consistência:** Escalas Likert validadas
- ✅ **Outliers:** Identificados e tratados
- ✅ **Normalidade:** Transformações aplicadas quando necessário

### Estatísticas Descritivas Principais
- **Percepção de Recompensas:** M = 4.51, DP = 0.89
- **Intenção Comportamental:** M = 4.55, DP = 0.92
- **Qualidade do Serviço:** M = 1.64, DP = 0.87
- **Correlação principal:** r = 0.896 (p < 0.001)

## ⚠️ Notas Importantes

1. **Dados sensíveis:** Dados pessoais foram anonimizados
2. **Backup:** Dados originais preservados em `raw/`
3. **Versionamento:** Cada processamento gera nova versão
4. **Encoding:** Todos os CSVs em UTF-8
5. **Separador:** Vírgula (,) como separador padrão
