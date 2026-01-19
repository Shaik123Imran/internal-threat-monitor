# Insider Threat Predictor - Academic Project

A comprehensive insider threat detection system built with Python and Tkinter that uses multiple detection methodologies including rule-based scoring, AI-powered anomaly detection, and sentiment analysis.

## Features

- **Rule-Based Risk Scoring**: Assigns risk points based on user activities
- **AI-Powered Anomaly Detection**: Uses Isolation Forest algorithm to detect anomalous behavior patterns
- **Sentiment Analysis**: Analyzes user communications for negative sentiment using TextBlob
- **User Status Management**: Tracks user account states (ACTIVE/LOCKED)
- **Gamification**: Security awareness mechanism rewarding good behavior
- **Real-Time Dashboard**: Visual representation with color coding and progress bars
- **Data Export**: CSV export functionality for activity logs and incidents
- **MongoDB Integration**: Persistent storage for events, incidents, and user data
- **Dynamic Data Loading**: Load events from URLs or local files (CSV/JSON)
- **Hybrid Processing**: Seamlessly switches between real events and simulation

## Technologies Used

- Python 3.x
- Tkinter: GUI framework
- NumPy: Numerical computing
- scikit-learn: Machine learning (Isolation Forest)
- TextBlob: Natural language processing for sentiment analysis
- MongoDB: Database for persistent storage
- pymongo: MongoDB Python driver
- requests: HTTP library for URL data loading

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shaik123Imran/internal-threat-monitor.git
cd internal-threat-monitor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Download NLTK data for TextBlob:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

4. **Install and start MongoDB** (for dynamic data loading):
   - **Windows**: Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
   - **macOS**: `brew install mongodb-community`
   - **Linux**: `sudo apt-get install mongodb` or follow [MongoDB Installation Guide](https://docs.mongodb.com/manual/installation/)
   
   Start MongoDB service:
   ```bash
   # Windows (run as administrator)
   net start MongoDB
   
   # macOS/Linux
   sudo systemctl start mongod
   # or
   mongod
   ```

## Usage

### Basic Usage

Run the application:
```bash
# With default MongoDB URI (localhost:27017)
python main.py

# With custom MongoDB URI
python main.py "mongodb://your-connection-string"
```

### Dynamic Data Loading

The application supports loading real event data from URLs or local files:

1. **Load from URL**: 
   - Click "📥 Load Event Data (URL/File)" button
   - Enter a URL pointing to a JSON or CSV file
   - Events will be loaded into MongoDB and processed automatically

2. **Load from File**:
   - Click "📥 Load Event Data (URL/File)" button
   - Select a local CSV or JSON file
   - Events will be loaded into MongoDB and processed automatically

3. **Event Format**:
   - **CSV**: Must include columns: `timestamp`, `user_id`, `activity`
   - **JSON**: Array of objects with fields: `timestamp`, `user_id`, `activity`
   - Optional fields: `risk_increase`, `details`, `ip_address`, `file_path`, `url`

4. **Hybrid Mode**: 
   - If no real events are available in the database, the system automatically falls back to random simulation
   - Real events are processed first, then simulation continues

### Application Controls

- **Start Monitoring**: Begins activity simulation and risk assessment
- **Stop Monitoring**: Halts activity simulation
- **Pause/Resume**: Temporarily pause activity generation
- **Reset All Risk Scores**: Clears all data and unlocks users
- **Export Activity Log**: Export activity log to CSV
- **Export Incidents**: Export incident alerts to CSV

## Project Structure

```
internal-threat-monitor/
├── main.py              # Main application entry point
├── config.py            # Configuration and constants
├── gui_styles.py        # GUI styling and themes
├── detection.py         # Detection modules (AI, sentiment, gamification)
├── gui_components.py    # GUI component builders
├── storage.py           # MongoDB database operations
├── data_loader.py       # URL and file data loading
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Module Description

1. **config.py**: All configuration parameters, user definitions, risk rules, and thresholds
2. **gui_styles.py**: Color schemes, progress bar styles, and theme settings
3. **detection.py**: AI anomaly detection, sentiment analysis, and security points management
4. **gui_components.py**: Functions for building GUI components (tables, buttons, panels)
5. **storage.py**: MongoDB database operations for events, incidents, and user data
6. **data_loader.py**: Handles loading events from URLs and local files (CSV/JSON)
7. **main.py**: Main application class that integrates all modules

## Academic Purpose

This project demonstrates:
- Integration of multiple detection methodologies (rule-based, ML, NLP)
- Real-time monitoring and alerting systems
- User interface design for security dashboards
- Gamification as a security awareness mechanism
- Data visualization and risk assessment techniques

## License

Academic Project - For educational purposes only

## Author

[Imran Shaik]
[Insider Threat Predictor]
