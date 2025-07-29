#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXECUTAR ANÁLISE COMPLETA - VERIFICAÇÃO DO RELATÓRIO UNIFICADO
==============================================================

Script principal que executa todos os módulos de análise na ordem correta
e gera um relatório de verificação para comparar com RELATORIO_UNIFICADO_COMPLETO_FINAL.md

Estrutura de Execução:
1. Preparação de dados
2. Análise descritiva 
3. Modelos SEM
4. Machine Learning
5. Visualizações
6. Consolidação e relatório final
"""

import os
import sys
import subprocess
import time
from datetime import datetime
import pandas as pd

# Configurar caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
CSV_DIR = os.path.join(BASE_DIR, '..', 'csv_extraidos')

# Criar diretórios de output se não existirem
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'dados_processados'), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'visualizacoes'), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'resultados_sem'), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'diagramas'), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'relatorios'), exist_ok=True)

def log_execucao(mensagem):
    """Log com timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {mensagem}")

def executar_script(caminho_script, descricao):
    """Executa um script Python e captura o resultado"""
    log_execucao(f"🔄 Iniciando: {descricao}")
    log_execucao(f"📄 Script: {caminho_script}")
    
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(caminho_script):
            log_execucao(f"❌ ERRO: Arquivo não encontrado: {caminho_script}")
            return False, f"Arquivo não encontrado: {caminho_script}"
        
        # Executar o script
        resultado = subprocess.run(
            [sys.executable, caminho_script],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos de timeout
        )
        
        if resultado.returncode == 0:
            log_execucao(f"✅ Concluído: {descricao}")
            return True, resultado.stdout
        else:
            log_execucao(f"❌ ERRO em {descricao}")
            log_execucao(f"Erro: {resultado.stderr}")
            return False, resultado.stderr
            
    except subprocess.TimeoutExpired:
        log_execucao(f"⏰ TIMEOUT: {descricao} (>5min)")
        return False, "Timeout na execução"
    except Exception as e:
        log_execucao(f"❌ EXCEÇÃO em {descricao}: {str(e)}")
        return False, str(e)

def verificar_dados_entrada():
    """Verifica se os dados de entrada estão disponíveis"""
    log_execucao("🔍 Verificando dados de entrada...")
    
    arquivos_necessarios = [
        'Qualidade do serviço.csv',
        'Utilização.csv', 
        'Percepção novos serviços.csv',
        'Intenção comportamental.csv',
        'Aceitação da tecnologia.csv',
        'Experiência do usuário.csv',
        'Perfil Socioeconomico.csv'
    ]
    
    arquivos_encontrados = 0
    for arquivo in arquivos_necessarios:
        caminho = os.path.join(CSV_DIR, arquivo)
        if os.path.exists(caminho):
            arquivos_encontrados += 1
            log_execucao(f"✅ Encontrado: {arquivo}")
        else:
            log_execucao(f"❌ Ausente: {arquivo}")
    
    if arquivos_encontrados == len(arquivos_necessarios):
        log_execucao(f"✅ Todos os {len(arquivos_necessarios)} arquivos de dados encontrados")
        return True
    else:
        log_execucao(f"❌ Apenas {arquivos_encontrados}/{len(arquivos_necessarios)} arquivos encontrados")
        return False

def executar_analise_completa():
    """Executa toda a análise na ordem correta"""
    
    log_execucao("=" * 80)
    log_execucao("🚀 INICIANDO ANÁLISE COMPLETA - VERIFICAÇÃO DO RELATÓRIO UNIFICADO")
    log_execucao("=" * 80)
    
    # Verificar dados de entrada
    if not verificar_dados_entrada():
        log_execucao("❌ FALHA: Dados de entrada incompletos")
        return False
    
    # Definir sequência de execução
    sequencia_execucao = [
        # FASE 1: PREPARAÇÃO
        {
            'script': '01_preparacao/dados_reais_final.py',
            'descricao': 'FASE 1 - Preparação e Validação dos Dados',
            'obrigatorio': True
        },
        
        # FASE 2: ANÁLISE DESCRITIVA
        {
            'script': '02_descritiva/analise_expandida_completa.py',
            'descricao': 'FASE 2A - Análise Expandida Completa (Perfil Socioeconômico)',
            'obrigatorio': True
        },
        {
            'script': '02_descritiva/analise_completa_corrigida.py',
            'descricao': 'FASE 2B - Análise Completa Corrigida (Base Principal)',
            'obrigatorio': True
        },
        
        # FASE 3: MODELOS SEM
        {
            'script': '03_sem_modelos/fix_sem_models.py',
            'descricao': 'FASE 3A - Modelos SEM Fixados (Análise Fatorial)',
            'obrigatorio': True
        },
        {
            'script': '03_sem_modelos/analise_sem_corrigida.py',
            'descricao': 'FASE 3B - SEM Corrigida (Percepção → Intenção)',
            'obrigatorio': True
        },
        
        # FASE 4: MACHINE LEARNING
        {
            'script': '04_machine_learning/analise_estatistica_avancada.py',
            'descricao': 'FASE 4A - Análise Estatística Avançada (Random Forest, Clustering)',
            'obrigatorio': False
        },
        {
            'script': '04_machine_learning/fix_wtp_analysis.py',
            'descricao': 'FASE 4B - Análise WTP (Disposição a Pagar)',
            'obrigatorio': False
        },
        
        # FASE 5: VISUALIZAÇÕES
        {
            'script': '05_visualizacoes/criar_diagrama_sem_storytelling.py',
            'descricao': 'FASE 5A - Diagrama SEM com Storytelling',
            'obrigatorio': False
        },
        {
            'script': '05_visualizacoes/criar_diagrama_sem_profissional.py',
            'descricao': 'FASE 5B - Diagrama SEM Profissional',
            'obrigatorio': False
        },
        {
            'script': '05_visualizacoes/criar_diagrama_sem_completo_simples.py',
            'descricao': 'FASE 5C - Diagrama SEM Executivo',
            'obrigatorio': False
        },
        {
            'script': '05_visualizacoes/criar_diagrama_sem_completo.py',
            'descricao': 'FASE 5D - Diagrama SEM Completo',
            'obrigatorio': False
        },
        
        # FASE 6: CONSOLIDAÇÃO
        {
            'script': '06_consolidacao/analise_final.py',
            'descricao': 'FASE 6 - Consolidação Final',
            'obrigatorio': False
        }
    ]
    
    # Executar sequência
    resultados = {}
    falhas_criticas = 0
    
    for i, etapa in enumerate(sequencia_execucao, 1):
        log_execucao(f"\n{'='*60}")
        log_execucao(f"ETAPA {i}/{len(sequencia_execucao)}: {etapa['descricao']}")
        log_execucao(f"{'='*60}")
        
        caminho_script = os.path.join(BASE_DIR, etapa['script'])
        sucesso, resultado = executar_script(caminho_script, etapa['descricao'])
        
        resultados[etapa['script']] = {
            'sucesso': sucesso,
            'resultado': resultado,
            'obrigatorio': etapa['obrigatorio']
        }
        
        if not sucesso and etapa['obrigatorio']:
            falhas_criticas += 1
            log_execucao(f"🚨 FALHA CRÍTICA na etapa obrigatória: {etapa['descricao']}")
        
        # Pequena pausa entre execuções
        time.sleep(2)
    
    # Relatório de execução
    log_execucao(f"\n{'='*80}")
    log_execucao("📊 RELATÓRIO DE EXECUÇÃO")
    log_execucao(f"{'='*80}")
    
    sucessos = sum(1 for r in resultados.values() if r['sucesso'])
    total = len(resultados)
    
    log_execucao(f"✅ Sucessos: {sucessos}/{total}")
    log_execucao(f"❌ Falhas: {total - sucessos}/{total}")
    log_execucao(f"🚨 Falhas Críticas: {falhas_criticas}")
    
    # Detalhar resultados
    for script, resultado in resultados.items():
        status = "✅ SUCESSO" if resultado['sucesso'] else "❌ FALHA"
        tipo = "OBRIGATÓRIO" if resultado['obrigatorio'] else "OPCIONAL"
        log_execucao(f"{status} [{tipo}] {script}")
    
    return falhas_criticas == 0

