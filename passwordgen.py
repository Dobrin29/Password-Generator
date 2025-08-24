import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import math

APP_TITLE = "Password Generator v.1.Dobrin"
DEFAULT_LENGTH = 15
MIN_LENGTH = 4
MAX_LENGTH = 32
AMBIGUOUS = set("O0Il1")

def build_alphabet(use_upper, use_lower, use_digits, use_symbols, avoid_ambiguous):
    groups = []
    if use_upper:
        groups.append(string.ascii_uppercase)
    if use_lower:
        groups.append(string.ascii_lowercase)
    if use_digits:
        groups.append(string.digits)
    if use_symbols:
        groups.append("!@#$%^&*_-")

    if not groups:
        raise ValueError("Select at least one character class.")

    # Merge groups
    alphabet = "".join(groups)

    if avoid_ambiguous:
        alphabet = "".join(ch for ch in alphabet if ch not in AMBIGUOUS)

        # If a group becomes empty after filtering, we need to ensure coverage
        # We'll validate later when picking at least one from each group.

    if len(alphabet) == 0:
        raise ValueError("Alphabet empty after filtering; relax constraints.")

    return groups, alphabet

def generate_password(length, use_upper, use_lower, use_digits, use_symbols, avoid_ambiguous):
    if length < MIN_LENGTH:
        raise ValueError(f"Length must be ≥ {MIN_LENGTH}.")

    groups, alphabet = build_alphabet(use_upper, use_lower, use_digits, use_symbols, avoid_ambiguous)

    # Ensure at least one char from each selected group (post-filtering).
    selected = []
    for grp in groups:
        pool = [ch for ch in grp if (not avoid_ambiguous or ch not in AMBIGUOUS)]
        if not pool:
            raise ValueError("A selected class became empty after removing ambiguous characters.")
        selected.append(secrets.choice(pool))

    # Fill the rest from aggregate alphabet.
    remaining = length - len(selected)
    if remaining < 0:
        raise ValueError("Length is smaller than number of selected character classes.")
    selected += [secrets.choice(alphabet) for _ in range(remaining)]

    # Shuffle securely.
    secrets.SystemRandom().shuffle(selected)
    return "".join(selected), len(alphabet)

def estimate_entropy(bits_per_char, length):
    # Approximate Shannon entropy: log2(|alphabet|^length) = length * log2(|alphabet|)
    if bits_per_char <= 0:
        return 0.0
    return length * math.log2(bits_per_char)

def entropy_label(alphabet_size, length):
    # Use alphabet_size directly: bits_per_char = log2(alphabet_size)
    if alphabet_size <= 1:
        return "Invalid", 0.0, "gray"
    bits = length * math.log2(alphabet_size)
    if bits < 60:
        return "Weak", bits, "red"
    elif bits < 90:
        return "Reasonable", bits, "orange"
    elif bits < 120:
        return "Strong", bits, "green"
    else:
        return "Excellent", bits, "blue"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("520x340")
        self.minsize(520, 340)
        try:
            # Improve scaling on high-DPI displays.
            self.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.length_var = tk.IntVar(value=DEFAULT_LENGTH)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=True)

        self.password_var = tk.StringVar(value="")
        self.alphabet_size = 0

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 8}

        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True)

        # Length
        row0 = ttk.Frame(frm); row0.pack(fill="x", **pad)
        ttk.Label(row0, text="Length").pack(side="left")
        self.len_spin = ttk.Spinbox(row0, from_=MIN_LENGTH, to=MAX_LENGTH, textvariable=self.length_var, width=6)
        self.len_spin.pack(side="left", padx=10)

        # Checkboxes
        row1 = ttk.LabelFrame(frm, text="Character classes")
        row1.pack(fill="x", **pad)
        ttk.Checkbutton(row1, text="Uppercase A–Z", variable=self.upper_var).pack(side="left", padx=8, pady=6)
        ttk.Checkbutton(row1, text="Lowercase a–z", variable=self.lower_var).pack(side="left", padx=8, pady=6)
        ttk.Checkbutton(row1, text="Digits 0–9", variable=self.digits_var).pack(side="left", padx=8, pady=6)
        ttk.Checkbutton(row1, text="Symbols !@#$%^&*_-", variable=self.symbols_var).pack(side="left", padx=8, pady=6)

        row2 = ttk.Frame(frm); row2.pack(fill="x", **pad)
        ttk.Checkbutton(row2, text="Avoid ambiguous (O, 0, I, l, 1)", variable=self.ambiguous_var).pack(side="left")

        # Output box
        row3 = ttk.LabelFrame(frm, text="Generated password")
        row3.pack(fill="x", **pad)
        self.out_entry = ttk.Entry(row3, textvariable=self.password_var, font=("Consolas", 12))
        self.out_entry.pack(fill="x", padx=10, pady=8)

        # Entropy meter
        row4 = ttk.Frame(frm); row4.pack(fill="x", **pad)
        self.entropy_lbl = ttk.Label(row4, text="Entropy: –  |  Strength: –")
        self.entropy_lbl.pack(side="left")

        # Buttons
        row5 = ttk.Frame(frm); row5.pack(fill="x", **pad)
        ttk.Button(row5, text="Generate", command=self.on_generate).pack(side="left")
        ttk.Button(row5, text="Copy", command=self.on_copy).pack(side="left", padx=10)
        ttk.Button(row5, text="Clear", command=self.on_clear).pack(side="left")

        # First run
        self.on_generate()

    def on_generate(self):
        try:
            length = int(self.length_var.get())
            pwd, alpha_size = generate_password(
                length=length,
                use_upper=self.upper_var.get(),
                use_lower=self.lower_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get(),
                avoid_ambiguous=self.ambiguous_var.get()
            )
            self.password_var.set(pwd)
            self.alphabet_size = alpha_size
            label, bits, color = entropy_label(alpha_size, length)
            self.entropy_lbl.configure(text=f"Entropy: {bits:.1f} bits  |  Strength: {label}", foreground=color)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_copy(self):
        pwd = self.password_var.get()
        if not pwd:
            return
        self.clipboard_clear()
        self.clipboard_append(pwd)
        # brief feedback in title bar
        self.after(50, lambda: self.title(f"{APP_TITLE} — Copied"))
        self.after(800, lambda: self.title(APP_TITLE))

    def on_clear(self):
        self.password_var.set("")
        self.entropy_lbl.configure(text="Entropy: –  |  Strength: –", foreground="black")

if __name__ == "__main__":
    app = App()
    app.mainloop()
