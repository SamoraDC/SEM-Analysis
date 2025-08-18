import pandas as pd
import numpy as np

# Carregar dados
perfil = pd.read_csv('csv_extraidos/Perfil Socioeconomico.csv')

print('=== ANÁLISE CORRETA DE ESCOLARIDADE ===')
escolaridade_col = perfil.columns[4]
print(f'Coluna: {escolaridade_col}')
print()

escolaridade_counts = perfil[escolaridade_col].value_counts()
total = len(perfil)

print('Distribuição Real de Escolaridade:')
for nivel, count in escolaridade_counts.items():
    pct = (count / total) * 100
    print(f'  {nivel}: {count} ({pct:.1f}%)')

print(f'\nTotal de respondentes: {total}')

# Verificar outras variáveis importantes
print('\n=== OUTRAS VARIÁVEIS ===')
print(f'Gênero:')
genero_counts = perfil['Gênero '].value_counts()
for genero, count in genero_counts.items():
    pct = (count / total) * 100
    print(f'  {genero}: {count} ({pct:.1f}%)')

print(f'\nRaça:')
raca_counts = perfil['Raça'].value_counts()
for raca, count in raca_counts.items():
    pct = (count / total) * 100
    print(f'  {raca}: {count} ({pct:.1f}%)')

print(f'\nRenda:')
renda_counts = perfil['Renda'].value_counts()
for renda, count in renda_counts.items():
    pct = (count / total) * 100
    print(f'  {renda}: {count} ({pct:.1f}%)') 