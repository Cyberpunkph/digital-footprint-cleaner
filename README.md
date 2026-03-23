# digital-footprint-cleaner
![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Tkinter](https://img.shields.io/badge/Tkinter-UI-orange)

# 🔍 Account Finder Tool

A simple Python desktop app that scans your Gmail inbox to discover websites you’ve signed up for—so you can clean up your online presence.

---

## ✨ Features

* 📥 Scan Gmail for account-related emails
* 🌐 Extract websites linked to your email
* 🧠 Automatically categorize:

  * Social Media
  * Shopping
  * Finance
  * Entertainment
* 📊 Clean UI (dark mode)
* 🔗 Open account or deletion pages
* 💾 Export results to CSV

---

## ⚙️ Requirements

* Python 3.8+
* Gmail account
* Google App Password (required)

## Suggested Workflow

1. Clone this repository.
2. Install requirements with `pip install -r requirements.txt`.
3. Enable IMAP and create a Google App Password.
4. Run `python account_finder.py`.
5. Enter Gmail credentials in the app.
6. Scan your inbox for account-related emails.
7. Review categorized accounts in the table.
8. Open sites to manage or delete accounts.
9. Export results to CSV for your records.

---

## 🔐 Setup Gmail Access

1. Enable **2-Step Verification**
2. Generate an **App Password**
3. Enable **IMAP access** in Gmail settings

---

## 🚀 How to Run

```bash
git clone https://github.com/yourusername/account-finder.git
cd account-finder
pip install -r requirements.txt
python account_finder.py
```

---

## ⚠️ Security Notice

* This app **does NOT store your credentials**
* Use a **Google App Password**, NOT your real password
* Your data stays local (no external servers)

---

## 📌 Limitations

* Only detects accounts that sent emails
* Cannot find accounts without email history
* Some domains may not be categorized correctly

---

## 🛠️ Future Improvements

* Smarter detection (email body scanning)
* More categories
* Progress bar UI
* Export to more formats
* Multi-email support

---

## 🤝 Contributing

Pull requests are welcome! Feel free to improve detection, UI, or performance.

---

## 📄 License

MIT License

