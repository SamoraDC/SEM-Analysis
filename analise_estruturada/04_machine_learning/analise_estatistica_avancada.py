import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, f_oneway, kruskal
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings
warnings.filterwarnings('ignore')

# Configuração para gráficos
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 12
sns.set_palette("Set2")

def carregar_e_preparar_dados():
    """Carregar e preparar dados para análises avançadas"""
    print("📊 CARREGANDO E PREPARANDO DADOS PARA ANÁLISES AVANÇADAS")
    print("="*70)
    
    # Carregar datasets
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
            df = pd.read_csv(f'csv_extraidos/{file}', encoding='utf-8')
            # Limpar nomes das colunas
            df.columns = [col.strip().replace('\xa0', '').replace('\n', '').replace('\r', '') 
                         for col in df.columns]
            name = file.replace('.csv', '').replace(' ', '_').lower()
            datasets[name] = df
            print(f"✓ {file}: {len(df)} registros")
        except Exception as e:
            print(f"✗ Erro ao carregar {file}: {e}")
    
    # Criar dataset integrado
    base_data = datasets['perfil_socioeconomico'].copy()
    
    for name, df in datasets.items():
        if name != 'perfil_socioeconomico':
            base_data = pd.merge(base_data, df, on='ID', how='left')
    
    print(f"\n✓ Dataset integrado criado: {len(base_data)} registros, {len(base_data.columns)} colunas")
    
    return base_data, datasets

def analise_anova_escolaridade_qualidade(data):
    """ANOVA: Escolaridade vs Qualidade do Serviço"""
    print("\n📈 ANÁLISE ANOVA: ESCOLARIDADE vs QUALIDADE")
    print("="*50)
    
    # Identificar coluna de escolaridade
    education_col = None
    for col in data.columns:
        if 'escolaridade' in col.lower():
            education_col = col
            break
    
    if not education_col:
        print("❌ Coluna de escolaridade não encontrada")
        return None
    
    # Identificar colunas de qualidade
    quality_cols = []
    for col in data.columns:
        if any(palavra in col.lower() for palavra in ['acessibilidade', 'atendimento', 'conforto', 
                                                     'custo', 'frequência', 'informação', 'limpeza',
                                                     'pontualidade', 'segurança', 'temperatura',
                                                     'tempo', 'velocidade']):
            quality_cols.append(col)
    
    if not quality_cols:
        print("❌ Colunas de qualidade não encontradas")
        return None
    
    print(f"Analisando {len(quality_cols)} atributos de qualidade por escolaridade...")
    
    resultados_anova = []
    
    for qual_col in quality_cols:
        try:
            # Converter valores para numérico
            data_clean = data[[education_col, qual_col]].dropna()
            data_clean[qual_col] = pd.to_numeric(data_clean[qual_col], errors='coerce')
            data_clean = data_clean.dropna()
            
            if len(data_clean) < 10:
                continue
            
            # Preparar grupos para ANOVA
            grupos = []
            labels = []
            
            for edu_level in data_clean[education_col].unique():
                group_values = data_clean[data_clean[education_col] == edu_level][qual_col]
                if len(group_values) >= 3:  # Mínimo 3 observações por grupo
                    grupos.append(group_values.values)
                    labels.append(edu_level)
            
            if len(grupos) >= 2:
                # Executar ANOVA
                f_stat, p_value = f_oneway(*grupos)
                
                # Calcular médias por grupo
                group_means = {}
                for i, label in enumerate(labels):
                    group_means[label] = np.mean(grupos[i])
                
                resultado = {
                    'atributo': qual_col,
                    'f_statistic': f_stat,
                    'p_value': p_value,
                    'significativo': p_value < 0.05,
                    'medias_grupos': group_means
                }
                
                resultados_anova.append(resultado)
                
                print(f"\n{qual_col}:")
                print(f"  F = {f_stat:.3f}, p = {p_value:.4f}")
                if p_value < 0.05:
                    print("  → Diferença SIGNIFICATIVA entre grupos de escolaridade")
                    # Mostrar médias
                    for label, media in group_means.items():
                        print(f"    {label}: {media:.2f}")
                else:
                    print("  → Não há diferença significativa")
        
        except Exception as e:
            print(f"  Erro em {qual_col}: {e}")
    
    return resultados_anova

