#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Criar Diagrama SEM com Storytelling Visual
Foco na experiência humana e narrativa clara
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arrow
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def criar_diagrama_storytelling():
    """Cria um diagrama SEM focado em storytelling visual"""
    
    print("🎨 CRIANDO DIAGRAMA SEM COM STORYTELLING...")
    
    # Configurar figura com proporção 16:9 para apresentações
    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Fundo suave
    fig.patch.set_facecolor('#FAFAFA')
    
    # Título principal com hierarquia visual
    ax.text(6, 7.5, 'DESCOBERTA PRINCIPAL:', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1565C0')
    ax.text(6, 7.1, 'Sistema de Recompensas Transforma Comportamento no Transporte Público', 
            ha='center', va='center', fontsize=14, color='#424242')
    ax.text(6, 6.8, 'Análise com 703 usuários reais • 7 dimensões investigadas', 
            ha='center', va='center', fontsize=11, color='#757575', style='italic')
    
    # Definir construtos com posicionamento narrativo (da esquerda para direita = jornada do usuário)
    construtos = {
        'Perfil\nDemográfico': (1.5, 5.5),      # QUEM SÃO
        'Qualidade\nAtual': (1.5, 3.5),        # SITUAÇÃO ATUAL
        'Experiência\nAtual': (3.5, 5.5),      # COMO SE SENTEM
        'Tecnologia': (3.5, 3.5),              # FACILITADOR
        'Recompensas': (6, 4.5),               # SOLUÇÃO
        'Intenção\nFutura': (8.5, 4.5),        # RESULTADO
        'Uso\nReal': (10.5, 4.5)               # COMPORTAMENTO
    }
    
    # Cores seguindo paleta psicológica
    cores_narrativa = {
        'Perfil\nDemográfico': '#E3F2FD',      # Azul claro - neutro, informativo
        'Qualidade\nAtual': '#FFEBEE',         # Rosa claro - problema atual
        'Experiência\nAtual': '#FFF3E0',       # Laranja claro - experiência
        'Tecnologia': '#E8F5E8',              # Verde claro - facilitador
        'Recompensas': '#FFF9C4',             # Amarelo claro - solução positiva
        'Intenção\nFutura': '#E1F5FE',        # Azul - resultado desejado
        'Uso\nReal': '#F3E5F5'                # Roxo claro - comportamento final
    }
    
    # Rótulos explicativos para storytelling
    rotulos_storytelling = {
        'Perfil\nDemográfico': 'QUEM SÃO\nOS USUÁRIOS',
        'Qualidade\nAtual': 'PROBLEMAS\nATUAIS',
        'Experiência\nAtual': 'COMO SE\nSENTEM HOJE',
        'Tecnologia': 'O QUE\nFACILITA',
        'Recompensas': 'A SOLUÇÃO\nMAGICA',
        'Intenção\nFutura': 'O QUE\nQUEREM',
        'Uso\nReal': 'O QUE\nFAZEM'
    }
    
    # Desenhar construtos como círculos mais atrativos
    construtos_coords = {}
    for nome, (x, y) in construtos.items():
        cor = cores_narrativa[nome]
        
        # Círculo principal
        circle = Circle((x, y), 0.7, facecolor=cor, edgecolor='#424242', linewidth=2)
        ax.add_patch(circle)
        construtos_coords[nome] = (x, y)
        
        # Texto do construto
        ax.text(x, y + 0.1, nome, ha='center', va='center', 
                fontsize=11, fontweight='bold', color='#212121')
        
        # Rótulo explicativo abaixo
        rotulo = rotulos_storytelling[nome]
        ax.text(x, y - 0.4, rotulo, ha='center', va='center',
                fontsize=8, color='#616161', style='italic')
    
    # Relações com narrativa visual
    relacoes_narrativa = [
        ('Perfil\nDemográfico', 'Uso\nReal', 0.25, 'contexto'),
        ('Qualidade\nAtual', 'Experiência\nAtual', 0.42, 'influencia'),
        ('Qualidade\nAtual', 'Tecnologia', 0.36, 'influencia'),
        ('Tecnologia', 'Recompensas', 0.36, 'facilita'),
        ('Recompensas', 'Intenção\nFutura', 0.896, 'transforma'),  # PRINCIPAL
        ('Intenção\nFutura', 'Uso\nReal', 0.60, 'resulta'),
        ('Experiência\nAtual', 'Intenção\nFutura', 0.08, 'baixa')
    ]
    
    # Desenhar relações com storytelling
    for origem, destino, coef, tipo in relacoes_narrativa:
        x1, y1 = construtos_coords[origem]
        x2, y2 = construtos_coords[destino]
        
        # Definir estilo narrativo
        if tipo == 'transforma':  # DESCOBERTA PRINCIPAL
            cor_seta = '#C62828'  # Vermelho forte
            largura = 5
            alpha = 1.0
            destaque = True
        elif tipo == 'facilita':
            cor_seta = '#2E7D32'  # Verde forte
            largura = 3
            alpha = 0.9
            destaque = False
        elif tipo == 'resulta':
            cor_seta = '#1565C0'  # Azul forte
            largura = 3
            alpha = 0.9
            destaque = False
        elif tipo == 'baixa':
            cor_seta = '#9E9E9E'  # Cinza - relação fraca
            largura = 1
            alpha = 0.6
            destaque = False
        else:  # contexto, influencia
            cor_seta = '#455A64'  # Cinza azulado
            largura = 2
            alpha = 0.7
            destaque = False
        
        # Calcular pontos de conexão
        dx = x2 - x1
        dy = y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        dx_norm = dx / dist
        dy_norm = dy / dist
        
        x1_adj = x1 + dx_norm * 0.7
        y1_adj = y1 + dy_norm * 0.7
        x2_adj = x2 - dx_norm * 0.7
        y2_adj = y2 - dy_norm * 0.7
        
        # Desenhar seta
        ax.annotate('', xy=(x2_adj, y2_adj), xytext=(x1_adj, y1_adj),
                   arrowprops=dict(arrowstyle='->', lw=largura, 
                                 color=cor_seta, alpha=alpha))
        
        # Coeficiente com destaque visual apropriado
        mid_x = (x1_adj + x2_adj) / 2
        mid_y = (y1_adj + y2_adj) / 2
        
        if destaque:
            # Destaque especial para descoberta principal
            bbox_props = dict(boxstyle="round,pad=0.4", 
                            facecolor='#FFEB3B', edgecolor='#F57F17',
                            linewidth=2, alpha=0.95)
            fontsize = 13
            fontweight = 'bold'
            color = '#BF360C'
        else:
            bbox_props = dict(boxstyle="round,pad=0.25", 
                            facecolor='white', edgecolor='#BDBDBD',
                            linewidth=1, alpha=0.9)
            fontsize = 10
            fontweight = 'normal'
            color = '#424242'
        
        ax.text(mid_x, mid_y, f'{coef:.3f}', 
                bbox=bbox_props, fontsize=fontsize, fontweight=fontweight,
                ha='center', va='center', color=color)
    
    # Narrativa visual - Caixas de insights
    
    # 1. Situação Atual (lado esquerdo)
    situacao_box = FancyBboxPatch((0.2, 1.5), 4, 1.2,
                                  boxstyle="round,pad=0.1",
                                  facecolor='#FFCDD2', edgecolor='#D32F2F',
                                  linewidth=2, alpha=0.8)
    ax.add_patch(situacao_box)
    ax.text(2.2, 2.3, '😔 SITUAÇÃO ATUAL', fontsize=12, fontweight='bold', 
            ha='center', color='#C62828')
    ax.text(2.2, 1.9, 'Qualidade baixa (1.67/5) • Experiência ruim (1.42/5)', 
            fontsize=10, ha='center', color='#D32F2F')
    ax.text(2.2, 1.6, 'Usuários insatisfeitos mas dependentes do transporte', 
            fontsize=9, ha='center', color='#D32F2F', style='italic')
    
    # 2. A Transformação (centro)
    transformacao_box = FancyBboxPatch((4.8, 2.5), 2.4, 1.2,
                                       boxstyle="round,pad=0.1",
                                       facecolor='#C8E6C9', edgecolor='#388E3C',
                                       linewidth=2, alpha=0.8)
    ax.add_patch(transformacao_box)
    ax.text(6, 3.3, '⚡ TRANSFORMAÇÃO', fontsize=12, fontweight='bold', 
            ha='center', color='#2E7D32')
    ax.text(6, 2.9, 'Recompensas mudam TUDO', fontsize=11, ha='center', 
            color='#388E3C', fontweight='bold')
    ax.text(6, 2.6, '89% de correlação', fontsize=10, ha='center', color='#2E7D32')
    
    # 3. Resultado (lado direito)
    resultado_box = FancyBboxPatch((7.8, 1.5), 4, 1.2,
                                   boxstyle="round,pad=0.1",
                                   facecolor='#BBDEFB', edgecolor='#1976D2',
                                   linewidth=2, alpha=0.8)
    ax.add_patch(resultado_box)
    ax.text(9.8, 2.3, '🎯 RESULTADO DESEJADO', fontsize=12, fontweight='bold', 
            ha='center', color='#1565C0')
    ax.text(9.8, 1.9, 'Intenção alta (4.51/5) • Uso aumentado (60%)', 
            fontsize=10, ha='center', color='#1976D2')
    ax.text(9.8, 1.6, 'Usuários engajados e satisfeitos', 
            fontsize=9, ha='center', color='#1976D2', style='italic')
    
    # Seta de transformação (visual storytelling)
    ax.annotate('', xy=(7.5, 2.1), xytext=(4.5, 2.1),
               arrowprops=dict(arrowstyle='->', lw=6, color='#FF6F00', alpha=0.8))
    ax.text(6, 1.8, 'RECOMPENSAS TRANSFORMAM', fontsize=11, fontweight='bold',
            ha='center', color='#EF6C00')
    
    # Estatísticas finais (canto superior direito, mais discreto)
    ax.text(10.5, 6.8, 'DADOS DA PESQUISA', fontsize=10, fontweight='bold', 
            ha='center', color='#424242')
    ax.text(10.5, 6.5, '703 usuários', fontsize=9, ha='center', color='#616161')
    ax.text(10.5, 6.3, '7 dimensões', fontsize=9, ha='center', color='#616161')
    ax.text(10.5, 6.1, '65+ variáveis', fontsize=9, ha='center', color='#616161')
    ax.text(10.5, 5.8, 'R² = 80.3%', fontsize=9, ha='center', color='#616161')
    
    # Remover qualquer faixa amarela ou elemento que atrapalhe
    plt.tight_layout()
    plt.savefig('diagrama_sem_storytelling_limpo.png', 
                dpi=300, bbox_inches='tight',
                facecolor='#FAFAFA', edgecolor='none')
    plt.close()
    
    print("✅ Diagrama SEM com storytelling salvo como 'diagrama_sem_storytelling_limpo.png'")

def criar_diagrama_executivo_simples():
    """Versão ultra-simplificada para executivos"""
    
    print("🎨 CRIANDO VERSÃO EXECUTIVA...")
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    
    # Título executivo
    ax.text(5, 5.5, 'DESCOBERTA: Recompensas Aumentam Uso do Transporte Público em 89%', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1565C0')
    ax.text(5, 5.1, 'Pesquisa com 703 usuários reais', 
            ha='center', va='center', fontsize=12, color='#757575')
    
    # Apenas 3 elementos principais
    elementos = {
        'PROBLEMA\nATUAL': (2, 3),
        'SOLUÇÃO\nRECOMPENSAS': (5, 3),
        'RESULTADO\nESPERADO': (8, 3)
    }
    
    cores_exec = ['#FFCDD2', '#C8E6C9', '#BBDEFB']
    bordas_exec = ['#D32F2F', '#388E3C', '#1976D2']
    
    for i, (nome, (x, y)) in enumerate(elementos.items()):
        # Retângulo arredondado
        rect = FancyBboxPatch((x-1, y-0.8), 2, 1.6,
                              boxstyle="round,pad=0.1",
                              facecolor=cores_exec[i], 
                              edgecolor=bordas_exec[i],
                              linewidth=3)
        ax.add_patch(rect)
        
        ax.text(x, y, nome, ha='center', va='center', 
                fontsize=14, fontweight='bold', color=bordas_exec[i])
    
    # Setas de processo
    ax.annotate('', xy=(3.8, 3), xytext=(3.2, 3),
               arrowprops=dict(arrowstyle='->', lw=4, color='#FF6F00'))
    ax.annotate('', xy=(6.8, 3), xytext=(6.2, 3),
               arrowprops=dict(arrowstyle='->', lw=4, color='#FF6F00'))
    
    # Estatística principal
    ax.text(5, 1.5, '89% de correlação entre recompensas e intenção de uso', 
            ha='center', va='center', fontsize=16, fontweight='bold', 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#FFEB3B', alpha=0.9),
            color='#BF360C')
    
    plt.tight_layout()
    plt.savefig('diagrama_executivo_simples.png', 
                dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print("✅ Diagrama executivo salvo como 'diagrama_executivo_simples.png'")

def main():
    """Função principal"""
    print("[INICIO] CRIANDO DIAGRAMAS COM STORYTELLING VISUAL")
    print("="*60)
    
    criar_diagrama_storytelling()
    criar_diagrama_executivo_simples()
    
    print("\n🎉 DIAGRAMAS COM STORYTELLING CRIADOS!")
    print("📁 Arquivos gerados:")
    print("   1. diagrama_sem_storytelling_limpo.png (Narrativa completa)")
    print("   2. diagrama_executivo_simples.png (Versão executiva)")

if __name__ == "__main__":
    main() 