'''
Arquivo para análise de dados de transporte público e modelagem SEM.

Este script realiza:
1. Carregamento dos dados consolidados (BDTP.csv).
2. Limpeza e preparação dos dados utilizando pandas:
    - Renomeação e padronização de nomes de colunas.
    - Limpeza de valores (remoção de espaços, tratamento de categorias).
    - Conversão de escalas Likert para valores numéricos.
    - Conversão de tipos de dados.
3. Definição das especificações dos Modelos de Equações Estruturais (SEM)
   em formato semopy, conforme o escopo do projeto.
4. Modelagem SEM para cada bloco temático do questionário.
5. Modelagem SEM global integrando as variáveis de todas as seções.
6. Geração de tabelas e visualizações dos resultados.
'''

print("DEBUG: Script iniciado, tentando importar bibliotecas...") # DEBUG PRINT 1

import pandas as pd
import numpy as np
import semopy
import re
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import logit
from scipy import stats
import os
import sys

print("DEBUG: Bibliotecas importadas com sucesso.") # DEBUG PRINT 2

# --- 1. Carregar Dados ---
def load_data(file_path='csv_extraidos/BDTP.csv'):
    '''Carrega o arquivo CSV consolidado.'''
    print(f"DEBUG: Entrando na função load_data com file_path={file_path}") # DEBUG PRINT
    try:
        print("DEBUG: load_data - Dentro do bloco try inicial.") # DEBUG PRINT
        df = pd.read_csv(file_path, sep=',')
        print(f"Dados carregados com sucesso de {file_path}. Shape: {df.shape}")
        # DESCOMENTE AS PRÓXIMAS 3 LINHAS PARA VER OS NOMES EXATOS DAS COLUNAS DO SEU CSV:
        print("\nNOMES ORIGINAIS DAS COLUNAS DO CSV (para depuração do mapeamento):")
        for col_idx, col_name in enumerate(df.columns):
            print(f"Coluna {col_idx}: '{col_name}'")
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return None
    except pd.errors.ParserError:
        print(f"Erro de parser ao ler {file_path}. Tentando com separador ';'...")
        try:
            df = pd.read_csv(file_path, sep=';')
            print(f"Dados carregados com sucesso de {file_path} com separador ';'. Shape: {df.shape}")
            # DESCOMENTE AS PRÓXIMAS 3 LINHAS PARA VER OS NOMES EXATOS DAS COLUNAS DO SEU CSV (tentativa com ';'):
            print("\nNOMES ORIGINAIS DAS COLUNAS DO CSV (para depuração do mapeamento) - tentativa com ';':")
            for col_idx, col_name in enumerate(df.columns):
                print(f"Coluna {col_idx}: '{col_name}'")
            return df
        except Exception as e:
            print(f"Erro ao carregar BDTP.csv mesmo com separador ';': {e}")
            return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar {file_path}: {e}")
        return None

# --- 2. Limpeza e Preparação dos Dados ---
def normalize_column_name(col_name):
    '''Normaliza o nome da coluna: minúsculas, snake_case, remove acentos e caracteres especiais.'''
    if not isinstance(col_name, str):
        return str(col_name) # Garante que é string
    name = col_name.lower()
    name = re.sub(r'[\n\r\t]+', ' ', name) # Remove quebras de linha e tabs, substitui por espaço
    name = name.strip()
    # Remove acentos (simplificado, pode precisar de unicodedata para robustez total)
    name = re.sub(r'[áàâãä]', 'a', name)
    name = re.sub(r'[éèêë]', 'e', name)
    name = re.sub(r'[íìîï]', 'i', name)
    name = re.sub(r'[óòôõö]', 'o', name)
    name = re.sub(r'[úùûü]', 'u', name)
    name = re.sub(r'ç', 'c', name)
    # Remove caracteres especiais exceto underscore e alphanumeric. Mantém espaços para substituir por underscore depois.
    name = re.sub(r'[^a-z0-9_ ]', '', name)
    name = re.sub(r'\s+', '_', name) # Substitui um ou mais espaços por um único underscore
    name = re.sub(r'_+', '_', name) # Remove underscores duplicados
    return name.strip('_')

def get_column_mappings():
    """Retorna um dicionário de mapeamento. CHAVES DEVEM SER IDÊNTICAS AOS NOMES LIDOS DO CSV.
       Atualizado com base na saída EXATA de df.columns (usando repr()) fornecida pelo usuário."""
    print("DEBUG: Entrando em get_column_mappings (versão SUPER corrigida com repr() do usuário)") # DEBUG PRINT
    mapping = {
        'ID': 'id',
        'Preço da passagem': 'qual_preco_passagem',
        'Espaço disponível é suficiente para os passageiros sentados ou em pé': 'qual_espaco_disponivel',
        'Temperatura interna\xa0': 'qual_temperatura_interna',
        'Tempo total de viagem\xa0 ': 'qual_tempo_viagem',
        'Frequência com que os veículos passam ao longo dia ': 'qual_frequencia_veiculos',
        'Velocidade dos veículos\xa0\xa0': 'qual_velocidade_veiculos',
        'Segurança dentro dos veículos e nos pontos de ônibus/estações ': 'qual_seguranca',
        'Informação de linhas, horários e itinerários\xa0 ': 'qual_informacao_linhas',
        'Locais atendidos pelo transporte público\xa0': 'qual_locais_atendidos',
        'Confiabilidade nos horários\xa0': 'qual_confiabilidade_horarios',
        'Facilidade de entrada e saída dos veículos e/ou estações e pontos de ônibus  ': 'qual_facilidade_acesso',
        'Limpeza dentro do veículo e nos pontos de ônibus e estações': 'qual_limpeza',
        'Qual a forma que você faz a maioria das viagens?': 'util_forma_principal_viagem',
        'Você tem carteira de motorista?': 'util_possui_carteira',
        'Você tem veículo próprio?': 'util_possui_veiculo',
        'Você costuma usar o transporte público em quais dias?': 'util_dias_uso_tp',
        'Como você define sua frequência de uso do transporte público?': 'util_frequencia_uso_tp',
        'Quantas passagens você usa por dia em suas viagens no transporte público?\n': 'util_qtd_passagens_dia',
        'Qual o meio de pagamento você utiliza para pagar pelo transporte?': 'util_meio_pagamento',
        'Qual a principal razão dos seus deslocamentos diários?': 'util_razao_deslocamento',
        'Quanto tempo você gasta por dia com transporte?': 'util_tempo_gasto_transporte',
        'Qual a principal razão pela qual você preferiria utilizar outro meio de transporte ao invés do transporte público?\n\n': 'util_razao_preferir_outro_transporte',
        'Eu gostaria de ganhar pontos ou créditos para trocar por produtos e serviços': 'percep_gostaria_pontos_creditos',
        'Eu gostaria de poder usar qualquer veículo do transporte público de forma ilimitada': 'percep_gostaria_uso_ilimitado',
        'Eu gostaria de poder realizar uma compra antecipada por passagens ilimitadas no transporte público (pré-pago)': 'percep_gostaria_pre_pago_ilimitado',
        'Eu gostaria de poder realizar um pagamento depois de usar passagens ilimitadas no transporte público (pós-pago)': 'percep_gostaria_pos_pago_ilimitado',
        'Eu gostaria de ter a opção de\xa0pagar um valor diário por passagens ilimitadas no transporte público': 'percep_gostaria_pagar_diario_ilimitado',
        'Eu gostaria de ter a opção de pagar\xa0um valor mensal por passagens ilimitadas no transporte público': 'percep_gostaria_pagar_mensal_ilimitado',
        'Eu gostaria de ter a opção de pagar\xa0um valor anual por passagens ilimitadas no transporte público': 'percep_gostaria_pagar_anual_ilimitado',
        'Eu gostaria de receber um valor de volta por quilômetro viajado\xa0no transporte público\xa0': 'percep_gostaria_cashback_km',
        'Eu gostaria de receber desconto na passagem por viajar em horários fora de pico': 'percep_gostaria_desconto_fora_pico',
        'Se eu ganhasse pontos para trocar por produtos e serviços,\xa0usaria mais o transporte público\xa0': 'intencao_usaria_mais_com_pontos',
        'Se eu pudesse pagar por dia para ter passagens ilimitadas, usaria mais transporte público': 'intencao_usaria_mais_passe_diario',
        'Se eu pudesse pagar por mês para ter passagens ilimitadas, usaria mais transporte público\xa0': 'intencao_usaria_mais_passe_mensal',
        'Se eu pudesse pagar por ano para ter passagens ilimitadas, usaria mais transporte público\xa0': 'intencao_usaria_mais_passe_anual',
        'Se eu recebesse um valor em troca por quilometro viajado, usaria mais o transporte público\xa0': 'intencao_usaria_mais_cashback_km',
        'Se ganhasse desconto na passagem por viajar em horários fora de pico, usaria mais o transporte público\xa0': 'intencao_usaria_mais_desconto_fora_pico',
        'Eu aceitaria participar se ganhasse 10 pontos para trocar por produtos e serviços por utilizar o transporte público': 'aceit_participar_10_pontos',
        'Eu aceitaria pagar até 10 reais por dia para ter viagens ilimitadas nesse mesmo dia no transporte público': 'aceit_pagar_ate_10_dia',
        'Eu aceitaria pagar de 10 a 20 reais por dia para ter viagens ilimitadas nesse mesmo dia\xa0no transporte público': 'aceit_pagar_10_20_dia',
        'Eu aceitaria pagar entre 150 e 200 reais mensais para ter viagens ilimitadas em um mês no transporte público': 'aceit_pagar_150_200_mes',
        'Eu aceitaria pagar entre 200 e 300 reais mensais para ter viagens ilimitadas em um mês no transporte público': 'aceit_pagar_200_300_mes',
        'Eu aceitaria pagar de 800 a 1000 reais por ano para ter viagens ilimitadas em um ano\xa0no transporte público': 'aceit_pagar_800_1000_ano',
        'Eu aceitaria pagar entre 1000 e 1200 reais por ano para ter viagens ilimitadas em um ano\xa0no transporte público': 'aceit_pagar_1000_1200_ano',
        'Eu aceitaria receber até 50 centavos por quilômetro percorrido no transporte público\xa0': 'aceit_receber_50cent_km',
        'Eu aceitaria receber até 5 reais a cada 20 quilômetros percorridos no transporte público\xa0': 'aceit_receber_5reais_20km',
        'Eu aceitaria viajar em horários fora de pico se recebesse até 1 real de desconto na passagem': 'aceit_desconto_1real_fora_pico',
        'Eu aceitaria viajar em horários fora de pico se recebesse até 2 reais de desconto na passagem': 'aceit_desconto_2reais_fora_pico',
        'Eu estou satisfeito com o serviço entregue pelo transporte público\xa0': 'exp_satisfeito_servico',
        'O serviço transporte Público correspondem às minhas expectativas': 'exp_corresponde_expectativas',
        'Considero que as minhas necessidades de deslocamento estão sendo atendidos pelo transporte público': 'exp_necessidades_atendidas',
        'Considero que o transporte público tem um bom custo benefício\xa0': 'exp_bom_custo_beneficio',
        'Considero que sou recompensado por usar o transporte público': 'exp_sente_recompensado',
        'Cartões': 'exp_facilidade_cartoes',
        'Aplicativos de celular': 'exp_facilidade_aplicativos',
        'Qr Code': 'exp_facilidade_qrcode',
        'Bilhete impresso': 'exp_facilidade_bilhete_impresso',
        'Gênero\xa0': 'genero',
        'Raça': 'raca',
        'Idade': 'idade_faixa',
        'Nível de escolaridade\n': 'escolaridade',
        'Situação Profissional\xa0': 'situacao_profissional',
        'Possui filhos?\xa0 (Insira o número, no caso de não possuir colocar o número zero)': 'possui_filhos',
        'Renda': 'renda_faixa'
    }
    return mapping

