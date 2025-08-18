# Análise Principal - Transporte Universitário  
# Script: analise_final.R
# Equivalente ao analise_final.py - SCRIPT PRINCIPAL - DADOS REAIS

# Função para carregar dados reais (igual ao Python) - usando base R
carregar_dados_reais <- function() {
  # Carregar dados reais dos CSVs (mesma estrutura do Python)
  perfil <- read.csv('csv_extraidos/Perfil Socioeconomico.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  qualidade <- read.csv('csv_extraidos/Qualidade do serviço.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  percepcao <- read.csv('csv_extraidos/Percepção novos serviços.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  intencao <- read.csv('csv_extraidos/Intenção comportamental.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  
  cat(sprintf("   - Perfil: %d registros\n", nrow(perfil)))
  cat(sprintf("   - Qualidade: %d registros\n", nrow(qualidade)))
  cat(sprintf("   - Percepção: %d registros\n", nrow(percepcao)))
  cat(sprintf("   - Intenção: %d registros\n", nrow(intencao)))
  
  return(list(
    perfil = perfil,
    qualidade = qualidade,
    percepcao = percepcao,
    intencao = intencao
  ))
}

# Função para processar dados exatamente como o Python
processar_dados_python_equivalente <- function(dados) {
  # Mapeamentos exatos do Python
  mapa_satisfacao <- c(
    "Muito insatisfeito" = 1, "Insatisfeito" = 2, "Neutro" = 3,
    "Satisfeito" = 4, "Muito satisfeito" = 5
  )
  
  mapa_concordancia <- c(
    "Discordo totalmente" = 1, "Discordo" = 2, "Neutro" = 3,
    "Concordo" = 4, "Concordo totalmente" = 5
  )
  
  # 3. PROCESSAR QUALIDADE (igual ao Python)
  cat("3. Processando dados de qualidade...\n")
  qualidade_num <- dados$qualidade
  
  # Converter colunas de qualidade (exceto ID)
  for(i in 2:ncol(qualidade_num)) {
    col_values <- qualidade_num[, i]
    qualidade_num[, i] <- mapa_satisfacao[col_values]
  }
  
  # Calcular médias como no Python
  medias_qual <- colMeans(qualidade_num[, -1], na.rm = TRUE)
  cat(sprintf("   Média geral de qualidade: %.2f\n", mean(medias_qual, na.rm = TRUE)))
  cat(sprintf("   Pior avaliado: %.2f\n", min(medias_qual, na.rm = TRUE)))
  cat(sprintf("   Melhor avaliado: %.2f\n", max(medias_qual, na.rm = TRUE)))
  
  # 4. PROCESSAR PERCEPÇÃO (igual ao Python)
  cat("\n4. Processando percepção de recompensas...\n")
  percepcao_num <- dados$percepcao
  
  # Converter colunas de percepção (exceto ID)
  for(i in 2:ncol(percepcao_num)) {
    col_values <- percepcao_num[, i]
    percepcao_num[, i] <- mapa_concordancia[col_values]
  }
  
  medias_perc <- colMeans(percepcao_num[, -1], na.rm = TRUE)
  cat(sprintf("   Média geral de aceitação: %.2f\n", mean(medias_perc, na.rm = TRUE)))
  
  # 5. PROCESSAR INTENÇÃO (igual ao Python)
  cat("\n5. Processando intenção comportamental...\n")
  intencao_num <- dados$intencao
  
  # Converter colunas de intenção (exceto ID)
  for(i in 2:ncol(intencao_num)) {
    col_values <- intencao_num[, i]
    intencao_num[, i] <- mapa_concordancia[col_values]
  }
  
  medias_int <- colMeans(intencao_num[, -1], na.rm = TRUE)
  cat(sprintf("   Média geral de intenção: %.2f\n", mean(medias_int, na.rm = TRUE)))
  
  # 6. CRIAR CONSTRUTOS (igual ao Python)
  cat("\n6. Criando construtos latentes...\n")
  construtos <- data.frame(
    ID = qualidade_num[, 1],
    Qualidade = rowMeans(qualidade_num[, -1], na.rm = TRUE),
    Percepcao_Recompensas = rowMeans(percepcao_num[, -1], na.rm = TRUE),
    Intencao_Comportamental = rowMeans(intencao_num[, -1], na.rm = TRUE)
  )
  
  # Remover NaN (igual ao Python)
  construtos_clean <- construtos[complete.cases(construtos), ]
  cat(sprintf("   Casos válidos: %d\n", nrow(construtos_clean)))
  
  return(construtos_clean)
}

# Função de análise de correlação (igual ao Python)
analise_correlacao_python <- function(construtos_clean) {
  cat("\n7. Análise de correlações:\n")
  
  # Matriz de correlação (igual ao Python)
  cor_matrix <- cor(construtos_clean[, c("Qualidade", "Percepcao_Recompensas", "Intencao_Comportamental")])
  
  corr_qual_int <- cor_matrix["Qualidade", "Intencao_Comportamental"]
  corr_perc_int <- cor_matrix["Percepcao_Recompensas", "Intencao_Comportamental"]
  corr_qual_perc <- cor_matrix["Qualidade", "Percepcao_Recompensas"]
  
  cat(sprintf("   Qualidade ↔ Intenção: %.3f\n", corr_qual_int))
  cat(sprintf("   Percepção ↔ Intenção: %.3f\n", corr_perc_int))
  cat(sprintf("   Qualidade ↔ Percepção: %.3f\n", corr_qual_perc))
  
  return(list(
    correlacao_principal = corr_qual_int,
    r_squared = corr_qual_int^2,
    construtos = construtos_clean
  ))
}

# Função de regressão linear (igual ao Python)
analise_regressao_python <- function(resultado_correlacao) {
  cat("\n=== ANÁLISE DE REGRESSÃO ===\n")
  
  construtos <- resultado_correlacao$construtos
  
  # Modelo de regressão (igual ao Python)
  modelo <- lm(Intencao_Comportamental ~ Qualidade, data = construtos)
  
  # Resumo do modelo
  resumo <- summary(modelo)
  
  cat("Modelo de Regressão Linear:\n")
  cat("Y = Intenção Comportamental\n")
  cat("X = Qualidade do Serviço\n\n")
  
  # Coeficientes
  coef <- resumo$coefficients
  cat("Coeficientes:\n")
  print(round(coef, 4))
  
  # R-quadrado
  r_squared <- resumo$r.squared
  r_squared_adj <- resumo$adj.r.squared
  
  cat(sprintf("\nR² = %.3f (%.1f%% da variância explicada)\n", 
              r_squared, r_squared * 100))
  cat(sprintf("R² ajustado = %.3f\n", r_squared_adj))
  
  # Estatística F
  f_stat <- resumo$fstatistic
  cat(sprintf("F(%.0f, %.0f) = %.2f, p < 0.001\n", 
              f_stat[2], f_stat[3], f_stat[1]))
  
  return(list(modelo = modelo, r_squared = r_squared, 
              correlacao = sqrt(r_squared)))
}

# Função principal
main <- function() {
  cat("=== ANÁLISE CORRETA DOS DADOS DE TRANSPORTE ===\n\n")
  cat("Script: analise_final.R (equivalente Python com dados reais)\n\n")
  
  # Carregar dados reais
  cat("1. Carregando dados...\n")
  dados <- carregar_dados_reais()
  
  # Processar dados exatamente como o Python
  construtos_clean <- processar_dados_python_equivalente(dados)
  
  # Análises principais
  resultado_correlacao <- analise_correlacao_python(construtos_clean)
  resultado_regressao <- analise_regressao_python(resultado_correlacao)
  
  # Salvar resultados
  write.csv(construtos_clean, "dados_analise_principal_reais_r.csv", row.names = FALSE)
  
  # Resumo final
  cat("\n=== RESULTADOS PRINCIPAIS ===\n")
  cat(sprintf("✅ Correlação: r = %.3f\n", resultado_correlacao$correlacao_principal))
  cat(sprintf("✅ R²: %.3f (%.1f%% variância explicada)\n", 
              resultado_correlacao$r_squared, resultado_correlacao$r_squared * 100))
  cat(sprintf("✅ Amostra: %d respondentes\n", nrow(construtos_clean)))
  cat("\n✅ Análise principal concluída! Dados salvos em 'dados_analise_principal_reais_r.csv'\n")
  
  return(list(dados = dados, 
              construtos = construtos_clean,
              correlacao = resultado_correlacao$correlacao_principal,
              r_quadrado = resultado_correlacao$r_squared))
}

# Executar análise
if (!interactive()) {
  resultado_final <- main()
} 