import pandas as pd

# Carregar dados
perfil = pd.read_csv('csv_extraidos/Perfil Socioeconomico.csv')

print('DADOS REAIS:')
print(f'Total: {len(perfil)} respondentes')

# Gênero
print('\nGÊNERO:')
genero = perfil.iloc[:, 1].value_counts()
for k, v in genero.items():
    print(f'{k}: {v} ({v/len(perfil)*100:.1f}%)')

# Escolaridade
print('\nESCOLARIDADE:')
esc = perfil.iloc[:, 4].value_counts()
for k, v in esc.items():
    print(f'{k}: {v} ({v/len(perfil)*100:.1f}%)')

# Raça
print('\nRAÇA:')
raca = perfil.iloc[:, 2].value_counts()
for k, v in raca.items():
    print(f'{k}: {v} ({v/len(perfil)*100:.1f}%)')

print('\nDados extraídos com sucesso!') 