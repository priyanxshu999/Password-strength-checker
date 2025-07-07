import re
import tkinter as tk
from tkinter import messagebox, ttk

# ──────────────────────────────────────────────────────────────────────────────
# 1) Load dictionary words
# ──────────────────────────────────────────────────────────────────────────────
def load_word_set() -> set:
    # try full NLTK corpus
    try:
        import nltk
        from nltk.corpus import words
        try:
            word_list = words.words()
        except LookupError:
            nltk.download("words", quiet=True)
            word_list = words.words()
        if word_list:
            print(f"[INFO] Loaded NLTK corpus ({len(word_list)} words)")
            return {w.lower() for w in word_list if len(w) >= 5}
    except Exception as err:
        print(f"[INFO] Could not load NLTK corpus → {err}")

    # fallback mini‑list (top common words + “human” etc.)
    fallback = """
    password hello human dragon football monkey iloveyou welcome
    sunshine admin login qwerty princess baseball master shadow
    superman hunter letmein trustno1 ninja abc123 soccer charlie
    michael mustang batman 111111 123456 123456789 12345678 000000
    """
    print("[INFO] Using built‑in fallback word list")
    return {w for w in fallback.split() if w}

WORD_SET = load_word_set()


def contains_dict_word(pw: str) -> bool:
    for token in re.findall(r"[a-zA-Z]{5,}", pw.lower()):
        if token in WORD_SET:
            return True
    return False


# ──────────────────────────────────────────────────────────────────────────────
# 2) Password‑strength engine
# ──────────────────────────────────────────────────────────────────────────────
def check_strength(password: str):
    score = 0
    suggestions = []

    # length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 12 characters")

    # character classes
    if re.search(r"[A-Z]", password): score += 1
    else: suggestions.append("Add uppercase letters")

    if re.search(r"[a-z]", password): score += 1
    else: suggestions.append("Add lowercase letters")

    if re.search(r"[0-9]", password): score += 1
    else: suggestions.append("Add numbers")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1
    else: suggestions.append("Add special characters")

    # repeating chars
    if re.search(r"(.)\1\1", password):
        suggestions.append("Avoid repeating characters (e.g. aaa, 111)")

    # dictionary
    if contains_dict_word(password):
        suggestions.append("Avoid dictionary words or common phrases")

    # rating
    if score <= 3:
        return "Weak", suggestions
    elif score <= 5:
        return "Medium", suggestions
    else:
        return "Strong", suggestions


# ──────────────────────────────────────────────────────────────────────────────
# 3) GUI
# ──────────────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("🧠 Password Strength Checker")
root.geometry("500x400")
root.config(bg="#121212")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)

tk.Label(root, text="🧠 Password Strength Checker",
         font=("Segoe UI", 16, "bold"), fg="#00FFFF", bg="#121212").pack(pady=15)

entry = tk.Entry(root, width=30, font=("Consolas", 14), bg="#1f1f1f",
                 fg="#00FFCC", insertbackground="#00FFCC",
                 relief="flat", justify="center")
entry.pack(pady=10)


def analyze_password():
    pwd = entry.get()
    if not pwd:
        messagebox.showwarning("Empty", "Enter a password to check.")
        return
    strength, tips = check_strength(pwd)
    strength_label.config(text=f"🛡 Strength: {strength}",
                          fg={"Weak": "#e74c3c",
                              "Medium": "#f1c40f",
                              "Strong": "#2ecc71"}[strength])
    suggestion_box.config(state=tk.NORMAL)
    suggestion_box.delete(1.0, tk.END)
    suggestion_box.insert(tk.END, "• " + "\n• ".join(tips) if tips
                          else "🔥 Your password is a fortress!")
    suggestion_box.config(state=tk.DISABLED)


tk.Button(root, text="Check Strength", command=analyze_password,
          bg="#0a84ff", fg="white", font=("Segoe UI", 12, "bold"),
          relief="flat", bd=0, padx=10, pady=5).pack(pady=10)

strength_label = tk.Label(root, text="", font=("Segoe UI", 14, "bold"),
                          bg="#121212")
strength_label.pack(pady=5)

suggestion_box = tk.Text(root, height=6, width=50, wrap="word",
                         font=("Consolas", 11), bg="#1e1e1e", fg="#f39c12",
                         relief="flat", state=tk.DISABLED)
suggestion_box.pack(pady=10)

tk.Label(root, text="Built by Priyanshu 💻", font=("Segoe UI", 8),
         fg="#555", bg="#121212").pack(side="bottom", pady=5)

root.mainloop()
