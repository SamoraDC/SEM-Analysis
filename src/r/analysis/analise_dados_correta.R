# Análise Descritiva Completa - Transporte Universitário
# Script: analise_dados_correta.R
# Equivalente ao analise_dados_correta.py

# Função principal de análise descritiva
main <- function() {
  cat("=== ANÁLISE DESCRITIVA COMPLETA - DADOS REAIS ===\n\n")
  
  # Carregar dados reais dos CSVs
  perfil <- read.csv('csv_extraidos/Perfil Socioeconomico.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  qualidade <- read.csv('csv_extraidos/Qualidade do serviço.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  percepcao <- read.csv('csv_extraidos/Percepção novos serviços.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  intencao <- read.csv('csv_extraidos/Intenção comportamental.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  utilizacao <- read.csv('csv_extraidos/Utilização.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  
  cat(sprintf("Total de respondentes: %d\n\n", nrow(perfil)))
  
  # Mapeamentos para conversão
  mapa_satisfacao <- c(
    "Muito insatisfeito" = 1, "Insatisfeito" = 2, "Neutro" = 3,
    "Satisfeito" = 4, "Muito satisfeito" = 5
  )
  
  mapa_concordancia <- c(
    "Discordo totalmente" = 1, "Discordo" = 2, "Neutro" = 3,
    "Concordo" = 4, "Concordo totalmente" = 5
  )
  
  # ANÁLISE DE QUALIDADE
  cat("1. ANÁLISE DE QUALIDADE DO SERVIÇO:\n")
  qualidade_num <- qualidade
  
  # Converter dados de qualidade
  for(i in 2:ncol(qualidade_num)) {
    col_values <- qualidade_num[, i]
    qualidade_num[, i] <- mapa_satisfacao[col_values]
  }
  
  # Calcular estatísticas de qualidade
  medias_qualidade <- colMeans(qualidade_num[, -1], na.rm = TRUE)
  cat(sprintf("   Média geral de qualidade: %.2f\n", mean(medias_qualidade, na.rm = TRUE)))
  cat(sprintf("   Desvio padrão: %.2f\n", sd(medias_qualidade, na.rm = TRUE)))
  cat(sprintf("   Mínimo: %.2f\n", min(medias_qualidade, na.rm = TRUE)))
  cat(sprintf("   Máximo: %.2f\n", max(medias_qualidade, na.rm = TRUE)))
  
  # ANÁLISE DE PERCEPÇÃO
  cat("\n2. ANÁLISE DE PERCEPÇÃO DE RECOMPENSAS:\n")
  percepcao_num <- percepcao
  
  # Converter dados de percepção
  for(i in 2:ncol(percepcao_num)) {
    col_values <- percepcao_num[, i]
    percepcao_num[, i] <- mapa_concordancia[col_values]
  }
  
  # Calcular estatísticas de percepção
  medias_percepcao <- colMeans(percepcao_num[, -1], na.rm = TRUE)
  cat(sprintf("   Média geral de aceitação: %.2f\n", mean(medias_percepcao, na.rm = TRUE)))
  cat(sprintf("   Desvio padrão: %.2f\n", sd(medias_percepcao, na.rm = TRUE)))
  cat(sprintf("   Mínimo: %.2f\n", min(medias_percepcao, na.rm = TRUE)))
  cat(sprintf("   Máximo: %.2f\n", max(medias_percepcao, na.rm = TRUE)))
  
  # ANÁLISE DE INTENÇÃO
  cat("\n3. ANÁLISE DE INTENÇÃO COMPORTAMENTAL:\n")
  intencao_num <- intencao
  
  # Converter dados de intenção
  for(i in 2:ncol(intencao_num)) {
    col_values <- intencao_num[, i]
    intencao_num[, i] <- mapa_concordancia[col_values]
  }
  
  # Calcular estatísticas de intenção
  medias_intencao <- colMeans(intencao_num[, -1], na.rm = TRUE)
  cat(sprintf("   Média geral de intenção: %.2f\n", mean(medias_intencao, na.rm = TRUE)))
  cat(sprintf("   Desvio padrão: %.2f\n", sd(medias_intencao, na.rm = TRUE)))
  cat(sprintf("   Mínimo: %.2f\n", min(medias_intencao, na.rm = TRUE)))
  cat(sprintf("   Máximo: %.2f\n", max(medias_intencao, na.rm = TRUE)))
  
  # ANÁLISE DE CORRELAÇÕES
  cat("\n4. MATRIZ DE CORRELAÇÕES:\n")
  
  # Criar construtos
  construtos <- data.frame(
    Qualidade = rowMeans(qualidade_num[, -1], na.rm = TRUE),
    Percepcao = rowMeans(percepcao_num[, -1], na.rm = TRUE),
    Intencao = rowMeans(intencao_num[, -1], na.rm = TRUE)
  )
  
  # Calcular matriz de correlação
  cor_matrix <- cor(construtos, use = "complete.obs")
  cat("   Matriz de Correlação:\n")
  print(round(cor_matrix, 3))
  
  # Correlações específicas
  cat(sprintf("\n   Correlações principais:\n"))
  cat(sprintf("   Qualidade ↔ Percepção: %.3f\n", cor_matrix["Qualidade", "Percepcao"]))
  cat(sprintf("   Qualidade ↔ Intenção: %.3f\n", cor_matrix["Qualidade", "Intencao"]))
  cat(sprintf("   Percepção ↔ Intenção: %.3f\n", cor_matrix["Percepcao", "Intencao"]))
  
  # ANÁLISE DEMOGRÁFICA RESUMIDA
  cat("\n5. RESUMO DEMOGRÁFICO:\n")
  
  # Gênero
  genero_tab <- table(perfil$Gênero)
  cat(sprintf("   Gênero - Feminino: %.1f%%, Masculino: %.1f%%\n", 
              prop.table(genero_tab)["Feminino"] * 100,
              prop.table(genero_tab)["Masculino"] * 100))
  
  # Raça
  raca_tab <- table(perfil$Raça)
  raca_prop <- prop.table(raca_tab) * 100
  cat(sprintf("   Raça - Negros: %.1f%%, Brancos: %.1f%%\n", 
              raca_prop["Negra ( pretos e pardos)"],
              raca_prop["Branca"]))
  
  cat("\n=== ANÁLISE DESCRITIVA CONCLUÍDA ===\n")
  
  # Retornar dados processados
  return(list(
    construtos = construtos,
    correlacoes = cor_matrix,
    qualidade_stats = list(media = mean(medias_qualidade, na.rm = TRUE)),
    percepcao_stats = list(media = mean(medias_percepcao, na.rm = TRUE)),
    intencao_stats = list(media = mean(medias_intencao, na.rm = TRUE))
  ))
}

# Executar análise
if (!interactive()) {
  resultado_descritivo <- main()
} 