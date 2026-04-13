# Network Intrusion Detection System (NIDS)

> 🔴 **Problem**: Hackers attack networks  
> 💡 **Solution**: Detect suspicious network activity with ML-based anomaly detection

## 🎯 Overview

The Network Intrusion Detection System (NIDS) is a full-stack application for detecting suspicious network activity using machine learning. It monitors network traffic patterns and identifies anomalies that may indicate security threats or attacks.

### Key Features
- 🔍 **Real-time Traffic Monitoring**: Analyzes incoming network traffic
- 🤖 **ML-based Detection**: Isolation Forest algorithm for anomaly detection
- 📊 **Interactive Dashboard**: Beautiful React-based visualization
- 🚨 **Alert System**: Severity-based alerts for detected anomalies
- 📈 **Statistics & Analytics**: Detailed traffic and threat analysis
- 🔄 **RESTful API**: FastAPI backend with comprehensive endpoints

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Web Dashboard                       │
│          (Real-time visualization & controls)                │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  (Traffic analysis, Detection routing, Alert management)     │
└────────────────────┬────────────────────────────────────────┘
                     │ ML Model
┌────────────────────┬────────────────────────────────────────┐
│                                                              │
│  Isolation Forest Model  │  Anomaly Detection Engine         │
│  (Trained on normal traffic patterns)                        │
│                                                              │
└────────────┬─────────────────────────────────┬──────────────┘
             │                                 │
      ┌──────┴────────┐              ┌────────┴──────┐
      │  PostgreSQL   │              │  Model Cache  │
      │  Database     │              │   (Pickle)    │
      └───────────────┘              └───────────────┘
```

## 📋 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | FastAPI | 0.104.1 |
| ML Engine | scikit-learn | 1.3.2 |
| Database | PostgreSQL | 12+ |
| Frontend | React | 18.2.0 |
| UI Framework | Tailwind CSS | 3.3.0 |
| Build Tool | Vite | 5.0.0 |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.example config/.env
# Edit config/.env with your PostgreSQL credentials

# Initialize database
python -m database.init

# Train the ML model (optional, uses synthetic data by default)
python -m ml_engine.train

# Start FastAPI server
python -m uvicorn backend.main:app --reload
```

Backend will run at: `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: `http://localhost:3000` or `http://localhost:5173`

## 📡 API Endpoints

### Health & Status
- `GET /` - Welcome endpoint
- `GET /health` - System health check

### Traffic Analysis
- `POST /api/traffic` - Analyze network traffic
- `GET /api/traffic` - Get traffic history
- `GET /api/stats` - Get detection statistics

### Alerts
- `GET /api/alerts` - Get detection alerts
- `GET /api/alerts?unresolved_only=true` - Get active alerts

### Example: Analyze Traffic

```bash
curl -X POST http://localhost:8000/api/traffic \
  -H "Content-Type: application/json" \
  -d {
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.1",
    "source_port": 54321,
    "destination_port": 80,
    "protocol": "TCP",
    "packet_count": 1542,
    "byte_count": 2048576,
    "duration": 12.5
  }
```

## 🔬 ML Detection Model

### Algorithm: Isolation Forest

**Why Isolation Forest?**
- Unsupervised learning (no labeled training data needed)
- Excellent for detecting anomalies in high-dimensional data
- Fast training and detection
- Robust against different types of attacks

### Features Used
1. **Source Port** - Range: 1024-65535
2. **Destination Port** - Range: 1-65535
3. **Packet Count** - Number of packets in connection
4. **Byte Count** - Total bytes transferred
5. **Duration** - Connection duration in seconds

### Training Process

```python
# Generate or load network traffic data
X = load_training_data()  # Shape: (n_samples, 5)

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = IsolationForest(contamination=0.1, n_estimators=100)
model.fit(X_scaled)

# Save for inference
save(model, "detection_model.pkl")
```

### Anomaly Detection

Each traffic record receives an anomaly score (0-1):
- **Score < 0.5**: Normal traffic
- **Score 0.5-0.8**: Suspicious
- **Score > 0.8**: High anomaly risk
- **Score > 0.9**: Critical alert

## 📊 Dashboard