def analise_regressao_renda_uso_tp(data):
    """Regressão: Renda vs Uso do Transporte Público"""
    print("\n💰 ANÁLISE DE REGRESSÃO: RENDA vs USO DO TP")
    print("="*50)
    
    # Identificar colunas
    income_col = None
    transport_col = None
    
    for col in data.columns:
        if 'renda' in col.lower():
            income_col = col
        elif 'forma' in col.lower() and 'viagens' in col.lower():
            transport_col = col
    
    if not income_col or not transport_col:
        print("❌ Colunas necessárias não encontradas")
        return None
    
    # Preparar dados
    data_clean = data[[income_col, transport_col]].dropna()
    
    # Codificar renda como ordinal
    renda_mapping = {
        'Não possuo renda': 0,
        'Até 1 salário mínimo:  R$ 1.302': 1,
        'De 1 a 2 salários mínimos: R$ 1.302 a R$ 2.604': 2,
        'De 2 a 3 salários mínimos: R$ 2.604 a R$ 3.906': 3,
        'De 3 a 5 salários mínimos: R$ 3.906 a R$ 6.510': 4,
        'De 5 a 10 salários mínimos: R$ 6.510 a R$ 13.020': 5,
        'Acima de 10 salários mínimos:  R$ 13.020': 6
    }
    
    # Codificar uso do TP como binário
    data_clean['renda_ordinal'] = data_clean[income_col].map(renda_mapping)
    data_clean['usa_tp'] = (data_clean[transport_col] == 'Utilizo o transporte público').astype(int)
    
    # Remover valores não mapeados
    data_clean = data_clean.dropna()
    
    if len(data_clean) < 20:
        print("❌ Dados insuficientes para regressão")
        return None
    
    # Regressão logística
    X = data_clean['renda_ordinal']
    y = data_clean['usa_tp']
    
    # Adicionar constante
    X_const = sm.add_constant(X)
    
    # Ajustar modelo
    modelo_logit = sm.Logit(y, X_const).fit(disp=0)
    
    print(f"Regressão Logística: Renda → Uso do TP")
    print(f"Pseudo R²: {modelo_logit.prsquared:.3f}")
    print(f"AIC: {modelo_logit.aic:.1f}")
    
    # Coeficientes
    coef_renda = modelo_logit.params['renda_ordinal']
    p_value = modelo_logit.pvalues['renda_ordinal']
    
    print(f"Coeficiente Renda: {coef_renda:.3f} (p = {p_value:.4f})")
    
    if p_value < 0.05:
        odds_ratio = np.exp(coef_renda)
        print(f"Odds Ratio: {odds_ratio:.3f}")
        if coef_renda < 0:
            print("→ Maior renda REDUZ probabilidade de usar TP")
        else:
            print("→ Maior renda AUMENTA probabilidade de usar TP")
    else:
        print("→ Renda NÃO influencia significativamente o uso do TP")
    
    # Calcular percentuais por faixa de renda
    print(f"\nPercentuais de uso do TP por faixa de renda:")
    for renda_cat, renda_num in renda_mapping.items():
        subset = data_clean[data_clean['renda_ordinal'] == renda_num]
        if len(subset) > 0:
            pct_uso = subset['usa_tp'].mean() * 100
            print(f"  {renda_cat}: {pct_uso:.1f}%")
    
    return {
        'modelo': modelo_logit,
        'coeficiente': coef_renda,
        'p_value': p_value,
        'pseudo_r2': modelo_logit.prsquared,
        'significativo': p_value < 0.05
    }

