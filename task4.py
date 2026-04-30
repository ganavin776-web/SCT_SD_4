import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- DATA ----------------
all_books = []

# ---------------- SCRAPE ----------------
def scrape_books():
    global all_books
    try:
        table.delete(*table.get_children())
        all_books = []

        status_label.config(text="Scraping started...")

        base_url = "https://books.toscrape.com/catalogue/page-{}.html"

        for page in range(1, 4):
            status_label.config(text=f"Scraping page {page}...")
            window.update_idletasks()

            response = requests.get(base_url.format(page))
            soup = BeautifulSoup(response.text, "html.parser")

            books = soup.find_all("article", class_="product_pod")

            for book in books:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text
                rating = book.find("p")["class"][1]
                availability = book.find("p", class_="instock availability").text.strip()

                all_books.append([title, price, rating, availability])

        display_books(all_books)
        status_label.config(text="Scraping completed ✅")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- DISPLAY ----------------
def display_books(data):
    table.delete(*table.get_children())
    for book in data:
        table.insert("", "end", values=book)

# ---------------- SEARCH ----------------
def search_books(event=None):
    query = search_var.get().lower()
    filtered = [b for b in all_books if query in b[0].lower()]
    display_books(filtered)

# ---------------- SORT ----------------
def sort_column(index):
    global all_books

    if index == 1:
        sorted_data = sorted(all_books, key=lambda x: float(x[1].replace("£", "")))
    elif index == 2:
        rating_map = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
        sorted_data = sorted(all_books, key=lambda x: rating_map.get(x[2], 0))
    else:
        sorted_data = sorted(all_books, key=lambda x: x[index])

    display_books(sorted_data)

# ---------------- GUI ----------------
window = tk.Tk()
window.title("Book Scraper Pro")
window.geometry("950x650")
window.configure(bg="#121212")  # 🌙 FULL DARK BACKGROUND

# Title
title = tk.Label(
    window,
    text="📚 Book Scraper Pro",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#121212"
)
title.pack(pady=10)

# ---------------- SEARCH SECTION ----------------
search_frame = tk.Frame(window, bg="#121212")
search_frame.pack(pady=10)

search_label = tk.Label(
    search_frame,
    text="🔍 Search Books:",
    font=("Arial", 12),
    fg="white",
    bg="#121212"
)
search_label.pack(side="left", padx=5)

search_var = tk.StringVar()

search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Arial", 12),
    width=40,
    bg="#000000",
    fg="white",
    insertbackground="white"
)
search_entry.pack(side="left")

search_entry.bind("<KeyRelease>", search_books)

# ---------------- BUTTON ----------------
btn = tk.Button(
    window,
    text="Start Scraping",
    command=scrape_books,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 11)
)
btn.pack(pady=10)

# Status
status_label = tk.Label(
    window,
    text="Ready",
    fg="lightblue",
    bg="#121212"
)
status_label.pack()

# ---------------- TABLE ----------------
frame = tk.Frame(window, bg="#121212")
frame.pack(fill="both", expand=True)

columns = ("Title", "Price", "Rating", "Availability")

style = ttk.Style()
style.theme_use("default")

# Dark table styling
style.configure("Treeview",
    background="#1e1e1e",
    foreground="white",
    fieldbackground="#1e1e1e",
    rowheight=25
)

style.configure("Treeview.Heading",
    background="#000000",
    foreground="white"
)

table = ttk.Treeview(frame, columns=columns, show="headings")

table.heading("Title", text="Title", command=lambda: sort_column(0))
table.heading("Price", text="Price", command=lambda: sort_column(1))
table.heading("Rating", text="Rating", command=lambda: sort_column(2))
table.heading("Availability", text="Availability", command=lambda: sort_column(3))

for col in columns:
    table.column(col, width=220)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
table.pack(fill="both", expand=True)

window.mainloop()