import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, pearsonr
from factor_analyzer import FactorAnalyzer
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import warnings
warnings.filterwarnings('ignore')

# Configuração global para gráficos
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def carregar_dados():
    """Carregar todos os datasets"""
    print("📁 Carregando datasets...")
    datasets = {}
    
    files = [
        'Qualidade do serviço.csv',
        'Utilização.csv', 
        'Percepção novos serviços.csv',
        'Intenção comportamental.csv',
        'Aceitação da tecnologia.csv',
        'Experiência do usuário.csv',
        'Perfil Socioeconomico.csv'
    ]
    
    for file in files:
        try:
            df = pd.read_csv(f'../../data/raw/csv_extraidos/{file}', encoding='utf-8')
            name = file.replace('.csv', '').replace(' ', '_').lower()
            datasets[name] = df
            print(f"✓ {file}: {len(df)} registros, {len(df.columns)} colunas")
        except Exception as e:
            print(f"✗ Erro ao carregar {file}: {e}")
    
    return datasets

def limpar_colunas(df):
    """Limpar nomes das colunas removendo caracteres especiais"""
    new_columns = []
    for col in df.columns:
        # Remove caracteres especiais comuns
        clean_col = col.strip().replace('\xa0', '').replace('\n', '').replace('\r', '')
        new_columns.append(clean_col)
    df.columns = new_columns
    return df

def analise_perfil_socioeconomico_completa(datasets):
    """Análise completa do perfil socioeconômico"""
    print("\n🔍 ANÁLISE COMPLETA DO PERFIL SOCIOECONÔMICO")
    print("="*60)
    
    df = limpar_colunas(datasets['perfil_socioeconomico'].copy())
    
    # Identificar colunas dinamicamente
    gender_col = None
    race_col = None
    age_col = None
    education_col = None
    profession_col = None
    children_col = None
    income_col = None
    
    for col in df.columns:
        if 'gênero' in col.lower() or 'genero' in col.lower():
            gender_col = col
        elif 'raça' in col.lower() or 'raca' in col.lower():
            race_col = col
        elif 'idade' in col.lower():
            age_col = col
        elif 'escolaridade' in col.lower():
            education_col = col
        elif 'profissional' in col.lower():
            profession_col = col
        elif 'filhos' in col.lower():
            children_col = col
        elif 'renda' in col.lower():
            income_col = col
    
    print(f"Colunas identificadas:")
    print(f"Gênero: {gender_col}")
    print(f"Raça: {race_col}")
    print(f"Idade: {age_col}")
    print(f"Escolaridade: {education_col}")
    print(f"Profissão: {profession_col}")
    print(f"Filhos: {children_col}")
    print(f"Renda: {income_col}")
    
    resultados = {}
    
    # 1. ANÁLISE DE GÊNERO
    if gender_col:
        print(f"\n1. DISTRIBUIÇÃO POR GÊNERO")
        print("-"*30)
        gender_dist = df[gender_col].value_counts()
        gender_pct = df[gender_col].value_counts(normalize=True) * 100
        
        for cat, count in gender_dist.items():
            pct = gender_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        resultados['genero'] = {
            'distribuicao': gender_dist.to_dict(),
            'percentuais': gender_pct.to_dict()
        }
    
    # 2. ANÁLISE DE ETNIA/RAÇA
    if race_col:
        print(f"\n2. DISTRIBUIÇÃO POR ETNIA/RAÇA")
        print("-"*30)
        race_dist = df[race_col].value_counts()
        race_pct = df[race_col].value_counts(normalize=True) * 100
        
        for cat, count in race_dist.items():
            pct = race_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        resultados['raca'] = {
            'distribuicao': race_dist.to_dict(),
            'percentuais': race_pct.to_dict()
        }
    
    # 3. ANÁLISE DE ESCOLARIDADE
    if education_col:
        print(f"\n3. DISTRIBUIÇÃO POR NÍVEL DE ESCOLARIDADE")
        print("-"*40)
        edu_dist = df[education_col].value_counts()
        edu_pct = df[education_col].value_counts(normalize=True) * 100
        
        # Ordenar por ordem educacional
        ordem_educacao = {
            'Fundamental': 1,
            'Ensino Médio': 2, 
            'Técnico': 2,
            'Graduação': 3,
            'Pós-graduação': 4
        }
        
        for cat, count in edu_dist.items():
            pct = edu_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        resultados['escolaridade'] = {
            'distribuicao': edu_dist.to_dict(),
            'percentuais': edu_pct.to_dict()
        }
    
    # 4. ANÁLISE DE IDADE
    if age_col:
        print(f"\n4. DISTRIBUIÇÃO POR FAIXA ETÁRIA")
        print("-"*30)
        age_dist = df[age_col].value_counts()
        age_pct = df[age_col].value_counts(normalize=True) * 100
        
        for cat, count in age_dist.items():
            pct = age_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        resultados['idade'] = {
            'distribuicao': age_dist.to_dict(),
            'percentuais': age_pct.to_dict()
        }
    
    # 5. ANÁLISE DE SITUAÇÃO PROFISSIONAL
    if profession_col:
        print(f"\n5. DISTRIBUIÇÃO POR SITUAÇÃO PROFISSIONAL")
        print("-"*40)
        prof_dist = df[profession_col].value_counts()
        prof_pct = df[profession_col].value_counts(normalize=True) * 100
        
        for cat, count in prof_dist.items():
            pct = prof_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        resultados['profissao'] = {
            'distribuicao': prof_dist.to_dict(),
            'percentuais': prof_pct.to_dict()
        }
    
    # 6. ANÁLISE DE FILHOS
    if children_col:
        print(f"\n6. DISTRIBUIÇÃO POR NÚMERO DE FILHOS")
        print("-"*35)
        try:
            children_dist = df[children_col].value_counts().sort_index()
            children_pct = df[children_col].value_counts(normalize=True).sort_index() * 100
            
            for cat, count in children_dist.items():
                pct = children_pct[cat]
                print(f"  {cat} filhos: {count} ({pct:.1f}%)")
            
            # Estatísticas
            children_numeric = pd.to_numeric(df[children_col], errors='coerce')
            media_filhos = children_numeric.mean()
            print(f"\n  Média de filhos: {media_filhos:.2f}")
            
            resultados['filhos'] = {
                'distribuicao': children_dist.to_dict(),
                'percentuais': children_pct.to_dict(),
                'media': media_filhos
            }
        except Exception as e:
            print(f"  Erro na análise de filhos: {e}")
    
    # 7. ANÁLISE DE RENDA
    if income_col:
        print(f"\n7. DISTRIBUIÇÃO POR FAIXA DE RENDA")
        print("-"*35)
        income_dist = df[income_col].value_counts()
        income_pct = df[income_col].value_counts(normalize=True) * 100
        
        for cat, count in income_dist.items():
            pct = income_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        resultados['renda'] = {
            'distribuicao': income_dist.to_dict(),
            'percentuais': income_pct.to_dict()
        }
    
    return resultados

