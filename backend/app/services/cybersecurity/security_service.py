"""Cybersecurity & Risk Service - Intrusion Detection, Anomaly Detection"""

from typing import Dict, List, Any
from datetime import datetime


class IntrusionDetectionSystem:
    """Detect potential intrusions"""
    
    @staticmethod
    def analyze_network_traffic(traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze network traffic for intrusions"""
        threat_score = 0.0
        threats = []
        
        # Check for suspicious IPs
        source_ip = traffic_data.get('source_ip', '')
        if source_ip.startswith('192.168.') or source_ip.startswith('10.'):
            # Internal IP - less suspicious
            threat_score += 0.0
        else:
            threat_score += 0.2
        
        # Check traffic volume
        bytes_transferred = traffic_data.get('bytes', 0)
        if bytes_transferred > 1000000:  # > 1MB
            threat_score += 0.3
            threats.append('Large data transfer detected')
        
        # Check port
        port = traffic_data.get('port', 80)
        suspicious_ports = [22, 23, 3389, 445]
        if port in suspicious_ports:
            threat_score += 0.2
            threats.append(f'Access to sensitive port {port}')
        
        # Time-based analysis
        hour = datetime.now().hour
        if hour < 6 or hour > 22:
            threat_score += 0.15
            threats.append('Off-hours activity')
        
        is_threat = threat_score >= 0.5
        
        return {
            'is_threat': is_threat,
            'threat_score': round(threat_score, 2),
            'severity': 'critical' if threat_score >= 0.8 else 'high' if threat_score >= 0.5 else 'medium' if threat_score >= 0.3 else 'low',
            'detected_threats': threats if threats else ['No threats detected']
        }


class AnomalyDetector:
    """Detect anomalous behavior"""
    
    @staticmethod
    def detect_anomaly(metrics: Dict[str, float], historical_baseline: Dict[str, float]) -> Dict[str, Any]:
        """Detect anomalies compared to baseline"""
        anomalies = []
        anomaly_score = 0.0
        
        for metric, value in metrics.items():
            baseline = historical_baseline.get(metric, value)
            if baseline == 0:
                continue
            
            deviation = abs(value - baseline) / baseline
            
            if deviation > 2.0:  # 200% deviation
                anomalies.append(f"{metric}: {value} (baseline: {baseline})")
                anomaly_score += 0.3
            elif deviation > 0.5:  # 50% deviation
                anomaly_score += 0.1
        
        return {
            'is_anomalous': anomaly_score >= 0.4,
            'anomaly_score': round(min(1.0, anomaly_score), 2),
            'detected_anomalies': anomalies if anomalies else ['No anomalies detected'],
            'recommendation': 'Investigate immediately' if anomaly_score >= 0.7 else 'Monitor closely' if anomaly_score >= 0.4 else 'Normal operation'
        }


class ComplianceMonitor:
    """Monitor compliance with security policies"""
    
    POLICIES = {
        'password_strength': {'min_length': 12, 'requires_special': True},
        'mfa_required': True,
        'access_review_days': 90,
        'encryption_required': True
    }
    
    @staticmethod
    def check_compliance(system_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with policies"""
        violations = []
        compliance_score = 100
        
        # Password policy
        if system_config.get('password_min_length', 0) < 12:
            violations.append('Password minimum length below policy')
            compliance_score -= 15
        
        # MFA
        if not system_config.get('mfa_enabled', False):
            violations.append('Multi-factor authentication not enabled')
            compliance_score -= 25
        
        # Encryption
        if not system_config.get('encryption_at_rest', False):
            violations.append('Data encryption at rest not enabled')
            compliance_score -= 20
        
        # Access review
        days_since_review = system_config.get('days_since_access_review', 0)
        if days_since_review > 90:
            violations.append(f'Access review overdue by {days_since_review - 90} days')
            compliance_score -= 10
        
        return {
            'is_compliant': len(violations) == 0,
            'compliance_score': max(0, compliance_score),
            'violations': violations if violations else ['No violations found'],
            'priority': 'critical' if compliance_score < 60 else 'high' if compliance_score < 80 else 'normal'
        }


def analyze_security_alert(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze security alert"""
    ids = IntrusionDetectionSystem()
    
    if alert_data.get('type') == 'network':
        return ids.analyze_network_traffic(alert_data)
    
    # Generic threat assessment
    severity = alert_data.get('severity', 'medium')
    threat_score = {'critical': 0.9, 'high': 0.7, 'medium': 0.5, 'low': 0.3}.get(severity, 0.5)
    
    return {
        'is_threat': threat_score >= 0.5,
        'threat_score': threat_score,
        'severity': severity
    }
