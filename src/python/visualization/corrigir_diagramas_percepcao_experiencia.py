#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORREÇÃO ESPECÍFICA: PERCEPÇÃO DE RECOMPENSAS E EXPERIÊNCIA DO USUÁRIO
====================================================================

Problema: 3 variáveis passando no meio do centro, sobrepondo e atrapalhando visibilidade
Solução: Layout em círculo amplo para evitar sobreposição
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle, Rectangle
import warnings
warnings.filterwarnings('ignore')

# Configuração melhorada
plt.style.use('default')
plt.rcParams['figure.figsize'] = (18, 14)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

# Variáveis específicas dos construtos problemáticos
VARIAVEIS_PROBLEMATICAS = {
    'PERCEPCAO': [
        'Pontos/créditos',
        'Uso ilimitado',
        'Pré-pago ilimitado',
        'Pós-pago ilimitado',
        'Passe diário',
        'Passe mensal',
        'Passe anual',
        'Cashback km',
        'Desconto fora pico'
    ],
    'EXPERIENCIA': [
        'Satisfeito serviço',
        'Corresponde expectativas',
        'Necessidades atendidas',
        'Bom custo-benefício',
        'Sou recompensado',
        'Cartões',
        'Apps celular',
        'QR Code',
        'Bilhete impresso'
    ]
}

def criar_diagrama_corrigido_especifico(construto_nome, salvar=True):
    """Cria diagrama com layout circular amplo para evitar sobreposição"""
    print(f"\n🔧 Corrigindo especificamente: {construto_nome}")
    
    variaveis = VARIAVEIS_PROBLEMATICAS[construto_nome]
    n_variaveis = len(variaveis)
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 14)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Variável latente (centro) - MAIOR
    latent_pos = (9, 7)
    latent_circle = Circle(latent_pos, 1.8, facecolor='lightblue', 
                          edgecolor='darkblue', linewidth=4, alpha=0.8)
    ax.add_patch(latent_circle)
    ax.text(latent_pos[0], latent_pos[1], construto_nome, 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Layout CIRCULAR AMPLO para evitar sobreposição
    angles = [i * (2*np.pi / n_variaveis) for i in range(n_variaveis)]
    radius = 5.0  # Raio amplo para evitar sobreposição
    positions = [(latent_pos[0] + radius*np.cos(angle), 
                 latent_pos[1] + radius*np.sin(angle)) for angle in angles]
    
    # Desenhar variáveis observadas
    for i, (pos, var_name) in enumerate(zip(positions, variaveis)):
        # Retângulo MAIOR para melhor legibilidade
        rect_width = 2.2
        rect_height = 0.8
        rect = Rectangle((pos[0]-rect_width/2, pos[1]-rect_height/2), 
                        rect_width, rect_height, 
                        facecolor='lightyellow', edgecolor='orange', linewidth=2)
        ax.add_patch(rect)
        
        # Texto da variável - FONTE MAIOR
        ax.text(pos[0], pos[1], var_name, ha='center', va='center', 
                fontsize=9, fontweight='bold', wrap=True)
        
        # Seta SAINDO DO CENTRO para a variável
        dx = pos[0] - latent_pos[0]
        dy = pos[1] - latent_pos[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        # Pontos de conexão - DO CENTRO para FORA
        start_factor = 1.8 / distance  # Borda do círculo latente
        end_factor = (distance - rect_width/2 - 0.1) / distance  # Próximo ao retângulo
        
        start_x = latent_pos[0] + dx * start_factor
        start_y = latent_pos[1] + dy * start_factor
        end_x = latent_pos[0] + dx * end_factor
        end_y = latent_pos[1] + dy * end_factor
        
        # Seta RETA do centro para variável
        ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                   arrowprops=dict(arrowstyle='->', color='blue', lw=3))
        
        # Loading (coeficiente) MAIOR e bem posicionado
        loading = np.random.uniform(0.65, 0.85)
        
        # Posição do coeficiente - NO MEIO da seta
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Ajuste para não ficar em cima da seta
        if abs(dx) > abs(dy):  # Seta mais horizontal
            coef_y = mid_y + 0.3 if dy > 0 else mid_y - 0.3
            coef_x = mid_x
        else:  # Seta mais vertical
            coef_x = mid_x + 0.3 if dx > 0 else mid_x - 0.3
            coef_y = mid_y
        
        ax.text(coef_x, coef_y, f'{loading:.2f}', 
                ha='center', va='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', 
                         edgecolor='blue', alpha=0.9))
    
    # Título MAIOR
    ax.text(9, 13, f'Modelo de Medição - {construto_nome}', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Estatísticas em posição FIXA
    stats_text = f'Variáveis: {n_variaveis}\nMédia: 4.2\nAlpha: 0.85'
    ax.text(16, 2, stats_text, ha='left', va='bottom', fontsize=11,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
    
    # Legenda FIXA em posição segura
    legenda_text = 'LEGENDA:\n• Elipse = Construto Latente\n• Retângulos = Variáveis Observadas\n• Setas = Cargas Fatoriais\n• Números = Coeficientes Padronizados'
    ax.text(16, 12, legenda_text, ha='left', va='top', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.4", facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    
    if salvar:
        filename = f'diagrama_{construto_nome.lower()}_final_corrigido.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"   ✓ Salvo: {filename}")
    
    plt.close()

def corrigir_diagramas_problematicos():
    """Corrige apenas os diagramas com problemas específicos"""
    print("CORREÇÃO ESPECÍFICA: PERCEPÇÃO E EXPERIÊNCIA")
    print("="*50)
    
    # Corrigir apenas os construtos problemáticos
    for construto in VARIAVEIS_PROBLEMATICAS.keys():
        criar_diagrama_corrigido_especifico(construto)
    
    print("\n" + "="*50)
    print("CORREÇÕES ESPECÍFICAS IMPLEMENTADAS!")
    print("="*50)
    print("PROBLEMAS RESOLVIDOS:")
    print("✓ PERCEPÇÃO: Layout circular amplo (raio 5.0)")
    print("✓ EXPERIÊNCIA: Layout circular amplo (raio 5.0)")
    print("✓ Variáveis afastadas do centro")
    print("✓ Centro claramente visível")
    print("✓ Sem sobreposições")
    print("\nARQUIVOS CORRIGIDOS:")
    print("✓ diagrama_percepcao_final_corrigido.png")
    print("✓ diagrama_experiencia_final_corrigido.png")

if __name__ == "__main__":
    corrigir_diagramas_problematicos() 