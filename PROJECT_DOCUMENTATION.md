# Insider Threat Predictor - Project Documentation
## Comprehensive Guide for College Review

**Project Title:** Insider Threat Detection and Risk Assessment System  
**Author:** Imran Shaik  
**Course:** Insider Threat Predictor  
**Date:** February 2026

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Installation Guide](#installation-guide)
4. [How to Access and Run](#how-to-access-and-run)
5. [How It Works - Step by Step](#how-it-works---step-by-step)
6. [Key Features Explained](#key-features-explained)
7. [Technical Implementation](#technical-implementation)
8. [Database Structure](#database-structure)
9. [Testing and Usage Examples](#testing-and-usage-examples)
10. [Future Enhancements](#future-enhancements)

---

## Project Overview

### What is This Project?

The **Insider Threat Predictor** is a comprehensive security monitoring system designed to detect and assess potential insider threats within an organization. It combines multiple detection methodologies including rule-based scoring, AI-powered anomaly detection, and sentiment analysis to provide real-time risk assessment.

### Problem Statement

Organizations face significant risks from insider threats - employees or authorized users who may intentionally or unintentionally cause harm. Traditional security systems focus on external threats, but insider threats require different detection approaches:

- **Behavioral Analysis**: Understanding normal vs. anomalous user behavior
- **Risk Scoring**: Quantifying threat levels based on activities
- **Real-time Monitoring**: Continuous assessment of user actions
- **Automated Alerting**: Immediate notification of high-risk incidents

### Solution Approach

This project implements a multi-layered detection system:

1. **Rule-Based Detection**: Assigns risk points based on predefined activity types
2. **AI-Powered Anomaly Detection**: Uses machine learning (Isolation Forest) to identify unusual patterns
3. **Sentiment Analysis**: Analyzes user communications for negative sentiment
4. **Gamification**: Encourages good security behavior through positive reinforcement
5. **Database Integration**: Persistent storage using MongoDB for real-world data

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (Tkinter GUI Dashboard)                    │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐      ┌─────────▼──────────┐
│  Event Loader  │      │  Detection Engine  │
│  (URL/File)    │      │  (AI + Rules)       │
└───────┬────────┘      └─────────┬──────────┘
        │                         │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   MongoDB Database      │
        │   (Persistent Storage)  │
        └─────────────────────────┘
```

### Module Structure

1. **main.py** - Main application controller
2. **config.py** - Configuration and constants
3. **gui_components.py** - GUI component builders
4. **gui_styles.py** - Styling and themes
5. **detection.py** - AI detection and sentiment analysis
6. **storage.py** - MongoDB database operations
7. **data_loader.py** - URL and file data loading

---

## Installation Guide

### Prerequisites

- **Python 3.8 or higher**
- **MongoDB** (for dynamic data loading)
- **Internet connection** (for downloading dependencies)

### Step-by-Step Installation

#### Step 1: Clone the Repository

```bash
git clone https://github.com/Shaik123Imran/internal-threat-monitor.git
cd internal-threat-monitor
```

#### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning library
- `textblob` - Natural language processing
- `pymongo` - MongoDB driver
- `requests` - HTTP library for URL loading

#### Step 3: Install MongoDB

**Windows:**
1. Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
2. Run the installer
3. Start MongoDB service:
   ```bash
   net start MongoDB
   ```

**macOS:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongod
```

#### Step 4: Download NLTK Data (Optional but Recommended)

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

This improves sentiment analysis accuracy.

---

## How to Access and Run

### Method 1: Default MongoDB (Localhost)

```bash
python main.py
```

The application will:
1. Connect to MongoDB at `mongodb://localhost:27017/`
2. Show a data loading dialog (if MongoDB is connected)
3. Start the dashboard interface

### Method 2: Custom MongoDB URI

```bash
python main.py "mongodb://your-connection-string"
```

Example:
```bash
python main.py "mongodb+srv://username:password@cluster.mongodb.net/"
```

### Application Startup Flow

1. **Initialization**: Application window opens
2. **Database Connection**: Attempts to connect to MongoDB
3. **Data Loading Dialog**: If connected, prompts to load data from URL or file
4. **Dashboard Ready**: Main interface displays with all controls

---

## How It Works - Step by Step

### Phase 1: Initialization

1. **Application Launch**
   - Creates main window (1300x750 pixels)
   - Initializes data structures (risk scores, user status, security points)
   - Connects to MongoDB database
   - Builds user interface components

2. **Database Connection**
   - Attempts connection to MongoDB
   - Creates collections: `events`, `incidents`, `users`, `risk_scores`
   - Sets up indexes for performance
   - Displays connection status

3. **Data Loading Prompt**
   - If MongoDB connected: Shows dialog to load events
   - Options: Load from URL, Load from File, or Skip (use simulation)
   - Events are validated and stored in database

### Phase 2: Event Processing

#### Real Event Processing (When Data Loaded)

1. **Event Retrieval**
   - System queries MongoDB for unprocessed events
   - Events sorted chronologically (oldest first)
   - One event processed per simulation cycle

2. **Event Validation**
   - Checks user_id exists in system
   - Validates activity type matches risk rules
   - Extracts optional fields (details, IP address, etc.)

3. **Risk Calculation**
   - Gets risk points from event or calculates from activity type
   - Updates user's risk score
   - Awards security points for good behavior (gamification)

#### Simulation Mode (When No Real Events)

1. **Random Activity Generation**
   - Randomly selects user and activity type
   - Calculates risk increase based on activity
   - Generates timestamp

2. **Database Storage**
   - Saves simulated events to MongoDB
   - Marks source as "simulation"
   - Enables future analysis

### Phase 3: Detection and Analysis

#### Rule-Based Detection

1. **Risk Score Accumulation**
   - Each activity adds risk points
   - Risk scores accumulate over time
   - Threshold: 20 points triggers incident

2. **Risk Level Categorization**
   - **Low Risk** (0-5): Green indicator
   - **Medium Risk** (6-15): Yellow indicator
   - **High Risk** (16+): Red indicator

#### AI Anomaly Detection

1. **Data Collection**
   - System collects historical risk patterns
   - Features: [user_risk, average_risk, max_risk]
   - Minimum 10 samples required for training

2. **Model Training**
   - Uses Isolation Forest algorithm
   - Trains on normal behavior patterns
   - Retrains every 50 activities

3. **Anomaly Detection**
   - Compares current user pattern to learned patterns
   - Flags anomalies (unusual behavior)
   - Adds 8 risk points for detected anomalies

#### Sentiment Analysis

1. **Communication Monitoring**
   - Randomly analyzes user messages (30% probability)
   - Uses TextBlob for sentiment scoring
   - Range: -1 (very negative) to +1 (very positive)

2. **Risk Adjustment**
   - Negative sentiment (< 0.0): Adds 6 risk points
   - Positive/Neutral: No risk increase
   - Logs sentiment analysis results

### Phase 4: Alerting and Response

1. **Incident Detection**
   - Monitors risk scores continuously
   - When threshold exceeded (≥20 points):
     - Creates incident alert
     - Locks user account
     - Resets risk score to 0
     - Saves incident to database

2. **User Status Management**
   - **ACTIVE**: User can accumulate risk
   - **LOCKED**: User cannot accumulate risk
   - Auto-unlock when risk decays to 0

3. **Gamification**
   - Users earn security points for:
     - Normal activities (0 risk): +1 point
     - Low-risk activities (5 risk): +0.5 points
     - Risk decay: +0.5 points per cycle
   - Encourages security-conscious behavior

### Phase 5: Risk Decay

1. **Natural Risk Reduction**
   - Every 5 seconds, all risk scores decrease by 1
   - Simulates natural risk reduction over time
   - Prevents indefinite risk accumulation

2. **Auto-Unlock**
   - Locked users automatically unlock when risk reaches 0
   - Allows users to return to normal monitoring

---

## Key Features Explained

### 1. Real-Time Dashboard

**Visual Components:**
- **User Risk Scores Table**: Shows all users with color-coded risk levels
- **Progress Bars**: Visual representation of risk levels per user
- **Activity Log**: Real-time feed of all user activities
- **Incident Alerts**: List of security incidents and AI detections
- **Statistics Panel**: Total activities, average risk, highest risk

**Color Coding:**
- 🟢 **Green**: Low risk (0-5 points)
- 🟡 **Yellow**: Medium risk (6-15 points)
- 🔴 **Red**: High risk (16+ points)
- 🔒 **Locked**: User account locked

### 2. Dynamic Data Loading

**Supported Formats:**

**CSV Format:**
```csv
timestamp,user_id,activity,risk_increase,details,ip_address
2024-01-15T10:30:00,user_A,file_download,5,Downloaded sensitive file,192.168.1.100
2024-01-15T10:35:00,user_B,login_from_unusual_ip,8,Login from new location,203.0.113.50
```

**JSON Format:**
```json
[
  {
    "timestamp": "2024-01-15T10:30:00",
    "user_id": "user_A",
    "activity": "file_download",
    "risk_increase": 5,
    "details": "Downloaded sensitive file",
    "ip_address": "192.168.1.100"
  }
]
```

**Loading Methods:**
- **From URL**: Enter URL pointing to JSON/CSV file
- **From File**: Select local CSV/JSON file
- **Validation**: System validates all events before processing

### 3. AI-Powered Anomaly Detection

**Algorithm: Isolation Forest**
- Unsupervised learning algorithm
- Detects anomalies without labeled data
- Works well with small datasets (academic-friendly)

**How It Works:**
1. Collects historical risk patterns
2. Trains model on "normal" behavior
3. Flags patterns that deviate significantly
4. Adds risk penalty for anomalies

**Advantages:**
- No need for labeled threat data
- Adapts to organization's normal patterns
- Detects subtle anomalies

### 4. Sentiment Analysis

**Technology: TextBlob**
- Natural language processing library
- Analyzes text sentiment (positive/negative/neutral)
- Polarity score: -1 to +1

**Use Case:**
- Monitors user communications
- Detects negative sentiment (potential disgruntlement)
- Adds risk points for concerning messages

**Example:**
- Message: "I'm frustrated with this company"
- Sentiment: -0.65 (negative)
- Action: +6 risk points

### 5. Gamification System

**Purpose:** Encourage positive security behavior

**Point System:**
- Normal activities: +1 security point
- Low-risk activities: +0.5 security points
- Risk decay: +0.5 security points per cycle
- Bonus: Random bonuses for maintaining low risk

**Benefits:**
- Positive reinforcement
- Security awareness training
- Behavioral change encouragement

---

## Technical Implementation

### Risk Scoring Rules

| Activity | Risk Points | Description |
|----------|-------------|-------------|
| normal | 0 | Regular user activity |
| file_download | 5 | Downloading files |
| login_from_unusual_ip | 8 | Login from new location |
| access_sensitive_folder | 10 | Accessing sensitive data |
| data_copy_to_usb | 15 | Potential data exfiltration |

### Risk Thresholds

- **Incident Threshold**: 20 points
- **Low Risk**: 0-5 points
- **Medium Risk**: 6-15 points
- **High Risk**: 16+ points

### Timing Parameters

- **Activity Simulation**: Every 1.2 seconds
- **Risk Decay**: Every 5 seconds (-1 point)
- **AI Retraining**: Every 50 activities
- **Sentiment Analysis**: 30% probability per activity

### Database Collections

**events**
- Stores all user activities
- Fields: timestamp, user_id, activity, risk_increase, details, source
- Indexed on: timestamp, user_id, processed

**incidents**
- Stores security incidents
- Fields: timestamp, user_id, risk_score, message, alert_type
- Indexed on: timestamp

**users**
- User profiles (optional, can use config.py)
- Fields: user_id, role, metadata

**risk_scores**
- Historical risk score snapshots
- Fields: timestamp, risk_scores (dictionary)

---

## Database Structure

### MongoDB Collections Schema

#### Events Collection
```javascript
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "user_id": "user_A",
  "activity": "file_download",
  "risk_increase": 5,
  "details": "Downloaded sensitive file",
  "source": "File: events.csv",
  "ip_address": "192.168.1.100",
  "file_path": "/data/file.txt",
  "processed": false,
  "created_at": ISODate,
  "processed_at": ISODate
}
```

#### Incidents Collection
```javascript
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "user_id": "user_A",
  "risk_score": 20,
  "message": "HIGH-RISK ALERT: user_A (developer) triggered security incident",
  "user_role": "developer",
  "alert_type": "RULE_BASED" | "AI_ANOMALY",
  "created_at": ISODate
}
```

---

## Testing and Usage Examples

### Example 1: Loading Data from File

1. **Create Sample CSV File:**
```csv
timestamp,user_id,activity,risk_increase,details
2024-01-15T10:00:00,user_A,file_download,5,Downloaded project files
2024-01-15T10:05:00,user_B,access_sensitive_folder,10,Accessed HR folder
2024-01-15T10:10:00,user_C,data_copy_to_usb,15,Copied files to USB
```

2. **Load in Application:**
   - Click "📥 Load Event Data (URL/File)"
   - Select "📁 Load from File"
   - Choose your CSV file
   - System validates and loads events

3. **Start Monitoring:**
   - Click "▶ Start Monitoring"
   - Events process chronologically
   - Risk scores update in real-time

### Example 2: Loading Data from URL

1. **Host JSON File:**
   - Upload events.json to web server
   - Get public URL (e.g., https://example.com/events.json)

2. **Load in Application:**
   - Click "📥 Load Event Data (URL/File)"
   - Enter URL in text field
   - Click "Load from URL"
   - System fetches and validates data

### Example 3: Simulated Mode

1. **Skip Data Loading:**
   - Click "Skip (Use Simulated Data)"
   - System generates random activities
   - All events saved to database

2. **Monitor Activities:**
   - Watch real-time activity log
   - Observe risk score changes
   - See AI anomaly detection in action

---

## User Interface Guide

### Main Dashboard Components

#### 1. Control Buttons (Top Section)

- **▶ Start Monitoring**: Begins activity processing
- **⏹ Stop Monitoring**: Halts all activity processing
- **🔄 Reset All Risk Scores**: Clears all data and unlocks users
- **⏸ Pause / ▶ Resume**: Temporarily pause activity generation
- **📥 Load Event Data**: Load events from URL or file
- **📥 Export Activity Log**: Export to CSV
- **📥 Export Incidents**: Export incidents to CSV

#### 2. User Risk Scores Table

Displays:
- User ID
- Role
- Current Risk Score
- Status (ACTIVE/LOCKED)
- Security Score (gamification points)

Color-coded rows indicate risk level.

#### 3. Progress Bars

Visual representation:
- Green bar: Low risk
- Yellow bar: Medium risk
- Red bar: High risk
- Locked indicator: 🔒 LOCKED

#### 4. Activity Log Tab

Shows:
- Timestamp
- User ID
- Activity Description
- Risk Increase

#### 5. Incident Alerts Tab

Shows:
- Timestamp
- User ID
- Risk Score
- Alert Message

#### 6. Statistics Panel

Displays:
- Total Activities
- Average Risk Score
- Highest Risk Score

---

## Workflow Demonstration

### Complete Workflow Example

**Scenario:** Monitoring user activities for potential insider threats

1. **Launch Application**
   ```
   python main.py
   ```

2. **Load Event Data**
   - Dialog appears: "Load Event Data"
   - Choose: "📁 Load from File"
   - Select: `sample_events.csv`
   - Result: "Successfully loaded 50 events!"

3. **Start Monitoring**
   - Click: "▶ Start Monitoring"
   - System begins processing events chronologically

4. **Observe Real-Time Updates**
   - Activity log shows events as they process
   - Risk scores increase based on activities
   - Progress bars update with colors

5. **AI Detection Triggers**
   - After 10 events, AI model trains
   - Detects anomalous pattern for user_B
   - Adds 8 risk points
   - Logs AI alert

6. **Incident Occurs**
   - user_C reaches 20 risk points
   - System triggers incident alert
   - User account locked
   - Incident saved to database

7. **Risk Decay**
   - Every 5 seconds, risk scores decrease
   - Locked user's risk decays to 0
   - User automatically unlocked

8. **Export Data**
   - Click: "📥 Export Incidents"
   - Save: `incidents_2024-01-15.csv`
   - Use for reporting/analysis

---

## Technical Details for Reviewers

### Machine Learning Implementation

**Algorithm:** Isolation Forest (scikit-learn)

**Why Isolation Forest?**
- Unsupervised learning (no labeled data needed)
- Efficient for anomaly detection
- Works well with small datasets
- Academic-friendly implementation

**Features Used:**
- User's current risk score
- Average risk across all users
- Maximum risk in system

**Training:**
- Minimum 10 samples required
- Retrains every 50 activities
- Adapts to changing patterns

### Database Design

**Why MongoDB?**
- Flexible schema for event data
- Easy to add new fields
- Good performance for time-series data
- JSON-like structure matches Python dictionaries

**Indexes:**
- `timestamp`: For chronological sorting
- `user_id`: For user-specific queries
- `processed`: For finding unprocessed events

### Error Handling

**Robust Error Handling:**
- Database connection failures: Graceful fallback to simulation
- Invalid event data: Validation and rejection
- Network errors: User-friendly error messages
- File parsing errors: Detailed error reporting

---

## Future Enhancements

### Planned Improvements

1. **Real-Time Web Monitoring**
   - Monitor actual website logs
   - Parse web server access logs
   - Real-time threat detection

2. **Advanced Analytics**
   - Risk trend analysis
   - User behavior profiling
   - Predictive threat modeling

3. **Integration Capabilities**
   - SIEM integration
   - Email alerts
   - Slack/Teams notifications

4. **Enhanced AI Models**
   - Deep learning for pattern recognition
   - Time-series analysis
   - Multi-user correlation detection

---

## Conclusion

This project demonstrates:

✅ **Multi-layered Security Detection**
- Rule-based scoring
- AI-powered anomaly detection
- Sentiment analysis

✅ **Real-World Application**
- MongoDB database integration
- Dynamic data loading
- Persistent storage

✅ **User-Friendly Interface**
- Intuitive dashboard
- Real-time updates
- Visual indicators

✅ **Academic Excellence**
- Clean code structure
- Comprehensive documentation
- Modular design

---

## Contact and Support

**Repository:** https://github.com/Shaik123Imran/internal-threat-monitor

**For Questions:**
- Review code comments
- Check README.md
- Examine module documentation

---

**Document Version:** 1.0  
**Last Updated:** February 2026
