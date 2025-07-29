#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VALIDAÇÃO DOS SCRIPTS R SEM CORRIGIDOS
=====================================

Script para validar se os scripts R corrigidos são fidedignos
aos seus equivalentes em Python em termos de:
- Estrutura de funções
- Lógica de processamento
- Outputs gerados
- Cálculos estatísticos
"""

import re
import os

def extrair_funcoes_python(arquivo_python):
    """Extrai todas as funções de um arquivo Python"""
    print(f"\n=== ANALISANDO {arquivo_python} ===")
    
    if not os.path.exists(arquivo_python):
        print(f"❌ Arquivo não encontrado: {arquivo_python}")
        return {}
    
    with open(arquivo_python, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Extrair definições de funções
    funcoes = {}
    padrao_funcao = r'def\s+(\w+)\s*\([^)]*\):'
    matches = re.findall(padrao_funcao, conteudo)
    
    for nome_funcao in matches:
        # Extrair o corpo da função
        inicio = conteudo.find(f'def {nome_funcao}(')
        if inicio != -1:
            # Encontrar o fim da função (próxima função ou fim do arquivo)
            proximo_def = conteudo.find('\ndef ', inicio + 1)
            if proximo_def != -1:
                corpo = conteudo[inicio:proximo_def]
            else:
                corpo = conteudo[inicio:]
            
            funcoes[nome_funcao] = {
                'linhas': len(corpo.split('\n')),
                'tem_prints': 'print(' in corpo,
                'tem_matplotlib': 'plt.' in corpo or 'matplotlib' in corpo,
                'tem_pandas': 'pd.' in corpo or 'DataFrame' in corpo,
                'tem_numpy': 'np.' in corpo or 'numpy' in corpo,
                'tem_sklearn': 'sklearn' in corpo or 'LinearRegression' in corpo,
                'tem_calculos_indices': 'chi2' in corpo or 'cfi' in corpo or 'rmsea' in corpo,
                'tem_correlacao': 'corr' in corpo or 'correlation' in corpo,
                'tem_regressao': 'LinearRegression' in corpo or 'lm(' in corpo,
                'tem_equacoes': 'equacao' in corpo.lower() or 'formula' in corpo,
                'tem_diagrama': 'diagrama' in corpo.lower() or 'plot' in corpo
            }
    
    print(f"✓ Funções encontradas: {len(funcoes)}")
    for nome, info in funcoes.items():
        print(f"  - {nome}: {info['linhas']} linhas")
    
    return funcoes

def extrair_funcoes_r(arquivo_r):
    """Extrai todas as funções de um arquivo R"""
    print(f"\n=== ANALISANDO {arquivo_r} ===")
    
    if not os.path.exists(arquivo_r):
        print(f"❌ Arquivo não encontrado: {arquivo_r}")
        return {}
    
    with open(arquivo_r, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Extrair definições de funções em R
    funcoes = {}
    padrao_funcao = r'(\w+)\s*<-\s*function\s*\([^)]*\)'
    matches = re.findall(padrao_funcao, conteudo)
    
    for nome_funcao in matches:
        # Extrair o corpo da função
        inicio = conteudo.find(f'{nome_funcao} <- function(')
        if inicio != -1:
            # Encontrar o fim da função (próxima função ou fim do arquivo)
            proximo_def = conteudo.find(' <- function(', inicio + 1)
            if proximo_def != -1:
                corpo = conteudo[inicio:proximo_def]
            else:
                corpo = conteudo[inicio:]
            
            funcoes[nome_funcao] = {
                'linhas': len(corpo.split('\n')),
                'tem_prints': 'cat(' in corpo or 'print(' in corpo,
                'tem_graficos': 'png(' in corpo or 'plot(' in corpo or 'ggplot' in corpo,
                'tem_dataframes': 'data.frame' in corpo or 'read.csv' in corpo,
                'tem_calculos_indices': 'chi2' in corpo or 'cfi' in corpo or 'rmsea' in corpo,
                'tem_correlacao': 'cor(' in corpo,
                'tem_regressao': 'lm(' in corpo,
                'tem_equacoes': 'equacao' in corpo.lower() or 'formula' in corpo,
                'tem_diagrama': 'diagrama' in corpo.lower() or 'plot' in corpo,
                'tem_conversao_likert': 'converter_likert' in corpo,
                'tem_construtos': 'construto' in corpo.lower(),
                'tem_sem': 'sem' in corpo.lower() or 'structural' in corpo.lower()
            }
    
    print(f"✓ Funções encontradas: {len(funcoes)}")
    for nome, info in funcoes.items():
        print(f"  - {nome}: {info['linhas']} linhas")
    
    return funcoes

def comparar_funcionalidades(funcoes_python, funcoes_r, nome_script):
    """Compara as funcionalidades entre scripts Python e R"""
    print(f"\n=== COMPARAÇÃO DE FUNCIONALIDADES - {nome_script} ===")
    
    # Mapear funções similares
    mapeamento_funcoes = {
        'analise_sem_rigorosa': {
            'carregar_dados_completos': 'carregar_dados_completos',
            'preparar_construtos_latentes': 'preparar_construtos_latentes', 
            'modelo_sem_estrutural': 'modelo_sem_estrutural',
            'calcular_indices_ajuste': 'calcular_indices_ajuste',
            'criar_diagrama_caminho': 'criar_diagrama_caminho',
            'gerar_tabela_indices_ajuste': 'gerar_tabela_indices_ajuste',
            'gerar_equacoes_estruturais': 'gerar_equacoes_estruturais',
            'executar_analise_sem_completa': 'executar_analise_sem_completa'
        },
        'analise_sem_completa_todas_variaveis': {
            'carregar_todos_dados': 'carregar_todos_dados',
            'converter_likert_avancado': 'converter_likert_avancado',
            'preparar_construtos_completos': 'preparar_construtos_completos',
            'criar_diagrama_individual': 'criar_diagrama_individual',
            'criar_diagrama_gigante_completo': 'criar_diagrama_gigante_completo',
            'executar_analise_completa': 'executar_analise_completa'
        }
    }
    
    funcoes_mapeadas = mapeamento_funcoes.get(nome_script, {})
    
    score_total = 0
    max_score = 0
    
    print("FUNCÕES PRINCIPAIS:")
    for func_py, func_r in funcoes_mapeadas.items():
        max_score += 1
        
        if func_py in funcoes_python and func_r in funcoes_r:
            print(f"✓ {func_py} ↔ {func_r}: PRESENTES")
            score_total += 1
            
            # Comparar características específicas
            py_info = funcoes_python[func_py]
            r_info = funcoes_r[func_r]
            
            caracteristicas = []
            if py_info.get('tem_prints') and r_info.get('tem_prints'):
                caracteristicas.append("prints")
            if py_info.get('tem_correlacao') and r_info.get('tem_correlacao'):
                caracteristicas.append("correlação")
            if py_info.get('tem_regressao') and r_info.get('tem_regressao'):
                caracteristicas.append("regressão")
            if py_info.get('tem_calculos_indices') and r_info.get('tem_calculos_indices'):
                caracteristicas.append("índices")
            if py_info.get('tem_diagrama') and r_info.get('tem_diagrama'):
                caracteristicas.append("diagrama")
            
            if caracteristicas:
                print(f"    Funcionalidades comuns: {', '.join(caracteristicas)}")
                
        elif func_py in funcoes_python:
            print(f"⚠ {func_py}: Apenas em Python")
        elif func_r in funcoes_r:
            print(f"⚠ {func_r}: Apenas em R")
        else:
            print(f"❌ {func_py} ↔ {func_r}: AUSENTES")
    
    # Funções adicionais em R
    funcoes_r_extras = set(funcoes_r.keys()) - set(funcoes_mapeadas.values())
    if funcoes_r_extras:
        print(f"\nFUNCÕES EXTRAS EM R: {', '.join(funcoes_r_extras)}")
    
    # Funções adicionais em Python
    funcoes_py_extras = set(funcoes_python.keys()) - set(funcoes_mapeadas.keys())
    if funcoes_py_extras:
        print(f"FUNÇÕES EXTRAS EM PYTHON: {', '.join(funcoes_py_extras)}")
    
    # Calcular score de equivalência
    if max_score > 0:
        percentual = (score_total / max_score) * 100
        print(f"\n📊 SCORE DE EQUIVALÊNCIA: {score_total}/{max_score} ({percentual:.1f}%)")
        
        if percentual >= 95:
            status = "🎯 EXCELENTE"
        elif percentual >= 85:
            status = "✅ BOM"
        elif percentual >= 70:
            status = "⚠️ REGULAR"
        else:
            status = "❌ INSUFICIENTE"
            
        print(f"STATUS: {status}")
    
    return score_total, max_score

def analisar_estrutura_dados(arquivo_python, arquivo_r):
    """Analisa a estrutura de dados processados"""
    print(f"\n=== ANÁLISE DE ESTRUTURA DE DADOS ===")
    
    # Ler conteúdo dos arquivos
    with open(arquivo_python, 'r', encoding='utf-8') as f:
        conteudo_py = f.read()
    
    with open(arquivo_r, 'r', encoding='utf-8') as f:
        conteudo_r = f.read()
    
    # Verificar processamento de construtos
    construtos_py = re.findall(r"construtos\['(\w+)'\]", conteudo_py)
    construtos_r = re.findall(r"construtos_completos\$(\w+)", conteudo_r)
    
    print(f"CONSTRUTOS IDENTIFICADOS:")
    print(f"  Python: {set(construtos_py) if construtos_py else 'Nenhum'}")
    print(f"  R: {set(construtos_r) if construtos_r else 'Nenhum'}")
    
    # Verificar datasets
    datasets_py = re.findall(r"datasets\['([^']+)'\]", conteudo_py)
    datasets_r = re.findall(r"datasets\$([A-Za-z_]+)", conteudo_r)
    
    print(f"DATASETS PROCESSADOS:")
    print(f"  Python: {set(datasets_py) if datasets_py else 'Nenhum'}")
    print(f"  R: {set(datasets_r) if datasets_r else 'Nenhum'}")
    
    # Verificar cálculos estatísticos
    calculos_py = []
    calculos_r = []
    
    if 'r2_score' in conteudo_py: calculos_py.append('R²')
    if 'LinearRegression' in conteudo_py: calculos_py.append('Regressão Linear')
    if 'correlation' in conteudo_py or '.corr()' in conteudo_py: calculos_py.append('Correlação')
    
    if 'summary(' in conteudo_r and 'r.squared' in conteudo_r: calculos_r.append('R²')
    if 'lm(' in conteudo_r: calculos_r.append('Regressão Linear')
    if 'cor(' in conteudo_r: calculos_r.append('Correlação')
    
    print(f"CÁLCULOS ESTATÍSTICOS:")
    print(f"  Python: {calculos_py if calculos_py else 'Nenhum'}")
    print(f"  R: {calculos_r if calculos_r else 'Nenhum'}")

def validar_outputs_gerados(arquivo_python, arquivo_r):
    """Valida se os outputs gerados são equivalentes"""
    print(f"\n=== VALIDAÇÃO DE OUTPUTS ===")
    
    with open(arquivo_python, 'r', encoding='utf-8') as f:
        conteudo_py = f.read()
    
    with open(arquivo_r, 'r', encoding='utf-8') as f:
        conteudo_r = f.read()
    
    # Arquivos salvos
    arquivos_py = re.findall(r"savefig\('([^']+)'\)", conteudo_py)
    arquivos_py += re.findall(r"to_csv\('([^']+)'\)", conteudo_py)
    arquivos_py += re.findall(r'open\(\'([^\']+)\', \'w\'', conteudo_py)
    
    arquivos_r = re.findall(r'png\("([^"]+)"\)', conteudo_r)
    arquivos_r += re.findall(r'write\.csv\([^,]+,\s*"([^"]+)"', conteudo_r)
    arquivos_r += re.findall(r'writeLines\([^,]+,\s*"([^"]+)"', conteudo_r)
    
    print(f"ARQUIVOS GERADOS:")
    print(f"  Python: {arquivos_py if arquivos_py else 'Nenhum'}")
    print(f"  R: {arquivos_r if arquivos_r else 'Nenhum'}")
    
    # Verificar correspondência de arquivos
    arquivos_comuns = set(os.path.basename(f) for f in arquivos_py) & set(os.path.basename(f) for f in arquivos_r)
    print(f"  Arquivos em comum: {arquivos_comuns if arquivos_comuns else 'Nenhum'}")
    
    # Tipos de visualização
    viz_py = []
    viz_r = []
    
    if 'plt.show()' in conteudo_py or 'plt.savefig' in conteudo_py: viz_py.append('Matplotlib')
    if 'diagrama' in conteudo_py.lower(): viz_py.append('Diagrama SEM')
    
    if 'plot(' in conteudo_r or 'png(' in conteudo_r: viz_r.append('R Graphics')
    if 'diagrama' in conteudo_r.lower(): viz_r.append('Diagrama SEM')
    
    print(f"TIPOS DE VISUALIZAÇÃO:")
    print(f"  Python: {viz_py if viz_py else 'Nenhum'}")
    print(f"  R: {viz_r if viz_r else 'Nenhum'}")

def main():
    """Função principal de validação"""
    print("🔍 VALIDAÇÃO DOS SCRIPTS R SEM CORRIGIDOS")
    print("=" * 60)
    
    # Scripts a serem validados
    scripts = [
        {
            'nome': 'analise_sem_rigorosa',
            'python': 'analise_sem_rigorosa.py',
            'r': 'analise_sem_rigorosa.R'
        },
        {
            'nome': 'analise_sem_completa_todas_variaveis', 
            'python': 'analise_sem_completa_todas_variaveis.py',
            'r': 'analise_sem_completa_todas_variaveis.R'
        }
    ]
    
    resultados_gerais = {
        'total_scripts': len(scripts),
        'scripts_validados': 0,
        'score_medio': 0
    }
    
    for script in scripts:
        print(f"\n{'='*80}")
        print(f"VALIDANDO: {script['nome'].upper()}")
        print(f"{'='*80}")
        
        # Extrair funções
        funcoes_py = extrair_funcoes_python(script['python'])
        funcoes_r = extrair_funcoes_r(script['r'])
        
        if funcoes_py and funcoes_r:
            # Comparar funcionalidades
            score, max_score = comparar_funcionalidades(funcoes_py, funcoes_r, script['nome'])
            
            # Analisar estrutura de dados
            analisar_estrutura_dados(script['python'], script['r'])
            
            # Validar outputs
            validar_outputs_gerados(script['python'], script['r'])
            
            # Atualizar resultados gerais
            if max_score > 0:
                percentual = (score / max_score) * 100
                resultados_gerais['score_medio'] += percentual
                resultados_gerais['scripts_validados'] += 1
        
        else:
            print("❌ ERRO: Não foi possível extrair funções de um ou ambos os arquivos")
    
    # Resumo final
    print(f"\n{'='*80}")
    print("RESUMO FINAL DA VALIDAÇÃO")
    print(f"{'='*80}")
    
    if resultados_gerais['scripts_validados'] > 0:
        score_final = resultados_gerais['score_medio'] / resultados_gerais['scripts_validados']
        print(f"📊 Score médio de equivalência: {score_final:.1f}%")
        
        if score_final >= 90:
            status_final = "🎯 EXCELENTE - Scripts R são muito fidedignos aos Python"
        elif score_final >= 80:
            status_final = "✅ BOM - Scripts R são bem equivalentes aos Python"
        elif score_final >= 70:
            status_final = "⚠️ REGULAR - Scripts R precisam de melhorias"
        else:
            status_final = "❌ INSUFICIENTE - Scripts R precisam de reescrita significativa"
        
        print(f"🎯 Status final: {status_final}")
        
        print(f"\n📋 SCRIPTS ANALISADOS:")
        for script in scripts:
            if os.path.exists(script['python']) and os.path.exists(script['r']):
                print(f"  ✓ {script['nome']}: Python ↔ R")
            else:
                print(f"  ❌ {script['nome']}: Arquivos faltando")
    
    print(f"\n🔍 Validação concluída!")

if __name__ == "__main__":
    main() 