def clean_data(df):
    '''Aplica todas as etapas de limpeza e preparação no DataFrame.'''
    print("DEBUG: Entrando na função clean_data") # DEBUG PRINT
    if df is None:
        print("DEBUG: clean_data - DataFrame de entrada é None, retornando None.") # DEBUG PRINT
        return None

    col_map = get_column_mappings()

    # Diagnóstico ANTES de renomear - IMPRIMIR CHAVES E COLUNAS REAIS
    print("\n--- DEBUG: DIAGNÓSTICO DETALHADO ANTES DO RENAME ---")
    print("Chaves do dicionário de mapeamento (col_map.keys()):")
    print(list(col_map.keys()))
    print("Nomes das colunas do DataFrame (df.columns.tolist()):")
    print(df.columns.tolist())
    print("Comparando cada chave com as colunas do DataFrame:")
    for key_map in col_map.keys():
        if key_map not in df.columns:
            print(f"  -> CHAVE NÃO ENCONTRADA NO DF: '{key_map}' (Tipo: {type(key_map)}, Comprimento: {len(key_map)})")
            # Tentar encontrar similaridades
            for col_df in df.columns:
                if key_map.strip() == col_df.strip():
                    print(f"     POTENCIALMENTE SIMILAR (após strip): '{col_df}' (Tipo: {type(col_df)}, Comprimento: {len(col_df)})")
                    # Imprimir representação para ver caracteres invisíveis
                    print(f"     Repr da chave: {repr(key_map)}")
                    print(f"     Repr da coluna DF: {repr(col_df)}")
                    break
        # else:
        #     print(f"  -> Chave ENCONTRADA: '{key_map}'")
    print("----------------------------------------------------\n")

    try:
        print("DEBUG: clean_data - Tentando renomear colunas...") # DEBUG PRINT
        df.rename(columns=col_map, inplace=True, errors='raise') # Usar 'raise' para ver se alguma chave causa erro
        print("DEBUG: clean_data - Renomeação concluída (ou nenhuma chave incompatível encontrada).") # DEBUG PRINT
    except Exception as e:
        print(f"ERRO CRÍTICO DURANTE RENAME: {e}") # DEBUG PRINT
        return None # Aborta a limpeza se o rename falhar

    # Diagnóstico *após* rename
    print("\n--- Diagnóstico Pós-Rename ---")
    expected_new_cols = ['qual_temperatura_interna', 'possui_filhos', 'util_qtd_passagens_dia']
    for col in expected_new_cols:
        if col in df.columns:
            print(f"Coluna '{col}' encontrada após rename.")
        else:
            # Tenta encontrar a versão original normalizada se o rename falhou
            original_key_found = False
            for k, v in col_map.items():
                if v == col: # Encontrou o mapeamento para o nome esperado
                    normalized_original = normalize_column_name(k)
                    if normalized_original in df.columns:
                        print(f"ERRO: Coluna '{col}' NÃO encontrada após rename, mas '{normalized_original}' existe. Falha no mapeamento de '{k}'")
                        original_key_found = True
                        break
                    else:
                        print(f"ERRO: Coluna '{col}' NÃO encontrada após rename. Tentativa de encontrar '{k}' (norm: '{normalized_original}') falhou.")
                        original_key_found = True # Mesmo que não encontrada, marcamos para não repetir msg
                        break # Para esta coluna esperada
            if not original_key_found:
                print(f"ERRO: Coluna '{col}' NÃO encontrada após rename e não foi possível rastrear a chave original no mapa.")

    print("----------------------------")

    print("DEBUG: clean_data - Iniciando normalização de todos os nomes de colunas...") # DEBUG PRINT
    df.columns = [normalize_column_name(col) for col in df.columns]
    print("\nNomes das colunas após mapeamento e normalização final:")
    # Imprimir todos pode ser verboso, descomente se necessário
    # for col_name in df.columns:
    #     print(f"- {col_name}")
    print("Lista de nomes após normalização final (primeiros/últimos 5):")
    cols_final = list(df.columns)
    if len(cols_final) > 10:
        print(cols_final[:5])
        print("[...] ")
        print(cols_final[-5:])
    else:
        print(cols_final)

    likert_map_5pt_satisfacao = {
        'Muito insatisfeito': 1,
        'Insatisfeito': 2,
        'Neutro': 3,
        'Satisfeito': 4,
        'Muito satisfeito': 5
    }
    likert_map_5pt_concordancia = {
        'Discordo totalmente': 1,
        'Discordo': 2,
        'Neutro': 3,
        'Concordo': 4,
        'Concordo totalmente': 5
    }
    likert_map_5pt_facilidade = {
        'Muito difícil': 1,
        'Difícil': 2,
        'Neutro': 3,
        'Fácil': 4,
        'Muito Fácil': 5
    }
    
    cols_satisfacao = [col for col in df.columns if col.startswith('qual_') ]
    cols_concordancia = [col for col in df.columns if col.startswith('percep_') or col.startswith('intencao_') or col.startswith('aceit_') or col.startswith('exp_satisfeito') or col.startswith('exp_corresponde') or col.startswith('exp_necessidades') or col.startswith('exp_bom_custo') or col.startswith('exp_sente') ]
    cols_facilidade = [col for col in df.columns if col.startswith('exp_facilidade_')]

    for col_list, likert_map in [
        (cols_satisfacao, likert_map_5pt_satisfacao),
        (cols_concordancia, likert_map_5pt_concordancia),
        (cols_facilidade, likert_map_5pt_facilidade)
    ]:
        for col in col_list:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().replace({'(?i)^nan$': pd.NA, '(?i)^None$': pd.NA, '^$': pd.NA}, regex=True)
                df[col] = df[col].replace({
                    'Fácil ': 'Fácil', 'Muito Fácil ': 'Muito Fácil',
                    'Fácil\xa0': 'Fácil', 'Muito Fácil\xa0': 'Muito Fácil',
                    'Concordo ': 'Concordo', 'Concordo totalmente ': 'Concordo totalmente',
                    'Discordo ': 'Discordo', 'Discordo totalmente ': 'Discordo totalmente',
                    'Neutro ': 'Neutro',
                    'Satisfeito ': 'Satisfeito', 'Muito satisfeito ': 'Muito satisfeito',
                    'Insatisfeito ': 'Insatisfeito', 'Muito insatisfeito ': 'Muito insatisfeito',
                })
                df[col] = pd.to_numeric(df[col].map(likert_map), errors='coerce')
            # else:
                # print(f"Aviso DEBUG: Coluna '{col}' não encontrada para mapeamento Likert após normalização.")

    print("DEBUG: clean_data - Verificando coluna 'possui_filhos'...") # DEBUG PRINT
    if 'possui_filhos' in df.columns:
        print("DEBUG: clean_data - Coluna 'possui_filhos' encontrada, tentando conversão numérica.") # DEBUG PRINT
        df['possui_filhos'] = pd.to_numeric(df['possui_filhos'], errors='coerce').fillna(0).astype(int)
    else:
        print("AVISO: Coluna 'possui_filhos' não encontrada após rename/normalização para conversão numérica.")
    
    # Limpeza final para colunas de objeto que não foram convertidas (ex: renda_faixa, etc.)
    print("DEBUG: clean_data - Limpando colunas object restantes...") # DEBUG PRINT
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip().replace({'(?i)^nan$': pd.NA, '(?i)^None$': pd.NA, '^$': pd.NA}, regex=True)

    print(f"\nShape do DataFrame após limpeza: {df.shape}")
    print("DEBUG: clean_data - Saindo da função clean_data") # DEBUG PRINT
    return df

