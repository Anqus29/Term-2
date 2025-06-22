import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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
            height=70
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
        
        # Main frame for everything up to issues
        self.main_frame = ttk.Frame(
            self,
            borderwidth=10,
            relief=SOLID,
            padding=(20, 10),
        )
        self.main_frame.pack(
            side=TOP,
            fill='x',
            padx=60,
            pady=(40,0)
            )

        # Instruction label
        self.instruction = ttk.Label(
            self.main_frame,
            text="Enter your password:", 
            font=("Arial", 14)
            )
        self.instruction.pack(
            side=TOP, 
            padx=20, 
            pady=(10, 10)
            )
            
        # Password entry frame
        self.password_entry_frame = ttk.Frame(
            self.main_frame
            )
        self.password_entry_frame.pack(
            side=TOP,
            anchor=CENTER,
            pady=10,
            fill='x'
            )

        self.password_entry_frame.columnconfigure(0, weight=1)  # Entry column (center)
        self.password_entry_frame.columnconfigure(1, weight=0)  # Checkbox column (right)

        # Password entry field
        self.password_entry = ttk.Entry(
            self.password_entry_frame,
            font=("Arial", 16),         
            bootstyle="success", 
            show="*",
            width=10
            )              
        self.password_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(230,10)
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
        self.show_password_check.grid(
            row=0,
            column=1, 
            sticky=E,
            padx=(0, 130)
            )   

       # Button frame
        self.button_frame = ttk.Frame(
            self.main_frame
        )
        self.button_frame.pack(
            side=TOP, 
            pady=(10,20),
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

    # Password length and generate button frame
        gen_frame = ttk.Frame(self.main_frame)
        gen_frame.pack(
            pady=10
            )

        length_label = ttk.Label(
            gen_frame, 
            text="Password Length:",
            font=("Arial", 14)
            )
        length_label.pack(side=LEFT, 
            padx=(0, 5)
            )

        self.length_var = ttk.IntVar(value=12)
        self.password_length = ttk.Spinbox(
            gen_frame, 
            from_=6, 
            to=64, 
            textvariable=self.length_var, 
            width=5, 
            state="readonly"
            )
        self.password_length.pack(
            side=LEFT, 
            padx=(0, 10)
            )

        gen_btn = ttk.Button(
            gen_frame, 
            text="Generate Password", 
            command=self.generate_password,
            style = "warning"
            )
        gen_btn.pack(side=LEFT)


        # Progress bar
        self.password_strength = ttk.Progressbar(
            self.main_frame, 
            orient=HORIZONTAL, 
            length=600, 
            bootstyle="success"
            )
        self.password_strength.pack(
            side=TOP, 
            padx=20, 
            pady=(20)
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
            pady=(20, 20)
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

    def change_theme(self, event):
        selected_theme = self.theme_combo.get()
        # Map back to original theme name
        original_theme = self.theme_map[selected_theme]
        style = self.winfo_toplevel().style
        style.theme_use(original_theme)

    def check_password(self):
        password = self.password_entry.get()
        password_score = 0
        password_issues = []

        if not password:
            self.password_issues_label.config(
                text="Password cannot be empty",
                bootstyle="DANGER"
                )
            self.password_strength['value'] = 0
            return

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
            self.show_password_check.config(text="Hide password ")
        else:
            self.password_entry.config(show='*')
            self.show_password_check.config(text="Show password")

    def check_for_secrets(self, password):
        return

    def settings_window(self):
        settings_win = ttk.Toplevel(self)
        settings_win.title("Settings")
        settings_win.geometry("400x200")
        settings_win.resizable(False, False)

        style = self.winfo_toplevel().style
        theme_names = style.theme_names()
        themes = [theme.capitalize() for theme in theme_names]
        theme_map = dict(zip(themes, theme_names))  # Map capitalized to original

        theme_label = ttk.Label(settings_win, text="Select Theme:")
        theme_label.pack(pady=(20, 5))

        self.theme_combo = ttk.Combobox(settings_win, values=themes, state="readonly", width=20)
        self.theme_combo.set(style.theme.name.capitalize())
        self.theme_combo.pack(pady=5)

        self.theme_map = theme_map
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)


    # Information window        
    def info_window(self):
        current_theme = self.winfo_toplevel().style.theme.name
        info_win = ttk.Window(
            themename=current_theme,
            title="Information",
            size=(800, 600)
            )
        
        info_win.configure(bg=info_win.style.colors.bg)

        if current_theme in ["superhero"]:
            text_colour = "white"
        else:
            text_colour = "black"

        info_title = ttk.Label(
            info_win,
            text="Password Checker Information",
            font=("Arial", 18),
            bootstyle="success",
            foreground=text_colour,
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
            foreground=text_colour,
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
    resizable=(False, False)
    )
    PasswordChecker(app)
    app.mainloop()