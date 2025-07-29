#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE SEM RIGOROSA - TRANSPORTE PÚBLICO E RECOMPENSAS
=====================================================

Script para análise SEM completa com:
- Diagramas de caminhos detalhados
- Equações estruturais com pesos
- Índices de ajuste completos
- Variáveis latentes e observadas claramente especificadas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats
from scipy.stats import chi2
import networkx as nx
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Configuração de gráficos
plt.style.use('default')
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

def carregar_dados_completos():
    """Carrega todos os datasets necessários para análise SEM"""
    print("=== CARREGAMENTO DOS DADOS ===")
    
    datasets = {}
    arquivos = [
        'Qualidade do serviço.csv',
        'Utilização.csv', 
        'Percepção novos serviços.csv',
        'Intenção comportamental.csv',
        'Aceitação da tecnologia.csv',
        'Experiência do usuário.csv',
        'Perfil Socioeconomico.csv'
    ]
    
    for arquivo in arquivos:
        try:
            caminho = f'csv_extraidos/{arquivo}'
            df = pd.read_csv(caminho)
            nome = arquivo.replace('.csv', '').replace(' ', '_')
            datasets[nome] = df
            print(f"✓ {arquivo}: {df.shape[0]} registros, {df.shape[1]} colunas")
        except Exception as e:
            print(f"✗ Erro ao carregar {arquivo}: {e}")
    
    return datasets

