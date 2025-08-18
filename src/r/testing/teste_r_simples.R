# Teste simples R
cat("=== TESTE R FUNCIONANDO ===\n")
cat("R versão instalada e funcionando!\n")
cat("Diretório atual:", getwd(), "\n")

# Verificar se dados existem
if(file.exists("csv_extraidos/Perfil Socioeconomico.csv")) {
  cat("✓ Arquivo de dados encontrado!\n")
} else {
  cat("✗ Arquivo de dados não encontrado!\n")
}

cat("✓ Teste R concluído com sucesso!\n") 