# --- 3. Especificações do Modelo SEM (semopy) ---

# Modelo 1: Qualidade Percebida e Satisfação
model_spec_qualidade = '''
  # Measurement Model
  QualidadePercebida =~ qual_preco_passagem + qual_espaco_disponivel + qual_temperatura_interna + qual_tempo_viagem + qual_frequencia_veiculos + qual_velocidade_veiculos + qual_seguranca + qual_informacao_linhas + qual_locais_atendidos + qual_confiabilidade_horarios + qual_facilidade_acesso + qual_limpeza
'''

# Modelo 2: Utilização do Transporte
model_spec_utilizacao = '''
  # Measurement Model
  FrequenciaUso =~ util_frequencia_uso_tp + util_qtd_passagens_dia + util_dias_uso_tp
  MotivoUso =~ util_razao_deslocamento + util_tempo_gasto_transporte
'''

# Modelo 3: Percepção sobre Recompensas
model_spec_percepcao = '''
  # Measurement Model
  ValorRecompensas =~ percep_gostaria_pontos_creditos + percep_gostaria_cashback_km + percep_gostaria_desconto_fora_pico
  PreferenciaPassesIlimitados =~ percep_gostaria_uso_ilimitado + percep_gostaria_pre_pago_ilimitado + percep_gostaria_pos_pago_ilimitado + percep_gostaria_pagar_diario_ilimitado + percep_gostaria_pagar_mensal_ilimitado + percep_gostaria_pagar_anual_ilimitado
'''

# Modelo 4: Intenção de Uso com Recompensas
model_spec_intencao = '''
  # Measurement Model
  IntencaoUsoPasses =~ intencao_usaria_mais_passe_diario + intencao_usaria_mais_passe_mensal + intencao_usaria_mais_passe_anual
  IntencaoUsoRecompensas =~ intencao_usaria_mais_com_pontos + intencao_usaria_mais_cashback_km + intencao_usaria_mais_desconto_fora_pico
'''

# Modelo 5: Disposição a Participar (WTP)
model_spec_aceitacao = '''
  # Measurement Model
  DisposicaoPagarDiario =~ aceit_pagar_ate_10_dia + aceit_pagar_10_20_dia
  DisposicaoPagarMensal =~ aceit_pagar_150_200_mes + aceit_pagar_200_300_mes
  DisposicaoPagarAnual =~ aceit_pagar_800_1000_ano + aceit_pagar_1000_1200_ano
  DisposicaoAceitarRecompensas =~ aceit_participar_10_pontos + aceit_receber_50cent_km + aceit_receber_5reais_20km + aceit_desconto_1real_fora_pico + aceit_desconto_2reais_fora_pico
'''

# Modelo 6: Experiência e Facilidade de Pagamento
model_spec_experiencia = '''
  # Measurement Model
  ExperienciaGeralComTP =~ exp_satisfeito_servico + exp_corresponde_expectativas + exp_necessidades_atendidas + exp_bom_custo_beneficio + exp_sente_recompensado
  FacilidadePagamento =~ exp_facilidade_cartoes + exp_facilidade_aplicativos + exp_facilidade_qrcode + exp_facilidade_bilhete_impresso
'''

# Modelo Global: Integrando diferentes dimensões
model_spec_global = '''
  # Measurement Model
  QualidadePercebida =~ qual_preco_passagem + qual_espaco_disponivel + qual_seguranca + qual_confiabilidade_horarios
  ExperienciaGeral =~ exp_satisfeito_servico + exp_corresponde_expectativas + exp_necessidades_atendidas
  ValorRecompensas =~ percep_gostaria_pontos_creditos + percep_gostaria_cashback_km + percep_gostaria_desconto_fora_pico
  DisposicaoAceitar =~ aceit_participar_10_pontos + aceit_receber_50cent_km + aceit_desconto_1real_fora_pico
  
  # Structural Model
  ExperienciaGeral ~ QualidadePercebida
  DisposicaoAceitar ~ ValorRecompensas
  DisposicaoAceitar ~ ExperienciaGeral
'''

# Dicionário de todos os modelos para facilitar o processamento
sem_models = {
    "Qualidade do Serviço": model_spec_qualidade,
    "Utilização do Transporte": model_spec_utilizacao,
    "Percepção sobre Recompensas": model_spec_percepcao,
    "Intenção de Uso": model_spec_intencao,
    "Disposição a Participar": model_spec_aceitacao,
    "Experiência e Facilidade de Pagamento": model_spec_experiencia,
    "Modelo Global": model_spec_global
}

def extract_vars_from_sem_spec(spec_string):
    '''Extrai nomes de variáveis observadas (indicadores) de uma string SEM.
       Assume que indicadores são snake_case ou palavras simples minúsculas.'''
    
    # Primeiro, limpar a string para remover possíveis quebras de linha que possam
    # ter sido incluídas em variáveis ou especificações
    spec_string = re.sub(r'(\w+)\n\s*(\w+)', r'\1 \2', spec_string)
    
    # Padrão para encontrar variáveis observadas em relações de medida (format varLatente =~ var1 + var2 + ...)
    # ou em relações estruturais (var1 ~ var2)
    pattern = r'(?:=~|~)\s*([a-zA-Z0-9_\s+]+)'
    matches = re.findall(pattern, spec_string)
    
    # Processar cada match para extrair os nomes de variáveis individuais
    observed_vars = set()
    for match in matches:
        # Dividir por '+' para obter variáveis individuais nas relações de medida
        individual_vars = [v.strip() for v in match.split('+')]
        for var in individual_vars:
            # Ignorar variáveis latentes (começam com letra maiúscula) e strings vazias
            if var and not var[0].isupper():
                # Verificar se a variável contém quebras de linha e remover
                var = var.replace('\n', '').strip()
                
                # Extrair apenas o nome da variável (parte antes do espaço)
                # Isso garante que apenas o nome real da variável seja usado,
                # descartando qualquer texto adicional após o nome
                if ' ' in var:
                    var = var.split(' ')[0].strip()
                
                if var:  # Verificar novamente se não está vazio
                    observed_vars.add(var)
    
    # Definir keywords para excluir falsos positivos
    sem_keywords = {
        'sem', 'model', 'measurement', 'structural', 'regressions', 'covariances', 
        'latents', 'observed', 'define', 'load', 'data', 'fit', 'params', 
        'inspect', 'compare', 'calc_stats', 'semopy', 'pd',
        # Adicionar palavras-chave capitalizadas que podem ser confundidas com variáveis
        'Model', 'Measurement', 'Structural', 'Latent', 'Observed', 'Regressions', 'Covariances',
        # Palavras comuns de comentários
        'modelo', 'relações', 'estruturais', 'apenas', 'usando', 'para'
    }
    
    # Filtrar keywords e variáveis vazias
    observed_vars = {var for var in observed_vars if var.lower() not in sem_keywords}
    
    # Imprimir as variáveis encontradas para diagnóstico
    print(f"DEBUG: Variáveis extraídas: {observed_vars}")
    
    return observed_vars