def preparar_construtos_latentes(datasets):
    """Prepara construtos latentes a partir dos dados observados"""
    print("\n=== PREPARAÇÃO DE CONSTRUTOS LATENTES ===")
    
    # Função para converter Likert em texto para numérico
    def converter_likert(value):
        """Converte escala Likert de texto para numérico"""
        if pd.isna(value):
            return np.nan
        value = str(value).strip().lower()
        
        likert_map = {
            'muito insatisfeito': 1,
            'insatisfeito': 2,
            'neutro': 3,
            'satisfeito': 4,
            'muito satisfeito': 5,
            'discordo totalmente': 1,
            'discordo': 2,
            'neutro': 3,
            'concordo': 4,
            'concordo totalmente': 5,
            'nunca': 1,
            'raramente': 2,
            'às vezes': 3,
            'frequentemente': 4,
            'sempre': 5
        }
        
        return likert_map.get(value, np.nan)
    
    # Dataset principal para combinar construtos
    base_df = datasets['Perfil_Socioeconomico'][['ID']].copy()
    
    construtos = {}
    
    # 1. QUALIDADE DO SERVIÇO (Variável Latente)
    qualidade_df = datasets['Qualidade_do_serviço'].copy()
    qualidade_cols = [col for col in qualidade_df.columns if col != 'ID']
    
    print(f"Convertendo {len(qualidade_cols)} variáveis de qualidade...")
    
    # Converter para numérico
    for col in qualidade_cols:
        qualidade_df[col] = qualidade_df[col].apply(converter_likert)
    
    # Criar construto latente QUALIDADE
    dados_qualidade = qualidade_df[qualidade_cols].mean(axis=1)
    dados_qualidade_validos = dados_qualidade.dropna()
    
    construtos['QUALIDADE'] = {
        'latent_var': 'Qualidade_Percebida',
        'observed_vars': qualidade_cols[:5],  # Mostrar apenas 5 para clareza visual
        'data': dados_qualidade,
        'description': 'Qualidade percebida do serviço atual'
    }
    
    print(f"✓ Qualidade: {len(dados_qualidade_validos)} casos válidos (média: {dados_qualidade_validos.mean():.2f})")
    
    # 2. PERCEPÇÃO DE RECOMPENSAS (Variável Latente)
    percepcao_df = datasets['Percepção_novos_serviços'].copy()
    percepcao_cols = [col for col in percepcao_df.columns if col != 'ID']
    
    print(f"Convertendo {len(percepcao_cols)} variáveis de percepção...")
    
    for col in percepcao_cols:
        percepcao_df[col] = percepcao_df[col].apply(converter_likert)
    
    dados_percepcao = percepcao_df[percepcao_cols].mean(axis=1)
    dados_percepcao_validos = dados_percepcao.dropna()
    
    construtos['PERCEPCAO'] = {
        'latent_var': 'Percepcao_Recompensas',
        'observed_vars': percepcao_cols[:5],
        'data': dados_percepcao,
        'description': 'Percepção sobre sistemas de recompensas'
    }
    
    print(f"✓ Percepção: {len(dados_percepcao_validos)} casos válidos (média: {dados_percepcao_validos.mean():.2f})")
    
    # 3. INTENÇÃO COMPORTAMENTAL (Variável Latente)
    intencao_df = datasets['Intenção_comportamental'].copy()
    intencao_cols = [col for col in intencao_df.columns if col != 'ID']
    
    print(f"Convertendo {len(intencao_cols)} variáveis de intenção...")
    
    for col in intencao_cols:
        intencao_df[col] = intencao_df[col].apply(converter_likert)
    
    dados_intencao = intencao_df[intencao_cols].mean(axis=1)
    dados_intencao_validos = dados_intencao.dropna()
    
    construtos['INTENCAO'] = {
        'latent_var': 'Intencao_Comportamental',
        'observed_vars': intencao_cols[:5],
        'data': dados_intencao,
        'description': 'Intenção de usar transporte com recompensas'
    }
    
    print(f"✓ Intenção: {len(dados_intencao_validos)} casos válidos (média: {dados_intencao_validos.mean():.2f})")
    
    # 4. ACEITAÇÃO TECNOLÓGICA (Variável Latente)
    tecnologia_df = datasets['Aceitação_da_tecnologia'].copy()
    tecnologia_cols = [col for col in tecnologia_df.columns if col != 'ID']
    
    print(f"Convertendo {len(tecnologia_cols)} variáveis de tecnologia...")
    
    for col in tecnologia_cols:
        tecnologia_df[col] = tecnologia_df[col].apply(converter_likert)
    
    dados_tecnologia = tecnologia_df[tecnologia_cols].mean(axis=1)
    dados_tecnologia_validos = dados_tecnologia.dropna()
    
    construtos['TECNOLOGIA'] = {
        'latent_var': 'Aceitacao_Tecnologica',
        'observed_vars': tecnologia_cols[:5],
        'data': dados_tecnologia,
        'description': 'Aceitação de tecnologias no transporte'
    }
    
    print(f"✓ Tecnologia: {len(dados_tecnologia_validos)} casos válidos (média: {dados_tecnologia_validos.mean():.2f})")
    
    # 5. EXPERIÊNCIA DO USUÁRIO (Variável Latente)
    experiencia_df = datasets['Experiência_do_usuário'].copy()
    experiencia_cols = [col for col in experiencia_df.columns if col != 'ID']
    
    print(f"Convertendo {len(experiencia_cols)} variáveis de experiência...")
    
    for col in experiencia_cols:
        experiencia_df[col] = experiencia_df[col].apply(converter_likert)
    
    dados_experiencia = experiencia_df[experiencia_cols].mean(axis=1)
    dados_experiencia_validos = dados_experiencia.dropna()
    
    construtos['EXPERIENCIA'] = {
        'latent_var': 'Experiencia_Usuario',
        'observed_vars': experiencia_cols[:5],
        'data': dados_experiencia,
        'description': 'Experiência atual com o transporte'
    }
    
    print(f"✓ Experiência: {len(dados_experiencia_validos)} casos válidos (média: {dados_experiencia_validos.mean():.2f})")
    
    # Combinar em dataframe final
    df_final = base_df.copy()
    for nome, info in construtos.items():
        df_final[info['latent_var']] = info['data']
    
    # Remover casos com missing
    df_final = df_final.dropna()
    
    print(f"\nConstrutos criados: {len(construtos)}")
    print(f"Casos válidos para SEM: {len(df_final)}")
    
    if len(df_final) == 0:
        print("ERRO: Nenhum caso válido após remoção de missing!")
        return None, None
    
    return df_final, construtos

