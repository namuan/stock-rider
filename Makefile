export PROJECTNAME=$(shell basename "$(PWD)")

.SILENT: ;               # no need for @

setup: ## Setup Virtual Env
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

deps: ## Install dependencies
	./venv/bin/pip install -r requirements.txt

lint: ## Runs black for code formatting
	./venv/bin/black krider --exclude generated

clean: ## Clean package
	rm -rf build dist

run: lint ## Run all unit tests
	./venv/bin/python local_main.py

rmdb: # Removes database
	(test -f stockstore.db && rm stockstore.db) || echo "No database found"

repopulate: rmdb ## Re-index data
	./venv/bin/python local_main.py populate-data --period 12mo --interval 1d

volume: ## Run Volume Analysis
	./venv/bin/python local_main.py volume-analysis

gainlose: ## Calculate biggest gainers/losers
	./venv/bin/python local_main.py gainers-losers

pipeline: repopulate volume gainlose ## Runs the whole pipeline
	echo "Completed"

package: clean
	./pypi.sh

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo