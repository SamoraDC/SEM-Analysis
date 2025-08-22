#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT MESTRE - REPRODUÇÃO COMPLETA DO RELATÓRIO
===============================================

Este script executa toda a sequência de análises necessárias
para reproduzir o RELATORIO_UNIFICADO_COMPLETO_FINAL.md
"""

import subprocess
import sys
import os
from pathlib import Path

def run_script(script_path, description):
    """Executa um script e reporta o resultado"""
    print(f"\n{'='*60}")
    print(f"🚀 EXECUTANDO: {description}")
    print(f"📄 Script: {script_path}")
    print('='*60)
    
    # Verificar se o arquivo existe
    if not os.path.exists(script_path):
        print(f"❌ ARQUIVO NÃO ENCONTRADO: {script_path}")
        return False
    
    try:
        # Configurar ambiente para UTF-8
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['LC_ALL'] = 'pt_BR.UTF-8'
        
        if script_path.endswith('.py'):
            # Usar uv run para scripts Python (executar do diretório raiz)
            result = subprocess.run(['uv', 'run', script_path], 
                                  capture_output=True, text=True, cwd='.', env=env)
        elif script_path.endswith('.R'):
            # Usar Rscript para scripts R (executar do diretório raiz)
            result = subprocess.run(['Rscript', script_path], 
                                  capture_output=True, text=True, cwd='.', env=env)
        else:
            print(f"❌ Tipo de arquivo não suportado: {script_path}")
            return False
            
        if result.returncode == 0:
            print(f"✅ SUCESSO: {description}")
            if result.stdout:
                print("📤 Output:")
                print(result.stdout)
        else:
            print(f"❌ ERRO: {description}")
            if result.stderr:
                print("📤 Stderr:")
                print(result.stderr)
            if result.stdout:
                print("📤 Stdout:")
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ EXCEÇÃO: {e}")
        return False
    
    return True

def main():
    """Executa toda a sequência de análises"""
    
    print("🎯 REPRODUÇÃO COMPLETA DO RELATÓRIO UNIFICADO")
    print("=" * 70)
    
    # Sequência de execução Python
    python_sequence = [
        ("src/python/core/dados_preparacao.py", "1. Preparação dos Dados"),
        ("src/python/analysis/analise_demografica.py", "2. Análise Demográfica"),
        ("src/python/analysis/analise_descritiva.py", "3. Análise Descritiva"),
        ("src/python/analysis/modelos_sem.py", "4. Modelos SEM"),
        ("src/python/analysis/analise_sem_principal.py", "5. Análise SEM Principal"),
        ("src/python/analysis/machine_learning.py", "6. Machine Learning & Clustering"),
        ("src/python/analysis/analise_wtp.py", "7. Análise WTP"),
        ("src/python/visualization/diagramas_sem.py", "8. Diagramas SEM"),
        ("src/python/visualization/diagramas_simples.py", "9. Diagramas Simples"),
        ("src/python/visualization/diagramas_profissionais.py", "10. Diagramas Profissionais"),
        ("src/python/core/analise_final.py", "11. Consolidação Final")
    ]
    
    print("\n🐍 EXECUTANDO SEQUÊNCIA PYTHON...")
    for script_path, description in python_sequence:
        if os.path.exists(script_path):
            if not run_script(script_path, description):
                print(f"⚠️  Falha em {script_path}, continuando...")
        else:
            print(f"⚠️  Script não encontrado: {script_path}")
    
    # Sequência de execução R
    r_sequence = [
        ("src/r/core/dados_preparacao.R", "1. Preparação dos Dados (R)"),
        ("src/r/analysis/analise_descritiva.R", "2. Análise Descritiva (R)"),
        ("src/r/analysis/analise_sem_principal.R", "3. Análise SEM Principal (R)"),
        ("src/r/analysis/modelos_sem_rigorosos.R", "4. Modelos SEM Rigorosos (R)"),
        ("src/r/analysis/analise_completa.R", "5. Análise Completa (R)")
    ]
    
    print("\n📊 EXECUTANDO SEQUÊNCIA R...")
    for script_path, description in r_sequence:
        if os.path.exists(script_path):
            if not run_script(script_path, description):
                print(f"⚠️  Falha em {script_path}, continuando...")
        else:
            print(f"⚠️  Script não encontrado: {script_path}")
    
    print("\n" + "="*70)
    print("🎉 REPRODUÇÃO COMPLETA FINALIZADA!")
    print("📄 Relatório disponível em: results/reports/RELATORIO_UNIFICADO_COMPLETO_FINAL.md")
    print("🖼️  Imagens disponíveis em: results/images/")
    print("📊 Outputs disponíveis em: results/outputs/")
    print("="*70)

if __name__ == "__main__":
    main()
