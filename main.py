import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.file_name = "books.json"
        self.books = self.load_data()

        # Поля ввода
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Название:").grid(row=0, column=0)
        self.entry_title = tk.Entry(frame)
        self.entry_title.grid(row=0, column=1)

        tk.Label(frame, text="Автор:").grid(row=1, column=0)
        self.entry_author = tk.Entry(frame)
        self.entry_author.grid(row=1, column=1)

        tk.Label(frame, text="Жанр:").grid(row=2, column=0)
        self.entry_genre = tk.Entry(frame)
        self.entry_genre.grid(row=2, column=1)

        tk.Label(frame, text="Страниц:").grid(row=3, column=0)
        self.entry_pages = tk.Entry(frame)
        self.entry_pages.grid(row=3, column=1)

        tk.Button(frame, text="Добавить книгу", command=self.add_book).grid(row=4, columnspan=2, pady=10)

        # Фильтры
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10)

        tk.Label(filter_frame, text="Жанр:").pack(side="left")
        self.filter_genre = tk.Entry(filter_frame, width=10)
        self.filter_genre.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Мин. страниц:").pack(side="left")
        self.filter_pages = tk.Entry(filter_frame, width=5)
        self.filter_pages.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Применить", command=self.update_table).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Сброс", command=self.reset_filter).pack(side="left")

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.pack(padx=10, pady=10)

        self.update_table()

    def add_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        genre = self.entry_genre.get()
        pages = self.entry_pages.get()

        if not title or not author or not genre:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        
        try:
            pages = int(pages)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(new_book)
        self.save_data()
        self.update_table()
        
        # Очистка полей
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_pages.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        f_genre = self.filter_genre.get().lower()
        f_pages = self.filter_pages.get()

        for b in self.books:
            show = True
            if f_genre and f_genre not in b['genre'].lower():
                show = False
            if f_pages and b['pages'] < int(f_pages):
                show = False
            
            if show:
                self.tree.insert("", tk.END, values=(b['title'], b['author'], b['genre'], b['pages']))

    def reset_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_pages.delete(0, tk.END)
        self.update_table()

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()