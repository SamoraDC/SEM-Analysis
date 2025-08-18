import pandas as pd
import numpy as np

print('=== TESTE SIMPLES DOS DADOS ===')

# Carregar dados
try:
    perfil = pd.read_csv('csv_extraidos/Perfil Socioeconomico.csv')
    qualidade = pd.read_csv('csv_extraidos/Qualidade do serviço.csv')
    percepcao = pd.read_csv('csv_extraidos/Percepção novos serviços.csv')
    intencao = pd.read_csv('csv_extraidos/Intenção comportamental.csv')
    
    print(f'✓ Dados carregados: {len(perfil)} respondentes')
    
    # Função para converter valores de forma segura
    def converter_para_numerico(valor):
        if pd.isna(valor):
            return np.nan
        if isinstance(valor, (int, float)):
            return float(valor)
        
        valor_str = str(valor).lower().strip()
        
        # Mapeamento de satisfação
        mapa_satisfacao = {
            'muito insatisfeito': 1, 'insatisfeito': 2, 'neutro': 3,
            'satisfeito': 4, 'muito satisfeito': 5
        }
        
        # Mapeamento de concordância 
        mapa_concordancia = {
            'discordo totalmente': 1, 'discordo': 2, 'neutro': 3,
            'concordo': 4, 'concordo totalmente': 5
        }
        
        if valor_str in mapa_satisfacao:
            return mapa_satisfacao[valor_str]
        elif valor_str in mapa_concordancia:
            return mapa_concordancia[valor_str]
        else:
            # Tentar converter diretamente para número
            try:
                return float(valor_str)
            except:
                return 3.0  # Neutro como padrão
    
    # Processar qualidade (pular ID)
    print('Processando qualidade...')
    qualidade_cols = [col for col in qualidade.columns if col != 'ID']
    qualidade_valores = []
    
    for idx, row in qualidade.iterrows():
        valores_linha = []
        for col in qualidade_cols:
            val_convertido = converter_para_numerico(row[col])
            valores_linha.append(val_convertido)
        
        media_linha = np.nanmean(valores_linha) if valores_linha else np.nan
        qualidade_valores.append(media_linha)
    
    # Processar percepção (pular ID)
    print('Processando percepção...')
    percepcao_cols = [col for col in percepcao.columns if col != 'ID']
    percepcao_valores = []
    
    for idx, row in percepcao.iterrows():
        valores_linha = []
        for col in percepcao_cols:
            val_convertido = converter_para_numerico(row[col])
            valores_linha.append(val_convertido)
        
        media_linha = np.nanmean(valores_linha) if valores_linha else np.nan
        percepcao_valores.append(media_linha)
    
    # Processar intenção (pular ID)
    print('Processando intenção...')
    intencao_cols = [col for col in intencao.columns if col != 'ID']
    intencao_valores = []
    
    for idx, row in intencao.iterrows():
        valores_linha = []
        for col in intencao_cols:
            val_convertido = converter_para_numerico(row[col])
            valores_linha.append(val_convertido)
        
        media_linha = np.nanmean(valores_linha) if valores_linha else np.nan
        intencao_valores.append(media_linha)
    
    # Criar DataFrame final
    construtos = pd.DataFrame({
        'Qualidade': qualidade_valores[:len(percepcao_valores)],
        'Percepcao_Recompensas': percepcao_valores,
        'Intencao_Comportamental': intencao_valores[:len(percepcao_valores)]
    })
    
    # Remover NaN
    construtos_clean = construtos.dropna()
    
    print(f'\n=== RESULTADOS ===')
    print(f'✓ Casos válidos: {len(construtos_clean)}')
    print(f'✓ Média Qualidade: {construtos_clean["Qualidade"].mean():.2f}')
    print(f'✓ Média Percepção: {construtos_clean["Percepcao_Recompensas"].mean():.2f}')
    print(f'✓ Média Intenção: {construtos_clean["Intencao_Comportamental"].mean():.2f}')
    
    # Calcular correlação
    correlacao = construtos_clean['Percepcao_Recompensas'].corr(construtos_clean['Intencao_Comportamental'])
    print(f'✓ Correlação Percepção ↔ Intenção: {correlacao:.3f}')
    
    # Calcular R²
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    
    X = construtos_clean[['Percepcao_Recompensas']].values
    y = construtos_clean['Intencao_Comportamental'].values
    model = LinearRegression().fit(X, y)
    r2 = r2_score(y, model.predict(X))
    
    print(f'✓ R² Percepção → Intenção: {r2:.3f}')
    print(f'✓ Coeficiente: {model.coef_[0]:.3f}')
    
    print('\n=== VALIDAÇÃO DOS RESULTADOS ESPERADOS ===')
    print(f'Amostra esperada: 703, obtida: {len(perfil)} {"✓" if len(perfil) == 703 else "✗"}')
    print(f'Correlação esperada: ~0.896, obtida: {correlacao:.3f} {"✓" if abs(correlacao - 0.896) < 0.1 else "✗"}')
    print(f'R² esperado: ~0.803, obtido: {r2:.3f} {"✓" if abs(r2 - 0.803) < 0.1 else "✗"}')
    
except Exception as e:
    print(f'Erro: {e}')
    import traceback
    traceback.print_exc() 