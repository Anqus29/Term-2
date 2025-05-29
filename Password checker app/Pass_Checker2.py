import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import re

class PasswordChecker(ttk.Frame):
    def __init__(self, master=None):

        super().__init__(master)
        self.pack(fill='both', expand=True) 
        self.create_widgets()

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
            pady=60
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

        # Password entry field
        self.password_entry = ttk.Entry(
            self, 
            show="*", 
            font=("Arial", 14), 
            bootstyle="success"
            )
        self.password_entry.pack(
            side=TOP, 
            padx=20, 
            pady=10
            )

        # Button frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side=TOP, 
            pady=10
            )

        # Check password button
        self.check_button = ttk.Button(
            self.button_frame, 
            text="Check Password", 
            command=self.check_password, 
            bootstyle="success-OUTLINE"
            )
        self.check_button.pack(
            side=LEFT, 
            padx=5
            )
        
        self.password_entry.bind("<Return>", 
            lambda event: self.check_password()
            )
        
        # Create password button
        self.create_password_button = ttk.Button(
            self.button_frame, 
            text="Generate Password", 
            command=self.generate_password, 
            bootstyle="success-OUTLINE"
            )
        self.create_password_button.pack(
            side=RIGHT, 
            padx=5
            )
        
        # Save password button
        self.save_password_button = ttk.Button(
            self,
            text="Save Password to Clipboard", 
            command=self.save_password, 
            bootstyle="success-OUTLINE"
            )
        self.save_password_button.pack(
            side=TOP, 
            padx=5,
            pady=10
            )

        self.password_length = ttk.Scale(
            self.button_frame, 
            from_=8, 
            to=20, 
            orient=HORIZONTAL, 
            bootstyle="success"
            )
        self.password_length.pack(
            side=TOP, 
            padx=5, 
            pady=10, 
            )

        # Result percentage
        self.result_slider = ttk.Progressbar(
            self, 
            orient=HORIZONTAL, 
            length=300, 
            bootstyle="success"
            )
        self.result_slider.pack(
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
        self.result_slider['value'] = (password_score / 11) * 100
        if password_issues:
            self.password_issues_label.config(text="\n".join(password_issues))
        else:
            self.password_issues_label.config(text="No issues found. Password is strong!")
    
    def generate_password(self):

        self.password_entry.delete(0, 'end')
        
        self.password_entry.insert(0, "GeneratedPassword123!")
        self.check_password()

    def save_password(self):
        password = self.password_entry.get()
        if password:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            self.master.update()

if __name__ == "__main__":
    app = ttk.Window(themename="superhero", title="Password Checker", size=(1080, 720))
    PasswordChecker(app)
    app.mainloop()