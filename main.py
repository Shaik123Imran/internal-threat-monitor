"""
================================================================================
INSIDER THREAT PREDICTOR - ACADEMIC PROJECT
================================================================================

Project Title: Insider Threat Detection and Risk Assessment System
Author: [Your Name]
Course: [Course Name]
Date: [Submission Date]

Main Application File
=====================
This is the main entry point for the Insider Threat Predictor application.
It integrates all modules and manages the application lifecycle.

Run this file to start the application:
    python main.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import random
import csv
import os

# Import configuration
from config import (
    USERS, RISK_RULES, RISK_THRESHOLD, RISK_LOW, RISK_MEDIUM, RISK_HIGH,
    RISK_DECAY_INTERVAL, RISK_DECAY_AMOUNT, SIMULATION_INTERVAL,
    USER_STATUS_ACTIVE, USER_STATUS_LOCKED,
    AI_ANOMALY_RISK_PENALTY, AI_RETRAIN_INTERVAL,
    SENTIMENT_ANALYSIS_PROBABILITY
)

# Import GUI components and styles
from gui_components import (
    build_user_table, build_logs, build_statistics,
    build_monitoring_controls, build_controls
)
from gui_styles import COLORS, FONTS

# Import detection modules
from detection import (
    AnomalyDetector, SentimentAnalyzer, SecurityPointsManager, verify_textblob_setup
)

# Import database and data loading modules
from storage import DatabaseManager
from data_loader import DataLoader


class InsiderThreatApp:
    """
    Main Application Class: Insider Threat Predictor
    
    This class serves as the central controller for the entire application.
    It integrates all modules and manages the complete lifecycle of the
    insider threat detection system.
    """

    def __init__(self, root, mongodb_uri: str = None):
        """
        Initialize the application window and core components.
        
        Args:
            root: Tkinter root window
            mongodb_uri: MongoDB connection URI (default: mongodb://localhost:27017/)
        """
        self.root = root
        self.root.title("Insider Threat Predictor")
        self.root.geometry("1300x750")
        self.root.configure(bg=COLORS['bg_dark'])

        # Initialize data structures
        self.risk_scores = {user_id: 0 for user_id in USERS.keys()}
        self.user_status = {user_id: USER_STATUS_ACTIVE for user_id in USERS.keys()}
        self.security_points = {user_id: 0.0 for user_id in USERS.keys()}
        
        # Initialize state
        self.simulation_active = False
        self.monitoring_running = False
        self.total_activities = 0
        self.use_real_events = False  # Flag to track if using real events from DB
        
        # Initialize database connection
        default_uri = mongodb_uri or "mongodb://localhost:27017/"
        self.db_manager = DatabaseManager(default_uri)
        self.db_connected = self.db_manager.is_connected()
        
        # Initialize detection modules
        self.anomaly_detector = AnomalyDetector()
        
        # Build UI
        self.build_ui()
        
        # Show data input dialog on startup (if DB connected)
        if self.db_connected:
            self.show_data_input_dialog()
        
        # Start risk decay timer
        self.start_risk_decay()
        
        # Verify TextBlob setup
        verify_textblob_setup()
    
    def show_data_input_dialog(self):
        """
        Show dialog to load data from URL or file.
        This allows users to provide real event data.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Load Event Data")
        dialog.geometry("500x300")
        dialog.configure(bg=COLORS['bg_dark'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"500x300+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Load Event Data",
            font=FONTS['heading'],
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_white']
        ).pack(pady=20)
        
        tk.Label(
            dialog,
            text="Choose data source:",
            font=FONTS['label'],
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_white']
        ).pack(pady=10)
        
        # URL input frame
        url_frame = tk.Frame(dialog, bg=COLORS['bg_dark'])
        url_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            url_frame,
            text="URL:",
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_white'],
            font=FONTS['small']
        ).pack(side="left", padx=5)
        
        url_entry = tk.Entry(url_frame, width=40, font=FONTS['small'])
        url_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        def load_from_url():
            url = url_entry.get().strip()
            if not url:
                messagebox.showwarning("Warning", "Please enter a URL")
                return
            
            self.load_events_from_url(url)
            dialog.destroy()
        
        url_button = tk.Button(
            url_frame,
            text="Load from URL",
            command=load_from_url,
            bg="#4a8a4a",
            fg=COLORS['fg_white'],
            font=FONTS['small'],
            padx=10,
            pady=5
        )
        url_button.pack(side="left", padx=5)
        
        # File input frame
        file_frame = tk.Frame(dialog, bg=COLORS['bg_dark'])
        file_frame.pack(pady=10, padx=20, fill="x")
        
        def load_from_file():
            filename = filedialog.askopenfilename(
                title="Select Event Data File",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("JSON files", "*.json"),
                    ("All files", "*.*")
                ]
            )
            if filename:
                self.load_events_from_file(filename)
                dialog.destroy()
        
        file_button = tk.Button(
            file_frame,
            text="📁 Load from File",
            command=load_from_file,
            bg="#4a4a8a",
            fg=COLORS['fg_white'],
            font=FONTS['small'],
            padx=20,
            pady=8
        )
        file_button.pack(side="left", padx=5)
        
        # Skip button
        def skip_loading():
            messagebox.showinfo("Info", "You can load data later using the 'Load Data' button.\nUsing simulated events for now.")
            dialog.destroy()
        
        skip_button = tk.Button(
            dialog,
            text="Skip (Use Simulated Data)",
            command=skip_loading,
            bg="#4a4a4a",
            fg=COLORS['fg_white'],
            font=FONTS['small'],
            padx=15,
            pady=5
        )
        skip_button.pack(pady=20)
        
        # Database status
        db_status_text = "✓ MongoDB Connected" if self.db_connected else "✗ MongoDB Not Connected"
        db_status_color = COLORS['fg_green'] if self.db_connected else COLORS['fg_red']
        
        tk.Label(
            dialog,
            text=db_status_text,
            bg=COLORS['bg_dark'],
            fg=db_status_color,
            font=FONTS['small']
        ).pack(pady=5)

    def build_ui(self):
        """Build the complete user interface."""
        # Title
        title_label = tk.Label(
            self.root,
            text="Insider Threat Predictor Dashboard",
            font=FONTS['title'],
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_white']
        )
        title_label.pack(anchor="w", padx=20, pady=10)

        # Monitoring controls
        self.start_button, self.stop_button = build_monitoring_controls(
            self.root,
            self.start_monitoring,
            self.stop_monitoring,
            self.reset_all_risk_scores
        )

        # Summary label
        self.summary_label = tk.Label(
            self.root,
            text="Total High-Risk Users: 0     Incidents Logged: 0",
            font=FONTS['label'],
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_alert']
        )
        self.summary_label.pack(anchor="w", padx=22)

        # Control buttons
        self.pause_button = build_controls(
            self.root,
            self.toggle_simulation,
            self.export_activity_log,
            self.export_incidents
        )
        
        # Log tables
        self.activity_table, self.incident_table = build_logs(self.root)
        
        # User table
        self.user_table, self.progress_bars_frame, self.user_progress_bars = build_user_table(self.root)
        
        # Statistics
        self.stats_total_activities_label, self.stats_avg_risk_label, self.stats_max_risk_label = build_statistics(self.root)
        
        # Initial refresh
        self.refresh_users()
        
        # Schedule periodic database status updates
        self.update_db_status_periodic()

    def simulate_activity(self):
        """
        Simulate user activity - uses real events from database if available,
        otherwise falls back to random simulation.
        """
        if not self.monitoring_running or not self.simulation_active:
            return
        
        # Try to get real event from database first
        real_event = None
        if self.db_connected and self.use_real_events:
            real_event = self.db_manager.get_next_unprocessed_event()
        
        if real_event:
            # Process real event from database
            selected_user = real_event['user_id']
            selected_activity = real_event['activity']
            risk_increase = real_event.get('risk_increase', RISK_RULES.get(selected_activity, 0))
            
            # Mark event as processed
            self.db_manager.mark_event_processed(real_event['_id'])
            
            # Use enhanced details if available
            event_details = real_event.get('details', '')
        else:
            # Fall back to random simulation if no real events available
            selected_user = random.choice(list(USERS.keys()))
            selected_activity = random.choice(list(RISK_RULES.keys()))
            risk_increase = RISK_RULES[selected_activity]
            event_details = ''

        if self.user_status[selected_user] == USER_STATUS_ACTIVE:
            self.risk_scores[selected_user] = max(0, self.risk_scores[selected_user] + risk_increase)
            SecurityPointsManager.award_points(selected_user, risk_increase, self.risk_scores, self.security_points)
        else:
            risk_increase = 0

        # Use timestamp from real event if available, otherwise use current time
        if real_event and 'timestamp' in real_event:
            if isinstance(real_event['timestamp'], datetime):
                timestamp = real_event['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            else:
                timestamp = real_event['timestamp']
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        activity_description = self.get_activity_description(selected_activity)
        if event_details:
            activity_description += f" - {event_details}"
        
        self.total_activities += 1
        
        self.activity_table.insert("", 0, values=(timestamp, selected_user, activity_description, risk_increase))
        
        # Save event to database if not already there (for simulated events)
        if not real_event and self.db_connected:
            self.db_manager.save_event({
                'timestamp': timestamp,
                'user_id': selected_user,
                'activity': selected_activity,
                'risk_increase': risk_increase,
                'details': event_details,
                'source': 'simulation'
            })

        # AI Anomaly Detection
        if self.user_status[selected_user] == USER_STATUS_ACTIVE:
            if self.anomaly_detector.detect_anomaly(selected_user, self.risk_scores):
                self.risk_scores[selected_user] = max(0, self.risk_scores[selected_user] + AI_ANOMALY_RISK_PENALTY)
                self.raise_ai_alert(selected_user, AI_ANOMALY_RISK_PENALTY)
                if self.risk_scores[selected_user] >= RISK_THRESHOLD:
                    self.raise_incident(selected_user)

        # Sentiment Analysis
        if random.random() < SENTIMENT_ANALYSIS_PROBABILITY:
            risk_inc, self.total_activities = SentimentAnalyzer.analyze_sentiment(
                selected_user, self.user_status[selected_user],
                self.risk_scores, self.activity_table, self.total_activities
            )
            if self.risk_scores[selected_user] >= RISK_THRESHOLD:
                self.raise_incident(selected_user)

        # Check threshold
        if self.risk_scores[selected_user] >= RISK_THRESHOLD:
            self.raise_incident(selected_user)

        # Collect training data and retrain
        self.anomaly_detector.collect_training_data(self.risk_scores)
        if self.anomaly_detector.activities_since_training >= AI_RETRAIN_INTERVAL:
            self.anomaly_detector.train_model()
            self.anomaly_detector.activities_since_training = 0
        else:
            self.anomaly_detector.activities_since_training += 1

        # Refresh UI
        self.refresh_users()
        self.update_statistics()
        self.root.after(SIMULATION_INTERVAL, self.simulate_activity)
    
    def get_activity_description(self, activity_code):
        """Convert activity code to human-readable description."""
        descriptions = {
            "normal": "Normal Activity",
            "file_download": "File Download Detected",
            "login_from_unusual_ip": "Login from Unusual IP Address",
            "access_sensitive_folder": "Access to Sensitive Folder",
            "data_copy_to_usb": "Data Copy to USB Device"
        }
        return descriptions.get(activity_code, activity_code)
    
    def start_monitoring(self):
        """Start the monitoring system."""
        if not self.monitoring_running:
            self.monitoring_running = True
            self.simulation_active = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.pause_button.config(state="normal")
            self.simulate_activity()
    
    def stop_monitoring(self):
        """Stop the monitoring system."""
        if self.monitoring_running:
            self.monitoring_running = False
            self.simulation_active = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.pause_button.config(state="disabled")
    
    def toggle_simulation(self):
        """Toggle the simulation between paused and active states."""
        if not self.monitoring_running:
            return
        self.simulation_active = not self.simulation_active
        if self.simulation_active:
            self.pause_button.config(text="⏸ Pause")
            self.simulate_activity()
        else:
            self.pause_button.config(text="▶ Resume")
    
    def reset_all_risk_scores(self):
        """Reset all risk scores, clear logs, and unlock all users."""
        confirm = messagebox.askyesno(
            "Reset All Data",
            "Are you sure you want to reset all risk scores, clear logs, and unlock all users?\n\n"
            "This action cannot be undone.",
            icon="warning"
        )
        if not confirm:
            return
        
        for user_id in self.risk_scores:
            self.risk_scores[user_id] = 0
        for user_id in self.user_status:
            self.user_status[user_id] = USER_STATUS_ACTIVE
        for user_id in self.security_points:
            self.security_points[user_id] = 0.0
        
        for item_id in self.activity_table.get_children():
            self.activity_table.delete(item_id)
        for item_id in self.incident_table.get_children():
            self.incident_table.delete(item_id)
        
        self.total_activities = 0
        self.anomaly_detector = AnomalyDetector()
        
        # Clear database events if connected
        if self.db_connected:
            self.db_manager.clear_processed_events()
        
        self.refresh_users()
        self.update_statistics()
        messagebox.showinfo("Reset Complete", "All risk scores, logs, and incidents have been cleared.\nAll users have been unlocked.\nAI model has been reset.")
    
    def load_events_from_url(self, url: str):
        """
        Load events from a URL and save to database.
        
        Args:
            url: URL to fetch event data from
        """
        if not self.db_connected:
            messagebox.showerror("Error", "MongoDB is not connected. Please check your connection.")
            return
        
        try:
            # Show loading message
            loading_msg = messagebox.showinfo("Loading", "Fetching data from URL...\nPlease wait.")
            
            # Load events from URL
            events, error = DataLoader.load_from_url(url)
            
            if error:
                messagebox.showerror("Error", f"Failed to load data from URL:\n{error}")
                return
            
            if not events:
                messagebox.showwarning("Warning", "No valid events found in the URL data.")
                return
            
            # Save events to database
            saved_count = self.db_manager.save_events_batch(events)
            
            if saved_count > 0:
                self.use_real_events = True
                messagebox.showinfo(
                    "Success",
                    f"Successfully loaded {saved_count} events from URL!\n\n"
                    f"Events will be processed when you start monitoring."
                )
                self.update_db_status()
            else:
                messagebox.showerror("Error", "Failed to save events to database.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading from URL:\n{str(e)}")
    
    def load_events_from_file(self, file_path: str):
        """
        Load events from a local file and save to database.
        
        Args:
            file_path: Path to the event data file
        """
        if not self.db_connected:
            messagebox.showerror("Error", "MongoDB is not connected. Please check your connection.")
            return
        
        try:
            # Load events from file
            events, error = DataLoader.load_from_file(file_path)
            
            if error:
                messagebox.showerror("Error", f"Failed to load data from file:\n{error}")
                return
            
            if not events:
                messagebox.showwarning("Warning", "No valid events found in the file.")
                return
            
            # Save events to database
            saved_count = self.db_manager.save_events_batch(events)
            
            if saved_count > 0:
                self.use_real_events = True
                messagebox.showinfo(
                    "Success",
                    f"Successfully loaded {saved_count} events from file!\n\n"
                    f"File: {os.path.basename(file_path)}\n"
                    f"Events will be processed when you start monitoring."
                )
                self.update_db_status()
            else:
                messagebox.showerror("Error", "Failed to save events to database.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading from file:\n{str(e)}")
    
    def update_db_status(self):
        """Update the database status indicator in the UI."""
        if not hasattr(self, 'db_status_label'):
            return
        
        if self.db_connected:
            unprocessed = self.db_manager.get_unprocessed_event_count()
            total = self.db_manager.get_total_event_count()
            
            if total > 0:
                status_text = f"DB: ✓ Connected | Events: {unprocessed} unprocessed / {total} total"
                status_color = COLORS['fg_green']
            else:
                status_text = "DB: ✓ Connected | No events loaded"
                status_color = COLORS['fg_green']
        else:
            status_text = "DB: ✗ Not Connected"
            status_color = COLORS['fg_red']
        
        self.db_status_label.config(text=status_text, fg=status_color)
    
    def update_db_status_periodic(self):
        """Periodically update database status indicator."""
        self.update_db_status()
        # Update every 5 seconds
        self.root.after(5000, self.update_db_status_periodic)
    
    def start_risk_decay(self):
        """Start the risk decay timer."""
        for user_id in self.risk_scores:
            old_score = self.risk_scores[user_id]
            self.risk_scores[user_id] = max(0, old_score - RISK_DECAY_AMOUNT)
            
            SecurityPointsManager.award_decay_points(user_id, self.user_status[user_id], self.security_points)
            
            if (self.user_status[user_id] == USER_STATUS_LOCKED and 
                self.risk_scores[user_id] == 0 and old_score > 0):
                self.user_status[user_id] = USER_STATUS_ACTIVE
        
        self.refresh_users()
        self.update_statistics()
        self.root.after(RISK_DECAY_INTERVAL, self.start_risk_decay)

    def refresh_users(self):
        """Refresh the user risk scores table with current data."""
        for row_id in self.user_table.get_children():
            self.user_table.delete(row_id)

        high_risk_count = 0
        for user_id, user_info in USERS.items():
            current_risk_score = self.risk_scores[user_id]
            current_status = self.user_status[user_id]
            
            if current_risk_score >= RISK_THRESHOLD:
                high_risk_count += 1

            if current_status == USER_STATUS_LOCKED:
                risk_tag = "locked_user"
            elif current_risk_score <= RISK_LOW:
                risk_tag = "low_risk"
            elif current_risk_score <= RISK_MEDIUM:
                risk_tag = "medium_risk"
            else:
                risk_tag = "high_risk"

            security_score = self.security_points[user_id]
            self.user_table.insert("", "end",
                values=(user_id, user_info["role"], current_risk_score, current_status, f"{security_score:.1f}"),
                tags=(risk_tag,))
            
            self.update_user_progress_bar(user_id, current_risk_score, current_status)

        incident_count = len(self.incident_table.get_children())
        self.summary_label.config(
            text=f"Total High-Risk Users: {high_risk_count}     Incidents Logged: {incident_count}"
        )
    
    def update_user_progress_bar(self, user_id, risk_score, status):
        """Update the progress bar and visual indicators for a specific user."""
        if not hasattr(self, 'user_progress_bars') or user_id not in self.user_progress_bars:
            return
        
        try:
            progress_bar = self.user_progress_bars[user_id]['progress_bar']
            risk_label = self.user_progress_bars[user_id]['risk_label']
            status_indicator = self.user_progress_bars[user_id]['status_indicator']
        except (KeyError, TypeError):
            return
        
        progress_value = min(risk_score, RISK_THRESHOLD)
        progress_bar['value'] = progress_value
        
        try:
            if status == USER_STATUS_LOCKED:
                progress_bar['style'] = 'red.Horizontal.TProgressbar'
                status_indicator.config(text="🔒 LOCKED", fg=COLORS['fg_locked'])
            elif risk_score <= RISK_LOW:
                progress_bar['style'] = 'green.Horizontal.TProgressbar'
                status_indicator.config(text="", fg=COLORS['bg_panel'])
            elif risk_score <= RISK_MEDIUM:
                progress_bar['style'] = 'yellow.Horizontal.TProgressbar'
                status_indicator.config(text="", fg=COLORS['bg_panel'])
            else:
                progress_bar['style'] = 'red.Horizontal.TProgressbar'
                status_indicator.config(text="⚠ HIGH", fg=COLORS['fg_red'])
            
            if risk_score <= RISK_LOW:
                risk_label.config(text=str(risk_score), fg=COLORS['fg_green'])
            elif risk_score <= RISK_MEDIUM:
                risk_label.config(text=str(risk_score), fg=COLORS['fg_yellow'])
            else:
                risk_label.config(text=str(risk_score), fg=COLORS['fg_red'])
        except Exception:
            pass
    
    def update_statistics(self):
        """Update the statistics panel with current calculated metrics."""
        if len(self.risk_scores) > 0:
            average_risk = sum(self.risk_scores.values()) / len(self.risk_scores)
        else:
            average_risk = 0
        
        max_risk_score = max(self.risk_scores.values()) if self.risk_scores else 0
        
        self.stats_total_activities_label.config(text=f"Total Activities: {self.total_activities}")
        self.stats_avg_risk_label.config(text=f"Average Risk Score: {average_risk:.1f}")
        self.stats_max_risk_label.config(text=f"Highest Risk Score: {max_risk_score}")

    def raise_incident(self, user_id):
        """Raise an incident alert when a user's risk score exceeds the threshold."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_role = USERS[user_id]["role"]
        incident_message = f"HIGH-RISK ALERT: {user_id} ({user_role}) triggered security incident - Account LOCKED"

        self.incident_table.insert("", 0, values=(timestamp, user_id, self.risk_scores[user_id], incident_message))
        self.user_status[user_id] = USER_STATUS_LOCKED
        self.risk_scores[user_id] = 0
    
    def raise_ai_alert(self, user_id, risk_penalty):
        """Log an AI-detected anomaly alert."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_role = USERS[user_id]["role"]
        ai_alert_message = f"AI ALERT: {user_id} ({user_role}) - Anomalous behavior detected by Isolation Forest (+{risk_penalty} risk)"
        self.incident_table.insert("", 0, values=(timestamp, user_id, self.risk_scores[user_id], ai_alert_message))
        
        # Save AI alert to database
        if self.db_connected:
            self.db_manager.save_incident({
                'timestamp': timestamp,
                'user_id': user_id,
                'risk_score': self.risk_scores[user_id],
                'message': ai_alert_message,
                'user_role': user_role,
                'alert_type': 'AI_ANOMALY'
            })

    def export_activity_log(self):
        """Export the activity log to a CSV file."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Activity Log"
            )
            if not filename:
                return
            
            with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Time", "User", "Activity", "Risk Increase"])
                for item_id in self.activity_table.get_children():
                    row_values = self.activity_table.item(item_id, 'values')
                    csv_writer.writerow(row_values)
            
            messagebox.showinfo("Success", f"Activity log exported to {os.path.basename(filename)}")
        except Exception as error:
            messagebox.showerror("Error", f"Failed to export activity log: {str(error)}")
    
    def export_incidents(self):
        """Export incident alerts to a CSV file."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Incidents"
            )
            if not filename:
                return
            
            with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Time", "User", "Risk Score", "Message"])
                for item_id in self.incident_table.get_children():
                    row_values = self.incident_table.item(item_id, 'values')
                    csv_writer.writerow(row_values)
            
            messagebox.showinfo("Success", f"Incidents exported to {os.path.basename(filename)}")
        except Exception as error:
            messagebox.showerror("Error", f"Failed to export incidents: {str(error)}")


if __name__ == "__main__":
    import sys
    
    # Check for MongoDB URI as command line argument
    mongodb_uri = None
    if len(sys.argv) > 1:
        mongodb_uri = sys.argv[1]
        print(f"Using MongoDB URI: {mongodb_uri}")
    else:
        print("Using default MongoDB URI: mongodb://localhost:27017/")
        print("To specify custom URI: python main.py <mongodb_uri>")
    
    root_window = tk.Tk()
    application = InsiderThreatApp(root_window, mongodb_uri=mongodb_uri)
    root_window.mainloop()