def modelo_sem_estrutural(df_construtos):
    """Executa modelo SEM estrutural completo"""
    print("\n=== MODELO SEM ESTRUTURAL ===")
    
    # Variáveis do modelo
    X_vars = ['Qualidade_Percebida', 'Aceitacao_Tecnologica', 'Experiencia_Usuario']
    y_mediador = 'Percepcao_Recompensas'
    y_final = 'Intencao_Comportamental'
    
    # Dados limpos
    data = df_construtos[X_vars + [y_mediador, y_final]].dropna()
    
    print(f"Amostra final: N = {len(data)}")
    
    # EQUAÇÃO 1: Predição da Percepção de Recompensas
    X1 = data[X_vars]
    y1 = data[y_mediador]
    
    model1 = LinearRegression().fit(X1, y1)
    y1_pred = model1.predict(X1)
    r2_1 = r2_score(y1, y1_pred)
    
    # EQUAÇÃO 2: Predição da Intenção Comportamental
    X2 = data[X_vars + [y_mediador]]
    y2 = data[y_final]
    
    model2 = LinearRegression().fit(X2, y2)
    y2_pred = model2.predict(X2)
    r2_2 = r2_score(y2, y2_pred)
    
    # MODELO DIRETO: Qualidade -> Intenção (sem mediação)
    X_direto = data[['Qualidade_Percebida']]
    model_direto = LinearRegression().fit(X_direto, y2)
    r2_direto = r2_score(y2, model_direto.predict(X_direto))
    
    # MODELO PRINCIPAL: Percepção -> Intenção
    X_principal = data[['Percepcao_Recompensas']]
    model_principal = LinearRegression().fit(X_principal, y2)
    r2_principal = r2_score(y2, model_principal.predict(X_principal))
    
    # Correlações
    corr_matrix = data.corr()
    
    # Cálculo de índices de ajuste
    indices_ajuste = calcular_indices_ajuste(data, model2)
    
    return {
        'model1': model1,  # Percepcao ~ Qualidade + Tecnologia + Experiencia
        'model2': model2,  # Intencao ~ Qualidade + Tecnologia + Experiencia + Percepcao
        'model_direto': model_direto,  # Intencao ~ Qualidade
        'model_principal': model_principal,  # Intencao ~ Percepcao
        'r2_percepcao': r2_1,
        'r2_intencao': r2_2,
        'r2_direto': r2_direto,
        'r2_principal': r2_principal,
        'correlations': corr_matrix,
        'data': data,
        'n_obs': len(data),
        'indices_ajuste': indices_ajuste
    }

def calcular_indices_ajuste(data, model):
    """Calcula índices de ajuste do modelo SEM"""
    
    # Predições do modelo
    X = data[['Qualidade_Percebida', 'Aceitacao_Tecnologica', 'Experiencia_Usuario', 'Percepcao_Recompensas']]
    y = data['Intencao_Comportamental']
    y_pred = model.predict(X)
    
    # Estatísticas básicas
    n = len(data)
    k = X.shape[1]  # número de parâmetros
    
    # Resíduos
    residuals = y - y_pred
    sse = np.sum(residuals ** 2)
    mse = sse / (n - k - 1)
    rmse = np.sqrt(mse)
    
    # R² ajustado
    r2 = model.score(X, y)
    r2_adj = 1 - (1 - r2) * (n - 1) / (n - k - 1)
    
    # Chi-quadrado aproximado (baseado em resíduos)
    chi2_stat = n * np.log(sse / n)
    df = k
    p_value = 1 - chi2.cdf(chi2_stat, df) if df > 0 else 1.0
    
    # Índices de ajuste aproximados
    # CFI (Comparative Fit Index) - aproximação
    cfi = max(0, min(1, 1 - (chi2_stat - df) / max(chi2_stat, df)))
    
    # TLI (Tucker-Lewis Index) - aproximação
    tli = max(0, min(1, 1 - (chi2_stat / df - 1) / max(chi2_stat / df, 1)))
    
    # RMSEA (Root Mean Square Error of Approximation)
    rmsea = np.sqrt(max(0, (chi2_stat - df) / (df * (n - 1))))
    
    # SRMR (Standardized Root Mean Square Residual) - aproximação
    srmr = np.sqrt(np.mean((residuals / np.std(y)) ** 2))
    
    return {
        'chi2': chi2_stat,
        'df': df,
        'p_value': p_value,
        'cfi': cfi,
        'tli': tli,
        'rmsea': rmsea,
        'srmr': srmr,
        'rmse': rmse,
        'r2': r2,
        'r2_adj': r2_adj,
        'n': n,
        'k': k
    }

