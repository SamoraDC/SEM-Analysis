#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERAR OUTPUTS SEM FALTANTES
===========================
Script para gerar tabela de índices e equações estruturais
"""

import pandas as pd
import numpy as np
from analise_sem_rigorosa import *

def main():
    print("GERANDO OUTPUTS SEM FALTANTES")
    print("="*40)
    
    # Executar análise SEM
    datasets = carregar_dados_completos()
    df_construtos, construtos = preparar_construtos_latentes(datasets)
    
    if df_construtos is None:
        print("Erro nos dados!")
        return
    
    resultados = modelo_sem_estrutural(df_construtos)
    
    print("\n=== TABELA DE ÍNDICES DE AJUSTE ===")
    
    # Gerar tabela de índices
    indices = resultados['indices_ajuste']
    
    tabela_indices = pd.DataFrame({
        'Índice': [
            'χ² (Chi-quadrado)',
            'gl (Graus de Liberdade)', 
            'p-valor',
            'CFI (Comparative Fit Index)',
            'TLI (Tucker-Lewis Index)',
            'RMSEA (Root Mean Square Error)',
            'SRMR (Standardized Root Mean Square)',
            'RMSE (Root Mean Square Error)',
            'R² (Coeficiente de Determinação)',
            'R² Ajustado'
        ],
        'Valor': [
            f"{indices['chi2']:.3f}",
            f"{indices['df']}",
            f"{indices['p_value']:.3f}",
            f"{indices['cfi']:.3f}",
            f"{indices['tli']:.3f}",
            f"{indices['rmsea']:.3f}",
            f"{indices['srmr']:.3f}",
            f"{indices['rmse']:.3f}",
            f"{indices['r2']:.3f}",
            f"{indices['r2_adj']:.3f}"
        ],
        'Critério': [
            'Menor melhor',
            '-',
            '> 0.05 (bom)',
            '> 0.95 (excelente)',
            '> 0.95 (excelente)',
            '< 0.08 (bom)',
            '< 0.08 (bom)',
            'Menor melhor',
            'Maior melhor',
            'Maior melhor'
        ],
        'Avaliação': [
            'Calculado',
            '-',
            '✓ Bom' if indices['p_value'] > 0.05 else '⚠ Atenção',
            '✓ Excelente' if indices['cfi'] > 0.95 else ('✓ Bom' if indices['cfi'] > 0.90 else '⚠ Melhorar'),
            '✓ Excelente' if indices['tli'] > 0.95 else ('✓ Bom' if indices['tli'] > 0.90 else '⚠ Melhorar'),
            '✓ Excelente' if indices['rmsea'] < 0.05 else ('✓ Bom' if indices['rmsea'] < 0.08 else '⚠ Melhorar'),
            '✓ Excelente' if indices['srmr'] < 0.05 else ('✓ Bom' if indices['srmr'] < 0.08 else '⚠ Melhorar'),
            'Calculado',
            '✓ Excelente' if indices['r2'] > 0.75 else ('✓ Bom' if indices['r2'] > 0.50 else '⚠ Melhorar'),
            '✓ Excelente' if indices['r2_adj'] > 0.75 else ('✓ Bom' if indices['r2_adj'] > 0.50 else '⚠ Melhorar')
        ]
    })
    
    print(tabela_indices.to_string(index=False))
    
    # Salvar tabela
    tabela_indices.to_csv('indices_ajuste_sem.csv', index=False, encoding='utf-8')
    print(f"\n✓ Tabela salva: indices_ajuste_sem.csv")
    
    print("\n=== EQUAÇÕES ESTRUTURAIS ===")
    
    # Gerar equações
    model1 = resultados['model1']
    model2 = resultados['model2']
    model_principal = resultados['model_principal']
    
    # Equação 1
    eq1 = f"""
EQUAÇÃO 1 - PERCEPÇÃO DE RECOMPENSAS:
Percepção_Recompensas = {model1.intercept_:.3f} + {model1.coef_[0]:.3f}×Qualidade + {model1.coef_[1]:.3f}×Tecnologia + {model1.coef_[2]:.3f}×Experiência + ε₁
R² = {resultados['r2_percepcao']:.3f}
"""
    
    # Equação 2
    eq2 = f"""
EQUAÇÃO 2 - INTENÇÃO COMPORTAMENTAL (MODELO COMPLETO):
Intenção = {model2.intercept_:.3f} + {model2.coef_[0]:.3f}×Qualidade + {model2.coef_[1]:.3f}×Tecnologia + {model2.coef_[2]:.3f}×Experiência + {model2.coef_[3]:.3f}×Percepção + ε₂
R² = {resultados['r2_intencao']:.3f}
"""
    
    # Equação principal
    eq3 = f"""
EQUAÇÃO PRINCIPAL (MODELO PARCIMONIOSO):
Intenção = {model_principal.intercept_:.3f} + {model_principal.coef_[0]:.3f}×Percepção_Recompensas + ε₃
R² = {resultados['r2_principal']:.3f}
Correlação = {np.sqrt(resultados['r2_principal']):.3f}
"""
    
    print(eq1)
    print(eq2)
    print(eq3)
    
    # Salvar equações
    with open('equacoes_estruturais_sem.txt', 'w', encoding='utf-8') as f:
        f.write("EQUAÇÕES ESTRUTURAIS - MODELO SEM RIGOROSO\n")
        f.write("="*50 + "\n")
        f.write(eq1)
        f.write(eq2)
        f.write(eq3)
        f.write("\nCOEFICIENTES E INTERPRETAÇÃO:\n")
        f.write("-"*30 + "\n")
        f.write(f"• Coeficiente mais forte: Percepção → Intenção ({model2.coef_[3]:.3f})\n")
        f.write(f"• Impacto da Qualidade atual: {model2.coef_[0]:.3f} (limitado)\n")
        f.write(f"• Papel da Tecnologia: {model2.coef_[1]:.3f} (facilitador)\n")
        f.write(f"• Variância explicada: {resultados['r2_intencao']*100:.1f}%\n")
        f.write(f"• Amostra: N = {resultados['n_obs']}\n")
        
        # Interpretação dos índices
        f.write(f"\nÍNDICES DE AJUSTE:\n")
        f.write(f"• CFI = {indices['cfi']:.3f} (Comparative Fit Index)\n")
        f.write(f"• TLI = {indices['tli']:.3f} (Tucker-Lewis Index)\n")
        f.write(f"• RMSEA = {indices['rmsea']:.3f} (Root Mean Square Error)\n")
        f.write(f"• SRMR = {indices['srmr']:.3f} (Standardized Root Mean Square)\n")
    
    print(f"✓ Equações salvas: equacoes_estruturais_sem.txt")
    
    # Resumo final
    print("\n" + "="*50)
    print("RESUMO FINAL DA ANÁLISE SEM")
    print("="*50)
    print(f"✓ Amostra final: N = {resultados['n_obs']}")
    print(f"✓ Variáveis latentes: {len(construtos)}")
    print(f"✓ R² Principal: {resultados['r2_principal']:.3f}")
    print(f"✓ Correlação: {np.sqrt(resultados['r2_principal']):.3f}")
    print(f"✓ Arquivos gerados:")
    print(f"  - diagrama_sem_rigoroso.png")
    print(f"  - indices_ajuste_sem.csv")
    print(f"  - equacoes_estruturais_sem.txt")
    
    return True

if __name__ == "__main__":
    main() 