#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE COMPLETA E CORRIGIDA - TRANSPORTE PÚBLICO E RECOMPENSAS
============================================================

Script corrigido que:
1. Examina a estrutura real dos dados
2. Aplica análises adequadas aos dados disponíveis
3. Corrige problemas de codificação e mapeamento
4. Produz resultados condizentes com a realidade dos dados
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import LabelEncoder
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
import warnings
warnings.filterwarnings('ignore')

# Configurações
plt.style.use('default')
sns.set_palette("Set2")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# ============================================================================
# 1. CARREGAMENTO E INSPEÇÃO DOS DADOS REAIS
# ============================================================================

def carregar_dados():
    """Carrega todos os arquivos CSV e examina sua estrutura real"""
    print("=== CARREGAMENTO E INSPEÇÃO DOS DADOS ===")
    
    # Dicionário para armazenar os datasets
    datasets = {}
    
    # Lista de arquivos
    arquivos = [
        'Qualidade do serviço.csv',
        'Utilização.csv', 
        'Percepção novos serviços.csv',
        'Intenção comportamental.csv',
        'Aceitação da tecnologia.csv',
        'Experiência do usuário.csv',
        'Perfil Socioeconomico.csv',
        'BDTP.csv'
    ]
    
    for arquivo in arquivos:
        try:
            caminho = f'csv_extraidos/{arquivo}'
            df = pd.read_csv(caminho)
            nome = arquivo.replace('.csv', '').replace(' ', '_')
            datasets[nome] = df
            
            print(f"\n{arquivo}:")
            print(f"  - Shape: {df.shape}")
            print(f"  - Colunas: {list(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            print(f"  - IDs únicos: {df['ID'].nunique()}")
            
        except Exception as e:
            print(f"Erro ao carregar {arquivo}: {e}")
    
    return datasets

def examinar_estrutura_real(datasets):
    """Examina a estrutura real de cada dataset"""
    print("\n=== ANÁLISE DETALHADA DA ESTRUTURA ===")
    
    estrutura = {}
    
    for nome, df in datasets.items():
        print(f"\n{nome.upper()}:")
        
        # Informações básicas
        info = {
            'shape': df.shape,
            'colunas': list(df.columns),
            'tipos': df.dtypes.to_dict(),
            'missing': df.isnull().sum().to_dict(),
            'valores_unicos': {}
        }
        
        # Examinar valores únicos nas primeiras colunas não-ID
        colunas_analise = [col for col in df.columns if col != 'ID'][:3]
        for col in colunas_analise:
            if df[col].dtype == 'object':
                unicos = df[col].value_counts().head(5)
                info['valores_unicos'][col] = unicos.to_dict()
                print(f"  {col}: {list(unicos.index)}")
        
        estrutura[nome] = info
    
    return estrutura

# ============================================================================
# 2. MAPEAMENTO CORRETO DAS ESCALAS
# ============================================================================

def criar_mapeamentos_corretos():
    """Cria mapeamentos baseados na estrutura real dos dados"""
    
    # Escalas de satisfação (dados reais)
    satisfacao_map = {
        'Muito insatisfeito': 1,
        'Insatisfeito': 2, 
        'Neutro': 3,
        'Satisfeito': 4,
        'Muito satisfeito': 5
    }
    
    # Escalas de concordância (dados reais)
    concordancia_map = {
        'Discordo totalmente': 1,
        'Discordo': 2,
        'Neutro': 3, 
        'Concordo': 4,
        'Concordo totalmente': 5
    }
    
    # Facilidade de uso
    facilidade_map = {
        'Muito difícil': 1,
        'Difícil': 2,
        'Neutro': 3,
        'Fácil': 4,
        'Muito Fácil': 5
    }
    
    # Frequência de uso
    frequencia_map = {
        'Não utilizo o transporte público': 0,
        'Uso menos de uma vez por semana': 1,
        'Uso uma ou duas vezes por semana': 2,
        'Uso três a quatro vezes por semana': 3,
        'Uso cinco ou mais vezes por semana': 4
    }
    
    return {
        'satisfacao': satisfacao_map,
        'concordancia': concordancia_map,
        'facilidade': facilidade_map,
        'frequencia': frequencia_map
    }

def aplicar_codificacao(datasets, mapeamentos):
    """Aplica codificação correta aos dados"""
    print("\n=== APLICANDO CODIFICAÇÃO CORRETA ===")
    
    datasets_coded = {}
    
    for nome, df in datasets.items():
        df_coded = df.copy()
        
        if nome == 'Qualidade_do_serviço':
            # Aplicar mapeamento de satisfação às colunas de qualidade
            for col in df.columns:
                if col != 'ID':
                    df_coded[col] = df[col].map(mapeamentos['satisfacao'])
        
        elif nome == 'Percepção_novos_serviços':
            # Aplicar mapeamento de concordância 
            for col in df.columns:
                if col != 'ID':
                    df_coded[col] = df[col].map(mapeamentos['concordancia'])
        
        elif nome == 'Experiência_do_usuário':
            # Aplicar mapeamentos adequados por tipo de questão
            for col in df.columns:
                if col == 'ID':
                    continue
                elif any(palavra in col for palavra in ['satisfeito', 'correspondem', 'necessidades', 'custo', 'recompensado']):
                    df_coded[col] = df[col].map(mapeamentos['concordancia'])
                elif any(palavra in col for palavra in ['Cartões', 'Aplicativos', 'Qr', 'Bilhete']):
                    df_coded[col] = df[col].map(mapeamentos['facilidade'])
        
        datasets_coded[nome] = df_coded
        print(f"Codificado: {nome}")
    
    return datasets_coded

# ============================================================================
# 3. ANÁLISE DESCRITIVA CORRIGIDA
# ============================================================================

def analise_descritiva_real(datasets_coded):
    """Análise descritiva baseada nos dados reais"""
    print("\n=== ANÁLISE DESCRITIVA REAL ===")
    
    resultados = {}
    
    # Análise da Qualidade do Serviço
    if 'Qualidade_do_serviço' in datasets_coded:
        df_qual = datasets_coded['Qualidade_do_serviço']
        
        print("\nQUALIDADE DO SERVIÇO:")
        quality_scores = df_qual.drop('ID', axis=1).mean().sort_values(ascending=False)
        
        print("Atributos mais bem avaliados:")
        for attr, score in quality_scores.head(3).items():
            print(f"  - {attr[:50]}...: {score:.2f}")
        
        print("Atributos pior avaliados:")
        for attr, score in quality_scores.tail(3).items():
            print(f"  - {attr[:50]}...: {score:.2f}")
        
        resultados['qualidade'] = quality_scores
    
    # Análise de Utilização
    if 'Utilização' in datasets_coded:
        df_util = datasets_coded['Utilização']
        
        print("\nPADRÕES DE UTILIZAÇÃO:")
        
        # Meio de transporte principal
        transporte = df_util['Qual a forma que você faz a maioria das viagens?'].value_counts()
        print("Principal meio de transporte:")
        for meio, count in transporte.head(3).items():
            pct = (count/len(df_util))*100
            print(f"  - {meio}: {count} ({pct:.1f}%)")
        
        resultados['utilizacao'] = transporte
    
    # Análise Socioeconômica
    if 'Perfil_Socioeconomico' in datasets_coded:
        df_perfil = datasets_coded['Perfil_Socioeconomico']
        
        print("\nPERFIL SOCIOECONÔMICO:")
        
        # Verificar nomes reais das colunas
        print(f"Colunas disponíveis: {list(df_perfil.columns)}")
        
        # Encontrar coluna de gênero (pode ter caracteres especiais)
        genero_col = None
        for col in df_perfil.columns:
            if 'gênero' in col.lower() or 'genero' in col.lower():
                genero_col = col
                break
        
        if genero_col:
            genero = df_perfil[genero_col].value_counts()
            print("Distribuição por gênero:")
            for g, count in genero.items():
                pct = (count/len(df_perfil))*100
                print(f"  - {g}: {count} ({pct:.1f}%)")
        
        # Faixa etária
        if 'Idade' in df_perfil.columns:
            idade = df_perfil['Idade'].value_counts()
            print("\nDistribuição por idade:")
            for i, count in idade.head(3).items():
                pct = (count/len(df_perfil))*100
                print(f"  - {i}: {count} ({pct:.1f}%)")
            
            resultados['perfil'] = {'genero': genero if genero_col else None, 'idade': idade}
        else:
            print("Coluna 'Idade' não encontrada")
    
    return resultados

# ============================================================================
# 4. ANÁLISE FACTORIAL CORRIGIDA
# ============================================================================

def analise_factorial_real(datasets_coded):
    """Análise factorial baseada nos dados numéricos reais"""
    print("\n=== ANÁLISE FACTORIAL CORRIGIDA ===")
    
    resultados_factorial = {}
    
    # Qualidade do Serviço
    if 'Qualidade_do_serviço' in datasets_coded:
        df_qual = datasets_coded['Qualidade_do_serviço'].drop('ID', axis=1)
        
        # Remover valores missing
        df_qual_clean = df_qual.dropna()
        
        if len(df_qual_clean) > 50:  # Verificar se há dados suficientes
            print(f"Analisando Qualidade do Serviço (n={len(df_qual_clean)})")
            
            try:
                # Teste de adequação
                bartlett_chi2, bartlett_p = calculate_bartlett_sphericity(df_qual_clean)
                kmo_all, kmo_model = calculate_kmo(df_qual_clean)
                
                print(f"Bartlett test: χ²={bartlett_chi2:.2f}, p={bartlett_p:.4f}")
                print(f"KMO: {kmo_model:.3f}")
                
                if kmo_model > 0.5 and bartlett_p < 0.05:
                    # Determinar número de fatores
                    fa = FactorAnalyzer(n_factors=25, rotation=None)
                    fa.fit(df_qual_clean)
                    
                    # Critério de Kaiser (eigenvalues > 1)
                    eigenvalues = fa.get_eigenvalues()[0]
                    n_factors = sum(eigenvalues > 1)
                    
                    print(f"Número de fatores sugerido (Kaiser): {n_factors}")
                    
                    # Análise factorial final
                    fa_final = FactorAnalyzer(n_factors=n_factors, rotation='varimax')
                    fa_final.fit(df_qual_clean)
                    
                    loadings = pd.DataFrame(
                        fa_final.loadings_, 
                        index=df_qual_clean.columns,
                        columns=[f'Fator_{i+1}' for i in range(n_factors)]
                    )
                    
                    print("Cargas factoriais principais:")
                    print(loadings.round(3))
                    
                    resultados_factorial['qualidade'] = {
                        'loadings': loadings,
                        'eigenvalues': eigenvalues,
                        'variance': fa_final.get_factor_variance()
                    }
                
            except Exception as e:
                print(f"Erro na análise factorial de qualidade: {e}")
    
    return resultados_factorial

# ============================================================================
# 5. ANÁLISE DE CORRELAÇÕES E ASSOCIAÇÕES
# ============================================================================

def analise_correlacoes_real(datasets_coded):
    """Análise de correlações entre diferentes dimensões"""
    print("\n=== ANÁLISE DE CORRELAÇÕES REAL ===")
    
    correlacoes = {}
    
    # Criar scores compostos para cada dimensão
    if 'Qualidade_do_serviço' in datasets_coded:
        df_qual = datasets_coded['Qualidade_do_serviço']
        qual_score = df_qual.drop('ID', axis=1).mean(axis=1)
        correlacoes['qualidade_score'] = qual_score
    
    if 'Experiência_do_usuário' in datasets_coded:
        df_exp = datasets_coded['Experiência_do_usuário']
        # Colunas de satisfação (primeiras 5)
        sat_cols = [col for col in df_exp.columns if col != 'ID'][:5]
        if sat_cols:
            exp_score = df_exp[sat_cols].mean(axis=1)
            correlacoes['experiencia_score'] = exp_score
    
    if 'Percepção_novos_serviços' in datasets_coded:
        df_perc = datasets_coded['Percepção_novos_serviços']
        perc_score = df_perc.drop('ID', axis=1).mean(axis=1)
        correlacoes['percepcao_score'] = perc_score
    
    # Matriz de correlações
    if len(correlacoes) > 1:
        df_corr = pd.DataFrame(correlacoes)
        matriz_corr = df_corr.corr()
        
        print("Matriz de correlações entre dimensões:")
        print(matriz_corr.round(3))
        
        # Visualização
        plt.figure(figsize=(8, 6))
        sns.heatmap(matriz_corr, annot=True, cmap='RdBu_r', center=0, 
                   square=True, fmt='.3f')
        plt.title('Correlações entre Dimensões')
        plt.tight_layout()
        plt.savefig('correlacoes_dimensoes.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return matriz_corr
    
    return None

# ============================================================================
# 6. ANÁLISE DE SEGMENTAÇÃO
# ============================================================================

def analise_segmentacao(datasets_coded):
    """Análise de segmentação por perfil socioeconômico"""
    print("\n=== ANÁLISE DE SEGMENTAÇÃO ===")
    
    if 'Perfil_Socioeconomico' not in datasets_coded:
        print("Dados de perfil não disponíveis")
        return None
    
    df_perfil = datasets_coded['Perfil_Socioeconomico']
    
    # Encontrar coluna de gênero
    genero_col = None
    for col in df_perfil.columns:
        if 'gênero' in col.lower() or 'genero' in col.lower():
            genero_col = col
            break
    
    # Análise por gênero
    if 'Qualidade_do_serviço' in datasets_coded and genero_col:
        df_qual = datasets_coded['Qualidade_do_serviço']
        
        # Merge dos dados
        df_merged = df_qual.merge(df_perfil[['ID', genero_col]], on='ID')
        
        # Score médio de qualidade por gênero
        qual_por_genero = df_merged.groupby(genero_col).apply(
            lambda x: x.drop(['ID', genero_col], axis=1).mean(axis=1).mean()
        )
        
        print("Satisfação média com qualidade por gênero:")
        for genero, score in qual_por_genero.items():
            print(f"  - {genero}: {score:.2f}")
    
    # Análise por faixa etária
    if 'Utilização' in datasets_coded and 'Idade' in df_perfil.columns:
        df_util = datasets_coded['Utilização']
        df_merged_util = df_util.merge(df_perfil[['ID', 'Idade']], on='ID')
        
        # Uso de transporte público por idade
        uso_por_idade = df_merged_util.groupby('Idade')['Qual a forma que você faz a maioria das viagens?'].apply(
            lambda x: (x == 'Utilizo o transporte público').mean() * 100
        )
        
        print("\nUso de transporte público por faixa etária:")
        for idade, pct in uso_por_idade.sort_values(ascending=False).items():
            print(f"  - {idade}: {pct:.1f}%")
    
    return qual_por_genero if 'qual_por_genero' in locals() else None

# ============================================================================
# 7. RELATÓRIO FINAL CORRIGIDO
# ============================================================================

def gerar_relatorio_final(datasets, resultados_desc, resultados_fact, correlacoes, segmentacao):
    """Gera relatório final com base nos dados reais"""
    print("\n" + "="*80)
    print("RELATÓRIO FINAL - ANÁLISE CORRIGIDA")
    print("="*80)
    
    # Resumo dos dados
    print("\n1. RESUMO DOS DADOS:")
    total_respondentes = len(datasets.get('Perfil_Socioeconomico', []))
    print(f"   - Total de respondentes: {total_respondentes}")
    
    for nome, df in datasets.items():
        if nome != 'Perfil_Socioeconomico':
            print(f"   - {nome.replace('_', ' ')}: {len(df)} registros")
    
    # Principais achados
    print("\n2. PRINCIPAIS ACHADOS:")
    
    if 'qualidade' in resultados_desc:
        quality_scores = resultados_desc['qualidade']
        melhor_attr = quality_scores.index[0]
        pior_attr = quality_scores.index[-1]
        
        print(f"   - Melhor atributo de qualidade: {melhor_attr[:60]}... (Score: {quality_scores.iloc[0]:.2f})")
        print(f"   - Pior atributo de qualidade: {pior_attr[:60]}... (Score: {quality_scores.iloc[-1]:.2f})")
    
    if 'utilizacao' in resultados_desc:
        principal_transporte = resultados_desc['utilizacao'].index[0]
        pct_principal = (resultados_desc['utilizacao'].iloc[0] / resultados_desc['utilizacao'].sum()) * 100
        print(f"   - Principal meio de transporte: {principal_transporte} ({pct_principal:.1f}%)")
    
    # Correlações
    if correlacoes is not None:
        print("\n3. CORRELAÇÕES ENTRE DIMENSÕES:")
        correlacoes_principais = correlacoes.values[correlacoes.values != 1.0]
        if len(correlacoes_principais) > 0:
            corr_max = correlacoes_principais.max()
            corr_min = correlacoes_principais.min()
            print(f"   - Correlação mais forte: {corr_max:.3f}")
            print(f"   - Correlação mais fraca: {corr_min:.3f}")
    
    # Limitações identificadas
    print("\n4. LIMITAÇÕES IDENTIFICADAS:")
    print("   - Alta concentração de respostas extremas (muito insatisfeito/concordo totalmente)")
    print("   - Possível viés de amostragem em alguns grupos demográficos")
    print("   - Dados faltantes em algumas dimensões")
    
    # Recomendações
    print("\n5. RECOMENDAÇÕES PARA ANÁLISES FUTURAS:")
    print("   - Aplicar técnicas de rebalanceamento para lidar com respostas extremas")
    print("   - Considerar análises não-paramétricas devido à distribuição dos dados")
    print("   - Expandir amostra para grupos sub-representados")
    print("   - Implementar modelos SEM com estimadores robustos")
    
    print("\n" + "="*80)

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal que executa toda a análise corrigida"""
    print("INICIANDO ANÁLISE COMPLETA E CORRIGIDA")
    print("="*60)
    
    # 1. Carregar e examinar dados
    datasets = carregar_dados()
    estrutura = examinar_estrutura_real(datasets)
    
    # 2. Aplicar codificação correta
    mapeamentos = criar_mapeamentos_corretos()
    datasets_coded = aplicar_codificacao(datasets, mapeamentos)
    
    # 3. Análises
    resultados_desc = analise_descritiva_real(datasets_coded)
    resultados_fact = analise_factorial_real(datasets_coded)
    correlacoes = analise_correlacoes_real(datasets_coded)
    segmentacao = analise_segmentacao(datasets_coded)
    
    # 4. Relatório final
    gerar_relatorio_final(datasets, resultados_desc, resultados_fact, 
                         correlacoes, segmentacao)
    
    return {
        'datasets': datasets,
        'datasets_coded': datasets_coded,
        'resultados_descritivos': resultados_desc,
        'resultados_factoriais': resultados_fact,
        'correlacoes': correlacoes,
        'segmentacao': segmentacao
    }

if __name__ == "__main__":
    resultados = main() 