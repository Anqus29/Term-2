import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import re
import secrets
import string
import random
import hashlib
import requests


class PasswordChecker(ttk.Frame):
    """
    PassCheck: A password generator and checker app.
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.load_common_passwords()
        self.include_symbols_var = ttk.BooleanVar(value=True)
        self.show_crack_time_var = ttk.BooleanVar(value=True)
        self.pwning_password_var = ttk.BooleanVar(value=True)
        self.create_widgets()

    def load_common_passwords(self):
        """
        Load a set of common passwords from a file.
        """
        try:
            with open(
                "Password checker app/common_passwords.txt",
                "r",
                encoding="utf-8"
            ) as file:
                self.common_passwords_set = set(
                    line.strip().lower() for line in file
                )
        except FileNotFoundError:
            print("common_passwords.txt not found.")
            self.common_passwords_set = set()
        except Exception as exc:
            print(f"Error loading common passwords: {exc}")
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
            text="PassCheck",
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
            pady=(40, 0)
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

        self.password_entry_frame.columnconfigure(0, weight=1)
        self.password_entry_frame.columnconfigure(1, weight=0)

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
            padx=(230, 10)
        )
        self.password_entry.bind("<Return>", lambda event: self.check_password())

        self._password_placeholder = "Enter password here"
        self._placeholder_active = False

        def set_placeholder():
            self.password_entry.delete(0, 'end')
            self.password_entry.insert(0, self._password_placeholder)
            self.password_entry.config(foreground='grey', show='')
            self._placeholder_active = True

        def clear_placeholder(event=None):
            if self._placeholder_active:
                self.password_entry.delete(0, 'end')
                fg = self.winfo_toplevel().style.colors.fg
                self.password_entry.config(foreground=fg, show='*')
                self._placeholder_active = False

        def restore_placeholder(event=None):
            if not self.password_entry.get():
                set_placeholder()

        set_placeholder()
        self.password_entry.bind('<FocusIn>', clear_placeholder)
        self.password_entry.bind('<FocusOut>', restore_placeholder)
        self._set_placeholder = set_placeholder  # Save for theme change

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
        length_label.pack(side=LEFT, padx=(0, 5))

        self.length_var = ttk.IntVar(value=12)
        self.password_length = ttk.Spinbox(
            gen_frame,
            from_=8,
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
            style="warning"
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
        original_theme = self.theme_map[selected_theme]
        style = self.winfo_toplevel().style
        style.theme_use(original_theme)
        # Update placeholder color if active
        if getattr(self, '_placeholder_active', False):
            self.password_entry.config(foreground='grey', show='')

    def check_password(self):
        password = self.password_entry.get()
        # Ignore placeholder for checking
        if getattr(self, '_placeholder_active', False):
            password = ''
        password_score = 0
        password_issues = []
        include_symbols = self.include_symbols_var.get()

        if not password:
            self.password_issues_label.config(
                text="Password cannot be empty",
                bootstyle="DANGER"
            )
            self.password_strength['value'] = 0
            return

        if self.check_for_secrets(password):
            return

        if self.pwning_password_var.get():
            pwned_count = self.is_password_pwned(password)
            if pwned_count:
                password_issues.append(
                    f"This password has appeared in {pwned_count} data breaches! Choose another."
                )
                self.password_issues_label.config(
                    text="\n".join(password_issues),
                    bootstyle="DANGER"
                )
                self.password_strength['value'] = 0
                return

        if self.common_passwords(password):
            self.password_issues_label.config(
                text="This password is too common. Please choose a different one.",
                bootstyle="DANGER"
            )
            self.password_strength['value'] = 0
            return

        checks = [
            (r".{8,}", 3, "Password must be at least 8 characters long"),
            (r"(?=.*[A-Z])", 2, "Password must contain at least one uppercase letter"),
            (r"(?=.*[a-z])", 2, "Password must contain at least one lowercase letter"),
            (r"(?=.*\d)", 3, "Password must contain at least one digit")
        ]

        if include_symbols:
            checks.append(
                (r"(?=.*[!@#$%^&*()_+={}\[\]:;\"'<>?,./\\|`~])", 3, "Password must contain at least one special character")
            )

        for pattern, score, warning in checks:
            if re.search(pattern, password):
                password_score += score
            else:
                password_issues.append(warning)

        if re.search(r"[{}\[\]()<>\';\"\\\/|]", password):
            password_issues.append(
                "For security reasons password must not contain any of the following characters: { } < > [ ] ( ) ; ' \" \\ / |"
            )

        total_score = sum(score for _, score, _ in checks)
        if total_score == 0:
            self.password_strength['value'] = 0
        else:
            self.password_strength['value'] = (password_score / total_score) * 100

        if password_issues:
            self.password_issues_label.config(
                text="\n".join(password_issues),
                bootstyle="DANGER"
            )
        else:
            self.password_issues_label.config(
                text="No issues found. Password is strong!",
                bootstyle="SUCCESS"
            )

        # Show crack time if enabled
        if self.show_crack_time_var.get():
            crack_time = self.estimate_crack_time(password)
            self.password_issues_label.config(
                text=f"{self.password_issues_label.cget('text')}\nEstimated crack time: {crack_time}"
            )

    def generate_password(self):
        # Remove placeholder if present
        if getattr(self, '_placeholder_active', False):
            self.password_entry.delete(0, 'end')
            self.password_entry.config(foreground='black', show='*')
            self._placeholder_active = False

        self.password_entry.delete(0, 'end')
        length = self.length_var.get()
        include_symbols = self.include_symbols_var.get()

        lowers = string.ascii_lowercase
        uppers = string.ascii_uppercase
        digits = string.digits
        punctuation = '!@#$%^&*-_=+:,.?'

        required_types = [lowers, uppers, digits]
        if include_symbols:
            required_types.append(punctuation)

        # Ensure password length is at least the number of required types
        if length < len(required_types):
            length = len(required_types)
            self.length_var.set(length)

        # Always include at least one of each selected type
        password_characters = [secrets.choice(charset) for charset in required_types]
        all_characters = ''.join(required_types)

        # Fill the rest of the password
        password_characters += [secrets.choice(all_characters) for _ in range(length - len(password_characters))]
        random.shuffle(password_characters)

        self.password_entry.insert(0, ''.join(password_characters))
        self.check_password()

    def save_password(self):
        password = self.password_entry.get()
        if getattr(self, '_placeholder_active', False):
            return
        if password:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            self.master.update()

    def common_passwords(self, password):
        return password.strip().lower() in self.common_passwords_set

    def is_password_pwned(self, password):
        sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return False  # API error, treat as not pwned
            for line in response.text.splitlines():
                hash_suffix, count = line.split(':')
                if hash_suffix.strip().upper() == suffix:
                    return int(count)
            return 0  # Not found
        except Exception as e:
            print(f"Pwned check failed: {e}")
            return False  # Network error, treat as not pwned

    def toggle_password(self):
        # Only toggle if not showing placeholder
        if getattr(self, '_placeholder_active', False):
            return
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
            self.show_password_check.config(text="Hide password ")
        else:
            self.password_entry.config(show='*')
            self.show_password_check.config(text="Show password")

    def check_for_secrets(self, password):
        # Pop culture and weak password Easter eggs
        secrets = [
            ("bean", "BEANNNNN"),
            ("roman", "Warning do not approach"),
            ("angus", "The best of course"),
            ("finn", "Warning "),
            ("fong", "Its Fonging time"),
            ("starwars", "May the force be with you"),
            ("password", "Please do not use 'password' as a password"),
            ("123456", "Come on, you can do better than that!"),
            ("qwerty", "Everyone has a keyboard"),
            ("precious", "One password to rule them all? Not a good idea!"),
            ("pokemon", "Gotta catch 'em all, but not with this password!"),
            ("never gonna give you up", "Never gonna give you up, never gonna let you down!"),
            ("minecraft", "Crafting a better password is a good idea!"),
            ("pikachu", "Gotta catch a better password!"),
            ("hogwarts", "Alohomora won’t unlock your security!"),
            ("batman", "Even superheroes need stronger passwords!"),
            ("frodo", "One password to rule them all? Not a good idea!"),
            ("winteriscoming", "A Lannister always pays his debts, but don’t pay with your password!"),
            ("creeper", "That’s a blocky password—try something less common!"),
            ("spongebob", "Is mayonnaise a password? No!"),
            ("dundermifflin", "Bears. Beets. Battlestar Galactica. Bad password."),
            ("mario", "It’s-a me, a weak password!"),
            ("tardis", "Don’t let the Daleks exterminate your security!"),
            ("heisenberg", "Say my name… but not as your password!"),
            ("disney", "Let it go… and pick a stronger password!"),
            ("sus", "That password is kinda sus…"),
            ("fortnite", "Victory Royale? Not with this password!"),
            ("zelda", "It’s dangerous to go alone—use a better password!"),
        ]
        for secret_code, response in secrets:
            if secret_code.lower() in password.lower():
                self.password_issues_label.config(
                    text=response,
                    bootstyle="DANGER"
                )
                return True
        return False

    def estimate_crack_time(self, password):
        guesses_per_second = 1e10
        charset = 0
        if any(c.islower() for c in password):
            charset += 26
        if any(c.isupper() for c in password):
            charset += 26
        if any(c.isdigit() for c in password):
            charset += 10
        if any(c in '!@#$%^&*-_=+:,.?' for c in password):
            charset += len('!@#$%^&*-_=+:,.?')
        if charset == 0:
            return "Very weak"
        total_guesses = charset ** len(password)
        seconds = total_guesses / guesses_per_second

        max_seconds = 10**20
        if seconds > max_seconds:
            return "Longer than the heat death of the universe"

        intervals = [
            ('trillions of years', 60*60*24*365*1e12),
            ('billions of years', 60*60*24*365*1e9),
            ('millions of years', 60*60*24*365*1e6),
            ('millennia', 60*60*24*365*1000),
            ('centuries', 60*60*24*365*100),
            ('decades', 60*60*24*365*10),
            ('years', 60*60*24*365),
            ('days', 60*60*24),
            ('hours', 60*60),
            ('minutes', 60),
            ('seconds', 1)
        ]
        for name, count in intervals:
            value = seconds // count
            if value >= 1:
                return f"~{int(value)} {name}"
        return "<1 second"

    def settings_window(self):
        if hasattr(self, 'settings_win'):
            try:
                if self.settings_win.winfo_exists():
                    self.settings_win.destroy()
            except Exception:
                pass

        self.settings_win = ttk.Toplevel(self)
        self.settings_win.title("Settings")
        self.settings_win.geometry("600x400")
        self.settings_win.resizable(False, False)

        settings_title = ttk.Label(
            self.settings_win,
            text="Settings",
            font=("Arial", 18),
            bootstyle="success"
        )
        settings_title.pack(pady=20)

        style = self.winfo_toplevel().style
        theme_names = style.theme_names()
        themes = [theme.capitalize() for theme in theme_names]
        theme_map = dict(zip(themes, theme_names))

        theme_label = ttk.Label(self.settings_win, text="Select Theme:")
        theme_label.pack(pady=(20, 5))

        self.theme_combo = ttk.Combobox(self.settings_win, values=themes, state="readonly", width=20)
        self.theme_combo.set(style.theme.name.capitalize())
        self.theme_combo.pack(pady=10)

        self.theme_map = theme_map
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        symbols_check = ttk.Checkbutton(
            self.settings_win,
            text="Include Symbols in Password",
            variable=self.include_symbols_var
        )
        symbols_check.pack(pady=(30, 10))

        crack_time_check = ttk.Checkbutton(
            self.settings_win,
            text="Show password strength as crack time",
            variable=self.show_crack_time_var
        )
        crack_time_check.pack(pady=10)

        pwned_password = ttk.Checkbutton(
            self.settings_win,
            text="Check password against pwned database",
            variable=self.pwning_password_var
        )
        pwned_password.pack(pady=10)

    def info_window(self):
        if hasattr(self, 'info_win'):
            try:
                if self.info_win.winfo_exists():
                    self.info_win.destroy()
            except Exception:
                pass

        current_theme = self.winfo_toplevel().style.theme.name
        self.info_win = ttk.Toplevel(self)
        self.info_win.title("Information")
        self.info_win.geometry("800x600")
        self.info_win.resizable(False, False)

        if current_theme in ["superhero"]:
            text_colour = "white"
        else:
            text_colour = "black"

        info_title = ttk.Label(
            self.info_win,
            text="Password Checker Information",
            font=("Arial", 18),
            bootstyle="success",
            foreground=text_colour,
            background=self.info_win.style.colors.bg
        )
        info_title.pack(
            side=TOP,
            pady=20
        )

        info_label = ttk.Label(
            self.info_win,
            bootstyle="success",
            text="Welcome to PassCheck\n"
                 "Created by Angus Briscoe\n\n"
                 "The app checks whether a password is considered safe based on various criteria including whether the password is a common one. "
                 "You can also generate a strong password and save it to your clipboard.\n\n"
                 "Settings may be changed in the settings window.\n\n"
                 "For more information, please visit the GitHub repository.",
            font=("Arial", 14),
            foreground=text_colour,
            background=self.info_win.style.colors.bg
        )
        info_label.pack(
            padx=20,
            pady=20
        )


if __name__ == "__main__":
    app = ttk.Window(
        themename="superhero",
        title="PassCheck",
        size=(1080, 840),
        resizable=(False, False)
    )
    PasswordChecker(app)
    app.mainloop()