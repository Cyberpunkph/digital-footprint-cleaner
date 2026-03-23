import imaplib
import email
import re
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import csv
from concurrent.futures import ThreadPoolExecutor

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

IGNORE_DOMAINS = [
    "gmail.com", "google.com", "youtube.com",
    "amazonaws.com", "mailchimp.com"
]

CATEGORIES = {
    "Social": ["facebook.com", "instagram.com", "twitter.com", "tiktok.com", "reddit.com"],
    "Shopping": ["amazon.com", "shopee.ph", "lazada.com", "ebay.com"],
    "Finance": ["paypal.com", "gcash.com", "paymaya.com"],
    "Tech": ["github.com", "discord.com"]
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

def extract_domains(text):
    return re.findall(r'https?://([a-zA-Z0-9.-]+)', text)

def process_email(msg_bytes):
    domains = []
    try:
        msg = email.message_from_bytes(msg_bytes)

        # FROM
        sender = msg.get("From", "")
        match = re.search(r'@([a-zA-Z0-9.-]+)', sender)
        if match:
            domains.append(clean_domain(match.group(1)))

        # REPLY-TO
        reply = msg.get("Reply-To", "")
        match = re.search(r'@([a-zA-Z0-9.-]+)', reply)
        if match:
            domains.append(clean_domain(match.group(1)))

        # BODY
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    if body:
                        body = body.decode(errors="ignore")
                        domains += extract_domains(body)
        else:
            body = msg.get_payload(decode=True)
            if body:
                body = body.decode(errors="ignore")
                domains += extract_domains(body)

    except:
        pass

    return [clean_domain(d.lower()) for d in domains if d]

# ---------------- SCAN ----------------
def scan_accounts():
    status_label.config(text="⚡ Scanning (elite mode)...", fg=ACCENT)
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

        for term in SEARCH_TERMS:
            status, messages = imap.search(None, f'(SUBJECT "{term}")')
            if status == "OK":
                ids.extend(messages[0].split())

        ids = list(set(ids))[:200]  # limit

        if not ids:
            messagebox.showinfo("Info", "No emails found.")
            return

        counter = Counter()

        def fetch_and_process(e_id):
            try:
                status, msg_data = imap.fetch(e_id, "(RFC822)")
                if status != "OK":
                    return []
                for response in msg_data:
                    if isinstance(response, tuple):
                        return process_email(response[1])
            except:
                return []
            return []

        # ⚡ MULTITHREADING
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(fetch_and_process, ids)

        for domains in results:
            for d in domains:
                if d not in IGNORE_DOMAINS:
                    counter[d] += 1

        imap.logout()

        # Clear table
        for row in tree.get_children():
            tree.delete(row)

        # Insert results
        for domain, count in counter.most_common():
            tree.insert("", "end", values=(domain, count, categorize(domain)))

        # Top 5 display
        top = counter.most_common(5)
        top_text = " | ".join([f"{d}({c})" for d, c in top])
        stats_label.config(text=f"Top: {top_text}")

        total_label.config(text=f"Total: {len(counter)} domains")
        status_label.config(text="✅ Done", fg="#22c55e")

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

    messagebox.showinfo("Saved", "Exported!")

# ---------------- OPEN ----------------
def open_site():
    selected = tree.focus()
    if not selected:
        return

    domain = tree.item(selected)["values"][0]
    webbrowser.open(f"https://{domain}")

# ---------------- UI ----------------
root = tk.Tk()
root.title("Account Finder ELITE")
root.geometry("950x600")
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

tk.Label(root, text="🕵️ Account Finder ELITE", font=("Segoe UI", 18, "bold"),
         bg=BG, fg=TEXT).pack(pady=10)

frame = tk.Frame(root, bg=CARD)
frame.pack(padx=20, pady=10, fill="x")

tk.Label(frame, text="Gmail", bg=CARD, fg=MUTED).grid(row=0, column=0)
email_entry = tk.Entry(frame, width=40, bg=BG, fg=TEXT, insertbackground=TEXT)
email_entry.grid(row=0, column=1)

tk.Label(frame, text="App Password", bg=CARD, fg=MUTED).grid(row=1, column=0)
password_entry = tk.Entry(frame, show="*", width=40, bg=BG, fg=TEXT, insertbackground=TEXT)
password_entry.grid(row=1, column=1)

tk.Button(frame, text="Scan", command=scan_accounts,
          bg=ACCENT, fg="black").grid(row=0, column=2, rowspan=2, padx=10)

columns = ("Domain", "Emails", "Category")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True, padx=20, pady=10)

bottom = tk.Frame(root, bg=BG)
bottom.pack(fill="x", padx=20)

tk.Button(bottom, text="Open", command=open_site,
          bg="#334155", fg=TEXT).pack(side="left")

tk.Button(bottom, text="Export CSV", command=export_csv,
          bg="#334155", fg=TEXT).pack(side="left", padx=5)

total_label = tk.Label(bottom, text="Total: 0", bg=BG, fg=MUTED)
total_label.pack(side="left", padx=20)

stats_label = tk.Label(bottom, text="Top: -", bg=BG, fg=MUTED)
stats_label.pack(side="left", padx=20)

status_label = tk.Label(bottom, text="Idle", bg=BG, fg=MUTED)
status_label.pack(side="right")

root.mainloop()
