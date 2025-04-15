import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from main import HerbalApp  # Ensure HerbalApp is correctly imported

# File to store user credentials and search history
USER_DATA_FILE = "users.json"

# Load existing user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save user data to file
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

USER_CREDENTIALS = load_user_data()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        with self.canvas.before:
            Color(0.1, 0.5, 0.2, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(size=self.update_rect, pos=self.update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})

        title_label = Label(
            text="[b]Smart Herb[/b]",
            markup=True,
            font_size=28,
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        layout.add_widget(title_label)

        self.username = TextInput(hint_text="Username", multiline=False, size_hint=(None, None), width=280, height=40)
        self.password = TextInput(hint_text="Password", password=True, multiline=False, size_hint=(None, None), width=280, height=40)

        login_button = Button(text="Login", size_hint=(None, None), width=280, height=45, background_color=(0.2, 0.8, 0.3, 1))
        register_button = Button(text="Register", size_hint=(None, None), width=280, height=40, background_color=(0.1, 0.6, 1, 1))

        login_button.bind(on_press=self.validate_login)
        register_button.bind(on_press=self.register_user)

        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_button)
        layout.add_widget(register_button)

        layout.size_hint = (None, None)
        layout.width = 300
        layout.height = 260
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.6}
        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def validate_login(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
            # Pass the username to the HerbalScreen (main screen)
            self.manager.get_screen("main").update_username(username)
            self.manager.current = "main"
        else:
            self.show_popup("Login Failed", "Invalid Username or Password")

    def register_user(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()

        if username in USER_CREDENTIALS:
            self.show_popup("Registration Failed", "Username already exists.")
        elif not username or not password:
            self.show_popup("Error", "Username and Password cannot be empty.")
        else:
            USER_CREDENTIALS[username] = {"password": password, "search_history": []}
            save_user_data(USER_CREDENTIALS)
            self.show_popup("Success", "User registered successfully!")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, font_size=18), size_hint=(0.6, 0.4))
        popup.open()

class HerbalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.herbal_app = HerbalApp(username="")  # Empty username as placeholder
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Add the HerbalApp (main app interface)
        layout.add_widget(self.herbal_app)

        # Logout button
        logout_button = Button(
            text="Logout", 
            size_hint=(None, None), 
            width=280, 
            height=45, 
            background_color=(1, 0.3, 0.3, 1)
        )
        logout_button.bind(on_press=self.logout)  # Bind the logout function
        layout.add_widget(logout_button)

        self.add_widget(layout)  # Ensure the layout is added to the screen

    def update_username(self, username):
        self.herbal_app.username = username  # Set the username to HerbalApp

    def on_enter(self):
        # Get the username from the LoginScreen and update HerbalApp
        username = self.manager.get_screen("login").username.text.strip()
        self.herbal_app.username = username

    def logout(self, instance):
        # Clear the username and reset the app's state
        self.herbal_app.username = ""  # Reset username
        self.manager.current = "login"  # Switch to login screen

class HerbalAppMain(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HerbalScreen(name="main"))
        return sm

if __name__ == '__main__':
    HerbalAppMain().run()
