import pandas as pd
import numpy as np

# Carregar dados
perfil = pd.read_csv('csv_extraidos/Perfil Socioeconomico.csv')
qualidade = pd.read_csv('csv_extraidos/Qualidade do serviço.csv')
percepcao = pd.read_csv('csv_extraidos/Percepção novos serviços.csv')
intencao = pd.read_csv('csv_extraidos/Intenção comportamental.csv')
utilizacao = pd.read_csv('csv_extraidos/Utilização.csv')

print('=== DADOS REAIS PARA CORREÇÃO DO RELATÓRIO ===')
print(f'Total: {len(perfil)} respondentes')
print()

# 1. GÊNERO
print('1. GÊNERO:')
genero = perfil['Gênero\xa0'].value_counts()
total = len(perfil)
for k, v in genero.items():
    print(f'   {k}: {v} ({v/total*100:.1f}%)')
print()

# 2. ESCOLARIDADE
print('2. ESCOLARIDADE:')
esc = perfil['Nível de escolaridade\n'].value_counts()
for k, v in esc.items():
    print(f'   {k}: {v} ({v/total*100:.1f}%)')
print()

# 3. RAÇA
print('3. RAÇA:')
raca = perfil['Raça'].value_counts()
for k, v in raca.items():
    print(f'   {k}: {v} ({v/total*100:.1f}%)')
print()

# 4. RENDA
print('4. RENDA:')
renda = perfil['Renda'].value_counts()
for k, v in renda.items():
    print(f'   {k}: {v} ({v/total*100:.1f}%)')
print()

# 5. SITUAÇÃO PROFISSIONAL
print('5. SITUAÇÃO PROFISSIONAL:')
prof = perfil['Situação Profissional\xa0'].value_counts()
for k, v in prof.items():
    print(f'   {k}: {v} ({v/total*100:.1f}%)')
print()

# 6. PRINCIPAL MEIO DE TRANSPORTE
print('6. PRINCIPAL MEIO DE TRANSPORTE:')
transporte = utilizacao['Qual é o seu principal meio de transporte?'].value_counts()
for k, v in transporte.items():
    print(f'   {k}: {v} ({v/len(utilizacao)*100:.1f}%)')
print()

# 7. CARTEIRA DE MOTORISTA
print('7. CARTEIRA DE MOTORISTA:')
carteira = utilizacao['Você possui carteira de motorista?'].value_counts()
for k, v in carteira.items():
    print(f'   {k}: {v} ({v/len(utilizacao)*100:.1f}%)')
print()

# 8. FREQUÊNCIA DE USO TP
print('8. FREQUÊNCIA DE USO TP:')
freq = utilizacao['Com que frequência você utiliza o transporte público?'].value_counts()
for k, v in freq.items():
    print(f'   {k}: {v} ({v/len(utilizacao)*100:.1f}%)')
print()

# 9. QUALIDADE - MÉDIAS
print('9. QUALIDADE - MÉDIAS (escala 1-5):')
mapa_satisfacao = {
    'Muito insatisfeito': 1, 'Insatisfeito': 2, 'Neutro': 3,
    'Satisfeito': 4, 'Muito satisfeito': 5
}

qualidade_num = qualidade.copy()
for col in qualidade.columns[1:]:
    qualidade_num[col] = qualidade[col].map(mapa_satisfacao)

medias_qual = qualidade_num.iloc[:, 1:].mean().sort_values()
for item, media in medias_qual.items():
    print(f'   {item}: {media:.2f}')
print()

# 10. PERCEPÇÃO DE RECOMPENSAS - MÉDIAS
print('10. PERCEPÇÃO DE RECOMPENSAS - MÉDIAS (escala 1-5):')
mapa_concordancia = {
    'Discordo totalmente': 1, 'Discordo': 2, 'Neutro': 3,
    'Concordo': 4, 'Concordo totalmente': 5
}

percepcao_num = percepcao.copy()
for col in percepcao.columns[1:]:
    percepcao_num[col] = percepcao[col].map(mapa_concordancia)

medias_perc = percepcao_num.iloc[:, 1:].mean().sort_values(ascending=False)
for item, media in medias_perc.items():
    print(f'   {item}: {media:.2f}')
print()

