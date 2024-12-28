#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = embedding-module
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	
## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 app tests

## Format using black
.PHONY: format
format:
	black app tests

## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	python3 -m venv .venv
	@echo ">>> New virtualenv created. Activate with:\nsource .venv/bin/activate"

## Initialize the database using Alembic
.PHONY: init_db
init_db:
	docker-compose up db -d  # Start the Docker services

## Run the FastAPI application locally
.PHONY: run
run:
	. .venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## TODO: Add project rules here


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
