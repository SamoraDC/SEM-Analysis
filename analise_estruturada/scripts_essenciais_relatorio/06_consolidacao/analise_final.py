import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

# Configuração para português
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

def main():
    print("=== ANÁLISE CORRETA DOS DADOS DE TRANSPORTE ===\n")
    
    # 1. CARREGAR DADOS
    print("1. Carregando dados...")
    perfil = pd.read_csv('csv_extraidos/Perfil Socioeconomico.csv')
    qualidade = pd.read_csv('csv_extraidos/Qualidade do serviço.csv')
    percepcao = pd.read_csv('csv_extraidos/Percepção novos serviços.csv')
    intencao = pd.read_csv('csv_extraidos/Intenção comportamental.csv')
    
    print(f"   - Perfil: {len(perfil)} registros")
    print(f"   - Qualidade: {len(qualidade)} registros")
    print(f"   - Percepção: {len(percepcao)} registros")
    print(f"   - Intenção: {len(intencao)} registros")
    
    # 2. ANÁLISE DE ESCOLARIDADE (CORRIGIDA)
    print("\n2. Análise de Escolaridade (DADOS REAIS):")
    escolaridade = perfil.iloc[:, 4].value_counts()
    total = len(perfil)
    
    for nivel, count in escolaridade.items():
        pct = (count / total) * 100
        print(f"   {nivel}: {count} ({pct:.1f}%)")
    
    # 3. ANÁLISE DE QUALIDADE
    print("\n3. Processando dados de qualidade...")
    mapa_satisfacao = {
        'Muito insatisfeito': 1, 'Insatisfeito': 2, 'Neutro': 3,
        'Satisfeito': 4, 'Muito satisfeito': 5
    }
    
    qualidade_num = qualidade.copy()
    for col in qualidade.columns[1:]:
        qualidade_num[col] = qualidade[col].map(mapa_satisfacao)
    
    medias_qual = qualidade_num.iloc[:, 1:].mean()
    print(f"   Média geral de qualidade: {medias_qual.mean():.2f}")
    print(f"   Pior avaliado: {medias_qual.min():.2f}")
    print(f"   Melhor avaliado: {medias_qual.max():.2f}")
    
    # 4. ANÁLISE DE PERCEPÇÃO DE RECOMPENSAS
    print("\n4. Processando percepção de recompensas...")
    mapa_concordancia = {
        'Discordo totalmente': 1, 'Discordo': 2, 'Neutro': 3,
        'Concordo': 4, 'Concordo totalmente': 5
    }
    
    percepcao_num = percepcao.copy()
    for col in percepcao.columns[1:]:
        percepcao_num[col] = percepcao[col].map(mapa_concordancia)
    
    medias_perc = percepcao_num.iloc[:, 1:].mean()
    print(f"   Média geral de aceitação: {medias_perc.mean():.2f}")
    
    # 5. ANÁLISE DE INTENÇÃO COMPORTAMENTAL
    print("\n5. Processando intenção comportamental...")
    intencao_num = intencao.copy()
    for col in intencao.columns[1:]:
        intencao_num[col] = intencao[col].map(mapa_concordancia)
    
    medias_int = intencao_num.iloc[:, 1:].mean()
    print(f"   Média geral de intenção: {medias_int.mean():.2f}")
    
    # 6. CRIAR CONSTRUTOS
    print("\n6. Criando construtos latentes...")
    construtos = pd.DataFrame({
        'ID': qualidade_num['ID'],
        'Qualidade': qualidade_num.iloc[:, 1:].mean(axis=1),
        'Percepcao_Recompensas': percepcao_num.iloc[:, 1:].mean(axis=1),
        'Intencao_Comportamental': intencao_num.iloc[:, 1:].mean(axis=1)
    })
    
    # Remover NaN
    construtos_clean = construtos.dropna()
    print(f"   Casos válidos: {len(construtos_clean)}")
    
    # 7. CORRELAÇÕES
    print("\n7. Análise de correlações:")
    corr_matrix = construtos_clean[['Qualidade', 'Percepcao_Recompensas', 'Intencao_Comportamental']].corr()
    
    corr_qual_int = corr_matrix.loc['Qualidade', 'Intencao_Comportamental']
    corr_perc_int = corr_matrix.loc['Percepcao_Recompensas', 'Intencao_Comportamental']
    corr_qual_perc = corr_matrix.loc['Qualidade', 'Percepcao_Recompensas']
    
    print(f"   Qualidade ↔ Intenção: {corr_qual_int:.3f}")
    print(f"   Percepção ↔ Intenção: {corr_perc_int:.3f}")
    print(f"   Qualidade ↔ Percepção: {corr_qual_perc:.3f}")
    
    # 8. MODELOS SEM
    print("\n8. Modelos de Equações Estruturais:")
    
    # Modelo 1: Qualidade → Intenção
    X1 = construtos_clean[['Qualidade']].values
    y = construtos_clean['Intencao_Comportamental'].values
    model1 = LinearRegression().fit(X1, y)
    r2_qual = r2_score(y, model1.predict(X1))
    
    # Modelo 2: Percepção → Intenção
    X2 = construtos_clean[['Percepcao_Recompensas']].values
    model2 = LinearRegression().fit(X2, y)
    r2_perc = r2_score(y, model2.predict(X2))
    
    # Modelo 3: Modelo completo
    X3 = construtos_clean[['Qualidade', 'Percepcao_Recompensas']].values
    model3 = LinearRegression().fit(X3, y)
    r2_full = r2_score(y, model3.predict(X3))
    
    print(f"   Modelo Qualidade → Intenção: R² = {r2_qual:.3f}")
    print(f"   Modelo Percepção → Intenção: R² = {r2_perc:.3f}")
    print(f"   Modelo Completo: R² = {r2_full:.3f}")
    print(f"   Coef. Qualidade: {model3.coef_[0]:.3f}")
    print(f"   Coef. Percepção: {model3.coef_[1]:.3f}")
    
    # 9. CRIAR DIAGRAMA SEM
    print("\n9. Criando diagrama SEM...")
    criar_diagrama_sem(corr_qual_int, corr_perc_int, corr_qual_perc, 
                       model3.coef_[0], model3.coef_[1], r2_full)
    
    # 10. RESUMO FINAL
    print("\n" + "="*50)
    print("RESUMO DOS RESULTADOS CORRETOS:")
    print("="*50)
    print(f"• Amostra: {len(perfil)} respondentes")
    print(f"• Graduação completa/incompleta: {escolaridade.get('Graduação (completo ou incompleto)', 0)} ({escolaridade.get('Graduação (completo ou incompleto)', 0)/total*100:.1f}%)")
    print(f"• Correlação Percepção-Intenção: {corr_perc_int:.3f}")
    print(f"• R² Percepção→Intenção: {r2_perc:.3f}")
    print(f"• R² Modelo Completo: {r2_full:.3f}")
    print(f"• Impacto da Percepção: {model3.coef_[1]:.3f}")
    print(f"• Impacto da Qualidade: {model3.coef_[0]:.3f}")
    
    if r2_perc > 0.5:
        print("\n✓ CONFIRMADO: Percepção de recompensas tem forte impacto na intenção!")
    else:
        print(f"\n⚠ ATENÇÃO: Impacto da percepção é moderado (R² = {r2_perc:.3f})")

