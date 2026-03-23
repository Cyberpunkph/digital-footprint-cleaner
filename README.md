# 🕵️ Account Finder ELITE

A powerful **OSINT-style email analysis tool** that scans your Gmail inbox to discover linked platforms, services, and digital footprints based on email activity.

Built with Python and Tkinter, this tool helps you **identify accounts, platforms, and services associated with your email** by analyzing senders and embedded links.

---

## 🚀 Features

* 🔍 **Deep Email Analysis**

  * Extracts domains from:

    * Sender (`From`)
    * Reply-To headers
    * Email body links

* ⚡ **Multithreaded Scanning**

  * Faster processing using concurrent workers

* 🧠 **Smart Filtering**

  * Removes noise (e.g., Gmail, AWS, tracking services)

* 📊 **Insights Dashboard**

  * Top domains (leaderboard)
  * Total discovered services
  * Categorized results

* 🌐 **Auto Categorization**

  * Social, Finance, Shopping, Tech, etc.

* 📁 **Export Results**

  * Save findings as CSV

* 🔗 **Quick Access**

  * Open detected platforms directly in browser
---

## ⚙️ Requirements

### 🧩 System

* Python **3.8+**
* Linux / Windows / macOS
* Recommended: Kali Linux (for OSINT workflows)

### 📦 Python Libraries

Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install tk numpy pandas matplotlib tkinter email imaplib
```

> Note: `imaplib` and `email` are built-in in most Python versions.

---

## 🔐 Gmail Setup (IMPORTANT)

This tool uses **IMAP**, so Gmail must be configured:

### ✅ Steps:

1. Enable **2-Step Verification**
2. Generate an **App Password**
3. Use that password in the tool (NOT your real password)

👉 Google Account → Security → App Passwords

---

## 🧠 How It Works

```
User Input (Email + App Password)
        ↓
IMAP Connection (Gmail)
        ↓
Search Emails (keywords like "login", "verify")
        ↓
Fetch Emails
        ↓
Extract Data:
    - Sender domains
    - Reply-To domains
    - Links inside emails
        ↓
Clean & Filter Data
        ↓
Categorize Platforms
        ↓
Display Results in UI
        ↓
(Optional) Export CSV / Open Sites
```

---

## 📖 Usage Guide

### ▶️ Run the Tool

```bash
python account_finder_elite.py
```

### 🧭 Steps

1. Enter your **Gmail address**
2. Enter your **App Password**
3. Click **Scan**
4. Wait for analysis to complete
5. Explore results:

   * Domains found
   * Categories
   * Frequency
6. Optional:

   * Click **Open** → Visit site
   * Click **Export CSV** → Save data

---

## 📊 Output Example

| Domain       | Emails | Category |
| ------------ | ------ | -------- |
| facebook.com | 12     | Social   |
| paypal.com   | 5      | Finance  |
| shopee.ph    | 9      | Shopping |

---

## ⚠️ Disclaimer

This tool is intended for:

* ✅ Personal email analysis
* ✅ Security awareness
* ✅ OSINT learning

❌ **Do NOT use on accounts you do not own**
Unauthorized access may violate laws and terms of service.

---

## 🧪 Future Improvements

* 🕵️ Username OSINT scanning (cross-platform)
* 📡 Breach database integration
* 📊 Graph visualization dashboard
* ⚡ Async scanning engine
* 💻 CLI version

---

## 👨‍💻 Author

Developed as part of a cybersecurity / OSINT learning project.

---

## ⭐ Support

If you like this project:

* Star ⭐ the repo
* Share with others
* Improve and contribute

---

## 🧠 Pro Tip

The more emails you have (especially older ones), the more **accurate and powerful** the results will be.

---

🔥 **Account Finder ELITE — Turn your inbox into intelligence**