def analise_utilizacao_completa(datasets):
    """Análise completa de utilização do transporte"""
    print("\n🚌 ANÁLISE COMPLETA DE UTILIZAÇÃO DO TRANSPORTE")
    print("="*60)
    
    df = limpar_colunas(datasets['utilização'].copy())
    
    # Identificar colunas
    modal_col = None
    license_col = None
    vehicle_col = None
    frequency_col = None
    payment_col = None
    
    for col in df.columns:
        if 'forma' in col.lower() and 'viagens' in col.lower():
            modal_col = col
        elif 'carteira' in col.lower() and 'motorista' in col.lower():
            license_col = col
        elif 'veículo próprio' in col.lower() or 'veiculo proprio' in col.lower():
            vehicle_col = col
        elif 'frequência' in col.lower() or 'frequencia' in col.lower():
            frequency_col = col
        elif 'pagamento' in col.lower():
            payment_col = col
    
    resultados = {}
    
    # 1. ANÁLISE MODAL
    if modal_col:
        print(f"\n1. DISTRIBUIÇÃO MODAL (Principal meio de transporte)")
        print("-"*50)
        modal_dist = df[modal_col].value_counts()
        modal_pct = df[modal_col].value_counts(normalize=True) * 100
        
        for cat, count in modal_dist.items():
            pct = modal_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        resultados['modal'] = {
            'distribuicao': modal_dist.to_dict(),
            'percentuais': modal_pct.to_dict()
        }
    
    # 2. ANÁLISE DE CARTEIRA DE MOTORISTA
    if license_col:
        print(f"\n2. POSSE DE CARTEIRA DE MOTORISTA")
        print("-"*35)
        license_dist = df[license_col].value_counts()
        license_pct = df[license_col].value_counts(normalize=True) * 100
        
        for cat, count in license_dist.items():
            pct = license_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        # Categorizar por tipo
        tem_carteira = df[license_col] != 'Não tenho'
        pct_com_carteira = tem_carteira.sum() / len(df) * 100
        print(f"\n  RESUMO: {pct_com_carteira:.1f}% possuem algum tipo de carteira")
        
        resultados['carteira'] = {
            'distribuicao': license_dist.to_dict(),
            'percentuais': license_pct.to_dict(),
            'percentual_com_carteira': pct_com_carteira
        }
    
    # 3. ANÁLISE DE VEÍCULO PRÓPRIO
    if vehicle_col:
        print(f"\n3. POSSE DE VEÍCULO PRÓPRIO")
        print("-"*30)
        vehicle_dist = df[vehicle_col].value_counts()
        vehicle_pct = df[vehicle_col].value_counts(normalize=True) * 100
        
        for cat, count in vehicle_dist.items():
            pct = vehicle_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        resultados['veiculo'] = {
            'distribuicao': vehicle_dist.to_dict(),
            'percentuais': vehicle_pct.to_dict()
        }
    
    # 4. ANÁLISE DE FREQUÊNCIA DE USO DO TP
    if frequency_col:
        print(f"\n4. FREQUÊNCIA DE USO DO TRANSPORTE PÚBLICO")
        print("-"*45)
        freq_dist = df[frequency_col].value_counts()
        freq_pct = df[frequency_col].value_counts(normalize=True) * 100
        
        for cat, count in freq_dist.items():
            pct = freq_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        # Categorizar usuários
        usuarios_ativos = ~df[frequency_col].str.contains('Não utilizo', na=False)
        pct_usuarios = usuarios_ativos.sum() / len(df) * 100
        print(f"\n  RESUMO: {pct_usuarios:.1f}% são usuários ativos do transporte público")
        
        resultados['frequencia'] = {
            'distribuicao': freq_dist.to_dict(),
            'percentuais': freq_pct.to_dict(),
            'percentual_usuarios_ativos': pct_usuarios
        }
    
    # 5. ANÁLISE DE MEIO DE PAGAMENTO
    if payment_col:
        print(f"\n5. MEIO DE PAGAMENTO PREFERIDO")
        print("-"*30)
        payment_dist = df[payment_col].value_counts()
        payment_pct = df[payment_col].value_counts(normalize=True) * 100
        
        for cat, count in payment_dist.items():
            pct = payment_pct[cat]
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        resultados['pagamento'] = {
            'distribuicao': payment_dist.to_dict(),
            'percentuais': payment_pct.to_dict()
        }
    
    return resultados

