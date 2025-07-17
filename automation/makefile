PYTHON := python
SRC := ./src/
TESTS := ./tests/
INSTAL := pyinstaller
REQ := pyREQ.txt

.PHONY: install run test lint clean build help

run: 
	@echo "Running main.py with args: $(ARGS)"
	$(PYTHON) $(SRC)/main.py $(ARGS)

install:
	@echo "Installing dependencies from $(REQ)..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(REQ)

lint:
	@echo "Linting with flake8..."
	flake8 $(SRC) $(SRC)/$(TESTS)

test:
	@echo "Running unit tests"
	$(PYTHON) $(SRC)/testRunner.py

build:
	@echo "Building package..."
	$(INSTAL) .\main.spec -y --clean

clean:
	@echo "Cleaning build artifacts..."
	@if exist build rmdir /s /q build
	@if exist dist rmdir /s /q dist
	@if exist "src/output" rmdir /s /q "src/output"
	@if exist "src/log1.txt" del /q "src\log1.txt"
	@if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
	
help:
	@echo "Makefile commands:"
	@echo "  install     - install dependencies from $(REQ)"
	@echo "  run         - run main.py with optional ARGS, e.g. make run ARGS='--foo bar'"
	@echo "  test        - run tests with pytest"
	@echo "  lint        - run flake8 linter"
	@echo "  build       - build executable with pyinstaller"
	@echo "  clean       - remove build artifacts"
	@echo "  help        - show this help message"