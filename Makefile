# Makefile for Quiz Application Development

.PHONY: help build test start stop clean logs shell pytest frontend-test integration-test

# Default target
help:
	@echo "📚 Quiz App Development Commands"
	@echo "================================"
	@echo ""
	@echo "🏗️  Build & Deploy:"
	@echo "  make build      - Build Docker containers"
	@echo "  make start      - Start all services"
	@echo "  make stop       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test       - Run all tests"
	@echo "  make pytest     - Run Python backend tests only"
	@echo "  make frontend   - Run frontend JavaScript tests"
	@echo "  make integration - Run integration tests"
	@echo ""
	@echo "🔧 Development:"
	@echo "  make logs       - Show application logs"
	@echo "  make shell      - Open shell in app container"
	@echo "  make clean      - Clean up containers and volumes"
	@echo "  make db-shell   - Open database shell"
	@echo ""
	@echo "📊 Status:"
	@echo "  make status     - Show container status"
	@echo "  make health     - Check application health"

# Build containers
build:
	@echo "🏗️ Building Docker containers..."
	docker-compose build

# Start services  
start:
	@echo "🚀 Starting services..."
	docker-compose up -d
	@echo "✅ Services started. Application available at http://localhost:9080"

# Stop services
stop:
	@echo "⏹️ Stopping services..."
	docker-compose down

# Restart services
restart: stop start

# Run all tests
test:
	@echo "🧪 Running complete test suite..."
	./run_tests.sh

# Run Python backend tests only
pytest:
	@echo "🐍 Running Python backend tests..."
	docker-compose exec quiz-app python -m pytest test_api.py -v

# Run frontend tests
frontend:
	@echo "🌐 Running frontend tests..."
	node test_frontend.js

# Run integration tests
integration:
	@echo "🔗 Running integration tests..."
	@echo "Ensuring services are running..."
	@make start
	@sleep 10
	@echo "Running integration test suite..."
	./run_tests.sh

# Show logs
logs:
	@echo "📋 Showing application logs..."
	docker-compose logs -f quiz-app

# Open shell in application container
shell:
	@echo "🐚 Opening shell in application container..."
	docker-compose exec quiz-app /bin/bash

# Open database shell
db-shell:
	@echo "🗄️ Opening database shell..."
	docker-compose exec postgres psql -U quiz -d quizdb

# Clean up
clean:
	@echo "🧹 Cleaning up containers and volumes..."
	docker-compose down -v
	docker system prune -f

# Show container status
status:
	@echo "📊 Container Status:"
	@docker-compose ps

# Check application health
health:
	@echo "❤️ Checking application health..."
	@if curl -f -s http://localhost:9080/ > /dev/null; then \
		echo "✅ Application is healthy"; \
	else \
		echo "❌ Application is not responding"; \
		exit 1; \
	fi

# Development with auto-reload
dev:
	@echo "👨‍💻 Starting development mode with auto-reload..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Run tests in watch mode (requires entr)
test-watch:
	@echo "👀 Running tests in watch mode..."
	find . -name "*.py" | entr -r make pytest

# Database migrations and setup
db-init:
	@echo "🗄️ Initializing database..."
	docker-compose exec quiz-app python -c "from webapi import engine, Base; Base.metadata.create_all(bind=engine)"

# Add sample data
db-seed:
	@echo "🌱 Seeding database with sample data..."
	docker-compose exec quiz-app python add_nursing_questions_to_db.py

# Database backup
db-backup:
	@echo "💾 Creating database backup..."
	docker-compose exec postgres pg_dump -U quiz quizdb > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Performance test
perf-test:
	@echo "🚀 Running performance tests..."
	@for i in {1..10}; do \
		time curl -s http://localhost:9080/ > /dev/null; \
	done

# Security scan (if trivy is installed)
security-scan:
	@if command -v trivy >/dev/null 2>&1; then \
		echo "🔒 Running security scan..."; \
		trivy image quiz-app-quiz-app; \
	else \
		echo "⚠️ Trivy not installed. Install with: brew install trivy"; \
	fi