def run_sem_model(df_cleaned, model_name, model_spec):
    """
    Executa um modelo SEM específico e retorna os resultados.
    
    Args:
        df_cleaned: DataFrame com dados limpos
        model_name: Nome do modelo para fins de log
        model_spec: Especificação do modelo em formato semopy
        
    Returns:
        Dicionário com resultados do modelo ou None se falhar
    """
    print(f"\n{'='*80}")
    print(f"Executando modelo SEM: {model_name}")
    print(f"{'='*80}")
    
    try:
        # Criar instância do modelo
        sem_model = semopy.Model(model_spec)
        
        # Extrair variáveis necessárias
        cols_for_model = extract_vars_from_sem_spec(model_spec)
        print(f"Variáveis necessárias para o modelo: {sorted(list(cols_for_model))}")
        
        # Verificar se todas as colunas estão disponíveis
        missing_cols = [col for col in cols_for_model if col not in df_cleaned.columns]
        if missing_cols:
            print(f"ERRO: Colunas ausentes no DataFrame: {missing_cols}")
            return None
        
        # Criar subset de dados apenas com as colunas necessárias
        data_for_model = df_cleaned[list(cols_for_model)].copy()
        
        # Pré-processar variáveis categóricas - mostrar estatísticas
        categorical_cols = data_for_model.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            print(f"\nVariáveis categóricas no modelo: {list(categorical_cols)}")
            print("Convertendo variáveis categóricas para formatos numéricos...")
            
            for col in categorical_cols:
                # Mostrar valores únicos para debug
                unique_vals = data_for_model[col].dropna().unique()
                print(f"  {col}: {len(unique_vals)} valores únicos - {unique_vals[:5]}...")
                
                # MELHORIA: Usar codificação ordinal mais robusta para variáveis categóricas
                # Em vez de tentar converter para numérico diretamente (o que causa falhas),
                # sempre usar codificação ordinal para variáveis categóricas
                if len(unique_vals) > 0:  # Certifica-se que existe pelo menos um valor não-nulo
                    values = data_for_model[col].dropna().unique()
                    value_map = {val: idx+1 for idx, val in enumerate(values)}
                    data_for_model[col] = data_for_model[col].map(value_map)
                    print(f"  {col}: Aplicada codificação ordinal - mapeamento: {value_map}")
                else:
                    print(f"  {col}: Sem valores únicos não-nulos, preenchendo com 0.")
                    data_for_model[col] = 0
        
        # MELHORIA: Converter todas as colunas para numérico com tratamento mais robusto
        for col in data_for_model.columns:
            # Tentar converter para numérico, se falhar, preencher com valores ausentes
            try:
                data_for_model[col] = pd.to_numeric(data_for_model[col], errors='coerce')
                # Preencher valores ausentes com a média da coluna ou 0 se não houver média
                if data_for_model[col].isna().any():
                    fill_value = data_for_model[col].mean()
                    if pd.isna(fill_value):
                        fill_value = 0
                    data_for_model[col] = data_for_model[col].fillna(fill_value)
            except Exception as e:
                print(f"  Erro ao converter {col}: {e}")
                data_for_model[col] = data_for_model[col].astype('float64').fillna(0)
        
        # Verificar distribuição das colunas numéricas para debug
        for col in data_for_model.columns:
            unique_vals = data_for_model[col].unique()
            if len(unique_vals) < 10:  # Mostrar apenas para variáveis com poucos valores únicos
                print(f"Distribuição de {col}: {data_for_model[col].value_counts().head(5)}")
        
        # MELHORIA: Não remover linhas com valores ausentes, em vez disso, imputar valores
        orig_shape = data_for_model.shape
        # Verificar se há valores ausentes após o tratamento
        if data_for_model.isna().any().any():
            print("Ainda há valores ausentes após conversão, imputando com 0")
            data_for_model = data_for_model.fillna(0)
        
        print(f"Shape após tratamento: {data_for_model.shape}")
        
        # Verificar se há variáveis com variância zero (constantes)
        constant_cols = [col for col in data_for_model.columns if data_for_model[col].nunique(dropna=False) <= 1]
        if constant_cols:
            print(f"AVISO: Removendo colunas constantes: {constant_cols}")
            data_for_model.drop(columns=constant_cols, inplace=True)
        
        # Verificar se há dados suficientes
        if data_for_model.empty or len(data_for_model) < 10:  # MELHORIA: Ajustar limite para no mínimo 10 observações
            print(f"ERRO: Dados insuficientes para ajustar o modelo ({len(data_for_model)} linhas, {len(data_for_model.columns)} colunas).")
            return None
        
        # Ajustar o modelo
        print(f"Ajustando modelo com {len(data_for_model)} observações e {len(data_for_model.columns)} variáveis...")
        res = sem_model.fit(data_for_model, clean_slate=True)
        
        # Calcular estatísticas do modelo
        stats = semopy.calc_stats(sem_model)
        
        # Extrair params para tabela de resultados
        params = sem_model.inspect()
        
        # Criar dicionário de resultados
        results = {
            'model': sem_model,
            'fit_result': res,
            'stats': stats,
            'params': params,
            'data': data_for_model,
            'n_obs': len(data_for_model)
        }
        
        # Exibir resumo dos resultados
        print(f"\nResultados do modelo '{model_name}':")
        print(f"Convergência: {res}")
        
        # Verificar como as estatísticas são retornadas (pode variar conforme a versão do semopy)
        print("\nEstatísticas de ajuste:")
        if hasattr(stats, 'Tbl'):
            print(stats.Tbl)
        else:
            print(stats)  # Assumindo que stats é um DataFrame em versões mais recentes
        
        # Resumo dos parâmetros
        print("\nResumo dos parâmetros estimados:")
        if not params.empty:
            display_cols = ['lval', 'op', 'rval', 'Estimate']
            if all(col in params.columns for col in display_cols):
                print(params[display_cols].head(10))
                if len(params) > 10:
                    print(f"... e mais {len(params) - 10} parâmetros.")
            else:
                print("Formato de parâmetros inesperado, exibindo colunas disponíveis:")
                print(params.head(10))
        else:
            print("Nenhum parâmetro estimado retornado.")
        
        return results
        
    except Exception as e:
        print(f"ERRO ao executar modelo '{model_name}': {e}")
        import traceback
        traceback.print_exc()
        return None

def run_all_sem_models(df_cleaned):
    """
    Executa todos os modelos SEM definidos e retorna os resultados.
    
    Args:
        df_cleaned: DataFrame com dados limpos
        
    Returns:
        Dicionário com resultados de todos os modelos
    """
    results = {}
    
    # Executar cada modelo individualmente
    for model_name, model_spec in sem_models.items():
        print(f"\nProcessando modelo: {model_name}")
        model_result = run_sem_model(df_cleaned, model_name, model_spec)
        if model_result:
            results[model_name] = model_result
    
    return results

def create_results_directory():
    """Cria diretório para salvar resultados se não existir"""
    os.makedirs('resultados', exist_ok=True)
    os.makedirs('resultados/figuras', exist_ok=True)
    os.makedirs('resultados/tabelas', exist_ok=True)

def save_model_results_table(results, output_path="resultados/tabelas/resultados_modelos.txt"):
    """
    Salva os resultados dos modelos SEM em formato de tabela.
    
    Args:
        results: Dicionário com resultados dos modelos
        output_path: Caminho para salvar a tabela
    """
    if not results:
        print("Sem resultados para salvar.")
        return
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Escrever cabeçalho
        f.write("Resultados dos Modelos de Equações Estruturais (SEM)\n")
        f.write("="*80 + "\n\n")
        
        # Para cada modelo
        for model_name, model_results in results.items():
            if not model_results:
                continue
                
            f.write(f"Modelo: {model_name}\n")
            f.write("-"*80 + "\n")
            
            # Estatísticas de ajuste
            f.write("Estatísticas de Ajuste:\n")
            stats = model_results['stats']
            if hasattr(stats, 'Tbl'):
                f.write(str(stats.Tbl) + "\n\n")
            else:
                f.write(str(stats) + "\n\n")
            
            # Parâmetros do modelo
            f.write("Parâmetros Estimados:\n")
            params = model_results['params']
            
            # Formatar parâmetros em uma tabela
            param_rows = []
            for _, row in params.iterrows():
                # Verifica se o valor é numérico antes de formatar
                try:
                    estimate = f"{float(row['Estimate']):.4f}" if pd.notnull(row['Estimate']) else ''
                    std_err = f"{float(row['Std. Err']):.4f}" if 'Std. Err' in row and pd.notnull(row['Std. Err']) else ''
                    t_value = f"{float(row['t-value']):.4f}" if 't-value' in row and pd.notnull(row['t-value']) else ''
                    p_value = f"{float(row['p-value']):.4f}" if 'p-value' in row and pd.notnull(row['p-value']) else ''
                except (ValueError, TypeError):
                    # Se não for possível converter para float, use o valor direto
                    estimate = str(row['Estimate']) if pd.notnull(row['Estimate']) else ''
                    std_err = str(row['Std. Err']) if 'Std. Err' in row and pd.notnull(row['Std. Err']) else ''
                    t_value = str(row['t-value']) if 't-value' in row and pd.notnull(row['t-value']) else ''
                    p_value = str(row['p-value']) if 'p-value' in row and pd.notnull(row['p-value']) else ''
                
                param_rows.append([
                    row['lval'] if 'lval' in row else '',
                    row['op'] if 'op' in row else '',
                    row['rval'] if 'rval' in row else '',
                    estimate,
                    std_err,
                    t_value,
                    p_value
                ])
            
            # Escrever cabeçalho da tabela
            f.write(f"{'lval':<15} {'op':<5} {'rval':<15} {'Estimate':<10} {'Std. Err':<10} {'t-value':<10} {'p-value':<10}\n")
            f.write("-"*80 + "\n")
            
            # Escrever linhas da tabela
            for row in param_rows:
                f.write(f"{row[0]:<15} {row[1]:<5} {row[2]:<15} {row[3]:<10} {row[4]:<10} {row[5]:<10} {row[6]:<10}\n")
            
            f.write("\n" + "="*80 + "\n\n")
    
    print(f"Resultados salvos em: {output_path}")