The interactive dashboard provides:

### 🎨 Key Metrics
- **Total Traffic**: Cumulative connections analyzed
- **Anomalies**: Number of suspicious connections
- **Detection Rate**: Percentage of traffic flagged
- **Active Alerts**: Current unresolved threats
- **Critical Alerts**: High-severity threats

### 📈 Visualizations
- **Packet Count Chart**: Traffic volume by source IP
- **Anomaly Score Trends**: Detection confidence over time
- **Alert Timeline**: When threats were detected

### 🔔 Alerts Table
- Timestamp of detection
- Source/Destination IPs
- Threat severity level
- Anomaly score
- Resolution status

## 🔧 Configuration

Edit `config/.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/nids_db

# API
DEBUG=True
SECRET_KEY=your-secret-key-here

# ML Model
ANOMALY_THRESHOLD=0.8  # Score threshold for alerting
```

## 📁 Project Structure

```
.
├── backend/                  # FastAPI application
│   ├── __init__.py
│   ├── main.py              # API routes
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # DB configuration
│   ├── config.py            # Settings
│   └── ml_service.py        # Detection engine
│
├── frontend/                # React dashboard
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── AlertsTable.jsx
│   │   │   └── TrafficChart.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── ml_engine/              # ML utilities
│   ├── __init__.py
│   ├── data_processor.py   # Data loading & processing
│   └── train.py            # Model training script
│
├── database/               # Database utilities
│   ├── init.py            # DB initialization
│   └── schema.py          # SQL schemas
│
├── config/                # Configuration
│   └── .env.example       # Environment template
│
└── requirements.txt       # Python dependencies
```

## 🎓 Training the Model

### Option 1: Synthetic Data (Default)

```bash
python ml_engine/train.py
# Uses generated normal and anomalous traffic patterns
```

### Option 2: Real Traffic Data

Create a CSV file with columns:
```
source_port,destination_port,packet_count,byte_count,duration
54321,80,1542,2048576,12.5
...
```

Then train:
```bash
python ml_engine/train.py --data path/to/traffic.csv
```

## 🐳 Docker Deployment (Optional)

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📊 Sample Traffic Data

You can upload test traffic records via the API:

```python
import requests

traffic_samples = [
    {
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1",
        "source_port": 54321,
        "destination_port": 80,
        "protocol": "TCP",
        "packet_count": 1542,
        "byte_count": 2048576,
        "duration": 12.5
    },
    # More samples...
]

for traffic in traffic_samples:
    response = requests.post(
        'http://localhost:8000/api/traffic',
        json=traffic
    )
    print(response.json())
```

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Install missing dependencies
pip install -r requirements.txt --upgrade

# Check PostgreSQL connection
psql -U user -d nids_db -c "SELECT 1"
```

### Database connection error
```bash
# Update DATABASE_URL in config/.env
DATABASE_URL=postgresql://username:password@localhost:5432/nids_db

# Reinitialize database
python -m database.init
```

### Frontend can't connect to backend
```bash
# Ensure backend is running
curl http://localhost:8000/

# Check CORS settings in backend/main.py
# Frontend URL should be in allow_origins list
```

### ML model not detecting anomalies
```bash
# Retrain model
python ml_engine/train.py

# Check ANOMALY_THRESHOLD in config/.env
# Lower threshold = more sensitive detection
```

## 📚 Further Development

### Enhancements
- [ ] Real-time packet capture integration (Scapy/libpcap)
- [ ] Advanced threat intelligence integration
- [ ] User authentication & role-based access
- [ ] Persistent alert notifications
- [ ] GraphQL API endpoint
- [ ] Kubernetes deployment configs
- [ ] ML model versioning & comparison
- [ ] Geographic visualization of attacks
- [ ] Export reports (PDF/CSV)
- [ ] Integration with SIEM platforms

### Testing
```bash
# Run backend tests
pytest backend/

# Run frontend tests
npm test
```

## 📄 License

MIT License - Feel free to use for educational and commercial purposes

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at `http://localhost:8000/docs` (Swagger UI)
- Check logs in the terminal

---

**Built with ❤️ for network security**

Made with FastAPI, React, and scikit-learn
