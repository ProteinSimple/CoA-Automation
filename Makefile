FRONTEND := coat-ui
BACKEND := automation

.PHONY: test build

test:
	$(MAKE) -C $(BACKEND) test

build:
	@echo "Building python backend target and copying"
	pwsh -Command "& { . $(BACKEND)/python_env/Scripts/Activate.ps1; ./bin/buildPy.ps1; }"
	@echo "Building Frontend target"
	cd $(FRONTEND) && npm run tauri build

run:
	@echo "Building python backend target and copying"
	pwsh -Command "& { . $(BACKEND)/python_env/Scripts/Activate.ps1; ./bin/buildPy.ps1; }"
	@echo "Running Frontend in dev mode"
	cd $(FRONTEND) && npm run tauri dev