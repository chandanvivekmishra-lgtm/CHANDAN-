"""SQLAlchemy models for the NIDS database."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from backend.database import Base


class NetworkTraffic(Base):
    """Model for network traffic records."""
    
    __tablename__ = "network_traffic"
    
    id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String(50), index=True)
    destination_ip = Column(String(50), index=True)
    source_port = Column(Integer)
    destination_port = Column(Integer)
    protocol = Column(String(20))
    packet_count = Column(Integer)
    byte_count = Column(Integer)
    duration = Column(Float)
    is_anomaly = Column(Boolean, default=False, index=True)
    anomaly_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class DetectionAlert(Base):
    """Model for intrusion detection alerts."""
    
    __tablename__ = "detection_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    traffic_id = Column(Integer, index=True)  # Reference to NetworkTraffic
    alert_type = Column(String(100))
    severity = Column(String(20))  # low, medium, high, critical
    description = Column(Text)
    source_ip = Column(String(50), index=True)
    destination_ip = Column(String(50))
    anomaly_score = Column(Float)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class MLModel(Base):
    """Model for tracking ML model versions."""
    
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), index=True)
    version = Column(Integer)
    accuracy = Column(Float)
    training_samples = Column(Integer)
    is_active = Column(Boolean, default=False)
    model_path = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