def analise_clusters_perfil_usuarios(data):
    """Análise de Clusters: Perfil dos Usuários"""
    print("\n🎯 ANÁLISE DE CLUSTERS: PERFIL DOS USUÁRIOS")
    print("="*50)
    
    # Selecionar variáveis para clustering
    cluster_vars = []
    
    # Identificar colunas numéricas relevantes
    for col in data.columns:
        if any(palavra in col.lower() for palavra in ['qualidade', 'satisfação', 'recompensa', 
                                                     'intenção', 'percepção']):
            # Tentar converter para numérico
            try:
                numeric_values = pd.to_numeric(data[col], errors='coerce')
                if numeric_values.notna().sum() > len(data) * 0.5:  # Pelo menos 50% valores válidos
                    cluster_vars.append(col)
            except:
                continue
    
    if len(cluster_vars) < 3:
        print("❌ Variáveis insuficientes para clustering")
        return None
    
    print(f"Variáveis selecionadas para clustering: {len(cluster_vars)}")
    
    # Preparar dados
    cluster_data = data[cluster_vars].copy()
    
    # Converter para numérico
    for col in cluster_vars:
        cluster_data[col] = pd.to_numeric(cluster_data[col], errors='coerce')
    
    # Remover linhas com valores faltantes
    cluster_data = cluster_data.dropna()
    
    if len(cluster_data) < 50:
        print("❌ Dados insuficientes após limpeza")
        return None
    
    print(f"Dataset final para clustering: {len(cluster_data)} observações")
    
    # Padronizar dados
    scaler = StandardScaler()
    cluster_data_scaled = scaler.fit_transform(cluster_data)
    
    # Determinar número ótimo de clusters (método do cotovelo)
    inertias = []
    K_range = range(2, 11)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(cluster_data_scaled)
        inertias.append(kmeans.inertia_)
    
    # Escolher k=4 como padrão (pode ser ajustado)
    k_optimal = 4
    
    # Aplicar K-means
    kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(cluster_data_scaled)
    
    # Adicionar labels aos dados originais
    cluster_data['Cluster'] = cluster_labels
    
    print(f"\nClusters identificados (k={k_optimal}):")
    
    # Analisar características de cada cluster
    cluster_summary = []
    
    for cluster_id in range(k_optimal):
        cluster_subset = cluster_data[cluster_data['Cluster'] == cluster_id]
        n_obs = len(cluster_subset)
        pct_total = n_obs / len(cluster_data) * 100
        
        print(f"\nCluster {cluster_id + 1}: {n_obs} observações ({pct_total:.1f}%)")
        
        # Características do cluster
        cluster_means = {}
        for var in cluster_vars:
            mean_val = cluster_subset[var].mean()
            cluster_means[var] = mean_val
            print(f"  {var}: {mean_val:.2f}")
        
        cluster_summary.append({
            'cluster_id': cluster_id + 1,
            'n_observacoes': n_obs,
            'percentual': pct_total,
            'caracteristicas': cluster_means
        })
    
    # PCA para visualização
    pca = PCA(n_components=2)
    cluster_data_pca = pca.fit_transform(cluster_data_scaled)
    
    # Criar visualização
    plt.figure(figsize=(12, 8))
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    for i in range(k_optimal):
        mask = cluster_labels == i
        plt.scatter(cluster_data_pca[mask, 0], cluster_data_pca[mask, 1], 
                   c=colors[i], label=f'Cluster {i+1}', alpha=0.6)
    
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} da variância)')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} da variância)')
    plt.title('Análise de Clusters - Perfil dos Usuários (PCA)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    filename = 'clusters_perfil_usuarios.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Visualização salva como: {filename}")
    
    return {
        'cluster_summary': cluster_summary,
        'k_optimal': k_optimal,
        'pca_variance_explained': pca.explained_variance_ratio_[:2].sum(),
        'data_with_clusters': cluster_data
    }

def analise_machine_learning_previsao(data):
    """Machine Learning: Previsão de Uso do Transporte Público"""
    print("\n🤖 MACHINE LEARNING: PREVISÃO DE USO DO TP")
    print("="*50)
    
    # Preparar variáveis preditoras
    features = []
    target_col = None
    
    # Identificar target (uso do TP)
    for col in data.columns:
        if 'forma' in col.lower() and 'viagens' in col.lower():
            target_col = col
            break
    
    if not target_col:
        print("❌ Variável target não encontrada")
        return None
    
    # Selecionar features categóricas relevantes
    categorical_features = []
    
    for col in data.columns:
        if any(palavra in col.lower() for palavra in ['gênero', 'raça', 'idade', 'escolaridade', 
                                                     'renda', 'profissional', 'carteira', 'veículo']):
            categorical_features.append(col)
    
    print(f"Features categóricas identificadas: {len(categorical_features)}")
    
    # Preparar dataset
    ml_data = data[categorical_features + [target_col]].copy()
    ml_data = ml_data.dropna()
    
    if len(ml_data) < 100:
        print("❌ Dados insuficientes para ML")
        return None
    
    # Criar target binário
    ml_data['usa_tp'] = (ml_data[target_col] == 'Utilizo o transporte público').astype(int)
    
    # Codificar variáveis categóricas
    label_encoders = {}
    X_encoded = pd.DataFrame()
    
    for col in categorical_features:
        if col in ml_data.columns:
            le = LabelEncoder()
            # Tratar valores NaN
            ml_data[col] = ml_data[col].fillna('Missing')
            X_encoded[col] = le.fit_transform(ml_data[col])
            label_encoders[col] = le
    
    y = ml_data['usa_tp']
    
    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Treinar Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    rf_model.fit(X_train, y_train)
    
    # Fazer predições
    y_pred = rf_model.predict(X_test)
    y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
    
    # Avaliar modelo
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"Resultados do Modelo Random Forest:")
    print(f"  Acurácia: {accuracy:.3f}")
    print(f"  Precisão: {precision:.3f}")
    print(f"  Recall: {recall:.3f}")
    print(f"  F1-Score: {f1:.3f}")
    print(f"  AUC-ROC: {auc:.3f}")
    
    # Importância das features
    feature_importance = pd.DataFrame({
        'feature': X_encoded.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nImportância das Features:")
    for _, row in feature_importance.head(10).iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")
    
    return {
        'modelo': rf_model,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'auc_roc': auc,
        'feature_importance': feature_importance,
        'label_encoders': label_encoders
    }

def gerar_dashboard_visualizacoes(data, resultados_analises):
    """Gerar dashboard com visualizações avançadas"""
    print("\n📊 GERANDO DASHBOARD DE VISUALIZAÇÕES")
    print("="*45)
    
    # Configurar subplot
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Distribuição de Renda vs Uso do TP
    plt.subplot(2, 3, 1)
    
    # Preparar dados para o gráfico
    income_col = None
    transport_col = None
    
    for col in data.columns:
        if 'renda' in col.lower():
            income_col = col
        elif 'forma' in col.lower() and 'viagens' in col.lower():
            transport_col = col
    
    if income_col and transport_col:
        crosstab_renda = pd.crosstab(data[income_col], data[transport_col], normalize='index')
        if 'Utilizo o transporte público' in crosstab_renda.columns:
            uso_tp_por_renda = crosstab_renda['Utilizo o transporte público'] * 100
            uso_tp_por_renda.plot(kind='bar', color='skyblue')
            plt.title('Uso do TP por Faixa de Renda', fontsize=12, fontweight='bold')
            plt.ylabel('% que usa TP')
            plt.xticks(rotation=45, ha='right')
    
    # 2. Distribuição por Gênero
    plt.subplot(2, 3, 2)
    
    gender_col = None
    for col in data.columns:
        if 'gênero' in col.lower() or 'genero' in col.lower():
            gender_col = col
            break
    
    if gender_col:
        gender_counts = data[gender_col].value_counts()
        plt.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', 
                colors=['lightcoral', 'lightblue', 'lightgreen'])
        plt.title('Distribuição por Gênero', fontsize=12, fontweight='bold')
    
    # 3. Escolaridade vs Qualidade (se disponível nos resultados)
    plt.subplot(2, 3, 3)
    
    if 'anova' in resultados_analises and resultados_analises['anova']:
        # Pegar primeiro resultado significativo
        resultado_sig = None
        for res in resultados_analises['anova']:
            if res['significativo']:
                resultado_sig = res
                break
        
        if resultado_sig:
            medias = resultado_sig['medias_grupos']
            plt.bar(range(len(medias)), list(medias.values()), color='lightgreen')
            plt.title(f'Qualidade por Escolaridade\n({resultado_sig["atributo"]})', 
                     fontsize=12, fontweight='bold')
            plt.xticks(range(len(medias)), list(medias.keys()), rotation=45, ha='right')
            plt.ylabel('Média de Qualidade')
    
    # 4. Carteira de Motorista vs Uso do TP
    plt.subplot(2, 3, 4)
    
    license_col = None
    for col in data.columns:
        if 'carteira' in col.lower() and 'motorista' in col.lower():
            license_col = col
            break
    
    if license_col and transport_col:
        data_temp = data.copy()
        data_temp['tem_carteira'] = data_temp[license_col] != 'Não tenho'
        crosstab_carteira = pd.crosstab(data_temp['tem_carteira'], data_temp[transport_col], 
                                       normalize='index')
        if 'Utilizo o transporte público' in crosstab_carteira.columns:
            uso_tp_carteira = crosstab_carteira['Utilizo o transporte público'] * 100
            uso_tp_carteira.plot(kind='bar', color=['orange', 'green'])
            plt.title('Uso do TP por Posse de Carteira', fontsize=12, fontweight='bold')
            plt.ylabel('% que usa TP')
            plt.xticks([0, 1], ['Sem Carteira', 'Com Carteira'], rotation=0)
    
    # 5. Importância das Features (se disponível)
    plt.subplot(2, 3, 5)
    
    if 'ml' in resultados_analises and resultados_analises['ml']:
        feature_imp = resultados_analises['ml']['feature_importance'].head(8)
        plt.barh(range(len(feature_imp)), feature_imp['importance'], color='purple', alpha=0.7)
        plt.yticks(range(len(feature_imp)), feature_imp['feature'])
        plt.title('Importância das Features (ML)', fontsize=12, fontweight='bold')
        plt.xlabel('Importância')
    
    # 6. Performance do Modelo ML (se disponível)
    plt.subplot(2, 3, 6)
    
    if 'ml' in resultados_analises and resultados_analises['ml']:
        ml_results = resultados_analises['ml']
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
        values = [ml_results['accuracy'], ml_results['precision'], 
                 ml_results['recall'], ml_results['f1_score'], ml_results['auc_roc']]
        
        plt.bar(metrics, values, color='teal', alpha=0.7)
        plt.title('Performance do Modelo ML', fontsize=12, fontweight='bold')
        plt.ylabel('Score')
        plt.xticks(rotation=45)
        plt.ylim(0, 1)
        
        # Adicionar valores nas barras
        for i, v in enumerate(values):
            plt.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    filename = 'dashboard_analises_avancadas.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Dashboard salvo como: {filename}")
    
    return filename

def gerar_relatorio_final_avancado(resultados_analises):
    """Gerar relatório final com todas as análises avançadas"""
    print("\n📄 GERANDO RELATÓRIO FINAL AVANÇADO")
    print("="*45)
    
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    filename = f"RELATORIO_ANALISES_AVANCADAS_{timestamp}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO DE ANÁLISES ESTATÍSTICAS AVANÇADAS\n")
        f.write("## Análise de Transporte Público e Sistema de Recompensas\n\n")
        f.write(f"**Data:** {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # Resumo Executivo
        f.write("## RESUMO EXECUTIVO\n\n")
        f.write("Este relatório apresenta análises estatísticas avançadas incluindo:\n")
        f.write("- **ANOVA**: Diferenças entre grupos de escolaridade na avaliação da qualidade\n")
        f.write("- **Regressão Logística**: Impacto da renda no uso do transporte público\n")
        f.write("- **Análise de Clusters**: Segmentação de usuários por perfil comportamental\n")
        f.write("- **Machine Learning**: Modelo preditivo para uso do transporte público\n\n")
        
        # ANOVA Results
        if 'anova' in resultados_analises and resultados_analises['anova']:
            f.write("## 1. ANÁLISE ANOVA - ESCOLARIDADE vs QUALIDADE\n\n")
            
            resultados_sig = [r for r in resultados_analises['anova'] if r['significativo']]
            
            f.write(f"**{len(resultados_sig)} de {len(resultados_analises['anova'])} atributos** ")
            f.write("mostraram diferenças significativas entre grupos de escolaridade.\n\n")
            
            for resultado in resultados_sig:
                f.write(f"### {resultado['atributo']}\n")
                f.write(f"- **F-statistic**: {resultado['f_statistic']:.3f}\n")
                f.write(f"- **p-value**: {resultado['p_value']:.4f}\n")
                f.write(f"- **Significativo**: {'✓' if resultado['significativo'] else '✗'}\n\n")
                
                f.write("**Médias por grupo de escolaridade:**\n")
                for grupo, media in resultado['medias_grupos'].items():
                    f.write(f"- {grupo}: {media:.2f}\n")
                f.write("\n")
        
        # Regressão Results
        if 'regressao' in resultados_analises and resultados_analises['regressao']:
            f.write("## 2. REGRESSÃO LOGÍSTICA - RENDA vs USO DO TP\n\n")
            
            reg_result = resultados_analises['regressao']
            f.write(f"**Pseudo R²**: {reg_result['pseudo_r2']:.3f}\n")
            f.write(f"**Coeficiente da Renda**: {reg_result['coeficiente']:.3f}\n")
            f.write(f"**p-value**: {reg_result['p_value']:.4f}\n")
            f.write(f"**Significativo**: {'✓' if reg_result['significativo'] else '✗'}\n\n")
            
            if reg_result['significativo']:
                if reg_result['coeficiente'] < 0:
                    f.write("**Interpretação**: Maior renda está associada a MENOR probabilidade de usar TP.\n")
                else:
                    f.write("**Interpretação**: Maior renda está associada a MAIOR probabilidade de usar TP.\n")
            else:
                f.write("**Interpretação**: Renda não influencia significativamente o uso do TP.\n")
            f.write("\n")
        
        # Clusters Results
        if 'clusters' in resultados_analises and resultados_analises['clusters']:
            f.write("## 3. ANÁLISE DE CLUSTERS - PERFIL DOS USUÁRIOS\n\n")
            
            cluster_result = resultados_analises['clusters']
            f.write(f"**Número de clusters identificados**: {cluster_result['k_optimal']}\n")
            f.write(f"**Variância explicada pelo PCA**: {cluster_result['pca_variance_explained']:.1%}\n\n")
            
            for cluster_info in cluster_result['cluster_summary']:
                f.write(f"### Cluster {cluster_info['cluster_id']}\n")
                f.write(f"- **Tamanho**: {cluster_info['n_observacoes']} observações ")
                f.write(f"({cluster_info['percentual']:.1f}%)\n")
                f.write("- **Características principais**:\n")
                
                # Pegar as 3 características mais distintivas (valores mais altos)
                caracteristicas = cluster_info['caracteristicas']
                top_chars = sorted(caracteristicas.items(), key=lambda x: x[1], reverse=True)[:3]
                
                for char, valor in top_chars:
                    f.write(f"  - {char}: {valor:.2f}\n")
                f.write("\n")
        
        # ML Results
        if 'ml' in resultados_analises and resultados_analises['ml']:
            f.write("## 4. MACHINE LEARNING - MODELO PREDITIVO\n\n")
            
            ml_result = resultados_analises['ml']
            f.write("**Modelo**: Random Forest Classifier\n\n")
            f.write("### Métricas de Performance\n")
            f.write(f"- **Acurácia**: {ml_result['accuracy']:.3f}\n")
            f.write(f"- **Precisão**: {ml_result['precision']:.3f}\n")
            f.write(f"- **Recall**: {ml_result['recall']:.3f}\n")
            f.write(f"- **F1-Score**: {ml_result['f1_score']:.3f}\n")
            f.write(f"- **AUC-ROC**: {ml_result['auc_roc']:.3f}\n\n")
            
            f.write("### Features Mais Importantes\n")
            top_features = ml_result['feature_importance'].head(10)
            for _, row in top_features.iterrows():
                f.write(f"- **{row['feature']}**: {row['importance']:.3f}\n")
            f.write("\n")
        
        # Conclusões
        f.write("## CONCLUSÕES E RECOMENDAÇÕES\n\n")
        f.write("### Principais Insights\n\n")
        
        # Conclusões baseadas nos resultados
        if 'anova' in resultados_analises and resultados_analises['anova']:
            resultados_sig = [r for r in resultados_analises['anova'] if r['significativo']]
            if resultados_sig:
                f.write("1. **Diferenças por Escolaridade**: Identificadas diferenças significativas ")
                f.write("na avaliação da qualidade entre grupos de escolaridade.\n")
        
        if 'regressao' in resultados_analises and resultados_analises['regressao']:
            if resultados_analises['regressao']['significativo']:
                f.write("2. **Impacto da Renda**: A renda influencia significativamente ")
                f.write("a probabilidade de uso do transporte público.\n")
        
        if 'clusters' in resultados_analises and resultados_analises['clusters']:
            f.write("3. **Segmentação de Usuários**: Identificados perfis distintos de usuários ")
            f.write("com diferentes padrões comportamentais.\n")
        
        if 'ml' in resultados_analises and resultados_analises['ml']:
            if resultados_analises['ml']['accuracy'] > 0.7:
                f.write("4. **Modelo Preditivo**: Desenvolvido modelo com boa capacidade ")
                f.write("de predição do uso do transporte público.\n")
        
        f.write("\n### Recomendações Estratégicas\n\n")
        f.write("1. **Políticas Segmentadas**: Desenvolver estratégias específicas por perfil socioeconômico\n")
        f.write("2. **Melhoria da Qualidade**: Focar nos atributos com maior variação entre grupos\n")
        f.write("3. **Sistema de Recompensas**: Implementar programa adaptado aos diferentes clusters\n")
        f.write("4. **Monitoramento Preditivo**: Utilizar modelo ML para identificar usuários em risco\n\n")
        
        f.write("---\n\n")
        f.write("*Relatório gerado automaticamente pelo sistema de análise estatística avançada*\n")
    
    print(f"✓ Relatório salvo como: {filename}")
    return filename

def main():
    """Função principal para executar todas as análises avançadas"""
    print("🔬 SISTEMA DE ANÁLISES ESTATÍSTICAS AVANÇADAS")
    print("="*70)
    
    # Carregar dados
    data, datasets = carregar_e_preparar_dados()
    
    if data is None or len(data) == 0:
        print("❌ Erro ao carregar dados")
        return
    
    # Executar análises
    resultados_analises = {}
    
    try:
        # 1. ANOVA
        print("\n" + "="*70)
        resultados_analises['anova'] = analise_anova_escolaridade_qualidade(data)
        
        # 2. Regressão
        print("\n" + "="*70)
        resultados_analises['regressao'] = analise_regressao_renda_uso_tp(data)
        
        # 3. Clusters
        print("\n" + "="*70)
        resultados_analises['clusters'] = analise_clusters_perfil_usuarios(data)
        
        # 4. Machine Learning
        print("\n" + "="*70)
        resultados_analises['ml'] = analise_machine_learning_previsao(data)
        
        # 5. Visualizações
        print("\n" + "="*70)
        dashboard = gerar_dashboard_visualizacoes(data, resultados_analises)
        
        # 6. Relatório Final
        print("\n" + "="*70)
        relatorio = gerar_relatorio_final_avancado(resultados_analises)
        
        print(f"\n🎉 ANÁLISES AVANÇADAS CONCLUÍDAS COM SUCESSO!")
        print(f"📊 Dashboard: {dashboard}")
        print(f"📄 Relatório: {relatorio}")
        
    except Exception as e:
        print(f"❌ Erro durante as análises: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 