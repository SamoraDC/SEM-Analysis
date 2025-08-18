# Análise Demográfica - Transporte Universitário
# Script: dados_reais_final.R
# Equivalente ao dados_reais_final.py - DADOS REAIS

# Função principal de análise
main <- function() {
  cat("=== DADOS REAIS PARA CORREÇÃO DO RELATÓRIO ===\n")
  
  # Carregar dados reais dos CSVs (igual ao Python) - usando base R
  perfil <- read.csv('csv_extraidos/Perfil Socioeconomico.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  qualidade <- read.csv('csv_extraidos/Qualidade do serviço.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  percepcao <- read.csv('csv_extraidos/Percepção novos serviços.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  intencao <- read.csv('csv_extraidos/Intenção comportamental.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  utilizacao <- read.csv('csv_extraidos/Utilização.csv', fileEncoding = "UTF-8", stringsAsFactors = FALSE)
  
  cat(sprintf("Total: %d respondentes\n\n", nrow(perfil)))
  
  # 1. ANÁLISE DE GÊNERO (igual ao Python)
  cat("1. GÊNERO:\n")
  genero_counts <- table(perfil$Gênero)
  genero_prop <- prop.table(genero_counts) * 100
  
  for(i in 1:length(genero_counts)) {
    nome_genero <- names(genero_counts)[i]
    count <- genero_counts[i]
    percent <- genero_prop[i]
    cat(sprintf("   %s: %d (%.1f%%)\n", nome_genero, count, percent))
  }
  
  # 2. ANÁLISE DE ESCOLARIDADE (igual ao Python)
  cat("\n2. ESCOLARIDADE:\n")
  escolaridade_counts <- table(perfil$Escolaridade)
  escolaridade_counts <- sort(escolaridade_counts, decreasing = TRUE)
  escolaridade_prop <- prop.table(escolaridade_counts) * 100
  
  for(i in 1:length(escolaridade_counts)) {
    nome_esc <- names(escolaridade_counts)[i]
    count <- escolaridade_counts[i]
    percent <- escolaridade_prop[i]
    cat(sprintf("   %s: %d (%.1f%%)\n", nome_esc, count, percent))
  }
  
  # 3. ANÁLISE DE RAÇA (igual ao Python)
  cat("\n3. RAÇA:\n")
  raca_counts <- table(perfil$Raça)
  raca_counts <- sort(raca_counts, decreasing = TRUE)
  raca_prop <- prop.table(raca_counts) * 100
  
  for(i in 1:length(raca_counts)) {
    nome_raca <- names(raca_counts)[i]
    count <- raca_counts[i]
    percent <- raca_prop[i]
    cat(sprintf("   %s: %d (%.1f%%)\n", nome_raca, count, percent))
  }
  
  # 4. ANÁLISE DE RENDA (igual ao Python)
  cat("\n4. RENDA:\n")
  renda_counts <- table(perfil$Renda)
  renda_counts <- sort(renda_counts, decreasing = TRUE)
  renda_prop <- prop.table(renda_counts) * 100
  
  for(i in 1:length(renda_counts)) {
    nome_renda <- names(renda_counts)[i]
    count <- renda_counts[i]
    percent <- renda_prop[i]
    cat(sprintf("   %s: %d (%.1f%%)\n", nome_renda, count, percent))
  }
  
  # 5. ANÁLISE DE CARTEIRA DE MOTORISTA (igual ao Python)
  cat("\n5. CARTEIRA DE MOTORISTA:\n")
  carteira_counts <- table(perfil$Carteira.de.motorista)
  carteira_prop <- prop.table(carteira_counts) * 100
  
  for(i in 1:length(carteira_counts)) {
    nome_carteira <- names(carteira_counts)[i]
    count <- carteira_counts[i]
    percent <- carteira_prop[i]
    cat(sprintf("   %s: %d (%.1f%%)\n", nome_carteira, count, percent))
  }
  
  cat("\n=== ANÁLISE DEMOGRÁFICA CONCLUÍDA ===\n")
  
  # Retornar lista com dados para uso posterior
  return(list(
    perfil = perfil,
    qualidade = qualidade,
    percepcao = percepcao,
    intencao = intencao,
    utilizacao = utilizacao
  ))
}

# Executar análise
if (!interactive()) {
  dados_resultado <- main()
} 