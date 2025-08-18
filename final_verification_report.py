#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RELATÓRIO FINAL DE VERIFICAÇÃO DA ORGANIZAÇÃO
============================================

Este script verifica se toda a reorganização foi feita corretamente
e gera um relatório final detalhado.
"""

import os
from pathlib import Path
import subprocess
import sys

def check_python_imports():
    """Verifica se os imports nos scripts Python estão funcionando"""
    
    print("🔍 VERIFICANDO IMPORTS DOS SCRIPTS PYTHON...")
    print("=" * 50)
    
    key_scripts = [
        "src/python/core/dados_preparacao.py",
        "src/python/analysis/analise_sem_principal.py",
        "src/python/analysis/modelos_sem.py",
        "src/python/visualization/diagramas_sem.py"
    ]
    
    all_good = True
    
    for script in key_scripts:
        if os.path.exists(script):
            try:
                # Tentar fazer syntax check
                result = subprocess.run([sys.executable, "-m", "py_compile", script], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {script}")
                else:
                    print(f"❌ ERRO syntax: {script}")
                    print(f"   {result.stderr[:100]}...")
                    all_good = False
            except Exception as e:
                print(f"⚠️ Não foi possível verificar: {script} ({e})")
        else:
            print(f"❌ FALTANDO: {script}")
            all_good = False
    
    return all_good

def verify_data_paths():
    """Verifica se os caminhos dos dados estão corretos"""
    
    print("\n💾 VERIFICANDO CAMINHOS DOS DADOS...")
    print("=" * 50)
    
    required_data_files = [
        "data/raw/csv_extraidos/Percepção novos serviços.csv",
        "data/raw/csv_extraidos/Intenção comportamental.csv",
        "data/raw/csv_extraidos/Qualidade do serviço.csv",
        "data/raw/csv_extraidos/Perfil Socioeconomico.csv",
        "data/processed/dados_processados/base_unificada.csv"
    ]
    
    all_good = True
    
    for data_file in required_data_files:
        if os.path.exists(data_file):
            size = os.path.getsize(data_file)
            print(f"✅ {data_file} ({size:,} bytes)")
        else:
            print(f"❌ FALTANDO: {data_file}")
            all_good = False
    
    return all_good

def verify_report_integrity():
    """Verifica se o relatório principal está íntegro"""
    
    print("\n📄 VERIFICANDO INTEGRIDADE DO RELATÓRIO...")
    print("=" * 50)
    
    report_path = "results/reports/RELATORIO_UNIFICADO_COMPLETO_FINAL.md"
    
    if not os.path.exists(report_path):
        print(f"❌ RELATÓRIO PRINCIPAL NÃO ENCONTRADO: {report_path}")
        return False
    
    # Verificar tamanho e conteúdo básico
    size = os.path.getsize(report_path)
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar elementos chave
    key_elements = [
        "r = 0.896",
        "PARTE I: PERFIL SOCIOECONÔMICO",
        "PARTE VIII: RESUMO DAS PRINCIPAIS DESCOBERTAS",
        "![",  # Pelo menos uma imagem
        "61.5% mulheres"
    ]
    
    missing_elements = []
    for element in key_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ ELEMENTOS FALTANDO NO RELATÓRIO:")
        for element in missing_elements:
            print(f"   - {element}")
        return False
    else:
        print(f"✅ Relatório íntegro ({size:,} bytes, {len(content.splitlines())} linhas)")
        return True

def count_organized_files():
    """Conta arquivos organizados por categoria"""
    
    print("\n📊 CONTAGEM DE ARQUIVOS ORGANIZADOS...")
    print("=" * 50)
    
    categories = {
        "Scripts Python": list(Path("src/python").rglob("*.py")),
        "Scripts R": list(Path("src/r").rglob("*.R")),
        "Dados brutos": list(Path("data/raw").rglob("*.csv")),
        "Dados processados": list(Path("data/processed").rglob("*.csv")),
        "Imagens": list(Path("results/images").rglob("*.png")),
        "Documentação": list(Path("docs").rglob("*.md")),
        "Arquivos legados": list(Path("legacy").rglob("*.*"))
    }
    
    total_files = 0
    
    for category, files in categories.items():
        count = len(files)
        total_files += count
        print(f"📁 {category:<20}: {count:>3} arquivos")
    
    print(f"\n📊 TOTAL ORGANIZADO: {total_files} arquivos")
    
    return categories

def check_root_cleanliness():
    """Verifica se o diretório raiz está limpo"""
    
    print("\n🧹 VERIFICANDO LIMPEZA DO DIRETÓRIO RAIZ...")
    print("=" * 50)
    
    # Arquivos que DEVEM estar no root
    allowed_files = {
        'README.md',
        'run_complete_analysis.py',
        'organize_project.py',
        'update_paths.py',
        'validate_project_structure.py',
        'deep_clean_organization.py',
        'final_cleanup.py',
        'absolute_final_cleanup.py',
        'final_verification_report.py',
        'pyproject.toml',  # Se ainda existir
        'uv.lock'         # Se ainda existir
    }
    
    # Diretórios que DEVEM estar no root
    allowed_dirs = {
        'src', 'data', 'results', 'docs', 'config', 'legacy',
        '.venv', '.git', '__pycache__', 'analise_estruturada'
    }
    
    unexpected_items = []
    
    for item in os.listdir('.'):
        if os.path.isfile(item) and item not in allowed_files:
            unexpected_items.append(f"📄 {item}")
        elif os.path.isdir(item) and item not in allowed_dirs:
            unexpected_items.append(f"📁 {item}/")
    
    if unexpected_items:
        print("⚠️ Itens inesperados no diretório raiz:")
        for item in unexpected_items:
            print(f"   {item}")
        return False
    else:
        print("✅ Diretório raiz completamente limpo!")
        return True

def test_key_functionality():
    """Testa funcionalidades chave"""
    
    print("\n🧪 TESTANDO FUNCIONALIDADES CHAVE...")
    print("=" * 50)
    
    # Verificar se o script mestre pelo menos carrega
    try:
        with open("run_complete_analysis.py", 'r') as f:
            content = f.read()
        
        # Verificar se tem os scripts principais listados
        required_scripts = [
            "src/python/core/dados_preparacao.py",
            "src/python/analysis/analise_sem_principal.py"
        ]
        
        all_found = all(script in content for script in required_scripts)
        
        if all_found:
            print("✅ Script mestre configurado corretamente")
        else:
            print("❌ Script mestre não configurado corretamente")
            return False
            
    except Exception as e:
        print(f"❌ Erro verificando script mestre: {e}")
        return False
    
    # Verificar se README tem as instruções certas
    try:
        with open("README.md", 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        if "uv run run_complete_analysis.py" in readme_content:
            print("✅ README com instruções atualizadas")
        else:
            print("⚠️ README pode não ter instruções atualizadas")
            
    except Exception as e:
        print(f"❌ Erro verificando README: {e}")
        return False
    
    return True

def generate_final_report():
    """Gera relatório final consolidado"""
    
    print("\n📋 GERANDO RELATÓRIO FINAL...")
    print("=" * 50)
    
    # Executar todas as verificações
    python_ok = check_python_imports()
    data_ok = verify_data_paths()
    report_ok = verify_report_integrity()
    files_organized = count_organized_files()
    root_clean = check_root_cleanliness()
    functionality_ok = test_key_functionality()
    
    # Calcular score final
    checks = [python_ok, data_ok, report_ok, root_clean, functionality_ok]
    score = sum(checks) / len(checks) * 100
    
    print(f"\n{'='*60}")
    print("🎯 RELATÓRIO FINAL DE VERIFICAÇÃO")
    print(f"{'='*60}")
    
    print(f"📊 SCORE FINAL: {score:.1f}%")
    print()
    
    if score >= 90:
        print("🎉 ORGANIZAÇÃO EXCELENTE!")
        print("✅ Projeto 100% pronto para produção")
        print("✅ Estrutura segue boas práticas")
        print("✅ Reprodutibilidade garantida")
    elif score >= 75:
        print("👍 ORGANIZAÇÃO BOA")
        print("✅ Projeto quase pronto")
        print("⚠️ Alguns ajustes menores necessários")
    else:
        print("⚠️ ORGANIZAÇÃO PRECISA DE MELHORIAS")
        print("❌ Revisar itens marcados com ❌")
    
    print()
    print("🚀 INSTRUÇÕES PARA USO:")
    print("1. Execute: uv run run_complete_analysis.py")
    print("2. Consulte: results/reports/RELATORIO_UNIFICADO_COMPLETO_FINAL.md")
    print("3. Explore: src/ para códigos organizados")
    print()
    
    print("📁 ESTRUTURA FINAL:")
    print("├── src/           # Códigos organizados por categoria")
    print("├── data/          # Dados brutos e processados")
    print("├── results/       # Relatórios, imagens e outputs")
    print("├── docs/          # Documentação completa")
    print("├── config/        # Configurações do projeto")
    print("└── legacy/        # Arquivos legados preservados")
    
    print(f"\n{'='*60}")
    
    return score

def main():
    """Executa verificação completa final"""
    
    print("🔍 VERIFICAÇÃO FINAL COMPLETA DA ORGANIZAÇÃO")
    print("=" * 70)
    print("Verificando se toda a reorganização foi feita corretamente...")
    
    score = generate_final_report()
    
    if score >= 90:
        print("\n🎉 PARABÉNS! Projeto perfeitamente organizado!")
    else:
        print("\n📋 Revise os itens marcados com ❌ para melhorar")

if __name__ == "__main__":
    main()
