import imaplib
import email
import re
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import csv

# ---------------- THEME ----------------
BG = "#0f172a"
CARD = "#1e293b"
ACCENT = "#38bdf8"
TEXT = "#e2e8f0"
MUTED = "#94a3b8"

# ---------------- CONFIG ----------------
SEARCH_TERMS = [
    "welcome", "verify", "account", "signup",
    "confirm", "password", "security", "login", "reset"
]

# Expanded platform detection
CATEGORIES = {
    "Social": ["facebook.com", "instagram.com", "twitter.com", "tiktok.com", "reddit.com"],
    "Shopping": ["amazon.com", "shopee.ph", "lazada.com", "ebay.com"],
    "Finance": ["paypal.com", "gcash.com", "paymaya.com"],
    "Entertainment": ["netflix.com", "spotify.com", "youtube.com"],
    "Tech": ["github.com", "stackoverflow.com", "discord.com"],
}

# Known useless/noise domains
IGNORE_DOMAINS = [
    "gmail.com", "google.com", "youtube.com",
    "amazonaws.com", "mailchimp.com"
]

DELETE_LINKS = {
    "facebook.com": "https://www.facebook.com/settings?tab=your_facebook_information",
    "instagram.com": "https://www.instagram.com/accounts/remove/request/permanent/",
}

# ---------------- HELPERS ----------------
def clean_domain(domain):
    parts = domain.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else domain

def categorize(domain):
    for cat, domains in CATEGORIES.items():
        if domain in domains:
            return cat
    return "Other"

def extract_domains_from_body(msg):
    domains = []
    try:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    domains += re.findall(r'https?://([a-zA-Z0-9.-]+)', body)
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")
            domains += re.findall(r'https?://([a-zA-Z0-9.-]+)', body)
    except:
        pass
    return domains

# ---------------- SCAN ----------------
def scan_accounts():
    status_label.config(text="🔄 Scanning...", fg=ACCENT)
    root.update()

    try:
        email_user = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email_user or not password:
            messagebox.showwarning("Input Error", "Enter Gmail & App Password")
            return

        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(email_user, password)
        imap.select("inbox")

        ids = []

        # IMAP-safe search
        for term in SEARCH_TERMS:
            status, messages = imap.search(None, f'(SUBJECT "{term}")')
            if status == "OK":
                ids.extend(messages[0].split())

        ids = list(set(ids))

        if not ids:
            messagebox.showinfo("Info", "No emails found.")
            return

        counter = Counter()

        for e_id in ids[:300]:  # limit for speed
            status, msg_data = imap.fetch(e_id, "(RFC822)")
            if status != "OK":
                continue

            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    # FROM email
                    sender = msg.get("From", "")
                    match = re.search(r'@([a-zA-Z0-9.-]+)', sender)
                    if match:
                        domain = clean_domain(match.group(1).lower())
                        if domain not in IGNORE_DOMAINS:
                            counter[domain] += 1

                    # BODY links (🔥 NEW FEATURE)
                    domains = extract_domains_from_body(msg)
                    for d in domains:
                        d = clean_domain(d.lower())
                        if d not in IGNORE_DOMAINS:
                            counter[d] += 1

        imap.logout()

        # Clear table
        for row in tree.get_children():
            tree.delete(row)

        # Insert results
        for domain, count in counter.most_common():
            tree.insert("", "end", values=(domain, count, categorize(domain)))

        # Stats
        total_label.config(text=f"Total Found: {len(counter)} domains")

        status_label.config(text="✅ Scan complete", fg="#22c55e")

    except imaplib.IMAP4.error as e:
        messagebox.showerror("IMAP Error", str(e))
        status_label.config(text="❌ Login failed", fg="red")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="❌ Error", fg="red")

# ---------------- EXPORT ----------------
def export_csv():
    path = filedialog.asksaveasfilename(defaultextension=".csv")
    if not path:
        return

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Domain", "Count", "Category"])

        for row in tree.get_children():
            writer.writerow(tree.item(row)["values"])

    messagebox.showinfo("Saved", "CSV exported!")

# ---------------- OPEN ----------------
def open_site():
    selected = tree.focus()
    if not selected:
        return

    domain = tree.item(selected)["values"][0]
    url = DELETE_LINKS.get(domain, f"https://{domain}")
    webbrowser.open(url)

# ---------------- UI ----------------
root = tk.Tk()
root.title("Account Finder PRO")
root.geometry("900x560")
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background=CARD,
    foreground=TEXT,
    rowheight=28,
    fieldbackground=CARD
)

style.map("Treeview",
    background=[("selected", ACCENT)]
)

# Header
tk.Label(root, text="🔎 Account Finder PRO", font=("Segoe UI", 18, "bold"),
         bg=BG, fg=TEXT).pack(pady=10)

# Input
frame = tk.Frame(root, bg=CARD)
frame.pack(padx=20, pady=10, fill="x")

tk.Label(frame, text="Gmail", bg=CARD, fg=MUTED).grid(row=0, column=0, padx=10)
email_entry = tk.Entry(frame, width=40, bg=BG, fg=TEXT, insertbackground=TEXT)
email_entry.grid(row=0, column=1)

tk.Label(frame, text="App Password", bg=CARD, fg=MUTED).grid(row=1, column=0, padx=10)
password_entry = tk.Entry(frame, show="*", width=40, bg=BG, fg=TEXT, insertbackground=TEXT)
password_entry.grid(row=1, column=1)

tk.Button(frame, text="Scan", command=scan_accounts,
          bg=ACCENT, fg="black").grid(row=0, column=2, rowspan=2, padx=10)

# Table
columns = ("Domain", "Emails", "Category")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True, padx=20, pady=10)

# Bottom
bottom = tk.Frame(root, bg=BG)
bottom.pack(fill="x", padx=20)

tk.Button(bottom, text="Open Site", command=open_site,
          bg="#334155", fg=TEXT).pack(side="left", padx=5)

tk.Button(bottom, text="Export CSV", command=export_csv,
          bg="#334155", fg=TEXT).pack(side="left", padx=5)

total_label = tk.Label(bottom, text="Total Found: 0", bg=BG, fg=MUTED)
total_label.pack(side="left", padx=20)

status_label = tk.Label(bottom, text="Idle", bg=BG, fg=MUTED)
status_label.pack(side="right")

root.mainloop()
