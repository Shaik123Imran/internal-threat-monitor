"""
Configuration Module
====================
This module contains all configuration parameters, constants, and data definitions
for the Insider Threat Predictor application.

It includes:
- User database with role definitions
- Risk scoring rules mapping activities to risk values
- Risk thresholds for alerting and visual color coding
- Timing parameters for activity simulation and risk decay
- AI model configuration (Isolation Forest parameters)
- Sentiment analysis configuration
- Gamification parameters for security awareness
"""

# User database: Maps user IDs to their roles
# Each user is tracked individually for risk scoring
USERS = {
    "user_A": {"role": "developer"},
    "user_B": {"role": "sales"},
    "user_C": {"role": "analyst"},
    "user_D": {"role": "admin"},
}

# Risk scoring rules: Maps activity types to risk point values
# Higher values indicate more suspicious activities
RISK_RULES = {
    "normal": 0,                      # No risk - normal user activity
    "file_download": 5,               # Low risk - downloading files
    "login_from_unusual_ip": 8,       # Medium risk - unusual login location
    "access_sensitive_folder": 10,   # High risk - accessing sensitive data
    "data_copy_to_usb": 15,           # Very high risk - potential data exfiltration
}

# Risk threshold: Score at which an incident alert is triggered
RISK_THRESHOLD = 20

# Risk level thresholds for visual color coding in the GUI
# Used to categorize users into low/medium/high risk groups
RISK_LOW = 5      # Green: Low risk (0-5 points)
RISK_MEDIUM = 15  # Yellow: Medium risk (6-15 points)
RISK_HIGH = 20    # Red: High risk (16+ points)

# Risk decay settings: Risk scores naturally decrease over time
# This simulates the natural reduction of risk as time passes
RISK_DECAY_INTERVAL = 5000  # Decay every 5 seconds (in milliseconds)
RISK_DECAY_AMOUNT = 1       # Decrease risk by 1 point each decay cycle

# Simulation timing: Interval between activity simulations
SIMULATION_INTERVAL = 1200  # 1.2 seconds between activities

# User status constants: Define possible user account states
USER_STATUS_ACTIVE = "ACTIVE"  # User can accumulate risk from activities
USER_STATUS_LOCKED = "LOCKED"  # User is locked and cannot accumulate risk

# Gamification / Security Awareness Configuration
# ===============================================
# This feature implements a security awareness mechanism through gamification.
# Users earn security points for demonstrating good security practices and normal behavior.
# This encourages positive security behavior by rewarding users for:
# - Performing normal, low-risk activities
# - Maintaining low risk scores over time
# - Following security best practices
# The security score serves as a positive reinforcement mechanism to promote
# security-conscious behavior in the organization.

SECURITY_POINTS_NORMAL_ACTIVITY = 1      # Points awarded for normal activities (0 risk)
SECURITY_POINTS_LOW_RISK_ACTIVITY = 0.5  # Points awarded for low-risk activities (5 points)
SECURITY_POINTS_PER_DECAY_CYCLE = 0.5   # Points awarded when risk decays (good behavior)

# AI Anomaly Detection Configuration
# Isolation Forest parameters for lightweight, academic-friendly implementation
AI_CONTAMINATION = 0.1  # Expected proportion of anomalies (10%)
AI_MIN_SAMPLES = 10     # Minimum samples needed before training model
AI_ANOMALY_RISK_PENALTY = 8  # Risk points added when AI detects anomaly
AI_RETRAIN_INTERVAL = 50  # Retrain model after this many activities

# Sentiment Analysis Configuration
# TextBlob sentiment analysis for communication monitoring
NEGATIVE_SENTIMENT_THRESHOLD = 0.0  # Sentiment score below this is considered negative
NEGATIVE_SENTIMENT_RISK_PENALTY = 6  # Risk points added for negative sentiment messages
SENTIMENT_ANALYSIS_PROBABILITY = 0.3  # 30% chance to analyze sentiment per activity

# Simulated user communication messages
# Mix of positive, neutral, and negative sentiment messages
SIMULATED_MESSAGES = [
    # Positive messages
    "Great work on the project! Really impressed with the progress.",
    "Thanks for your help today, I really appreciate it.",
    "The team meeting went well, everyone contributed great ideas.",
    "Looking forward to collaborating on the new feature.",
    "Excellent presentation, very clear and well-organized.",
    
    # Neutral messages
    "Meeting scheduled for 3 PM tomorrow.",
    "Please review the document and provide feedback.",
    "The system update will be deployed tonight.",
    "Can you send me the latest version of the report?",
    "Reminder: Deadline for the project is next Friday.",
    
    # Negative messages (these will trigger risk increase)
    "I'm really frustrated with how things are going here.",
    "This is unacceptable, I can't work under these conditions.",
    "I'm done with this place, nothing ever works properly.",
    "This is a complete waste of my time and effort.",
    "I'm seriously considering leaving this company.",
    "The management doesn't care about us at all.",
    "This project is a disaster and going nowhere.",
    "I hate dealing with these constant problems.",
    "Why does everything have to be so difficult here?",
    "I'm fed up with all these unnecessary restrictions.",
]

