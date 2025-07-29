import pandas as pd
import numpy as np
import os
from datetime import datetime

print("=" * 80)
print("RELATORIO DE VERIFICACAO - ANALISE ESTRUTURADA")
print("=" * 80)
print(f"Data de Execucao: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print()

# Configurar caminhos
csv_dir = os.path.join('..', 'csv_extraidos')
output_dir = os.path.join('outputs', 'relatorios')
os.makedirs(output_dir, exist_ok=True)

try:
    # Carregar dados principais
    perfil = pd.read_csv(os.path.join(csv_dir, 'Perfil Socioeconomico.csv'))
    qualidade = pd.read_csv(os.path.join(csv_dir, 'Qualidade do serviço.csv'))
    percepcao = pd.read_csv(os.path.join(csv_dir, 'Percepção novos serviços.csv'))
    intencao = pd.read_csv(os.path.join(csv_dir, 'Intenção comportamental.csv'))
    
    print("✅ DADOS CARREGADOS COM SUCESSO")
    print(f"   - Perfil Socioeconômico: {len(perfil)} respondentes")
    print(f"   - Qualidade do Serviço: {len(qualidade)} respondentes")
    print(f"   - Percepção de Recompensas: {len(percepcao)} respondentes")
    print(f"   - Intenção Comportamental: {len(intencao)} respondentes")
    print()
    
    # ===== VERIFICAÇÕES PRINCIPAIS =====
    print("📊 VERIFICACOES PRINCIPAIS vs RELATORIO ORIGINAL")
    print("-" * 60)
    
    # 1. TOTAL DE RESPONDENTES
    total_respondentes = len(perfil)
    print(f"1. Total de Respondentes:")
    print(f"   Encontrado: {total_respondentes}")
    print(f"   Esperado: 703")
    print(f"   Status: {'✅ CORRETO' if total_respondentes == 703 else '❌ DIVERGENTE'}")
    print()
    
    # 2. GÊNERO
    print("2. Distribuição por Gênero:")
    genero = perfil['Gênero\xa0'].value_counts()
    feminino_pct = (genero.get('Feminino', 0) / total_respondentes) * 100
    masculino_pct = (genero.get('Masculino', 0) / total_respondentes) * 100
    
    print(f"   Feminino: {genero.get('Feminino', 0)} ({feminino_pct:.1f}%)")
    print(f"   Masculino: {genero.get('Masculino', 0)} ({masculino_pct:.1f}%)")
    print(f"   Esperado Feminino: 61.5%")
    print(f"   Status Feminino: {'✅ CORRETO' if abs(feminino_pct - 61.5) < 0.1 else '❌ DIVERGENTE'}")
    print()
    
    # 3. ETNIA/RAÇA
    print("3. Distribuição por Etnia:")
    raca = perfil['Raça'].value_counts()
    negros_pct = (raca.get('Negra ( pretos e pardos)', 0) / total_respondentes) * 100
    brancos_pct = (raca.get('Branca', 0) / total_respondentes) * 100
    
    print(f"   População Negra: {raca.get('Negra ( pretos e pardos)', 0)} ({negros_pct:.1f}%)")
    print(f"   População Branca: {raca.get('Branca', 0)} ({brancos_pct:.1f}%)")
    print(f"   Esperado Negros: 59.2%")
    print(f"   Status Negros: {'✅ CORRETO' if abs(negros_pct - 59.2) < 0.1 else '❌ DIVERGENTE'}")
    print()
    
    # 4. ESCOLARIDADE
    print("4. Nível de Escolaridade:")
    esc = perfil['Nível de escolaridade\n'].value_counts()
    
    # Calcular ensino médio ou superior
    ensino_medio_superior = 0
    for categoria in esc.index:
        if any(termo in categoria for termo in ['Ensino Médio', 'Graduação', 'Pós-graduação']):
            ensino_medio_superior += esc[categoria]
    
    ems_pct = (ensino_medio_superior / total_respondentes) * 100
    print(f"   Ensino Médio ou Superior: {ensino_medio_superior} ({ems_pct:.1f}%)")
    print(f"   Esperado: 82.2%")
    print(f"   Status: {'✅ CORRETO' if abs(ems_pct - 82.2) < 1.0 else '❌ DIVERGENTE'}")
    print()
    
    # 5. ANÁLISE DE QUALIDADE
    print("5. Análise de Qualidade do Serviço:")
    mapa_satisfacao = {
        'Muito insatisfeito': 1, 'Insatisfeito': 2, 'Neutro': 3,
        'Satisfeito': 4, 'Muito satisfeito': 5
    }
    
    qualidade_num = qualidade.copy()
    for col in qualidade.columns[1:]:
        qualidade_num[col] = qualidade[col].map(mapa_satisfacao)
    
    media_qualidade = qualidade_num.iloc[:, 1:].mean().mean()
    print(f"   Média Geral de Qualidade: {media_qualidade:.2f}")
    print(f"   Esperado: 1.64")
    print(f"   Status: {'✅ CORRETO' if abs(media_qualidade - 1.64) < 0.1 else '❌ DIVERGENTE'}")
    print()
    
    # 6. ANÁLISE DE PERCEPÇÃO DE RECOMPENSAS
    print("6. Percepção de Recompensas:")
    mapa_concordancia = {
        'Discordo totalmente': 1, 'Discordo': 2, 'Neutro': 3,
        'Concordo': 4, 'Concordo totalmente': 5
    }
    
    percepcao_num = percepcao.copy()
    for col in percepcao.columns[1:]:
        percepcao_num[col] = percepcao[col].map(mapa_concordancia)
    
    media_percepcao = percepcao_num.iloc[:, 1:].mean().mean()
    print(f"   Média Geral de Percepção: {media_percepcao:.2f}")
    print(f"   Esperado: 4.51")
    print(f"   Status: {'✅ CORRETO' if abs(media_percepcao - 4.51) < 0.1 else '❌ DIVERGENTE'}")
    print()
    
    # 7. ANÁLISE DE INTENÇÃO COMPORTAMENTAL
    print("7. Intenção Comportamental:")
    intencao_num = intencao.copy()
    for col in intencao.columns[1:]:
        intencao_num[col] = intencao[col].map(mapa_concordancia)
    
    media_intencao = intencao_num.iloc[:, 1:].mean().mean()
    print(f"   Média Geral de Intenção: {media_intencao:.2f}")
    print(f"   Esperado: 4.55")
    print(f"   Status: {'✅ CORRETO' if abs(media_intencao - 4.55) < 0.1 else '❌ DIVERGENTE'}")
    print()
    
    # 8. MODELO SEM PRINCIPAL
    print("8. Modelo SEM - Percepção → Intenção:")
    
    # Criar construtos
    construtos = pd.DataFrame({
        'ID': qualidade_num['ID'],
        'Qualidade': qualidade_num.iloc[:, 1:].mean(axis=1),
        'Percepcao_Recompensas': percepcao_num.iloc[:, 1:].mean(axis=1),
        'Intencao_Comportamental': intencao_num.iloc[:, 1:].mean(axis=1)
    })
    
    construtos_clean = construtos.dropna()
    
    # Calcular correlação
    corr_percepcao_intencao = construtos_clean['Percepcao_Recompensas'].corr(construtos_clean['Intencao_Comportamental'])
    
    # Modelo de regressão
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    
    X = construtos_clean[['Percepcao_Recompensas']].values
    y = construtos_clean['Intencao_Comportamental'].values
    
    model = LinearRegression().fit(X, y)
    r2 = r2_score(y, model.predict(X))
    
    print(f"   Correlação Percepção ↔ Intenção: {corr_percepcao_intencao:.3f}")
    print(f"   R² do Modelo: {r2:.3f}")
    print(f"   Casos Válidos: {len(construtos_clean)}")
    print(f"   Esperado Correlação: 0.896")
    print(f"   Esperado R²: 0.803")
    print(f"   Status Correlação: {'✅ CORRETO' if abs(corr_percepcao_intencao - 0.896) < 0.05 else '❌ DIVERGENTE'}")
    print(f"   Status R²: {'✅ CORRETO' if abs(r2 - 0.803) < 0.05 else '❌ DIVERGENTE'}")
    print()
    
    # ===== RESUMO FINAL =====
    print("=" * 80)
    print("📋 RESUMO DA VERIFICAÇÃO")
    print("=" * 80)
    
    verificacoes = [
        ("Total de Respondentes", total_respondentes == 703),
        ("Predominância Feminina", abs(feminino_pct - 61.5) < 0.1),
        ("População Negra", abs(negros_pct - 59.2) < 0.1),
        ("Ensino Médio/Superior", abs(ems_pct - 82.2) < 1.0),
        ("Qualidade Baixa", abs(media_qualidade - 1.64) < 0.1),
        ("Percepção Alta", abs(media_percepcao - 4.51) < 0.1),
        ("Intenção Alta", abs(media_intencao - 4.55) < 0.1),
        ("Correlação SEM", abs(corr_percepcao_intencao - 0.896) < 0.05),
        ("R² do Modelo", abs(r2 - 0.803) < 0.05)
    ]
    
    sucessos = sum(1 for _, status in verificacoes if status)
    total_verificacoes = len(verificacoes)
    
    print(f"✅ Verificações Corretas: {sucessos}/{total_verificacoes}")
    print(f"❌ Verificações Divergentes: {total_verificacoes - sucessos}/{total_verificacoes}")
    print(f"📊 Taxa de Conformidade: {(sucessos/total_verificacoes)*100:.1f}%")
    print()
    
    for nome, status in verificacoes:
        emoji = "✅" if status else "❌"
        print(f"{emoji} {nome}")
    
    print()
    
    if sucessos == total_verificacoes:
        print("🎉 VERIFICAÇÃO COMPLETA: Todos os resultados batem com o relatório original!")
    elif sucessos >= total_verificacoes * 0.8:
        print("⚠️ VERIFICAÇÃO PARCIAL: Maioria dos resultados está correta.")
    else:
        print("❌ VERIFICAÇÃO FALHOU: Muitas divergências encontradas.")
    
    # Salvar relatório
    relatorio_path = os.path.join(output_dir, 'RELATORIO_VERIFICACAO_FINAL.md')
    
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO DE VERIFICAÇÃO FINAL - ANÁLISE ESTRUTURADA\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write(f"## 📊 RESULTADOS DA VERIFICAÇÃO\n\n")
        f.write(f"**Taxa de Conformidade:** {(sucessos/total_verificacoes)*100:.1f}%\n")
        f.write(f"**Verificações Corretas:** {sucessos}/{total_verificacoes}\n\n")
        
        f.write("### Principais Descobertas Confirmadas:\n\n")
        f.write(f"- **Total de Respondentes:** {total_respondentes} (703 esperado)\n")
        f.write(f"- **Predominância Feminina:** {feminino_pct:.1f}% (61.5% esperado)\n")
        f.write(f"- **População Negra:** {negros_pct:.1f}% (59.2% esperado)\n")
        f.write(f"- **Ensino Médio/Superior:** {ems_pct:.1f}% (82.2% esperado)\n")
        f.write(f"- **Qualidade Média:** {media_qualidade:.2f} (1.64 esperado)\n")
        f.write(f"- **Percepção Recompensas:** {media_percepcao:.2f} (4.51 esperado)\n")
        f.write(f"- **Intenção Comportamental:** {media_intencao:.2f} (4.55 esperado)\n")
        f.write(f"- **Correlação Percepção→Intenção:** {corr_percepcao_intencao:.3f} (0.896 esperado)\n")
        f.write(f"- **R² do Modelo SEM:** {r2:.3f} (0.803 esperado)\n\n")
        
        f.write("### Status das Verificações:\n\n")
        for nome, status in verificacoes:
            emoji = "✅" if status else "❌"
            f.write(f"{emoji} {nome}\n")
        
        f.write(f"\n### Conclusão:\n\n")
        if sucessos == total_verificacoes:
            f.write("🎉 **VERIFICAÇÃO COMPLETA:** Todos os resultados reproduzem fielmente o relatório original!\n")
        elif sucessos >= total_verificacoes * 0.8:
            f.write("⚠️ **VERIFICAÇÃO PARCIAL:** A maioria dos resultados está correta, com pequenas divergências.\n")
        else:
            f.write("❌ **VERIFICAÇÃO FALHOU:** Muitas divergências encontradas em relação ao relatório original.\n")
    
    print(f"\n📄 Relatório salvo em: {relatorio_path}")
    print("\n" + "=" * 80)
    print("VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)

except Exception as e:
    print(f"❌ ERRO na verificação: {e}")
    import traceback
    traceback.print_exc() 