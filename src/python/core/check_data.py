import pandas as pd

# Carregar dados
perfil = pd.read_csv('csv_extraidos/Perfil Socioeconomico.csv')

print('DADOS REAIS:')
print(f'Total: {len(perfil)} respondentes')
print()

# Escolaridade
print('ESCOLARIDADE:')
esc = perfil.iloc[:, 4].value_counts()
for k, v in esc.items():
    print(f'{k}: {v} ({v/len(perfil)*100:.1f}%)')

print()

# Gênero  
print('GÊNERO:')
gen = perfil.iloc[:, 1].value_counts()
for k, v in gen.items():
    print(f'{k}: {v} ({v/len(perfil)*100:.1f}%)') 