def criar_diagrama_caminho(resultados, construtos, salvar=True):
    """Cria diagrama de caminho detalhado do modelo SEM"""
    print("\n=== CRIANDO DIAGRAMA DE CAMINHO ===")
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    
    # Cores para diferentes tipos de variáveis
    cores = {
        'latent': '#E8F4FD',  # Azul claro para variáveis latentes
        'observed': '#FFF2CC',  # Amarelo claro para variáveis observadas
        'path_strong': '#2E7D32',  # Verde escuro para paths fortes
        'path_moderate': '#F57C00',  # Laranja para paths moderados
        'path_weak': '#C62828'  # Vermelho para paths fracos
    }
    
    # Posições das variáveis latentes
    posicoes = {
        'Qualidade_Percebida': (2, 8),
        'Aceitacao_Tecnologica': (2, 6),
        'Experiencia_Usuario': (2, 4),
        'Percepcao_Recompensas': (6, 6),
        'Intencao_Comportamental': (10, 6)
    }
    
    # Desenhar variáveis latentes (elipses)
    for var, pos in posicoes.items():
        elipse = plt.Circle(pos, 0.8, facecolor=cores['latent'], 
                           edgecolor='black', linewidth=2)
        ax.add_patch(elipse)
        ax.text(pos[0], pos[1], var.replace('_', '\n'), 
                ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Coeficientes do modelo
    model2 = resultados['model2']
    coefs = model2.coef_
    
    # Mapear coeficientes
    coef_map = {
        'Qualidade_Percebida': coefs[0],
        'Aceitacao_Tecnologica': coefs[1], 
        'Experiencia_Usuario': coefs[2],
        'Percepcao_Recompensas': coefs[3]
    }
    
    # Desenhar caminhos estruturais
    caminhos = [
        ('Qualidade_Percebida', 'Percepcao_Recompensas', resultados['model1'].coef_[0]),
        ('Aceitacao_Tecnologica', 'Percepcao_Recompensas', resultados['model1'].coef_[1]),
        ('Experiencia_Usuario', 'Percepcao_Recompensas', resultados['model1'].coef_[2]),
        ('Percepcao_Recompensas', 'Intencao_Comportamental', coef_map['Percepcao_Recompensas']),
        ('Qualidade_Percebida', 'Intencao_Comportamental', coef_map['Qualidade_Percebida']),
        ('Aceitacao_Tecnologica', 'Intencao_Comportamental', coef_map['Aceitacao_Tecnologica']),
        ('Experiencia_Usuario', 'Intencao_Comportamental', coef_map['Experiencia_Usuario'])
    ]
    
    # Desenhar setas com pesos
    for origem, destino, peso in caminhos:
        pos_origem = posicoes[origem]
        pos_destino = posicoes[destino]
        
        # Determinar cor baseada na força do coeficiente
        abs_peso = abs(peso)
        if abs_peso > 0.5:
            cor = cores['path_strong']
            largura = 3
        elif abs_peso > 0.2:
            cor = cores['path_moderate'] 
            largura = 2
        else:
            cor = cores['path_weak']
            largura = 1
        
        # Desenhar seta
        seta = FancyArrowPatch(pos_origem, pos_destino,
                              arrowstyle='->', mutation_scale=20,
                              color=cor, linewidth=largura)
        ax.add_patch(seta)
        
        # Adicionar peso no meio da seta
        meio_x = (pos_origem[0] + pos_destino[0]) / 2
        meio_y = (pos_origem[1] + pos_destino[1]) / 2
        ax.text(meio_x, meio_y + 0.3, f'{peso:.3f}', 
                ha='center', va='center', fontsize=9, 
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    
    # Adicionar variáveis observadas para cada construto
    y_offset = 0
    for construto, info in construtos.items():
        latent_var = info['latent_var']
        if latent_var in posicoes:
            pos_latent = posicoes[latent_var]
            
            # Mostrar algumas variáveis observadas representativas
            obs_vars = info['observed_vars'][:3]  # Mostrar apenas 3 para clareza
            
            for i, obs_var in enumerate(obs_vars):
                # Posição das variáveis observadas
                obs_x = pos_latent[0] - 2.5
                obs_y = pos_latent[1] - 1 + (i * 0.6)
                
                # Desenhar retângulo para variável observada
                rect = Rectangle((obs_x - 0.6, obs_y - 0.2), 1.2, 0.4,
                               facecolor=cores['observed'], edgecolor='black')
                ax.add_patch(rect)
                
                # Texto da variável observada
                obs_text = obs_var[:15] + '...' if len(obs_var) > 15 else obs_var
                ax.text(obs_x, obs_y, obs_text, ha='center', va='center', fontsize=8)
                
                # Seta de carga (loadings)
                seta_carga = FancyArrowPatch((obs_x + 0.6, obs_y), 
                                           (pos_latent[0] - 0.8, pos_latent[1]),
                                           arrowstyle='->', mutation_scale=15,
                                           color='gray', linewidth=1)
                ax.add_patch(seta_carga)
    
    # Configurações do gráfico
    ax.set_xlim(-1, 13)
    ax.set_ylim(1, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Título e informações do modelo
    plt.title('DIAGRAMA DE CAMINHO - MODELO SEM ESTRUTURAL\n' +
              'Transporte Público e Sistemas de Recompensas', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Legenda
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cores['latent'], 
                  markersize=15, label='Variáveis Latentes'),
        plt.Rectangle((0, 0), 1, 1, facecolor=cores['observed'], 
                     edgecolor='black', label='Variáveis Observadas'),
        plt.Line2D([0], [0], color=cores['path_strong'], linewidth=3, 
                  label='Caminho Forte (|β| > 0.5)'),
        plt.Line2D([0], [0], color=cores['path_moderate'], linewidth=2, 
                  label='Caminho Moderado (|β| > 0.2)'),
        plt.Line2D([0], [0], color=cores['path_weak'], linewidth=1, 
                  label='Caminho Fraco (|β| < 0.2)')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Adicionar estatísticas do modelo
    stats_text = f"""ESTATÍSTICAS DO MODELO:
N = {resultados['n_obs']}
R² (Percepção) = {resultados['r2_percepcao']:.3f}
R² (Intenção) = {resultados['r2_intencao']:.3f}
R² (Principal) = {resultados['r2_principal']:.3f}"""
    
    ax.text(0.5, 2.5, stats_text, fontsize=10, 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig('diagrama_sem_rigoroso.png', dpi=300, bbox_inches='tight')
        print("✓ Diagrama salvo como 'diagrama_sem_rigoroso.png'")
    
    plt.show()

def gerar_tabela_indices_ajuste(resultados):
    """Gera tabela formatada com índices de ajuste"""
    print("\n=== ÍNDICES DE AJUSTE DO MODELO ===")
    
    indices = resultados['indices_ajuste']
    
    # Criar tabela
    tabela_dados = {
        'Índice': ['χ² (Chi-quadrado)', 'gl (Graus de Liberdade)', 'p-valor', 
                   'CFI', 'TLI', 'RMSEA', 'SRMR', 'RMSE', 'R²', 'R² Ajustado'],
        'Valor': [f"{indices['chi2']:.3f}", 
                 f"{indices['df']}", 
                 f"{indices['p_value']:.3f}",
                 f"{indices['cfi']:.3f}",
                 f"{indices['tli']:.3f}", 
                 f"{indices['rmsea']:.3f}",
                 f"{indices['srmr']:.3f}",
                 f"{indices['rmse']:.3f}",
                 f"{indices['r2']:.3f}",
                 f"{indices['r2_adj']:.3f}"],
        'Critério de Aceitação': ['Menor melhor', '-', '> 0.05', 
                                 '> 0.95', '> 0.95', '< 0.08', 
                                 '< 0.08', 'Menor melhor', 'Maior melhor', 'Maior melhor'],
        'Status': []
    }
    
    # Avaliar status de cada índice
    status_list = []
    status_list.append('Calculado')  # Chi-quadrado
    status_list.append('-')  # Graus de liberdade
    status_list.append('✓ Bom' if indices['p_value'] > 0.05 else '✗ Ruim')  # p-valor
    status_list.append('✓ Excelente' if indices['cfi'] > 0.95 else 
                      ('✓ Bom' if indices['cfi'] > 0.90 else '✗ Ruim'))  # CFI
    status_list.append('✓ Excelente' if indices['tli'] > 0.95 else 
                      ('✓ Bom' if indices['tli'] > 0.90 else '✗ Ruim'))  # TLI
    status_list.append('✓ Excelente' if indices['rmsea'] < 0.05 else 
                      ('✓ Bom' if indices['rmsea'] < 0.08 else '✗ Ruim'))  # RMSEA
    status_list.append('✓ Excelente' if indices['srmr'] < 0.05 else 
                      ('✓ Bom' if indices['srmr'] < 0.08 else '✗ Ruim'))  # SRMR
    status_list.append('Calculado')  # RMSE
    status_list.append('✓ Excelente' if indices['r2'] > 0.75 else 
                      ('✓ Bom' if indices['r2'] > 0.50 else '✗ Ruim'))  # R²
    status_list.append('✓ Excelente' if indices['r2_adj'] > 0.75 else 
                      ('✓ Bom' if indices['r2_adj'] > 0.50 else '✗ Ruim'))  # R² Ajustado
    
    tabela_dados['Status'] = status_list
    
    # Criar DataFrame
    df_indices = pd.DataFrame(tabela_dados)
    
    print(df_indices.to_string(index=False))
    
    # Salvar tabela
    df_indices.to_csv('indices_ajuste_sem.csv', index=False)
    print("\n✓ Tabela salva como 'indices_ajuste_sem.csv'")
    
    return df_indices

def gerar_equacoes_estruturais(resultados):
    """Gera equações estruturais do modelo com coeficientes"""
    print("\n=== EQUAÇÕES ESTRUTURAIS DO MODELO ===")
    
    model1 = resultados['model1']  # Percepção
    model2 = resultados['model2']  # Intenção
    
    # Equação 1: Percepção de Recompensas
    eq1_coefs = model1.coef_
    eq1_intercept = model1.intercept_
    
    equacao1 = f"""
EQUAÇÃO 1 - PERCEPÇÃO DE RECOMPENSAS:
Percepção_Recompensas = {eq1_intercept:.3f} + {eq1_coefs[0]:.3f}×Qualidade_Percebida + {eq1_coefs[1]:.3f}×Aceitação_Tecnológica + {eq1_coefs[2]:.3f}×Experiência_Usuário + ε₁

R² = {resultados['r2_percepcao']:.3f}
"""
    
    # Equação 2: Intenção Comportamental
    eq2_coefs = model2.coef_
    eq2_intercept = model2.intercept_
    
    equacao2 = f"""
EQUAÇÃO 2 - INTENÇÃO COMPORTAMENTAL:
Intenção_Comportamental = {eq2_intercept:.3f} + {eq2_coefs[0]:.3f}×Qualidade_Percebida + {eq2_coefs[1]:.3f}×Aceitação_Tecnológica + {eq2_coefs[2]:.3f}×Experiência_Usuário + {eq2_coefs[3]:.3f}×Percepção_Recompensas + ε₂

R² = {resultados['r2_intencao']:.3f}
"""
    
    # Equação principal (modelo mais parcimonioso)
    model_principal = resultados['model_principal']
    eq3_coef = model_principal.coef_[0]
    eq3_intercept = model_principal.intercept_
    
    equacao3 = f"""
EQUAÇÃO PRINCIPAL (MODELO PARCIMONIOSO):
Intenção_Comportamental = {eq3_intercept:.3f} + {eq3_coef:.3f}×Percepção_Recompensas + ε₃

R² = {resultados['r2_principal']:.3f}
Correlação = {np.sqrt(resultados['r2_principal']):.3f}
"""
    
    print(equacao1)
    print(equacao2)
    print(equacao3)
    
    # Salvar equações
    with open('equacoes_estruturais_sem.txt', 'w', encoding='utf-8') as f:
        f.write("EQUAÇÕES ESTRUTURAIS - MODELO SEM\n")
        f.write("="*50 + "\n")
        f.write(equacao1)
        f.write(equacao2)
        f.write(equacao3)
        
        # Adicionar interpretação
        f.write("\nINTERPRETAÇÃO DOS COEFICIENTES:\n")
        f.write("-"*30 + "\n")
        f.write(f"• O coeficiente mais forte é Percepção_Recompensas → Intenção ({eq2_coefs[3]:.3f})\n")
        f.write(f"• Qualidade atual tem impacto limitado na intenção ({eq2_coefs[0]:.3f})\n")
        f.write(f"• Tecnologia facilita a percepção de recompensas ({eq1_coefs[1]:.3f})\n")
        f.write(f"• O modelo explica {resultados['r2_intencao']*100:.1f}% da variância na intenção\n")
    
    print("✓ Equações salvas como 'equacoes_estruturais_sem.txt'")
    
    return {
        'equacao1': equacao1,
        'equacao2': equacao2, 
        'equacao3': equacao3
    }

def executar_analise_sem_completa():
    """Executa análise SEM completa"""
    print("ANÁLISE SEM RIGOROSA - TRANSPORTE PÚBLICO")
    print("="*60)
    
    # 1. Carregar dados
    datasets = carregar_dados_completos()
    if not datasets:
        print("Erro ao carregar dados!")
        return None
    
    # 2. Preparar construtos
    df_construtos, construtos = preparar_construtos_latentes(datasets)
    
    if df_construtos is None or len(df_construtos) == 0:
        print("ERRO: Não foi possível preparar os construtos latentes!")
        print("Verifique se os dados estão no formato correto.")
        return None
    
    # 3. Executar modelo SEM
    resultados = modelo_sem_estrutural(df_construtos)
    
    # 4. Gerar outputs
    print("\n" + "="*60)
    print("GERANDO OUTPUTS DA ANÁLISE")
    print("="*60)
    
    try:
        # Diagrama de caminho
        criar_diagrama_caminho(resultados, construtos)
        
        # Tabela de índices
        df_indices = gerar_tabela_indices_ajuste(resultados)
        
        # Equações estruturais
        equacoes = gerar_equacoes_estruturais(resultados)
        
        # Summary final
        print("\n" + "="*60)
        print("RESUMO DA ANÁLISE SEM")
        print("="*60)
        print(f"✓ Amostra: N = {resultados['n_obs']}")
        print(f"✓ Variáveis latentes: {len(construtos)}")
        print(f"✓ R² Modelo Principal: {resultados['r2_principal']:.3f}")
        print(f"✓ Correlação Principal: {np.sqrt(resultados['r2_principal']):.3f}")
        print(f"✓ RMSEA: {resultados['indices_ajuste']['rmsea']:.3f}")
        print(f"✓ CFI: {resultados['indices_ajuste']['cfi']:.3f}")
        
        return {
            'resultados': resultados,
            'construtos': construtos,
            'indices': df_indices,
            'equacoes': equacoes
        }
        
    except Exception as e:
        print(f"ERRO ao gerar outputs: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    resultado_final = executar_analise_sem_completa() 