def plot_sem_model_fit(results, output_dir="resultados/figuras"):
    """
    Cria gráficos de barras para comparar o ajuste entre os modelos.
    
    Args:
        results: Dicionário com resultados dos modelos
        output_dir: Diretório para salvar os gráficos
    """
    if not results:
        print("Sem resultados para plotar.")
        return
    
    # Extrair métricas de ajuste de cada modelo
    models = []
    cfi_values = []
    tli_values = []
    rmsea_values = []
    srmr_values = []
    
    for model_name, model_result in results.items():
        if not model_result:
            continue
            
        stats = model_result['stats']
        
        # CORREÇÃO: Extrair métricas com manipulação segura
        try:
            # Extrair métricas com tratamento adequado para diferentes formatos de output
            if hasattr(stats, 'CFI'):
                cfi = float(stats.CFI) if not pd.isna(stats.CFI) else 0
            elif isinstance(stats, pd.DataFrame) and 'CFI' in stats.columns:
                cfi = float(stats['CFI'].iloc[0]) if not pd.isna(stats['CFI'].iloc[0]) else 0
            else:
                cfi = 0
                
            if hasattr(stats, 'TLI'):
                tli = float(stats.TLI) if not pd.isna(stats.TLI) else 0
            elif isinstance(stats, pd.DataFrame) and 'TLI' in stats.columns:
                tli = float(stats['TLI'].iloc[0]) if not pd.isna(stats['TLI'].iloc[0]) else 0
            else:
                tli = 0
                
            if hasattr(stats, 'RMSEA'):
                rmsea = float(stats.RMSEA) if not pd.isna(stats.RMSEA) else 0
            elif isinstance(stats, pd.DataFrame) and 'RMSEA' in stats.columns:
                rmsea = float(stats['RMSEA'].iloc[0]) if not pd.isna(stats['RMSEA'].iloc[0]) else 0
            else:
                rmsea = 0
                
            if hasattr(stats, 'SRMR'):
                srmr = float(stats.SRMR) if not pd.isna(stats.SRMR) else 0
            elif isinstance(stats, pd.DataFrame) and 'SRMR' in stats.columns:
                srmr = float(stats['SRMR'].iloc[0]) if not pd.isna(stats['SRMR'].iloc[0]) else 0
            else:
                srmr = 0
            
            models.append(model_name)
            cfi_values.append(cfi)
            tli_values.append(tli)
            rmsea_values.append(rmsea)
            srmr_values.append(srmr)
            
        except Exception as e:
            print(f"Erro ao extrair métricas para {model_name}: {e}")
    
    # Se não tiver dados suficientes, sair da função
    if len(models) == 0:
        print("Sem dados suficientes para criar gráficos de ajuste.")
        return
    
    # Criar dataframe com métricas
    metrics_df = pd.DataFrame({
        'Modelo': models,
        'CFI': cfi_values,
        'TLI': tli_values,
        'RMSEA': rmsea_values,
        'SRMR': srmr_values
    })
    
    try:
        # Criar gráfico
        plt.figure(figsize=(12, 8))
        
        # Configurar barras
        x = np.arange(len(models))
        width = 0.2
        
        # Plotar cada métrica
        plt.bar(x - width*1.5, metrics_df['CFI'], width, label='CFI')
        plt.bar(x - width/2, metrics_df['TLI'], width, label='TLI')
        plt.bar(x + width/2, metrics_df['RMSEA'], width, label='RMSEA')
        plt.bar(x + width*1.5, metrics_df['SRMR'], width, label='SRMR')
        
        # Adicionar linhas de referência para valores ideais
        plt.axhline(y=0.95, color='g', linestyle='--', alpha=0.5, label='CFI/TLI > 0.95 (bom)')
        plt.axhline(y=0.90, color='y', linestyle='--', alpha=0.5, label='CFI/TLI > 0.90 (aceitável)')
        plt.axhline(y=0.05, color='r', linestyle='--', alpha=0.5, label='RMSEA/SRMR < 0.05 (bom)')
        plt.axhline(y=0.08, color='orange', linestyle='--', alpha=0.5, label='RMSEA/SRMR < 0.08 (aceitável)')
        
        # Configurar eixos e legendas
        plt.xlabel('Modelo')
        plt.ylabel('Valor')
        plt.title('Métricas de Ajuste dos Modelos SEM')
        plt.xticks(x, models, rotation=45, ha='right')
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Salvar figura
        output_path = os.path.join(output_dir, 'metricas_ajuste_modelos.png')
        plt.savefig(output_path)
        plt.close()
        
        print(f"Gráfico de métricas de ajuste salvo em: {output_path}")
    except Exception as e:
        print(f"Erro ao criar gráfico de ajuste: {e}")
        import traceback
        traceback.print_exc()

def plot_latent_variable_loadings(results, output_dir="resultados/figuras"):
    """
    Cria gráficos das cargas fatoriais para cada variável latente.
    
    Args:
        results: Dicionário com resultados dos modelos
        output_dir: Diretório para salvar os gráficos
    """
    if not results:
        print("Sem resultados para plotar cargas fatoriais.")
        return
    
    # Para cada modelo
    for model_name, model_result in results.items():
        if not model_result:
            continue
            
        params = model_result['params']
        
        # Filtrar apenas relações de medição (=~)
        measurement_params = params[params['op'] == '=~']
        
        # Obter variáveis latentes únicas
        latent_vars = measurement_params['lval'].unique()
        
        for latent in latent_vars:
            # Filtrar parâmetros para esta variável latente
            latent_params = measurement_params[measurement_params['lval'] == latent]
            
            # Ordenar por valor estimado para melhor visualização
            latent_params = latent_params.sort_values('Estimate', ascending=False)
            
            # Criar gráfico
            plt.figure(figsize=(10, max(6, len(latent_params) * 0.4)))
            
            # Barras horizontais para cargas fatoriais
            plt.barh(latent_params['rval'], latent_params['Estimate'])
            
            # Adicionar valores nas barras
            for i, v in enumerate(latent_params['Estimate']):
                plt.text(max(v + 0.02, 0.1), i, f"{v:.2f}", va='center')
            
            # Configurar eixos e título
            plt.xlabel('Carga Fatorial')
            plt.ylabel('Variável Observada')
            plt.title(f'Cargas Fatoriais para {latent} ({model_name})')
            plt.grid(axis='x', alpha=0.3)
            plt.xlim(0, 1.1)
            plt.tight_layout()
            
            # Salvar figura
            safe_latent_name = latent.replace(' ', '_')
            output_path = os.path.join(output_dir, f'cargas_{model_name}_{safe_latent_name}.png')
            plt.savefig(output_path)
            plt.close()
            
            print(f"Gráfico de cargas para {latent} salvo em: {output_path}")

def plot_path_diagram(results, output_dir="resultados/figuras"):
    """
    Cria diagramas de caminho (path diagrams) para os modelos SEM.
    
    Args:
        results: Dicionário com resultados dos modelos
        output_dir: Diretório para salvar os diagramas
    """
    if not results:
        print("Sem resultados para criar diagramas de caminho.")
        return
    
    # MELHORIA: Verificar se graphviz está disponível
    try:
        import importlib
        graphviz_spec = importlib.util.find_spec("graphviz")
        graphviz_available = graphviz_spec is not None
        if not graphviz_available:
            print("AVISO: Módulo graphviz não está instalado. Diagramas de caminho não serão gerados.")
            print("Para instalar, execute: pip install graphviz")
            return
    except Exception:
        print("AVISO: Não foi possível verificar se o módulo graphviz está instalado.")
        print("Se os diagramas não forem gerados, instale com: pip install graphviz")
    
    for model_name, model_result in results.items():
        if not model_result:
            continue
            
        try:
            # Criar figura para o diagrama
            plt.figure(figsize=(12, 10))
            
            # Gerar diagrama de caminho
            semopy.semplot(model_result['model'], "resultados/figuras/temp_dot_file.dot", 
                           plot_covs=True, std_ests=True)
            
            # Salvar figura final
            output_path = os.path.join(output_dir, f'diagrama_{model_name.replace(" ", "_")}.png')
            plt.savefig(output_path)
            plt.close()
            
            print(f"Diagrama de caminho para {model_name} salvo em: {output_path}")
            
        except Exception as e:
            print(f"Erro ao criar diagrama para {model_name}: {e}")
            if "No graphviz module is installed" in str(e):
                print("Para instalar graphviz, execute: pip install graphviz")

