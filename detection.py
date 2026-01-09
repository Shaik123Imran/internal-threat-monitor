"""
Detection Module
================
This module contains all detection-related functions including:
- AI anomaly detection using Isolation Forest
- Sentiment analysis using TextBlob
- Risk scoring and gamification functions
"""

import random
import numpy as np
from datetime import datetime
from sklearn.ensemble import IsolationForest
from textblob import TextBlob

from config import (
    AI_CONTAMINATION, AI_MIN_SAMPLES, AI_ANOMALY_RISK_PENALTY, AI_RETRAIN_INTERVAL,
    NEGATIVE_SENTIMENT_THRESHOLD, NEGATIVE_SENTIMENT_RISK_PENALTY, SENTIMENT_ANALYSIS_PROBABILITY,
    SIMULATED_MESSAGES, SECURITY_POINTS_NORMAL_ACTIVITY, SECURITY_POINTS_LOW_RISK_ACTIVITY,
    SECURITY_POINTS_PER_DECAY_CYCLE, RISK_LOW, USERS
)


class AnomalyDetector:
    """AI-based anomaly detection using Isolation Forest algorithm."""
    
    def __init__(self):
        self.model = None
        self.historical_data = []
        self.activities_since_training = 0
    
    def collect_training_data(self, risk_scores):
        """
        Collect current risk score patterns for AI model training.
        Stores feature vectors: [user_risk_score, avg_risk_score, max_risk_score]
        
        Args:
            risk_scores: Dictionary of user_id -> risk_score
        """
        all_scores = list(risk_scores.values())
        avg_risk = sum(all_scores) / len(all_scores) if all_scores else 0
        max_risk = max(all_scores) if all_scores else 0
        
        for user_id, risk_score in risk_scores.items():
            feature_vector = [risk_score, avg_risk, max_risk]
            self.historical_data.append(feature_vector)
    
    def train_model(self):
        """Train the Isolation Forest model on historical risk score data."""
        if len(self.historical_data) < AI_MIN_SAMPLES:
            return
        
        try:
            training_data = np.array(self.historical_data)
            self.model = IsolationForest(
                contamination=AI_CONTAMINATION,
                random_state=42,
                n_estimators=100
            )
            self.model.fit(training_data)
        except Exception as e:
            print(f"Model training error: {e}")
            self.model = None
    
    def detect_anomaly(self, user_id, risk_scores):
        """
        Use Isolation Forest to detect anomalous user behavior.
        
        Args:
            user_id: ID of the user to check
            risk_scores: Dictionary of all user risk scores
            
        Returns:
            True if anomaly detected, False otherwise
        """
        if self.model is None:
            return False
        
        try:
            all_scores = list(risk_scores.values())
            avg_risk = sum(all_scores) / len(all_scores) if all_scores else 0
            max_risk = max(all_scores) if all_scores else 0
            
            current_user_risk = risk_scores[user_id]
            feature_vector = np.array([[current_user_risk, avg_risk, max_risk]])
            prediction = self.model.predict(feature_vector)
            
            return prediction[0] == -1
        except Exception as e:
            print(f"Anomaly detection error: {e}")
            return False


class SentimentAnalyzer:
    """Sentiment analysis for user communications using TextBlob."""
    
    @staticmethod
    def analyze_sentiment(user_id, user_status, risk_scores, activity_table, total_activities):
        """
        Analyze sentiment of a simulated user communication message.
        
        Args:
            user_id: ID of the user
            user_status: Current user status (ACTIVE/LOCKED)
            risk_scores: Dictionary of risk scores (will be modified)
            activity_table: Activity log table to insert results
            total_activities: Counter for total activities
            
        Returns:
            Tuple of (risk_increase, updated_total_activities)
        """
        from config import USER_STATUS_ACTIVE
        
        if user_status != USER_STATUS_ACTIVE:
            return 0, total_activities
        
        message = random.choice(SIMULATED_MESSAGES)
        
        try:
            blob = TextBlob(message)
            sentiment_score = blob.sentiment.polarity
        except Exception:
            sentiment_score = 0.0
        
        if sentiment_score < NEGATIVE_SENTIMENT_THRESHOLD:
            sentiment_label = "Negative"
            is_negative = True
        elif sentiment_score > 0.1:
            sentiment_label = "Positive"
            is_negative = False
        else:
            sentiment_label = "Neutral"
            is_negative = False
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        risk_increase = 0
        
        if is_negative:
            risk_increase = NEGATIVE_SENTIMENT_RISK_PENALTY
            if user_id in risk_scores:
                risk_scores[user_id] = max(0, risk_scores[user_id] + risk_increase)
        
        display_message = message[:50] + "..." if len(message) > 50 else message
        activity_description = f"Communication Sentiment: {sentiment_label} (Score: {sentiment_score:.2f}) - \"{display_message}\""
        
        if activity_table:
            activity_table.insert("", 0, values=(timestamp, user_id, activity_description, risk_increase))
        
        return risk_increase, total_activities + 1


class SecurityPointsManager:
    """Manages security points for gamification feature."""
    
    @staticmethod
    def award_points(user_id, risk_increase, risk_scores, security_points):
        """
        Award security points to users for good security behavior.
        
        Args:
            user_id: ID of the user
            risk_increase: Risk points from the activity
            risk_scores: Dictionary of current risk scores
            security_points: Dictionary of security points (will be modified)
        """
        if risk_increase == 0:
            security_points[user_id] += SECURITY_POINTS_NORMAL_ACTIVITY
        elif risk_increase == 5:
            security_points[user_id] += SECURITY_POINTS_LOW_RISK_ACTIVITY
        
        if risk_scores[user_id] < RISK_LOW:
            if random.random() < 0.1:
                security_points[user_id] += 0.5
    
    @staticmethod
    def award_decay_points(user_id, user_status, security_points):
        """
        Award points when risk decays (good behavior).
        
        Args:
            user_id: ID of the user
            user_status: Current user status
            security_points: Dictionary of security points (will be modified)
        """
        from config import USER_STATUS_ACTIVE
        
        if user_status == USER_STATUS_ACTIVE:
            security_points[user_id] += SECURITY_POINTS_PER_DECAY_CYCLE


def verify_textblob_setup():
    """Verify that TextBlob and NLTK are properly configured."""
    try:
        test_blob = TextBlob("test")
        _ = test_blob.sentiment.polarity
    except Exception:
        pass

