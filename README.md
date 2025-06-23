# PassCheck

**PassCheck** is a Python application that helps users generate strong, secure passwords and check the strength and safety of their chosen passwords. It is designed to address the common cybersecurity issue of weak and reused passwords.

---

## Features

- **Secure Password Generation:**  
  Generate passwords with a mix of uppercase, lowercase, digits, and symbols.

- **Customizable Length:**  
  Choose your desired password length.

- **Password Strength Checker:**  
  Instantly see how strong your password is, with feedback and suggestions.

- **Common Password Detection:**  
  Prevents use of passwords found in common password lists.

- **Pwned Password Check:**  
  Checks if your password has appeared in known data breaches (requires internet).

- **Clipboard Copy:**  
  Easily copy generated passwords to your clipboard.

- **Theme Customization:**  
  Switch between different visual themes.

- **User-Friendly Interface:**  
  Simple, modern interface built with [ttkbootstrap](https://ttkbootstrap.readthedocs.io/).

- **Fun Easter Eggs:**  
  Get pop culture messages for certain passwords!

---

## Requirements

- Python 3.x
- [ttkbootstrap](https://pypi.org/project/ttkbootstrap/)
- requests

---

## Installation

1. **Clone or download this repository.**
2. **Install dependencies:**
   ```sh
   pip install ttkbootstrap requests

---

## Troubleshooting

- **Pwned Password Check Fails or is Slow:**  
  - Make sure your computer is connected to the internet.
  - If you see timeout or SSL errors, your network may be blocking the Have I Been Pwned API.  
  - Try disabling the pwned password check in the Settings window if you experience lag or errors.

- **App Does Not Start:**  
  - Ensure you have installed all required dependencies (`ttkbootstrap`, `requests`).
  - Make sure you are using Python 3.x.

- **Common Passwords Not Detected:**  
  - Ensure the `common_passwords.txt` file is present in the correct folder (`Password checker app`).

- **Clipboard Copy Not Working:**  
  - Some operating systems or remote desktop environments may restrict clipboard access.

If you encounter other issues, please check your Python installation and dependencies, or contact the developer.
