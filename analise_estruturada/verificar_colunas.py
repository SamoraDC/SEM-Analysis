import pandas as pd
import os

# Configurar caminhos
csv_dir = os.path.join('..', 'csv_extraidos')

# Lista de arquivos
arquivos = [
    'Qualidade do serviço.csv',
    'Utilização.csv', 
    'Percepção novos serviços.csv',
    'Intenção comportamental.csv',
    'Aceitação da tecnologia.csv',
    'Experiência do usuário.csv',
    'Perfil Socioeconomico.csv'
]

print("=== VERIFICACAO DE COLUNAS DOS DATASETS ===\n")

for arquivo in arquivos:
    try:
        caminho = os.path.join(csv_dir, arquivo)
        df = pd.read_csv(caminho)
        print(f"{arquivo}:")
        print(f"  Shape: {df.shape}")
        print(f"  Colunas: {list(df.columns)}")
        print()
    except Exception as e:
        print(f"ERRO ao carregar {arquivo}: {e}")
        print()

print("=== VERIFICACAO CONCLUIDA ===") 