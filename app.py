!pip install folium
!pip install tkinter
!pip install tkintermapview

import folium
import webbrowser
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import json
from tkintermapview import TkinterMapView
import tempfile
from PIL import Image, ImageTk
import io
import base64

class DataManager:
    """Class to handle all data persistence"""
    
    def __init__(self):
        self.data_file = "mineral_app_data.json"
        self.load_data()
    
    def load_data(self):
        """Load data from file or create default data"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.MineralData = data.get('MineralData', self.get_default_minerals())
                self.CountryProfiles = data.get('CountryProfiles', self.get_default_countries())
                self.Users = data.get('Users', self.get_default_users())
        except FileNotFoundError:
            # Create default data if file doesn't exist
            self.MineralData = self.get_default_minerals()
            self.CountryProfiles = self.get_default_countries()
            self.Users = self.get_default_users()
            self.save_data()
    
    def save_data(self):
        """Save all data to file"""
        data = {
            'MineralData': self.MineralData,
            'CountryProfiles': self.CountryProfiles,
            'Users': self.Users
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_default_minerals(self):
        return {
            "Cobalt": {"Location": "Africa, DRC", "Production": 1200, "Color": "#1f77b4"},
            "Lithium": {"Location": "Africa, Zimbabwe", "Production": 950, "Color": "#ff7f0e"},
            "Gold": {"Location": "Africa, S.A", "Production": 2500, "Color": "#d4af37"}
        }
    
    def get_default_countries(self):
        return {
            "South Africa": {"Production": 1000, "GDP": 35000, "Projects": 5, "Color": "#2ca02c"},
            "Lesotho": {"Production": 600, "GDP": 18000, "Projects": 3, "Color": "#9467bd"},
            "Swaziland": {"Production": 1200, "GDP": 41000, "Projects": 4, "Color": "#8c564b"}
        }
    
    def get_default_users(self):
        return {
            "admin": {"password": "adminpass", "role": "Administrator"},
            "ngqwele": {"password": "ngodlii", "role": "Administrator"},
            "investor": {"password": "investorpass", "role": "Investor"},
            "researcher": {"password": "researcherpass", "role": "Researcher"},
            "Lungelo": {"password": "Gcwabaza", "role": "Administrator"},
            "thuthuzela": {"password": "fazzie", "role": "Administrator"},
            "thuthuzela": {"password": "fazzie", "role": "Administrator"},
            "lesedi": {"password": "molomo", "role": "Administrator"},
            "abigail": {"password": "sekwati", "role": "Administrator"}
        }
    
    def add_mineral(self, name, location, production, color):
        self.MineralData[name] = {
            "Location": location,
            "Production": production,
            "Color": color
        }
        self.save_data()
    
    def update_mineral(self, old_name, new_name, location, production, color):
        if old_name != new_name and old_name in self.MineralData:
            del self.MineralData[old_name]
        self.MineralData[new_name] = {
            "Location": location,
            "Production": production,
            "Color": color
        }
        self.save_data()
    
    def delete_mineral(self, name):
        if name in self.MineralData:
            del self.MineralData[name]
            self.save_data()
            return True
        return False
    
    def add_country(self, name, production, gdp, projects, color):
        self.CountryProfiles[name] = {
            "Production": production,
            "GDP": gdp,
            "Projects": projects,
            "Color": color
        }
        self.save_data()
    
    def update_country(self, old_name, new_name, production, gdp, projects, color):
        if old_name != new_name and old_name in self.CountryProfiles:
            del self.CountryProfiles[old_name]
        self.CountryProfiles[new_name] = {
            "Production": production,
            "GDP": gdp,
            "Projects": projects,
            "Color": color
        }
        self.save_data()
    
    def delete_country(self, name):
        if name in self.CountryProfiles:
            del self.CountryProfiles[name]
            self.save_data()
            return True
        return False
    
    def add_user(self, username, password, role):
        self.Users[username] = {"password": password, "role": role}
        self.save_data()
    
    def delete_user(self, username):
        if username in self.Users:
            del self.Users[username]
            self.save_data()
            return True
        return False

class ModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoMineral Hub - Mineral Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8f9fa')
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Modern color scheme
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'background': '#f8f9fa'
        }
        
        self.current_user_role = None
        self.current_user = None
        self.setup_styles()
        self.build_login()

    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Primary.TButton', 
                       background=self.colors['secondary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Secondary.TButton',
                       background=self.colors['light'],
                       foreground=self.colors['dark'],
                       borderwidth=1,
                       padding=(15, 8),
                       font=('Segoe UI', 9))
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 20, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['background'])
        
        style.configure('Card.TFrame',
                       background='white',
                       relief='raised',
                       borderwidth=1)

    def clear_frame(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_scrollable_frame(self, parent):
        """Create a scrollable frame and return the scrollable content frame"""
        # Create main container
        container = tk.Frame(parent, bg=self.colors['background'])
        container.pack(fill='both', expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(container, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)
        
        # Bind mousewheel to canvas
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        return scrollable_frame, canvas

    def build_login(self):
        self.clear_frame()
        
        # Main container with gradient background
        main_frame = tk.Frame(self.root, bg=self.colors['primary'])
        main_frame.pack(fill='both', expand=True)
        
        # Login card
        login_card = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        login_card.place(relx=0.5, rely=0.5, anchor='center', width=400, height=450)
        
        # Company logo/header
        header_frame = tk.Frame(login_card, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', padx=2, pady=2)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="GeoMineral Hub", 
                font=('Segoe UI', 18, 'bold'), bg=self.colors['primary'], 
                fg='white').pack(expand=True)
        
        tk.Label(header_frame, text="Mineral Management System", 
                font=('Segoe UI', 10), bg=self.colors['primary'], 
                fg=self.colors['light']).pack(expand=True)
        
        # Form container
        form_frame = tk.Frame(login_card, bg='white', padx=30, pady=30)
        form_frame.pack(fill='both', expand=True)
        
        tk.Label(form_frame, text="Welcome Back", font=('Segoe UI', 16, 'bold'),
                bg='white', fg=self.colors['dark']).pack(pady=(0, 20))
        
        # Username field
        tk.Label(form_frame, text="Username", font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.colors['dark'], anchor='w').pack(fill='x', pady=(5, 0))
        self.username_entry = ttk.Entry(form_frame, font=('Segoe UI', 11))
        self.username_entry.pack(fill='x', pady=(5, 15), ipady=8)
        
        # Password field
        tk.Label(form_frame, text="Password", font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.colors['dark'], anchor='w').pack(fill='x', pady=(5, 0))
        self.password_entry = ttk.Entry(form_frame, show="•", font=('Segoe UI', 11))
        self.password_entry.pack(fill='x', pady=(5, 20), ipady=8)
        
        # Login button
        login_btn = ttk.Button(form_frame, text="Sign In", style='Primary.TButton',
                              command=self.login)
        login_btn.pack(fill='x', ipady=10, pady=(0, 15))
        
        # Sign up button for researchers
        signup_btn = ttk.Button(form_frame, text="Sign Up as Researcher", 
                               style='Secondary.TButton',
                               command=self.show_researcher_signup)
        signup_btn.pack(fill='x', ipady=8)
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Footer
        footer_frame = tk.Frame(login_card, bg=self.colors['light'], height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame, text="© 2025 GeoMineral Hub. All rights reserved.",
                font=('Segoe UI', 8), bg=self.colors['light'], 
                fg=self.colors['dark']).pack(expand=True)

