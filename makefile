
PYTHON := python3

PIP := $(PYTHON) -m pip

all: help 

install: 
	@echo ">>> Instalando dependências..."
	$(PIP) install pygame pygame-menu
	@echo ">>> Dependências instaladas com sucesso."

run:
	@echo ">>> Iniciando o jogo..."
	$(PYTHON) main.py

clean:
	@echo ">>> Limpando arquivos temporários, saves e rankings..."
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@find . -type f -name "*.pyc" -delete
	@rm -f savegame.json high_scores.json
	@echo ">>> Limpeza concluída."

help:
	@echo "Uso: make [alvo]"
	@echo ""
	@echo "Alvos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: all install run clean help