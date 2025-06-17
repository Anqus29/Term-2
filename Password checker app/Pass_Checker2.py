import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import style
import re
import secrets
import string
import random

class PasswordChecker(ttk.Frame):
    def __init__(self, master=None):

        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.load_common_passwords()
        self.create_widgets()
        colours = "success"
        
    
    def load_common_passwords(self):
        try:
            with open("Password checker app/common_passwords.txt", "r") as file:
                self.common_passwords_set = set(line.strip().lower() for line in file)
        except FileNotFoundError:
            print("Password checker app/common_passwords.txt not found. Please ensure the file exists in the same directory as this script.")
            self.common_passwords_set = set()
        except Exception as e:
            print(f"An error occurred while loading common passwords: {e}")
            self.common_passwords_set = set()
        

    
    def create_widgets(self):


        # Title frame
        self.title_bar = ttk.Frame(
            self, 
            bootstyle='success', 
            height=60
            )
        self.title_bar.pack(
            side=TOP, 
            fill='x',
            padx=0,
            pady=(0, 10)
            )
        self.title_bar.pack_propagate(False)

        # Title
        self.title = ttk.Label(
            self.title_bar,
            text="Password Checker",
            font=("Arial", 20),
            bootstyle="inverse-success"
            )
        self.title.pack(
            side=TOP, 
            pady=10
            )

        # Invisable frame for spacing
        self.invisible_frame = ttk.Frame(
            self, 
            borderwidth=0, 
            relief="flat"
            )
        self.invisible_frame.pack(
            side=TOP,
            fill='x', 
            padx=0, 
            pady=(0, 20)
            )

        # Instruction label
        self.instruction = ttk.Label(
            self,
            text="Enter your password:", 
            font=("Arial", 14)
            )
        self.instruction.pack(
            side=TOP, 
            padx=20, 
            pady=(0, 10)
            )
            
        # Password entry frame
        self.password_entry_frame = ttk.Frame(self)
        self.password_entry_frame.pack(
            side=TOP,
            padx=20,
            pady=(0, 10),
            fill='x'
            )

        # Password entry field
        self.password_entry = ttk.Entry(
            self.password_entry_frame,
            font=("Arial", 16),         
            bootstyle="success", 
            show="*",
            width=24
            )              
        self.password_entry.pack(
            side=LEFT,
            fill='x',
            expand=True,
            padx=2,
            pady=2
            )

        self.password_entry.bind("<Return>", lambda event: self.check_password())
        
        self.show_password_var = ttk.BooleanVar(value=False)

        # Show password checkbox
        self.show_password_check = ttk.Checkbutton(
            self.password_entry_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            bootstyle="success-toolbutton"
            )
        self.show_password_check.pack(
            side=LEFT, 
            padx=5
            )


       # Button frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(
            side=TOP, 
            pady=(10, 20),
            )   

        # Check password button
        self.check_button = ttk.Button(
            self.button_frame, 
            text="Check Password", 
            command=self.check_password, 
            bootstyle="success",
            padding=10,
            width=18
            )
        self.check_button.pack(
            side=LEFT, 
            padx=5
            )

        # Generate password button
        self.create_password_button = ttk.Button(
            self.button_frame, 
            text="Generate Password", 
            command=self.generate_password, 
            bootstyle="warning",
            padding=10,
            width=18
            )
        self.create_password_button.pack(
            side=LEFT, 
            padx=5
            )
        
        # Save password button
        self.save_password_button = ttk.Button(
            self.button_frame,
            text="Save Password to Clipboard", 
            command=self.save_password, 
            bootstyle="info",
            padding=10,
            width=18
            )
        self.save_password_button.pack(
            side=LEFT, 
            padx=5
            )

        # Password length label
        self.password_length_label = ttk.Label(
            self, 
            text="Password Length: 8", 
            font=("Arial", 14)
            )
        self.password_length_label.pack(
            side=TOP, 
            padx=5, 
            pady=(10, 0)
            )

        # Password length slider
        self.password_length = ttk.Scale(
            self, 
            from_=8, 
            to=24, 
            orient=HORIZONTAL,
            length=300, 
            bootstyle="success",
            command=lambda value: self.password_length_label.config(
            text="Password Length: " + str(int(float(value))))
            )
        self.password_length.pack(
            side=TOP, 
            padx=0, 
            pady=(0, 40) 
            )

        # Progress bar
        self.password_strength = ttk.Progressbar(
            self, 
            orient=HORIZONTAL, 
            length=600, 
            bootstyle="success"
            )
        self.password_strength.pack(
            side=TOP, 
            padx=20, 
            pady=(0, 20)
            )

        # Password issues label
        self.password_issues_label = ttk.Label(
            self, 
            text="", 
            font=("Arial", 14), 
            bootstyle="DANGER"
            )
        self.password_issues_label.pack(
            side=TOP, 
            padx=20, 
            pady=(0, 20)
            )
        
        # Bottom frame for buttons
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(
            side=BOTTOM, 
            padx=20,
            pady=20,
            fill='x'
            )

        # Settings button
        self.settings_button = ttk.Button(
            self.bottom_frame,
            text="Settings", 
            command=self.settings_window, 
            bootstyle="success-OUTLINE",
            padding=10,
            width=15
            )
        self.settings_button.pack(
            side=LEFT,
            padx=20
            )

        # Information button
        self.info_button = ttk.Button(
            self.bottom_frame,
            text="Information", 
            command=self.info_window, 
            bootstyle="success-OUTLINE",
            padding=10,
            width=15
            )
        self.info_button.pack(
            side=RIGHT,
            padx=20
            )

    def check_password(self):
        password = self.password_entry.get()
        password_score = 0
        password_issues = []

        checks = [
            (r".{8,}", 3, "Password must be at least 8 characters long"),
            (r"(?=.*[A-Z])", 2, "Password must contain at least one uppercase letter"),
            (r"(?=.*[a-z])", 2, "Password must contain at least one lowercase letter"),
            (r"(?=.*\d)", 3, "Password must contain at least one digit"),
            (r"(?=.*[!@#$%^&*-_=+:,.?])", 3, "Password must contain at least one special character"),
        ]

        for pattern, score, warning in checks:
            if re.search(pattern, password):
                password_score += score
            else:
                password_issues.append(warning)


        if self.common_passwords(password):
            self.password_issues_label.config(
                text="This password is too common. Please choose a different one.",
                bootstyle="DANGER"
            )
            self.password_strength['value'] = 0
            return

        if re.search(r"[{}\[\]()<>\';\"\\\/|]", password):
            password_issues.append(
                "For security reasons password must not contain any of the following characters: { } < > [ ] ( ) ; ' \" \\ / |"
                )
                                   
        self.password_strength['value'] = (password_score / 13) * 100
        if password_issues:
            self.password_issues_label.config(text="\n".join(password_issues),
                bootstyle="DANGER"
                )
        else:
            self.password_issues_label.config(
                text="No issues found. Password is strong!",
                bootstyle="SUCCESS"
                )
    
    def generate_password(self):

        self.password_entry.delete(0, 'end')
        length = int(self.password_length.get())

        # Gets possible characters for the password
        lowers = string.ascii_lowercase
        uppers = string.ascii_uppercase
        digits = string.digits
        punctuation = '!@#$%^&*-_=+:,.?'

        # Ensure the password contains at least one of each character type
        password_characters = [
            secrets.choice(lowers),
            secrets.choice(uppers),
            secrets.choice(digits),
            secrets.choice(punctuation)
            ]
        
        # Fill the rest of the password with random characters
        all_characters = lowers + uppers + digits + punctuation
        password_characters += [secrets.choice(all_characters) for _ in range(length - 4)]
        random.shuffle(password_characters)

        self.password_entry.insert(0, ''.join(password_characters))
        self.check_password()

    # Save password to clipboard
    def save_password(self):
        password = self.password_entry.get()
        if password:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            self.master.update()

    # Check if the password is common
    def common_passwords(self, password):
        return (password.strip().lower() in self.common_passwords_set)
    
    def toggle_password(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    

    def settings_window(self):

        

        current_theme = self.winfo_toplevel().style.theme.name
        settings_win = ttk.Window(
            themename=current_theme,
            title="Settings", 
            size=(600, 400)
            )
        settings_win.configure(bg=settings_win.style.colors.bg)

        if current_theme in ["superhero"]:
            text_color = "white"
        else:
            text_color = "black"

        settings_title = ttk.Label(
            settings_win, 
            text="Settings", 
            font=("Arial", 18), 
            bootstyle="success",
            foreground=text_color,
            background=settings_win.style.colors.bg
        )
        settings_title.pack(
            side=TOP, 
            pady=20
        )
        
        settings_frame = ttk.Frame(settings_win)
        settings_frame.pack(
            fill=BOTH, 
            expand=True
        )

        dark_mode_var = ttk.BooleanVar(value=self.winfo_toplevel().style.theme.name in ["superhero", "darkly"])
        def toggle_dark_mode():
            style = self.winfo_toplevel().style
            if style.theme.name in ["superhero", "darkly"]:
                style.theme_use("flatly")  # or another light theme
                dark_mode_var.set(False)
            else:
                style.theme_use("superhero")
                dark_mode_var.set(True)

    # Dark mode toggle
        settings_win.dark_mode = ttk.Checkbutton(
            settings_frame,
            bootstyle="success-toolbutton",
            text="Dark Mode",
            variable=dark_mode_var,
            command=toggle_dark_mode
            )
        settings_win.dark_mode.pack(
            side=TOP,
            padx=20, 
            pady=20,
            expand=True
            )

    # Information window        
    def info_window(self):

        
        current_theme = self.winfo_toplevel().style.theme.name
        info_win = ttk.Window(
            themename=current_theme,
            title="Information",
            size=(800, 600)
            )
        info_win.configure(bg=info_win.style.colors.bg)

        # Choose text color based on theme
        if current_theme in ["superhero"]:
            text_color = "white"
        else:
            text_color = "black"

        info_title = ttk.Label(
            info_win,
            text="Password Checker Information",
            font=("Arial", 18),
            bootstyle="success",
            foreground=text_color,
            background=info_win.style.colors.bg
            )
        info_title.pack(
            side=TOP,
            pady=20
            )

        info_label = ttk.Label(
            info_win,
            bootstyle="success",
            text="Welcome to my password checker app\n"
                "Created by Angus Briscoe\n\n"
                "The app checks whether a password is considered safe based on various criteria including whether the password is a common one. "
                "You can also generate a strong password and save it to your clipboard.\n\n"
                "Settings may be changed in the settings window.\n\n"
                "For more information, please visit the GitHub repository.",
            font=("Arial", 14),
            foreground=text_color,
            background=info_win.style.colors.bg
            )
        info_label.pack(
            padx=20,
            pady=20
            )

if __name__ == "__main__":
    app = ttk.Window(themename="superhero",
    title="Password Checker", 
    size=(1080, 840),
    minsize=(800, 800))
    PasswordChecker(app)
    app.mainloop()