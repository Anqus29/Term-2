import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import re
from pynput.keyboard import Key, Listener

class PasswordChecker(ttk.Frame):
    def __init__(self, master=None):

        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        # Title
        self.title = ttk.Label(self, text="Password Checker", font=("Arial", 20), bootstyle=SUCCESS)
        self.title.pack(side=TOP, padx=5, pady=20)

        # Invisable frame for spacing
        self.invisible_frame = ttk.Frame(self, bootstyle="success", borderwidth=0, relief="flat")
        self.invisible_frame.pack(side=TOP, fill='none', padx=0, pady=60)

        # Password entry text
        self.instruction = ttk.Label(self, text="Enter your password:", font=("Arial", 14))
        self.instruction.pack(side=TOP, padx=20, pady=15)

        # Password entry field
        self.password_entry = ttk.Entry(self, show="*", font=("Arial", 14), bootstyle="success")
        self.password_entry.pack(side=TOP, padx=20, pady=10)

        # Check password button
        self.check_button = ttk.Button(self, text="Check Password", command=self.check_password, bootstyle="success-OUTLINE")
        self.check_button.pack(side=TOP, padx=20, pady=10)
        self.password_entry.bind("<Return>", lambda event: self.check_password())

        # Result percentage
        self.result_slider = ttk.Progressbar(self, orient=HORIZONTAL, length=300, bootstyle="success")
        self.result_slider.pack(side=TOP, padx=20, pady=50)

        # Password issues
        self.password_issues_label = ttk.Label(self, text="", font=("Arial", 14), bootstyle="DANGER")
        self.password_issues_label.pack(side=TOP, padx=20, pady=10)

    def check_password(self):
        password = self.password_entry.get()
        password_score = 0
        password_issues = []

        checks = [
            (r".{8,}", 1, "Password must be at least 8 characters long"),
            (r"(?=.*[A-Z])", 2, "Password must contain at least one uppercase letter"),
            (r"(?=.*[a-z])", 2, "Password must contain at least one lowercase letter"),
            (r"(?=.*\d)", 3, "Password must contain at least one digit"),
            (r"(?=.*[@$!%*?&])", 3, "Password must contain at least one special character"),
        ]

        for pattern, score, warning in checks:
            if re.search(pattern, password):
                password_score += score
            else:
                password_issues.append(warning)

        if re.search(r"[{}<>]", password):
            password_issues.append("For security reasons password must not contain any of the following characters: {}<>")
        self.result_slider['value'] = password_score * 10
        if password_issues:
            self.password_issues_label.config(text="\n".join(password_issues))
        else:
            self.password_issues_label.config(text="No issues found. Password is strong!")

if __name__ == "__main__":
    app = ttk.Window(themename="superhero", title="Password Checker", size=(1080, 720))
    PasswordChecker(app)
    app.mainloop()