def gerar_relatorio_verificacao():
    """Gera relatório de verificação comparando com o relatório original"""
    log_execucao("\n📝 Gerando relatório de verificação...")
    
    relatorio_path = os.path.join(OUTPUT_DIR, 'relatorios', 'RELATORIO_VERIFICACAO_ANALISE.md')
    
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO DE VERIFICAÇÃO - ANÁLISE ESTRUTURADA\n\n")
        f.write(f"**Data de Execução:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        f.write("## 🎯 OBJETIVO\n\n")
        f.write("Este relatório verifica se a análise estruturada reproduz os resultados do ")
        f.write("RELATORIO_UNIFICADO_COMPLETO_FINAL.md.\n\n")
        
        f.write("## 📊 PRINCIPAIS DESCOBERTAS A VERIFICAR\n\n")
        f.write("### Descobertas do Relatório Original:\n")
        f.write("- **Correlação Percepção → Intenção:** r = 0.896\n")
        f.write("- **Variância Explicada:** 80.3% da intenção comportamental\n")
        f.write("- **Perfil Educacional:** 82.2% com ensino médio ou superior\n")
        f.write("- **Predominância Feminina:** 61.5% dos usuários\n")
        f.write("- **População Negra:** 59.2% dos usuários\n")
        f.write("- **Usuários de TP:** 70.3% como principal meio\n")
        f.write("- **Qualidade Média:** 1.64/5 (baixa)\n")
        f.write("- **Percepção Recompensas:** 4.51/5 (alta)\n")
        f.write("- **Intenção Comportamental:** 4.55/5 (alta)\n\n")
        
        f.write("## 🔍 VERIFICAÇÕES REALIZADAS\n\n")
        f.write("### Estrutura de Dados:\n")
        f.write("- [ ] 703 respondentes válidos\n")
        f.write("- [ ] 7 datasets principais carregados\n")
        f.write("- [ ] Codificação de escalas Likert correta\n\n")
        
        f.write("### Análises Estatísticas:\n")
        f.write("- [ ] Modelo SEM Percepção → Intenção\n")
        f.write("- [ ] Análise fatorial confirmatória\n")
        f.write("- [ ] Correlações entre construtos\n")
        f.write("- [ ] Segmentação sociodemográfica\n\n")
        
        f.write("### Visualizações:\n")
        f.write("- [ ] Diagramas SEM gerados\n")
        f.write("- [ ] Gráficos de distribuição\n")
        f.write("- [ ] Mapas de correlação\n\n")
        
        f.write("## 📈 RESULTADOS DA VERIFICAÇÃO\n\n")
        f.write("*Este relatório será atualizado após a execução completa da análise.*\n\n")
        
        f.write("## 📋 CHECKLIST DE CONFORMIDADE\n\n")
        f.write("- [ ] Dados carregados corretamente\n")
        f.write("- [ ] Análise descritiva executada\n")
        f.write("- [ ] Modelos SEM ajustados\n")
        f.write("- [ ] Visualizações geradas\n")
        f.write("- [ ] Resultados compatíveis com relatório original\n\n")
        
        f.write("---\n")
        f.write("*Relatório gerado automaticamente pela análise estruturada*\n")
    
    log_execucao(f"📄 Relatório de verificação salvo em: {relatorio_path}")

def main():
    """Função principal"""
    inicio = time.time()
    
    try:
        # Executar análise completa
        sucesso = executar_analise_completa()
        
        # Gerar relatório de verificação
        gerar_relatorio_verificacao()
        
        # Resultado final
        fim = time.time()
        duracao = fim - inicio
        
        log_execucao(f"\n{'='*80}")
        if sucesso:
            log_execucao("🎉 ANÁLISE COMPLETA EXECUTADA COM SUCESSO!")
        else:
            log_execucao("⚠️ ANÁLISE COMPLETA COM FALHAS CRÍTICAS")
        
        log_execucao(f"⏱️ Tempo total de execução: {duracao:.1f} segundos")
        log_execucao(f"📁 Resultados salvos em: {OUTPUT_DIR}")
        log_execucao(f"{'='*80}")
        
        return sucesso
        
    except KeyboardInterrupt:
        log_execucao("\n🛑 Execução interrompida pelo usuário")
        return False
    except Exception as e:
        log_execucao(f"\n💥 ERRO INESPERADO: {str(e)}")
        return False

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1) 