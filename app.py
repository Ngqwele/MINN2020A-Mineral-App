!pip install folium
!pip install tkinter

import folium
import webbrowser
import os
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import json

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
            "asande": {"password": "mkhulise", "role": "Researcher"}
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
        self.root.title("Ngqwele Minerals - Mineral Management System")
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
        for widget in self.root.winfo_children():
            widget.destroy()

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
        
        tk.Label(header_frame, text="Ngqwele Minerals", 
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
        
        tk.Label(footer_frame, text="© 2024 Ngqwele Minerals. All rights reserved.",
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
        
        tk.Label(title_frame, text="Ngqwele Minerals", font=('Segoe UI', 20, 'bold'),
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
        
        welcome_text = f"""Welcome to Ngqwele Minerals Management System
        As {self.current_user_role}, you have access to comprehensive mineral data, 
        country profiles, interactive maps, and analytical charts to support your 
        decision-making process."""
        
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
                {"name": "📈 Analytics & Charts", "command": self.show_charts, "color": self.colors['danger']},
                {"name": "🗺️ Interactive Map", "command": self.show_map, "color": self.colors['success']}
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
        
        content_frame = tk.Frame(self.root, bg=self.colors['background'], padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Header with management buttons for admins
        header_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
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
        
        # Add mineral form (initially hidden)
        self.add_mineral_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        
        # Minerals cards
        self.minerals_frame = tk.Frame(content_frame, bg=self.colors['background'])
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

    def show_country_profiles(self):
        self.clear_frame()
        self.create_navigation("Country Profiles")
        
        content_frame = tk.Frame(self.root, bg=self.colors['background'], padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Header with management buttons for admins
        header_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        header_frame.pack(fill='x', pady=(0, 20))
        
        total_countries = len(self.data_manager.CountryProfiles)
        total_production = sum(data['Production'] for data in self.data_manager.CountryProfiles.values())
        total_gdp = sum(data['GDP'] for data in self.data_manager.CountryProfiles.values())
        
        stats_text = f"🌍 Regional Overview: {total_countries} Countries | Total Production: {total_production:,} tons | Combined GDP: R{total_gdp:,}M"
        tk.Label(header_frame, text=stats_text, font=('Segoe UI', 12, 'bold'),
                bg='white', fg=self.colors['primary'], pady=15).pack()
        
        # Management buttons for administrators
        if self.current_user_role == "Administrator":
            manage_frame = tk.Frame(header_frame, bg='white')
            manage_frame.pack(pady=(0, 10))
            
            ttk.Button(manage_frame, text="➕ Add Country", 
                      style='Primary.TButton',
                      command=self.show_add_country_form).pack(side='left', padx=5)
        
        # Add country form (initially hidden)
        self.add_country_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        
        # Countries display frame
        self.countries_frame = tk.Frame(content_frame, bg=self.colors['background'])
        self.countries_frame.pack(fill='both', expand=True)
        
        self.refresh_countries_display()

    def show_add_country_form(self):
        """Show the add country form inline"""
        if hasattr(self, 'add_country_frame'):
            self.add_country_frame.pack_forget()
        
        self.add_country_frame = tk.Frame(self.countries_frame, bg='white', relief='raised', bd=1)
        self.add_country_frame.pack(fill='x', padx=20, pady=10, ipadx=10, ipady=10)
        
        tk.Label(self.add_country_frame, text="➕ Add New Country", 
                font=('Segoe UI', 12, 'bold'), bg='white', 
                fg=self.colors['primary']).pack(anchor='w', pady=(0, 10))
        
        # Form fields
        form_fields = tk.Frame(self.add_country_frame, bg='white')
        form_fields.pack(fill='x')
        
        # Country Name
        tk.Label(form_fields, text="Country Name:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=(0, 10))
        self.country_name_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        self.country_name_entry.grid(row=0, column=1, sticky='w', pady=5, padx=(0, 20))
        
        # Production
        tk.Label(form_fields, text="Production:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=(0, 10))
        self.country_production_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        self.country_production_entry.grid(row=0, column=3, sticky='w', pady=5, padx=(0, 20))
        
        # GDP
        tk.Label(form_fields, text="GDP (R Millions):", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=(0, 10))
        self.country_gdp_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        self.country_gdp_entry.grid(row=1, column=1, sticky='w', pady=5, padx=(0, 20))
        
        # Projects
        tk.Label(form_fields, text="Projects:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=1, column=2, sticky='w', pady=5, padx=(0, 10))
        self.country_projects_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        self.country_projects_entry.grid(row=1, column=3, sticky='w', pady=5, padx=(0, 20))
        
        # Color
        tk.Label(form_fields, text="Color:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=(0, 10))
        self.country_color_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        self.country_color_entry.insert(0, "#2ca02c")
        self.country_color_entry.grid(row=2, column=1, sticky='w', pady=5, padx=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(self.add_country_frame, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="💾 Save Country", style='Primary.TButton',
                  command=self.save_country).pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="❌ Cancel", style='Secondary.TButton',
                  command=self.cancel_add_country).pack(side='left')

    def save_country(self):
        """Save new country from inline form"""
        name = self.country_name_entry.get().strip()
        production = self.country_production_entry.get().strip()
        gdp = self.country_gdp_entry.get().strip()
        projects = self.country_projects_entry.get().strip()
        color = self.country_color_entry.get().strip()
        
        if not all([name, production, gdp, projects]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        try:
            production_val = int(production)
            gdp_val = int(gdp)
            projects_val = int(projects)
        except ValueError:
            messagebox.showerror("Error", "Production, GDP, and Projects must be numbers")
            return
            
        if name in self.data_manager.CountryProfiles:
            messagebox.showerror("Error", "Country already exists")
            return
            
        # Use data manager to save country
        self.data_manager.add_country(name, production_val, gdp_val, projects_val, color)
        
        messagebox.showinfo("Success", f"Country '{name}' added successfully!")
        
        # Clear form and refresh display
        self.cancel_add_country()
        self.refresh_countries_display()

    def cancel_add_country(self):
        """Cancel adding country and hide form"""
        if hasattr(self, 'add_country_frame'):
            self.add_country_frame.pack_forget()

    def refresh_countries_display(self):
        """Refresh the countries display"""
        # Clear existing countries display
        for widget in self.countries_frame.winfo_children():
            widget.pack_forget()
        
        # Show countries
        for country, profile in self.data_manager.CountryProfiles.items():
            card = tk.Frame(self.countries_frame, bg='white', relief='raised', bd=1)
            card.pack(fill='x', padx=20, pady=10, ipadx=10, ipady=10)
            
            # Header with country name and actions
            header = tk.Frame(card, bg='white')
            header.pack(fill='x', pady=(0, 10))
            
            tk.Label(header, text=f"🇿🇦 {country}", font=('Segoe UI', 12, 'bold'),
                    bg='white', fg=profile['Color']).pack(side='left')
            
            # Action buttons for admins
            if self.current_user_role == "Administrator":
                action_frame = tk.Frame(header, bg='white')
                action_frame.pack(side='right')
                
                ttk.Button(action_frame, text="✏️ Edit", 
                          command=lambda c=country: self.edit_country(c),
                          style='Secondary.TButton').pack(side='left', padx=2)
                
                ttk.Button(action_frame, text="🗑️ Remove", 
                          command=lambda c=country: self.remove_country(c),
                          style='Secondary.TButton').pack(side='left', padx=2)
            
            # Country info
            info = f"""⚡ Production: {profile['Production']:,} tons
💰 GDP: R{profile['GDP']:,} Million
🏗️ Active Projects: {profile['Projects']}
📊 Economic Rating: {'★★★★☆' if profile['GDP'] > 30000 else '★★★☆☆'}"""
            
            tk.Label(card, text=info, font=('Segoe UI', 10),
                   bg='white', fg=self.colors['dark'], justify='left').pack(anchor='w')

    def edit_country(self, country_name):
        """Edit country inline"""
        country_data = self.data_manager.CountryProfiles[country_name]
        
        # Create edit form
        edit_frame = tk.Frame(self.countries_frame, bg='white', relief='raised', bd=1)
        edit_frame.pack(fill='x', padx=20, pady=10, ipadx=10, ipady=10)
        
        tk.Label(edit_frame, text=f"✏️ Edit {country_name}", 
                font=('Segoe UI', 12, 'bold'), bg='white', 
                fg=self.colors['primary']).pack(anchor='w', pady=(0, 10))
        
        # Form fields
        form_fields = tk.Frame(edit_frame, bg='white')
        form_fields.pack(fill='x')
        
        # Country Name
        tk.Label(form_fields, text="Country Name:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=(0, 10))
        edit_name_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        edit_name_entry.insert(0, country_name)
        edit_name_entry.grid(row=0, column=1, sticky='w', pady=5, padx=(0, 20))
        
        # Production
        tk.Label(form_fields, text="Production:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=(0, 10))
        edit_production_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        edit_production_entry.insert(0, str(country_data['Production']))
        edit_production_entry.grid(row=0, column=3, sticky='w', pady=5, padx=(0, 20))
        
        # GDP
        tk.Label(form_fields, text="GDP:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=(0, 10))
        edit_gdp_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        edit_gdp_entry.insert(0, str(country_data['GDP']))
        edit_gdp_entry.grid(row=1, column=1, sticky='w', pady=5, padx=(0, 20))
        
        # Projects
        tk.Label(form_fields, text="Projects:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=1, column=2, sticky='w', pady=5, padx=(0, 10))
        edit_projects_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        edit_projects_entry.insert(0, str(country_data['Projects']))
        edit_projects_entry.grid(row=1, column=3, sticky='w', pady=5, padx=(0, 20))
        
        # Color
        tk.Label(form_fields, text="Color:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=(0, 10))
        edit_color_entry = ttk.Entry(form_fields, font=('Segoe UI', 10), width=20)
        edit_color_entry.insert(0, country_data['Color'])
        edit_color_entry.grid(row=2, column=1, sticky='w', pady=5, padx=(0, 20))
        
        def save_edit():
            new_name = edit_name_entry.get().strip()
            production = edit_production_entry.get().strip()
            gdp = edit_gdp_entry.get().strip()
            projects = edit_projects_entry.get().strip()
            color = edit_color_entry.get().strip()
            
            if not all([new_name, production, gdp, projects]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            try:
                production_val = int(production)
                gdp_val = int(gdp)
                projects_val = int(projects)
            except ValueError:
                messagebox.showerror("Error", "Production, GDP, and Projects must be numbers")
                return
                
            # Use data manager to update country
            self.data_manager.update_country(country_name, new_name, production_val, gdp_val, projects_val, color)
            
            messagebox.showinfo("Success", f"Country updated successfully!")
            edit_frame.destroy()
            self.refresh_countries_display()
        
        # Buttons
        button_frame = tk.Frame(edit_frame, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="💾 Save Changes", style='Primary.TButton',
                  command=save_edit).pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="❌ Cancel", style='Secondary.TButton',
                  command=lambda: edit_frame.destroy()).pack(side='left')
        
        ttk.Button(button_frame, text="🗑️ Delete", 
                  command=lambda: self.remove_country(country_name, edit_frame),
                  style='Secondary.TButton').pack(side='left', padx=(10, 0))

    def remove_country(self, country_name, parent=None):
        """Remove country with confirmation"""
        result = messagebox.askyesno("Confirm Removal", 
                                   f"Are you sure you want to remove {country_name}?")
        if result:
            if self.data_manager.delete_country(country_name):
                messagebox.showinfo("Success", f"Country '{country_name}' removed successfully!")
                if parent:
                    parent.destroy()
                self.refresh_countries_display()

    def show_map(self):
        locations = [
            {"name": "Cobalt (DRC)", "lat": -4, "lon": 15},
            {"name": "Lithium (Zimbabwe)", "lat": -20, "lon": 30},
            {"name": "Graphite (Mozambique)", "lat": -18, "lon": 35},
            {"name": "Manganese (South Africa)", "lat": -30, "lon": 25}
        ]

        m = folium.Map(location=[-15, 20], zoom_start=4, tiles='OpenStreetMap')

        for loc in locations:
            folium.Marker(
                location=[loc["lat"], loc["lon"]],
                popup=loc["name"],
                tooltip=loc["name"],
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

        map_file = "africa_deposits_map.html"
        m.save(map_file)
        webbrowser.open('file://' + os.path.realpath(map_file))
        
        # Show confirmation
        messagebox.showinfo("Map Opened", 
                          "The interactive map has been opened in your web browser.\n\n" +
                          "Locations marked:\n• Cobalt (DRC)\n• Lithium (Zimbabwe)\n" +
                          "• Graphite (Mozambique)\n• Manganese (South Africa)")

    def show_charts(self):
        self.clear_frame()
        self.create_navigation("Analytics & Charts")
        
        content_frame = tk.Frame(self.root, bg=self.colors['background'], padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Header with table view button
        header_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="Data Analytics Dashboard", 
                font=('Segoe UI', 14, 'bold'), bg='white', 
                fg=self.colors['primary']).pack(pady=15)
        
        # Table view button for researchers and admins
        if self.current_user_role in ["Administrator", "Researcher"]:
            btn_frame = tk.Frame(header_frame, bg='white')
            btn_frame.pack(pady=(0, 10))
            
            ttk.Button(btn_frame, text="📊 Show Data Tables", 
                      style='Primary.TButton',
                      command=self.show_data_tables).pack(side='left', padx=5)
        
        # Create matplotlib charts
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Mineral Production Chart
        minerals = list(self.data_manager.MineralData.keys())
        production = [data['Production'] for data in self.data_manager.MineralData.values()]
        colors = [data['Color'] for data in self.data_manager.MineralData.values()]
        
        ax1.bar(minerals, production, color=colors, alpha=0.8)
        ax1.set_title('Mineral Production (tonnes/day)', fontweight='bold', pad=20)
        ax1.tick_params(axis='x', rotation=45)
        
        # Country GDP Chart
        countries = list(self.data_manager.CountryProfiles.keys())
        gdp = [data['GDP'] for data in self.data_manager.CountryProfiles.values()]
        colors_country = [data['Color'] for data in self.data_manager.CountryProfiles.values()]
        
        ax2.bar(countries, gdp, color=colors_country, alpha=0.8)
        ax2.set_title('Country GDP (R Millions)', fontweight='bold', pad=20)
        ax2.tick_params(axis='x', rotation=45)
        
        # Projects Pie Chart
        projects = [data['Projects'] for data in self.data_manager.CountryProfiles.values()]
        ax3.pie(projects, labels=countries, autopct='%1.1f%%', colors=colors_country)
        ax3.set_title('Projects Distribution', fontweight='bold', pad=20)
        
        # Production Comparison
        country_production = [data['Production'] for data in self.data_manager.CountryProfiles.values()]
        ax4.bar(countries, country_production, color=colors_country, alpha=0.8)
        ax4.set_title('Country Production (tons)', fontweight='bold', pad=20)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout(pad=3.0)
        
        # Embed chart in tkinter
        chart_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        chart_frame.pack(fill='both', expand=True, pady=10)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Chart description
        desc_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        desc_frame.pack(fill='x', pady=10)
        
        desc_text = """📊 Analytics Dashboard Overview:
• Mineral Production: Daily output across different minerals
• Country GDP: Economic strength of operating countries  
• Projects Distribution: Allocation of mining projects
• Country Production: Production capacity by country"""
        
        tk.Label(desc_frame, text=desc_text, font=('Segoe UI', 10),
                bg='white', fg=self.colors['dark'], justify='left', pady=10).pack()

    def show_data_tables(self):
        """Show data in table format"""
        self.clear_frame()
        self.create_navigation("Data Tables")
        
        content_frame = tk.Frame(self.root, bg=self.colors['background'], padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill='both', expand=True, pady=10)
        
        # Minerals tab
        minerals_frame = ttk.Frame(notebook)
        notebook.add(minerals_frame, text="📊 Minerals Data")
        
        # Create minerals table
        minerals_columns = ('Mineral', 'Location', 'Production', 'Color')
        minerals_tree = ttk.Treeview(minerals_frame, columns=minerals_columns, show='headings', height=8)
        
        for col in minerals_columns:
            minerals_tree.heading(col, text=col)
            minerals_tree.column(col, width=150)
        
        for mineral, data in self.data_manager.MineralData.items():
            minerals_tree.insert('', 'end', values=(
                mineral, data['Location'], data['Production'], data['Color']
            ))
        
        minerals_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar for minerals
        minerals_scrollbar = ttk.Scrollbar(minerals_frame, orient='vertical', command=minerals_tree.yview)
        minerals_tree.configure(yscrollcommand=minerals_scrollbar.set)
        minerals_scrollbar.pack(side='right', fill='y')
        
        # Countries tab
        countries_frame = ttk.Frame(notebook)
        notebook.add(countries_frame, text="🌍 Countries Data")
        
        # Create countries table
        countries_columns = ('Country', 'Production', 'GDP', 'Projects', 'Color')
        countries_tree = ttk.Treeview(countries_frame, columns=countries_columns, show='headings', height=8)
        
        for col in countries_columns:
            countries_tree.heading(col, text=col)
            countries_tree.column(col, width=120)
        
        for country, data in self.data_manager.CountryProfiles.items():
            countries_tree.insert('', 'end', values=(
                country, data['Production'], data['GDP'], data['Projects'], data['Color']
            ))
        
        countries_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar for countries
        countries_scrollbar = ttk.Scrollbar(countries_frame, orient='vertical', command=countries_tree.yview)
        countries_tree.configure(yscrollcommand=countries_scrollbar.set)
        countries_scrollbar.pack(side='right', fill='y')

    def manage_users(self):
        self.clear_frame()
        self.create_navigation("User Management")
        
        content_frame = tk.Frame(self.root, bg=self.colors['background'], padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Current users section
        users_card = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        users_card.pack(fill='both', expand=True, pady=(0, 20))
        
        tk.Label(users_card, text="👥 Current Users", font=('Segoe UI', 14, 'bold'),
                bg='white', fg=self.colors['primary']).pack(anchor='w', padx=20, pady=15)
        
        # Users list with scrollbar
        list_frame = tk.Frame(users_card, bg='white')
        list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create treeview for users
        columns = ('Username', 'Role', 'Actions')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # Define headings
        tree.heading('Username', text='Username')
        tree.heading('Role', text='Role')
        tree.heading('Actions', text='Actions')
        
        tree.column('Username', width=200)
        tree.column('Role', width=150)
        tree.column('Actions', width=100)
        
        # Add users to treeview
        for username, info in self.data_manager.Users.items():
            tree.insert('', 'end', values=(username, info['role'], 'Remove'))
        
        tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Bind remove action
        def on_item_click(event):
            item = tree.selection()[0]
            username = tree.item(item, 'values')[0]
            if username != self.current_user:  # Prevent self-removal
                self.remove_user(username)
            else:
                messagebox.showwarning("Action Denied", "You cannot remove your own account while logged in.")
        
        tree.bind('<Double-1>', on_item_click)
        
        # Add new user section
        add_user_card = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        add_user_card.pack(fill='x', pady=10)
        
        tk.Label(add_user_card, text="➕ Add New User", font=('Segoe UI', 14, 'bold'),
                bg='white', fg=self.colors['primary']).pack(anchor='w', padx=20, pady=15)
        
        form_frame = tk.Frame(add_user_card, bg='white')
        form_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Username
        tk.Label(form_frame, text="Username:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.new_username_entry = ttk.Entry(form_frame, font=('Segoe UI', 10), width=20)
        self.new_username_entry.grid(row=0, column=1, sticky='w', padx=10, pady=5)
        
        # Password
        tk.Label(form_frame, text="Password:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.new_password_entry = ttk.Entry(form_frame, show="•", font=('Segoe UI', 10), width=20)
        self.new_password_entry.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        # Role
        tk.Label(form_frame, text="Role:", font=('Segoe UI', 10, 'bold'),
                bg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.new_role_var = tk.StringVar(value="Researcher")
        role_menu = ttk.Combobox(form_frame, textvariable=self.new_role_var,
                               values=["Administrator", "Investor", "Researcher"],
                               state="readonly", width=18)
        role_menu.grid(row=2, column=1, sticky='w', padx=10, pady=5)
        
        # Add button
        ttk.Button(form_frame, text="Add User", style='Primary.TButton',
                  command=self.add_user).grid(row=3, column=0, columnspan=2, pady=15)

    def create_navigation(self, title):
        """Create navigation header for sub-pages"""
        nav_frame = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        nav_frame.pack(fill='x', side='top')
        nav_frame.pack_propagate(False)
        
        # Back button and title
        back_btn = ttk.Button(nav_frame, text="← Back to Dashboard", 
                             style='Secondary.TButton',
                             command=self.build_dashboard)
        back_btn.pack(side='left', padx=20, pady=10)
        
        tk.Label(nav_frame, text=title, font=('Segoe UI', 16, 'bold'),
                bg=self.colors['primary'], fg='white').pack(expand=True)
        
        # User info
        user_info = tk.Label(nav_frame, 
                           text=f"👤 {self.current_user} ({self.current_user_role})",
                           font=('Segoe UI', 10),
                           bg=self.colors['primary'], fg=self.colors['light'])
        user_info.pack(side='right', padx=20, pady=10)

    def add_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        role = self.new_role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        if username in self.data_manager.Users:
            messagebox.showerror("Error", "Username already exists")
            return
            
        self.data_manager.add_user(username, password, role)
        messagebox.showinfo("Success", f"User '{username}' added successfully!")
        self.manage_users()

    def remove_user(self, username):
        if self.data_manager.delete_user(username):
            messagebox.showinfo("Success", f"User '{username}' removed successfully!")
            self.manage_users()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernApp(root)
    root.mainloop()
