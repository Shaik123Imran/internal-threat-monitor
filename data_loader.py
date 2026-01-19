"""
Data Loader Module - URL and File Input Handling
================================================
This module handles loading events from URLs and local files.
Supports CSV and JSON formats with enhanced field support.

Enhanced Event Format:
- timestamp: ISO format datetime string
- user_id: User identifier
- activity: Activity type (must match RISK_RULES keys)
- risk_increase: Optional risk points (if not provided, calculated from activity)
- details: Optional additional details about the activity
- source: Optional source of the event (file/url/system)
- ip_address: Optional IP address
- file_path: Optional file path for file-related activities
- url: Optional URL for web-related activities
"""

import csv
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import os


class DataLoader:
    """Handles loading events from URLs and local files."""
    
    @staticmethod
    def load_from_url(url: str, timeout: int = 30) -> tuple[List[Dict], Optional[str]]:
        """
        Load events from a URL (supports JSON and CSV).
        
        Args:
            url: URL to fetch data from
            timeout: Request timeout in seconds
        
        Returns:
            Tuple of (events_list, error_message)
            events_list is empty if error occurred
        """
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            
            # Try JSON first
            if 'json' in content_type or url.endswith('.json'):
                try:
                    data = response.json()
                    return DataLoader._parse_json_data(data, source=f"URL: {url}")
                except json.JSONDecodeError:
                    pass
            
            # Try CSV
            if 'csv' in content_type or url.endswith('.csv'):
                try:
                    csv_data = response.text
                    return DataLoader._parse_csv_data(csv_data, source=f"URL: {url}")
                except Exception as e:
                    return [], f"CSV parsing error: {str(e)}"
            
            # Try to auto-detect format
            try:
                data = response.json()
                return DataLoader._parse_json_data(data, source=f"URL: {url}")
            except:
                try:
                    csv_data = response.text
                    return DataLoader._parse_csv_data(csv_data, source=f"URL: {url}")
                except Exception as e:
                    return [], f"Unable to parse data format: {str(e)}"
                    
        except requests.exceptions.RequestException as e:
            return [], f"Network error: {str(e)}"
        except Exception as e:
            return [], f"Error loading from URL: {str(e)}"
    
    @staticmethod
    def load_from_file(file_path: str) -> tuple[List[Dict], Optional[str]]:
        """
        Load events from a local file (supports JSON and CSV).
        
        Args:
            file_path: Path to the file
        
        Returns:
            Tuple of (events_list, error_message)
        """
        if not os.path.exists(file_path):
            return [], f"File not found: {file_path}"
        
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return DataLoader._parse_json_data(data, source=f"File: {file_path}")
            
            elif file_ext == '.csv':
                with open(file_path, 'r', encoding='utf-8') as f:
                    csv_data = f.read()
                return DataLoader._parse_csv_data(csv_data, source=f"File: {file_path}")
            
            else:
                # Try to auto-detect
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    return DataLoader._parse_json_data(data, source=f"File: {file_path}")
                except:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            csv_data = f.read()
                        return DataLoader._parse_csv_data(csv_data, source=f"File: {file_path}")
                    except Exception as e:
                        return [], f"Unable to parse file format: {str(e)}"
                        
        except Exception as e:
            return [], f"Error reading file: {str(e)}"
    
    @staticmethod
    def _parse_json_data(data: any, source: str = "") -> tuple[List[Dict], Optional[str]]:
        """
        Parse JSON data into event list.
        Supports both list of events and single event object.
        
        Args:
            data: JSON data (list or dict)
            source: Source identifier for events
        
        Returns:
            Tuple of (events_list, error_message)
        """
        events = []
        
        try:
            # If it's a list of events
            if isinstance(data, list):
                for item in data:
                    event = DataLoader._normalize_event(item, source)
                    if event:
                        events.append(event)
            
            # If it's a single event object
            elif isinstance(data, dict):
                event = DataLoader._normalize_event(data, source)
                if event:
                    events.append(event)
            
            # If it's nested (e.g., {"events": [...]})
            elif isinstance(data, dict) and 'events' in data:
                for item in data['events']:
                    event = DataLoader._normalize_event(item, source)
                    if event:
                        events.append(event)
            
            return events, None
            
        except Exception as e:
            return [], f"JSON parsing error: {str(e)}"
    
    @staticmethod
    def _parse_csv_data(csv_data: str, source: str = "") -> tuple[List[Dict], Optional[str]]:
        """
        Parse CSV data into event list.
        Supports enhanced CSV format with multiple columns.
        
        Args:
            csv_data: CSV string data
            source: Source identifier for events
        
        Returns:
            Tuple of (events_list, error_message)
        """
        events = []
        
        try:
            csv_reader = csv.DictReader(csv_data.splitlines())
            
            for row in csv_reader:
                event = DataLoader._normalize_event(row, source)
                if event:
                    events.append(event)
            
            return events, None
            
        except Exception as e:
            return [], f"CSV parsing error: {str(e)}"
    
    @staticmethod
    def _normalize_event(raw_event: Dict, source: str = "") -> Optional[Dict]:
        """
        Normalize event data to standard format.
        Handles various field names and formats.
        
        Args:
            raw_event: Raw event dictionary
            source: Source identifier
        
        Returns:
            Normalized event dictionary or None if invalid
        """
        from config import RISK_RULES, USERS
        
        # Extract user_id (handle various field names)
        user_id = (
            raw_event.get('user_id') or 
            raw_event.get('user') or 
            raw_event.get('username') or
            raw_event.get('userId')
        )
        
        # Extract activity (handle various field names)
        activity = (
            raw_event.get('activity') or 
            raw_event.get('action') or 
            raw_event.get('event_type') or
            raw_event.get('type')
        )
        
        # Validate required fields
        if not user_id or not activity:
            return None
        
        # Validate user exists
        if user_id not in USERS:
            return None
        
        # Validate activity exists in RISK_RULES
        if activity not in RISK_RULES:
            return None
        
        # Extract timestamp (handle various formats)
        timestamp = raw_event.get('timestamp') or raw_event.get('time') or raw_event.get('date')
        if not timestamp:
            timestamp = datetime.now().isoformat()
        elif isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()
        
        # Build normalized event
        normalized = {
            'timestamp': timestamp,
            'user_id': user_id,
            'activity': activity,
            'source': source or raw_event.get('source', 'unknown')
        }
        
        # Add optional enhanced fields
        if 'risk_increase' in raw_event:
            normalized['risk_increase'] = int(raw_event['risk_increase'])
        
        if 'details' in raw_event:
            normalized['details'] = str(raw_event['details'])
        
        if 'ip_address' in raw_event or 'ip' in raw_event:
            normalized['ip_address'] = raw_event.get('ip_address') or raw_event.get('ip')
        
        if 'file_path' in raw_event or 'filepath' in raw_event:
            normalized['file_path'] = raw_event.get('file_path') or raw_event.get('filepath')
        
        if 'url' in raw_event:
            normalized['url'] = raw_event.get('url')
        
        # Copy any other fields that might be useful
        for key in ['severity', 'category', 'description', 'metadata']:
            if key in raw_event:
                normalized[key] = raw_event[key]
        
        return normalized
    
    @staticmethod
    def create_sample_csv_file(file_path: str, num_events: int = 50):
        """
        Create a sample CSV file for testing.
        
        Args:
            file_path: Path where to create the file
            num_events: Number of sample events to generate
        """
        from config import USERS, RISK_RULES
        import random
        
        activities = list(RISK_RULES.keys())
        users = list(USERS.keys())
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'user_id', 'activity', 'risk_increase', 
                'details', 'ip_address', 'file_path'
            ])
            writer.writeheader()
            
            for i in range(num_events):
                timestamp = datetime.now().isoformat()
                user = random.choice(users)
                activity = random.choice(activities)
                risk = RISK_RULES[activity]
                
                writer.writerow({
                    'timestamp': timestamp,
                    'user_id': user,
                    'activity': activity,
                    'risk_increase': risk,
                    'details': f'Sample event {i+1}',
                    'ip_address': f'192.168.1.{random.randint(1, 255)}',
                    'file_path': f'/data/file_{i}.txt' if activity in ['file_download', 'data_copy_to_usb'] else ''
                })
    
    @staticmethod
    def create_sample_json_file(file_path: str, num_events: int = 50):
        """
        Create a sample JSON file for testing.
        
        Args:
            file_path: Path where to create the file
            num_events: Number of sample events to generate
        """
        from config import USERS, RISK_RULES
        import random
        
        activities = list(RISK_RULES.keys())
        users = list(USERS.keys())
        
        events = []
        for i in range(num_events):
            timestamp = datetime.now().isoformat()
            user = random.choice(users)
            activity = random.choice(activities)
            risk = RISK_RULES[activity]
            
            event = {
                'timestamp': timestamp,
                'user_id': user,
                'activity': activity,
                'risk_increase': risk,
                'details': f'Sample event {i+1}',
                'ip_address': f'192.168.1.{random.randint(1, 255)}',
            }
            
            if activity in ['file_download', 'data_copy_to_usb']:
                event['file_path'] = f'/data/file_{i}.txt'
            
            events.append(event)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2)
