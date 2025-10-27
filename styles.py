# styles.py
import tkinter as tk

class Styles:
    # Bootstrap-like color scheme
    PRIMARY = "#007bff"
    SECONDARY = "#6c757d"
    SUCCESS = "#28a745"
    DANGER = "#dc3545"
    WARNING = "#ffc107"
    INFO = "#17a2b8"
    LIGHT = "#f8f9fa"
    DARK = "#343a40"
    WHITE = "#ffffff"
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    HEADING_FONT = (FONT_FAMILY, 18, "bold")
    SUBHEADING_FONT = (FONT_FAMILY, 14, "bold")
    NORMAL_FONT = (FONT_FAMILY, 10)
    SMALL_FONT = (FONT_FAMILY, 9)
    
    @staticmethod
    def create_button(parent, text, command, bg_color=PRIMARY, fg_color="white"):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=Styles.NORMAL_FONT,
            padx=15,
            pady=5,
            relief="flat",
            bd=0
        )
    
    @staticmethod
    def create_card(parent, bg_color=WHITE):
        card = tk.Frame(parent, bg=bg_color, relief="raised", bd=1)
        return card