def analises_cruzadas_avancadas(datasets):
    """Análises cruzadas avançadas entre variáveis"""
    print("\n🔄 ANÁLISES CRUZADAS AVANÇADAS")
    print("="*50)
    
    # Combinar dados de perfil e utilização
    perfil = limpar_colunas(datasets['perfil_socioeconomico'].copy())
    utilizacao = limpar_colunas(datasets['utilização'].copy())
    
    # Merge dos dados
    dados_combinados = pd.merge(perfil, utilizacao, on='ID', how='inner')
    
    print(f"Dados combinados: {len(dados_combinados)} registros")
    
    resultados = {}
    
    # 1. ESCOLARIDADE vs USO DO TRANSPORTE PÚBLICO
    education_col = None
    modal_col = None
    
    for col in perfil.columns:
        if 'escolaridade' in col.lower():
            education_col = col
            break
    
    for col in utilizacao.columns:
        if 'forma' in col.lower() and 'viagens' in col.lower():
            modal_col = col
            break
    
    if education_col and modal_col:
        print(f"\n1. ESCOLARIDADE vs ESCOLHA MODAL")
        print("-"*35)
        
        tabela_cruzada = pd.crosstab(
            dados_combinados[education_col], 
            dados_combinados[modal_col], 
            normalize='index'
        ) * 100
        
        print("Percentual por linha (escolaridade):")
        for edu in tabela_cruzada.index:
            print(f"\n{edu}:")
            for modal in tabela_cruzada.columns:
                if tabela_cruzada.loc[edu, modal] > 5:  # Só mostra se > 5%
                    print(f"  {modal}: {tabela_cruzada.loc[edu, modal]:.1f}%")
        
        # Teste qui-quadrado
        chi2, p_value, dof, expected = chi2_contingency(pd.crosstab(
            dados_combinados[education_col], 
            dados_combinados[modal_col]
        ))
        
        print(f"\nTeste Qui-quadrado: χ² = {chi2:.3f}, p = {p_value:.3f}")
        if p_value < 0.05:
            print("→ Há associação significativa entre escolaridade e escolha modal")
        else:
            print("→ Não há associação significativa")
        
        resultados['escolaridade_modal'] = {
            'tabela_cruzada': tabela_cruzada.to_dict(),
            'chi2': chi2,
            'p_value': p_value,
            'significativo': p_value < 0.05
        }
    
    # 2. ETNIA vs USO DO TRANSPORTE PÚBLICO
    race_col = None
    for col in perfil.columns:
        if 'raça' in col.lower() or 'raca' in col.lower():
            race_col = col
            break
    
    if race_col and modal_col:
        print(f"\n2. ETNIA vs ESCOLHA MODAL")
        print("-"*25)
        
        tabela_cruzada_raca = pd.crosstab(
            dados_combinados[race_col], 
            dados_combinados[modal_col], 
            normalize='index'
        ) * 100
        
        print("Percentual por linha (etnia):")
        for raca in tabela_cruzada_raca.index:
            uso_tp = 0
            if 'Utilizo o transporte público' in tabela_cruzada_raca.columns:
                uso_tp = tabela_cruzada_raca.loc[raca, 'Utilizo o transporte público']
            print(f"  {raca}: {uso_tp:.1f}% usam TP")
        
        resultados['etnia_modal'] = {
            'tabela_cruzada': tabela_cruzada_raca.to_dict()
        }
    
    # 3. CARTEIRA DE MOTORISTA vs USO DO TP
    license_col = None
    for col in utilizacao.columns:
        if 'carteira' in col.lower() and 'motorista' in col.lower():
            license_col = col
            break
    
    if license_col and modal_col:
        print(f"\n3. CARTEIRA DE MOTORISTA vs ESCOLHA MODAL")
        print("-"*40)
        
        # Simplificar categorias de carteira
        dados_combinados['tem_carteira'] = dados_combinados[license_col] != 'Não tenho'
        
        tabela_carteira = pd.crosstab(
            dados_combinados['tem_carteira'], 
            dados_combinados[modal_col], 
            normalize='index'
        ) * 100
        
        print("Percentual por posse de carteira:")
        for tem_carteira in [True, False]:
            label = "COM carteira" if tem_carteira else "SEM carteira"
            uso_tp = 0
            if 'Utilizo o transporte público' in tabela_carteira.columns:
                uso_tp = tabela_carteira.loc[tem_carteira, 'Utilizo o transporte público']
            print(f"  {label}: {uso_tp:.1f}% usam TP")
        
        resultados['carteira_modal'] = {
            'tabela_cruzada': tabela_carteira.to_dict()
        }
    
    # 4. RENDA vs USO DO TRANSPORTE PÚBLICO
    income_col = None
    for col in perfil.columns:
        if 'renda' in col.lower():
            income_col = col
            break
    
    if income_col and modal_col:
        print(f"\n4. RENDA vs ESCOLHA MODAL")
        print("-"*25)
        
        tabela_renda = pd.crosstab(
            dados_combinados[income_col], 
            dados_combinados[modal_col], 
            normalize='index'
        ) * 100
        
        print("Percentual por faixa de renda:")
        for renda in tabela_renda.index:
            uso_tp = 0
            if 'Utilizo o transporte público' in tabela_renda.columns:
                uso_tp = tabela_renda.loc[renda, 'Utilizo o transporte público']
            print(f"  {renda}: {uso_tp:.1f}% usam TP")
        
        resultados['renda_modal'] = {
            'tabela_cruzada': tabela_renda.to_dict()
        }
    
    return resultados

