import imaplib
import email
import re
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import csv

# ---------------- THEME COLORS ----------------
BG = "#0f172a"          # dark background
CARD = "#1e293b"        # panels
ACCENT = "#38bdf8"      # blue highlight
TEXT = "#e2e8f0"        # light text
MUTED = "#94a3b8"

# ---------------- CONFIG ----------------
SEARCH_TERMS = [
    "welcome", "verify", "account", "signup",
    "confirm", "password", "security", "login", "reset"
]

CATEGORIES = {
    "Social": ["facebook.com", "instagram.com", "twitter.com", "tiktok.com"],
    "Shopping": ["amazon.com", "shopee.ph", "lazada.com"],
    "Finance": ["paypal.com", "gcash.com"],
    "Entertainment": ["netflix.com", "spotify.com"],
}

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

# ---------------- SCAN ----------------
def scan_accounts():
    status_label.config(text="🔄 Scanning...", fg=ACCENT)
    root.update()

    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(email_entry.get(), password_entry.get())
        imap.select("inbox")

        query = ' OR '.join([f'SUBJECT "{term}"' for term in SEARCH_TERMS])
        _, messages = imap.search(None, query)

        ids = messages[0].split()
        counter = Counter()

        for e_id in ids:
            _, msg_data = imap.fetch(e_id, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    sender = msg.get("From", "")
                    match = re.search(r'@([a-zA-Z0-9.-]+)', sender)

                    if match:
                        domain = clean_domain(match.group(1).lower())
                        counter[domain] += 1

        imap.logout()

        for row in tree.get_children():
            tree.delete(row)

        for domain, count in counter.most_common():
            tree.insert("", "end", values=(domain, count, categorize(domain)))

        status_label.config(text="✅ Scan complete", fg="#22c55e")

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
root.title("Account Finder")
root.geometry("800x520")
root.configure(bg=BG)

# Style
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
tk.Label(root, text="Account Finder", font=("Segoe UI", 18, "bold"),
         bg=BG, fg=TEXT).pack(pady=10)

# Input Card
frame = tk.Frame(root, bg=CARD)
frame.pack(padx=20, pady=10, fill="x")

tk.Label(frame, text="Gmail", bg=CARD, fg=MUTED).grid(row=0, column=0, padx=10, pady=5)
email_entry = tk.Entry(frame, width=40, bg=BG, fg=TEXT, insertbackground=TEXT)
email_entry.grid(row=0, column=1, padx=10)

tk.Label(frame, text="App Password", bg=CARD, fg=MUTED).grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(frame, show="*", width=40, bg=BG, fg=TEXT, insertbackground=TEXT)
password_entry.grid(row=1, column=1, padx=10)

tk.Button(frame, text="Scan", command=scan_accounts,
          bg=ACCENT, fg="black", relief="flat").grid(row=0, column=2, rowspan=2, padx=10)

# Table
columns = ("Domain", "Emails", "Category")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True, padx=20, pady=10)

# Bottom bar
bottom = tk.Frame(root, bg=BG)
bottom.pack(fill="x", padx=20, pady=5)

tk.Button(bottom, text="Open Site", command=open_site,
          bg="#334155", fg=TEXT).pack(side="left", padx=5)

tk.Button(bottom, text="Export CSV", command=export_csv,
          bg="#334155", fg=TEXT).pack(side="left", padx=5)

status_label = tk.Label(bottom, text="Idle", bg=BG, fg=MUTED)
status_label.pack(side="right")

root.mainloop()
