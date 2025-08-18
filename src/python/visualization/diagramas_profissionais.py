#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Criar Diagrama SEM Profissional - Estilo Acadêmico
Baseado no layout da imagem de referência fornecida
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def criar_diagrama_sem_profissional():
    """Cria um diagrama SEM profissional seguindo padrões acadêmicos"""
    
    print("🎨 CRIANDO DIAGRAMA SEM PROFISSIONAL...")
    
    # Configurar figura com fundo branco limpo
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Título principal
    ax.text(5, 7.5, 'MODELO ESTRUTURAL DE TRANSPORTE PÚBLICO E RECOMPENSAS', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(5, 7.2, 'Análise de Equações Estruturais com 7 Construtos (N=703)', 
            ha='center', va='center', fontsize=12)
    
    # Definir posições dos construtos de forma organizada
    construtos = {
        'Perfil\nSocioeconômico': (1.5, 6),
        'Qualidade\nServiço': (1.5, 4.5),
        'Experiência\nUsuário': (4, 6),
        'Aceitação\nTecnologia': (4, 3),
        'Percepção\nRecompensas': (6.5, 4.5),
        'Intenção\nComportamental': (8.5, 4.5),
        'Utilização\nReal': (8.5, 6)
    }
    
    # Cores suaves e profissionais
    cores_construtos = {
        'Perfil\nSocioeconômico': '#E8F4FD',
        'Qualidade\nServiço': '#E1F5FE', 
        'Experiência\nUsuário': '#F3E5F5',
        'Aceitação\nTecnologia': '#E8F5E8',
        'Percepção\nRecompensas': '#FFF3E0',
        'Intenção\nComportamental': '#FCE4EC',
        'Utilização\nReal': '#F1F8E9'
    }
    
    # Desenhar construtos como retângulos arredondados
    construtos_shapes = {}
    for nome, (x, y) in construtos.items():
        cor = cores_construtos[nome]
        
        # Retângulo arredondado
        rect = FancyBboxPatch((x-0.6, y-0.3), 1.2, 0.6,
                              boxstyle="round,pad=0.02",
                              facecolor=cor,
                              edgecolor='black',
                              linewidth=1.5)
        ax.add_patch(rect)
        construtos_shapes[nome] = (x, y)
        
        # Texto do construto
        ax.text(x, y, nome, ha='center', va='center', 
                fontsize=10, fontweight='bold')
    
    # Definir relações com coeficientes reais dos dados
    relacoes = [
        ('Perfil\nSocioeconômico', 'Utilização\nReal', 0.25, 'direto'),
        ('Qualidade\nServiço', 'Experiência\nUsuário', 0.42, 'direto'),
        ('Experiência\nUsuário', 'Intenção\nComportamental', 0.08, 'direto'),
        ('Aceitação\nTecnologia', 'Percepção\nRecompensas', 0.36, 'direto'),
        ('Percepção\nRecompensas', 'Intenção\nComportamental', 0.896, 'forte'),
        ('Intenção\nComportamental', 'Utilização\nReal', 0.60, 'direto'),
        ('Qualidade\nServiço', 'Aceitação\nTecnologia', 0.36, 'correlação')
    ]
    
    # Desenhar as setas/relações
    for origem, destino, coef, tipo in relacoes:
        x1, y1 = construtos_shapes[origem]
        x2, y2 = construtos_shapes[destino]
        
        # Definir estilo baseado no tipo e força da relação
        if tipo == 'forte':
            cor_seta = '#D32F2F'  # Vermelho para relação muito forte
            largura = 3
            estilo = '->'
        elif tipo == 'direto':
            cor_seta = '#1976D2'  # Azul para relações diretas
            largura = 2
            estilo = '->'
        else:  # correlação
            cor_seta = '#388E3C'  # Verde para correlações
            largura = 2
            estilo = '<->'
        
        # Calcular pontos de conexão nas bordas dos retângulos
        dx = x2 - x1
        dy = y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        
        # Normalizar e ajustar para as bordas
        dx_norm = dx / dist
        dy_norm = dy / dist
        
        x1_adj = x1 + dx_norm * 0.6
        y1_adj = y1 + dy_norm * 0.3
        x2_adj = x2 - dx_norm * 0.6
        y2_adj = y2 - dy_norm * 0.3
        
        # Desenhar seta
        if estilo == '<->':
            # Seta bidirecional para correlações
            ax.annotate('', xy=(x2_adj, y2_adj), xytext=(x1_adj, y1_adj),
                       arrowprops=dict(arrowstyle='<->', lw=largura, 
                                     color=cor_seta, alpha=0.8))
        else:
            # Seta unidirecional
            ax.annotate('', xy=(x2_adj, y2_adj), xytext=(x1_adj, y1_adj),
                       arrowprops=dict(arrowstyle='->', lw=largura, 
                                     color=cor_seta, alpha=0.8))
        
        # Adicionar coeficiente no meio da seta
        mid_x = (x1_adj + x2_adj) / 2
        mid_y = (y1_adj + y2_adj) / 2
        
        # Destacar coeficiente da relação mais forte
        if coef > 0.8:
            bbox_props = dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.9)
            fontweight = 'bold'
            fontsize = 11
        else:
            bbox_props = dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.9)
            fontweight = 'normal'
            fontsize = 10
        
        ax.text(mid_x, mid_y, f'{coef:.3f}', 
                bbox=bbox_props, fontsize=fontsize, fontweight=fontweight,
                ha='center', va='center')
    
    # Adicionar legenda de interpretação
    legenda_x = 0.5
    legenda_y = 2.5
    
    ax.text(legenda_x, legenda_y, 'LEGENDA:', fontsize=12, fontweight='bold')
    
    # Elementos da legenda
    elementos_legenda = [
        ('Retângulos: Construtos Latentes', '#E8F4FD'),
        ('Setas Vermelhas: Relação Muito Forte (r > 0.8)', '#D32F2F'),
        ('Setas Azuis: Relações Estruturais Diretas', '#1976D2'),
        ('Setas Verdes: Correlações', '#388E3C'),
        ('Números: Coeficientes Padronizados', 'black')
    ]
    
    for i, (texto, cor) in enumerate(elementos_legenda):
        y_pos = legenda_y - 0.3 * (i + 1)
        
        if 'Setas' in texto:
            # Desenhar pequena seta demonstrativa
            ax.annotate('', xy=(legenda_x + 0.3, y_pos), xytext=(legenda_x, y_pos),
                       arrowprops=dict(arrowstyle='->', lw=2, color=cor))
            ax.text(legenda_x + 0.5, y_pos, texto, fontsize=10, va='center')
        elif 'Retângulos' in texto:
            # Desenhar pequeno retângulo demonstrativo
            rect_demo = FancyBboxPatch((legenda_x, y_pos-0.1), 0.3, 0.2,
                                      boxstyle="round,pad=0.02",
                                      facecolor=cor, edgecolor='black')
            ax.add_patch(rect_demo)
            ax.text(legenda_x + 0.5, y_pos, texto, fontsize=10, va='center')
        else:
            ax.text(legenda_x, y_pos, texto, fontsize=10, va='center', color=cor)
    
    # Adicionar estatísticas do modelo no canto superior direito
    stats_x = 7
    stats_y = 2.5
    
    estatisticas = [
        'ESTATÍSTICAS DO MODELO:',
        '',
        'N = 703 respondentes',
        'Construtos = 7',
        'Variáveis = 65+',
        '',
        'ACHADO PRINCIPAL:',
        'Percepção -> Intenção',
        'r = 0.896 (Muito Forte)',
        '',
        'R² = 80.3%',
        'p < 0.001'
    ]
    
    for i, stat in enumerate(estatisticas):
        y_pos = stats_y - 0.2 * i
        if i == 0 or 'ACHADO' in stat:
            fontweight = 'bold'
            fontsize = 11
        else:
            fontweight = 'normal'
            fontsize = 10
        
        ax.text(stats_x, y_pos, stat, fontsize=fontsize, 
                fontweight=fontweight, va='center')
    
    # Adicionar caixa de destaque para a descoberta principal
    destaque_x = 2.5
    destaque_y = 1.5
    
    # Caixa de destaque
    destaque_rect = FancyBboxPatch((destaque_x-0.8, destaque_y-0.4), 4, 0.8,
                                   boxstyle="round,pad=0.05",
                                   facecolor='#FFEB3B', edgecolor='#F57F17',
                                   linewidth=2, alpha=0.9)
    ax.add_patch(destaque_rect)
    
    ax.text(destaque_x + 1.2, destaque_y, 
            '[BUSCA] DESCOBERTA PRINCIPAL: Percepção de Recompensas explica 80% da Intenção Comportamental',
            fontsize=12, fontweight='bold', ha='center', va='center')
    
    # Salvar com alta resolução
    plt.tight_layout()
    plt.savefig('diagrama_sem_profissional_7_construtos.png', 
                dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print("✅ Diagrama SEM profissional salvo como 'diagrama_sem_profissional_7_construtos.png'")

def criar_diagrama_simplificado_foco():
    """Cria um diagrama simplificado focando apenas nas relações mais importantes"""
    
    print("🎨 CRIANDO DIAGRAMA SIMPLIFICADO...")
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Título
    ax.text(5, 5.5, 'MODELO SIMPLIFICADO - RELAÇÕES PRINCIPAIS', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(5, 5.2, 'Foco nas Descobertas Mais Importantes (N=703)', 
            ha='center', va='center', fontsize=12)
    
    # Apenas os construtos mais importantes
    construtos_principais = {
        'Aceitação\nTecnologia': (2, 3),
        'Percepção\nRecompensas': (5, 3),
        'Intenção\nComportamental': (8, 3)
    }
    
    cores_principais = {
        'Aceitação\nTecnologia': '#E8F5E8',
        'Percepção\nRecompensas': '#FFF3E0',
        'Intenção\nComportamental': '#FCE4EC'
    }
    
    # Desenhar construtos principais
    for nome, (x, y) in construtos_principais.items():
        cor = cores_principais[nome]
        
        # Círculo maior para destaque
        circle = plt.Circle((x, y), 0.8, facecolor=cor, edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        
        ax.text(x, y, nome, ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    # Relações principais
    relacoes_principais = [
        ('Aceitação\nTecnologia', 'Percepção\nRecompensas', 0.360),
        ('Percepção\nRecompensas', 'Intenção\nComportamental', 0.896)
    ]
    
    for origem, destino, coef in relacoes_principais:
        x1, y1 = construtos_principais[origem]
        x2, y2 = construtos_principais[destino]
        
        # Seta mais grossa para o relacionamento principal
        if coef > 0.8:
            largura = 5
            cor = '#D32F2F'
        else:
            largura = 3
            cor = '#1976D2'
        
        ax.annotate('', xy=(x2-0.8, y2), xytext=(x1+0.8, y1),
                   arrowprops=dict(arrowstyle='->', lw=largura, color=cor))
        
        # Coeficiente em destaque
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 0.3
        
        if coef > 0.8:
            bbox_props = dict(boxstyle="round,pad=0.4", facecolor='yellow', alpha=1.0)
            fontsize = 14
        else:
            bbox_props = dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=1.0)
            fontsize = 12
        
        ax.text(mid_x, mid_y, f'r = {coef:.3f}', 
                bbox=bbox_props, fontsize=fontsize, fontweight='bold',
                ha='center', va='center')
    
    # Explicação clara
    ax.text(5, 1.5, 
            'INTERPRETAÇÃO: Tecnologia facilita a percepção de recompensas,\nque por sua vez é o PRINCIPAL preditor da intenção comportamental',
            ha='center', va='center', fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('diagrama_sem_simplificado_foco.png', 
                dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print("✅ Diagrama simplificado salvo como 'diagrama_sem_simplificado_foco.png'")

def main():
    """Função principal"""
    print("[INICIO] CRIANDO DIAGRAMAS SEM PROFISSIONAIS")
    print("="*60)
    
    # Criar ambos os diagramas
    criar_diagrama_sem_profissional()
    criar_diagrama_simplificado_foco()
    
    print("\n🎉 DIAGRAMAS CRIADOS COM SUCESSO!")
    print("📁 Arquivos gerados:")
    print("   1. diagrama_sem_profissional_7_construtos.png (Completo)")
    print("   2. diagrama_sem_simplificado_foco.png (Simplificado)")

if __name__ == "__main__":
    main() 