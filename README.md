# cybershield-url-scanner
A Python desktop app with CustomTkinter to detect phishing and suspicious URLs.
# 🛡️ CyberShield URL Scanner Pro

Desktop application built with **Python** and **CustomTkinter** to analyze suspicious links and detect common *phishing* indicators.

## ✨ Features
- Unencrypted connection detection (`HTTP`).
- Identification of redirection characters (`@`) and excessive hyphens.
- Detection of URL shorteners (`bit.ly`, `tinyurl`, etc.) and high-risk domain extensions (`.xyz`, `.tk`, `.top`).
- Modern dark-mode UI with a visual risk progress bar.
- Automatic scan history logging with timestamps (`historial.txt`).

## 🚀 How to Run
1. Install the required library:
   ```bash
   pip install customtkinter
   ```
2. Run the application:
   ```bash
   python app_pro.py
   ```
