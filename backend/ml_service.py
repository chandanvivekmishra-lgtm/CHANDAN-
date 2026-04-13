"""Machine Learning detection engine using Isolation Forest."""
import numpy as np
import pickle
import logging
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from backend.config import settings

logger = logging.getLogger(__name__)


class DetectionEngine:
    """ML-based anomaly detection engine using Isolation Forest."""
    
    def __init__(self):
        """Initialize the detection engine."""
        self.model = None
        self.scaler = None
        self.is_initialized = False
        self.anomaly_threshold = settings.anomaly_threshold
        
        # Try to load pre-trained model
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model from disk."""
        try:
            model_path = Path(settings.model_path)
            scaler_path = Path(settings.scaler_path)
            
            if model_path.exists() and scaler_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                
                self.is_initialized = True
                logger.info("Pre-trained model loaded successfully")
            else:
                logger.warning("Pre-trained model files not found. Initialize with training data.")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
    
    def train(self, X: np.ndarray):
        """
        Train the Isolation Forest model on normal traffic data.
        
        Args:
            X: Training data (n_samples, n_features)
        """
        try:
            # Normalize features
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Train Isolation Forest
            self.model = IsolationForest(
                contamination=0.1,  # Expect ~10% anomalies
                random_state=42,
                n_estimators=100
            )
            self.model.fit(X_scaled)
            
            self.is_initialized = True
            logger.info("Model trained successfully")
            
            # Save model
            self._save_model()
        
        except Exception as e:
            logger.error(f"Error training model: {e}")
    
    def detect(self, features: list) -> tuple:
        """
        Detect if traffic is anomalous.
        
        Args:
            features: List of feature values [source_port, dest_port, packet_count, byte_count, duration]
        
        Returns:
            Tuple of (is_anomaly: bool, anomaly_score: float)
        """
        if not self.is_initialized:
            return False, 0.0
        
        try:
            # Convert to numpy array and reshape
            X = np.array(features).reshape(1, -1)
            
            # Normalize
            X_scaled = self.scaler.transform(X)
            
            # Get anomaly score (lower is more anomalous)
            anomaly_score = -self.model.score_samples(X_scaled)[0]
            
            # Normalize to 0-1 range (approximate)
            normalized_score = 1.0 / (1.0 + np.exp(-anomaly_score))
            
            # Determine if anomalous
            is_anomaly = normalized_score >= self.anomaly_threshold
            
            return is_anomaly, normalized_score
        
        except Exception as e:
            logger.error(f"Error during detection: {e}")
            return False, 0.0
    
    def _save_model(self):
        """Save trained model to disk."""
        try:
            Path(settings.model_path).parent.mkdir(parents=True, exist_ok=True)
            Path(settings.scaler_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(settings.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            with open(settings.scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
