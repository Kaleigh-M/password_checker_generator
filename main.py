import tkinter as tk
from tkinter import ttk
import random
import string
import zxcvbn

def generate_strong_password(length=16):
    if length < 12:
        raise ValueError("Password length should be at least 12 characters for strength.")
    
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for _ in range(length))

    if (not any(char.isupper() for char in password) or
        not any(char.islower() for char in password) or
        not any(char.isdigit() for char in password) or
        not any(char in string.punctuation for char in password)):
        return generate_strong_password(length)
    
    return password

class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker and Generator")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="Enter Password:").grid(column=0, row=0, sticky=tk.W)
        self.password_entry = ttk.Entry(main_frame, show="*", width=30)
        self.password_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

        check_button = ttk.Button(main_frame, text="Check Strength", command=self.check_password_strength)
        check_button.grid(column=2, row=0, sticky=tk.W)

        generate_button = ttk.Button(main_frame, text="Generate Strong Password", command=self.generate_password)
        generate_button.grid(column=1, row=3, sticky=tk.W)

        self.generated_password_label = ttk.Label(main_frame, text="", font=('Helvetica', 12, 'bold'))
        self.generated_password_label.grid(column=1, row=4, sticky=tk.W)

        self.strength_label = ttk.Label(main_frame, text="", font=('Helvetica', 12, 'bold'))
        self.strength_label.grid(column=1, row=1, sticky=tk.W)

        self.feedback_label = ttk.Label(main_frame, text="", wraplength=400, justify="left")
        self.feedback_label.grid(column=0, row=2, columnspan=3, sticky=(tk.W, tk.E))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def check_password_strength(self):
        password = self.password_entry.get()
        result = zxcvbn.zxcvbn(password)

        score = result['score']
        strength = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"][score]
        self.strength_label.config(text=f"Strength: {strength}")

        feedback = result['feedback']
        suggestions = feedback.get('suggestions', [])

        if len(password) < 12:
            suggestions.append("Consider using at least 12 characters for a stronger password.")
        if not any(char.isdigit() for char in password):
            suggestions.append("Add numbers to your password to increase its strength.")
        if not any(char.isupper() for char in password):
            suggestions.append("Add uppercase letters to your password to increase its strength.")
        if not any(char in string.punctuation for char in password):
            suggestions.append("Add special characters to your password to increase its strength.")
        
        feedback_text = "\n".join(suggestions)
        self.feedback_label.config(text=feedback_text)

    def generate_password(self):
        password = generate_strong_password()
        self.generated_password_label.config(text=f"Generated Password: {password}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()
