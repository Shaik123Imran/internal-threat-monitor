"""
GUI Components Module
=====================
This module contains functions for building GUI components including:
- Tables (user risk scores, activity log, incident alerts)
- Buttons and controls
- Progress bars
- Statistics panels
"""

import tkinter as tk
from tkinter import ttk
from config import USERS, RISK_THRESHOLD
from gui_styles import configure_progress_bar_styles, configure_table_tags, COLORS, FONTS


def build_user_table(parent):
    """
    Build the user risk scores table with color coding and progress bars.
    
    Args:
        parent: Parent widget (root window)
        
    Returns:
        Tuple of (user_table, progress_bars_frame, user_progress_bars_dict)
    """
    table_frame = tk.Frame(parent, bg=COLORS['bg_panel'])
    table_frame.pack(fill="x", padx=20, pady=15)

    tk.Label(
        table_frame,
        text="User Risk Scores",
        bg=COLORS['bg_panel'],
        fg=COLORS['fg_white'],
        font=FONTS['heading']
    ).pack(anchor="w", padx=10, pady=5)

    table_columns = ("User ID", "Role", "Risk Score", "Status", "Security Score")
    user_table = ttk.Treeview(table_frame, columns=table_columns, show="headings", height=5)

    for column in table_columns:
        user_table.heading(column, text=column)
        user_table.column(column, anchor="center")
    
    configure_progress_bar_styles()
    user_table.pack(fill="x", padx=10, pady=5)
    configure_table_tags(user_table)
    
    progress_bars_frame = tk.Frame(table_frame, bg=COLORS['bg_panel'])
    progress_bars_frame.pack(fill="x", padx=10, pady=5)
    
    user_progress_bars = {}
    
    for user_id in USERS.keys():
        user_progress_frame = tk.Frame(progress_bars_frame, bg=COLORS['bg_panel'])
        user_progress_frame.pack(fill="x", pady=2)
        
        user_label = tk.Label(
            user_progress_frame,
            text=f"{user_id}:",
            bg=COLORS['bg_panel'],
            fg=COLORS['fg_white'],
            font=FONTS['tiny'],
            width=12,
            anchor="w"
        )
        user_label.pack(side="left", padx=5)
        
        progress_bar = ttk.Progressbar(
            user_progress_frame,
            length=200,
            mode='determinate',
            maximum=RISK_THRESHOLD
        )
        progress_bar.pack(side="left", padx=5, fill="x", expand=True)
        
        risk_label = tk.Label(
            user_progress_frame,
            text="0",
            bg=COLORS['bg_panel'],
            fg=COLORS['fg_white'],
            font=FONTS['small_bold'],
            width=5,
            anchor="e"
        )
        risk_label.pack(side="left", padx=5)
        
        status_indicator = tk.Label(
            user_progress_frame,
            text="",
            bg=COLORS['bg_panel'],
            fg=COLORS['fg_locked'],
            font=FONTS['small_bold'],
            width=8
        )
        status_indicator.pack(side="left", padx=5)
        
        user_progress_bars[user_id] = {
            'progress_bar': progress_bar,
            'risk_label': risk_label,
            'status_indicator': status_indicator
        }
    
    return user_table, progress_bars_frame, user_progress_bars


def build_logs(parent):
    """
    Build the log tables in a tabbed notebook.
    
    Args:
        parent: Parent widget (root window)
        
    Returns:
        Tuple of (activity_table, incident_table)
    """
    log_frame = tk.Frame(parent, bg=COLORS['bg_panel'])
    log_frame.pack(fill="both", expand=True, padx=20, pady=10)

    notebook = ttk.Notebook(log_frame)
    notebook.pack(fill="both", expand=True)

    activity_tab = ttk.Frame(notebook)
    notebook.add(activity_tab, text="Activity Log")

    activity_columns = ("Time", "User", "Activity", "Risk Increase")
    activity_table = ttk.Treeview(activity_tab, columns=activity_columns, show="headings")

    for column in activity_columns:
        activity_table.heading(column, text=column)
        activity_table.column(column, anchor="center")

    activity_table.pack(fill="both", expand=True)

    incident_tab = ttk.Frame(notebook)
    notebook.add(incident_tab, text="Incident Alerts")

    incident_columns = ("Time", "User", "Risk Score", "Message")
    incident_table = ttk.Treeview(incident_tab, columns=incident_columns, show="headings")

    for column in incident_columns:
        incident_table.heading(column, text=column)
        incident_table.column(column, anchor="center")

    incident_table.pack(fill="both", expand=True)
    
    return activity_table, incident_table


