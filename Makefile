.PHONY: help install dev run test lint format fix check clean

# Variáveis
PYTHON := python3
UV := uv
SRC_DIR := src
TEST_DIR := tests

# Cores para output
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
RED := \033[0;31m
NC := \033[0m # No Color

##@ Ajuda

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)Comandos disponíveis:$(NC)"
	@awk 'BEGIN {FS = ":.*##"; printf "\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Instalação

install: ## Instala dependências de produção
	@echo "$(BLUE)Instalando dependências...$(NC)"
	$(UV) sync --no-dev

dev: ## Instala dependências de desenvolvimento
	@echo "$(BLUE)Instalando dependências de desenvolvimento...$(NC)"
	$(UV) sync

##@ Execução

run: ## Executa o servidor de desenvolvimento
	@echo "$(BLUE)Iniciando servidor...$(NC)"
	$(UV) run uvicorn src.server.app:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Executa o servidor em modo produção
	@echo "$(BLUE)Iniciando servidor em modo produção...$(NC)"
	$(UV) run uvicorn src.server.app:app --host 0.0.0.0 --port 8000 --workers 4

##@ Qualidade de Código

lint: ## Verifica código com ruff (sem modificar)
	@echo "$(BLUE)Verificando código...$(NC)"
	$(UV) run ruff check $(SRC_DIR)

format: ## Formata código com ruff
	@echo "$(BLUE)Formatando código...$(NC)"
	$(UV) run ruff format $(SRC_DIR)

fix: ## Corrige problemas automaticamente (lint + format)
	@echo "$(BLUE)Corrigindo e formatando código...$(NC)"
	$(UV) run ruff check --fix $(SRC_DIR)
	$(UV) run ruff format $(SRC_DIR)
	@echo "$(GREEN)✓ Código corrigido e formatado!$(NC)"

check: ## Verifica código sem modificar (lint + format check)
	@echo "$(BLUE)Verificando código...$(NC)"
	$(UV) run ruff check $(SRC_DIR)
	$(UV) run ruff format --check $(SRC_DIR)
	@echo "$(GREEN)✓ Código está ok!$(NC)"

##@ Testes

test: ## Executa testes
	@echo "$(BLUE)Executando testes...$(NC)"
	$(UV) run pytest $(TEST_DIR) -v

test-cov: ## Executa testes com cobertura
	@echo "$(BLUE)Executando testes com cobertura...$(NC)"
	$(UV) run pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term

##@ Performance

profile: ## Profila a aplicação com py-spy
	@echo "$(BLUE)Iniciando profiling...$(NC)"
	$(UV) run py-spy record -o profile.svg -- $(PYTHON) run.py

memory: ## Analisa uso de memória
	@echo "$(BLUE)Analisando memória...$(NC)"
	$(UV) run python -m memory_profiler $(SRC_DIR)/streaming/reader.py

benchmark: ## Executa benchmarks
	@echo "$(BLUE)Executando benchmarks...$(NC)"
	$(UV) run python $(SRC_DIR)/tests/benchmark_memoryview.py

##@ Limpeza

clean: ## Remove arquivos temporários
	@echo "$(BLUE)Limpando arquivos temporários...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -f profile.svg 2>/dev/null || true
	@echo "$(GREEN)✓ Limpeza concluída!$(NC)"

clean-all: clean ## Remove arquivos temporários e venv
	@echo "$(BLUE)Removendo ambiente virtual...$(NC)"
	rm -rf .venv
	@echo "$(GREEN)✓ Limpeza completa!$(NC)"

##@ Utilitários

watch: ## Observa mudanças e executa lint automaticamente
	@echo "$(BLUE)Observando mudanças no código...$(NC)"
	@while true; do \
		inotifywait -q -r -e modify,create,delete $(SRC_DIR); \
		make lint; \
	done

validate: check test ## Valida código (check + test) - use antes de commit
	@echo "$(GREEN)✓ Validação completa!$(NC)"

info: ## Mostra informações do projeto
	@echo "$(BLUE)Informações do Projeto:$(NC)"
	@echo "  Python: $(shell $(PYTHON) --version)"
	@echo "  uv: $(shell $(UV) --version)"
	@echo "  Diretório: $(PWD)"
	@echo "  Fonte: $(SRC_DIR)"
	@echo "  Testes: $(TEST_DIR)"
