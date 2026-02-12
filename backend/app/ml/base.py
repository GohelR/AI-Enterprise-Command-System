"""Machine Learning utilities and base classes"""

import pickle
import json
import os
from typing import Any, Dict, Optional
import numpy as np
from datetime import datetime
from backend.app.core.config import settings


class MLModelBase:
    """Base class for ML models"""
    
    def __init__(self, model_name: str, model_version: str = "1.0.0"):
        self.model_name = model_name
        self.model_version = model_version
        self.model = None
        self.model_path = os.path.join(settings.MODEL_STORAGE_PATH, f"{model_name}_{model_version}.pkl")
        
    def save_model(self):
        """Save model to disk"""
        os.makedirs(settings.MODEL_STORAGE_PATH, exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load model from disk"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"Model loaded from {self.model_path}")
            return True
        return False
    
    def predict(self, X):
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not loaded or trained")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get prediction probabilities"""
        if self.model is None:
            raise ValueError("Model not loaded or trained")
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        return None


class ModelRegistry:
    """Model registry for tracking ML models"""
    
    def __init__(self):
        self.registry_path = os.path.join(settings.MODEL_STORAGE_PATH, "model_registry.json")
        self.registry = self.load_registry()
    
    def load_registry(self) -> Dict:
        """Load model registry"""
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_registry(self):
        """Save model registry"""
        os.makedirs(settings.MODEL_STORAGE_PATH, exist_ok=True)
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def register_model(self, model_name: str, model_version: str, metadata: Dict[str, Any]):
        """Register a new model"""
        key = f"{model_name}_{model_version}"
        self.registry[key] = {
            **metadata,
            "registered_at": datetime.utcnow().isoformat(),
            "model_name": model_name,
            "model_version": model_version
        }
        self.save_registry()
    
    def get_model_info(self, model_name: str, model_version: str) -> Optional[Dict]:
        """Get model information"""
        key = f"{model_name}_{model_version}"
        return self.registry.get(key)
    
    def list_models(self) -> Dict:
        """List all registered models"""
        return self.registry


# Feature engineering utilities
def extract_text_features(text: str) -> Dict[str, Any]:
    """Extract features from text"""
    words = text.split()
    return {
        'length': len(text),
        'word_count': len(words),
        'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
        'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0
    }


def normalize_features(features: np.ndarray) -> np.ndarray:
    """Normalize features to 0-1 range"""
    min_val = np.min(features, axis=0)
    max_val = np.max(features, axis=0)
    range_val = max_val - min_val
    range_val[range_val == 0] = 1  # Avoid division by zero
    return (features - min_val) / range_val
