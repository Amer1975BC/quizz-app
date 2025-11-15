# 🧪 Quiz App Testing Guide

Dit document beschrijft het uitgebreide testsysteem van de Quiz applicatie, ontworpen om fouten snel te detecteren tijdens de ontwikkeling.

## 📋 Overzicht Test Suite

De Quiz App heeft een complete test suite met:

### 🔧 **Automatische Tests**
- **Backend API Tests** - Python/pytest voor alle endpoints
- **Frontend Logic Tests** - JavaScript tests voor timer en UI logica  
- **Integration Tests** - End-to-end tests voor volledige workflows
- **Database Tests** - Validatie van categorie scheiding en data integriteit
- **Error Handling Tests** - Verificatie van foutafhandeling

### 🎯 **Test Coverage**
- ✅ **Container Health** - Docker containers en services
- ✅ **Database Connectivity** - PostgreSQL verbinding en queries
- ✅ **API Endpoints** - Alle REST endpoints (/api/start, /api/question, etc.)
- ✅ **Category Separation** - Strikte scheiding tussen quiz categorieën
- ✅ **Timer Functionality** - Pause/resume en kleur warnings
- ✅ **Error Scenarios** - Invalid sessions, missing data, etc.

## 🚀 Tests Uitvoeren

### **Volledige Test Suite**
```bash
# Alle tests uitvoeren
./run_tests.sh

# Of via development script
./dev.sh test
```

### **Specifieke Test Types**
```bash
# Alleen backend Python tests
./dev.sh pytest

# Alleen frontend JavaScript tests  
./dev.sh frontend

# Application health check
./dev.sh health
```

### **Development Commands**
```bash
# Toon alle beschikbare commands
./dev.sh help

# Start applicatie
./dev.sh start

# Bekijk logs
./dev.sh logs

# Open database shell
./dev.sh db-shell
```

## 📊 Test Uitvoer Voorbeeld

```
🧪 Quiz App Automated Test Suite
=================================

🔍 Checking Docker containers...
✓ PASS: Quiz app container is running
✓ PASS: PostgreSQL container is running

🗄️  Testing Database Connectivity...
✓ PASS: Database connection successful
✓ PASS: General questions found: 104
✓ PASS: PSPO1 questions found: 65
✓ PASS: Nursing questions found: 100

📋 Testing Quiz Category Separation...
✓ PASS: General quiz session created
✓ PASS: PSPO1 quiz question retrieved
✓ PASS: Nursing quiz question retrieved

📊 Test Results Summary
==========================
Total Tests: 19
Passed: 19
Failed: 0
Success Rate: 100%

🎉 All tests passed!
```

## 🔧 Test Files Structuur

```
quiz-app/
├── test_api.py              # Backend Python tests
├── test_frontend.js         # Frontend JavaScript tests  
├── run_tests.sh            # Hoofdtest script
├── dev.sh                  # Development helper
├── pytest.ini             # Pytest configuratie
├── requirements-test.txt   # Test dependencies
└── .github/
    └── workflows/
        └── test.yml        # CI/CD pipeline
```

## 🎯 Specifieke Test Scenarios

### **1. Category Filtering Tests**
Valideert dat:
- Algemene quiz alleen algemene vragen toont
- PSPO1 quiz alleen Scrum-gerelateerde vragen toont  
- Verpleegkundig quiz alleen medische rekenvragen toont

### **2. Timer Functionality Tests**
Controleert:
- Timer start/pause/resume functionaliteit
- Kleur waarschuwingen (groen → geel → rood)
- Tijd formatting (MM:SS)

### **3. API Endpoint Tests**
Test alle endpoints:
- `POST /api/start` - Quiz sessie starten
- `GET /api/question` - Vragen ophalen
- `POST /api/answer` - Antwoorden indienen
- Error handling voor invalid input

### **4. Database Integrity Tests**
Verifieert:
- Juiste vraag aantallen per categorie
- Alle vragen hebben keuze opties
- Database connectiviteit

## 🚨 Fout Detectie

### **Build-time Checks**
Tests kunnen geïntegreerd worden in Docker build:
```dockerfile
# In Dockerfile.dev
RUN python -m pytest test_api.py -v
```

### **Pre-commit Hooks**
Automatische tests voor elke commit:
```yaml
# .pre-commit-config.yaml
- id: pytest
  name: Backend Tests
- id: frontend-tests  
  name: Frontend Tests
```

### **CI/CD Pipeline**
GitHub Actions draait tests automatisch:
```yaml
# .github/workflows/test.yml
- name: Run Python tests
  run: pytest test_api.py -v
- name: Run integration tests
  run: ./run_tests.sh
```

## 🛠️ Troubleshooting

### **Veelvoorkomende Problemen**

1. **"Database connection failed"**
   ```bash
   # Check database status
   ./dev.sh status
   
   # Restart services  
   ./dev.sh restart
   ```

2. **"Container not running"**
   ```bash
   # Start containers
   ./dev.sh start
   
   # Check logs
   ./dev.sh logs
   ```

3. **"API endpoint not accessible"**
   ```bash
   # Check application health
   ./dev.sh health
   
   # Verify port 9080 is accessible
   curl http://localhost:9080/
   ```

### **Debug Mode**
Voor gedetailleerde test output:
```bash
# Verbose test uitvoer
bash -x run_tests.sh

# Backend tests met debug
./dev.sh shell
pytest test_api.py -v -s
```

## 📈 Performance Testing

### **Load Testing**
```bash
# Eenvoudige performance test
for i in {1..10}; do
  time curl -s http://localhost:9080/ > /dev/null
done
```

### **Memory & Resource Monitoring**
```bash
# Container resource usage
docker stats quiz-app-quiz-app-1

# Database performance
./dev.sh db-shell
# In PostgreSQL:
# EXPLAIN ANALYZE SELECT * FROM questions WHERE explanation = 'PSPO1';
```

## 🔒 Security Testing

### **Vulnerability Scanning**
```bash
# Container security scan (requires trivy)
trivy image quiz-app-quiz-app

# Dependency audit  
pip audit
```

### **Input Validation Tests**
De test suite controleert automatisch:
- SQL injection preventie
- Invalid session handling
- Malformed JSON requests

## 📝 Test Development

### **Nieuwe Tests Toevoegen**

1. **Backend Test** (test_api.py):
```python
def test_new_feature(self, test_db):
    """Test nieuwe functionaliteit"""
    response = client.post("/api/new-endpoint")
    assert response.status_code == 200
```

2. **Frontend Test** (test_frontend.js):
```javascript
testNewUIFeature() {
    // Test nieuwe UI functionaliteit
    this.assert(condition, 'New feature works correctly');
}
```

3. **Integration Test** (run_tests.sh):
```bash
test_new_integration() {
    # Nieuwe end-to-end test
    if curl -s "http://localhost:9080/new-endpoint"; then
        print_status "PASS" "New integration test passed"
    fi
}
```

## 🎯 Best Practices

1. **Test Driven Development**: Schrijf tests voordat je features implementeert
2. **Fast Feedback**: Tests moeten snel zijn (< 30 seconden)
3. **Isolated Tests**: Elke test moet onafhankelijk runnen
4. **Clear Assertions**: Tests moeten duidelijke error messages geven
5. **Realistic Data**: Gebruik representatieve test data

## 📞 Support

Voor vragen over de test suite:
- Check de test uitvoer voor specifieke foutmeldingen
- Bekijk `./dev.sh logs` voor applicatie logs
- Use `./dev.sh shell` om container te onderzoeken
- Test individuele componenten met specifieke commands

---

**Happy Testing! 🧪✨**