def analise_qualidade_detalhada(datasets):
    """Análise detalhada da qualidade do serviço"""
    print("\n⭐ ANÁLISE DETALHADA DA QUALIDADE DO SERVIÇO")
    print("="*55)
    
    df = limpar_colunas(datasets['qualidade_do_serviço'].copy())
    
    # Identificar colunas de qualidade (excluindo ID)
    quality_cols = [col for col in df.columns if col != 'ID']
    
    print(f"Atributos de qualidade analisados: {len(quality_cols)}")
    
    resultados = {}
    
    # 1. ESTATÍSTICAS DESCRITIVAS POR ATRIBUTO
    print(f"\n1. ESTATÍSTICAS DESCRITIVAS POR ATRIBUTO")
    print("-"*45)
    
    stats_summary = []
    
    for col in quality_cols:
        try:
            # Converter para numérico se possível
            values = pd.to_numeric(df[col], errors='coerce')
            
            if values.notna().sum() > 0:
                media = values.mean()
                mediana = values.median()
                desvio = values.std()
                minimo = values.min()
                maximo = values.max()
                
                print(f"\n{col}:")
                print(f"  Média: {media:.2f}")
                print(f"  Mediana: {mediana:.2f}")
                print(f"  Desvio Padrão: {desvio:.2f}")
                print(f"  Min-Max: {minimo:.1f} - {maximo:.1f}")
                
                stats_summary.append({
                    'atributo': col,
                    'media': media,
                    'mediana': mediana,
                    'desvio': desvio,
                    'min': minimo,
                    'max': maximo
                })
        except:
            print(f"  {col}: Não numérico")
    
    # 2. RANKING DOS ATRIBUTOS
    print(f"\n2. RANKING DOS ATRIBUTOS (por média)")
    print("-"*35)
    
    stats_df = pd.DataFrame(stats_summary)
    if not stats_df.empty:
        stats_df_sorted = stats_df.sort_values('media', ascending=False)
        
        print("Melhores avaliados:")
        for i, row in stats_df_sorted.head(5).iterrows():
            print(f"  {i+1}. {row['atributo']}: {row['media']:.2f}")
        
        print("\nPiores avaliados:")
        for i, row in stats_df_sorted.tail(5).iterrows():
            print(f"  {len(stats_df_sorted)-i}. {row['atributo']}: {row['media']:.2f}")
        
        resultados['ranking'] = {
            'melhores': stats_df_sorted.head(5).to_dict('records'),
            'piores': stats_df_sorted.tail(5).to_dict('records')
        }
    
    # 3. ANÁLISE DE CORRELAÇÕES
    print(f"\n3. CORRELAÇÕES ENTRE ATRIBUTOS")
    print("-"*30)
    
    # Criar matriz de dados numéricos
    numeric_data = pd.DataFrame()
    for col in quality_cols:
        values = pd.to_numeric(df[col], errors='coerce')
        if values.notna().sum() > 10:  # Mínimo de 10 valores válidos
            numeric_data[col] = values
    
    if not numeric_data.empty:
        corr_matrix = numeric_data.corr()
        
        # Encontrar correlações mais altas (excluindo diagonal)
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if not pd.isna(corr_val):
                    corr_pairs.append({
                        'atributo1': corr_matrix.columns[i],
                        'atributo2': corr_matrix.columns[j],
                        'correlacao': corr_val
                    })
        
        corr_pairs_df = pd.DataFrame(corr_pairs)
        corr_pairs_df = corr_pairs_df.sort_values('correlacao', key=abs, ascending=False)
        
        print("Correlações mais fortes:")
        for _, row in corr_pairs_df.head(10).iterrows():
            print(f"  {row['atributo1']} ↔ {row['atributo2']}: {row['correlacao']:.3f}")
        
        resultados['correlacoes'] = corr_pairs_df.head(20).to_dict('records')
    
    return resultados

