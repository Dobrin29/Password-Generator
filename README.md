PassGen - Password Generator
============================

1. What is PassGen by Dobrin Dobrev?
-------------------
PassGen is a standalone Windows desktop application that generates strong, cryptographically secure passwords.
It was built in Python and packaged as a single portable .exe file. You don’t need Python or any libraries
to use it — just double-click the file.

The project has two goals:
1) Provide a practical tool for safe password creation.
2) Serve as a learning journey — from raw Python script, through GUI design, to a packaged Windows app.

---

2. Features
-----------
- Uses Python’s "secrets" module (cryptographically secure random numbers).
- Supports customizable character sets:
    * Uppercase (A–Z)
    * Lowercase (a–z)
    * Digits (0–9)
    * Symbols (!@#$%^&*_-)
    * Option to exclude ambiguous characters (O, 0, I, l, 1)
- Adjustable length: 4 to 128 characters.
- Displays entropy estimate and password strength rating.
- One-click copy to clipboard.
- Portable single-file .exe, no Python needed.

---

3. How the App Was Built
-------------------------
Step 1: Core logic (CLI)
- A simple script used "secrets.choice" to generate a password.
- Validated cryptographic randomness before adding complexity.

Step 2: GUI (Tkinter)
- Tkinter was chosen because it is included in Python’s standard library.
- Added options for length, character classes, and entropy feedback.

Step 3: Packaging with PyInstaller
- CLI build:
    pyinstaller --onefile --name PasswordGen passwordgen.py
- GUI build without console:
    pyinstaller --onefile --noconsole --name PassGen gui_passwordgen.py

Step 4: Distribution
- The final .exe is placed in the "dist" folder.
- Because of "--onefile," only PassGen.exe is required.

---

4. How to Use PassGen
----------------------
1) Launch PassGen.exe.
2) Choose password length (4–128).
3) Select which character sets to include.
4) Optionally exclude ambiguous characters.
5) Click "Generate" to create a password.
6) Use "Copy" to place the password in your clipboard.
7) Entropy value and strength label update automatically.

---

5. Security Considerations
---------------------------
- PassGen is completely offline. It does not connect to the internet or save files.
- Passwords only exist in RAM and in the clipboard until pasted.
- Clipboard caution: copied passwords remain until replaced.
- Entropy guide:
    * < 60 bits = Weak
    * 60–89 bits = Reasonable
    * 90–119 bits = Strong
    * 120+ bits = Excellent
- Unsigned .exe files may trigger antivirus warnings. This is expected for home-built tools.

---

6. Possible Improvements
-------------------------
- Add a Windows installer with shortcuts and uninstall option (Inno Setup).
- Digitally sign the .exe to avoid antivirus false positives.
- Extra features:
    * Custom user-defined symbols
    * Passphrase generation (Diceware style)
    * Local encrypted vault storage

---

7. Learning Takeaways
----------------------
- Always use "secrets" instead of "random" for passwords.
- A virtual environment (venv) ensures clean builds.
- PyInstaller options matter:
    * "--onefile" makes apps portable.
    * "--noconsole" is for GUI apps.
- Even a basic GUI (Tkinter) greatly improves usability.
- Removing ambiguous characters helps readability but slightly reduces entropy.
- Installers and code signing are the next step for professional distribution.

---

8. License / Disclaimer
------------------------
This project was created as a learning exercise by Dobrin Dobrev.
Use at your own risk. Always follow organizational password policies and best security practices.