def analyze_factors_by_sociodemographics(df, results, output_dir="resultados/figuras"):
    """
    Analisa fatores latentes por variáveis sociodemográficas.
    
    Args:
        df: DataFrame com dados completos
        results: Dicionário com resultados dos modelos
        output_dir: Diretório para salvar os gráficos
    """
    # Verificar se temos o modelo global
    if 'Modelo Global' not in results or not results['Modelo Global']:
        print("Modelo Global não disponível para análise sociodemográfica.")
        return
    
    # Extrair fatores latentes do modelo global
    global_model = results['Modelo Global']['model']
    global_data = results['Modelo Global']['data']
    
    try:
        # Estimar scores dos fatores latentes
        latent_scores = global_model.predict(global_data)
        
        # Adicionar scores ao DataFrame original
        df_with_scores = global_data.copy()
        for col in latent_scores.columns:
            df_with_scores[col] = latent_scores[col]
        
        # Adicionar variáveis sociodemográficas (assumindo que estão no DataFrame original)
        sociodem_vars = ['genero', 'idade_faixa', 'escolaridade', 'renda_faixa']
        
        # Verificar quais variáveis sociodemográficas estão disponíveis
        available_sociodem = [var for var in sociodem_vars if var in df.columns]
        
        if not available_sociodem:
            print("Nenhuma variável sociodemográfica disponível para análise.")
            return
        
        # Criar ID único para juntar DataFrames
        df['temp_id'] = range(len(df))
        df_with_scores['temp_id'] = range(len(df_with_scores))
        
        # Juntar scores com variáveis sociodemográficas
        merged_df = pd.merge(
            df_with_scores, 
            df[['temp_id'] + available_sociodem],
            on='temp_id',
            how='inner'
        )
        
        # Para cada variável sociodemográfica disponível
        for socio_var in available_sociodem:
            # Para cada fator latente
            for latent_var in latent_scores.columns:
                try:
                    # Criar boxplot
                    plt.figure(figsize=(12, 6))
                    
                    # Ordenar categorias se possível (para idade, renda, etc.)
                    categories = merged_df[socio_var].unique()
                    if socio_var == 'idade_faixa' or socio_var == 'renda_faixa':
                        # Tentar ordenar por faixa numérica extraída (e.g., "18-25" -> 18)
                        def extract_first_number(s):
                            match = re.search(r'(\d+)', str(s))
                            return int(match.group(1)) if match else 0
                        categories = sorted(categories, key=extract_first_number)
                    
                    # Criar boxplot
                    sns.boxplot(x=socio_var, y=latent_var, data=merged_df, order=categories)
                    
                    # Adicionar pontos individuais (jitter para evitar sobreposição)
                    sns.stripplot(x=socio_var, y=latent_var, data=merged_df, 
                                 order=categories, color='black', alpha=0.2, size=3, jitter=True)
                    
                    # Configurar eixos e título
                    plt.title(f'{latent_var} por {socio_var}')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    
                    # Realizar ANOVA para testar diferenças entre grupos
                    categories = merged_df[socio_var].dropna().unique()
                    if len(categories) > 1:  # Precisa de pelo menos 2 grupos para ANOVA
                        groups = [merged_df[merged_df[socio_var] == cat][latent_var].dropna() for cat in categories]
                        valid_groups = [g for g in groups if len(g) > 0]
                        
                        if len(valid_groups) > 1:
                            f_stat, p_val = stats.f_oneway(*valid_groups)
                            plt.annotate(f'ANOVA: F={f_stat:.2f}, p={p_val:.4f}', 
                                        xy=(0.02, 0.96), xycoords='axes fraction',
                                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
                    
                    # Salvar figura
                    output_path = os.path.join(output_dir, f'{latent_var}_por_{socio_var}.png')
                    plt.savefig(output_path)
                    plt.close()
                    
                    print(f"Análise de {latent_var} por {socio_var} salva em: {output_path}")
                    
                except Exception as e:
                    print(f"Erro ao analisar {latent_var} por {socio_var}: {e}")
        
    except Exception as e:
        print(f"Erro na análise sociodemográfica: {e}")
        import traceback
        traceback.print_exc() 

# Adicionar função para análise Mixed Logit
def run_mixed_logit_analysis(df_cleaned, output_dir="resultados/tabelas"):
    """
    Executa análise Mixed Logit para modelar a escolha de transporte e
    a disposição a pagar por diferentes recompensas.
    
    Args:
        df_cleaned: DataFrame com dados limpos
        output_dir: Diretório para salvar os resultados
    """
    print("\n--- Executando Análise Mixed Logit ---")
    
    try:
        # Variáveis para análise Mixed Logit
        # 1. Disposição a pagar por passes diários
        formula_diario = "aceit_pagar_ate_10_dia ~ util_frequencia_uso_tp + renda_faixa + idade_faixa + genero"
        
        # 2. Disposição a pagar por passes mensais
        formula_mensal = "aceit_pagar_150_200_mes ~ util_frequencia_uso_tp + renda_faixa + idade_faixa + genero"
        
        # 3. Disposição a aceitar recompensa por quilômetro
        formula_km = "aceit_receber_50cent_km ~ util_frequencia_uso_tp + renda_faixa + idade_faixa + genero"
        
        # Dicionário para armazenar resultados
        results = {}
        
        # Preparar dados para análise com tratamento robusto
        df_analysis = df_cleaned.copy()
        
        # MELHORIA: Tratamento mais robusto para variáveis categóricas
        for col in ['util_frequencia_uso_tp', 'renda_faixa', 'idade_faixa', 'genero']:
            if col in df_analysis.columns:
                if df_analysis[col].dtype == 'object':
                    # Substituir NaN por categoria "Desconhecido"
                    df_analysis[col] = df_analysis[col].fillna('Desconhecido')
                    
                    # Verificar se precisamos codificar
                    if len(df_analysis[col].unique()) > 10:  # Muitas categorias, usar one-hot
                        print(f"Aplicando one-hot encoding para {col} (muitas categorias)")
                        dummies = pd.get_dummies(df_analysis[col], prefix=col, drop_first=True)
                        df_analysis = pd.concat([df_analysis, dummies], axis=1)
                        formula_diario = formula_diario.replace(col, " + ".join(dummies.columns))
                        formula_mensal = formula_mensal.replace(col, " + ".join(dummies.columns))
                        formula_km = formula_km.replace(col, " + ".join(dummies.columns))
                    else:  # Poucas categorias, usar codificação ordinal
                        print(f"Aplicando codificação ordinal para {col}")
                        categories = df_analysis[col].unique()
                        mapping = {cat: i for i, cat in enumerate(categories)}
                        df_analysis[col + '_coded'] = df_analysis[col].map(mapping)
                        formula_diario = formula_diario.replace(col, col + '_coded')
                        formula_mensal = formula_mensal.replace(col, col + '_coded')
                        formula_km = formula_km.replace(col, col + '_coded')
        
        # Preparar target para análise logit
        for col in ['aceit_pagar_ate_10_dia', 'aceit_pagar_150_200_mes', 'aceit_receber_50cent_km']:
            if col in df_analysis.columns:
                # Converter para binário (1 = concorda, 0 = não concorda)
                df_analysis[col+'_bin'] = df_analysis[col].apply(lambda x: 1 if x >= 4 else 0)
        
        # MELHORIA: Usar tratamento de exceções mais específico para cada modelo
        for formula, name in zip(
            [formula_diario, formula_mensal, formula_km],
            ["Disposição a Pagar Diário", "Disposição a Pagar Mensal", "Disposição a Aceitar por KM"]
        ):
            try:
                # Extrair variável dependente do nome da fórmula
                dep_var = formula.split('~')[0].strip()
                
                # Criar variável binária se não existir
                bin_var = dep_var+'_bin'
                if bin_var not in df_analysis.columns:
                    print(f"Variável {bin_var} não encontrada para {name}, pulando...")
                    continue
                
                # Modificar fórmula para usar variável binária
                formula_bin = formula.replace(dep_var, bin_var)
                
                # MELHORIA: Extrair colunas da fórmula de forma mais robusta
                import re
                pattern = r'([a-zA-Z0-9_]+)'
                cols_needed = re.findall(pattern, formula_bin)
                cols_needed = [c.strip() for c in cols_needed if c.strip() and c.strip() not in ['~', '+', '-', '*', '/', '(', ')']]
                
                # Verificar se todas as colunas existem
                missing_cols = [c for c in cols_needed if c not in df_analysis.columns]
                if missing_cols:
                    print(f"Colunas ausentes para análise de {name}: {missing_cols}")
                    continue
                
                # Criar subset de dados sem valores ausentes
                data_subset = df_analysis[cols_needed].copy()
                
                # Imputar valores ausentes com a média (numérico) ou modo (categórico)
                for col in data_subset.columns:
                    if data_subset[col].dtype in ['int64', 'float64']:
                        if data_subset[col].isna().any():
                            fill_value = data_subset[col].mean()
                            if pd.isna(fill_value):
                                fill_value = 0
                            data_subset[col] = data_subset[col].fillna(fill_value)
                    else:
                        if data_subset[col].isna().any():
                            fill_value = data_subset[col].mode().iloc[0] if not data_subset[col].mode().empty else "MISSING"
                            data_subset[col] = data_subset[col].fillna(fill_value)
                
                print(f"Dados para análise Mixed Logit de {name}: {data_subset.shape}")
                
                if len(data_subset) < 30:  # Verificar se há dados suficientes
                    print(f"Dados insuficientes para análise Mixed Logit de {name}")
                    continue
                
                # Verificar se há variação na variável dependente
                dep_var_values = data_subset[bin_var].unique()
                if len(dep_var_values) <= 1:
                    print(f"Sem variação na variável dependente para {name}: {dep_var_values}")
                    continue
                
                # MELHORIA: Verificar colinearidade extrema
                from statsmodels.stats.outliers_influence import variance_inflation_factor
                from statsmodels.tools.tools import add_constant
                
                # Preparar X para verificação VIF
                X = data_subset.drop(columns=[bin_var])
                
                # Verificar por variáveis constantes
                constant_cols = [col for col in X.columns if X[col].nunique() <= 1]
                if constant_cols:
                    print(f"Removendo colunas constantes para {name}: {constant_cols}")
                    X = X.drop(columns=constant_cols)
                
                # Se não sobrar nenhuma variável, pular
                if X.empty:
                    print(f"Sem variáveis independentes para análise de {name}")
                    continue
                
                try:
                    # Adicionar constante
                    X_with_const = add_constant(X)
                    
                    # Calcular VIF para cada variável
                    vif = pd.DataFrame()
                    vif["Variável"] = X_with_const.columns
                    vif["VIF"] = [variance_inflation_factor(X_with_const.values, i) for i in range(X_with_const.shape[1])]
                    
                    # Identificar variáveis com alta multicolinearidade
                    high_vif = vif[vif["VIF"] > 10].sort_values(by="VIF", ascending=False)
                    if not high_vif.empty:
                        print(f"Variáveis com alta multicolinearidade para {name}:")
                        print(high_vif)
                        
                        # Remover variáveis com VIF extremo (>30), mantendo pelo menos uma variável por categoria
                        extreme_vif_vars = high_vif[high_vif["VIF"] > 30]["Variável"].tolist()
                        if 'const' in extreme_vif_vars:
                            extreme_vif_vars.remove('const')
                        
                        if extreme_vif_vars:
                            print(f"Removendo variáveis com VIF extremo: {extreme_vif_vars}")
                            X = X.drop(columns=[col for col in extreme_vif_vars if col in X.columns])
                            
                            # Atualizar fórmula
                            formula_bin = bin_var + " ~ " + " + ".join(X.columns)
                except Exception as e:
                    print(f"Erro ao calcular VIF para {name}: {e}")
                    # Continuar sem verificação VIF
                
                # Ajustar modelo logit com tratamento para singularidade
                from statsmodels.tools.sm_exceptions import PerfectSeparationError
                
                try:
                    # Preparar dados para modelagem
                    y = data_subset[bin_var]
                    X = data_subset.drop(columns=[bin_var])
                    
                    # Adicionar constante se não existir
                    if 'const' not in X.columns:
                        X = add_constant(X)
                    
                    # Usar fit_regularized para lidar com separação perfeita
                    import statsmodels.api as sm
                    model = sm.Logit(y, X)
                    
                    try:
                        # Primeiro tentar ajuste normal
                        result = model.fit(disp=0, maxiter=100)
                    except PerfectSeparationError:
                        print(f"Perfeita separação detectada para {name}, usando ajuste regularizado (L1)")
                        result = model.fit_regularized(method='l1', alpha=0.01, disp=0, maxiter=100)
                    except Exception:
                        print(f"Erro no ajuste normal para {name}, usando ajuste regularizado (L1)")
                        result = model.fit_regularized(method='l1', alpha=0.01, disp=0, maxiter=100)
                    
                    # Armazenar resultado
                    results[name] = result
                    
                    print(f"\nResultado da análise Mixed Logit para {name}:")
                    print(result.summary().tables[1])
                    
                except Exception as e:
                    print(f"Erro na análise Mixed Logit para {name}: {e}")
                    import traceback
                    traceback.print_exc()
            
            except Exception as e:
                print(f"Erro ao preparar dados para {name}: {e}")
                import traceback
                traceback.print_exc()
        
        # Salvar resultados
        if results:
            output_path = os.path.join(output_dir, "resultados_mixed_logit.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("RESULTADOS DA ANÁLISE MIXED LOGIT\n")
                f.write("================================\n\n")
                
                for name, model_result in results.items():
                    f.write(f"Modelo: {name}\n")
                    f.write("-"*50 + "\n")
                    f.write(str(model_result.summary()) + "\n\n")
                    f.write("="*50 + "\n\n")
            
            print(f"Resultados da análise Mixed Logit salvos em: {output_path}")
            
            return results
    
    except Exception as e:
        print(f"Erro geral na análise Mixed Logit: {e}")
        import traceback
        traceback.print_exc()
    
    return None

# Aprimorar a função de plotagem para incluir tratamento de erros
def plot_loadings(results, output_dir="resultados/figuras"):
    """
    Gera gráficos de cargas fatoriais para todos os modelos.
    
    Args:
        results: Dicionário com resultados dos modelos SEM
        output_dir: Diretório para salvar os gráficos
    """
    if not results:
        print("Sem resultados para criar gráficos de cargas fatoriais.")
        return
    
    # Garantir que o diretório de saída existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Contador de gráficos criados com sucesso
    successful_plots = 0
    
    print("\nGerando gráficos de cargas fatoriais...")
    
    for nome_modelo, resultado in results.items():
        try:
            if 'params' not in resultado or resultado['params'] is None or resultado['params'].empty:
                print(f"Aviso: Não há parâmetros disponíveis para o modelo '{nome_modelo}'")
                continue
                
            params = resultado['params']
            
            # CORREÇÃO: Filtrar corretamente as cargas fatoriais
            # Verificar se a coluna 'op' existe
            if 'op' not in params.columns:
                print(f"Aviso: Coluna 'op' não encontrada nos parâmetros do modelo '{nome_modelo}'")
                continue
            
            # Filtrar apenas relações de medida (=~)
            loadings = params[params['op'] == '=~'].copy()
            
            if loadings.empty:
                print(f"Aviso: Nenhuma carga fatorial encontrada para o modelo '{nome_modelo}'")
                continue
            
            # Obter fatores latentes únicos
            if 'lval' not in loadings.columns:
                print(f"Aviso: Coluna 'lval' não encontrada nos parâmetros do modelo '{nome_modelo}'")
                continue
                
            latentes = loadings['lval'].unique()
            
            for latente in latentes:
                try:
                    # Filtrar para um fator específico
                    cargas = loadings[loadings['lval'] == latente].copy()
                    
                    if cargas.empty:
                        print(f"Aviso: Nenhuma carga encontrada para o fator '{latente}' no modelo '{nome_modelo}'")
                        continue
                    
                    # Verificar se temos as colunas necessárias
                    required_cols = ['rval', 'Estimate']
                    if not all(col in cargas.columns for col in required_cols):
                        print(f"Aviso: Colunas necessárias {required_cols} não encontradas para o fator '{latente}'")
                        continue
                    
                    # Garantir que as estimativas sejam numéricas
                    try:
                        cargas['Estimate'] = pd.to_numeric(cargas['Estimate'], errors='coerce')
                        # Preencher valores não numéricos com 0
                        cargas['Estimate'] = cargas['Estimate'].fillna(0)
                    except Exception as e:
                        print(f"Erro ao converter estimativas para números no fator '{latente}': {e}")
                        continue
                    
                    # Ordenar por magnitude da carga
                    cargas = cargas.sort_values('Estimate', ascending=False)
                    
                    # Criar figura com tamanho adaptativo baseado no número de variáveis
                    plt.figure(figsize=(10, max(6, len(cargas) * 0.5)))
                    
                    # Criar gráfico de barras horizontais para as cargas
                    bars = plt.barh(cargas['rval'], cargas['Estimate'])
                    
                    # Adicionar valores nas barras
                    for i, bar in enumerate(bars):
                        plt.text(
                            max(bar.get_width() + 0.02, 0.1),
                            bar.get_y() + bar.get_height()/2,
                            f"{cargas['Estimate'].iloc[i]:.2f}",
                            va='center'
                        )
                    
                    # Definir limites e título
                    plt.xlim(0, max(1.0, cargas['Estimate'].max() * 1.2))
                    plt.xlabel('Carga Fatorial')
                    plt.ylabel('Indicador')
                    plt.title(f'Cargas Fatoriais: {latente} ({nome_modelo})')
                    plt.grid(axis='x', alpha=0.3)
                    plt.tight_layout()
                    
                    # Salvar figura
                    safe_name = f"{nome_modelo.replace(' ', '_')}_{latente.replace(' ', '_')}"
                    output_path = os.path.join(output_dir, f"{safe_name}.png")
                    
                    try:
                        plt.savefig(output_path, dpi=300)
                        successful_plots += 1
                        print(f"Gráfico salvo em: {output_path}")
                    except Exception as e:
                        print(f"Erro ao salvar gráfico para {latente} em {nome_modelo}: {e}")
                    
                    plt.close()
                    
                except Exception as e:
                    print(f"Erro ao processar fator '{latente}' no modelo '{nome_modelo}': {e}")
                    import traceback
                    traceback.print_exc()
            
        except Exception as e:
            print(f"Erro ao processar modelo '{nome_modelo}': {e}")
            import traceback
            traceback.print_exc()
    
    if successful_plots > 0:
        print(f"\nGerados {successful_plots} gráficos de cargas fatoriais com sucesso.")
    else:
        print("\nAVISO: Nenhum gráfico de cargas fatoriais foi gerado com sucesso.")

print("DEBUG: Definições de funções concluídas. Entrando no bloco principal...") # DEBUG PRINT 3

# --- Bloco Principal de Execução ---
if __name__ == '__main__':
    print("DEBUG: Dentro do bloco if __name__ == '__main__'") # DEBUG PRINT 4
    print("Iniciando script de análise de transporte...")
    
    # 1. Carregamento dos dados
    df_raw = load_data()
    
    if df_raw is not None:
        # 2. Limpeza e preparação
        df_cleaned = clean_data(df_raw.copy())
        
        if df_cleaned is not None:
            print("\nInformações do DataFrame limpo (primeiras linhas e tipos):")
            print(df_cleaned.head(2))
            print(df_cleaned.dtypes.to_string())
            
            # Criar diretório para resultados
            create_results_directory()
            
            # 3. Executar modelos SEM individualmente
            try:
                print("\n--- Executando Modelos SEM Individualmente ---")
                results = {}
                
                # Lista de modelos para testar - agora incluindo todos os modelos definidos
                for model_name, model_spec in sem_models.items():
                    print(f"\nProcessando modelo: {model_name}")
                    model_result = run_sem_model(df_cleaned, model_name, model_spec)
                    if model_result:
                        results[model_name] = model_result
                
                # 4. Executar análise Mixed Logit
                mixed_logit_results = run_mixed_logit_analysis(df_cleaned)
                
                # 5. Gerar resultados e visualizações
                if results:
                    print("\n--- Gerando Resultados ---")
                    
                    # Salvar tabelas de resultados
                    save_model_results_table(results)
                    
                    # Gerar visualizações com tratamento de exceções
                    try:
                        # Gráficos de ajuste do modelo
                        plot_sem_model_fit(results)
                    except Exception as e:
                        print(f"Erro ao gerar gráficos de ajuste do modelo: {e}")
                    
                    try:
                        # Gráficos de cargas fatoriais
                        plot_loadings(results)
                    except Exception as e:
                        print(f"Erro ao gerar gráficos de cargas fatoriais: {e}")
                    
                    try:
                        # Diagramas de caminho
                        plot_path_diagram(results)
                    except Exception as e:
                        print(f"Erro ao gerar diagramas de caminho: {e}")
                    
                    try:
                        # Análise por fatores sociodemográficos (apenas para modelo global)
                        analyze_factors_by_sociodemographics(df_cleaned, results)
                    except Exception as e:
                        print(f"Erro ao realizar análise sociodemográfica: {e}")
                    
                    print("\nAnálise completa! Resultados salvos no diretório 'resultados/'.")
                else:
                    print("\nAVISO: Nenhum modelo SEM foi ajustado com sucesso.")
                
            except Exception as e:
                print(f"\nERRO durante a análise: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("ERRO: A limpeza de dados falhou.")
    else:
        print("ERRO: Falha ao carregar os dados.")

    print("\nScript de análise concluído.") 

# Adicionar função para visualizar e resumir resultados do modelo global
def visualize_global_model_results(results, output_dir="resultados/figuras"):
    """
    Cria visualizações específicas para o modelo global, destacando
    os relacionamentos mais importantes.
    
    Args:
        results: Dicionário com resultados dos modelos SEM
        output_dir: Diretório para salvar visualizações
    """
    # Verificar se o modelo global existe
    if 'Modelo Global' not in results or not results['Modelo Global']:
        print("Modelo Global não disponível para visualização.")
        return
    
    global_model = results['Modelo Global']
    params = global_model['params']
    
    try:
        # 1. Criar gráfico do modelo estrutural (relações entre variáveis latentes)
        plt.figure(figsize=(10, 6))
        
        # Filtrar relações entre variáveis latentes
        structural_relations = params[(params['op'] == '~') & 
                                      (params['lval'].str[0].str.isupper()) & 
                                      (params['rval'].str[0].str.isupper())]
        
        if not structural_relations.empty:
            # Preparar dados para gráfico
            relations = []
            estimates = []
            
            for _, row in structural_relations.iterrows():
                relations.append(f"{row['lval']} ← {row['rval']}")
                estimates.append(float(row['Estimate']))
            
            # Criar gráfico de barras horizontais
            plt.barh(relations, estimates, color='skyblue')
            
            # Adicionar valores nas barras
            for i, v in enumerate(estimates):
                plt.text(max(v + 0.02, 0.1), i, f"{v:.2f}", va='center')
            
            # Configurar eixos e título
            plt.xlabel('Estimativa do Coeficiente')
            plt.title('Relações Estruturais no Modelo Global')
            plt.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            
            # Salvar gráfico
            output_path = os.path.join(output_dir, 'modelo_global_estrutural.png')
            plt.savefig(output_path)
            plt.close()
            
            print(f"Gráfico de relações estruturais salvo em: {output_path}")
        
        # 2. Criar resumo visual das relações mais importantes
        plt.figure(figsize=(12, 10))
        
        try:
            # Usar networkx para criar gráfico direcionado
            import networkx as nx
            from matplotlib.patches import FancyArrowPatch
            
            # Criar grafo direcionado
            G = nx.DiGraph()
            
            # Adicionar nós (variáveis latentes)
            latent_vars = set(params[params['op'] == '~']['lval']) | set(params[params['op'] == '~']['rval'])
            latent_vars = [var for var in latent_vars if var[0].isupper()]
            
            for var in latent_vars:
                G.add_node(var)
            
            # Adicionar arestas (relações)
            for _, row in structural_relations.iterrows():
                G.add_edge(row['rval'], row['lval'], weight=float(row['Estimate']))
            
            # Definir posições dos nós
            pos = nx.spring_layout(G, seed=42)
            
            # Desenhar nós
            nx.draw_networkx_nodes(G, pos, node_size=5000, node_color='lightblue', alpha=0.8)
            
            # Desenhar arestas
            edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
            
            # Normalizar espessura
            max_width = 5
            min_width = 1
            if edge_weights:
                normalized_weights = [min_width + (w - min(edge_weights)) * (max_width - min_width) / 
                                     (max(edge_weights) - min(edge_weights)) if max(edge_weights) != min(edge_weights) 
                                     else max_width/2 for w in edge_weights]
            else:
                normalized_weights = []
            
            nx.draw_networkx_edges(G, pos, width=normalized_weights, alpha=0.7, 
                                  arrowsize=20, arrowstyle='->', edge_color='navy')
            
            # Adicionar rótulos
            nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
            
            # Adicionar pesos nas arestas
            edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges()}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
            
            plt.axis('off')
            plt.title('Diagrama de Relações do Modelo Global', fontsize=16)
            plt.tight_layout()
            
            # Salvar gráfico
            output_path = os.path.join(output_dir, 'modelo_global_diagrama.png')
            plt.savefig(output_path)
            plt.close()
            
            print(f"Diagrama de relações do modelo global salvo em: {output_path}")
            
        except ImportError:
            print("Biblioteca networkx não encontrada. Diagrama de rede não gerado.")
            print("Para instalar, execute: pip install networkx")
        
        # 3. Visualizar métricas de ajuste do modelo
        plt.figure(figsize=(8, 6))
        
        try:
            # Extrair métricas com tratamento adequado
            metrics = {}
            if hasattr(global_model['stats'], 'CFI'):
                metrics['CFI'] = float(global_model['stats'].CFI) if not pd.isna(global_model['stats'].CFI) else 0
            elif isinstance(global_model['stats'], pd.DataFrame) and 'CFI' in global_model['stats'].columns:
                metrics['CFI'] = float(global_model['stats']['CFI'].iloc[0]) if not pd.isna(global_model['stats']['CFI'].iloc[0]) else 0
            
            if hasattr(global_model['stats'], 'TLI'):
                metrics['TLI'] = float(global_model['stats'].TLI) if not pd.isna(global_model['stats'].TLI) else 0
            elif isinstance(global_model['stats'], pd.DataFrame) and 'TLI' in global_model['stats'].columns:
                metrics['TLI'] = float(global_model['stats']['TLI'].iloc[0]) if not pd.isna(global_model['stats']['TLI'].iloc[0]) else 0
            
            if hasattr(global_model['stats'], 'RMSEA'):
                metrics['RMSEA'] = float(global_model['stats'].RMSEA) if not pd.isna(global_model['stats'].RMSEA) else 0
            elif isinstance(global_model['stats'], pd.DataFrame) and 'RMSEA' in global_model['stats'].columns:
                metrics['RMSEA'] = float(global_model['stats']['RMSEA'].iloc[0]) if not pd.isna(global_model['stats']['RMSEA'].iloc[0]) else 0
            
            if hasattr(global_model['stats'], 'SRMR'):
                metrics['SRMR'] = float(global_model['stats'].SRMR) if not pd.isna(global_model['stats'].SRMR) else 0
            elif isinstance(global_model['stats'], pd.DataFrame) and 'SRMR' in global_model['stats'].columns:
                metrics['SRMR'] = float(global_model['stats']['SRMR'].iloc[0]) if not pd.isna(global_model['stats']['SRMR'].iloc[0]) else 0
            
            if metrics:
                # Criar gráfico de barras para métricas
                plt.bar(metrics.keys(), metrics.values(), color=['green', 'blue', 'red', 'orange'])
                
                # Adicionar líneas de referencia para valores ideales
                plt.axhline(y=0.95, color='g', linestyle='--', alpha=0.5, label='CFI/TLI > 0.95 (bom)')
                plt.axhline(y=0.90, color='y', linestyle='--', alpha=0.5, label='CFI/TLI > 0.90 (aceitável)')
                plt.axhline(y=0.05, color='r', linestyle='--', alpha=0.5, label='RMSEA/SRMR < 0.05 (bom)')
                plt.axhline(y=0.08, color='orange', linestyle='--', alpha=0.5, label='RMSEA/SRMR < 0.08 (aceitável)')
                
                # Adicionar valores encima das barras
                for i, (metric, value) in enumerate(metrics.items()):
                    plt.text(i, value + 0.02, f"{value:.3f}", ha='center')
                
                plt.ylim(0, max(max(metrics.values()) + 0.1, 1.0))
                plt.title('Métricas de Ajuste do Modelo Global')
                plt.legend()
                plt.grid(axis='y', alpha=0.3)
                plt.tight_layout()
                
                # Salvar gráfico
                output_path = os.path.join(output_dir, 'modelo_global_metricas.png')
                plt.savefig(output_path)
                plt.close()
                
                print(f"Gráfico de métricas de ajuste do modelo global salvo em: {output_path}")
            
        except Exception as e:
            print(f"Erro ao gerar gráfico de métricas: {e}")
    
    except Exception as e:
        print(f"Erro ao visualizar resultados do modelo global: {e}")
        import traceback
        traceback.print_exc()

# --- Modificar o bloco principal para incluir esta nova função ---
# Adicionar após a linha que executa plot_path_diagram(results)
if __name__ == '__main__':
    # ... codigo existente ...
    
    # 5. Gerar resultados e visualizações
    if results:
        print("\n--- Gerando Resultados ---")
        
        # Salvar tabelas de resultados
        save_model_results_table(results)
        
        # Gerar visualizações com tratamento de exceções
        try:
            # Gráficos de ajuste do modelo
            plot_sem_model_fit(results)
        except Exception as e:
            print(f"Erro ao gerar gráficos de ajuste do modelo: {e}")
        
        try:
            # Gráficos de cargas fatoriais
            plot_loadings(results)
        except Exception as e:
            print(f"Erro ao gerar gráficos de cargas fatoriais: {e}")
        
        try:
            # Diagramas de caminho
            plot_path_diagram(results)
        except Exception as e:
            print(f"Erro ao gerar diagramas de caminho: {e}")
            
        try:
            # Nova visualização do modelo global
            visualize_global_model_results(results)
        except Exception as e:
            print(f"Erro ao gerar visualizações do modelo global: {e}")
        
        try:
            # Análise por fatores sociodemográficos (apenas para modelo global)
            analyze_factors_by_sociodemographics(df_cleaned, results)
        except Exception as e:
            print(f"Erro ao realizar análise sociodemográfica: {e}")
        
        print("\nAnálise completa! Resultados salvos no diretório 'resultados/'.")
    else:
        print("\nAVISO: Nenhum modelo SEM foi ajustado com sucesso.")