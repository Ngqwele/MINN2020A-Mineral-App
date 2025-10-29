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

    def show_researcher_signup(self):
        """Show researcher signup form"""
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Researcher Sign Up")
        signup_window.geometry("400x350")
        signup_window.configure(bg='white')
        signup_window.resizable(False, False)
        
        # Center the window
        signup_window.transient(self.root)
        signup_window.grab_set()
        
        # Header
        header_frame = tk.Frame(signup_window, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', padx=2, pady=2)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Researcher Sign Up", 
                font=('Segoe UI', 16, 'bold'), bg=self.colors['primary'], 
                fg='white').pack(expand=True)
        
        # Form container
        form_frame = tk.Frame(signup_window, bg='white', padx=30, pady=30)
        form_frame.pack(fill='both', expand=True)
        
        # Username
        tk.Label(form_frame, text="Username", font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.colors['dark'], anchor='w').pack(fill='x', pady=(5, 0))
        username_entry = ttk.Entry(form_frame, font=('Segoe UI', 11))
        username_entry.pack(fill='x', pady=(5, 15), ipady=8)
        
        # Password
        tk.Label(form_frame, text="Password", font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.colors['dark'], anchor='w').pack(fill='x', pady=(5, 0))
        password_entry = ttk.Entry(form_frame, show="•", font=('Segoe UI', 11))
        password_entry.pack(fill='x', pady=(5, 20), ipady=8)
        
        def submit_signup():
            username = username_entry.get()
            password = password_entry.get()
            
            if not all([username, password]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            if username in self.data_manager.Users:
                messagebox.showerror("Error", "Username already exists")
                return
                
            # Add researcher to users using data manager
            self.data_manager.add_user(username, password, "Researcher")
            
            messagebox.showinfo("Success", 
                              "Researcher account created successfully!\n\n"
                              f"Welcome {username}!\n"
                              "You can now login with your credentials.")
            signup_window.destroy()
        
        # Submit button
        ttk.Button(form_frame, text="Create Researcher Account", 
                  style='Primary.TButton', command=submit_signup).pack(fill='x', ipady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.data_manager.Users.get(username)
        
        if user and password == user['password']:
            self.current_user_role = user['role']
            self.current_user = username
            self.build_dashboard()
        else:
            messagebox.showerror("Login Failed", 
                               "Invalid username or password. Please try again.")

    def build_dashboard(self):
        self.clear_frame()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True)
        
        # Header
        header = tk.Frame(main_container, bg=self.colors['primary'], height=80)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Company info
        title_frame = tk.Frame(header, bg=self.colors['primary'])
        title_frame.pack(side='left', padx=30, pady=20)
        
        tk.Label(title_frame, text="GeoMineral Hub", font=('Segoe UI', 20, 'bold'),
                bg=self.colors['primary'], fg='white').pack(anchor='w')
        tk.Label(title_frame, text="Mineral Management Dashboard", 
                font=('Segoe UI', 11), bg=self.colors['primary'], 
                fg=self.colors['light']).pack(anchor='w')
        
        # User info
        user_frame = tk.Frame(header, bg=self.colors['primary'])
        user_frame.pack(side='right', padx=30, pady=20)
        
        tk.Label(user_frame, text=f"Welcome, {self.current_user}", 
                font=('Segoe UI', 11, 'bold'), bg=self.colors['primary'], 
                fg='white').pack(anchor='e')
        tk.Label(user_frame, text=f"Role: {self.current_user_role}", 
                font=('Segoe UI', 10), bg=self.colors['primary'], 
                fg=self.colors['light']).pack(anchor='e')
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome card
        welcome_card = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        welcome_card.pack(fill='x', pady=(0, 20))
        
        welcome_text = f"""Welcome to GeoMineral Hub Management System
        As {self.current_user_role}."""
        
        tk.Label(welcome_card, text=welcome_text, font=('Segoe UI', 11),
                bg='white', fg=self.colors['dark'], justify='left',
                padx=20, pady=20).pack(fill='x')
        
        # Dashboard cards
        cards_frame = tk.Frame(content_frame, bg=self.colors['background'])
        cards_frame.pack(fill='both', expand=True)
        
        # Role-based options
        options = {
            "Administrator": [
                {"name": "📊 Minerals Data", "command": self.show_minerals, "color": self.colors['secondary']},
                {"name": "🗺️ Interactive Map", "command": self.show_map, "color": self.colors['success']},
                {"name": "🏛️ Country Profiles", "command": self.show_country_profiles, "color": self.colors['warning']},
                {"name": "📈 Analytics & Charts", "command": self.show_charts, "color": self.colors['danger']},
                {"name": "👥 User Management", "command": self.manage_users, "color": self.colors['primary']}
            ],
            "Investor": [
                {"name": "🗺️ Interactive Map", "command": self.show_map, "color": self.colors['success']},
                {"name": "🏛️ Country Profiles", "command": self.show_country_profiles, "color": self.colors['warning']},
                {"name": "📈 Analytics & Charts", "command": self.show_charts, "color": self.colors['danger']}
            ],
            "Researcher": [
                {"name": "📊 Minerals Data", "command": self.show_minerals, "color": self.colors['secondary']},
                {"name": "📈 Analytics & Charts", "command": self.show_charts, "color": self.colors['danger']}
            ]
        }
        
        # Create option buttons
        row, col = 0, 0
        for option in options.get(self.current_user_role, []):
            btn_frame = tk.Frame(cards_frame, bg=self.colors['background'])
            btn_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            btn = tk.Button(btn_frame, text=option['name'], 
                          font=('Segoe UI', 11, 'bold'),
                          bg=option['color'], fg='white',
                          relief='raised', bd=2,
                          width=20, height=4,
                          command=option['command'])
            btn.pack(fill='both', expand=True)
            
            # Hover effects
            def on_enter(e, btn=btn, color=option['color']):
                btn.config(bg=self.adjust_color(color, 20))
            
            def on_leave(e, btn=btn, color=option['color']):
                btn.config(bg=color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(3):
            cards_frame.columnconfigure(i, weight=1)
        for i in range(row + 1):
            cards_frame.rowconfigure(i, weight=1)
        
        # Logout button
        logout_frame = tk.Frame(content_frame, bg=self.colors['background'])
        logout_frame.pack(fill='x', pady=20)
        
        ttk.Button(logout_frame, text="🚪 Logout", style='Secondary.TButton',
                  command=self.build_login).pack(side='right')


    def adjust_color(self, color, amount):
        """Lighten or darken a color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = [min(255, max(0, c + amount)) for c in rgb]
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"

    def show_minerals(self):
        self.clear_frame()
        self.create_navigation("Minerals Data")
        
        # Create scrollable content
        scrollable_frame, _ = self.create_scrollable_frame(self.root)
        
        # Header with management buttons for admins
        header_frame = tk.Frame(scrollable_frame, bg='white', relief='raised', bd=1)
        header_frame.pack(fill='x', pady=(0, 20))
        
        total_minerals = len(self.data_manager.MineralData)
        total_production = sum(data['Production'] for data in self.data_manager.MineralData.values())
        
        stats_text = f"📈 Mineral Overview: {total_minerals} Minerals | Total Production: {total_production:,} tonnes/day"
        tk.Label(header_frame, text=stats_text, font=('Segoe UI', 12, 'bold'),
                bg='white', fg=self.colors['primary'], pady=15).pack()
        
        # Management buttons for administrators
        if self.current_user_role == "Administrator":
            manage_frame = tk.Frame(header_frame, bg='white')
            manage_frame.pack(pady=(0, 10))
            
            ttk.Button(manage_frame, text="➕ Add Mineral", 
                      style='Primary.TButton',
                      command=self.show_add_mineral_form).pack(side='left', padx=5)
        
        # Minerals cards
        self.minerals_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        self.minerals_frame.pack(fill='both', expand=True)
        
        self.refresh_minerals_display()

    def show_add_mineral_form(self):
        """Show the add mineral form inline"""
        # Remove existing form if any
        if hasattr(self, 'add_mineral_frame'):
            self.add_mineral_frame.pack_forget()
        
        self.add_mineral_frame = tk.Frame(self.minerals_frame, bg='white', relief='raised', bd=1)
        self.add_mineral_frame.pack(fill='x', padx=20, pady=10, ipadx=10, ipady=10)
        
        tk.Label(self.add_mineral_frame, text="➕ Add New Mineral", 
                font=('Segoe UI', 12, 'bold'), bg='white', 
                fg=self.colors['primary']).pack(anchor='w', pady=(0, 10))
        
        # Form fields
        form_fields = tk.Frame(self.add_mineral_frame, bg='white')
        form_fields.pack(fill='x')
        
        # Mineral Name
        tk.Label(form_fields, text="Mineral Name:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=(0, 10))
        self.mineral_name_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        self.mineral_name_entry.grid(row=0, column=1, sticky='w', pady=5, padx=(0, 20))
        
        # Location
        tk.Label(form_fields, text="Location:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=(0, 10))
        self.mineral_location_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        self.mineral_location_entry.grid(row=0, column=3, sticky='w', pady=5, padx=(0, 20))
        
        # Production
        tk.Label(form_fields, text="Production:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=(0, 10))
        self.mineral_production_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        self.mineral_production_entry.grid(row=1, column=1, sticky='w', pady=5, padx=(0, 20))
        
        # Color
        tk.Label(form_fields, text="Color:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=1, column=2, sticky='w', pady=5, padx=(0, 10))
        self.mineral_color_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        self.mineral_color_entry.insert(0, "#1f77b4")
        self.mineral_color_entry.grid(row=1, column=3, sticky='w', pady=5, padx=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(self.add_mineral_frame, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="💾 Save Mineral", style='Primary.TButton',
                  command=self.save_mineral).pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="❌ Cancel", style='Secondary.TButton',
                  command=self.cancel_add_mineral).pack(side='left')

    def save_mineral(self):
        """Save new mineral from inline form"""
        name = self.mineral_name_entry.get().strip()
        location = self.mineral_location_entry.get().strip()
        production = self.mineral_production_entry.get().strip()
        color = self.mineral_color_entry.get().strip()
        
        if not all([name, location, production]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        try:
            production_val = int(production)
        except ValueError:
            messagebox.showerror("Error", "Production must be a number")
            return
            
        if name in self.data_manager.MineralData:
            messagebox.showerror("Error", "Mineral already exists")
            return
            
        # Use data manager to save mineral
        self.data_manager.add_mineral(name, location, production_val, color)
        
        messagebox.showinfo("Success", f"Mineral '{name}' added successfully!")
        
        # Clear form and refresh display
        self.cancel_add_mineral()
        self.refresh_minerals_display()

    def cancel_add_mineral(self):
        """Cancel adding mineral and hide form"""
        if hasattr(self, 'add_mineral_frame'):
            self.add_mineral_frame.pack_forget()

    def refresh_minerals_display(self):
        """Refresh the minerals display"""
        # Clear existing minerals display
        for widget in self.minerals_frame.winfo_children():
            widget.pack_forget()
        
        # Show minerals
        for mineral, data in self.data_manager.MineralData.items():
            card = tk.Frame(self.minerals_frame, bg='white', relief='raised', bd=1)
            card.pack(fill='x', padx=20, pady=10, ipadx=10, ipady=10)
            
            # Header with mineral name and actions
            header = tk.Frame(card, bg='white')
            header.pack(fill='x', pady=(0, 10))
            
            tk.Label(header, text=f"🔨 {mineral}", font=('Segoe UI', 12, 'bold'),
                    bg='white', fg=data['Color']).pack(side='left')
            
            # Action buttons for admins
            if self.current_user_role == "Administrator":
                action_frame = tk.Frame(header, bg='white')
                action_frame.pack(side='right')
                
                ttk.Button(action_frame, text="✏️ Edit", 
                          command=lambda m=mineral: self.edit_mineral(m),
                          style='Secondary.TButton').pack(side='left', padx=2)
                
                ttk.Button(action_frame, text="🗑️ Remove", 
                          command=lambda m=mineral: self.remove_mineral(m),
                          style='Secondary.TButton').pack(side='left', padx=2)
            
            # Mineral info
            info = f"""📍 Location: {data['Location']}
⚡ Production: {data['Production']:,} tonnes per day
💎 Status: Active mining operations"""
            
            tk.Label(card, text=info, font=('Segoe UI', 10),
                   bg='white', fg=self.colors['dark'], justify='left').pack(anchor='w')

    def edit_mineral(self, mineral_name):
        """Edit mineral inline"""
        mineral_data = self.data_manager.MineralData[mineral_name]
        
        # Create edit form
        edit_frame = tk.Frame(self.minerals_frame, bg='white', relief='raised', bd=1)
        edit_frame.pack(fill='x', padx=20, pady=10, ipadx=10, ipady=10)
        
        tk.Label(edit_frame, text=f"✏️ Edit {mineral_name}", 
                font=('Segoe UI', 12, 'bold'), bg='white', 
                fg=self.colors['primary']).pack(anchor='w', pady=(0, 10))
        
        # Form fields
        form_fields = tk.Frame(edit_frame, bg='white')
        form_fields.pack(fill='x')
        
        # Mineral Name
        tk.Label(form_fields, text="Mineral Name:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=(0, 10))
        edit_name_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        edit_name_entry.insert(0, mineral_name)
        edit_name_entry.grid(row=0, column=1, sticky='w', pady=5, padx=(0, 20))
        
        # Location
        tk.Label(form_fields, text="Location:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=(0, 10))
        edit_location_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        edit_location_entry.insert(0, mineral_data['Location'])
        edit_location_entry.grid(row=0, column=3, sticky='w', pady=5, padx=(0, 20))
        
        # Production
        tk.Label(form_fields, text="Production:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=(0, 10))
        edit_production_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        edit_production_entry.insert(0, str(mineral_data['Production']))
        edit_production_entry.grid(row=1, column=1, sticky='w', pady=5, padx=(0, 20))
        
        # Color
        tk.Label(form_fields, text="Color:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=1, column=2, sticky='w', pady=5, padx=(0, 10))
        edit_color_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        edit_color_entry.insert(0, mineral_data['Color'])
        edit_color_entry.grid(row=1, column=3, sticky='w', pady=5, padx=(0, 20))
        
        def save_edit():
            new_name = edit_name_entry.get().strip()
            location = edit_location_entry.get().strip()
            production = edit_production_entry.get().strip()
            color = edit_color_entry.get().strip()
            
            if not all([new_name, location, production]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            try:
                production_val = int(production)
            except ValueError:
                messagebox.showerror("Error", "Production must be a number")
                return
                
            # Use data manager to update mineral
            self.data_manager.update_mineral(mineral_name, new_name, location, production_val, color)
            
            messagebox.showinfo("Success", f"Mineral updated successfully!")
            edit_frame.destroy()
            self.refresh_minerals_display()
        
        # Buttons
        button_frame = tk.Frame(edit_frame, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="💾 Save Changes", style='Primary.TButton',
                  command=save_edit).pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="❌ Cancel", style='Secondary.TButton',
                  command=lambda: edit_frame.destroy()).pack(side='left')
        
        ttk.Button(button_frame, text="🗑️ Delete", 
                  command=lambda: self.remove_mineral(mineral_name, edit_frame),
                  style='Secondary.TButton').pack(side='left', padx=(10, 0))

    def remove_mineral(self, mineral_name, parent=None):
        """Remove mineral with confirmation"""
        result = messagebox.askyesno("Confirm Removal", 
                                   f"Are you sure you want to remove {mineral_name}?")
        if result:
            if self.data_manager.delete_mineral(mineral_name):
                messagebox.showinfo("Success", f"Mineral '{mineral_name}' removed successfully!")
                if parent:
                    parent.destroy()
                self.refresh_minerals_display()
