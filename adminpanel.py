import tkinter as tk
from tkinter import messagebox, ttk
import requests
from requests.auth import HTTPBasicAuth
import threading
import json
import os
from datetime import datetime

# Настройкиы                                                                                                                                  о
SERVER_URL = "http://185.60.134.181:8988/admin"
USERNAME = "admin"
PASSWORD = "Igbwkejf33ncskfeUQH"

def center_window(window, width, height):
    """Центрирование окна на экране."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def show_custom_message(message_type, message):
    """Отображение кастомного сообщения без звука."""
    top = tk.Toplevel()
    top.overrideredirect(True)
    top.attributes("-topmost", True)
    top.configure(bg="#202020")
    top.geometry("300x150")
    center_window(top, 300, 150)

    if message_type == "error":
        text_color = "#ff4d4d"
    elif message_type == "info":
        text_color = "#4dff4d"
    elif message_type == "warning":
        text_color = "#ffff4d"
    else:
        text_color = "#c6c6c6"

    label = tk.Label(top, text=message, font=("Arial", 10), bg="#202020", fg=text_color, wraplength=280)
    label.pack(pady=20)
    ok_button = ttk.Button(top, text="OK", command=top.destroy, style="TButton")
    ok_button.pack(pady=10)
    top.bind("<Return>", lambda event: top.destroy())
    top.bind("<Escape>", lambda event: top.destroy())

def get_users():
    """Получение списка пользователей с сервера."""
    try:
        response = requests.get(f"{SERVER_URL}/users", auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        show_custom_message("error", f"Не удалось получить список пользователей: {e}")
        return []

def get_user_info(discord_id):
    """Получение информации о пользователе по Discord ID."""
    try:
        response = requests.get(f"{SERVER_URL}/user/{discord_id}", auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        show_custom_message("error", f"Не удалось получить информацию о пользователе: {e}")
        return None

def block_user(discord_id):
    """Блокировка пользователя по Discord ID."""
    try:
        response = requests.post(f"{SERVER_URL}/user/{discord_id}/block", auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        show_custom_message("info", "Пользователь заблокирован.")
    except requests.exceptions.RequestException as e:
        show_custom_message("error", f"Не удалось заблокировать пользователя: {e}")

def unblock_user(discord_id):
    """Разблокировка пользователя по Discord ID."""
    try:
        response = requests.post(f"{SERVER_URL}/user/{discord_id}/unblock", auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        show_custom_message("info", "Пользователь разблокирован.")
    except requests.exceptions.RequestException as e:
        show_custom_message("error", f"Не удалось разблокировать пользователя: {e}")

def delete_user(discord_id):
    """Удаление пользователя по Discord ID."""
    try:
        response = requests.post(f"{SERVER_URL}/user/{discord_id}/delete", auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        show_custom_message("info", "Пользователь удалён.")
    except requests.exceptions.RequestException as e:
        show_custom_message("error", f"Не удалось удалить пользователя: {e}")

def block_all_users():
    """Блокировка всех пользователей."""
    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите заблокировать всех пользователей?"):
        try:
            response = requests.post(f"{SERVER_URL}/users/block_all", auth=HTTPBasicAuth(USERNAME, PASSWORD))
            response.raise_for_status()
            show_custom_message("info", "Все пользователи заблокированы.")
        except requests.exceptions.RequestException as e:
            show_custom_message("error", f"Не удалось заблокировать всех пользователей: {e}")

class UserInfoWindow:
    """Класс для отображения окна с информацией о пользователе."""
    def __init__(self, parent, user_info):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg="#202020")
        self.window.geometry("400x350")

        title_bar = ttk.Frame(self.window, style="Title.TFrame")
        title_bar.pack(fill=tk.X)
        title_label = ttk.Label(title_bar, text=f"Информация о пользователе: {user_info['username']}", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, padx=5)
        close_button = ttk.Button(title_bar, text="X", command=self.window.destroy, style="Close.TButton", width=3)
        close_button.pack(side=tk.RIGHT, padx=2)

        content_frame = ttk.Frame(self.window, style="TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        details_frame = ttk.Frame(content_frame, style="TFrame")
        details_frame.pack(fill=tk.X, pady=5)

        row = 0
        tk.Label(details_frame, text="Discord ID:", font=("Arial", 10, "bold"), bg="#202020", fg="#c6c6c6").grid(row=row, column=0, sticky="e", padx=5, pady=2)
        discord_id_label = tk.Label(details_frame, text=user_info["discord_id"], font=("Arial", 10), bg="#202020", fg="#c6c6c6")
        discord_id_label.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        discord_id_label.bind("<Double-1>", lambda event: self.copy_to_clipboard(user_info["discord_id"]))
        row += 1

        tk.Label(details_frame, text="Username:", font=("Arial", 10, "bold"), bg="#202020", fg="#c6c6c6").grid(row=row, column=0, sticky="e", padx=5, pady=2)
        username_label = tk.Label(details_frame, text=user_info["username"], font=("Arial", 10), bg="#202020", fg="#c6c6c6")
        username_label.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        username_label.bind("<Double-1>", lambda event: self.copy_to_clipboard(user_info["username"]))
        row += 1

        status_text = "Разрешён" if user_info["status"] else "Заблокирован"
        tk.Label(details_frame, text="Статус:", font=("Arial", 10, "bold"), bg="#202020", fg="#c6c6c6").grid(row=row, column=0, sticky="e", padx=5, pady=2)
        tk.Label(details_frame, text=status_text, font=("Arial", 10), bg="#202020", fg="#c6c6c6").grid(row=row, column=1, sticky="w", padx=5, pady=2)
        row += 1

        last_launch_str = user_info["last_launch"]
        if last_launch_str:
            try:
                last_launch_dt = datetime.fromisoformat(last_launch_str.replace("Z", "+00:00"))
                formatted_last_launch = last_launch_dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                formatted_last_launch = "Неверный формат даты"
        else:
            formatted_last_launch = "Неизвестно"
        tk.Label(details_frame, text="Последний запуск:", font=("Arial", 10, "bold"), bg="#202020", fg="#c6c6c6").grid(row=row, column=0, sticky="e", padx=5, pady=2)
        last_launch_label = tk.Label(details_frame, text=formatted_last_launch, font=("Arial", 10), bg="#202020", fg="#c6c6c6")
        last_launch_label.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        last_launch_label.bind("<Double-1>", lambda event: self.copy_to_clipboard(formatted_last_launch))
        row += 1

        tk.Label(content_frame, text="IP-адреса:", font=("Arial", 10, "bold"), bg="#202020", fg="#c6c6c6").pack(anchor="w", padx=5, pady=5)
        self.ip_list = tk.Listbox(content_frame, height=5, bg="#202020", fg="#c6c6c6", font=("Arial", 10), relief="flat", highlightthickness=0)
        for ip in user_info["ips"].split(",") if user_info["ips"] else []:
            self.ip_list.insert(tk.END, ip.strip())
        self.ip_list.pack(fill=tk.X, padx=5, pady=5)
        self.ip_list.bind("<Double-1>", self.copy_ip)

        button_frame = ttk.Frame(content_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=10)

        if user_info["status"]:
            status_button = ttk.Button(button_frame, text="Заблокировать", command=lambda: self.block_user(user_info["discord_id"]), style="TButton")
        else:
            status_button = ttk.Button(button_frame, text="Разблокировать", command=lambda: self.unblock_user(user_info["discord_id"]), style="TButton")
        status_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(button_frame, text="Удалить пользователя", command=lambda: self.delete_user(user_info["discord_id"]), style="TButton")
        delete_button.pack(side=tk.LEFT, padx=5)

        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<ButtonRelease-1>", self.stop_move)
        title_bar.bind("<B1-Motion>", self.do_move)
        self._x = None
        self._y = None

    def copy_to_clipboard(self, text):
        """Копирование текста в буфер обмена."""
        self.parent.clipboard_clear()
        self.parent.clipboard_append(text)
        show_custom_message("info", "Текст скопирован в буфер обмена.")

    def copy_ip(self, event):
        """Копирование выбранного IP-адреса."""
        selected = self.ip_list.curselection()
        if selected:
            ip = self.ip_list.get(selected[0])
            self.copy_to_clipboard(ip)

    def block_user(self, discord_id):
        """Обработка блокировки пользователя."""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите заблокировать этого пользователя?"):
            block_user(discord_id)
            self.window.destroy()
            self.parent.load_users()  # Обновляем список пользователей

    def unblock_user(self, discord_id):
        """Обработка разблокировки пользователя."""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите разблокировать этого пользователя?"):
            unblock_user(discord_id)
            self.window.destroy()
            self.parent.load_users()  # Обновляем список пользователей

    def delete_user(self, discord_id):
        """Обработка удаления пользователя."""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого пользователя?"):
            delete_user(discord_id)
            self.window.destroy()
            self.parent.load_users()  # Обновляем список пользователей

    def start_move(self, event):
        """Начало перемещения окна."""
        self._x = event.x
        self._y = event.y

    def stop_move(self, event):
        """Окончание перемещения окна."""
        self._x = None
        self._y = None

    def do_move(self, event):
        """Перемещение окна."""
        if self._x is not None and self._y is not None:
            deltax = event.x - self._x
            deltay = event.y - self._y
            x = self.window.winfo_x() + deltax
            y = self.window.winfo_y() + deltay
            self.window.geometry(f"+{x}+{y}")

class MainWindow:
    """Основной класс окна управления пользователями."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#202020")
        self.root.geometry("500x400")
        self.root.eval("tk::PlaceWindow . center")
        self.setup_styles()

        title_bar = ttk.Frame(self.root, style="Title.TFrame")
        title_bar.pack(fill=tk.X)
        title_label = ttk.Label(title_bar, text="Управление пользователями", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, padx=5)
        close_button = ttk.Button(title_bar, text="X", command=self.root.destroy, style="Close.TButton", width=3)
        close_button.pack(side=tk.RIGHT, padx=2)

        content_frame = ttk.Frame(self.root, style="TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Добавляем метку для отображения количества пользователей
        self.user_count_label = tk.Label(content_frame, text="Количество пользователей: 0", 
                                        font=("Arial", 10, "bold"), bg="#202020", fg="#c6c6c6")
        self.user_count_label.pack(anchor="w", pady=5)

        search_frame = ttk.Frame(content_frame, style="TFrame")
        search_frame.pack(fill=tk.X, pady=5)
        self.search_entry = ttk.Entry(search_frame, style="TEntry")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_button = ttk.Button(search_frame, text="Поиск", command=self.search_users, style="TButton")
        search_button.pack(side=tk.RIGHT, padx=5)

        self.user_listbox = tk.Listbox(content_frame, bg="#202020", fg="#c6c6c6", font=("Arial", 10), relief="flat", highlightthickness=0)
        self.user_listbox.pack(fill=tk.BOTH, expand=True)
        self.user_listbox.bind("<Double-1>", self.show_user_info)
        self.user_listbox.bind("<Button-3>", self.show_user_menu)  # Привязка правого клика

        button_frame = ttk.Frame(content_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=5)
        refresh_button = ttk.Button(button_frame, text="Обновить", command=self.load_users, style="TButton")
        refresh_button.pack(side=tk.LEFT, padx=5)
        export_button = ttk.Button(button_frame, text="Экспорт ID", command=self.export_ids, style="TButton")
        export_button.pack(side=tk.LEFT, padx=5)
        blockListed_button = ttk.Button(button_frame, text="Заблокировать всех", command=block_all_users, style="TButton")
        blockListed_button.pack(side=tk.RIGHT, padx=5)
        unblock_all_button = ttk.Button(button_frame, text="Разблокировать всех", command=self.unblock_all_users, style="TButton")
        unblock_all_button.pack(side=tk.RIGHT, padx=5)

        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<ButtonRelease-1>", self.stop_move)
        title_bar.bind("<B1-Motion>", self.do_move)
        self._x = None
        self._y = None

        self.load_users()

    def export_ids(self):
        """Экспорт всех Discord ID в файл discord_ids.txt на рабочем столе."""
        try:
            with open(os.path.expanduser("~/Desktop/discord_ids.txt"), "w") as f:
                for user in self.users:
                    f.write(f"{user['discord_id']}\n")
            show_custom_message("info", "Все Discord ID записаны в файл на рабочем столе: discord_ids.txt")
        except Exception as e:
            show_custom_message("error", f"Не удалось записать ID в файл: {e}")

    def unblock_all_users(self):
        """Разблокировка всех пользователей."""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите разблокировать всех пользователей?"):
            try:
                response = requests.post(f"{SERVER_URL}/users/unblock_all", auth=HTTPBasicAuth(USERNAME, PASSWORD))
                response.raise_for_status()
                show_custom_message("info", "Все пользователи разблокированы.")
                self.load_users()  # Обновляем список пользователей
            except requests.exceptions.RequestException as e:
                show_custom_message("error", f"Не удалось разблокировать всех пользователей: {e}")

    def setup_styles(self):
        """Настройка стилей интерфейса."""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#202020")
        self.style.configure("TLabel", background="#202020", foreground="#c6c6c6", font=("Arial", 10, "bold"))
        self.style.configure("TButton", background="#8681e3", foreground="#202020", font=("Arial", 10, "bold"), padding=4, relief="flat")
        self.style.map("TButton", foreground=[("active", "#000000")], background=[("active", "#f4eee6")])
        self.style.configure("Title.TFrame", background="#8681e3")
        self.style.configure("Title.TLabel", background="#8681e3", foreground="#202020", font=("Arial", 10, "bold"))
        self.style.configure("Close.TButton", background="#8681e3", foreground="#202020", font=("Arial", 9, "bold"), padding=2)
        self.style.configure("TEntry", fieldbackground="#303030", foreground="#c6c6c6", font=("Arial", 10))

    def load_users(self):
        """Загрузка списка пользователей в отдельном потоке."""
        def fetch_users():
            users = get_users()
            self.root.after(0, self.update_user_list, users)
        threading.Thread(target=fetch_users, daemon=True).start()

    def update_user_list(self, users):
        """Обновление списка пользователей и метки с количеством в интерфейсе."""
        self.user_listbox.delete(0, tk.END)
        for user in users:
            self.user_listbox.insert(tk.END, user['username'])
        self.users = users
        # Обновляем метку с количеством пользователей
        self.user_count_label.config(text=f"Количество пользователей: {len(users)}")

    def search_users(self):
        """Поиск пользователей по имени."""
        search_term = self.search_entry.get().lower()
        filtered_users = [user for user in self.users if search_term in user["username"].lower()]
        self.user_listbox.delete(0, tk.END)
        for user in filtered_users:
            self.user_listbox.insert(tk.END, user["username"])

    def show_user_info(self, event):
        """Отображение информации о пользователе при двойном клике."""
        selection = self.user_listbox.curselection()
        if selection:
            index = selection[0]
            discord_id = self.users[index]["discord_id"]
            user_info = get_user_info(discord_id)
            if user_info:
                UserInfoWindow(self.root, user_info)

    def show_user_menu(self, event):
        """Отображение меню при правом клике на пользователе."""
        index = self.user_listbox.nearest(event.y)
        if index < 0:
            return
        discord_id = self.users[index]["discord_id"]
        username = self.users[index]["username"]
        
        # Создаем Toplevel окно для меню
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.overrideredirect(True)
        self.menu_window.attributes("-topmost", True)
        self.menu_window.configure(bg="#202020")
        
        # Размещаем окно рядом с местом клика
        x = self.root.winfo_x() + event.x
        y = self.root.winfo_y() + event.y
        self.menu_window.geometry(f"200x100+{x}+{y}")

        # Создаем заголовок с кнопкой "X"
        title_bar = ttk.Frame(self.menu_window, style="Title.TFrame")
        title_bar.pack(fill=tk.X)
        title_label = ttk.Label(title_bar, text=username, style="Title.TLabel")
        title_label.pack(side=tk.LEFT, padx=5)
        close_button = ttk.Button(title_bar, text="X", command=self.menu_window.destroy, style="Close.TButton", width=3)
        close_button.pack(side=tk.RIGHT, padx=2)

        # Создаем фрейм для содержимого
        content_frame = ttk.Frame(self.menu_window, style="TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Добавляем кнопку для удаления
        delete_button = ttk.Button(content_frame, text="Удалить пользователя", command=lambda: self.delete_user_from_menu(discord_id, self.menu_window))
        delete_button.pack(pady=5)

        # Привязываем события для перемещения окна
        self.menu_window.bind_all("<ButtonPress-1>", self.start_move_if_background)
        self.menu_window.bind_all("<ButtonRelease-1>", self.stop_move_menu)
        self.menu_window.bind_all("<B1-Motion>", self.do_move_menu)
        title_bar.bind("<ButtonPress-1>", self.start_move_menu)
        title_bar.bind("<ButtonRelease-1>", self.stop_move_menu)
        title_bar.bind("<B1-Motion>", self.do_move_menu)

        # Привязываем событие для закрытия окна
        self.menu_window.bind("<FocusOut>", lambda e: self.menu_window.destroy())
        self.menu_window.bind("<Escape>", lambda e: self.menu_window.destroy())

        self._menu_x = None
        self._menu_y = None

    def start_move_if_background(self, event):
        """Начать перемещение, если клик был на фоне."""
        if event.widget == self.menu_window or event.widget.master == self.menu_window:
            self.start_move_menu(event)

    def start_move_menu(self, event):
        """Начало перемещения окна меню."""
        self._menu_x = event.x
        self._menu_y = event.y

    def stop_move_menu(self, event):
        """Окончание перемещения окна меню."""
        self._menu_x = None
        self._menu_y = None

    def do_move_menu(self, event):
        """Перемещение окна меню."""
        if self._menu_x is not None and self._menu_y is not None:
            deltax = event.x - self._menu_x
            deltay = event.y - self._menu_y
            x = self.menu_window.winfo_x() + deltax
            y = self.menu_window.winfo_y() + deltay
            self.menu_window.geometry(f"+{x}+{y}")

    def delete_user_from_menu(self, discord_id, menu_window):
        """Удаление пользователя из меню."""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого пользователя?"):
            delete_user(discord_id)
            menu_window.destroy()
            self.load_users()  # Обновляем список пользователей

    def start_move(self, event):
        """Начало перемещения основного окна."""
        self._x = event.x
        self._y = event.y

    def stop_move(self, event):
        """Окончание перемещения основного окна."""
        self._x = None
        self._y = None

    def do_move(self, event):
        """Перемещение основного окна."""
        if self._x is not None and self._y is not None:
            deltax = event.x - self._x
            deltay = event.y - self._y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    app = MainWindow()
    app.root.mainloop()