def build_statistics(parent):
    """
    Build the statistics panel showing key metrics.
    
    Args:
        parent: Parent widget (root window)
        
    Returns:
        Tuple of (total_activities_label, avg_risk_label, max_risk_label)
    """
    stats_frame = tk.Frame(parent, bg=COLORS['bg_panel'])
    stats_frame.pack(fill="x", padx=20, pady=10)
    
    tk.Label(
        stats_frame,
        text="Statistics",
        bg=COLORS['bg_panel'],
        fg=COLORS['fg_white'],
        font=FONTS['heading']
    ).pack(anchor="w", padx=10, pady=5)
    
    stats_content_frame = tk.Frame(stats_frame, bg=COLORS['bg_panel'])
    stats_content_frame.pack(fill="x", padx=10, pady=5)
    
    total_activities_label = tk.Label(
        stats_content_frame,
        text="Total Activities: 0",
        bg=COLORS['bg_panel'],
        fg=COLORS['fg_stats'],
        font=FONTS['small']
    )
    total_activities_label.pack(side="left", padx=20)
    
    avg_risk_label = tk.Label(
        stats_content_frame,
        text="Average Risk Score: 0.0",
        bg=COLORS['bg_panel'],
        fg=COLORS['fg_stats'],
        font=FONTS['small']
    )
    avg_risk_label.pack(side="left", padx=20)
    
    max_risk_label = tk.Label(
        stats_content_frame,
        text="Highest Risk Score: 0",
        bg=COLORS['bg_panel'],
        fg=COLORS['fg_stats'],
        font=FONTS['small']
    )
    max_risk_label.pack(side="left", padx=20)
    
    return total_activities_label, avg_risk_label, max_risk_label


def build_monitoring_controls(parent, start_callback, stop_callback, reset_callback):
    """
    Build monitoring control buttons (Start/Stop/Reset).
    
    Args:
        parent: Parent widget
        start_callback: Function to call when Start is clicked
        stop_callback: Function to call when Stop is clicked
        reset_callback: Function to call when Reset is clicked
        
    Returns:
        Tuple of (start_button, stop_button)
    """
    monitoring_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
    monitoring_frame.pack(fill="x", padx=20, pady=10)
    
    start_button = tk.Button(
        monitoring_frame,
        text="▶ Start Monitoring",
        command=start_callback,
        bg="#4a8a4a",
        fg=COLORS['fg_white'],
        font=FONTS['button'],
        padx=20,
        pady=8,
        relief="flat",
        cursor="hand2"
    )
    start_button.pack(side="left", padx=5)
    
    stop_button = tk.Button(
        monitoring_frame,
        text="⏹ Stop Monitoring",
        command=stop_callback,
        bg="#8a4a4a",
        fg=COLORS['fg_white'],
        font=FONTS['button'],
        padx=20,
        pady=8,
        relief="flat",
        cursor="hand2",
        state="disabled"
    )
    stop_button.pack(side="left", padx=5)
    
    reset_button = tk.Button(
        monitoring_frame,
        text="🔄 Reset All Risk Scores",
        command=reset_callback,
        bg="#4a4a8a",
        fg=COLORS['fg_white'],
        font=FONTS['button'],
        padx=20,
        pady=8,
        relief="flat",
        cursor="hand2"
    )
    reset_button.pack(side="left", padx=5)
    
    return start_button, stop_button


def build_controls(parent, pause_callback, export_activity_callback, export_incident_callback):
    """
    Build control buttons for pause/resume and export functionality.
    
    Args:
        parent: Parent widget
        pause_callback: Function to call when Pause is clicked
        export_activity_callback: Function to call when Export Activity is clicked
        export_incident_callback: Function to call when Export Incident is clicked
        
    Returns:
        Pause button widget
    """
    control_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
    control_frame.pack(fill="x", padx=20, pady=5)
    
    pause_button = tk.Button(
        control_frame,
        text="⏸ Pause",
        command=pause_callback,
        bg="#4a4a4a",
        fg=COLORS['fg_white'],
        font=FONTS['label'],
        padx=15,
        pady=5,
        relief="flat",
        cursor="hand2",
        state="disabled"
    )
    pause_button.pack(side="left", padx=5)
    
    export_activity_button = tk.Button(
        control_frame,
        text="📥 Export Activity Log",
        command=export_activity_callback,
        bg="#4a4a4a",
        fg=COLORS['fg_white'],
        font=FONTS['label'],
        padx=15,
        pady=5,
        relief="flat",
        cursor="hand2"
    )
    export_activity_button.pack(side="left", padx=5)
    
    export_incident_button = tk.Button(
        control_frame,
        text="📥 Export Incidents",
        command=export_incident_callback,
        bg="#4a4a4a",
        fg=COLORS['fg_white'],
        font=FONTS['label'],
        padx=15,
        pady=5,
        relief="flat",
        cursor="hand2"
    )
    export_incident_button.pack(side="left", padx=5)
    
    return pause_button

