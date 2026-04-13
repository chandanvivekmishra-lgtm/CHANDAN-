"""FastAPI application initialization and route definitions."""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import get_db, engine, Base
from backend.models import NetworkTraffic, DetectionAlert, MLModel
from backend import schemas
from backend.config import settings
from backend.ml_service import DetectionEngine
import logging

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Network Intrusion Detection System API"
)

# Initialize ML engine
detection_engine = DetectionEngine()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/", tags=["Health"])
def read_root():
    """Root endpoint."""
    return {"message": "NIDS API is running"}


@app.get("/health", response_model=schemas.HealthCheckResponse, tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_connected = True
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        db_connected = False
    
    return {
        "status": "healthy",
        "model_enabled": detection_engine.is_initialized,
        "database_connected": db_connected,
        "version": settings.api_version
    }


@app.post("/api/traffic", response_model=schemas.NetworkTrafficResponse, tags=["Traffic"])
def analyze_traffic(
    traffic: schemas.NetworkTrafficCreate,
    db: Session = Depends(get_db)
):
    """Analyze network traffic and detect anomalies."""
    
    # Create traffic record
    traffic_record = NetworkTraffic(
        source_ip=traffic.source_ip,
        destination_ip=traffic.destination_ip,
        source_port=traffic.source_port,
        destination_port=traffic.destination_port,
        protocol=traffic.protocol,
        packet_count=traffic.packet_count,
        byte_count=traffic.byte_count,
        duration=traffic.duration
    )
    
    # Run anomaly detection
    if detection_engine.is_initialized:
        try:
            # Prepare features for detection
            features = [
                traffic.source_port,
                traffic.destination_port,
                traffic.packet_count,
                traffic.byte_count,
                traffic.duration
            ]
            
            is_anomaly, anomaly_score = detection_engine.detect(features)
            traffic_record.is_anomaly = is_anomaly
            traffic_record.anomaly_score = anomaly_score
            
            # Create alert if anomaly detected
            if is_anomaly:
                severity = "critical" if anomaly_score > 0.9 else "high"
                alert = DetectionAlert(
                    traffic_id=traffic_record.id,
                    alert_type="Anomalous Traffic",
                    severity=severity,
                    description=f"Anomalous network traffic detected with score {anomaly_score:.2f}",
                    source_ip=traffic.source_ip,
                    destination_ip=traffic.destination_ip,
                    anomaly_score=anomaly_score
                )
                db.add(alert)
        except Exception as e:
            logger.error(f"Error during detection: {e}")
    
    db.add(traffic_record)
    db.commit()
    db.refresh(traffic_record)
    
    return traffic_record


@app.get("/api/stats", response_model=schemas.DetectionStatsResponse, tags=["Statistics"])
def get_stats(db: Session = Depends(get_db)):
    """Get detection statistics."""
    
    total_traffic = db.query(NetworkTraffic).count()
    total_anomalies = db.query(NetworkTraffic).filter(NetworkTraffic.is_anomaly == True).count()
    active_alerts = db.query(DetectionAlert).filter(DetectionAlert.is_resolved == False).count()
    critical_alerts = db.query(DetectionAlert).filter(
        (DetectionAlert.severity == "critical") & 
        (DetectionAlert.is_resolved == False)
    ).count()
    
    detection_rate = (total_anomalies / total_traffic * 100) if total_traffic > 0 else 0
    
    return {
        "total_traffic": total_traffic,
        "total_anomalies": total_anomalies,
        "detection_rate": detection_rate,
        "active_alerts": active_alerts,
        "critical_alerts": critical_alerts
    }


@app.get("/api/alerts", response_model=list[schemas.DetectionAlertResponse], tags=["Alerts"])
def get_alerts(
    skip: int = 0,
    limit: int = 50,
    unresolved_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get detection alerts."""
    
    query = db.query(DetectionAlert)
    
    if unresolved_only:
        query = query.filter(DetectionAlert.is_resolved == False)
    
    alerts = query.order_by(DetectionAlert.created_at.desc()).offset(skip).limit(limit).all()
    return alerts


@app.get("/api/traffic", response_model=list[schemas.NetworkTrafficResponse], tags=["Traffic"])
def get_traffic(
    skip: int = 0,
    limit: int = 50,
    anomaly_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get network traffic records."""
    
    query = db.query(NetworkTraffic)
    
    if anomaly_only:
        query = query.filter(NetworkTraffic.is_anomaly == True)
    
    traffic = query.order_by(NetworkTraffic.created_at.desc()).offset(skip).limit(limit).all()
    return traffic
