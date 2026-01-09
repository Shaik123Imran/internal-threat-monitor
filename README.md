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

## Technologies Used

- Python 3.x
- Tkinter: GUI framework
- NumPy: Numerical computing
- scikit-learn: Machine learning (Isolation Forest)
- TextBlob: Natural language processing for sentiment analysis

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Insider Threat"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Download NLTK data for TextBlob:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

## Usage

Run the application:
```bash
python main.py
```

### Application Controls

- **Start Monitoring**: Begins activity simulation and risk assessment
- **Stop Monitoring**: Halts activity simulation
- **Pause/Resume**: Temporarily pause activity generation
- **Reset All Risk Scores**: Clears all data and unlocks users
- **Export Activity Log**: Export activity log to CSV
- **Export Incidents**: Export incident alerts to CSV

## Project Structure

```
Insider Threat/
├── main.py              # Main application entry point
├── config.py            # Configuration and constants
├── gui_styles.py        # GUI styling and themes
├── detection.py         # Detection modules (AI, sentiment, gamification)
├── gui_components.py    # GUI component builders
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Module Description

1. **config.py**: All configuration parameters, user definitions, risk rules, and thresholds
2. **gui_styles.py**: Color schemes, progress bar styles, and theme settings
3. **detection.py**: AI anomaly detection, sentiment analysis, and security points management
4. **gui_components.py**: Functions for building GUI components (tables, buttons, panels)
5. **main.py**: Main application class that integrates all modules

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

[Your Name]
[Course Name]