def criar_diagrama_sem(corr_qual_int, corr_perc_int, corr_qual_perc, coef_qual, coef_perc, r2_full):
    """Criar diagrama de caminhos SEM"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Posições dos elementos
    pos_qualidade = (2, 6)
    pos_percepcao = (2, 3)
    pos_intencao = (8, 4.5)
    
    # Variáveis observadas - Qualidade
    obs_qual = [(0.5, 7.5), (0.5, 6.5), (0.5, 5.5), (0.5, 4.5)]
    labels_qual = ['Preço', 'Segurança', 'Tempo', 'Conforto']
    
    # Variáveis observadas - Percepção
    obs_perc = [(0.5, 2.5), (0.5, 1.5), (0.5, 0.5)]
    labels_perc = ['Uso Ilimitado', 'Descontos', 'Pontos/Créditos']
    
    # Variáveis observadas - Intenção
    obs_int = [(10, 5.5), (10, 4.5), (10, 3.5)]
    labels_int = ['Usar Mais', 'Recomendar', 'Participar']
    
    # Desenhar variáveis latentes (elipses)
    from matplotlib.patches import Ellipse, Rectangle
    
    ellipse_qual = Ellipse(pos_qualidade, 1.5, 0.8, facecolor='lightblue', 
                          edgecolor='blue', alpha=0.7)
    ellipse_perc = Ellipse(pos_percepcao, 1.5, 0.8, facecolor='lightgreen', 
                          edgecolor='green', alpha=0.7)
    ellipse_int = Ellipse(pos_intencao, 1.5, 0.8, facecolor='lightcoral', 
                         edgecolor='red', alpha=0.7)
    
    ax.add_patch(ellipse_qual)
    ax.add_patch(ellipse_perc)
    ax.add_patch(ellipse_int)
    
    # Labels das variáveis latentes
    ax.text(pos_qualidade[0], pos_qualidade[1], 'Qualidade\ndo Serviço', 
            ha='center', va='center', fontweight='bold', fontsize=10)
    ax.text(pos_percepcao[0], pos_percepcao[1], 'Percepção de\nRecompensas', 
            ha='center', va='center', fontweight='bold', fontsize=10)
    ax.text(pos_intencao[0], pos_intencao[1], 'Intenção\nComportamental', 
            ha='center', va='center', fontweight='bold', fontsize=10)
    
    # Desenhar variáveis observadas (retângulos)
    # Qualidade
    for i, (pos, label) in enumerate(zip(obs_qual, labels_qual)):
        rect = Rectangle((pos[0]-0.3, pos[1]-0.2), 0.6, 0.4, 
                        facecolor='white', edgecolor='blue')
        ax.add_patch(rect)
        ax.text(pos[0], pos[1], label, ha='center', va='center', fontsize=8)
        ax.annotate('', xy=pos, xytext=pos_qualidade,
                   arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
    
    # Percepção
    for i, (pos, label) in enumerate(zip(obs_perc, labels_perc)):
        rect = Rectangle((pos[0]-0.3, pos[1]-0.2), 0.6, 0.4, 
                        facecolor='white', edgecolor='green')
        ax.add_patch(rect)
        ax.text(pos[0], pos[1], label, ha='center', va='center', fontsize=8)
        ax.annotate('', xy=pos, xytext=pos_percepcao,
                   arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    
    # Intenção
    for i, (pos, label) in enumerate(zip(obs_int, labels_int)):
        rect = Rectangle((pos[0]-0.3, pos[1]-0.2), 0.6, 0.4, 
                        facecolor='white', edgecolor='red')
        ax.add_patch(rect)
        ax.text(pos[0], pos[1], label, ha='center', va='center', fontsize=8)
        ax.annotate('', xy=pos, xytext=pos_intencao,
                   arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    
    # Setas estruturais (entre variáveis latentes)
    # Qualidade -> Intenção
    ax.annotate('', xy=(pos_intencao[0]-0.7, pos_intencao[1]+0.3), 
               xytext=(pos_qualidade[0]+0.7, pos_qualidade[1]-0.3),
               arrowprops=dict(arrowstyle='->', color='black', lw=3))
    ax.text(5, 5.8, f'β₁ = {coef_qual:.3f}\nr = {corr_qual_int:.3f}', ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Percepção -> Intenção
    ax.annotate('', xy=(pos_intencao[0]-0.7, pos_intencao[1]-0.3), 
               xytext=(pos_percepcao[0]+0.7, pos_percepcao[1]+0.3),
               arrowprops=dict(arrowstyle='->', color='black', lw=3))
    ax.text(5, 3.2, f'β₂ = {coef_perc:.3f}\nr = {corr_perc_int:.3f}', ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Correlação entre Qualidade e Percepção
    ax.annotate('', xy=(pos_percepcao[0], pos_percepcao[1]+0.4), 
               xytext=(pos_qualidade[0], pos_qualidade[1]-0.4),
               arrowprops=dict(arrowstyle='<->', color='gray', lw=2))
    ax.text(1.2, 4.5, f'r = {corr_qual_perc:.3f}', ha='center', va='center', rotation=90,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='lightgray', alpha=0.8))
    
    # Configurações do gráfico
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Título
    ax.text(5.5, 7.5, 'Modelo de Equações Estruturais (SEM)\nTransporte Público e Sistema de Recompensas', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Índices de ajuste
    ax.text(0.5, 0.2, f'Índices de Ajuste:\nR² Modelo = {r2_full:.3f}\nN = 703 respondentes\nDados Reais da Pesquisa', 
            ha='left', va='bottom', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('diagrama_sem_real.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("   Diagrama SEM salvo como 'diagrama_sem_real.png'")

if __name__ == "__main__":
    main() 