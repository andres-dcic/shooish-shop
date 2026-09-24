.PHONY: help security semgrep gitleaks trivy scan-app scan-app-secure semgrep-app semgrep-app-secure trivy-dockerfile trivy-dockerfile-secure gitleaks-app gitleaks-app-secure trivy-app trivy-app-secure trivy-terraform

SECURITY_DIR := $(CURDIR)
APP_DIR := $(CURDIR)/../app
APP_SECURE_DIR := $(CURDIR)/../app_secure

help:
	@echo "Security Tools Lab"
	@echo ""
	@echo "FULL REPOSITORY SCAN:"
	@echo "  make security              Run all checks (Semgrep + Gitleaks + Trivy)"
	@echo "  make semgrep               Run Semgrep (SAST)"
	@echo "  make gitleaks              Run Gitleaks (secret scanning)"
	@echo "  make trivy                 Run Trivy (filesystem scan)"
	@echo ""
	@echo "SCANNING VULNERABLE APP (app/):"
	@echo "  make scan-app              Run all checks on app/ directory"
	@echo "  make semgrep-app           Run Semgrep on app/ directory"
	@echo "  make gitleaks-app          Run Gitleaks on app/ directory"
	@echo "  make trivy-app             Run Trivy on app/ directory"
	@echo "  make trivy-dockerfile      Scan Dockerfile (vulnerable)"
	@echo ""
	@echo "SCANNING SECURE APP (app_secure/):"
	@echo "  make scan-app-secure       Run all checks on app_secure/ directory"
	@echo "  make semgrep-app-secure    Run Semgrep on app_secure/ directory"
	@echo "  make gitleaks-app-secure   Run Gitleaks on app_secure/ directory"
	@echo "  make trivy-app-secure      Run Trivy on app_secure/ directory"
	@echo "  make trivy-dockerfile-secure Scan Dockerfile.secure"
	@echo ""
	@echo "SCANNING INFRASTRUCTURE (terraform/):"
	@echo "  make trivy-terraform       Scan Terraform configuration"

security:
	@echo "Running all security checks. Findings are expected in this intentionally vulnerable lab."
	@$(MAKE) -k semgrep gitleaks trivy || true

scan-app:
	@echo "Running security checks on VULNERABLE app directory (app/)"
	@$(MAKE) -k semgrep-app || true

scan-app-secure:
	@echo "Running security checks on SECURE app directory (app_secure/)"
	@$(MAKE) -k semgrep-app-secure || true

semgrep:
	@echo ""
	@echo "===== SEMGREP / SAST (Full Repository) ====="
	docker run --rm -v "$(CURDIR)/..:/src:ro" -w /src semgrep/semgrep semgrep --config /src/security/tools/semgrep/rules.yml --json --metrics=off || true

semgrep-app:
	@echo ""
	@echo "===== SEMGREP / SAST (app/ - VULNERABLE) ====="
	docker run --rm -v "$(CURDIR)/..:/src:ro" -w /src semgrep/semgrep semgrep --config /src/security/tools/semgrep/rules.yml /src/app --json --metrics=off || true

semgrep-app-secure:
	@echo ""
	@echo "===== SEMGREP / SAST (app_secure/ - SECURE) ====="
	docker run --rm -v "$(CURDIR)/..:/src:ro" -w /src semgrep/semgrep semgrep --config /src/security/tools/semgrep/rules.yml /src/app_secure --json --metrics=off || true

gitleaks:
	@echo ""
	@echo "===== GITLEAKS / SECRETS ====="
	docker run --rm -v "$(CURDIR)/..:/repo:ro" -w /repo zricethezav/gitleaks:latest dir /repo --config=/repo/security/tools/gitleaks/config.toml --no-banner --verbose

gitleaks-app:
	@echo ""
	@echo "===== GITLEAKS / SECRETS (app/ - VULNERABLE) ====="
	docker run --rm -v "$(CURDIR)/..:/repo:ro" -w /repo zricethezav/gitleaks:latest dir /repo/app --config=/repo/security/tools/gitleaks/config.toml --no-banner --verbose || true

gitleaks-app-secure:
	@echo ""
	@echo "===== GITLEAKS / SECRETS (app_secure/ - SECURE) ====="
	docker run --rm -v "$(CURDIR)/..:/repo:ro" -w /repo zricethezav/gitleaks:latest dir /repo/app_secure --config=/repo/security/tools/gitleaks/config.toml --no-banner --verbose || true

trivy:
	@echo ""
	@echo "===== TRIVY / FILESYSTEM ====="
	docker run --rm -v "$(CURDIR)/..:/src:ro" aquasec/trivy:latest fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --ignore-unfixed --format table /src

trivy-dockerfile:
	@echo ""
	@echo "===== TRIVY / DOCKERFILE (app/ - VULNERABLE) ====="
	docker run --rm -v "$(CURDIR)/..:/src:ro" aquasec/trivy:latest config --severity HIGH,CRITICAL --format table /src/Dockerfile || true

trivy-dockerfile-secure:
	@echo ""
	@echo "===== TRIVY / DOCKERFILE (app_secure/ - SECURE) ====="
	docker run --rm -v "$(CURDIR)/..:/src:ro" aquasec/trivy:latest config --severity HIGH,CRITICAL --format table /src/Dockerfile.secure || true

trivy-app:
	@echo ""
	@echo "===== TRIVY / FILESYSTEM (app/ - VULNERABLE) ====="
	docker run --rm -v "$(CURDIR)/..:/src:ro" aquasec/trivy:latest fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --ignore-unfixed --format table /src/app || true

trivy-app-secure:
	@echo ""
	@echo "===== TRIVY / FILESYSTEM (app_secure/ - SECURE) ====="
	docker run --rm -v "$(CURDIR)/..:/src:ro" aquasec/trivy:latest fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --ignore-unfixed --format table /src/app_secure || true

trivy-terraform:
	@echo ""
	@echo "===== TRIVY / TERRAFORM CONFIG ====="
	docker run --rm -v "$(CURDIR)/..:/src:ro" aquasec/trivy:latest config --severity HIGH,CRITICAL --format table /src/terraform || true
