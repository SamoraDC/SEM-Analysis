# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data analysis project focused on public transportation acceptance and reward systems research. The project analyzes survey data (703 respondents) using Structural Equation Modeling (SEM), statistical analysis, and machine learning to understand user behavior patterns and willingness to pay for reward systems in public transportation.

## Key Technologies & Dependencies

- **Python**: Primary analysis language (>=3.12)
- **Core Libraries**: pandas, numpy, matplotlib, seaborn, scikit-learn
- **SEM Analysis**: semopy (for Structural Equation Modeling)
- **Factor Analysis**: factor-analyzer
- **Statistical**: scipy, statsmodels
- **Visualization**: graphviz (for SEM diagrams)

Install dependencies with:
```bash
# Using uv (recommended)
uv sync

# Or pip
pip install -r requirements.txt
```

## Project Structure

### Core Analysis Pipeline (`analise_estruturada/`)
The main analysis is organized in 6 sequential phases:

1. **01_preparacao/**: Data preparation and validation
   - `dados_reais_final.py` - Load and validate CSV datasets
   
2. **02_descritiva/**: Descriptive analysis
   - `analise_expandida_completa.py` - Socioeconomic profiling
   - `analise_completa_corrigida.py` - Base analysis with coding
   
3. **03_sem_modelos/**: Structural Equation Modeling
   - `fix_sem_models.py` - Factor analysis and SEM models
   - `analise_sem_corrigida.py` - Perception → Intention model
   
4. **04_machine_learning/**: ML and advanced analytics
   - `analise_estatistica_avancada.py` - Random Forest, clustering
   - `fix_wtp_analysis.py` - Willingness to Pay analysis
   
5. **05_visualizacoes/**: Diagram generation
   - Various SEM diagram creation scripts
   
6. **06_consolidacao/**: Final consolidation
   - `analise_final.py` - Results synthesis

### Key Data Files
- **Input**: `csv_extraidos/` contains 7 CSV files (Quality, Usage, Perception, etc.)
- **Output**: `analise_estruturada/outputs/` for processed data, visualizations, and reports

## Common Commands

### Run Complete Analysis
```bash
cd analise_estruturada
python executar_analise_completa.py
```

### Run Individual Phases
```bash
# Phase 1: Data preparation
python 01_preparacao/dados_reais_final.py

# Phase 2: Descriptive analysis
python 02_descritiva/analise_expandida_completa.py
python 02_descritiva/analise_completa_corrigida.py

# Phase 3: SEM models
python 03_sem_modelos/fix_sem_models.py
python 03_sem_modelos/analise_sem_corrigida.py

# Phase 4: Machine learning
python 04_machine_learning/analise_estatistica_avancada.py
python 04_machine_learning/fix_wtp_analysis.py

# Phase 5: Visualizations
python 05_visualizacoes/criar_diagrama_sem_storytelling.py

# Phase 6: Consolidation
python 06_consolidacao/analise_final.py
```

### Generate Reports
The main execution script automatically generates verification reports in `outputs/relatorios/`.

## Architecture Notes

### Data Flow
1. Raw CSV data → Data preparation → Coded datasets
2. Coded data → Descriptive analysis + SEM modeling
3. SEM results → Visualizations + ML analysis
4. All results → Final consolidation report

### Key Constructs Analyzed
- **Service Quality**: Infrastructure, reliability, pricing
- **Technology Acceptance**: Adoption patterns and barriers  
- **User Experience**: Satisfaction and expectations
- **Reward Perception**: Acceptance of incentive systems
- **Behavioral Intention**: Usage patterns and future intent
- **Willingness to Pay**: Economic preferences for rewards

### Statistical Models
- **SEM Models**: Perception → Intention relationship (r ≈ 0.896)
- **Factor Analysis**: Construct validation and dimensionality
- **Random Forest**: Feature importance and prediction
- **Clustering**: User segmentation analysis

## Data Requirements

The analysis expects 7 CSV files in `csv_extraidos/`:
- `Qualidade do serviço.csv` (705 rows)
- `Utilização.csv` (708 rows)
- `Percepção novos serviços.csv` (705 rows)
- `Intenção comportamental.csv` (705 rows)
- `Aceitação da tecnologia.csv` (705 rows)
- `Experiência do usuário.csv` (705 rows)
- `Perfil Socioeconomico.csv` (706 rows)

## Testing & Validation

No automated tests are present. Validation is done through:
- Data consistency checks in preparation phase
- Statistical model fit indices (SEM validation)
- Cross-validation in ML models
- Comparison with expected results in verification reports

## Development Workflow

1. Always run the complete pipeline via `executar_analise_completa.py` first
2. For debugging specific phases, run individual scripts
3. Check `outputs/relatorios/RELATORIO_VERIFICACAO_ANALISE.md` for validation
4. Key expected results: 703 valid respondents, SEM R² ≈ 0.80, correlation ≈ 0.896

## Output Interpretation

The analysis generates:
- **Statistical Models**: SEM diagrams showing relationships between constructs
- **Demographics**: Socioeconomic profiling (61.5% female, 59.2% Black, 82.2% high school+)
- **Behavioral Insights**: High intention (4.55/5) vs low service quality (1.64/5)
- **Economic Analysis**: Willingness to pay for different reward types