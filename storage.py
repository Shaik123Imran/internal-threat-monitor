"""
Storage Module - MongoDB Database Operations
===========================================
This module handles all database operations for storing and retrieving
events, incidents, and user data from MongoDB.

Collections:
- events: Raw user activity events from files/URLs
- incidents: Generated security incidents
- users: User profiles and metadata
- risk_scores: Current risk scores for users (for persistence)
"""

from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional
import json


class DatabaseManager:
    """
    Manages MongoDB database connections and operations.
    Handles all CRUD operations for events, incidents, and user data.
    """
    
    def __init__(self, connection_uri: str = "mongodb://localhost:27017/", database_name: str = "insider_threat"):
        """
        Initialize database connection.
        
        Args:
            connection_uri: MongoDB connection string
            database_name: Name of the database to use
        """
        try:
            self.client = MongoClient(connection_uri)
            self.db = self.client[database_name]
            self.events_collection = self.db["events"]
            self.incidents_collection = self.db["incidents"]
            self.users_collection = self.db["users"]
            self.risk_scores_collection = self.db["risk_scores"]
            
            # Create indexes for better query performance
            self.events_collection.create_index("timestamp")
            self.events_collection.create_index("user_id")
            self.events_collection.create_index("processed", sparse=True)
            self.incidents_collection.create_index("timestamp")
            
        except Exception as e:
            print(f"Database connection error: {e}")
            self.client = None
            self.db = None
    
    def is_connected(self) -> bool:
        """Check if database connection is active."""
        if self.client is None:
            return False
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False
    
    def save_event(self, event_data: Dict) -> bool:
        """
        Save a single event to the database.
        
        Args:
            event_data: Dictionary containing event information
                Required: timestamp, user_id, activity
                Optional: risk_increase, details, source, ip_address, etc.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            # Ensure timestamp is datetime object
            if isinstance(event_data.get('timestamp'), str):
                event_data['timestamp'] = datetime.fromisoformat(event_data['timestamp'].replace('Z', '+00:00'))
            elif not isinstance(event_data.get('timestamp'), datetime):
                event_data['timestamp'] = datetime.now()
            
            # Add metadata
            event_data['created_at'] = datetime.now()
            event_data['processed'] = False  # Mark as unprocessed initially
            
            self.events_collection.insert_one(event_data)
            return True
        except Exception as e:
            print(f"Error saving event: {e}")
            return False
    
    def save_events_batch(self, events: List[Dict]) -> int:
        """
        Save multiple events in a batch operation.
        
        Args:
            events: List of event dictionaries
        
        Returns:
            Number of events successfully saved
        """
        if not self.is_connected():
            return 0
        
        try:
            # Process timestamps and add metadata
            for event in events:
                if isinstance(event.get('timestamp'), str):
                    try:
                        event['timestamp'] = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                    except:
                        event['timestamp'] = datetime.now()
                elif not isinstance(event.get('timestamp'), datetime):
                    event['timestamp'] = datetime.now()
                
                event['created_at'] = datetime.now()
                event['processed'] = False
            
            result = self.events_collection.insert_many(events)
            return len(result.inserted_ids)
        except Exception as e:
            print(f"Error saving events batch: {e}")
            return 0
    
    def get_next_unprocessed_event(self) -> Optional[Dict]:
        """
        Get the next unprocessed event from the database.
        Returns events in chronological order.
        
        Returns:
            Event dictionary or None if no events available
        """
        if not self.is_connected():
            return None
        
        try:
            event = self.events_collection.find_one(
                {"processed": False},
                sort=[("timestamp", 1)]  # Sort by timestamp ascending
            )
            
            if event:
                # Convert ObjectId to string for JSON serialization
                event['_id'] = str(event['_id'])
            
            return event
        except Exception as e:
            print(f"Error getting next event: {e}")
            return None
    
    def mark_event_processed(self, event_id: str) -> bool:
        """
        Mark an event as processed.
        
        Args:
            event_id: MongoDB _id of the event
        
        Returns:
            True if successful
        """
        if not self.is_connected():
            return False
        
        try:
            self.events_collection.update_one(
                {"_id": ObjectId(event_id)},
                {"$set": {"processed": True, "processed_at": datetime.now()}}
            )
            return True
        except Exception as e:
            print(f"Error marking event processed: {e}")
            return False
    
    def save_incident(self, incident_data: Dict) -> bool:
        """
        Save an incident to the database.
        
        Args:
            incident_data: Dictionary containing incident information
                Required: timestamp, user_id, risk_score, message
        
        Returns:
            True if successful
        """
        if not self.is_connected():
            return False
        
        try:
            if isinstance(incident_data.get('timestamp'), str):
                incident_data['timestamp'] = datetime.fromisoformat(incident_data['timestamp'].replace('Z', '+00:00'))
            elif not isinstance(incident_data.get('timestamp'), datetime):
                incident_data['timestamp'] = datetime.now()
            
            incident_data['created_at'] = datetime.now()
            self.incidents_collection.insert_one(incident_data)
            return True
        except Exception as e:
            print(f"Error saving incident: {e}")
            return False
    
    def get_all_incidents(self, limit: int = 100) -> List[Dict]:
        """
        Get all incidents from the database.
        
        Args:
            limit: Maximum number of incidents to retrieve
        
        Returns:
            List of incident dictionaries
        """
        if not self.is_connected():
            return []
        
        try:
            incidents = list(self.incidents_collection.find().sort("timestamp", -1).limit(limit))
            for incident in incidents:
                incident['_id'] = str(incident['_id'])
            return incidents
        except Exception as e:
            print(f"Error getting incidents: {e}")
            return []
    
    def save_risk_scores(self, risk_scores: Dict[str, int]) -> bool:
        """
        Save current risk scores for all users.
        
        Args:
            risk_scores: Dictionary mapping user_id to risk_score
        
        Returns:
            True if successful
        """
        if not self.is_connected():
            return False
        
        try:
            document = {
                "timestamp": datetime.now(),
                "risk_scores": risk_scores
            }
            self.risk_scores_collection.insert_one(document)
            return True
        except Exception as e:
            print(f"Error saving risk scores: {e}")
            return False
    
    def get_unprocessed_event_count(self) -> int:
        """Get count of unprocessed events."""
        if not self.is_connected():
            return 0
        
        try:
            return self.events_collection.count_documents({"processed": False})
        except Exception:
            return 0
    
    def get_total_event_count(self) -> int:
        """Get total count of events."""
        if not self.is_connected():
            return 0
        
        try:
            return self.events_collection.count_documents({})
        except Exception:
            return 0
    
    def clear_processed_events(self) -> int:
        """
        Remove all processed events from database.
        Useful for cleanup.
        
        Returns:
            Number of events deleted
        """
        if not self.is_connected():
            return 0
        
        try:
            result = self.events_collection.delete_many({"processed": True})
            return result.deleted_count
        except Exception as e:
            print(f"Error clearing processed events: {e}")
            return 0
    
    def close(self):
        """Close database connection."""
        if self.client:
            self.client.close()
