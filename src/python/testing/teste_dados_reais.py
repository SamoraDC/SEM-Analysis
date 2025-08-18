import pandas as pd
import numpy as np

# Carregar dados
print('=== TESTE DOS DADOS REAIS ===')
perfil = pd.read_csv('csv_extraidos/Perfil Socioeconomico.csv')
qualidade = pd.read_csv('csv_extraidos/Qualidade do serviço.csv')
percepcao = pd.read_csv('csv_extraidos/Percepção novos serviços.csv')
intencao = pd.read_csv('csv_extraidos/Intenção comportamental.csv')
utilizacao = pd.read_csv('csv_extraidos/Utilização.csv')

print(f'Total: {len(perfil)} respondentes')
print()

# 1. GÊNERO
print('1. GÊNERO:')
# Verificar nomes das colunas
print("Colunas do perfil:", perfil.columns.tolist())
genero_col = [col for col in perfil.columns if 'gênero' in col.lower() or 'genero' in col.lower()]
if genero_col:
    genero = perfil[genero_col[0]].value_counts()
    total = len(perfil)
    for k, v in genero.items():
        print(f'   {k}: {v} ({v/total*100:.1f}%)')
print()

# 2. PRINCIPAL MEIO DE TRANSPORTE
print('2. PRINCIPAL MEIO DE TRANSPORTE:')
print("Colunas da utilização:", utilizacao.columns.tolist()[:3])
transporte_col = [col for col in utilizacao.columns if 'forma' in col.lower() and 'viagem' in col.lower()]
if transporte_col:
    transporte = utilizacao[transporte_col[0]].value_counts()
    for k, v in transporte.items():
        print(f'   {k}: {v} ({v/len(utilizacao)*100:.1f}%)')
print()

# 3. MAPEAR ESCALAS
print('3. PROCESSAMENTO DE ESCALAS:')
mapa_satisfacao = {
    'Muito insatisfeito': 1, 'Insatisfeito': 2, 'Neutro': 3,
    'Satisfeito': 4, 'Muito satisfeito': 5
}

mapa_concordancia = {
    'Discordo totalmente': 1, 'Discordo': 2, 'Neutro': 3,
    'Concordo': 4, 'Concordo totalmente': 5
}

# Processar qualidade
qualidade_num = qualidade.copy()
for col in qualidade.columns[1:]:
    if col in qualidade_num.columns:
        qualidade_num[col] = qualidade[col].map(mapa_satisfacao).fillna(qualidade[col])

# Processar percepção
percepcao_num = percepcao.copy()
for col in percepcao.columns[1:]:
    if col in percepcao_num.columns:
        percepcao_num[col] = percepcao[col].map(mapa_concordancia).fillna(percepcao[col])

# Processar intenção
intencao_num = intencao.copy()
for col in intencao.columns[1:]:
    if col in intencao_num.columns:
        intencao_num[col] = intencao[col].map(mapa_concordancia).fillna(intencao[col])

# Calcular médias
print('Calculando construtos...')
construtos = pd.DataFrame({
    'ID': qualidade_num['ID'],
    'Qualidade': qualidade_num.iloc[:, 1:].mean(axis=1),
    'Percepcao_Recompensas': percepcao_num.iloc[:, 1:].mean(axis=1),
    'Intencao_Comportamental': intencao_num.iloc[:, 1:].mean(axis=1)
})

construtos_clean = construtos.dropna()

print(f'Casos válidos: {len(construtos_clean)}')
print(f'Média Qualidade: {construtos_clean["Qualidade"].mean():.2f}')
print(f'Média Percepção: {construtos_clean["Percepcao_Recompensas"].mean():.2f}')
print(f'Média Intenção: {construtos_clean["Intencao_Comportamental"].mean():.2f}')

# Correlação principal
corr_principal = construtos_clean['Percepcao_Recompensas'].corr(construtos_clean['Intencao_Comportamental'])
print(f'\nCorrelação Percepção ↔ Intenção: {corr_principal:.3f}')

# Modelo de regressão
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

X = construtos_clean[['Percepcao_Recompensas']].values
y = construtos_clean['Intencao_Comportamental'].values
model = LinearRegression().fit(X, y)
r2 = r2_score(y, model.predict(X))

print(f'R² Percepção → Intenção: {r2:.3f}')
print(f'Coeficiente: {model.coef_[0]:.3f}')

print('\n=== RESULTADOS PRINCIPAIS ===')
print(f'✓ Amostra: {len(perfil)} respondentes')
print(f'✓ Correlação: {corr_principal:.3f}')
print(f'✓ R²: {r2:.3f}')
print('✓ Processamento concluído com sucesso!') 