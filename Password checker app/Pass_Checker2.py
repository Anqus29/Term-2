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
            height=60
            )
        self.title_bar.pack(
            side=TOP, 
            fill='x'
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
            pady=40
            )

        # Password entry text
        self.instruction = ttk.Label(
            self,
            text="Enter your password:", 
            font=("Arial", 14)
            )
        self.instruction.pack(
            side=TOP, 
            padx=20, 
            pady=15
            )
            
        # Password entry frame
        self.password_entry_frame = ttk.Frame(self)
        self.password_entry_frame.pack(
            side=TOP,
            padx=20,
            pady=10,
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
        self.show_password_check.pack(side=LEFT, padx=5)


       # Button frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side=TOP, pady=10)

        # Check password button
        self.check_button = ttk.Button(
            self.button_frame, 
            text="Check Password", 
            command=self.check_password, 
            bootstyle="success-OUTLINE"
            
        )
        self.check_button.pack(side=LEFT, padx=5)

        # Save password button
        self.save_password_button = ttk.Button(
            self.button_frame,
            text="Save Password to Clipboard", 
            command=self.save_password, 
            bootstyle="success-OUTLINE"
        )
        self.save_password_button.pack(side=LEFT, padx=5)

        # Generate password button (now in the button row)
        self.create_password_button = ttk.Button(
            self.button_frame, 
            text="Generate Password", 
            command=self.generate_password, 
            bootstyle="success-OUTLINE"
        )
        self.create_password_button.pack(side=LEFT, padx=5)

        # Password length label (instance variable for live update)
        self.password_length_label = ttk.Label(
            self, 
            text="Password Length: 8", 
            font=("Arial", 14)
        )
        self.password_length_label.pack(
            side=TOP, 
            padx=5, 
            pady=20
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
            pady=10, 
        )

        # Result percentage
        self.password_strength = ttk.Progressbar(
            self, 
            orient=HORIZONTAL, 
            length=300, 
            bootstyle="success"
            )
        self.password_strength.pack(
            side=TOP, 
            padx=20, 
            pady=50
            )

        # Password issues
        self.password_issues_label = ttk.Label(
            self, 
            text="", 
            font=("Arial", 14), 
            bootstyle="DANGER"
            )
        self.password_issues_label.pack(
            side=TOP, 
            padx=20, 
            pady=10
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
        self.info_button = ttk.Button(
            self.bottom_frame,
            text="Settings", 
            command=self.settings_window, 
            bootstyle="success-OUTLINE"
        )
        self.info_button.pack(
            side=RIGHT,
            padx=20
        )

        # Information button
        self.info_button = ttk.Button(
            self.bottom_frame,
            text="Information", 
            command=self.info_window, 
            bootstyle="success-OUTLINE"
        )
        self.info_button.pack(
            side=RIGHT
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

    

    #Settings
    def settings_window(self):
        settings_win = ttk.Window(
            themename="superhero", 
            title="Settings", 
            size=(400, 300)
            )
        
        settings_win.configure(bg=settings_win.style.colors.bg)

        settings_title = ttk.Label(
            settings_win, 
            text="Settings", 
            font=("Arial", 18), 
            bootstyle="success",
            foreground="white",
            background=settings_win.style.colors.bg
            )
        
        settings_title.pack(
            side=TOP, 
            pady=20
            )

        # Settings content can be added here
        settings_label = ttk.Label(
            settings_win,
            bootstyle="success",
            text="Settings will be available soon.",
            font=("Arial", 14),
            foreground="white",
            background=settings_win.style.colors.bg
        )
        settings_label.pack(
            padx=20, 
            pady=20
        )

    # Information area
    def info_window(self):
        info_win = ttk.Window(
            themename="superhero", 
            title="Information", 
            size=(600, 400)
            )
        
        info_win.configure(bg=info_win.style.colors.bg)

        info_title = ttk.Label(
            info_win, 
            text="Password Checker Information", 
            font=("Arial", 18), 
            bootstyle="success",
            foreground="white",
            background=info_win.style.colors.bg
            )
        
        info_title.pack(
            side=TOP, 
            pady=20
            )

        info_label = ttk.Label(
            info_win,
            bootstyle="success",
            text="This is a password checker application.\n\n"
                "It checks the strength of your password based on \nvarious criteria including whether the password is a \ncommon one. You can also generate a strong \npassword and save it to your clipboard.",
            font=("Arial", 14),
            foreground="white",
            background=info_win.style.colors.bg
        )
        info_label.pack(
            padx=20, 
            pady=20
            )


if __name__ == "__main__":
    app = ttk.Window(themename="superhero", title="Password Checker", size=(1080, 720))
    PasswordChecker(app)
    app.mainloop()