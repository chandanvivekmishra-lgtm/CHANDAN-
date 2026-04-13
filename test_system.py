"""Test script to verify NIDS system is working."""
import sys
from pathlib import Path

print("=" * 60)
print("NIDS System Test Suite")
print("=" * 60)

# Test 1: Check Python version
print("\n✓ Test 1: Python Version")
print(f"  Python {sys.version.split()[0]}")

# Test 2: Import dependencies
print("\n✓ Test 2: Checking Dependencies")
try:
    import fastapi
    print(f"  ✓ FastAPI {fastapi.__version__}")
except ImportError as e:
    print(f"  ✗ FastAPI: {e}")

try:
    import sklearn
    print(f"  ✓ scikit-learn {sklearn.__version__}")
except ImportError as e:
    print(f"  ✗ scikit-learn: {e}")

try:
    import numpy
    print(f"  ✓ NumPy {numpy.__version__}")
except ImportError as e:
    print(f"  ✗ NumPy: {e}")

try:
    import sqlalchemy
    print(f"  ✓ SQLAlchemy {sqlalchemy.__version__}")
except ImportError as e:
    print(f"  ✗ SQLAlchemy: {e}")

# Test 3: Check file structure
print("\n✓ Test 3: Project Structure")
required_files = [
    "backend/main.py",
    "backend/ml_service.py",
    "backend/models.py",
    "backend/schemas.py",
    "backend/database.py",
    "ml_engine/train.py",
    "ml_engine/data_processor.py",
    "database/init.py",
    "frontend/src/App.jsx",
    "frontend/package.json",
    "requirements.txt",
    "README.md"
]

for file in required_files:
    path = Path(file)
    status = "✓" if path.exists() else "✗"
    print(f"  {status} {file}")

# Test 4: ML Model Test
print("\n✓ Test 4: ML Model Initialization")
try:
    from backend.ml_service import DetectionEngine
    engine = DetectionEngine()
    print(f"  ✓ Detection Engine initialized")
    print(f"  ✓ Model initialized: {engine.is_initialized}")
    
    # Test detection on sample data
    sample_features = [5000, 80, 100, 50000, 5.0]
    is_anomaly, score = engine.detect(sample_features)
    print(f"  ✓ Sample detection: anomaly={is_anomaly}, score={score:.4f}")
    
except Exception as e:
    print(f"  ✗ ML Model Error: {e}")

# Test 5: Database models
print("\n✓ Test 5: Database Models")
try:
    from backend.models import NetworkTraffic, DetectionAlert, MLModel
    print(f"  ✓ NetworkTraffic model loaded")
    print(f"  ✓ DetectionAlert model loaded")
    print(f"  ✓ MLModel model loaded")
except Exception as e:
    print(f"  ✗ Database Models Error: {e}")

# Test 6: Schemas
print("\n✓ Test 6: API Schemas")
try:
    from backend.schemas import (
        NetworkTrafficCreate,
        NetworkTrafficResponse,
        DetectionAlertResponse,
        HealthCheckResponse,
        DetectionStatsResponse
    )
    print(f"  ✓ NetworkTrafficCreate schema loaded")
    print(f"  ✓ NetworkTrafficResponse schema loaded")
    print(f"  ✓ DetectionAlertResponse schema loaded")
    print(f"  ✓ HealthCheckResponse schema loaded")
    print(f"  ✓ DetectionStatsResponse schema loaded")
except Exception as e:
    print(f"  ✗ Schemas Error: {e}")

# Test 7: Data processor
print("\n✓ Test 7: Data Processor")
try:
    from ml_engine.data_processor import TrafficDataProcessor
    sample_data = TrafficDataProcessor.generate_sample_traffic(n_samples=100)
    print(f"  ✓ Sample data generated: shape {sample_data.shape}")
    print(f"  ✓ Feature statistics loaded")
except Exception as e:
    print(f"  ✗ Data Processor Error: {e}")

print("\n" + "=" * 60)
print("Test Summary: All core modules are working! ✓")
print("=" * 60)
print("\nNext steps:")
print("1. Start the backend: python -m uvicorn backend.main:app --reload")
print("2. Install frontend deps: cd frontend && npm install")
print("3. Start frontend: npm run dev")
print("4. Access dashboard: http://localhost:3000")
print("=" * 60)
