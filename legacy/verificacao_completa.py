import pandas as pd
import numpy as np

# Carregar todos os dados
perfil = pd.read_csv('csv_extraidos/Perfil Socioeconomico.csv')
qualidade = pd.read_csv('csv_extraidos/Qualidade do serviço.csv')
percepcao = pd.read_csv('csv_extraidos/Percepção novos serviços.csv')
intencao = pd.read_csv('csv_extraidos/Intenção comportamental.csv')
utilizacao = pd.read_csv('csv_extraidos/Utilização.csv')
experiencia = pd.read_csv('csv_extraidos/Experiência do usuário.csv')
aceitacao = pd.read_csv('csv_extraidos/Aceitação da tecnologia.csv')

print('=== VERIFICAÇÃO COMPLETA DOS DADOS ===')
print(f'Total de respondentes: {len(perfil)}')
print()

# 1. GÊNERO
print('1. GÊNERO:')
genero = perfil['Gênero '].value_counts()
total = len(perfil)
for k, v in genero.items():
    print(f'   {k}: {v} ({v/total*100:.1f}%)')
print()

# 2. ESCOLARIDADE
print('2. ESCOLARIDADE:')
esc = perfil.iloc[:, 4].value_counts()
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
renda = perfil['Renda familiar mensal'].value_counts()
for k, v in renda.items():
    print(f'   {k}: {v} ({v/total*100:.1f}%)')
print()

# 5. SITUAÇÃO PROFISSIONAL
print('5. SITUAÇÃO PROFISSIONAL:')
prof = perfil['Situação profissional'].value_counts()
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
print('9. QUALIDADE - MÉDIAS:')
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
print('10. PERCEPÇÃO DE RECOMPENSAS - MÉDIAS:')
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
print('11. INTENÇÃO COMPORTAMENTAL - MÉDIAS:')
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