.PHONY: help init-db migrate start dev

# Variables
VENV_BIN := venv/bin
PYTHON := $(VENV_BIN)/python
ALEMBIC := $(VENV_BIN)/alembic
UVICORN := $(VENV_BIN)/uvicorn
DB_HOST := localhost
DB_USER := postgres
DB_NAME := nexus
DB_PASSWORD := postgres

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

init-db: ## Initialize database (create schema and seed data)
	@echo "Initializing database: $(DB_NAME)"
	@export PGPASSWORD=$(DB_PASSWORD) && \
		psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) -f db/schema.sql && \
		psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) -f db/seed.sql
	@echo "Database initialization complete!"
	@echo ""
	@echo "Default user ID: 00000000-0000-0000-0000-000000000001"
	@echo "Make sure your .env file has:"
	@echo "DEFAULT_USER_ID=00000000-0000-0000-0000-000000000001"

migrate: ## Run database migrations
	@echo "Running database migrations..."
	@$(ALEMBIC) upgrade head
	@echo "Migrations complete!"

start: ## Start the API server
	@echo "Starting API server..."
	@$(UVICORN) app.main:app --reload

dev: migrate start ## Run migrations and start API in development mode (with reload)