# 11. INTENÇÃO COMPORTAMENTAL - MÉDIAS
print('11. INTENÇÃO COMPORTAMENTAL - MÉDIAS (escala 1-5):')
intencao_num = intencao.copy()
for col in intencao.columns[1:]:
    intencao_num[col] = intencao[col].map(mapa_concordancia)

medias_int = intencao_num.iloc[:, 1:].mean().sort_values(ascending=False)
for item, media in medias_int.items():
    print(f'   {item}: {media:.2f}')
print()

print('=== RESUMO GERAL ===')
print(f'Média geral qualidade: {qualidade_num.iloc[:, 1:].mean().mean():.2f}')
print(f'Média geral percepção: {percepcao_num.iloc[:, 1:].mean().mean():.2f}')
print(f'Média geral intenção: {intencao_num.iloc[:, 1:].mean().mean():.2f}')

# 12. CORRELAÇÕES PARA SEM
print('\n=== CORRELAÇÕES PARA MODELO SEM ===')
construtos = pd.DataFrame({
    'ID': qualidade_num['ID'],
    'Qualidade': qualidade_num.iloc[:, 1:].mean(axis=1),
    'Percepcao_Recompensas': percepcao_num.iloc[:, 1:].mean(axis=1),
    'Intencao_Comportamental': intencao_num.iloc[:, 1:].mean(axis=1)
})

construtos_clean = construtos.dropna()
corr_matrix = construtos_clean[['Qualidade', 'Percepcao_Recompensas', 'Intencao_Comportamental']].corr()

print(f'Correlação Qualidade ↔ Intenção: {corr_matrix.loc["Qualidade", "Intencao_Comportamental"]:.3f}')
print(f'Correlação Percepção ↔ Intenção: {corr_matrix.loc["Percepcao_Recompensas", "Intencao_Comportamental"]:.3f}')
print(f'Correlação Qualidade ↔ Percepção: {corr_matrix.loc["Qualidade", "Percepcao_Recompensas"]:.3f}')

# 13. MODELO SEM SIMPLES
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

X_perc = construtos_clean[['Percepcao_Recompensas']].values
X_qual = construtos_clean[['Qualidade']].values
X_both = construtos_clean[['Qualidade', 'Percepcao_Recompensas']].values
y = construtos_clean['Intencao_Comportamental'].values

model_perc = LinearRegression().fit(X_perc, y)
model_qual = LinearRegression().fit(X_qual, y)
model_both = LinearRegression().fit(X_both, y)

r2_perc = r2_score(y, model_perc.predict(X_perc))
r2_qual = r2_score(y, model_qual.predict(X_qual))
r2_both = r2_score(y, model_both.predict(X_both))

print(f'\nR² Percepção → Intenção: {r2_perc:.3f}')
print(f'R² Qualidade → Intenção: {r2_qual:.3f}')
print(f'R² Modelo Completo: {r2_both:.3f}')
print(f'Coeficiente Percepção: {model_both.coef_[1]:.3f}')
print(f'Coeficiente Qualidade: {model_both.coef_[0]:.3f}')
print(f'Casos válidos para SEM: {len(construtos_clean)}')

# 14. VERIFICAÇÕES ESPECÍFICAS PARA O RELATÓRIO
print('\n=== VERIFICAÇÕES ESPECÍFICAS ===')

# Ensino médio + superior
ensino_medio_superior = esc[esc.index.str.contains('Ensino Médio|Graduação|Pós-graduação')].sum()
print(f'Ensino médio ou superior: {ensino_medio_superior} ({ensino_medio_superior/total*100:.1f}%)')

# Negros (pretos + pardos)
negros = raca[raca.index.str.contains('Negra')].sum()
print(f'População negra: {negros} ({negros/total*100:.1f}%)')

# Mulheres
mulheres = genero.get('Feminino', 0)
print(f'Mulheres: {mulheres} ({mulheres/total*100:.1f}%)')

# Usuários de TP
usuarios_tp = transporte.get('Transporte público', 0)
print(f'Usuários de TP: {usuarios_tp} ({usuarios_tp/len(utilizacao)*100:.1f}%)')

print('\n=== DADOS CORRETOS CONFIRMADOS ===')
print('Todos os valores acima são REAIS dos dados originais!') 