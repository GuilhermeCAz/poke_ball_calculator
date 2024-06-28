# streamlit
.PHONY: streamlit
streamlit:
	python -m streamlit run app.py

# python
.PHONY: dependencies
dependencies:
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt

.PHONY: requirements
requirements:
	pip-compile -o requirements.txt
	pip-compile -o requirements-dev.txt --extra=dev

.PHONY: help
help:
	@echo Available targets:
	@echo streamlit        : Run streamlit
	@echo dependencies     : Install dependencies
	@echo requirements     : Compile requirements files
	@echo help             : Show this help message

.DEFAULT_GOAL := help