def analise_recompensas_detalhada(datasets):
    """Análise detalhada das percepções sobre recompensas"""
    print("\n🎁 ANÁLISE DETALHADA DE RECOMPENSAS")
    print("="*45)
    
    # Analisar percepção e intenção comportamental
    percepcao = limpar_colunas(datasets['percepção_novos_serviços'].copy())
    intencao = limpar_colunas(datasets['intenção_comportamental'].copy())
    
    resultados = {}
    
    # 1. ANÁLISE DE PERCEPÇÃO
    print(f"\n1. ANÁLISE DE PERCEPÇÃO DE RECOMPENSAS")
    print("-"*40)
    
    perception_cols = [col for col in percepcao.columns if col != 'ID']
    
    perception_stats = []
    for col in perception_cols:
        values = pd.to_numeric(percepcao[col], errors='coerce')
        if values.notna().sum() > 0:
            media = values.mean()
            perception_stats.append({
                'tipo_recompensa': col,
                'media_percepcao': media
            })
    
    if perception_stats:
        perception_df = pd.DataFrame(perception_stats)
        perception_df = perception_df.sort_values('media_percepcao', ascending=False)
        
        print("Recompensas mais valorizadas:")
        for _, row in perception_df.head(5).iterrows():
            print(f"  {row['tipo_recompensa']}: {row['media_percepcao']:.2f}")
        
        resultados['percepcao'] = perception_df.to_dict('records')
    
    # 2. ANÁLISE DE INTENÇÃO COMPORTAMENTAL
    print(f"\n2. ANÁLISE DE INTENÇÃO COMPORTAMENTAL")
    print("-"*40)
    
    intention_cols = [col for col in intencao.columns if col != 'ID']
    
    intention_stats = []
    for col in intention_cols:
        values = pd.to_numeric(intencao[col], errors='coerce')
        if values.notna().sum() > 0:
            media = values.mean()
            intention_stats.append({
                'tipo_incentivo': col,
                'media_intencao': media
            })
    
    if intention_stats:
        intention_df = pd.DataFrame(intention_stats)
        intention_df = intention_df.sort_values('media_intencao', ascending=False)
        
        print("Incentivos com maior potencial:")
        for _, row in intention_df.head(5).iterrows():
            print(f"  {row['tipo_incentivo']}: {row['media_intencao']:.2f}")
        
        resultados['intencao'] = intention_df.to_dict('records')
    
    return resultados

def gerar_relatorio_expandido(datasets, all_results):
    """Gerar relatório expandido completo"""
    print("\n📊 GERANDO RELATÓRIO EXPANDIDO COMPLETO")
    print("="*50)
    
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    filename = f"RELATORIO_EXPANDIDO_COMPLETO_{timestamp}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO EXPANDIDO COMPLETO - ANÁLISE DE TRANSPORTE PÚBLICO E RECOMPENSAS\n\n")
        f.write(f"**Data de Geração:** {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # Resumo Executivo
        f.write("## RESUMO EXECUTIVO\n\n")
        f.write("Esta análise expandida apresenta insights detalhados sobre:\n")
        f.write("- **Perfil Socioeconômico Completo**: Gênero, etnia, escolaridade, renda, situação profissional\n")
        f.write("- **Comportamento de Utilização**: Modal split, posse de carteira, veículo próprio\n")
        f.write("- **Qualidade do Serviço**: Avaliação detalhada de todos os atributos\n")
        f.write("- **Sistema de Recompensas**: Percepção e intenção comportamental\n")
        f.write("- **Análises Cruzadas**: Interações entre variáveis socioeconômicas e uso do transporte\n\n")
        
        # Perfil Socioeconômico
        if 'perfil' in all_results:
            f.write("## 1. PERFIL SOCIOECONÔMICO DETALHADO\n\n")
            
            perfil_results = all_results['perfil']
            
            if 'genero' in perfil_results:
                f.write("### 1.1 Distribuição por Gênero\n\n")
                for cat, pct in perfil_results['genero']['percentuais'].items():
                    f.write(f"- **{cat}**: {pct:.1f}%\n")
                f.write("\n")
            
            if 'raca' in perfil_results:
                f.write("### 1.2 Distribuição por Etnia/Raça\n\n")
                for cat, pct in perfil_results['raca']['percentuais'].items():
                    f.write(f"- **{cat}**: {pct:.1f}%\n")
                f.write("\n")
            
            if 'escolaridade' in perfil_results:
                f.write("### 1.3 Distribuição por Escolaridade\n\n")
                for cat, pct in perfil_results['escolaridade']['percentuais'].items():
                    f.write(f"- **{cat}**: {pct:.1f}%\n")
                f.write("\n")
            
            if 'renda' in perfil_results:
                f.write("### 1.4 Distribuição por Renda\n\n")
                for cat, pct in perfil_results['renda']['percentuais'].items():
                    f.write(f"- **{cat}**: {pct:.1f}%\n")
                f.write("\n")
        
        # Utilização
        if 'utilizacao' in all_results:
            f.write("## 2. ANÁLISE DE UTILIZAÇÃO DO TRANSPORTE\n\n")
            
            util_results = all_results['utilizacao']
            
            if 'carteira' in util_results:
                f.write("### 2.1 Posse de Carteira de Motorista\n\n")
                f.write(f"**{util_results['carteira']['percentual_com_carteira']:.1f}% possuem algum tipo de carteira**\n\n")
                for cat, pct in util_results['carteira']['percentuais'].items():
                    f.write(f"- **{cat}**: {pct:.1f}%\n")
                f.write("\n")
            
            if 'modal' in util_results:
                f.write("### 2.2 Distribuição Modal\n\n")
                for cat, pct in util_results['modal']['percentuais'].items():
                    f.write(f"- **{cat}**: {pct:.1f}%\n")
                f.write("\n")
        
        # Qualidade
        if 'qualidade' in all_results:
            f.write("## 3. ANÁLISE DE QUALIDADE DO SERVIÇO\n\n")
            
            qual_results = all_results['qualidade']
            
            if 'ranking' in qual_results:
                f.write("### 3.1 Ranking de Atributos\n\n")
                f.write("**Melhores Avaliados:**\n")
                for i, attr in enumerate(qual_results['ranking']['melhores'], 1):
                    f.write(f"{i}. **{attr['atributo']}**: {attr['media']:.2f}\n")
                
                f.write("\n**Piores Avaliados:**\n")
                for i, attr in enumerate(qual_results['ranking']['piores'], 1):
                    f.write(f"{i}. **{attr['atributo']}**: {attr['media']:.2f}\n")
                f.write("\n")
        
        # Análises Cruzadas
        if 'cruzadas' in all_results:
            f.write("## 4. ANÁLISES CRUZADAS\n\n")
            
            cruz_results = all_results['cruzadas']
            
            if 'escolaridade_modal' in cruz_results and cruz_results['escolaridade_modal']['significativo']:
                f.write("### 4.1 Escolaridade vs Escolha Modal\n\n")
                f.write(f"**Teste Qui-quadrado**: χ² = {cruz_results['escolaridade_modal']['chi2']:.3f}, ")
                f.write(f"p = {cruz_results['escolaridade_modal']['p_value']:.3f}\n")
                f.write("→ **Há associação significativa entre escolaridade e escolha modal**\n\n")
        
        f.write("---\n\n")
        f.write("## CONCLUSÕES E RECOMENDAÇÕES\n\n")
        f.write("### Principais Insights:\n\n")
        f.write("1. **Perfil Diversificado**: Base de usuários heterogênea em termos socioeconômicos\n")
        f.write("2. **Oportunidades de Melhoria**: Atributos críticos identificados na qualidade\n")
        f.write("3. **Potencial de Recompensas**: Sistema de incentivos com alto potencial\n")
        f.write("4. **Segmentação Relevante**: Diferenças comportamentais por perfil socioeconômico\n\n")
        
        f.write("### Recomendações Estratégicas:\n\n")
        f.write("1. **Melhoria Direcionada**: Focar nos atributos de menor avaliação\n")
        f.write("2. **Segmentação de Políticas**: Adaptar estratégias por perfil socioeconômico\n")
        f.write("3. **Sistema de Recompensas**: Implementar programa de incentivos\n")
        f.write("4. **Monitoramento Contínuo**: Acompanhar evolução dos indicadores\n\n")
    
    print(f"✓ Relatório salvo como: {filename}")
    return filename

def main():
    """Função principal para executar toda a análise expandida"""
    print("🚀 INICIANDO ANÁLISE EXPANDIDA COMPLETA")
    print("="*60)
    
    # Carregar dados
    datasets = carregar_dados()
    
    if not datasets:
        print("❌ Nenhum dataset carregado. Verificar arquivos CSV.")
        return
    
    # Executar todas as análises
    all_results = {}
    
    try:
        # 1. Perfil Socioeconômico
        all_results['perfil'] = analise_perfil_socioeconomico_completa(datasets)
        
        # 2. Utilização
        all_results['utilizacao'] = analise_utilizacao_completa(datasets)
        
        # 3. Qualidade
        all_results['qualidade'] = analise_qualidade_detalhada(datasets)
        
        # 4. Recompensas
        all_results['recompensas'] = analise_recompensas_detalhada(datasets)
        
        # 5. Análises Cruzadas
        all_results['cruzadas'] = analises_cruzadas_avancadas(datasets)
        
        # 6. Gerar relatório
        relatorio = gerar_relatorio_expandido(datasets, all_results)
        
        print(f"\n🎉 ANÁLISE EXPANDIDA CONCLUÍDA COM SUCESSO!")
        print(f"📄 Relatório gerado: {relatorio}")
        
    except Exception as e:
        print(f"❌ Erro durante a análise: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 