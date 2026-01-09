"""
GUI Styles Module
=================
This module contains all styling configurations for the GUI components.
It includes color schemes, progress bar styles, and theme settings.
"""

import tkinter.ttk as ttk


def configure_progress_bar_styles():
    """
    Configure progress bar styles for different risk levels.
    Creates custom styles for green (low risk), yellow (medium risk),
    and red (high risk) progress bars.
    """
    style = ttk.Style()
    style.theme_use('clam')
    
    # Green progress bar for low risk
    style.configure('green.Horizontal.TProgressbar',
                   background='#4a8a4a',
                   troughcolor='#1a1a1a',
                   borderwidth=0,
                   lightcolor='#6aaa6a',
                   darkcolor='#4a8a4a')
    
    # Yellow/Orange progress bar for medium risk
    style.configure('yellow.Horizontal.TProgressbar',
                   background='#8a8a4a',
                   troughcolor='#1a1a1a',
                   borderwidth=0,
                   lightcolor='#aaaa6a',
                   darkcolor='#8a8a4a')
    
    # Red progress bar for high risk and locked users
    style.configure('red.Horizontal.TProgressbar',
                   background='#8a4a4a',
                   troughcolor='#1a1a1a',
                   borderwidth=0,
                   lightcolor='#aa6a6a',
                   darkcolor='#8a4a4a')


def configure_table_tags(user_table):
    """
    Configure color tags for the user risk scores table.
    Tags are applied to rows based on risk score ranges.
    
    Args:
        user_table: The ttk.Treeview table to configure
    """
    # Configure color tags for risk level visualization
    # Enhanced with foreground colors and locked user highlighting
    user_table.tag_configure("low_risk", background="#2d4a2d", foreground="#88ff88")    # Green for low risk
    user_table.tag_configure("medium_risk", background="#4a4a2d", foreground="#ffff88")  # Yellow for medium risk
    user_table.tag_configure("high_risk", background="#4a2d2d", foreground="#ff8888")    # Red for high risk
    user_table.tag_configure("locked_user", background="#3a1a1a", foreground="#ff6666")  # Special styling for locked users


# Color constants for consistent styling
COLORS = {
    'bg_dark': '#1e1e1e',      # Main background
    'bg_panel': '#2a2a2a',     # Panel background
    'fg_white': 'white',        # White text
    'fg_green': '#88ff88',      # Green text (low risk)
    'fg_yellow': '#ffff88',     # Yellow text (medium risk)
    'fg_red': '#ff8888',        # Red text (high risk)
    'fg_alert': '#ff5555',      # Alert red
    'fg_stats': '#88cc88',      # Statistics green
    'fg_locked': '#ff6666',     # Locked user red
}

# Font configurations
FONTS = {
    'title': ('Segoe UI', 22, 'bold'),
    'heading': ('Segoe UI', 14, 'bold'),
    'button': ('Segoe UI', 11, 'bold'),
    'label': ('Segoe UI', 11),
    'small': ('Segoe UI', 10),
    'small_bold': ('Segoe UI', 9, 'bold'),
    'tiny': ('Segoe UI', 9),
}

