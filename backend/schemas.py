"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NetworkTrafficCreate(BaseModel):
    """Schema for creating network traffic records."""
    
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    packet_count: int
    byte_count: int
    duration: float


class NetworkTrafficResponse(NetworkTrafficCreate):
    """Schema for network traffic response."""
    
    id: int
    is_anomaly: bool
    anomaly_score: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DetectionAlertResponse(BaseModel):
    """Schema for detection alert response."""
    
    id: int
    traffic_id: int
    alert_type: str
    severity: str
    description: str
    source_ip: str
    destination_ip: str
    anomaly_score: float
    is_resolved: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    
    status: str
    model_enabled: bool
    database_connected: bool
    version: str


class DetectionStatsResponse(BaseModel):
    """Schema for detection statistics."""
    
    total_traffic: int
    total_anomalies: int
    detection_rate: float
    active_alerts: int
    critical_alerts: int
