
import argparse
import asyncio
from configparser import ConfigParser
import configparser
import csv
import ctypes 
from datetime import datetime, timedelta
import io
import json
import logging
from multiprocessing.connection import Listener
import os
import random
import re
import socket
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import inspect  


original_getsource = inspect.getsource
def patched_getsource(obj):
    try:
        return original_getsource(obj)
    except OSError:
        return ""  
inspect.getsource = patched_getsource


import cv2
import GPUtil
import keyboard
import mouse
import mss
import numpy as np
from PIL import Image, ImageGrab, ImageTk
import psutil
import pyautogui
import pyperclip
from pynput import keyboard as pynput_keyboard, mouse as pynput_mouse
from pynput.keyboard import Key, KeyCode, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Controller as MouseController, Button, Listener as MouseListener
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
import torch
import torch.nn as nn
from torchvision import transforms
from ttkthemes import ThemedTk  
import win32con
import win32gui
import wmi

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
pyautogui.FAILSAFE = False





















"""
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)
parser.add_argument('--token')
args = parser.parse_args()
if args.port and args.token:

    try:
        s = socket.socket()
        s.connect(('localhost', args.port))
        s.send(args.token.encode())
        response = s.recv(1024).decode()
        s.close()
        if response != "OK":
            print("Ошибка проверки: неверный токен")
            sys.exit(1)
    except Exception as e:
        print(f"Ошибка проверки: {e}")
        sys.exit(1)
else:
    print("Ошибка: отсутствуют необходимые аргументы")
    sys.exit(1)
"""
RUSSIAN_TO_ENGLISH = {
    'а': 'f', 'б': ',', 'в': 'd', 'г': 'u', 'д': 'l', 'е': 't', 'ё': '`',
    'ж': ';', 'з': 'p', 'и': 'b', 'й': 'q', 'к': 'r', 'л': 'k', 'м': 'v',
    'н': 'y', 'о': 'j', 'п': 'g', 'р': 'h', 'с': 'c', 'т': 'n', 'у': 'e',
    'ф': 'a', 'х': '[', 'ц': 'w', 'ч': 'x', 'ш': 'i', 'щ': 'o', 'ъ': ']',
    'ы': 's', 'ь': 'm', 'э': "'", 'ю': '.', 'я': 'z'
}

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, relative_path)

class KeyTranslator:
    def __init__(self):
        self.controller = KeyboardController() 
        self.pressed_keys = set()
        
    def get_display_key(self, vk_code, keysym):  
        special_keys = {
            8: 'backspace',
            9: 'tab',
            13: 'enter',
            16: 'shift',
            17: 'ctrl',
            18: 'alt',
            20: 'caps lock',
            27: 'esc',
            32: 'space',
            37: 'left', 38: 'up', 39: 'right', 40: 'down',
            45: 'insert', 46: 'delete',
            75: 'k',
            112: 'F1', 113: 'F2', 114: 'F3', 115: 'F4', 116: 'F5',
            117: 'F6', 118: 'F7', 119: 'F8', 120: 'F9', 121: 'F10',
            122: 'F11', 123: 'F12',
        }
        if vk_code in special_keys:
            return special_keys[vk_code]
        elif 48 <= vk_code <= 57:  
            return chr(vk_code)
        elif 65 <= vk_code <= 90:  
            return chr(vk_code).lower()
        elif keysym:
            return keysym
        else:
            return f'Unknown_{vk_code}'

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char in RUSSIAN_TO_ENGLISH:  
                translated_char = RUSSIAN_TO_ENGLISH[key.char]
                self.controller.press(KeyCode.from_char(translated_char))
                self.pressed_keys.add(translated_char)
                return False  

            vk_code = key.vk if hasattr(key, 'vk') else key.value.vk
            pressed_key = self.get_display_key(vk_code, key.name if hasattr(key, 'name') else None)

            
            if self.is_changing_bind or (self.settings_open and (pressed_key == self.config["Hotkeys"] or pressed_key == self.config["Hotkeys"]["HideShowKey"])):
                return

            
            if pressed_key == self.config["Hotkeys"]["HideShowKey"]:
                self.toggle_visibility()
            elif pressed_key == self.config["General"]["ResetStatsKey"]:
                self.reset_all_stats()
        except Exception as e:
            print(f"Error in on_press: {e}")

    def on_release(self, key):
        try:
            char = key.char
            if char in RUSSIAN_TO_ENGLISH:
                translated_char = RUSSIAN_TO_ENGLISH[char]
                if translated_char in self.pressed_keys:
                    self.controller.release(KeyCode.from_char(translated_char))  
                    self.pressed_keys.remove(translated_char)
                return False
            else:
                if key in self.pressed_keys:
                    self.controller.release(key)
                    self.pressed_keys.remove(key)
        except AttributeError:
            if key in self.pressed_keys:
                self.controller.release(key)
                self.pressed_keys.remove(key)

    def start(self):
        with KeyboardListener(on_press=self.on_press, on_release=self.on_release) as listener:  
            listener.join()

try:
    with open(get_resource_path('themes.json'), 'r') as f:
        THEMES = json.load(f)
except FileNotFoundError:
    
    THEMES = {
        "dark": {
            "BACKGROUND_COLOR": "#1e1e1e",
            "BUTTON_COLOR": "#7a75e0",
            "ENTRY_BG_COLOR": "#3a3a3a",
            "TEXT_COLOR": "#9a95e8",
            "HEADER_TEXT_COLOR": "#000000",
            "ACTIVE_BUTTON_COLOR": "#5a55b0",
            "SCROLLBAR_COLOR": "#6f6bc8",
            "FRAME_BG_COLOR": "#1e1e1e",
            "LABEL_BG_COLOR": "#1e1e1e",
            "LABEL_FG_COLOR": "#9a95e8",
            "TEXT_BG_COLOR": "#1e1e1e",
            "TEXT_FG_COLOR": "#9a95e8",
            "TAB_BG_COLOR": "#5a55b0",
            "TAB_FG_COLOR": "#000000",
            "TAB_SELECTED_BG_COLOR": "#7a75e0",
            "TAB_SELECTED_FG_COLOR": "#000000",
            "SCROLLBAR_TROUGH_COLOR": "#282828",
            "SEPARATOR_COLOR": "#7a75e0",
            "ROW_BG_COLOR": "#282828",
            "DIM_TEXT_COLOR": "#888888"
        },
        "light": {
            "BACKGROUND_COLOR": "#f0f0f0",
            "BUTTON_COLOR": "#4a90e2",
            "ENTRY_BG_COLOR": "#ffffff",
            "TEXT_COLOR": "#333333",
            "HEADER_TEXT_COLOR": "#ffffff",
            "ACTIVE_BUTTON_COLOR": "#357abd",
            "SCROLLBAR_COLOR": "#a0c0e8",
            "FRAME_BG_COLOR": "#f0f0f0",
            "LABEL_BG_COLOR": "#f0f0f0",
            "LABEL_FG_COLOR": "#333333",
            "TEXT_BG_COLOR": "#f0f0f0",
            "TEXT_FG_COLOR": "#333333",
            "TAB_BG_COLOR": "#357abd",
            "TAB_FG_COLOR": "#ffffff",
            "TAB_SELECTED_BG_COLOR": "#4a90e2",
            "TAB_SELECTED_FG_COLOR": "#ffffff",
            "SCROLLBAR_TROUGH_COLOR": "#d0d0d0",
            "SEPARATOR_COLOR": "#4a90e2",
            "ROW_BG_COLOR": "#e0e0e0",
            "DIM_TEXT_COLOR": "#666666"
        }
    }

current_theme = "dark"

def set_theme(theme_name):
    global current_theme, BACKGROUND_COLOR, BUTTON_COLOR, ENTRY_BG_COLOR, TEXT_COLOR, HEADER_TEXT_COLOR, \
           ACTIVE_BUTTON_COLOR, SCROLLBAR_COLOR, FRAME_BG_COLOR, LABEL_BG_COLOR, LABEL_FG_COLOR, \
           TEXT_BG_COLOR, TEXT_FG_COLOR, TAB_BG_COLOR, TAB_FG_COLOR, TAB_SELECTED_BG_COLOR, \
           TAB_SELECTED_FG_COLOR, SCROLLBAR_TROUGH_COLOR, SEPARATOR_COLOR, ROW_BG_COLOR, DIM_TEXT_COLOR
    current_theme = theme_name
    theme = THEMES[theme_name]
    BACKGROUND_COLOR = theme["BACKGROUND_COLOR"]
    BUTTON_COLOR = theme["BUTTON_COLOR"]
    ENTRY_BG_COLOR = theme["ENTRY_BG_COLOR"]
    TEXT_COLOR = theme["TEXT_COLOR"]
    HEADER_TEXT_COLOR = theme["HEADER_TEXT_COLOR"]
    ACTIVE_BUTTON_COLOR = theme["ACTIVE_BUTTON_COLOR"]
    SCROLLBAR_COLOR = theme["SCROLLBAR_COLOR"]
    FRAME_BG_COLOR = theme["FRAME_BG_COLOR"]
    LABEL_BG_COLOR = theme["LABEL_BG_COLOR"]
    LABEL_FG_COLOR = theme["LABEL_FG_COLOR"]
    TEXT_BG_COLOR = theme["TEXT_BG_COLOR"]
    TEXT_FG_COLOR = theme["TEXT_FG_COLOR"]
    TAB_BG_COLOR = theme["TAB_BG_COLOR"]
    TAB_FG_COLOR = theme["TAB_FG_COLOR"]
    TAB_SELECTED_BG_COLOR = theme["TAB_SELECTED_BG_COLOR"]
    TAB_SELECTED_FG_COLOR = theme["TAB_SELECTED_FG_COLOR"]
    SCROLLBAR_TROUGH_COLOR = theme["SCROLLBAR_TROUGH_COLOR"]
    SEPARATOR_COLOR = theme["SEPARATOR_COLOR"]
    ROW_BG_COLOR = theme["ROW_BG_COLOR"]
    DIM_TEXT_COLOR = theme["DIM_TEXT_COLOR"]

def make_window_no_activate(hwnd):
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    style |= win32con.WS_EX_NOACTIVATE
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window or not self.text:
            return
        x, y = self.widget.winfo_pointerxy()
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x+10}+{y+10}")
        self.tooltip_window.attributes("-topmost", True)
        label = tk.Label(self.tooltip_window, text=self.text, bg=ENTRY_BG_COLOR, fg=TEXT_COLOR,
                         font=('Roboto', 10, 'bold'), relief='flat', bd=0)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class CustomErrorWindow:
    def __init__(self, app, title, message, buttons=None):
        self.app = app
        if app:
            self.root = tk.Toplevel(app.root)
        else:
            self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=BACKGROUND_COLOR)
        self.choice = None

        title_bar = tk.Frame(self.root, bg=BUTTON_COLOR)
        title_bar.pack(fill=tk.X)
        font_size = self.app.get_scaled_font_size(10) if self.app else 10
        title_label = tk.Label(title_bar, text=title, bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                               font=('Roboto', font_size, 'bold'))
        title_label.pack(side=tk.LEFT, padx=5)
        close_button = tk.Button(title_bar, text="X", command=self.root.destroy, bg=BUTTON_COLOR,
                                 fg=HEADER_TEXT_COLOR, font=('Roboto', font_size - 1, 'bold'),
                                 relief='flat', activebackground=ACTIVE_BUTTON_COLOR,
                                 activeforeground=HEADER_TEXT_COLOR)
        close_button.pack(side=tk.RIGHT, padx=2)

        message_label = tk.Label(self.root, text=message, bg=BACKGROUND_COLOR, fg=TEXT_COLOR,
                                 font=('Roboto', font_size, 'bold'), wraplength=280)
        message_label.pack(padx=10, pady=10)

        if buttons:
            button_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
            button_frame.pack(pady=5)
            for text, value in buttons:
                btn = tk.Button(button_frame, text=text, command=lambda v=value: self.set_choice_and_close(v),
                                bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR, font=('Roboto', 10, 'bold'), relief='flat')
                btn.pack(side=tk.LEFT, padx=5)

        title_bar.bind('<ButtonPress-1>', self.start_move)
        title_bar.bind('<ButtonRelease-1>', self.stop_move)
        title_bar.bind('<B1-Motion>', self.do_move)
        self._x = None
        self._y = None

        self.root.update_idletasks()
        req_height = self.root.winfo_reqheight()
        self.root.geometry(f"300x{req_height}")

        
        if self.app:
            self.app.add_resize_handle(self.root)

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.set_choice_and_close("no"))

    def set_choice_and_close(self, value):
        self.choice = value
        self.root.destroy()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f'+{x}+{y}')

    def stop_move(self, event):
        self.x = None
        self.y = None
        self.moving_window = None
            
class Logger:
    def __init__(self, app):
        self.app = app
        self.log_file = os.path.join(self.app.sniker_lite_path, "sniker_logs.txt")
        self.logs_text = None
        self.filter_var = tk.StringVar(value="all")

    def log(self, bot_name, message, level="info"):
        timestamp = datetime.now().strftime("[%Y-%m-d %H:%M:%S] ")
        full_message = f"{timestamp}[{bot_name}] {message}\n"
        
        if self.logs_text and self.logs_text.winfo_exists():
            try:
                self.logs_text.configure(state='normal')
                if self.filter_var.get() == "all" or self.filter_var.get() == level:
                    self.logs_text.insert(tk.END, full_message, level)
                self.logs_text.configure(state='disabled')
                self.logs_text.see(tk.END)
            except tk.TclError:
                pass  
        
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > 1 * 1024 * 1024:
            os.rename(self.log_file, f"{self.log_file}_{datetime.now().strftime('%Y%d_%H%M%S')}.txt")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(full_message)
            
class MultiBotApp:
    def __init__(self):
        self.root = ThemedTk(theme="default")
        self.root.overrideredirect(True)
        self.root.geometry("610x300+100+100")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.0)
        self.exiting = False
        self.server_sock = None
        self.error_windows = {}
        self.control_texts = {}
        self.bot_frames = {} 
        self.drag_threshold = 5
        self.last_toggle_time = 0
        self.scale_factor = 1.0
        self.assigning_key = None
        self.eat_keycode = None
        self.is_changing_bind = False
        self.settings_open = False
        self.eat_keycode = None
        self.expander_keycode = None
        self.food_cooldown_var = tk.DoubleVar(value=30)

        
        self.food_cooldown_var = tk.IntVar()
        self.auto_reconnect_var = tk.BooleanVar()
        self.auto_run_var = tk.BooleanVar()
        self.port_price_var = tk.StringVar()
        self.mine_price_var = tk.StringVar()
        self.building_price_var = tk.StringVar()
        self.anti_afk_var = tk.BooleanVar()
        self.lottery_var = tk.BooleanVar()
        self.roulette_var = tk.BooleanVar()
        self.telegram_token_var = tk.StringVar()
        self.take_out_bind_type_var = tk.StringVar(value="key")
        self.take_out_bind_value_var = tk.StringVar()
        self.put_away_bind_type_var = tk.StringVar(value="key")
        self.put_away_bind_value_var = tk.StringVar()
        self.animation_bind_value_var = tk.StringVar()
        self.animation_bind_type_var = tk.StringVar(value="key")
        self.hide_show_key_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.eat_key_var = tk.StringVar()
        self.expander_key_var = tk.StringVar()

        self.image_names = ['buyticket', 'gymSpace', 'ring', 'ekach', 'cursor', 'payday15', 'payday20', 'payday25', 'payday30', 'connection', 'ipserv', 'connect', 'done', 'dont', 'connect2', 'passw', 'voit', 'acep', 'E', 'F', 'H', 'jail', 'bankkard', 'toka', 'aneth', 'emshelp', 'lottery', 'spinbutton', 'cols', 'last', 'lastacc', 'cas', 'mony', 'payday', 'finish', 'fire', 'frukti', 'fruktisalat', 'knife', 'myaso', 'ovoshi', 'startCoocking', 'voda', 'whisk', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'] + ['d{}'.format(i) for i in range(1, 21)]

        appdata_path = os.getenv('APPDATA')
        if appdata_path:
            self.sniker_lite_path = os.path.join(appdata_path, "Sniker Lite")
            os.makedirs(self.sniker_lite_path, exist_ok=True)
        else:
            self.show_error("Ошибка", "Не удалось получить путь к AppData")
            sys.exit(1)

        self.thresholds = {'cols': 0.7, 'connection': 0.7, 'finish': 0.7, 'voit': 0.7}
        self.app = self
        self.logger = Logger(self)
        self.templates = self.load_templates()
        self.moving_window = None

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 535
        window_height = 475
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.current_geometry = f"{window_width}x{window_height}+{x}+{y}"

        jail_img = Image.open(get_resource_path('images/jail.jpg')).resize((16, 16), Image.LANCZOS)
        self.jail_icon = ImageTk.PhotoImage(jail_img)

        default_geometry = "535x475+106+62"

        self.config = ConfigParser()
        self.load_config()

        
        if "General" not in self.config:
            self.config.add_section("General")
        if "ResetStatsKey" not in self.config["General"]:
            self.config["General"]["ResetStatsKey"] = "F9"

        if "Windows" not in self.config:
            self.config["Windows"] = {}
        if "MainWindowGeometry" in self.config["Windows"]:
            geometry = self.config["Windows"]["MainWindowGeometry"]
            try:
                width_height, position = geometry.split('+', 1)
                width, height = map(int, width_height.split('x'))
                if width < 100 or height < 100:
                    self.root.geometry(default_geometry)
                    self.current_geometry = default_geometry
                else:
                    self.root.geometry(geometry)
                    self.current_geometry = geometry
            except ValueError:
                self.root.geometry(default_geometry)
                self.current_geometry = default_geometry
        else:
            self.root.geometry(default_geometry)
            self.current_geometry = default_geometry

        self.save_timer = None
        self.root.bind('<Configure>', self.save_main_window_geometry)

        selected_theme = self.config["General"].get("SelectedTheme", "dark")
        if selected_theme not in THEMES:
            selected_theme = "dark"
            self.config["General"]["SelectedTheme"] = "dark"
            self.logger.log("Theme", f"Invalid theme '{selected_theme}' detected, switching to 'dark'", "warning")
        set_theme(selected_theme)
        
        self.root.configure(bg=BACKGROUND_COLOR)

        self.game_left = 0
        self.game_top = 0
        self.game_width = int(self.config["General"].get("GameResolution", "1920x1080").split('x')[0])
        self.game_height = int(self.config["General"].get("GameResolution", "1920x1080").split('x')[1])
        self.scale_x = self.game_width / 1920.0
        self.scale_y = self.game_height / 1080.0
        self.current_setup_window = None

        
        self.auto_reconnect_var.set(self.config["AntiAfk"].getboolean("AutoReconnect", False))
        self.auto_run_var.set(self.config["General"].getboolean("AutoRun", False))
        self.port_price_var.set(self.config["Port"].get("BoxReward", ""))
        self.mine_price_var.set(self.config["Mine"].get("ActionReward", ""))
        self.building_price_var.set(self.config["Building"].get("ActionReward", ""))
        self.anti_afk_var.set(self.config["AntiAfk"].getboolean("AntiAfkEnabled", False))
        self.lottery_var.set(self.config["AntiAfk"].getboolean("LotteryEnabled", False))
        self.roulette_var.set(self.config["AntiAfk"].getboolean("RouletteEnabled", False))
        self.telegram_token_var.set(self.config["AntiAfk"].get("TelegramToken", ""))
        self.take_out_bind_value_var.set(self.config["AntiAfk"].get("TakeOutPhoneKey", "up"))
        self.put_away_bind_value_var.set(self.config["AntiAfk"].get("PutAwayPhoneKey", "backspace"))
        self.animation_bind_value_var.set(self.config["AntiAfk"].get("AnimationKey", "k"))
        self.hide_show_key_var.set(self.config["Hotkeys"].get("HideShowKey", "F12"))
        self.password_var.set(self.config["AntiAfk"].get("Password", ""))
        self.eat_key_var.set(self.config["Gym"].get("EatKey", ""))
        self.expander_key_var.set(self.config["Gym"].get("ExpanderKey", ""))

        self.hide_show_keycode = self.config["Hotkeys"].getint("HideShowKeyCode", 123)
        self.take_out_keycode = self.config["AntiAfk"].getint("TakeOutPhoneKeyCode", 38)
        self.put_away_keycode = self.config["AntiAfk"].getint("PutAwayPhoneKeyCode", 8)
        self.animation_keycode = self.config["AntiAfk"].getint("AnimationKeyCode", 75)
        
        try:
            self.expander_keycode = self.config["Gym"].getint("ExpanderKeyCode")
        except (ValueError, configparser.NoOptionError):
            self.expander_keycode = None
            self.logger.log("Config", "ExpanderKeyCode не задан или неверный, использую None", "warning")
        
        try:
            self.eat_keycode = self.config["Gym"].getint("EatKeyCode")
        except (ValueError, configparser.NoOptionError):
            self.eat_keycode = None  
            self.logger.log("Config", "EatKeyCode не задан или неверный, использую None", "warning")

        initial_keysym = "F12"
        self.hide_show_key_var.set(self.get_display_key(self.hide_show_keycode, initial_keysym))

        self.current_entry = None

        self.logger = Logger(self)

        logs_img = Image.open(get_resource_path('images/logs.jpg')).resize((16, 16), Image.LANCZOS)
        self.logs_icon = ImageTk.PhotoImage(logs_img)
        settings_img = Image.open(get_resource_path('images/setting.jpg')).resize((16, 16), Image.LANCZOS)
        self.settings_icon = ImageTk.PhotoImage(settings_img)
        home_img = Image.open(get_resource_path('images/home.jpg')).resize((16, 16), Image.LANCZOS)
        self.home_icon = ImageTk.PhotoImage(home_img)
        work_img = Image.open(get_resource_path('images/work.jpg')).resize((16, 16), Image.LANCZOS)
        self.work_icon = ImageTk.PhotoImage(work_img)
        access_img = Image.open(get_resource_path('images/access.jpg')).resize((16, 16), Image.LANCZOS)
        self.access_icon = ImageTk.PhotoImage(access_img)
        web_img = Image.open(get_resource_path('images/web.jpg')).resize((16, 16), Image.LANCZOS)
        self.web_icon = ImageTk.PhotoImage(web_img)
        clear_img = Image.open(get_resource_path('images/clear.jpg')).resize((16, 16), Image.LANCZOS)
        self.clear_icon = ImageTk.PhotoImage(clear_img)
        show_img = Image.open(get_resource_path('images/show.png')).resize((16, 16), Image.LANCZOS)
        self.show_icon = ImageTk.PhotoImage(show_img)
        hide_img = Image.open(get_resource_path('images/hide.png')).resize((16, 16), Image.LANCZOS)
        self.hide_icon = ImageTk.PhotoImage(hide_img)
        self.templates = self.load_templates()
        self.thresholds = {'cols': 0.7, 'connection': 0.7, 'finish': 0.7, 'voit': 0.7}  

        self.setup_styles()
        self.setup_gui()
        self.bots = {
            'port': PortBot(self),
            'mine': MineBot(self),
            'building': BuildingBot(self),
            'antiafk': AntiAfkBot(self),
            'ems': EMSChecker(self),
            'demorgan': DemorganBot(self),
            'farm': FarmBot(self),
            'dmtokar': DMTokarBot(self),
            'cooking': CookingBot(self),
            'gym': GymBot(self)
        }

        
        self.hotkeys = {
            'hide_show': {'key': self.hide_show_key_var.get(), 'keycode': self.hide_show_keycode, 'action': self.toggle_visibility},
            'eat': {'key': self.eat_key_var.get(), 'keycode': self.eat_keycode, 'action': lambda: self.bots['gym'].press_key(self.eat_keycode) if self.bots.get('gym') else None}
        }
        
        self.setup_hotkeys()
        self.bot_name_mapping = {
            'порт': 'port',
            'шахта': 'mine',
            'стройка': 'building',
            'antiafk': 'antiafk',
            'ems': 'ems',
            'швейка': 'demorgan',
            'ферма': 'farm',
            'токарь': 'dmtokar',
            'готовка': 'cooking',
            'качалка': 'gym'
        }

        self.tab_to_bot = {
            "Порт": "port",
            "Шахта": "mine",
            "Стройка": "building",
            "Ферма": "farm",
            "Анти-AFK": "antiafk",
            "EMS": "ems",
            "Швейка": "demorgan",
            "Токарь": "dmtokar",
            "Готовка": "cooking",
            "Качалка": "gym"
        }

        for bot_name in self.bots:
            if not self.config.has_section(bot_name):
                self.config.add_section(bot_name)
            if "ToggleKey" not in self.config[bot_name]:
                self.config[bot_name]["ToggleKey"] = "f5"
        self.bot_toggle_keys = {bot_name: self.config[bot_name].get("ToggleKey", "f5") for bot_name in self.bots}
        self.reset_stats_key = self.config["General"].get("ResetStatsKey", "F9")

        self.is_hidden = False  
        self.f12_pressed = False  
        self.setup_hotkeys()
        self._x = None
        self._y = None
        self.is_minimized = False
        self.logs_window = None
        self.is_hidden = False
        self.current_tab = None
        self.add_resize_handle(self.root)
        self.fade_in()

        self.moving = False  

        self.moving_window = None  
        self.resize_margin = 5      
        self.resize_direction = None
        self.resizing = False

        
        self.root.bind('<Motion>', lambda event: self.on_motion(event, self.root))
        self.root.bind('<ButtonPress-1>', lambda event: self.start_action(event, self.root))
        self.root.bind('<B1-Motion>', lambda event: self.do_action(event, self.root))
        self.root.bind('<ButtonRelease-1>', lambda event: self.stop_action(event, self.root))

        self.title_bar.bind('<ButtonPress-1>', lambda event: self.start_move(event, self.root))
        self.title_bar.bind('<B1-Motion>', lambda event: self.do_move(event, self.root))
        self.title_bar.bind('<ButtonRelease-1>', lambda event: self.stop_move(event, self.root))

        self.resize_margin = 5  
        self.resize_direction = None  
        self.resizing = False  

        
        self.title_bar.bind('<Motion>', lambda e: None)
        self.root.config(cursor="arrow")
        self.title_bar.config(cursor="arrow")
        
    def get_scaled_font_size(self, size):
         return int(size * self.scale_factor)

    def get_keycode(self, key_str):
        if key_str.isdigit():
            return int(key_str)
        else:
            return key_str.lower()

    def start_move_window(self, event, window):
        self._x = event.x
        self._y = event.y
        self.moving_window = window

    def do_move_window(self, event):
        if self.moving_window:
            deltax = event.x - self._x
            deltay = event.y - self._y
            x = self.moving_window.winfo_x() + deltax
            y = self.moving_window.winfo_y() + deltay
            self.moving_window.geometry(f'+{x}+{y}')

    def stop_move_window(self, event):
        self.moving_window = None

    def start_socket_server(self):
        """Запускает сервер сокетов для прослушивания команд от других экземпляров."""
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(("127.0.0.1", 12345))
        self.server_sock.listen(1)
        threading.Thread(target=self.socket_listener, daemon=True).start()

    def socket_listener(self):
        """Слушает входящие команды через сокет и обрабатывает их."""
        while True:
            conn, addr = self.server_sock.accept()
            data = conn.recv(1024).decode()
            if data == "shutdown":
                conn.send(b"ok")
                conn.close()
                self.root.after(0, self.shutdown)
                break
            conn.close()

    def shutdown(self):
        self.exiting = True
        if self.server_sock:
            self.server_sock.close()
        self.root.after(0, self.root.destroy)  

    def on_press(self, key):
        try:
            key_name = key.name if hasattr(key, 'name') else key.char
            key_name = key_name.lower() if key_name else None
            for hotkey in self.hotkeys.values():
                if key_name == hotkey['key'].lower():
                    hotkey['action']()
        except AttributeError:
            pass
    
    def on_motion(self, event, window):
        if event.widget != window:
            return  
        x = event.x
        y = event.y
        w = window.winfo_width()
        h = window.winfo_height()
        margin = self.resize_margin  

        
        if x < margin and y < margin:
            window.config(cursor='size_nw_se')
            self.resize_direction = 'nw'
        elif x > w - margin and y < margin:
            window.config(cursor='size_ne_sw')
            self.resize_direction = 'ne'
        elif x < margin and y > h - margin:
            window.config(cursor='size_ne_sw')
            self.resize_direction = 'sw'
        elif x > w - margin and y > h - margin:
            window.config(cursor='size_nw_se')
            self.resize_direction = 'se'
        elif x < margin:
            window.config(cursor='size_we')
            self.resize_direction = 'w'
        elif x > w - margin:
            window.config(cursor='size_we')
            self.resize_direction = 'e'
        elif y < margin:
            window.config(cursor='size_ns')
            self.resize_direction = 'n'
        elif y > h - margin:
            window.config(cursor='size_ns')
            self.resize_direction = 's'
        else:
            window.config(cursor='arrow')  
            self.resize_direction = None

    def start_resize(self, event, window):
        if self.resize_direction:
            self.resizing = True
            self.start_x = event.x_root
            self.start_y = event.y_root
            self.start_width = window.winfo_width()
            self.start_height = window.winfo_height()
            self.start_root_x = window.winfo_x()
            self.start_root_y = window.winfo_y()

    def do_resize(self, event, window):
        if self.resizing:
            deltax = event.x_root - self.start_x
            deltay = event.y_root - self.start_y
            new_width = self.start_width
            new_height = self.start_height
            new_x = self.start_root_x
            new_y = self.start_root_y
            if 'w' in self.resize_direction:
                new_width -= deltax
                new_x += deltax
            if 'e' in self.resize_direction:
                new_width += deltax
            if 'n' in self.resize_direction:
                new_height -= deltay
                new_y += deltay
            if 's' in self.resize_direction:
                new_height += deltay
            new_width = max(new_width, 100)  
            new_height = max(new_height, 100)  
            window.geometry(f'{new_width}x{new_height}+{new_x}+{new_y}')

    def stop_resize(self, event, window):
        self.resizing = False

    def start_action(self, event, window):
        if event.widget != window:
            return
        if self.resize_direction:
            self.resizing = True
            self.start_x = event.x_root
            self.start_y = event.y_root
            self.start_width = window.winfo_width()
            self.start_height = window.winfo_height()
            self.start_root_x = window.winfo_x()
            self.start_root_y = window.winfo_y()

    def do_action(self, event, window):
        if self.resizing:
            self.do_resize(event, window)

    def stop_action(self, event, window):
        self.resizing = False

    def add_resize_handle(self, window):
        window.bind('<Motion>', lambda event: self.on_motion(event, window))
        window.bind('<ButtonPress-1>', lambda event: self.start_action(event, window))
        window.bind('<B1-Motion>', lambda event: self.do_action(event, window))
        window.bind('<ButtonRelease-1>', lambda event: self.stop_action(event, window))

    def save_main_window_geometry(self, event):
        if self.root.winfo_ismapped() and not self.exiting:
            geometry = self.root.geometry()
            width_height, position = geometry.split('+', 1)
            width, height = map(int, width_height.split('x'))
            if width > 100 and height > 100:
                self.current_geometry = geometry
                if self.save_timer is not None:
                    try:
                        self.root.after_cancel(self.save_timer)
                    except ValueError:
                        pass
                self.save_timer = self.root.after(1000, self.do_save_main_geometry)

    def do_save_main_geometry(self):
        geometry = self.root.geometry()
        self.config["Windows"]["MainWindowGeometry"] = geometry
        with open(os.path.join(self.sniker_lite_path, "sniker_settings.ini"), "w", encoding='utf-8') as f:
            self.config.write(f)

    def create_toplevel(self, title, width=300, height=200):
        window = tk.Toplevel(self.root)
        window.overrideredirect(True)
        window.attributes("-topmost", True)
        window.configure(bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, cursor="arrow")
        
        title_bar = tk.Frame(window, bg=BUTTON_COLOR, relief='flat', bd=0, cursor="arrow")
        title_bar.pack(fill=tk.X)
        
        title_label = tk.Label(title_bar, text=title, bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                            font=('Roboto', 10, 'bold'), bd=0)
        title_label.pack(side=tk.LEFT, padx=5)
        
        close_button = tk.Button(title_bar, text="X", command=lambda: self.safe_destroy(window), bg=BUTTON_COLOR,
                                fg=HEADER_TEXT_COLOR, font=('Roboto', 10, 'bold'),
                                relief='flat', bd=0, activebackground=ACTIVE_BUTTON_COLOR,
                                activeforeground=HEADER_TEXT_COLOR)
        close_button.pack(side=tk.RIGHT, padx=2)
        
        content_frame = tk.Frame(window, bg=FRAME_BG_COLOR, bd=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        title_bar.bind('<ButtonPress-1>', lambda event: self.start_move(event, window))
        title_bar.bind('<B1-Motion>', lambda event: self.do_move(event, window))
        title_bar.bind('<ButtonRelease-1>', lambda event: self.stop_move(event, window))

        if "Windows" in self.config and f"{title}Geometry" in self.config["Windows"]:
            window.geometry(self.config["Windows"][f"{title}Geometry"])
        else:
            window.geometry(f"{width}x{height}+100+100")
        
        window.bind('<Configure>', lambda e: self.save_window_geometry(e, title))
        self.add_resize_handle(window)
        
        return window, content_frame

    def toggle_visibility(self):
        if self.is_hidden:
            self.root.attributes("-alpha", 1.0)  
            self.is_hidden = False
        else:
            self.root.attributes("-alpha", 0.0)  
            self.is_hidden = True

    def save_window_geometry(self, event, window_name):
        if event.widget.winfo_toplevel() == event.widget and not self.exiting:
            if hasattr(self, 'save_timer'):
                event.widget.after_cancel(self.save_timer)
            self.save_timer = event.widget.after(1000, lambda: self.do_save_geometry(event.widget, window_name))

    def do_save_geometry(self, window, window_name):
        if window.winfo_exists():
            geometry = window.geometry()
            
            safe_name = {
                "Настройки": "Settings",
                "Логи": "Logs"
                
            }.get(window_name, window_name)  
            self.config["Windows"][f"{safe_name}Geometry"] = geometry
            with open(os.path.join(self.sniker_lite_path, "sniker_settings.ini"), 'w', encoding='utf-8') as f:
                self.config.write(f)
                
    def fade_in(self):
        alpha = 0.0
        while alpha < 0.95:
            alpha += 0.05
            self.root.attributes("-alpha", alpha)
            self.root.update()
            time.sleep(0.02)

    def get_display_key(self, keycode, keysym):
        if 65 <= keycode <= 90:
            return chr(keycode).lower()
        elif 48 <= keycode <= 57:
            return chr(keycode)
        else:
            return keysym

    def start_move(self, event, window):
        self.x = event.x
        self.y = event.y
        self.moving_window = window
    
    def stop_move(self, event, window):
        self.x = None
        self.y = None
        self.moving_window = None
    
    def fade_out(self, callback):
        alpha = 0.95  
        while alpha > 0.0:
            alpha -= 0.05
            try:
                if not self.root.winfo_exists():  
                    break
                self.root.attributes("-alpha", alpha)
                self.root.update()
                time.sleep(0.02)
            except tk.TclError:
                break  
        
        try:
            if self.root.winfo_exists() and callable(callback):
                callback()
        except tk.TclError:
            pass  

    def on_setup_window_close(self, window):
        if self.current_setup_window == window:
            self.current_setup_window = None
        window.destroy()

    def on_error_window_close(self, error_key):
        if error_key in self.error_windows:
            del self.error_windows[error_key]

    def get_scaled_font_size(self, base_size):
        return int(base_size * min(self.scale_x, self.scale_y))

    def setup_styles(self):
        font_size = self.get_scaled_font_size(10)
        header_font_size = self.get_scaled_font_size(12)
        style = ttk.Style()
        theme_prefix = "Dark" if current_theme == "dark" else "Light"
        
        style.configure('TFrame', background=FRAME_BG_COLOR, borderwidth=0, relief='flat',
                        highlightcolor=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
        style.configure('TLabel', background=LABEL_BG_COLOR, foreground=LABEL_FG_COLOR,
                        font=('Roboto', font_size, 'bold'), borderwidth=0, relief='flat',
                        highlightcolor=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
        style.configure('TButton', background=BUTTON_COLOR, foreground=HEADER_TEXT_COLOR,
                        font=('Roboto', font_size, 'bold'), padding=4, relief='flat', borderwidth=0,
                        highlightcolor=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
        style.map('TButton', foreground=[('active', HEADER_TEXT_COLOR)],
                background=[('active', ACTIVE_BUTTON_COLOR)],
                bordercolor=[('active', BACKGROUND_COLOR)])
        
        style.configure('TNotebook', background=BACKGROUND_COLOR, borderwidth=-1, tabmargins=-1.5, padding=0,
                        bordercolor=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR,
                        highlightbackground=BACKGROUND_COLOR)
        style.configure('TNotebook.Tab', background=TAB_BG_COLOR, foreground=TAB_FG_COLOR,
                        padding=[7, 7], font=('Roboto', font_size, 'bold'), borderwidth=0,
                        bordercolor=BACKGROUND_COLOR, darkcolor=BACKGROUND_COLOR,
                        lightcolor=BACKGROUND_COLOR, focuscolor=BACKGROUND_COLOR,
                        highlightcolor=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
        style.map('TNotebook.Tab', background=[('selected', TAB_SELECTED_BG_COLOR)],
                foreground=[('selected', TAB_SELECTED_FG_COLOR)],
                bordercolor=[('selected', BACKGROUND_COLOR)],
                highlightcolor=[('selected', BACKGROUND_COLOR)])
        
        style.configure('Horizontal.TScale', background=FRAME_BG_COLOR, troughcolor='#444444' if current_theme == 'dark' else '#aaaaaa',
                        sliderrelief='raised', sliderlength=20, borderwidth=0)
        style.map('Horizontal.TScale', background=[('active', ACTIVE_BUTTON_COLOR)],
                troughcolor=[('active', '#555555' if current_theme == 'dark' else '#999999')])

        style.configure('Antiafk.Horizontal.TScale', parent='Horizontal.TScale', background=FRAME_BG_COLOR, 
                        troughcolor='#444444' if current_theme == 'dark' else '#aaaaaa',
                        sliderrelief='raised', sliderlength=20, borderwidth=0)
        style.map('Antiafk.Horizontal.TScale', background=[('active', ACTIVE_BUTTON_COLOR)],
                troughcolor=[('active', '#555555' if current_theme == 'dark' else '#999999')])

        style.configure('Antiafk.TEntry', fieldbackground=ENTRY_BG_COLOR, foreground=TEXT_FG_COLOR,
                        font=('Roboto', font_size), borderwidth=0, relief='flat',
                        highlightcolor=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
        style.map('Antiafk.TEntry',
          fieldbackground=[('readonly', ENTRY_BG_COLOR)],
          foreground=[('readonly', TEXT_FG_COLOR)],
          background=[('readonly', ENTRY_BG_COLOR)])
        style.configure('Antiafk.TLabel', background=LABEL_BG_COLOR, foreground=LABEL_FG_COLOR,
                        font=('Roboto', font_size, 'bold'), borderwidth=0, relief='flat',
                        highlightcolor=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
        style.configure('Antiafk.TCheckbutton', background=BACKGROUND_COLOR, foreground=TEXT_COLOR,
                        font=('Roboto', font_size), borderwidth=0, relief='flat',
                        highlightcolor=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
        style.map('Antiafk.TCheckbutton',
                background=[('active', BUTTON_COLOR)],
                foreground=[('active', HEADER_TEXT_COLOR)])
        style.configure('Vertical.TScrollbar', background=SCROLLBAR_COLOR, troughcolor=SCROLLBAR_TROUGH_COLOR,
                        arrowcolor=TEXT_COLOR, borderwidth=0, relief='flat',
                        highlightcolor=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
        style.configure('Antiafk.TCombobox', fieldbackground=ENTRY_BG_COLOR, background=ENTRY_BG_COLOR,
                        foreground=TEXT_FG_COLOR, font=('Roboto', font_size, 'bold'), borderwidth=0, relief='flat',
                        selectbackground=BUTTON_COLOR, selectforeground=HEADER_TEXT_COLOR)
        style.map('Antiafk.TCombobox', fieldbackground=[('readonly', ENTRY_BG_COLOR)],
                background=[('readonly', ENTRY_BG_COLOR)],
                foreground=[('readonly', TEXT_FG_COLOR)],
                selectbackground=[('readonly', BUTTON_COLOR)],
                selectforeground=[('readonly', HEADER_TEXT_COLOR)])
        
        self.root.option_add('*TCombobox*Listbox.background', ENTRY_BG_COLOR)
        self.root.option_add('*TCombobox*Listbox.foreground', TEXT_FG_COLOR)
        self.root.option_add('*TCombobox*Listbox.selectBackground', BUTTON_COLOR)
        self.root.option_add('*TCombobox*Listbox.selectForeground', HEADER_TEXT_COLOR)
        self.root.option_add('*TCombobox*Listbox.font', ('Roboto', font_size, 'bold'))
        style.configure('Custom.Vertical.TScrollbar',
                        background=SCROLLBAR_COLOR, troughcolor=SCROLLBAR_TROUGH_COLOR,
                        arrowcolor=TEXT_COLOR, borderwidth=0, gripcount=0, width=12, relief='flat')
        style.map('Custom.Vertical.TScrollbar', background=[('active', BUTTON_COLOR)])
        style.layout('TNotebook', [('Notebook.client', {'sticky': 'nswe'})])
        style.layout('TNotebook.Tab', [('Notebook.tab', {'sticky': 'nswe', 'children':
                                                        [('Notebook.padding', {'sticky': 'nswe',
                                                                            'children':
                                                                            [('Notebook.label', {'sticky': 'nswe'})]
                                                                            })]
                                                        })])
        
        style.configure('Horizontal.TSeparator', background=SEPARATOR_COLOR)
        style.configure('Header.TLabel', font=('Roboto', header_font_size, 'bold'), anchor='center',
                        background=LABEL_BG_COLOR, foreground=LABEL_FG_COLOR)
        style.configure('Antiafk.TFrame', background=FRAME_BG_COLOR)

    
    def apply_theme(self):
        self.root.configure(bg=BACKGROUND_COLOR)
        self.title_bar.configure(bg=BUTTON_COLOR)
        for child in self.title_bar.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR)
            elif isinstance(child, tk.Button):
                child.configure(bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR, activebackground=ACTIVE_BUTTON_COLOR,
                                activeforeground=HEADER_TEXT_COLOR)
        
        if hasattr(self, 'home_frame'):
            self.home_frame.configure(bg=FRAME_BG_COLOR)
            for widget in self.home_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR)
        
        def update_widget_colors(widget):
            if isinstance(widget, tk.Frame):
                widget.configure(bg=FRAME_BG_COLOR)
            elif isinstance(widget, tk.Label):
                widget.configure(bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR)
            elif isinstance(widget, tk.Text):
                widget.configure(bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR)
            elif isinstance(widget, tk.Button):
                widget.configure(bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR, activebackground=ACTIVE_BUTTON_COLOR)
            elif isinstance(widget, ttk.Entry):
                widget.configure(style='Antiafk.TEntry')  
            for child in widget.winfo_children():
                update_widget_colors(child)
        
        for bot_frame in self.bot_frames.values():
            update_widget_colors(bot_frame)
        
        self.setup_styles()
        
        if self.logs_window and self.logs_window.winfo_exists():
            self.logs_window.configure(bg=BACKGROUND_COLOR)
            logs_title_bar = self.logs_window.winfo_children()[0]
            logs_title_bar.configure(bg=BUTTON_COLOR)
            for child in logs_title_bar.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR)
                elif isinstance(child, tk.Button):
                    child.configure(bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR, activebackground=ACTIVE_BUTTON_COLOR,
                                    activeforeground=HEADER_TEXT_COLOR)
            filter_frame = self.logs_window.winfo_children()[1]
            filter_frame.configure(bg=FRAME_BG_COLOR)
            for child in filter_frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR)
                elif isinstance(child, tk.Radiobutton):
                    child.configure(bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR, selectcolor=TAB_SELECTED_BG_COLOR,
                                    activebackground=ACTIVE_BUTTON_COLOR, activeforeground=TEXT_FG_COLOR)
            self.logger.logs_text.configure(bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR)
        
        self.root.option_add('*TCombobox*Listbox.background', ENTRY_BG_COLOR)
        self.root.option_add('*TCombobox*Listbox.foreground', TEXT_FG_COLOR)
        self.root.option_add('*TCombobox*Listbox.selectBackground', BUTTON_COLOR)
        self.root.option_add('*TCombobox*Listbox.selectForeground', HEADER_TEXT_COLOR)

    def load_config(self):
        config_path = os.path.join(self.sniker_lite_path, "sniker_settings.ini")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config.read_file(f)
        except FileNotFoundError:
            pass
        except UnicodeDecodeError as e:
            self.logger.log("Config", f"Ошибка декодирования файла конфигурации: {e}", "error")

        if "General" not in self.config:
            self.config["General"] = {}
        if "GameResolution" not in self.config["General"]:
            self.config["General"]["GameResolution"] = "1920x1080"
        if "AutoRun" not in self.config["General"]:
            self.config["General"]["AutoRun"] = "True"
        if "SelectedTheme" not in self.config["General"]:
            self.config["General"]["SelectedTheme"] = "dark"
        if "AutoSaveOnExit" not in self.config["General"]:
            self.config["General"]["AutoSaveOnExit"] = "True"

        if "Port" not in self.config:
            self.config["Port"] = {}
        if "BoxReward" not in self.config["Port"]:
            self.config["Port"]["BoxReward"] = "132"
        if "CheckX" not in self.config["Port"]:
            self.config["Port"]["CheckX"] = "950.0"
        if "CheckY" not in self.config["Port"]:
            self.config["Port"]["CheckY"] = "480.0"

        if "Mine" not in self.config:
            self.config["Mine"] = {}
        if "ActionReward" not in self.config["Mine"]:
            self.config["Mine"]["ActionReward"] = "132"

        if "Building" not in self.config:
            self.config["Building"] = {}
        if "ActionReward" not in self.config["Building"]:
            self.config["Building"]["ActionReward"] = "132"

        if "AntiAfk" not in self.config:
            self.config["AntiAfk"] = {}
        if "AutoReconnect" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["AutoReconnect"] = "False"
        if "LotteryEnabled" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["LotteryEnabled"] = "True"
        if "RouletteEnabled" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["RouletteEnabled"] = "True"
        if "TelegramToken" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["TelegramToken"] = ""
        if "AnimationKey" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["AnimationKey"] = "k"
        if "TakeOutPhoneKey" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["TakeOutPhoneKey"] = "Up"
        if "PutAwayPhoneKey" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["PutAwayPhoneKey"] = "backspace"
        if "ChatFontSize" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["ChatFontSize"] = "15"
        if "LotteryConfigured" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["LotteryConfigured"] = "False"
        if "RouletteConfigured" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["RouletteConfigured"] = "False"
        if "AntiAfk" not in self.config:
            self.config["AntiAfk"] = {}
        if "AutoReconnect" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["AutoReconnect"] = "False"
        if "Password" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["Password"] = ""
        if "Character" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["Character"] = "1"

        if "EMS" not in self.config:
            self.config["EMS"] = {}

        if "Hotkeys" not in self.config:
            self.config["Hotkeys"] = {}
        if "HideShowKey" not in self.config["Hotkeys"]:
            self.config["Hotkeys"]["HideShowKey"] = "F12"

        if "Shveika" not in self.config:
            self.config["Shveika"] = {}
        if "KeyDelay" not in self.config["Shveika"]:
            self.config["Shveika"]["KeyDelay"] = "0.5"

        if "Hotkeys" not in self.config:
            self.config["Hotkeys"] = {}
        if "HideShowKeyCode" not in self.config["Hotkeys"]:
            self.config["Hotkeys"]["HideShowKeyCode"] = "123"
        if "TakeOutPhoneKeyCode" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["TakeOutPhoneKeyCode"] = "38"
        if "PutAwayPhoneKeyCode" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["PutAwayPhoneKeyCode"] = "8"
        if "AnimationKeyCode" not in self.config["AntiAfk"]:
            self.config["AntiAfk"]["AnimationKeyCode"] = "75"
        if "Gym" not in self.config:
            self.config["Gym"] = {}
        if "EatKey" not in self.config["Gym"]:
            self.config["Gym"]["EatKey"] = "j"  
        if "ExpanderKey" not in self.config["Gym"]:
            self.config["Gym"]["ExpanderKey"] = "h"  
        if "EatKeyCode" not in self.config["Gym"]:
            self.config["Gym"]["EatKeyCode"] = str(ord('j'))  
        if "ExpanderKeyCode" not in self.config["Gym"]:
            self.config["Gym"]["ExpanderKeyCode"] = str(ord('h'))

        bot_sections = ['Port', 'Mine', 'Building', 'AntiAfk', 'EMS', 'Shveika', 'Farm', 'DMTokar', 'Cooking', 'Gym']

        for bot_name in bot_sections:
            if bot_name not in self.config:
                self.config[bot_name] = {}
            if "ToggleKey" not in self.config[bot_name]:
                self.config[bot_name]["ToggleKey"] = "f5"

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config.read_file(f)
            
        sections = {
            "General": {
                "AutoRun": ("bool", "true"),
                "AutoSaveOnExit": ("bool", "true"),
            },
            "Port": {
                "BoxReward": ("int", "132"),
                "CheckX": ("float", "950.0"),
                "CheckY": ("float", "480.0"),
            },
            "Mine": {
                "ActionReward": ("int", "132"),
            },
            "Building": {
                "ActionReward": ("int", "132"),
            },
            "AntiAfk": {
                "AutoReconnect": ("bool", "false"),
                "LotteryEnabled": ("bool", "true"),
                "RouletteEnabled": ("bool", "true"),
                "ChatFontSize": ("int", "15"),
                "LotteryConfigured": ("bool", "false"),
                "RouletteConfigured": ("bool", "false"),
            },
            "Gym": {
                "FoodCooldown": ("int", "30"),
            },
            "Hotkeys": {
                "HideShowKeyCode": ("int", "123"),
            },
        }
        
        for section, options in sections.items():
            if section not in self.config:
                self.config[section] = {}
            for option, (typ, default) in options.items():
                if option in self.config[section]:
                    value = self.config[section][option]
                    try:
                        if typ == "bool":
                            self.config[section].getboolean(option)
                        elif typ == "int":
                            int(value)
                        elif typ == "float":
                            float(value)
                    except ValueError:
                        original = value
                        self.config[section][option] = default
                        self.logger.log("Config", f"Недопустимое значение {option} '{original}' в секции {section}, установлено значение по умолчанию {default}")

        
        config_path = os.path.join(self.sniker_lite_path, "sniker_settings.ini")
        try:
            with open(config_path, "w", encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            self.logger.log("Config", f"Ошибка при сохранении конфигурации: {e}", "error")

    def load_templates(self):
        templates = {}
        grayscale_images = ['cols', 'connection', 'finish', 'voit']
        for img in self.image_names:
            path = get_resource_path(f'images/{img}.jpg')
            if not os.path.exists(path):
                self.app.logger.log("AntiAfk", f"Файл не найден: {path}", "error")
                continue
            try:
                if img == 'cas':
                    
                    template = cv2.imread(path, cv2.IMREAD_COLOR)
                    if template is None:
                        print(f"OpenCV не смог загрузить {img}, пробуем PIL")
                        pil_img = Image.open(path)
                        print(f"PIL загрузил {img} с модом {pil_img.mode}")
                        if pil_img.mode == 'L':
                            
                            template = np.array(pil_img)
                        else:
                            
                            template = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                        print(f"PIL успешно загрузил {img}")
                else:
                    if img in grayscale_images:
                        template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    else:
                        template = cv2.imread(path, cv2.IMREAD_COLOR)
            except Exception as e:
                self.app.logger.log("AntiAfk", f"Ошибка при загрузке {img}: {e}", "error")
                template = None
            if template is None:
                self.app.logger.log("AntiAfk", f"Не удалось загрузить изображение: {img}", "error")
            else:
                templates[img] = template
        return templates

    def toggle_frame(self, frame):
        if frame.winfo_viewable():
            frame.pack_forget()
        else:
            frame.pack(fill=tk.X, pady=5)
        self.root.update_idletasks()
        self.root.geometry(self.current_geometry)

    def update_window_size(self, event=None):
        if self.exiting or not self.notebook.winfo_exists():
            return
        self.current_tab = self.notebook.index(self.notebook.select())
        self.root.update_idletasks()
        self.root.geometry(self.current_geometry)

    def configure_combobox_listbox(self, combobox):
        def postcommand():
            listbox_path = combobox.tk.call(combobox._w, "get", "popdown")
            listbox = self.root.nametowidget(listbox_path)
            listbox.configure(bg=ENTRY_BG_COLOR, fg=TEXT_FG_COLOR, selectbackground=BUTTON_COLOR, selectforeground=HEADER_TEXT_COLOR)
        combobox.configure(postcommand=postcommand)

    def assign_key(self, entry, var, keycode_var_name=None, callback=None):
        self.assigning_key = entry
        self.current_entry = entry
        entry.config(state='disabled')
        entry.delete(0, tk.END)
        entry.insert(0, "Нажмите клавишу...")
        self.is_changing_bind = True  

        def on_press(key):
            try:
                vk_code = key.vk if hasattr(key, 'vk') else key.value.vk
                char = key.char if hasattr(key, 'char') else None
                keysym = self.get_keysym(vk_code)
                display_key = self.get_display_key(vk_code, keysym)
                var.set(display_key)
                if keycode_var_name:
                    setattr(self, keycode_var_name, vk_code)
                entry.config(state='normal')
                entry.delete(0, tk.END)
                entry.insert(0, display_key)
                self.assigning_key = None
                self.current_entry = None
                self.is_changing_bind = False  
                if callback:
                    callback()
                return False
            except AttributeError:
                return True

        listener = pynput_keyboard.Listener(on_press=on_press)
        listener.start()

    def set_game_window(self):
        self.resolution_button.config(text="жду нажатия")
        instruction_window = tk.Toplevel(self.root)
        instruction_window.overrideredirect(True)
        instruction_window.attributes("-topmost", True)
        instruction_window.geometry("+10+10")
        instruction_window.configure(bg=BACKGROUND_COLOR)
        tk.Label(instruction_window, text="Зайдите в окно игры нажав в нем лкм, а после нажмите Enter",
                 bg=BACKGROUND_COLOR, fg=TEXT_COLOR, bd=0, highlightthickness=0,
                 font=('Roboto', self.get_scaled_font_size(12), 'bold')).pack(padx=3, pady=3)

        def on_enter_press(key):
            if key == pynput_keyboard.Key.enter:
                game_hwnd = win32gui.GetForegroundWindow()
                left, top, right, bottom = win32gui.GetWindowRect(game_hwnd)
                self.game_left = left
                self.game_top = top
                self.game_width = right - left
                self.game_height = bottom - top
                if self.game_width != 1920 or self.game_height != 1080:
                    self.show_error("Предупреждение",
                                    "Разрешение игры не 1920x1080. Масштабирование может работать некорректно.")
                self.scale_x = self.game_width / 1920.0
                self.scale_y = self.game_height / 1080.0
                self.config["General"]["GameResolution"] = f"{self.game_width}x{self.game_height}"
                self.resolution_display.config(text=f"Выбранное разрешение: {self.game_width}x{self.game_height}")
                instruction_window.destroy()
                self.resolution_button.config(text="успешно")
                self.root.after(5000, lambda: self.resolution_button.config(text="установить разрешение"))
                for bot in self.bots.values():
                    if hasattr(bot, 'update_search_area'):
                        bot.update_search_area()
                    elif hasattr(bot, 'update_areas'):
                        bot.update_areas()
                self.setup_styles()
                return False

        listener = pynput_keyboard.Listener(on_press=on_enter_press)
        listener.start()

    def create_bind_type_selector(self, frame, var):
        ttk.Label(frame, text="Тип:").pack(side=tk.LEFT)
        ttk.Radiobutton(frame, text="клавиша", variable=var, value="key", style='Antiafk.TCheckbutton').pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(frame, text="Мышь", variable=var, value="mouse", style='Antiafk.TCheckbutton').pack(side=tk.LEFT, padx=2)

    def setup_gui(self):
        self.title_bar = tk.Frame(self.root, bg=BUTTON_COLOR, borderwidth=0, highlightthickness=0)
        self.title_bar.pack(fill=tk.X, padx=0, pady=0)
        tk.Label(self.title_bar, text="SNIKER LITE", bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                font=('Roboto', self.get_scaled_font_size(10), 'bold')).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(self.title_bar, text="X", command=self.exit_gracefully, bg=BUTTON_COLOR,
                fg=HEADER_TEXT_COLOR, font=('Roboto', self.get_scaled_font_size(10), 'bold'),
                relief='flat', borderwidth=0, activebackground=ACTIVE_BUTTON_COLOR,
                activeforeground=HEADER_TEXT_COLOR).pack(side=tk.RIGHT, padx=2, pady=2)
        tk.Button(self.title_bar, text="–", command=self.toggle_minimize, bg=BUTTON_COLOR,
                fg=HEADER_TEXT_COLOR, font=('Roboto', self.get_scaled_font_size(10), 'bold'),
                relief='flat', borderwidth=0, activebackground=ACTIVE_BUTTON_COLOR,
                activeforeground=HEADER_TEXT_COLOR).pack(side=tk.RIGHT, padx=2, pady=2)
        tk.Button(self.title_bar, image=self.logs_icon, command=self.show_logs, bg=BUTTON_COLOR,
                relief='flat', borderwidth=0, activebackground=ACTIVE_BUTTON_COLOR).pack(side=tk.RIGHT, padx=2, pady=2)
        tk.Button(self.title_bar, image=self.settings_icon, command=self.open_settings_window,
                bg=BUTTON_COLOR, relief='flat', borderwidth=0, activebackground=ACTIVE_BUTTON_COLOR).pack(side=tk.RIGHT, padx=2, pady=2)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
        self.notebook.bind("<<NotebookTabChanged>>", self.update_window_size)

        home_frame = tk.Frame(self.notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.notebook.add(home_frame, text="Главная", image=self.home_icon, compound=tk.LEFT)
        tk.Label(home_frame, text="SNIKER LITE", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                font=('Roboto', self.get_scaled_font_size(18), 'bold')).pack(expand=True)
        self.home_frame = home_frame

        works_frame = tk.Frame(self.notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.notebook.add(works_frame, text="Работы", image=self.work_icon, compound=tk.LEFT)
        self.works_notebook = ttk.Notebook(works_frame)
        self.works_notebook.pack(fill=tk.BOTH, expand=True)

        port_frame = tk.Frame(self.works_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.works_notebook.add(port_frame, text="Порт")
        building_frame = tk.Frame(self.works_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.works_notebook.add(building_frame, text="Стройка")
        mine_frame = tk.Frame(self.works_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.works_notebook.add(mine_frame, text="Шахта")
        farm_frame = tk.Frame(self.works_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.works_notebook.add(farm_frame, text="Ферма")

        other_frame = tk.Frame(self.notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.notebook.add(other_frame, text="Другое", image=self.access_icon, compound=tk.LEFT)
        self.other_notebook = ttk.Notebook(other_frame)
        self.other_notebook.pack(fill=tk.BOTH, expand=True)

        antiafk_frame = tk.Frame(self.other_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.other_notebook.add(antiafk_frame, text="Antiafk")
        ems_frame = tk.Frame(self.other_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.other_notebook.add(ems_frame, text="Ems")
        cooking_frame = tk.Frame(self.other_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.other_notebook.add(cooking_frame, text="Готовка")
        gym_frame = tk.Frame(self.other_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.other_notebook.add(gym_frame, text="Качалка")
        self.bot_frames['gym'] = gym_frame

        demorgan_tab_frame = tk.Frame(self.notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.notebook.add(demorgan_tab_frame, text="Деморган", image=self.jail_icon, compound=tk.LEFT)
        self.demorgan_notebook = ttk.Notebook(demorgan_tab_frame)
        self.demorgan_notebook.pack(fill=tk.BOTH, expand=True)

        demorgan_sub_frame = tk.Frame(self.demorgan_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.demorgan_notebook.add(demorgan_sub_frame, text="Швейка")
        dmtokar_sub_frame = tk.Frame(self.demorgan_notebook, bg=FRAME_BG_COLOR, borderwidth=0, highlightthickness=0)
        self.demorgan_notebook.add(dmtokar_sub_frame, text="Токарь")

        self.bot_frames = {
            'port': port_frame,
            'building': building_frame,
            'mine': mine_frame,
            'farm': farm_frame,
            'antiafk': antiafk_frame,
            'ems': ems_frame,
            'demorgan': demorgan_sub_frame,
            'dmtokar': dmtokar_sub_frame,
            'cooking': cooking_frame,
            'gym': gym_frame
        }

    def save_settings(self):
        self.config["General"]["GameResolution"] = f"{self.game_width}x{self.game_height}"
        self.config["General"]["AutoRun"] = str(self.auto_run_var.get())
        
        self.config["Port"]["BoxReward"] = self.port_price_var.get()
        
        self.config["Mine"]["ActionReward"] = self.mine_price_var.get()
        
        self.config["Building"]["ActionReward"] = self.building_price_var.get()
        
        self.config["Gym"]["FoodCooldown"] = str(self.food_cooldown_var.get())
        self.config["Gym"]["EatKey"] = self.eat_key_var.get()
        self.config["Gym"]["EatKeyCode"] = str(self.eat_keycode) if self.eat_keycode else ""
        self.config["Gym"]["ExpanderKey"] = self.expander_key_var.get()
        self.config["Gym"]["ExpanderKeyCode"] = str(self.expander_keycode) if self.expander_keycode else ""
        
        self.config["AntiAfk"]["AntiAfkEnabled"] = str(self.anti_afk_var.get())
        self.config["AntiAfk"]["LotteryEnabled"] = str(self.lottery_var.get())
        self.config["AntiAfk"]["RouletteEnabled"] = str(self.roulette_var.get())
        self.config["AntiAfk"]["TelegramToken"] = self.telegram_token_var.get()
        self.config["AntiAfk"]["ChatFontSize"] = self.bots['antiafk'].chat_font_var.get()
        self.config["AntiAfk"]["Password"] = self.password_var.get()
        self.config["AntiAfk"]["AutoReconnect"] = str(self.auto_reconnect_var.get())
        self.config["Hotkeys"]["HideShowKeyCode"] = str(self.hide_show_keycode)
        self.config["AntiAfk"]["TakeOutPhoneKeyCode"] = str(self.take_out_keycode)
        self.config["AntiAfk"]["PutAwayPhoneKeyCode"] = str(self.put_away_keycode)
        self.config["AntiAfk"]["AnimationKeyCode"] = str(self.animation_keycode)
        self.config["Hotkeys"]["HideShowKey"] = self.hide_show_key_var.get()
        self.config["AntiAfk"]["TakeOutPhoneKey"] = self.take_out_bind_value_var.get()
        self.config["AntiAfk"]["PutAwayPhoneKey"] = self.put_away_bind_value_var.get()
        self.config["AntiAfk"]["AnimationKey"] = self.animation_bind_value_var.get()
        
        if hasattr(self.bots['antiafk'], 'lottery_app_coords') and self.bots['antiafk'].lottery_app_coords is not None:
            self.config["AntiAfk"]["LotteryAppX"] = str(self.bots['antiafk'].lottery_app_coords[0])
            self.config["AntiAfk"]["LotteryAppY"] = str(self.bots['antiafk'].lottery_app_coords[1])
        if hasattr(self.bots['antiafk'], 'lottery_buy_coords') and self.bots['antiafk'].lottery_buy_coords is not None:
            self.config["AntiAfk"]["LotteryBuyX"] = str(self.bots['antiafk'].lottery_buy_coords[0])
            self.config["AntiAfk"]["LotteryBuyY"] = str(self.bots['antiafk'].lottery_buy_coords[1])
        if hasattr(self.bots['antiafk'], 'casino_app_coords') and self.bots['antiafk'].casino_app_coords is not None:
            self.config["AntiAfk"]["CasinoAppX"] = str(self.bots['antiafk'].casino_app_coords[0])
            self.config["AntiAfk"]["CasinoAppY"] = str(self.bots['antiafk'].casino_app_coords[1])
        if hasattr(self.bots['antiafk'], 'spin_button_coords') and self.bots['antiafk'].spin_button_coords is not None:
            self.config["AntiAfk"]["SpinButtonX"] = str(self.bots['antiafk'].spin_button_coords[0])
            self.config["AntiAfk"]["SpinButtonY"] = str(self.bots['antiafk'].spin_button_coords[1])
        
        config_path = os.path.join(self.sniker_lite_path, "sniker_settings.ini")
        try:
            with open(config_path, "w", encoding='utf-8') as f:
                self.config.write(f)
            self.logger.log("Settings", "Настройки сохранены")
        except Exception as e:
            self.logger.log("Settings", f"Ошибка при сохранении настроек: {e}", "error")
        
        for bot_name in ['port', 'mine', 'building']:
            self.bots[bot_name].auto_run = self.config["General"].getboolean("AutoRun")
        for bot in self.bots.values():
            if hasattr(bot, 'resolution'):
                bot.resolution = self.config["General"]["GameResolution"]
                bot.scale_x = float(bot.resolution.split('x')[0]) / 1920
                bot.scale_y = float(bot.resolution.split('x')[1]) / 1080
                if hasattr(bot, 'update_areas'):
                    bot.update_areas()
                elif hasattr(bot, 'update_search_area'):
                    bot.update_search_area()
            if hasattr(bot, 'box_reward'):
                bot.box_reward = int(self.config["Port"]["BoxReward"])
            if hasattr(bot, 'action_reward'):
                if bot == self.bots['mine']:
                    bot.action_reward = int(self.config["Mine"]["ActionReward"])
                elif bot == self.bots['building']:
                    bot.action_reward = int(self.config["Building"]["ActionReward"])
            if bot == self.bots['antiafk']:
                bot.anti_afk_enabled = self.config["AntiAfk"].getboolean("AntiAfkEnabled")
                bot.lottery_enabled = self.config["AntiAfk"].getboolean("LotteryEnabled")
                bot.roulette_enabled = self.config["AntiAfk"].getboolean("RouletteEnabled")
                bot.telegram_token = self.config["AntiAfk"].get("TelegramToken", "")
                bot.chat_font_size = int(self.config["AntiAfk"]["ChatFontSize"])

    def show_error(self, title, message):
        error_key = f"{title}:{message}"
        if error_key in self.error_windows and self.error_windows[error_key].winfo_exists():
            self.error_windows[error_key].lift()
            return
        error_window = CustomErrorWindow(self, title, message)
        self.error_windows[error_key] = error_window.root
        error_window.root.protocol("WM_DELETE_WINDOW", lambda: self.on_error_window_close(error_key))

    def format_theme_name(self, name):
        return name.replace('_', ' ').title()

    def select_theme(self, theme_name, theme_window):
        set_theme(theme_name)
        self.apply_theme()
        self.config["General"]["SelectedTheme"] = theme_name
        with open(os.path.join(self.sniker_lite_path, "sniker_settings.ini"), 'w', encoding='utf-8') as f:
            self.config.write(f)
        theme_window.destroy()

    def open_theme_selection(self):
        if hasattr(self, 'settings_window') and self.settings_window.winfo_exists():
            self.settings_window.destroy()
        
        theme_window = tk.Toplevel(self.root)
        theme_window.overrideredirect(True)
        theme_window.attributes("-topmost", True)
        theme_window.configure(bg=BACKGROUND_COLOR)
        theme_window.geometry("450x350+100+100")

        title_bar = tk.Frame(theme_window, bg=BUTTON_COLOR)
        title_bar.pack(fill=tk.X)
        tk.Label(title_bar, text="Выбор темы", bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                font=('Roboto', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(title_bar, text="X", command=theme_window.destroy, bg=BUTTON_COLOR,
                fg=HEADER_TEXT_COLOR, font=('Roboto', 10, 'bold'), relief='flat').pack(side=tk.RIGHT, padx=2)

        content_frame = tk.Frame(theme_window, bg=FRAME_BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(content_frame, bg=FRAME_BG_COLOR, highlightthickness=0, height=300)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=FRAME_BG_COLOR)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        self.add_resize_handle(theme_window)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass

        theme_window.bind("<MouseWheel>", on_mousewheel)

        for theme_name in THEMES.keys():
            theme_frame = tk.Frame(scrollable_frame, bg=FRAME_BG_COLOR)
            theme_frame.pack(fill=tk.X, pady=5)
            formatted_name = self.format_theme_name(theme_name)
            theme_label = tk.Label(theme_frame, text=formatted_name, bg=FRAME_BG_COLOR, fg=TEXT_COLOR,
                                font=('Roboto', 10, 'bold'))
            theme_label.pack(side=tk.LEFT)
            colors_frame = tk.Frame(theme_frame, bg=FRAME_BG_COLOR)
            colors_frame.pack(side=tk.LEFT, padx=10)
            theme_colors = THEMES[theme_name]
            for color_key in ['BACKGROUND_COLOR', 'BUTTON_COLOR', 'TEXT_COLOR']:
                color = theme_colors[color_key]
                color_label = tk.Label(colors_frame, bg=color, width=2, height=1)
                color_label.pack(side=tk.LEFT, padx=2)
            theme_frame.bind("<Button-1>", lambda e, tn=theme_name: self.select_theme(tn, theme_window))
            theme_label.bind("<Button-1>", lambda e, tn=theme_name: self.select_theme(tn, theme_window))
            colors_frame.bind("<Button-1>", lambda e, tn=theme_name: self.select_theme(tn, theme_window))
            theme_frame.bind("<Enter>", lambda e, f=theme_frame: f.configure(bg=ACTIVE_BUTTON_COLOR))
            theme_frame.bind("<Leave>", lambda e, f=theme_frame: f.configure(bg=FRAME_BG_COLOR))

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        title_bar.bind('<ButtonPress-1>', lambda e: self.start_move_window(e, theme_window))
        title_bar.bind('<B1-Motion>', lambda e: self.do_move_window(e))
        title_bar.bind('<ButtonRelease-1>', lambda e: self.stop_move_window(e))

    def open_settings_window(self):
        self.settings_open = True
        if hasattr(self, 'settings_window') and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window, content_frame = self.create_toplevel("Settings", width=420, height=450)
        self.settings_window.bind('<Key>', self.key_handler)

        canvas = tk.Canvas(content_frame, bg=FRAME_BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=FRAME_BG_COLOR)

        self.settings_open = True
        self.settings_window.protocol("WM_DELETE_WINDOW", self.on_settings_close)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass

        self.settings_window.bind("<MouseWheel>", on_mousewheel)

        
        theme_frame = ttk.Frame(scrollable_frame, style='Antiafk.TFrame')
        theme_frame.pack(fill=tk.X, pady=5)
        theme_button = ttk.Button(theme_frame, text="Сменить тему", command=self.open_theme_selection)
        theme_button.pack(side=tk.LEFT, pady=2)
        save_button = ttk.Button(theme_frame, text="Сохранить", command=self.save_settings)
        save_button.pack(side=tk.LEFT, padx=5)

        
        other_frame = ttk.Frame(scrollable_frame, style='Antiafk.TFrame')
        other_frame.pack(fill=tk.X, pady=5)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(other_frame, text="Другое", style='Antiafk.TLabel', font=('Roboto', self.get_scaled_font_size(11), 'bold')).pack(anchor=tk.W)
        resolution_frame = ttk.Frame(other_frame)
        resolution_frame.pack(fill=tk.X, pady=2)
        resolution_label = ttk.Label(resolution_frame, text="Разрешение:", style='Antiafk.TLabel')
        resolution_label.pack(side=tk.LEFT, padx=5)
        self.resolution_button = ttk.Button(resolution_frame, text="установить разрешение", command=self.set_game_window)
        self.resolution_button.pack(side=tk.LEFT, padx=5)
        ToolTip(self.resolution_button, "Установить разрешение игрового окна")
        self.resolution_display = ttk.Label(other_frame, text=f"Выбранное разрешение: {self.game_width}x{self.game_height}", style='Antiafk.TLabel')
        self.resolution_display.pack(fill=tk.X, pady=2)
        hide_show_key_frame = ttk.Frame(other_frame)
        hide_show_key_frame.pack(fill=tk.X, pady=2)
        ttk.Label(hide_show_key_frame, text="Скрыть/показать окно:", style='Antiafk.TLabel').pack(side=tk.LEFT)
        hide_show_key_entry = ttk.Entry(hide_show_key_frame, textvariable=self.hide_show_key_var, width=5, style='Antiafk.TEntry', state='readonly')
        hide_show_key_entry.pack(side=tk.LEFT, padx=5)
        hide_show_key_entry.bind("<FocusIn>", lambda e, entry=hide_show_key_entry: self.start_bind_listener("key", self.hide_show_key_var, entry))
        ToolTip(hide_show_key_entry, "Клавиша для скрытия/показа окна")

        
        works_frame = ttk.Frame(scrollable_frame, style='Antiafk.TFrame')
        works_frame.pack(fill=tk.X, pady=5)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(works_frame, text="Работы", style='Antiafk.TLabel', font=('Roboto', self.get_scaled_font_size(11), 'bold')).pack(anchor=tk.W)
        port_price_frame = ttk.Frame(works_frame)
        port_price_frame.pack(fill=tk.X, pady=2)
        ttk.Label(port_price_frame, text="Цена за действие (Порт):", style='Antiafk.TLabel').pack(side=tk.LEFT)
        port_price_entry = ttk.Entry(port_price_frame, textvariable=self.port_price_var, width=5, style='Antiafk.TEntry')
        port_price_entry.pack(side=tk.LEFT, padx=5)
        ToolTip(port_price_entry, "Цена за ящик в порту")
        mine_price_frame = ttk.Frame(works_frame)
        mine_price_frame.pack(fill=tk.X, pady=2)
        ttk.Label(mine_price_frame, text="Цена за действие (Шахта):", style='Antiafk.TLabel').pack(side=tk.LEFT)
        mine_price_entry = ttk.Entry(mine_price_frame, textvariable=self.mine_price_var, width=5, style='Antiafk.TEntry')
        mine_price_entry.pack(side=tk.LEFT, padx=5)
        ToolTip(mine_price_entry, "Цена за действие в шахте")
        building_price_frame = ttk.Frame(works_frame)
        building_price_frame.pack(fill=tk.X, pady=2)
        ttk.Label(building_price_frame, text="Цена за действие (Стройка):", style='Antiafk.TLabel').pack(side=tk.LEFT)
        building_price_entry = ttk.Entry(building_price_frame, textvariable=self.building_price_var, width=5, style='Antiafk.TEntry')
        building_price_entry.pack(side=tk.LEFT, padx=5)
        ToolTip(building_price_entry, "Цена за действие на стройке")
        auto_run_check = ttk.Checkbutton(works_frame, text="Автобег", variable=self.auto_run_var, style='Antiafk.TCheckbutton')
        auto_run_check.pack(anchor=tk.W)
        ToolTip(auto_run_check, "Включить автобег для ботов")

        
        antiafk_frame = ttk.Frame(scrollable_frame, style='Antiafk.TFrame')
        antiafk_frame.pack(fill=tk.X, pady=5)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(antiafk_frame, text="Настройки Anti-AFK", style='Antiafk.TLabel', font=('Roboto', self.get_scaled_font_size(11), 'bold')).pack(anchor=tk.W)
        ttk.Checkbutton(antiafk_frame, text="Anti-AFK", variable=self.anti_afk_var, style='Antiafk.TCheckbutton').pack(anchor=tk.W)
        ttk.Checkbutton(antiafk_frame, text="Лотерея", variable=self.lottery_var, style='Antiafk.TCheckbutton').pack(anchor=tk.W)
        ttk.Checkbutton(antiafk_frame, text="Рулетки", variable=self.roulette_var, style='Antiafk.TCheckbutton').pack(anchor=tk.W)
        token_label_frame = ttk.Frame(antiafk_frame)
        token_label_frame.pack(fill=tk.X)
        ttk.Label(token_label_frame, text="Токен Telegram-бота:", style='Antiafk.TLabel').pack(side=tk.LEFT)
        paste_button = ttk.Button(token_label_frame, text="Вставить", command=lambda: telegram_token_entry.insert(0, self.root.clipboard_get()))
        paste_button.pack(side=tk.LEFT, padx=5)
        ToolTip(paste_button, "Вставить токен из буфера обмена")
        telegram_token_entry = ttk.Entry(antiafk_frame, textvariable=self.telegram_token_var, width=5, style='Antiafk.TEntry')
        telegram_token_entry.pack(fill=tk.X, pady=2)
        ToolTip(telegram_token_entry, "Токен для Telegram-бота")
        password_frame = ttk.Frame(antiafk_frame)
        password_frame.pack(fill=tk.X, pady=2)
        ttk.Label(password_frame, text="Пароль:", style='Antiafk.TLabel').pack(side=tk.LEFT)
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*", width=20, style='Antiafk.TEntry')
        self.password_entry.pack(side=tk.LEFT, padx=5)
        self.password_toggle_button = tk.Button(
            password_frame,
            image=self.show_icon,
            command=self.toggle_password_visibility,
            bg=BUTTON_COLOR,
            fg=HEADER_TEXT_COLOR,
            relief='flat',
            activebackground=ACTIVE_BUTTON_COLOR,
            activeforeground=HEADER_TEXT_COLOR,
            bd=0,
            highlightthickness=0
        )
        self.password_toggle_button.pack(side=tk.LEFT, padx=2)
        character_frame = ttk.Frame(antiafk_frame)
        character_frame.pack(fill=tk.X, pady=2)
        ttk.Label(character_frame, text="Настройка выбора персонажа:", style='Antiafk.TLabel').pack(side=tk.LEFT)
        set_character_button = ttk.Button(character_frame, text="Установить координаты", command=self.bots['antiafk'].setup_character_selection)
        set_character_button.pack(side=tk.LEFT, padx=5)
        ToolTip(set_character_button, "Настройте координаты для выбора персонажа")
        ttk.Checkbutton(antiafk_frame, text="Автореконнект", variable=self.auto_reconnect_var, style='Antiafk.TCheckbutton').pack(anchor=tk.W)
        reset_coords_button = ttk.Button(antiafk_frame, text="Сбросить координаты Anti-AFK", command=self.reset_antiafk_coords)
        reset_coords_button.pack(pady=5)
        take_out_phone_frame = ttk.Frame(antiafk_frame)
        take_out_phone_frame.pack(fill=tk.X, pady=2)
        ttk.Label(take_out_phone_frame, text="Достать телефон:", style='Antiafk.TLabel').pack(side=tk.LEFT)
        self.create_bind_type_selector(take_out_phone_frame, self.take_out_bind_type_var)
        take_out_key_entry = ttk.Entry(take_out_phone_frame, textvariable=self.take_out_bind_value_var, width=13, style='Antiafk.TEntry', state='readonly')
        take_out_key_entry.pack(side=tk.LEFT, padx=5)
        take_out_key_entry.bind("<FocusIn>", lambda e, entry=take_out_key_entry: self.start_bind_listener(self.take_out_bind_type_var.get(), self.take_out_bind_value_var, entry))
        ToolTip(take_out_key_entry, "Клавиша для доставания телефона")
        put_away_phone_frame = ttk.Frame(antiafk_frame)
        put_away_phone_frame.pack(fill=tk.X, pady=5)
        ttk.Label(put_away_phone_frame, text="Убрать телефон:", style='Antiafk.TLabel').pack(side=tk.LEFT)
        self.create_bind_type_selector(put_away_phone_frame, self.put_away_bind_type_var)
        put_away_key_entry = ttk.Entry(put_away_phone_frame, textvariable=self.put_away_bind_value_var, width=13, style='Antiafk.TEntry', state='readonly')
        put_away_key_entry.pack(side=tk.LEFT, padx=8)
        put_away_key_entry.bind("<FocusIn>", lambda e, entry=put_away_key_entry: self.start_bind_listener(self.put_away_bind_type_var.get(), self.put_away_bind_value_var, entry))
        ToolTip(put_away_key_entry, "Клавиша для убирания телефона")
        animation_key_frame = ttk.Frame(antiafk_frame)
        animation_key_frame.pack(fill=tk.X, pady=2)
        ttk.Label(animation_key_frame, text="Клавиша анимки:", style='Antiafk.TLabel').pack(side=tk.LEFT)
        self.create_bind_type_selector(animation_key_frame, self.animation_bind_type_var)
        animation_key_entry = ttk.Entry(animation_key_frame, textvariable=self.animation_bind_value_var, width=13, style='Antiafk.TEntry', state='readonly')
        animation_key_entry.pack(side=tk.LEFT, padx=5)
        animation_key_entry.bind("<FocusIn>", lambda e, entry=animation_key_entry: self.start_bind_listener(self.animation_bind_type_var.get(), self.animation_bind_value_var, entry))
        ToolTip(animation_key_entry, "Клавиша для анимации")
        chat_font_frame = ttk.Frame(antiafk_frame)
        chat_font_frame.pack(fill=tk.X, pady=2)
        ttk.Label(chat_font_frame, text="Размер шрифта чата:", style='Antiafk.TLabel').pack(side=tk.LEFT)
        chat_font_combobox = ttk.Combobox(chat_font_frame, textvariable=self.bots['antiafk'].chat_font_var,
                                        values=["15", "20", "25", "30"], state="readonly", width=5, style='Antiafk.TCombobox')
        chat_font_combobox.pack(side=tk.LEFT, padx=5)

        
        gym_frame = ttk.Frame(scrollable_frame, style='Antiafk.TFrame')
        gym_frame.pack(fill=tk.X, pady=5)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(gym_frame, text="Настройки качалки", style='Antiafk.TLabel', font=('Roboto', self.get_scaled_font_size(11), 'bold')).pack(anchor=tk.W)
        
        self.food_cooldown_str_var = tk.StringVar()
        food_cooldown_frame = ttk.Frame(gym_frame)
        food_cooldown_frame.pack(fill=tk.X, pady=2)
        ttk.Label(food_cooldown_frame, text="Кулдаун еды (мин):", style='Antiafk.TLabel').pack(side=tk.LEFT)
        food_cooldown_slider = ttk.Scale(food_cooldown_frame, from_=1, to=60, orient=tk.HORIZONTAL, 
                                 variable=self.food_cooldown_var, length=200, style='Antiafk.Horizontal.TScale')
        food_cooldown_slider.pack(side=tk.LEFT, padx=5)
        food_cooldown_value_label = ttk.Label(food_cooldown_frame, textvariable=self.food_cooldown_str_var, style='Antiafk.TLabel')
        food_cooldown_value_label.pack(side=tk.LEFT, padx=5)
        ToolTip(food_cooldown_slider, "Время между приемами пищи в минутах")
        
        def update_food_cooldown_str(*args):
            self.food_cooldown_str_var.set(f"{self.food_cooldown_var.get():.1f}")
        self.food_cooldown_var.trace("w", update_food_cooldown_str)
        update_food_cooldown_str()

        eat_key_frame = ttk.Frame(gym_frame)
        eat_key_frame.pack(fill=tk.X, pady=2)
        ttk.Label(eat_key_frame, text="Клавиша еды:", style='Antiafk.TLabel').pack(side=tk.LEFT)
        eat_key_entry = ttk.Entry(eat_key_frame, textvariable=self.eat_key_var, width=5, style='Antiafk.TEntry', state='readonly')
        eat_key_entry.pack(side=tk.LEFT, padx=5)
        eat_key_entry.bind("<FocusIn>", lambda e, entry=eat_key_entry: self.start_bind_listener("key", self.eat_key_var, entry))
        ToolTip(eat_key_entry, "Клавиша для действия 'Поесть'")

        expander_key_frame = ttk.Frame(gym_frame)
        expander_key_frame.pack(fill=tk.X, pady=2)
        ttk.Label(expander_key_frame, text="Клавиша эспандера:", style='Antiafk.TLabel', foreground=TEXT_COLOR).pack(side=tk.LEFT)
        expander_key_entry = ttk.Entry(expander_key_frame, textvariable=self.expander_key_var, width=5, style='Antiafk.TEntry', state='readonly')
        expander_key_entry.pack(side=tk.LEFT, padx=5)
        expander_key_entry.bind("<FocusIn>", lambda e, entry=expander_key_entry: self.start_bind_listener("key", self.expander_key_var, entry))
        ToolTip(expander_key_entry, "Клавиша для действия 'Взять эспандер'")
    
    def on_settings_close(self):
        self.settings_open = False
        self.settings_window.destroy()
    
    def toggle_password_visibility(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
            self.password_toggle_button.config(image=self.hide_icon)
        else:
            self.password_entry.config(show='*')
            self.password_toggle_button.config(image=self.show_icon)

    def do_move_window(self, event):
        if self.moving_window:
            deltax = event.x - self._x
            deltay = event.y - self._y
            x = self.moving_window.winfo_x() + deltax
            y = self.moving_window.winfo_y() + deltay
            self.moving_window.geometry(f'+{x}+{y}')

    def stop_move_window(self, event, window):
        self.x = None
        self.y = None
        self.moving_window = None

    def toggle_minimize(self):
        if not self.is_minimized:
            self.normal_geometry = self.root.geometry()
            self.notebook.pack_forget()
            self.root.geometry(f"270x{self.title_bar.winfo_height()}")
            self.is_minimized = True
        else:
            self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
            self.root.geometry(self.normal_geometry)
            self.is_minimized = False

    def setup_hotkeys(self):
        
        reset_key = self.config["General"].get("ResetStatsKey", "f9")
        keyboard.add_hotkey(reset_key, lambda: self.root.after(0, self.reset_all_stats), trigger_on_release=True)

        keyboard.add_hotkey('f5', lambda: self.root.after(0, self.toggle_active_bot))
        keyboard.add_hotkey('w+f5', lambda: self.root.after(0, self.toggle_active_bot))
        keyboard.add_hotkey('shift+f5', lambda: self.root.after(0, self.toggle_active_bot))
        keyboard.add_hotkey('w+shift+f5', lambda: self.root.after(0, self.toggle_active_bot))

        
        if "Gym" not in self.config:
            self.config.add_section("Gym")
        if "ExpanderKey" not in self.config["Gym"]:
            self.config["Gym"]["ExpanderKey"] = ""  

        
        def on_press(key):
            try:
                vk_code = key.vk if hasattr(key, 'vk') else key.value.vk
                if vk_code == self.hide_show_keycode:  
                    if not self.is_changing_bind:  
                        current_time = time.time()
                        if current_time - self.last_toggle_time > 0.2:
                            self.toggle_visibility()
                            self.last_toggle_time = current_time
            except AttributeError:
                pass

        self.keyboard_listener = pynput_keyboard.Listener(on_press=on_press)
        self.keyboard_listener.start()
    
    def on_key_press(self, event):
        if self.assigning_key:
            key = event.keysym
            if key == 'Escape':  
                self.assigning_key = None
                return
            print(f"Key pressed: {event.keysym}, assigning_key: {self.assigning_key}")
            if self.assigning_key == 'eat':
                self.eat_key_var.set(key)  
                self.config["Gym"]["EatKey"] = key  
                self.save_config()  
            
            self.assigning_key = None  
    
    def reset_all_stats(self):
        for bot in self.bots.values():
            if hasattr(bot, 'reset_stats'):
                bot.reset_stats()

    def force_reconnect(self):
        antiafk_bot = self.bots.get('antiafk')
        if antiafk_bot:
            if not antiafk_bot.bot_running:
                self.logger.log("AntiAfk", "Бот не активен", "warning")
                return
            if not antiafk_bot.auto_reconnect_enabled:
                self.logger.log("AntiAfk", "АвтоРеконект отключено", "warning")
                return
            if not antiafk_bot.password:
                self.logger.log("AntiAfk", "Пароль не указан в настройках", "warning")
                return
            antiafk_bot.perform_reconnect()
        else:
            self.logger.log("AntiAfk", "Бот AntiAfk не найден", "error")

    def key_handler(self, event):
        if self.assigning_key:
            if event.keysym == 'Escape':  
                self.current_entry.config(state='normal')
                self.current_entry.delete(0, tk.END)
                self.current_entry.insert(0, self.get_display_key(event.keycode, event.keysym))
                self.current_entry.config(state='readonly')
                self.assigning_key = None
                self.current_entry = None
                self.is_changing_bind = False
                return
            print(f"Key pressed: {event.keysym}, keycode: {event.keycode}, assigning_key: {self.assigning_key}")
            if self.assigning_key == "hide_show":
                self.hide_show_keycode = event.keycode
                display_key = self.get_display_key(event.keycode, event.keysym)
                self.hide_show_key_var.set(display_key)
                self.config["Hotkeys"]["HideShowKey"] = display_key
                self.config["Hotkeys"]["HideShowKeyCode"] = str(event.keycode)
            elif self.assigning_key == "take_out":
                self.take_out_keycode = event.keycode
                display_key = self.get_display_key(event.keycode, event.keysym)
                self.take_out_bind_value_var.set(display_key)
                self.config["AntiAfk"]["TakeOutPhoneKey"] = display_key
                self.config["AntiAfk"]["TakeOutPhoneKeyCode"] = str(event.keycode)
            elif self.assigning_key == "put_away":
                self.put_away_keycode = event.keycode
                display_key = self.get_display_key(event.keycode, event.keysym)
                self.put_away_bind_value_var.set(display_key)
                self.config["AntiAfk"]["PutAwayPhoneKey"] = display_key
                self.config["AntiAfk"]["PutAwayPhoneKeyCode"] = str(event.keycode)
            elif self.assigning_key == "animation":
                self.animation_keycode = event.keycode
                display_key = self.get_display_key(event.keycode, event.keysym)
                self.animation_bind_value_var.set(display_key)
                self.config["AntiAfk"]["AnimationKey"] = display_key
                self.config["AntiAfk"]["AnimationKeyCode"] = str(event.keycode)
            elif self.assigning_key == "eat":
                self.eat_keycode = event.keycode
                display_key = self.get_display_key(event.keycode, event.keysym)
                self.eat_key_var.set(display_key)
                self.config["Gym"]["EatKey"] = display_key
                self.config["Gym"]["EatKeyCode"] = str(event.keycode)
            elif self.assigning_key == "expander":
                self.expander_keycode = event.keycode
                display_key = self.get_display_key(event.keycode, event.keysym)
                self.expander_key_var.set(display_key)
                self.config["Gym"]["ExpanderKey"] = display_key
                self.config["Gym"]["ExpanderKeyCode"] = str(event.keycode)
            
            
            if self.current_entry:
                self.current_entry = None
            
            
            with open(os.path.join(self.sniker_lite_path, "sniker_settings.ini"), "w", encoding='utf-8') as f:
                self.config.write(f)
            self.assigning_key = None
            self.is_changing_bind = False
        else:
            if event.widget.winfo_toplevel() == self.root:
                if event.keycode == 120:  
                    self.toggle_hide_show()

    def toggle_window(self):
        current_time = time.time()
        if current_time - self.last_toggle_time < 0.5:  
            return
        self.last_toggle_time = current_time
        if self.is_hidden:
            self.root.deiconify()
            self.root.wm_attributes('-topmost', True)
        else:
            self.root.withdraw()
        self.is_hidden = not self.is_hidden

    def toggle_active_bot(self):
        current_time = time.time()
        if current_time - self.last_toggle_time < 1:  
            return
        self.last_toggle_time = current_time
        selected_tab = self.notebook.select()
        tab_text = self.notebook.tab(selected_tab, "text")
        if tab_text == "Работы":
            sub_notebook = self.works_notebook
            selected_sub_tab = sub_notebook.select()
            bot_name = self.bot_name_mapping.get(sub_notebook.tab(selected_sub_tab, "text").lower())
            if bot_name:
                self.bots[bot_name].toggle_bot()
        elif tab_text == "Другое":
            sub_notebook = self.other_notebook
            selected_sub_tab = sub_notebook.select()
            bot_name = self.bot_name_mapping.get(sub_notebook.tab(selected_sub_tab, "text").lower())
            if bot_name:
                self.bots[bot_name].toggle_bot()
        elif tab_text == "Деморган":
            sub_notebook = self.demorgan_notebook
            selected_sub_tab = sub_notebook.select()
            bot_name = self.bot_name_mapping.get(sub_notebook.tab(selected_sub_tab, "text").lower())
            if bot_name:
                self.bots[bot_name].toggle_bot()
        else:
            self.show_error("Info", "Бот не выбран")

    def toggle_bot(self, bot_name):
        bot = self.bots.get(bot_name)
        if bot:
            bot.toggle_bot()
        else:
            self.logger.log("Main", f"Бот {bot_name} не найден", "error")

    def start_bind_listener(self, bind_type, bind_value_var, entry_widget):
        self.shortcuts_disabled_during_binding = True
        if bind_type == "key":
            if bind_value_var == self.take_out_bind_value_var:
                self.assigning_key = "take_out"
            elif bind_value_var == self.put_away_bind_value_var:
                self.assigning_key = "put_away"
            elif bind_value_var == self.animation_bind_value_var:
                self.assigning_key = "animation"
            elif bind_value_var == self.hide_show_key_var:
                self.assigning_key = "hide_show"
            elif bind_value_var == self.eat_key_var:
                self.assigning_key = "eat"
            elif bind_value_var == self.expander_key_var:
                self.assigning_key = "expander"
            else:
                self.assigning_key = None
            if self.assigning_key:
                bind_value_var.set("Press a key...")
                self.current_entry = entry_widget
                entry_widget.config(state='normal')
        elif bind_type == "mouse":
            threading.Thread(target=self.capture_mouse_bind, args=(bind_value_var,), daemon=True).start()

    def capture_mouse_bind(self, var):
        def on_click(x, y, button, pressed):
            if pressed:
                button_name = str(button).split('.')[-1]
                self.root.after(0, lambda: var.set(button_name))
                return False
        with pynput_mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def set_key_bind(self, key, var):
        if isinstance(key, pynput_keyboard.Key):
            key_name = key.name
        elif isinstance(key, pynput_keyboard.KeyCode):
            key_name = key.char if key.char else str(key.vk)
        else:
            key_name = str(key)
        self.root.after(0, lambda: var.set(key_name))
        return False

    def set_mouse_bind(self, button, pressed, var):
        if pressed:
            button_name = str(button).split('.')[-1]
            self.root.after(0, lambda: var.set(button_name))
            return False

    def reset_active_bot_stats(self):
        selected_tab = self.notebook.select()
        tab_text = self.notebook.tab(selected_tab, "text")
        if tab_text == "Работы":
            sub_notebook = self.works_notebook
            selected_sub_tab = sub_notebook.select()
            bot_name = self.bot_name_mapping.get(sub_notebook.tab(selected_sub_tab, "text").lower())
            if bot_name and bot_name != 'ems':
                self.bots[bot_name].reset_stats()
        elif tab_text == "Другое":
            sub_notebook = self.other_notebook
            selected_sub_tab = sub_notebook.select()
            bot_name = self.bot_name_mapping.get(sub_notebook.tab(selected_sub_tab, "text").lower())
            if bot_name and bot_name != 'ems':
                self.bots[bot_name].reset_stats()
        else:
            self.show_error("Info", "Бот не выбран")

    def show_logs(self):
        if not self.logs_window or not self.logs_window.winfo_exists():
            self.logs_window, content_frame = self.create_toplevel("Логи", width=600, height=400)
            title_bar = self.logs_window.winfo_children()[0]
            tk.Button(title_bar, image=self.clear_icon, command=self.clear_logs, bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                      relief='flat', bd=0, activebackground=ACTIVE_BUTTON_COLOR, activeforeground=HEADER_TEXT_COLOR).pack(side=tk.RIGHT, padx=1, pady=0)

            filter_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
            filter_frame.pack(fill=tk.X, pady=5, padx=0)
            tk.Label(filter_frame, text="Фильтр:", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                     font=('Roboto', self.get_scaled_font_size(10), 'bold')).pack(side=tk.LEFT, padx=5)
            self.logger.filter_var = tk.StringVar(value="all")
            filter_options = [("Все", "all"), ("Инфо", "info"), ("Предупреждения", "warning"), ("Ошибки", "error")]

            for text, value in filter_options:
                rb = tk.Radiobutton(filter_frame, text=text, value=value, 
                                    variable=self.logger.filter_var,
                                    command=self.update_logs,
                                    bg=BUTTON_COLOR,              
                                    fg=HEADER_TEXT_COLOR,              
                                    selectcolor=TAB_SELECTED_BG_COLOR,     
                                    activebackground=ACTIVE_BUTTON_COLOR,
                                    activeforeground=TEXT_FG_COLOR,
                                    indicatoron=0,             
                                    relief='flat', bd=0,       
                                    font=('Roboto', self.get_scaled_font_size(10), 'bold'))
                rb.pack(side=tk.LEFT, padx=5, pady=0)

            self.logger.logs_text = tk.Text(content_frame, wrap=tk.WORD, state='disabled', bg=TEXT_BG_COLOR,
                                            fg=TEXT_FG_COLOR, font=('Roboto', self.get_scaled_font_size(10), 'bold'), bd=0)
            scrollbar = ttk.Scrollbar(content_frame, orient='vertical', 
                                    command=self.logger.logs_text.yview)
            self.logger.logs_text.configure(yscrollcommand=scrollbar.set)
            self.logger.logs_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=0)
         
            self.auto_update_id = self.root.after(5000, self.auto_update_logs)
            
            self.update_logs()
        
        self.logs_window.deiconify()
        self.logs_window.lift()

    def clear_logs(self):
        with open(self.logger.log_file, "w", encoding="utf-8") as f:
            f.write("")
        self.update_logs()

    def update_logs(self):
        self.logger.logs_text.configure(state='normal')
        self.logger.logs_text.delete(1.0, tk.END)
        try:
            with open(self.logger.log_file, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    if "[WARNING]" in line and (self.logger.filter_var.get() == "all" or self.logger.filter_var.get() == "warning"):
                        self.logger.logs_text.insert(tk.END, line, "warning")
                    elif "[ERROR]" in line and (self.logger.filter_var.get() == "all" or self.logger.filter_var.get() == "error"):
                        self.logger.logs_text.insert(tk.END, line, "error")
                    elif self.logger.filter_var.get() == "all" or self.logger.filter_var.get() == "info":
                        self.logger.logs_text.insert(tk.END, line, "info")
        except FileNotFoundError:
            self.logger.logs_text.insert(tk.END, "Лог-файл не найден.\n", "warning")
        except UnicodeDecodeError as e:
            self.logger.logs_text.insert(tk.END, f"Ошибка декодирования файла логов: {e}\n", "error")
        self.logger.logs_text.configure(state='disabled')
        self.logger.logs_text.see(tk.END)

    def auto_update_logs(self):
        if hasattr(self, 'logs_window') and self.logs_window.winfo_exists():
            self.update_logs()
            self.auto_update_id = self.root.after(5000, self.auto_update_logs)

    def start_move(self, event, window):
        self.x = event.x
        self.y = event.y
        self.moving_window = window

    def do_move(self, event, window):
        if self.moving_window == window:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = window.winfo_x() + deltax
            y = window.winfo_y() + deltay
            window.geometry(f'+{x}+{y}')

    def stop_move(self, event, window):
        self.x = None
        self.y = None
        self.moving_window = None

    def start_move_logs(self, event):
        self.logs_x = event.x
        self.logs_y = event.y

    def stop_move_logs(self, event):
        self.logs_x = None
        self.logs_y = None

    def do_move_logs(self, event):
        if self.logs_x is not None and self.logs_y is not None:
            deltax = event.x - self.logs_x
            deltay = event.y - self.logs_y
            x = self.logs_window.winfo_x() + deltax
            y = self.logs_window.winfo_y() + deltay
            self.logs_window.geometry(f"+{x}+{y}")

    def find_image(self, image_name):
        with mss.mss() as sct:
            monitor = {
                "left": self.game_left,
                "top": self.game_top,
                "width": self.game_width,
                "height": self.game_height
            }
            screenshot = np.array(sct.grab(monitor))
            screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            template = self.templates.get(image_name)
            if template is not None:
                result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > 0.7:
                    center_x = self.game_left + max_loc[0] + template.shape[1] // 2
                    center_y = self.game_top + max_loc[1] + template.shape[0] // 2  
                    return (center_x, center_y)
        return None

    def run(self):
        self.root.mainloop()

    def safe_destroy(self, window):
        try:
            if window.winfo_exists():
                window.destroy()
        except tk.TclError:
            pass  

    def exit_gracefully(self):
        self.exiting = True
        
        if self.save_timer:
            try:
                self.root.after_cancel(self.save_timer)
            except ValueError:
                pass
        
        if hasattr(self, 'auto_update_id'):
            try:
                self.root.after_cancel(self.auto_update_id)
            except tk.TclError:
                pass
        
        self.fade_out(self.final_cleanup)

    def final_cleanup(self):
        for bot in self.bots.values():
            if hasattr(bot, 'stop_bot'):
                bot.stop_bot()
        if self.config["General"].getboolean("AutoSaveOnExit"):
            threading.Thread(target=self.save_settings, daemon=True).start()
        self.safe_destroy(self.root)

    def reset_antiafk_coords(self):
        antiafk_bot = self.bots['antiafk']
        antiafk_bot.lottery_app_coords = None
        antiafk_bot.lottery_buy_coords = None
        antiafk_bot.casino_app_coords = None
        antiafk_bot.spin_button_coords = None
        for key in ["LotteryAppX", "LotteryAppY", "LotteryBuyX", "LotteryBuyY", "CasinoAppX", "CasinoAppY", "SpinButtonX", "SpinButtonY"]:
            if key in self.config["AntiAfk"]:
                del self.config["AntiAfk"][key]
        with open(os.path.join(self.sniker_lite_path, "sniker_settings.ini"), "w", encoding='utf-8') as f:
            self.config.write(f)
        messagebox.showinfo("Информация", "Координаты Anti-AFK сброшены")

    def final_cleanup(self):
        
        for bot in self.bots.values():
            if hasattr(bot, 'stop_bot'):
                bot.stop_bot()
        
        if self.config["General"].getboolean("AutoSaveOnExit"):
            self.save_settings()
        
        self.safe_destroy(self.root)
         
class PortBot:
    def __init__(self, app):
        self.app = app
        self.frame = self.app.bot_frames['port']
        self.box_count = 0
        self.anesthetic_count = 0
        self.money_count = 0
        self.timer_value = 0
        self.active = False
        self.script_active = False
        self.timer_running = False
        self.anesthetic_cooldown = False
        self.box_reward = int(self.app.config["Port"].get("BoxReward", "132"))
        self.auto_run = self.app.config["General"].getboolean("AutoRun")
        self.game_left = self.app.game_left
        self.game_top = self.app.game_top
        self.game_width = self.app.game_width
        self.game_height = self.app.game_height
        self.scale_x = self.app.scale_x
        self.scale_y = self.app.scale_y
        self.first_run = not self.app.config.has_section("PortSettings")

        if not self.first_run:
            self.check_x_base = float(self.app.config["PortSettings"].get("CheckX", "950.0"))
            self.check_y_base = float(self.app.config["PortSettings"].get("CheckY", "480.0"))
            self.anesthetic_area = {
                "left": int(self.app.config["PortSettings"].get("AnestheticLeft", "630")),
                "top": int(self.app.config["PortSettings"].get("AnestheticTop", "900")),
                "width": int(self.app.config["PortSettings"].get("AnestheticWidth", "500")),
                "height": int(self.app.config["PortSettings"].get("AnestheticHeight", "600"))
            }
        else:
            self.check_x_base = 950.0
            self.check_y_base = 480.0
            self.anesthetic_area = {"left": 630, "top": 900, "width": 500, "height": 600}

        self.setup_gui()
        self.start_threads()

    def setup_gui(self):
        stats_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        stats_frame.pack(pady=5, fill=tk.X)

        self.status_label = tk.Label(stats_frame, text="Статус: Неактивен", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                    font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.status_label.pack(anchor=tk.W)

        self.box_count_text = tk.Label(stats_frame, text="Ящики: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                    font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.box_count_text.pack(anchor=tk.W)

        self.heads_count_text = tk.Label(stats_frame, text="Обезболы: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                        font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.heads_count_text.pack(anchor=tk.W)

        self.money_count_text = tk.Label(stats_frame, text="Деньги: 0$", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                        font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.money_count_text.pack(anchor=tk.W)

        self.timer_text = tk.Label(stats_frame, text="Время: 00:00:00", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.timer_text.pack(anchor=tk.W)

        control_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        control_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        control_text = tk.Text(control_frame, wrap=tk.WORD, height=6, width=35, bd=0, bg=TEXT_BG_COLOR,
                               fg=TEXT_FG_COLOR, font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        control_text.config(cursor="arrow", selectbackground=control_text.cget("bg"),
                            selectforeground=control_text.cget("fg"))
        control_text.pack()
        self.app.control_texts['port'] = control_text  

        self.reconfigure_button = ttk.Button(self.frame, text="Перенастроить", command=self.show_setup_wizard)
        self.reconfigure_button.pack(pady=5)
        self.stats_labels = [
            self.box_count_text,
            self.heads_count_text,
            self.money_count_text,
            self.timer_text
        ]

    def show_setup_wizard(self):
        if self.app.current_setup_window and self.app.current_setup_window.winfo_exists():
            self.app.show_error("Информация", "Уже открыто окно настроек. Закройте его, чтобы открыть новое.")
            return
        self.setup_window = tk.Toplevel(self.app.root)
        self.setup_window.overrideredirect(True)
        self.setup_window.attributes("-topmost", True)
        self.setup_window.configure(bg=BACKGROUND_COLOR)
        self.setup_window.geometry("300x400+10+10")
        self.app.add_resize_handle(self.setup_window)

        title_bar = tk.Frame(self.setup_window, bg=BUTTON_COLOR, bd=0, highlightthickness=0)
        title_bar.pack(fill=tk.X, padx=0, pady=0)
        tk.Label(title_bar, text="Настройки бота", bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                 font=('Roboto', self.app.get_scaled_font_size(10), 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(title_bar, text="X", command=self.setup_window.destroy, bg=BUTTON_COLOR,
                  fg=HEADER_TEXT_COLOR, font=('Roboto', self.app.get_scaled_font_size(10), 'bold'),
                  relief='flat', bd=0, activebackground=ACTIVE_BUTTON_COLOR,
                  activeforeground=HEADER_TEXT_COLOR).pack(side=tk.RIGHT, padx=2, pady=2)

        self.content_frame = tk.Frame(self.setup_window, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.step = 1
        self.show_step_1()

        title_bar.bind('<ButtonPress-1>', self.start_move_setup)
        title_bar.bind('<B1-Motion>', self.do_move_setup)
        self.app.current_setup_window = self.setup_window
        self.setup_window.protocol("WM_DELETE_WINDOW", lambda: self.app.on_setup_window_close(self.setup_window))

    def show_step_1(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(self.content_frame, text="Настройка проверки ящиков", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                 font=('Roboto', self.app.get_scaled_font_size(12), 'bold')).pack(pady=5)
        tk.Label(self.content_frame,
                 text="Отнесите один ящик, как появится мини-игра, нажмите F2 и наведите курсор чуть правее красной полоски, затем нажмите Enter.",
                 wraplength=280, bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                 font=('Roboto', self.app.get_scaled_font_size(10), 'bold')).pack(pady=10)

        img_path = get_resource_path('images/porthelp.jpg')
        try:
            img = Image.open(img_path)
            photo = ImageTk.PhotoImage(img)
            self.img_label = tk.Label(self.content_frame, image=photo, bg=BACKGROUND_COLOR)
            self.img_label.image = photo
            self.img_label.pack(pady=10)
        except Exception as e:
            self.app.logger.log("Port", f"Ошибка загрузки porthelp.jpg: {e}", "error")

        def on_enter_press(key):
            if key == pynput_keyboard.Key.enter:
                x, y = pyautogui.position()
                self.check_x_base = (x - self.app.game_left) / self.scale_x
                self.check_y_base = (y - self.app.game_top) / self.scale_y
                self.app.config["PortSettings"] = {
                    "CheckX": str(self.check_x_base),
                    "CheckY": str(self.check_y_base)
                }
                self.show_step_2()
                return False

        listener = pynput_keyboard.Listener(on_press=on_enter_press)
        listener.start()

    def show_step_2(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(self.content_frame, text="Настройка обезболов", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                 font=('Roboto', self.app.get_scaled_font_size(12), 'bold')).pack(pady=5)
        tk.Label(self.content_frame,
                 text="Успешно положите ящик, чтобы появилась надпись 'Успешно'. Это определит область поиска обезболов.",
                 wraplength=280, bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                 font=('Roboto', self.app.get_scaled_font_size(10), 'bold')).pack(pady=10)

        self.search_for_done_image()

    def start_move_setup(self, event):
        self._x = event.x
        self._y = event.y

    def do_move_setup(self, event):
        if self._x is not None and self._y is not None:
            deltax = event.x - self._x
            deltay = event.y - self._y
            x = self.setup_window.winfo_x() + deltax
            y = self.setup_window.winfo_y() + deltay
            self.setup_window.geometry(f"+{x}+{y}")

    def search_for_done_image(self):
        done_template = cv2.imread(get_resource_path('images/done.jpg'))
        if done_template is None:
            self.app.logger.log("Port", "Ошибка: не удалось загрузить done.jpg", "error")
            tk.Label(self.content_frame, text="Ошибка: не удалось загрузить done.jpg.", bg=LABEL_BG_COLOR,
                     fg=LABEL_FG_COLOR, font=('Roboto', self.app.get_scaled_font_size(10), 'bold')).pack(pady=10)
            return

        status_label = tk.Label(self.content_frame, text="Идет поиск...", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        status_label.pack(pady=10)

        def search():
            start_time = time.time()
            search_duration = 300
            while time.time() - start_time < search_duration and self.setup_window.winfo_exists():
                with mss.mss() as sct:
                    monitor = {
                        "left": self.app.game_left,
                        "top": self.app.game_top,
                        "width": self.app.game_width,
                        "height": self.app.game_height
                    }
                    screenshot = np.array(sct.grab(monitor))
                    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                    result = cv2.matchTemplate(screenshot_bgr, done_template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    if max_val > 0.7:
                        top_left = max_loc
                        h, w = done_template.shape[:2]
                        center_x = top_left[0] + w // 2
                        center_y = top_left[1] + h // 2
                        left = max(center_x - 100, 0)
                        top = max(center_y - 100, 0)
                        right = min(center_x + 100, screenshot.shape[1])
                        bottom = min(center_y + 100, screenshot.shape[0])
                        self.anesthetic_area = {
                            "left": left,
                            "top": top,
                            "width": right - left,
                            "height": bottom - top
                        }
                        self.app.config["PortSettings"]["AnestheticLeft"] = str(left)
                        self.app.config["PortSettings"]["AnestheticTop"] = str(top)
                        self.app.config["PortSettings"]["AnestheticWidth"] = str(right - left)
                        self.app.config["PortSettings"]["AnestheticHeight"] = str(bottom - top)
                        with open(os.path.join(self.app.sniker_lite_path, "sniker_settings.ini"), "w") as f:
                            self.app.config.write(f)
                        status_label.config(text="Успешно! Настройка завершена.")
                        self.setup_window.after(3000, self.setup_window.destroy)
                        self.first_run = False
                        self.start_bot()
                        return
                time.sleep(0.5)
            status_label.config(text="Не удалось найти done.jpg. Попробуйте снова.")

        threading.Thread(target=search, daemon=True).start()

    def toggle_bot(self):
        if self.active:
            self.stop_bot()  
            self.status_label.config(text="Статус: Неактивен")
            self.active = False
        else:
            self.start_bot()  
            self.status_label.config(text="Статус: Активен")
            self.active = True

    def start_bot(self):
        self.script_active = True
        self.timer_running = True
        if self.auto_run:
            controller = KeyboardController()
            controller.press(pynput_keyboard.KeyCode.from_vk(0x57))  
            controller.press(Key.shift)  
        self.app.logger.log("Port", "Бот запущен (f5)")

    def stop_bot(self):
        self.script_active = False
        self.timer_running = False
        if self.auto_run:
            controller = KeyboardController()
            controller.release(pynput_keyboard.KeyCode.from_vk(0x57))  
            controller.release(Key.shift)

    def pixel_search_loop(self):
        while True:
            if self.script_active:
                self.check_boxes()
                self.check_anesthetics()
            time.sleep(0.001)

    def check_boxes(self):
        if not self.script_active:
            return
        hdc = user32.GetDC(0)
        x = int(self.app.game_left + self.check_x_base * self.scale_x)
        y = int(self.app.game_top + self.check_y_base * self.scale_y)
        pixel_color = gdi32.GetPixel(hdc, x, y)
        user32.ReleaseDC(0, hdc)
        blue = pixel_color & 0xff
        green = (pixel_color >> 8) & 0xff
        red = (pixel_color >> 16) & 0xff
        if (120 <= blue <= 130) and (205 <= green <= 215) and (30 <= red <= 35):
            self.app.logger.log("Port", "Пиксель найден")
            self.press_e()
            time.sleep(0.05)

    def press_e(self):
        controller = KeyboardController()
        controller.press(pynput_keyboard.KeyCode.from_vk(0x45))  
        controller.release(pynput_keyboard.KeyCode.from_vk(0x45))
        self.box_count += 1
        self.money_count += self.box_reward
        self.update_labels()
        start_time = time.time()
        while time.time() - start_time < 0.5:
            if not self.script_active:
                break
            time.sleep(0.01)

    def check_anesthetics(self):
        if self.anesthetic_cooldown:
            return
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(self.anesthetic_area))
            screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            template_aneth = self.app.templates['aneth']
            result = cv2.matchTemplate(screenshot_bgr, template_aneth, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.7:
                self.anesthetic_count += 1
                self.anesthetic_cooldown = True
                threading.Timer(15.0, self.reset_anesthetic_cooldown).start()
                self.update_labels()

    def reset_anesthetic_cooldown(self):
        self.anesthetic_cooldown = False

    def timer_loop(self):
        while True:
            if self.timer_running:
                self.timer_value += 1
                self.update_labels()
            time.sleep(1)

    def update_labels(self):
        def update():
            hours = self.timer_value // 3600
            minutes = (self.timer_value % 3600) // 60
            seconds = self.timer_value % 60
            self.box_count_text.config(text=f"Ящики: {self.box_count}")
            self.heads_count_text.config(text=f"Обезболы: {self.anesthetic_count}")
            self.money_count_text.config(text=f"Деньги: {self.money_count}$")
            self.timer_text.config(text=f"Время: {hours:02}:{minutes:02}:{seconds:02}")
        self.app.root.after(0, update)

    def start_threads(self):
        threading.Thread(target=self.pixel_search_loop, daemon=True).start()
        threading.Thread(target=self.timer_loop, daemon=True).start()

    def reset_stats(self):
        self.box_count = 0
        self.anesthetic_count = 0
        self.money_count = 0
        self.timer_value = 0
        self.update_labels()
        self.app.logger.log("Port", "Статистика сброшена (F9)")

class BuildingBot:
    def __init__(self, app):
        self.app = app
        self.frame = self.app.bot_frames['building']
        self.action_count = 0
        self.anesthetic_count = 0
        self.money_count = 0
        self.timer_value = 0
        self.active = False
        self.script_active = False
        self.timer_running = False
        self.anesthetic_cooldown = False
        self.action_reward = int(self.app.config["Building"]["ActionReward"]) if "Building" in self.app.config else 10
        self.auto_run = self.app.config["General"].getboolean("AutoRun")
        self.game_left = self.app.game_left
        self.game_top = self.app.game_top
        self.game_width = self.app.game_width
        self.game_height = self.app.game_height
        self.scale_x = self.app.scale_x
        self.scale_y = self.app.scale_y
        self.first_run = not self.app.config.has_section("BuildingSettings")
        if not self.first_run:
            self.search_area = {
                "left": int(self.app.config["BuildingSettings"].get("SearchLeft", "740")),
                "top": int(self.app.config["BuildingSettings"].get("SearchTop", "400")),
                "width": int(self.app.config["BuildingSettings"].get("SearchWidth", "450")),
                "height": int(self.app.config["BuildingSettings"].get("SearchHeight", "450"))
            }
            self.anesthetic_area = {
                "left": int(self.app.config["BuildingSettings"].get("AnestheticLeft", "630")),
                "top": int(self.app.config["BuildingSettings"].get("AnestheticTop", "900")),
                "width": int(self.app.config["BuildingSettings"].get("AnestheticWidth", "500")),
                "height": int(self.app.config["BuildingSettings"].get("AnestheticHeight", "600"))
            }
        else:
            self.search_area = {"left": 740, "top": 400, "width": 450, "height": 450}
            self.anesthetic_area = {"left": 630, "top": 900, "width": 500, "height": 600}
        self.thresholds = {'E': 0.95, 'F': 0.6, 'Y': 0.7}
        self.setup_gui()
        self.start_threads()

    def setup_gui(self):
        stats_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        stats_frame.pack(pady=5, fill=tk.X)

        self.status_label = tk.Label(stats_frame, text="Статус: Неактивен", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                    font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.status_label.pack(anchor=tk.W)

        self.action_count_text = tk.Label(stats_frame, text="Действия: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                        font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.action_count_text.pack(anchor=tk.W)

        self.heads_count_text = tk.Label(stats_frame, text="Обезболы: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                        font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.heads_count_text.pack(anchor=tk.W)

        self.money_count_text = tk.Label(stats_frame, text="Деньги: 0$", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                        font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.money_count_text.pack(anchor=tk.W)

        self.timer_text = tk.Label(stats_frame, text="Время: 00:00:00", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.timer_text.pack(anchor=tk.W)

        control_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        control_frame.pack(anchor=tk.W, expand=True, pady=5)
        control_text = tk.Text(control_frame, wrap=tk.WORD, height=6, width=35, bd=0, bg=TEXT_BG_COLOR,
                               fg=TEXT_FG_COLOR, font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        control_text.configure(state='disabled')
        control_text.config(cursor="arrow", selectbackground=control_text.cget("bg"),
                            selectforeground=control_text.cget("fg"))
        control_text.pack()
        self.app.control_texts['building'] = control_text  

        self.reconfigure_button = ttk.Button(self.frame, text="Перенастроить", command=self.show_setup_window)
        self.reconfigure_button.pack(pady=5)
        self.stats_labels = [
            self.action_count_text,
            self.heads_count_text,
            self.money_count_text,
            self.timer_text
        ]

    def show_setup_window(self):
        setup_window = tk.Toplevel(self.app.root)
        setup_window.overrideredirect(True)
        setup_window.attributes("-topmost", True)
        setup_window.configure(bg=BACKGROUND_COLOR)
        setup_window.geometry("300x200+10+10")

        title_bar = tk.Frame(setup_window, bg=BUTTON_COLOR, bd=0, highlightthickness=0)
        title_bar.pack(fill=tk.X)
        font_size = self.app.get_scaled_font_size(10)
        title_label = tk.Label(title_bar, text="Настройка бота Стройка", bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                               font=('Roboto', font_size, 'bold'))
        title_label.pack(side=tk.LEFT, padx=5)
        close_button = tk.Button(title_bar, text="X", command=setup_window.destroy, bg=BUTTON_COLOR,
                                 fg=HEADER_TEXT_COLOR, font=('Roboto', font_size - 1, 'bold'), relief='flat')
        close_button.pack(side=tk.RIGHT, padx=2)

        content_frame = tk.Frame(setup_window, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        instruction_label = tk.Label(content_frame,
                                     text="Начните действие на стройке и успешно выполните его.",
                                     wraplength=280, bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', font_size, 'bold'))
        instruction_label.pack(pady=5)
        status_label = tk.Label(content_frame, text="Ожидание...", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                font=('Roboto', font_size, 'bold'))
        status_label.pack(pady=5)

        def search_for_images():
            images = ['Y', 'F', 'E']
            found = False
            while not found and setup_window.winfo_exists():
                for img in images:
                    pos = self.app.find_image(img)
                    if pos:
                        left = max(pos[0] - 100, self.app.game_left)
                        top = max(pos[1] - 100, self.app.game_top)
                        right = min(pos[0] + 100, self.app.game_left + self.app.game_width)
                        bottom = min(pos[1] + 100, self.app.game_top + self.app.game_height)
                        self.search_area = {'left': left, 'top': top, 'width': right - left, 'height': bottom - top}
                        self.app.config["BuildingSettings"] = {
                            "SearchLeft": str(left),
                            "SearchTop": str(top),
                            "SearchWidth": str(right - left),
                            "SearchHeight": str(bottom - top)
                        }
                        status_label.config(text="Успешно!")
                        found = True
                        break
                time.sleep(1)

            if found:
                done_label = tk.Label(content_frame,
                                      text="Ищу обезболы... Выполните успешно одно действие на стройке.",
                                      bg=LABEL_BG_COLOR, wraplength=280, fg=LABEL_FG_COLOR,
                                      font=('Roboto', font_size, 'bold'))
                done_label.pack(pady=5)
                found_done = False
                while not found_done and setup_window.winfo_exists():
                    pos = self.app.find_image('done')
                    if pos:
                        left = max(pos[0] - 100, self.app.game_left)
                        top = max(pos[1] - 100, self.app.game_top)
                        right = min(pos[0] + 100, self.app.game_left + self.app.game_width)
                        bottom = min(pos[1] + 100, self.app.game_top + self.app.game_height)
                        self.anesthetic_area = {'left': left, 'top': top, 'width': right - left,
                                                'height': bottom - top}
                        self.app.config["BuildingSettings"]["AnestheticLeft"] = str(left)
                        self.app.config["BuildingSettings"]["AnestheticTop"] = str(top)
                        self.app.config["BuildingSettings"]["AnestheticWidth"] = str(right - left)
                        self.app.config["BuildingSettings"]["AnestheticHeight"] = str(bottom - top)
                        with open(os.path.join(self.app.sniker_lite_path, "sniker_settings.ini"), "w") as f:
                            self.app.config.write(f)
                        done_label.config(text="Успешно!")
                        self.first_run = False
                        setup_window.after(3000, setup_window.destroy)
                        found_done = True
                    time.sleep(1)

        threading.Thread(target=search_for_images, daemon=True).start()

    def toggle_bot(self):
        if self.active:
            self.stop_bot()  
            self.status_label.config(text="Статус: Неактивен")
            self.active = False
        else:
            self.start_bot()  
            self.status_label.config(text="Статус: Активен")
            self.active = True

    def start_bot(self):
        self.script_active = True
        self.timer_running = True
        if self.auto_run:
            controller = KeyboardController()
            controller.press(pynput_keyboard.KeyCode.from_vk(0x57))  
            controller.press(Key.shift)
        self.app.logger.log("Building", "Бот запущен (f5)")

    def stop_bot(self):
        self.script_active = False
        self.timer_running = False
        if self.auto_run:
            controller = KeyboardController()
            controller.release(pynput_keyboard.KeyCode.from_vk(0x57))  
            controller.release(Key.shift)

    def pixel_search_loop(self):
        while True:
            if self.script_active:
                self.check_actions()
                self.check_anesthetics()
            time.sleep(0.1)

    def check_actions(self):
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(self.search_area))
            gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
            for key in ['E', 'F', 'H']:
                if not self.script_active:
                    return
                template = self.app.templates[key]
                gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray_screenshot, gray_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > self.thresholds[key]:
                    self.app.logger.log("Building", f"Найдено {key}, нажимаю клавишу")
                    self.action_count += 1
                    self.money_count += self.action_reward
                    controller = KeyboardController()
                    vk_code = {'E': 0x45, 'F': 0x46, 'H': 0x48}[key]
                    for i in range(40):
                        if not self.script_active:
                            break
                        controller.press(pynput_keyboard.KeyCode.from_vk(vk_code))
                        time.sleep(0.03)
                        controller.release(pynput_keyboard.KeyCode.from_vk(vk_code))
                        time.sleep(random.uniform(0.05, 0.1))
                    self.update_labels()
                    time.sleep(0.5)
                    break

    def check_anesthetics(self):
        if self.anesthetic_cooldown:
            return
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(self.anesthetic_area))
            screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            template_aneth = self.app.templates['aneth']
            result = cv2.matchTemplate(screenshot_bgr, template_aneth, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.7:
                self.anesthetic_count += 1
                self.anesthetic_cooldown = True
                threading.Timer(15.0, self.reset_anesthetic_cooldown).start()
                self.update_labels()

    def reset_anesthetic_cooldown(self):
        self.anesthetic_cooldown = False

    def timer_loop(self):
        while True:
            if self.timer_running:
                self.timer_value += 1
                self.update_labels()
            time.sleep(1)

    def update_labels(self):
        def update():
            hours = self.timer_value // 3600
            minutes = (self.timer_value % 3600) // 60
            seconds = self.timer_value % 60
            self.action_count_text.config(text=f"Действия: {self.action_count}")
            self.heads_count_text.config(text=f"Обезболы: {self.anesthetic_count}")
            self.money_count_text.config(text=f"Деньги: {self.money_count}$")
            self.timer_text.config(text=f"Время: {hours:02}:{minutes:02}:{seconds:02}")
        self.app.root.after(0, update)

    def start_threads(self):
        threading.Thread(target=self.pixel_search_loop, daemon=True).start()
        threading.Thread(target=self.timer_loop, daemon=True).start()

    def reset_stats(self):
        self.action_count = 0
        self.anesthetic_count = 0
        self.money_count = 0
        self.timer_value = 0
        self.update_labels()
        self.app.logger.log("Building", "Статистика сброшена (F9)")
                   
class MineBot:
    def __init__(self, app):
        self.app = app
        self.frame = self.app.bot_frames['mine']
        self.action_count = 0
        self.anesthetic_count = 0
        self.money_count = 0
        self.timer_value = 0
        self.active = False
        self.script_active = False
        self.timer_running = False
        self.anesthetic_cooldown = False
        self.action_reward = int(self.app.config["Mine"]["ActionReward"]) if "Mine" in self.app.config else 5
        self.auto_run = self.app.config["General"].getboolean("AutoRun")
        self.game_left = self.app.game_left
        self.game_top = self.app.game_top
        self.game_width = self.app.game_width
        self.game_height = self.app.game_height
        self.scale_x = self.app.scale_x
        self.scale_y = self.app.scale_y
        self.first_run = not self.app.config.has_section("MineSettings")
        if not self.first_run:
            self.search_area = {
                "left": int(self.app.config["MineSettings"].get("SearchLeft", "740")),
                "top": int(self.app.config["MineSettings"].get("SearchTop", "400")),
                "width": int(self.app.config["MineSettings"].get("SearchWidth", "450")),
                "height": int(self.app.config["MineSettings"].get("SearchHeight", "450"))
            }
            self.anesthetic_area = {
                "left": int(self.app.config["MineSettings"].get("AnestheticLeft", "630")),
                "top": int(self.app.config["MineSettings"].get("AnestheticTop", "900")),
                "width": int(self.app.config["MineSettings"].get("AnestheticWidth", "500")),
                "height": int(self.app.config["MineSettings"].get("AnestheticHeight", "600"))
            }
        else:
            self.search_area = {"left": 740, "top": 400, "width": 450, "height": 450}
            self.anesthetic_area = {"left": 630, "top": 900, "width": 500, "height": 600}
        self.threshold = 0.95
        self.setup_gui()
        self.start_threads()

    def setup_gui(self):
        stats_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        stats_frame.pack(pady=5, fill=tk.X)

        self.status_label = tk.Label(stats_frame, text="Статус: Неактивен", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                    font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.status_label.pack(anchor=tk.W)

        self.action_count_text = tk.Label(stats_frame, text="Камни: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                        font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.action_count_text.pack(anchor=tk.W)

        self.heads_count_text = tk.Label(stats_frame, text="Обезболы: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                        font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.heads_count_text.pack(anchor=tk.W)

        self.money_count_text = tk.Label(stats_frame, text="Деньги: 0$", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                        font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.money_count_text.pack(anchor=tk.W)

        self.timer_text = tk.Label(stats_frame, text="Время: 00:00:00", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.timer_text.pack(anchor=tk.W)

        control_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        control_frame.pack(anchor=tk.W, expand=True, pady=5)
        control_text = tk.Text(control_frame, wrap=tk.WORD, height=6, width=35, bd=0, bg=TEXT_BG_COLOR,
                               fg=TEXT_FG_COLOR, font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        control_text.configure(state='disabled')
        control_text.config(cursor="arrow", selectbackground=control_text.cget("bg"),
                            selectforeground=control_text.cget("fg"))
        control_text.pack()
        self.app.control_texts['mine'] = control_text  

        self.reconfigure_button = ttk.Button(self.frame, text="Перенастроить", command=self.show_setup_window)
        self.reconfigure_button.pack(pady=5)
        
        self.stats_labels = [
            self.action_count_text,
            self.heads_count_text,
            self.money_count_text,
            self.timer_text
        ]

    def show_setup_window(self):
        if self.app.current_setup_window and self.app.current_setup_window.winfo_exists():
            messagebox.showinfo("Информация", "Уже открыто окно настроек. Закройте его, чтобы открыть новое.")
            return
        setup_window = tk.Toplevel(self.app.root)
        setup_window.overrideredirect(True)
        setup_window.attributes("-topmost", True)
        setup_window.configure(bg=BACKGROUND_COLOR)
        setup_window.geometry("400x450+10+10")

        title_bar = tk.Frame(setup_window, bg=BUTTON_COLOR, bd=0, highlightthickness=0)
        title_bar.pack(fill=tk.X)
        font_size = self.app.get_scaled_font_size(10)
        title_label = tk.Label(title_bar, text="Настройка бота Шахта", bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                               font=('Roboto', font_size, 'bold'))
        title_label.pack(side=tk.LEFT, padx=5)
        close_button = tk.Button(title_bar, text="X", command=setup_window.destroy, bg=BUTTON_COLOR,
                                 fg=HEADER_TEXT_COLOR, font=('Roboto', font_size - 1, 'bold'), relief='flat')
        close_button.pack(side=tk.RIGHT, padx=2)

        content_frame = tk.Frame(setup_window, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        instruction_label = tk.Label(content_frame,
                                     text="Начните действие в шахте и успешно выполните его, а после закончите работу у бота и получите деньги.",
                                     wraplength=280, bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', font_size, 'bold'))
        instruction_label.pack(pady=5)
        status_label = tk.Label(content_frame, text="Ожидание...", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                font=('Roboto', font_size, 'bold'))
        status_label.pack(pady=5)

        def search_for_images():
            found = False
            while not found and setup_window.winfo_exists():
                pos = self.app.find_image('E')
                if pos:
                    left = max(pos[0] - 100, self.app.game_left)
                    top = max(pos[1] - 100, self.app.game_top)
                    right = min(pos[0] + 100, self.app.game_left + self.app.game_width)
                    bottom = min(pos[1] + 100, self.app.game_top + self.app.game_height)
                    self.search_area = {'left': left, 'top': top, 'width': right - left, 'height': bottom - top}
                    self.app.config["MineSettings"] = {
                        "SearchLeft": str(left),
                        "SearchTop": str(top),
                        "SearchWidth": str(right - left),
                        "SearchHeight": str(bottom - top)
                    }
                    status_label.config(text="Успешно!")
                    found = True
                time.sleep(1)

            if found:
                done_label = tk.Label(content_frame,
                                      text="Ищу обезболы... Завершите работу в шахте чтобы вам заплатили.",
                                      bg=LABEL_BG_COLOR, wraplength=280, fg=LABEL_FG_COLOR,
                                      font=('Roboto', font_size, 'bold'))
                done_label.pack(pady=5)
                found_done = False
                while not found_done and setup_window.winfo_exists():
                    pos = self.app.find_image('mony')
                    if pos:
                        left = max(pos[0] - 100, self.app.game_left)
                        top = max(pos[1] - 100, self.app.game_top)
                        right = min(pos[0] + 100, self.app.game_left + self.app.game_width)
                        bottom = min(pos[1] + 100, self.app.game_top + self.app.game_height)
                        self.anesthetic_area = {'left': left, 'top': top, 'width': right - left,
                                                'height': bottom - top}
                        self.app.config["MineSettings"]["AnestheticLeft"] = str(left)
                        self.app.config["MineSettings"]["AnestheticTop"] = str(top)
                        self.app.config["MineSettings"]["AnestheticWidth"] = str(right - left)
                        self.app.config["MineSettings"]["AnestheticHeight"] = str(bottom - top)
                        with open(os.path.join(self.app.sniker_lite_path, "sniker_settings.ini"), "w") as f:
                            self.app.config.write(f)
                        done_label.config(text="Успешно!")
                        self.first_run = False
                        setup_window.after(3000, setup_window.destroy)
                        found_done = True
                    time.sleep(1)

        threading.Thread(target=search_for_images, daemon=True).start()

    def toggle_bot(self):
        if self.active:
            self.stop_bot()  
            self.status_label.config(text="Статус: Неактивен")
            self.active = False
        else:
            self.start_bot()  
            self.status_label.config(text="Статус: Активен")
            self.active = True

    def start_bot(self):
        self.script_active = True
        self.timer_running = True
        if self.auto_run:
            controller = KeyboardController()
            controller.press(pynput_keyboard.KeyCode.from_vk(0x57))  
            controller.press(Key.shift)
        self.app.logger.log("Mine", "Бот запущен (f5)")

    def stop_bot(self):
        self.script_active = False
        self.timer_running = False
        if self.auto_run:
            controller = KeyboardController()
            controller.release(pynput_keyboard.KeyCode.from_vk(0x57))  
            controller.release(Key.shift)

    def pixel_search_loop(self):
        while True:
            if self.script_active:
                self.check_actions()
                self.check_anesthetics()
            time.sleep(0.1)

    def check_actions(self):
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(self.search_area))
            gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
            template_E = self.app.templates['E']
            gray_template_E = cv2.cvtColor(template_E, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray_screenshot, gray_template_E, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > self.threshold:
                self.action_count += 1
                self.money_count += self.action_reward
                controller = KeyboardController()
                for _ in range(40):
                    controller.press(pynput_keyboard.KeyCode.from_vk(0x45))  
                    time.sleep(0.02)
                    controller.release(pynput_keyboard.KeyCode.from_vk(0x45))
                    time.sleep(random.uniform(0.05, 0.1))
                self.update_labels()
                time.sleep(0.5)

    def check_anesthetics(self):
        if self.anesthetic_cooldown:
            return
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(self.anesthetic_area))
            screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            template_aneth = self.app.templates['aneth']
            result = cv2.matchTemplate(screenshot_bgr, template_aneth, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.7:
                self.anesthetic_count += 1
                self.anesthetic_cooldown = True
                threading.Timer(15.0, self.reset_anesthetic_cooldown).start()
                self.update_labels()

    def reset_anesthetic_cooldown(self):
        self.anesthetic_cooldown = False

    def timer_loop(self):
        while True:
            if self.timer_running:
                self.timer_value += 1
                self.update_labels()
            time.sleep(1)

    def update_labels(self):
        def update():
            hours = self.timer_value // 3600
            minutes = (self.timer_value % 3600) // 60
            seconds = self.timer_value % 60
            self.action_count_text.config(text=f"Камни: {self.action_count}")
            self.heads_count_text.config(text=f"Обезболы: {self.anesthetic_count}")
            self.money_count_text.config(text=f"Деньги: {self.money_count}$")
            self.timer_text.config(text=f"Время: {hours:02}:{minutes:02}:{seconds:02}")
        self.app.root.after(0, update)

    def start_threads(self):
        threading.Thread(target=self.pixel_search_loop, daemon=True).start()
        threading.Thread(target=self.timer_loop, daemon=True).start()

    def reset_stats(self):
        self.action_count = 0
        self.anesthetic_count = 0
        self.money_count = 0
        self.timer_value = 0
        self.update_labels()
        self.app.logger.log("Mine", "Статистика сброшена (F9)")

class FarmBot:
    def __init__(self, app):
        self.app = app
        self.frame = self.app.bot_frames['farm']
        self.script_active = False
        self.search_area = None
        self.templates = self.load_templates() 
        self.load_config()
        self.setup_gui()

    def load_templates(self):
        templates = {}
        for img in ['acow', 'dcow']:
            path = get_resource_path(f'images/{img}.jpg')
            template = cv2.imread(path, cv2.IMREAD_COLOR)
            if template is not None:
                templates[img] = template
            else:
                print(f"Ошибка: не удалось загрузить {img}.jpg")
        return templates

    def load_config(self):
        if "FarmSettings" in self.app.config:
            self.search_area = {
                "left": int(self.app.config["FarmSettings"].get("SearchLeft", 0)),
                "top": int(self.app.config["FarmSettings"].get("SearchTop", 0)),
                "width": int(self.app.config["FarmSettings"].get("SearchWidth", 1600)),
                "height": int(self.app.config["FarmSettings"].get("SearchHeight", 1600))
            }

    def save_config(self):
        if self.search_area:
            self.app.config["FarmSettings"] = {
                "SearchLeft": str(self.search_area["left"]),
                "SearchTop": str(self.search_area["top"]),
                "SearchWidth": str(self.search_area["width"]),
                "SearchHeight": str(self.search_area["height"])
            }
            with open(os.path.join(self.app.sniker_lite_path, "sniker_settings.ini"), "w") as f:
                self.app.config.write(f)

    def setup_gui(self):
        self.status_label = tk.Label(self.frame, text="Статус: Неактивен", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.status_label.pack(pady=5)
        control_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        control_frame.pack(anchor=tk.W, expand=True, pady=5)
        control_text = tk.Text(control_frame, wrap=tk.WORD, height=1, width=35, bd=0, bg=TEXT_BG_COLOR,
                               fg=TEXT_FG_COLOR, font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        control_text.configure(state='disabled')
        control_text.config(cursor="arrow", selectbackground=control_text.cget("bg"),
                            selectforeground=control_text.cget("fg"))
        control_text.pack()
        self.reconfigure_button = ttk.Button(self.frame, text="Перенастроить",
                                             command=self.show_setup_window)
        self.reconfigure_button.pack(pady=5)
        
        self.stats_labels = [
            self.status_label
        ]

    def show_setup_window(self):
        if self.app.current_setup_window and self.app.current_setup_window.winfo_exists():
            self.app.show_error("Информация", "Уже открыто окно настроек. Закройте его.")
            return
        setup_window = tk.Toplevel(self.app.root)
        setup_window.overrideredirect(True)
        setup_window.attributes("-topmost", True)
        setup_window.configure(bg=BACKGROUND_COLOR)
        setup_window.geometry("300x150+10+10")

        title_bar = tk.Frame(setup_window, bg=BUTTON_COLOR, bd=0, highlightthickness=0)
        title_bar.pack(fill=tk.X)
        font_size = self.app.get_scaled_font_size(10)
        title_label = tk.Label(title_bar, text="Настройка бота Ферма", bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                               font=('Roboto', font_size, 'bold'))
        title_label.pack(side=tk.LEFT, padx=5)
        close_button = tk.Button(title_bar, text="X", command=setup_window.destroy, bg=BUTTON_COLOR,
                                 fg=HEADER_TEXT_COLOR, font=('Roboto', font_size - 1, 'bold'), relief='flat')
        close_button.pack(side=tk.RIGHT, padx=2)

        content_frame = tk.Frame(setup_window, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        instruction_label = tk.Label(content_frame,
                                     text="Подойдите к корове и начните её доить.\nПоиск...",
                                     wraplength=280, bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', font_size))
        instruction_label.pack(pady=5)

        def search_for_cow():
            while setup_window.winfo_exists():
                for img in ['acow', 'dcow']:
                    pos = self.find_image(img)
                    if pos:
                        left = max(pos[0] - 800, self.app.game_left)
                        top = max(pos[1] - 800, self.app.game_top)
                        right = min(pos[0] + 800, self.app.game_left + self.app.game_width)
                        bottom = min(pos[1] + 800, self.app.game_top + self.app.game_height)
                        self.search_area = {'left': left, 'top': top,
                                            'width': right - left, 'height': bottom - top}
                        self.save_config()
                        instruction_label.config(text="Область поиска установлена!")
                        setup_window.after(3000, setup_window.destroy)
                        return
                time.sleep(0.5)

        threading.Thread(target=search_for_cow, daemon=True).start()
        self.app.current_setup_window = setup_window
        setup_window.protocol("WM_DELETE_WINDOW",
                              lambda: self.app.on_setup_window_close(setup_window))

    def find_image(self, image_name):
        with mss.mss() as sct:
            monitor = {"left": self.app.game_left, "top": self.app.game_top,
                       "width": self.app.game_width, "height": self.app.game_height}
            screenshot = np.array(sct.grab(monitor))
            screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            template = self.templates.get(image_name)
            if template is not None:
                result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > 0.7:
                    center_x = self.app.game_left + max_loc[0] + template.shape[1] // 2
                    center_y = self.app.game_top + max_loc[1] + template.shape[0] // 2
                    return (center_x, center_y)
        return None

    def toggle_bot(self):
        if self.script_active:
            self.stop_bot()
        else:
            if self.search_area is None:
                self.show_setup_window()
            else:
                self.start_bot()

    def start_bot(self):
        self.script_active = True
        self.status_label.config(text="Статус: Активен")
        threading.Thread(target=self.bot_loop, daemon=True).start()

    def stop_bot(self):
        self.script_active = False
        self.status_label.config(text="Статус: Неактивен")

    def bot_loop(self):
        controller = KeyboardController()
        while self.script_active:
            if self.search_area:
                with mss.mss() as sct:
                    screenshot = np.array(sct.grab(self.search_area))
                    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                    for img in ['acow', 'dcow']:
                        template = self.templates.get(img)
                        if template is not None:
                            result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
                            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                            if max_val > 0.99:
                                vk_code = 0x41 if img == 'acow' else 0x44  
                                controller.press(pynput_keyboard.KeyCode.from_vk(vk_code))
                                time.sleep(0.01)
                                controller.release(pynput_keyboard.KeyCode.from_vk(vk_code))
                                print(f"Найдено изображение: {img}.jpg, max_val: {max_val:.4f}")
                                break
            time.sleep(0.06)

class AntiAfkBot:
    def __init__(self, app):
        self.app = app
        self.frame = self.app.bot_frames['antiafk']
        self.lottery_count = 0
        self.roulette_count = 0
        self.payday_count = 0
        self.timer_value = 0
        self.bot_running = False
        self.lottery_app_coords = None
        self.last_payday_detection = 0
        self.next_lottery_time = 0
        self.roulette_cooldown = False
        self.reconnect_count = 0
        self.reconnect_stage = "Ожидание"
        self.last_reconnect_time = 0
        self.anti_afk_enabled = False
        self.lottery_enabled = False
        self.roulette_enabled = False
        self.auto_reconnect_enabled = False
        self.action_history = []
        self.schedule_id_counter = 0
        self.scheduled_actions = []
        self.is_reconnecting = False

        self.ACTION_MAP = {
            "лотерея": "buy_lottery",
            "рулетка": "spin_roulette",
            "payday": "check_payday",
            "реконнект": "reconnect",
        }
        self.ACTION_DISPLAY_MAP = {
            "buy_lottery": "купить лотерейку",
            "spin_roulette": "прокрут рулетки",
            "check_payday": "получить payday",
            "reconnect": "выполнить реконнект"
        }

        
        self.anti_afk_enabled = self.app.config["AntiAfk"].getboolean("AntiAfkEnabled", True)
        self.lottery_enabled = self.app.config["AntiAfk"].getboolean("LotteryEnabled", True)
        self.roulette_enabled = self.app.config["AntiAfk"].getboolean("RouletteEnabled", True)
        self.telegram_token = self.app.config["AntiAfk"].get("TelegramToken", "")
        self.animation_key = self.load_bind("AnimationKey", "k")
        self.take_out_phone_key = self.load_bind("TakeOutPhoneKey", "up")
        self.put_away_phone_key = self.load_bind("PutAwayPhoneKey", "backspace")
        self.chat_font_size = self.app.config["AntiAfk"].getint("ChatFontSize", 15)
        self.chat_font_var = tk.StringVar(value=str(self.chat_font_size))
        self.auto_reconnect_enabled = self.app.config["AntiAfk"].getboolean("AutoReconnect", False)
        self.password = self.app.config["AntiAfk"].get("Password", "")
        self.min_lottery_interval = self.app.config["AntiAfk"].getint("MinLotteryInterval", 30 * 60)
        self.max_lottery_interval = self.app.config["AntiAfk"].getint("MaxLotteryInterval", 40 * 60)
        self.reconnect_interval = self.app.config["AntiAfk"].getint("ReconnectInterval", 60)
        self.reconnect_check_interval = self.app.config.getint('AntiAfk', 'reconnect_check_interval', fallback=300)

        self.character_coords = (
            int(self.app.config["AntiAfk"]["CharacterX"]),
            int(self.app.config["AntiAfk"]["CharacterY"])
        ) if "CharacterX" in self.app.config["AntiAfk"] else None

        
        self.scale_x = self.app.scale_x
        self.scale_y = self.app.scale_y
        self.game_left = self.app.game_left
        self.game_top = self.app.game_top
        self.game_width = self.app.game_width
        self.game_height = self.app.game_height

        
        self.chat_id = None
        self.application = None
        self.loop = None
        self.thresholds = {'lottery': 0.6, 'buyticket': 0.5, 'bankkard': 0.7, 'cols': 0.7, 'cas': 0.6,
                   'spinbutton': 0.7, 'payday': 0.6, 'kasspin': 0.7, 'connection': 0.6}
        self.reconnect_timer = None

        self.setup_gui()
        self.load_payday_templates()
        self.load_reconnect_templates()
        if 'cas' not in self.app.templates:
            path = get_resource_path('images/cas.jpg')
            template = cv2.imread(path, cv2.IMREAD_COLOR)
            if template is not None:
                self.app.templates['cas'] = template
            else:
                self.app.logger.log("AntiAfk", "Не удалось загрузить cas.jpg", "error")
        if 'kasspin' not in self.app.templates:
            path = get_resource_path('images/kasspin.jpg')
            template = cv2.imread(path, cv2.IMREAD_COLOR)
            if template is not None:
                self.app.templates['kasspin'] = template
            else:
                self.app.logger.log("AntiAfk", "Не удалось загрузить kasspin.jpg", "error")
        if 'spinbutton' not in self.app.templates:
            path = get_resource_path('images/spinbutton.jpg')
            template = cv2.imread(path, cv2.IMREAD_COLOR)
            if template is not None:
                self.app.templates['spinbutton'] = template
            else:
                self.app.logger.log("AntiAfk", "Не удалось загрузить spinbutton.jpg", "error")
        if self.telegram_token:
            self.setup_telegram_bot()

    def load_bind(self, config_key, default):
        bind_str = self.app.config["AntiAfk"].get(config_key, default).lower()
        try:
            if bind_str in Key.__members__:
                return Key[bind_str]
            elif len(bind_str) == 1:
                return KeyCode.from_char(bind_str)
            else:
                self.app.logger.log("AntiAfk", f"Неизвестная клавиша: {bind_str}", "warning")
                return KeyCode.from_char(default)
        except Exception as e:
            self.app.logger.log("AntiAfk", f"Ошибка загрузки клавиши {config_key}: {e}", "error")
            return KeyCode.from_char(default)

    def load_payday_templates(self):
        self.payday_templates = {}
        for size in [15, 20, 25, 30]:
            path = get_resource_path(f'images/payday{size}.jpg')
            template = cv2.imread(path)
            if template is not None:
                self.payday_templates[f'payday{size}'] = template
            else:
                print(f"Ошибка: не удалось загрузить файл {path}")

    def load_reconnect_templates(self):
        for img in ['connection', 'ipserv', 'connect', 'connect2', 'passw', 'voit', 'pers', 'acep', 'finish']:
            path = get_resource_path(f'images/{img}.jpg')
            template = cv2.imread(path)
            if template is not None:
                self.app.templates[img] = template
            else:
                print(f"Ошибка: не удалось загрузить {img}.jpg")

    def setup_gui(self):
        stats_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        stats_frame.pack(pady=5, fill=tk.X)
        self.time_text = tk.Label(stats_frame, text="Время: 00:00:00", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                  font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.time_text.pack(anchor=tk.W, padx=10)
        self.roulette_text = tk.Label(stats_frame, text="Рулетки: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                      font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.roulette_text.pack(anchor=tk.W, padx=10)
        self.lottery_text = tk.Label(stats_frame, text="Лотерейки: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.lottery_text.pack(anchor=tk.W, padx=10)
        self.payday_text = tk.Label(stats_frame, text="Payday: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                    font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.payday_text.pack(anchor=tk.W, padx=10)

        control_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        control_frame.pack(anchor=tk.W, expand=True, pady=5)
        control_text = tk.Text(control_frame, wrap=tk.WORD, height=6, width=35, bd=0, bg=TEXT_BG_COLOR,
                               fg=TEXT_FG_COLOR, font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        control_text.configure(state='disabled')
        control_text.pack()
        self.app.control_texts['antiafk'] = control_text

        button_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        button_frame.pack(side=tk.BOTTOM, pady=5)
        self.telegram_button = tk.Button(button_frame, text="Вкл Telegram-бот", width=20,
                                         command=self.toggle_telegram_bot, bg=BUTTON_COLOR,
                                         fg=HEADER_TEXT_COLOR, font=('Roboto', 10, 'bold'),
                                         relief='flat', activebackground=ACTIVE_BUTTON_COLOR)
        self.telegram_button.pack(side=tk.LEFT)

        self.stats_labels = [self.roulette_text, self.payday_text, self.lottery_text, self.time_text]

    def setup_character_selection(self):
        if self.app.current_setup_window and self.app.current_setup_window.winfo_exists():
            self.app.show_error("Информация", "Уже открыто окно настроек. Закройте его.")
            return

        setup_window = tk.Toplevel(self.app.root)
        setup_window.overrideredirect(True)
        setup_window.attributes("-topmost", True)
        setup_window.configure(bg=BACKGROUND_COLOR)
        setup_window.geometry("300x150+10+10")
        self.app.add_resize_handle(setup_window)

        title_bar = tk.Frame(setup_window, bg=BUTTON_COLOR)
        title_bar.pack(fill=tk.X)
        font_size = self.app.get_scaled_font_size(10)
        title_label = tk.Label(title_bar, text="Настройка выбора персонажа", bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                               font=('Roboto', font_size, 'bold'))
        title_label.pack(side=tk.LEFT, padx=5)
        close_button = tk.Button(title_bar, text="X", command=lambda: on_window_close(), bg=BUTTON_COLOR,
                                 fg=HEADER_TEXT_COLOR, font=('Roboto', font_size - 1, 'bold'), relief='flat')
        close_button.pack(side=tk.RIGHT, padx=2)

        content_frame = tk.Frame(setup_window, bg=FRAME_BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        instruction_label = tk.Label(content_frame,
                                     text="Перейдите к экрану выбора персонажа, наведите курсор на область выбора и нажмите Enter",
                                     wraplength=280, bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', font_size))
        instruction_label.pack(pady=5)

        def on_enter_press(key):
            if key == Key.enter:
                x, y = pyautogui.position()
                self.character_coords = (x, y)
                self.app.config["AntiAfk"]["CharacterX"] = str(x)
                self.app.config["AntiAfk"]["CharacterY"] = str(y)
                with open(os.path.join(self.app.sniker_lite_path, "sniker_settings.ini"), "w") as f:
                    self.app.config.write(f)
                instruction_label.config(text="Координаты установлены успешно")
                setup_window.update()
                setup_window.after(3000, setup_window.destroy)
                listener.stop()
                return False

        def on_window_close():
            listener.stop()
            setup_window.destroy()

        listener = KeyboardListener(on_press=on_enter_press)
        listener.start()

        setup_window.protocol("WM_DELETE_WINDOW", on_window_close)
        self.app.current_setup_window = setup_window

    def cancel_setup(self, setup_window, parent_window):
        setup_window.destroy()
        parent_window.deiconify()

    def finish_setup(self, setup_window, parent_window):
        setup_window.destroy()
        parent_window.deiconify()

    def toggle_telegram_bot(self):
        if not self.telegram_token:
            return
        if not self.application:
            self.setup_telegram_bot()
            self.telegram_button.config(text="Выкл Telegram-бот")
        else:
            self.stop_telegram_bot()
            self.telegram_button.config(text="Вкл Telegram-бот")

    def setup_telegram_bot(self):
        if not self.application:
            
            self.application = (
                Application.builder()
                .token(self.telegram_token)
                .read_timeout(60)      
                .write_timeout(60)     
                .connect_timeout(30)  
                .build()
            )
            
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CallbackQueryHandler(self.handle_callback))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
            self.loop = asyncio.new_event_loop()
            threading.Thread(target=self.run_polling, daemon=True).start()

    def stop_telegram_bot(self):
        if self.application:
            asyncio.run_coroutine_threadsafe(self.application.shutdown(), self.loop)
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.application = None
        self.loop = None

    def run_polling(self):
        asyncio.set_event_loop(self.loop)
        try:
            self.application.run_polling(
                drop_pending_updates=True,  
                timeout=20  
            )
        except telegram.error.TimedOut as e:
            
            self.app.logger.log("AntiAfk", f"Ошибка TimedOut в run_polling: {e}", "warning")
            
            time.sleep(5)
            self.run_polling()  
        except Exception as e:
            self.app.logger.log("AntiAfk", f"Критическая ошибка в run_polling: {e}", "error")

    async def start_command(self, update, context):
        self.chat_id = update.message.chat_id
        main_menu = [
            [InlineKeyboardButton("🤖 Управление ботом", callback_data="control")],
            [InlineKeyboardButton("⚙️ Настройки", callback_data="features")],
            [InlineKeyboardButton("ℹ️ Информация", callback_data="info")],
            [InlineKeyboardButton("🛠️ Утилиты", callback_data="utils")],
            [InlineKeyboardButton("🔄 Принудительный реконект", callback_data="force_reconnect")]
        ]
        reply_markup = InlineKeyboardMarkup(main_menu)
        await update.message.reply_text("Бот для управления игровыми функциями. Выберите категорию:", reply_markup=reply_markup)

    async def handle_callback(self, update, context):
        query = update.callback_query
        try:
            await query.answer()
        except telegram.error.BadRequest as e:
            if "query is too old" in str(e).lower() or "query id is invalid" in str(e).lower():
                await context.bot.send_message(chat_id=query.message.chat_id, text="Действие устарело, попробуйте снова.")
                return
            else:
                raise

        data = query.data

        if data == "main_menu":
            main_menu = [
                [InlineKeyboardButton("🤖 Управление ботом", callback_data="control")],
                [InlineKeyboardButton("⚙️ Настройки", callback_data="features")],
                [InlineKeyboardButton("ℹ️ Информация", callback_data="info")],
                [InlineKeyboardButton("🛠️ Утилиты", callback_data="utils")],
                [InlineKeyboardButton("🔄 Принудительный реконект", callback_data="force_reconnect")]
            ]
            reply_markup = InlineKeyboardMarkup(main_menu)
            await query.edit_message_text("Выберите категорию:", reply_markup=reply_markup)

        elif data == "control":
            control_menu = [
                [InlineKeyboardButton("Вкл/Выкл 🤖", callback_data="toggle_bot")],
                [InlineKeyboardButton("Статус ℹ️", callback_data="status")],
                [InlineKeyboardButton("Назад", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(control_menu)
            await query.edit_message_text("Управление ботом:", reply_markup=reply_markup)

        elif data == "features":
            features_menu = [
                [InlineKeyboardButton("🎟️ Лотерейки", callback_data="lottery_menu")],
                [InlineKeyboardButton("🎰 Рулетки", callback_data="roulette_menu")],
                [InlineKeyboardButton("🕹️ Анти-AFK", callback_data="antiafk_menu")],
                [InlineKeyboardButton("🔄 Авто-реконнект", callback_data="toggle_reconnect")],
                [InlineKeyboardButton("Купить лотерейку", callback_data="force_buy_lottery")],
                [InlineKeyboardButton("Крутить рулетку", callback_data="force_spin_roulette")],
                [InlineKeyboardButton("Назад", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(features_menu)
            await query.edit_message_text("Настройки:", reply_markup=reply_markup)

        elif data == "info":
            info_menu = [
                [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
                [InlineKeyboardButton("🖥️ Ресурсы компьютера", callback_data="resources")],
                [InlineKeyboardButton("Назад", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(info_menu)
            await query.edit_message_text("Информация:", reply_markup=reply_markup)

        elif data == "utils":
            utils_menu = [
                [InlineKeyboardButton("🖼️ Скриншот", callback_data="screenshot")],
                [InlineKeyboardButton("🕒 Запланировать действие", callback_data="schedule")],
                [InlineKeyboardButton("📋 Список запланированных", callback_data="list_scheduled")],
                [InlineKeyboardButton("❌ Отменить действие", callback_data="cancel_schedule")],
                [InlineKeyboardButton("Назад", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(utils_menu)
            await query.edit_message_text("Утилиты:", reply_markup=reply_markup)

        elif data == "toggle_bot":
            self.toggle_bot()
            status_text = "Бот включен 🟢" if self.bot_running else "Бот выключен 🔴"
            await context.bot.send_message(chat_id=query.message.chat_id, text=status_text)

        elif data == "status":
            await self.status_command(update, context)

        elif data == "lottery_menu":
            lottery_menu = [
                [InlineKeyboardButton("Вкл/Выкл 🎟️", callback_data="toggle_lottery")],
                [InlineKeyboardButton("Назад", callback_data="features")]
            ]
            reply_markup = InlineKeyboardMarkup(lottery_menu)
            await query.edit_message_text("Лотерейки:", reply_markup=reply_markup)

        elif data == "roulette_menu":
            roulette_menu = [
                [InlineKeyboardButton("Вкл/Выкл 🎰", callback_data="toggle_roulette")],
                [InlineKeyboardButton("Назад", callback_data="features")]
            ]
            reply_markup = InlineKeyboardMarkup(roulette_menu)
            await query.edit_message_text("Рулетки:", reply_markup=reply_markup)

        elif data == "antiafk_menu":
            antiafk_menu = [
                [InlineKeyboardButton("Вкл/Выкл 🕹️", callback_data="toggle_antiafk")],
                [InlineKeyboardButton("Назад", callback_data="features")]
            ]
            reply_markup = InlineKeyboardMarkup(antiafk_menu)
            await query.edit_message_text("Анти-AFK:", reply_markup=reply_markup)

        elif data == "toggle_lottery":
            self.lottery_enabled = not self.lottery_enabled
            self.save_config()
            await context.bot.send_message(chat_id=query.message.chat_id, text=f"Лотерейки {'включены' if self.lottery_enabled else 'выключены'}")

        elif data == "toggle_roulette":
            self.roulette_enabled = not self.roulette_enabled
            self.save_config()
            await context.bot.send_message(chat_id=query.message.chat_id, text=f"Рулетки {'включены' if self.roulette_enabled else 'выключены'}")

        elif data == "toggle_antiafk":
            self.anti_afk_enabled = not self.anti_afk_enabled
            self.save_config()
            await context.bot.send_message(chat_id=query.message.chat_id, text=f"Анти-AFK {'включен' if self.anti_afk_enabled else 'выключен'}")

        elif data == "toggle_reconnect":
            self.auto_reconnect_enabled = not self.auto_reconnect_enabled
            self.save_config()
            await context.bot.send_message(chat_id=query.message.chat_id, text=f"Авто-реконнект {'включен' if self.auto_reconnect_enabled else 'выключен'}")

        elif data == "stats":
            await self.stats_command(update, context)

        elif data == "resources":
            await self.resources_command(update, context)

        elif data == "logs":
            await self.send_log(update, context)

        elif data == "screenshot":
            await self.screenshot_command(update, context)

        elif data == "schedule":
            actions_list = ", ".join(self.ACTION_MAP.keys())
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Введите действие и время: 'запланировать действие HH:MM', например: запланировать лотерея 14:30. Доступные действия: {actions_list}"
            )

        elif data == "list_scheduled":
            if self.scheduled_actions:
                scheduled_text = "\n".join([f"{action['id']}: {action['russian_action']} в {action['time'].strftime('%H:%M')}" for action in self.scheduled_actions])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Запланированные действия:\n{scheduled_text}")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Нет запланированных действий")

        elif data == "cancel_schedule":
            if self.scheduled_actions:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите ID действия для отмены")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Нет запланированных действий для отмены")

        elif data == "force_reconnect":
            self.perform_reconnect()
            await context.bot.send_message(chat_id=query.message.chat_id, text="Принудительный реконект запущен 🔄")

        elif data == "force_buy_lottery":
            self.perform_lottery_purchase()
            await context.bot.send_message(chat_id=query.message.chat_id, text="Принудительная покупка лотерейки выполнена 🎟️ ")

        elif data == "force_spin_roulette":
            self.perform_roulette_spin(force=True)
            await context.bot.send_message(chat_id=query.message.chat_id, text="Принудительное вращение рулетки выполнено 🎰")

    async def handle_text(self, update, context):
        text = update.message.text.lower()
        parts = text.split()
        if len(parts) >= 2:
            if parts[0] == "интервал" and len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
                min_interval, max_interval = map(int, parts[1:3])
                if 10 <= min_interval <= max_interval <= 60:
                    self.min_lottery_interval = min_interval * 60
                    self.max_lottery_interval = max_interval * 60
                    self.save_config()
                    await update.message.reply_text(f"Интервал лотереек установлен: {min_interval}-{max_interval} минут")
                else:
                    await update.message.reply_text("Интервалы должны быть от 10 до 60 минут")
            elif parts[0] == "пароль" and len(parts) == 2:
                self.password = parts[1]
                self.save_config()
                await update.message.reply_text("Пароль обновлен")
            elif parts[0] == "реконект" and len(parts) == 2 and parts[1].isdigit():
                interval = int(parts[1])
                self.reconnect_interval = interval * 60 if interval > 0 else 0
                self.auto_reconnect_enabled = interval > 0
                self.save_config()
                await update.message.reply_text(f"Интервал проверки потери связи: {interval} минут" if interval > 0 else "Проверка потери связи отключена")
            elif parts[0] == "запланировать" and len(parts) == 3 and parts[2].count(":") == 1:
                action = parts[1]
                if action in self.ACTION_MAP:
                    await self.schedule_action(update, context, [action, self.ACTION_MAP[action], parts[2]])
                else:
                    actions_list = ", ".join(self.ACTION_MAP.keys())
                    await update.message.reply_text(f"Неизвестное действие. Доступные действия: {actions_list}")
            elif parts[0] == "отменить" and len(parts) == 2 and parts[1].isdigit():
                action_id = int(parts[1])
                for action in self.scheduled_actions:
                    if action['id'] == action_id:
                        self.scheduled_actions.remove(action)
                        await update.message.reply_text(f"Действие {action_id} отменено")
                        break
                else:
                    await update.message.reply_text("Действие не найдено")
            else:
                await update.message.reply_text("Неизвестная команда. Используйте меню или проверьте формат.")
        else:
            await update.message.reply_text("Неизвестная команда. Используйте меню для управления.")

    async def schedule_action(self, update, context, args):
        russian_action, internal_action, time_str = args
        try:
            action_time = datetime.strptime(time_str, "%H:%M")
            current_date = datetime.now().date()
            scheduled_time = datetime.combine(current_date, action_time.time())
            if scheduled_time < datetime.now():
                scheduled_time += timedelta(days=1)
            self.schedule_id_counter += 1
            self.scheduled_actions.append({
                "id": self.schedule_id_counter,
                "russian_action": self.ACTION_DISPLAY_MAP[internal_action],
                "internal_action": internal_action,
                "time": scheduled_time
            })
            await update.message.reply_text(f"Действие '{self.ACTION_DISPLAY_MAP[internal_action]}' запланировано на {time_str}")
            self.save_config()
        except ValueError:
            actions_list = ", ".join(self.ACTION_MAP.keys())
            await update.message.reply_text(f"Неверный формат времени. Используйте HH:MM, например: запланировать лотерея 14:30. Доступные действия: {actions_list}")

    async def status_command(self, update, context):
        if update.message:
            chat_id = update.message.chat_id
        elif update.callback_query and update.callback_query.message:
            chat_id = update.callback_query.message.chat_id
        else:
            self.app.logger.log("AntiAfk", "Не удалось определить chat_id", "error")
            return
        
        status = (f"ℹ️ Статус бота:\n"
                  f"Бот: {'включен' if self.bot_running else 'выключен'}\n"
                  f"Анти-AFK: {'включен' if self.anti_afk_enabled else 'выключен'}\n"
                  f"Лотерейки: {'включены' if self.lottery_enabled else 'выключены'}\n"
                  f"Рулетки: {'включены' if self.roulette_enabled else 'выключены'}\n"
                  f"Реконект: {'включен' if self.auto_reconnect_enabled else 'выключен'}")
        
        await context.bot.send_message(chat_id=chat_id, text=status)

    async def stats_command(self, update, context):
        stats = (f"📊 Статистика:\n"
                 f"Время: {self.timer_value // 3600:02}:{(self.timer_value % 3600) // 60:02}:{self.timer_value % 60:02} ⏳\n"
                 f"Рулетки: {self.roulette_count} 🎰\n"
                 f"Лотерейки: {self.lottery_count} 🎟️\n"
                 f"Payday: {self.payday_count} 💰\n"
                 f"Реконект: {self.reconnect_count} 🔄")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=stats)

    async def resources_command(self, update, context):
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_io_counters()
        try:
            w = wmi.WMI()
            cpu_temp = w.Win32_TemperatureProbe()[0].CurrentReading
        except:
            cpu_temp = "N/A"
        gpus = GPUtil.getGPUs()
        gpu_info = "\n".join([f"GPU {i}: {gpu.load * 100}% (Temp: {gpu.temperature}°C)" for i, gpu in enumerate(gpus)]) if gpus else "GPU не найдена"
        resources = (f"💻 Ресурсы компьютера:\n"
                     f"CPU: {cpu_percent}% (Частота: {cpu_freq.current if cpu_freq else 'N/A'} МГц, Макс: {cpu_freq.max if cpu_freq else 'N/A'} МГц, Temp: {cpu_temp}°C)\n"
                     f"Память: {memory.percent}% (Использовано: {memory.used // 1024**2} МБ / Всего: {memory.total // 1024**2} МБ)\n"
                     f"Диск: {disk.percent}% (Свободно: {disk.free // 1024**3} ГБ / Всего: {disk.total // 1024**3} ГБ)\n"
                     f"Сеть: Отправлено {net.bytes_sent // 1024**2} МБ, Получено {net.bytes_recv // 1024**2} МБ\n"
                     f"{gpu_info}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resources)

    async def screenshot_command(self, update, context):
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[1])
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buf)

    def toggle_bot(self):
        if self.bot_running:
            self.stop_bot()
        else:
            self.start_bot()

    def start_bot(self):
        if not (self.anti_afk_enabled or self.lottery_enabled or self.roulette_enabled):
            return
        if hasattr(self, 'bot_running') and self.bot_running:
            return  
        self.bot_running = True
        if self.anti_afk_enabled:
            self.press_animation_key()
        threading.Thread(target=self.bot_loop, daemon=True).start()
        threading.Thread(target=self.timer_loop, daemon=True).start()
        if self.auto_reconnect_enabled and self.password:
            self.schedule_reconnect_check()

    def stop_bot(self):
        self.bot_running = False
        controller = KeyboardController()
        controller.release(KeyCode.from_vk(0x57))  
        controller.release(KeyCode.from_vk(0x53))  
        if self.reconnect_timer:
            self.reconnect_timer.cancel()

    def press_bind(self, key):
        if key is None:
            return
        try:
            controller = KeyboardController()
            controller.press(key)
            time.sleep(0.05)
            controller.release(key)
        except Exception as e:
            self.app.logger.log("AntiAfk", f"Ошибка при нажатии клавиши: {e}", "error")

    def press_animation_key(self):
        self.press_bind(self.animation_key)

    def find_image_with_timeout(self, image_name, area, timeout=15):
        max_val_seen = 0
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.find_image_in_area(image_name, area)
            if not isinstance(result, tuple) or len(result) != 2:
                self.app.logger.log("AntiAfk", f"Неверный тип result: {type(result)}, значение: {result}", "error")
                return None
            position, max_val = result
            if position is not None and isinstance(position, tuple) and len(position) == 2:
                self.app.logger.log("AntiAfk", f"Изображение {image_name} найдено на координатах {position}", "info")
                return position
            if max_val > max_val_seen:
                max_val_seen = max_val
            time.sleep(0.1)
        self.app.logger.log("AntiAfk", f"Изображение {image_name} не найдено, максимальная корреляция: {max_val_seen}", "warning")
        return None

    def perform_lottery_purchase(self):
        self.app.logger.log("AntiAfk", "Начало покупки лотереи", "info")
        try:
            time.sleep(1)
            self.press_bind(self.take_out_phone_key)
            time.sleep(1)

            if self.lottery_app_coords:
                self.app.logger.log("AntiAfk", f"Клик по координатам: {self.lottery_app_coords}", "info")
                pyautogui.click(self.lottery_app_coords[0], self.lottery_app_coords[1])
            else:
                self.app.logger.log("AntiAfk", "Поиск иконки lottery", "info")
                pos = self.find_image_with_timeout('lottery', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=60)
                if pos and isinstance(pos, tuple) and len(pos) == 2:
                    self.app.logger.log("AntiAfk", f"Найдена иконка lottery на {pos}", "info")
                    pyautogui.click(pos[0], pos[1])
                else:
                    self.app.logger.log("AntiAfk", "Не удалось найти иконку лотереи", "warning")
                    return

            time.sleep(1)
            self.app.logger.log("AntiAfk", "Поиск кнопки buyticket", "info")
            pos = self.find_image_with_timeout('buyticket', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=15)
            if pos and isinstance(pos, tuple) and len(pos) == 2:
                self.app.logger.log("AntiAfk", f"Найдена кнопка buyticket на {pos}", "info")
                pyautogui.click(pos[0], pos[1])
                time.sleep(0.5)
            else:
                self.app.logger.log("AntiAfk", "Не удалось найти кнопку покупки лотереи в течение 15 секунд", "warning")
                self.press_bind(self.put_away_phone_key)
                time.sleep(0.1)
                self.press_bind(self.put_away_phone_key)
                return

            start_time = time.time()
            self.app.logger.log("AntiAfk", "Поиск bankkard", "info")
            bankkard_found = False
            while time.time() - start_time < 5:
                bankkard_area = {"left": 0, "top": self.app.game_height - 150, "width": self.app.game_width, "height": 150}
                result = self.find_image_in_area('bankkard', bankkard_area)
                if result[0]:
                    self.app.logger.log("AntiAfk", "Найден bankkard, лотерея куплена", "info")
                    self.lottery_count += 1
                    self.action_history.append({"timestamp": datetime.now(), "action": "buy_lottery"})
                    if self.application and self.chat_id:
                        asyncio.run_coroutine_threadsafe(
                            self.application.bot.send_message(chat_id=self.chat_id, text="Лотерейка куплена 🎟️"), self.loop)
                    bankkard_found = True
                    break
                time.sleep(0.1)
            if not bankkard_found:
                self.app.logger.log("AntiAfk", "Bankkard не найден в течение 5 секунд", "warning")

            self.press_bind(self.put_away_phone_key)
            time.sleep(0.1)
            self.press_bind(self.put_away_phone_key)

        except Exception as e:
            self.app.logger.log("AntiAfk", f"Ошибка при покупке лотереи: {e}", "error")
            self.press_bind(self.put_away_phone_key)
            time.sleep(0.1)
            self.press_bind(self.put_away_phone_key)
        finally:
            if self.anti_afk_enabled:
                self.press_animation_key()

    def perform_roulette_spin(self, force=False):
        if self.is_reconnecting:
            return
        if 'cas' in self.app.templates:
            self.app.logger.log("AntiAfk", f"Форма шаблона cas: {self.app.templates['cas'].shape if self.app.templates['cas'] is not None else 'None'}", "info")
        else:
            self.app.logger.log("AntiAfk", "cas отсутствует в шаблонах", "error")
        """Выполняет вращение рулетки, напрямую ища cas.jpg без зависимости от lottery.jpg."""
        cols_area = {"left": self.app.game_width - 350, "top": 0, "width": 350, "height": 200}
        pos = self.find_image_with_timeout('cols', cols_area) if not force else None
        if force or pos:
            if 'cas' not in self.app.templates or self.app.templates['cas'] is None:
                self.app.logger.log("AntiAfk", "Изображение cas.jpg не загружено или повреждено", "error")
                return

            controller = KeyboardController()
            controller.release(KeyCode.from_vk(0x57))  
            controller.release(KeyCode.from_vk(0x53))  
            time.sleep(1)

            self.app.logger.log("AntiAfk", "Открытие телефона", "info")
            self.press_bind(self.take_out_phone_key)
            time.sleep(1)

            cas_area = {
                "left": 0,
                "top": self.app.game_height // 2,
                "width": self.app.game_width,
                "height": self.app.game_height // 2
            }
            cas_pos = self.find_image_with_timeout('cas', cas_area, timeout=10)
            if cas_pos and isinstance(cas_pos, tuple) and len(cas_pos) == 2:
                self.app.logger.log("AntiAfk", f"Найдена иконка cas на {cas_pos}", "info")
                pyautogui.click(cas_pos[0], cas_pos[1])
                time.sleep(1)
            else:
                self.app.logger.log("AntiAfk", "Не удалось найти иконку cas.jpg в нижней половине экрана", "warning")
                self.press_bind(self.put_away_phone_key)
                time.sleep(0.1)
                self.press_bind(self.put_away_phone_key)
                return

            kasspin_area = {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}
            kasspin_pos = self.find_image_with_timeout('kasspin', kasspin_area, timeout=15)
            if kasspin_pos and isinstance(kasspin_pos, tuple) and len(kasspin_pos) == 2:
                self.app.logger.log("AntiAfk", f"Найдено изображение kasspin на {kasspin_pos}", "info")
                pyautogui.click(kasspin_pos[0], kasspin_pos[1])
                time.sleep(1)
            else:
                self.app.logger.log("AntiAfk", "Не удалось найти изображение kasspin в течение 15 секунд", "warning")
                self.press_bind(self.put_away_phone_key)
                time.sleep(0.1)
                self.press_bind(self.put_away_phone_key)
                return

            if hasattr(self, 'spin_button_coords') and self.spin_button_coords:
                self.app.logger.log("AntiAfk", f"Клик по сохраненным координатам спина: {self.spin_button_coords}", "info")
                pyautogui.click(self.spin_button_coords[0], self.spin_button_coords[1])
            else:
                spin_pos = self.find_image_with_timeout('spinbutton', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=10)
                if spin_pos and isinstance(spin_pos, tuple) and len(spin_pos) == 2:
                    self.app.logger.log("AntiAfk", f"Найдена кнопка spinbutton на {spin_pos}", "info")
                    pyautogui.click(spin_pos[0], spin_pos[1])
                else:
                    self.app.logger.log("AntiAfk", "Не удалось найти кнопку спина", "warning")
                    self.press_bind(self.put_away_phone_key)
                    time.sleep(0.1)
                    self.press_bind(self.put_away_phone_key)
                    return

            self.roulette_count += 1
            self.action_history.append({"timestamp": datetime.now(), "action": "spin_roulette"})
            self.roulette_cooldown = True
            threading.Timer(60.0, self.reset_roulette_cooldown).start()
            self.app.logger.log("AntiAfk", "Рулетка прокручена успешно", "info")
            
            time.sleep(0.5)
            controller.press(Key.esc)
            controller.release(Key.esc)
            time.sleep(0.5)
            controller.press(Key.esc)
            controller.release(Key.esc)
            time.sleep(0.5)
            self.press_bind(self.put_away_phone_key)
            time.sleep(0.5)
            self.press_animation_key()
            controller.press(KeyCode.from_vk(0x57))  
            controller.press(KeyCode.from_vk(0x53))  

            if self.application and self.chat_id:
                asyncio.run_coroutine_threadsafe(
                    self.application.bot.send_message(chat_id=self.chat_id, text="Рулетка прокручена 🎰"), self.loop)
        else:
            self.app.logger.log("AntiAfk", "Не удалось найти cols, пропускаем спин", "warning")

    def reset_roulette_cooldown(self):
        self.roulette_cooldown = False

    def check_for_payday(self):
        if self.is_reconnecting:
            return
        if time.time() - self.last_payday_detection < 15 * 60:
            return
        try:
            payday_area = {"left": 0, "top": 0, "width": 500, "height": 300}
            payday_key = f'payday{self.chat_font_size}'
            start_time = time.time()
            while time.time() - start_time < 30:  
                pos = self.find_image_with_timeout(payday_key, payday_area, timeout=5)
                if pos:
                    self.payday_count += 1
                    self.last_payday_detection = time.time()
                    self.action_history.append({"timestamp": datetime.now(), "action": "payday_detected"})
                    if self.application and self.chat_id:
                        asyncio.run_coroutine_threadsafe(
                            self.application.bot.send_message(chat_id=self.chat_id, text="Payday обнаружен 💰"), self.loop)
                    return
                time.sleep(5)
            self.app.logger.log("AntiAfk", "Payday не обнаружен в течение 1 минуты", "warning")
        except Exception as e:
            self.app.logger.log("AntiAfk", f"Ошибка при проверке Payday: {e}", "error")

    def find_image_in_area(self, image_name, area):
        try:
            with mss.mss() as sct:
                monitor = {
                    "left": self.game_left + area["left"],
                    "top": self.game_top + area["top"],
                    "width": area["width"],
                    "height": area["height"]
                }
                screen = np.array(sct.grab(monitor))
                screen_bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
                template = self.app.templates.get(image_name)
                if template is not None:
                    if len(template.shape) == 2:
                        screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
                        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                    else:
                        result = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    threshold = self.thresholds.get(image_name, 0.7)
                    if max_val > threshold:
                        abs_x = monitor["left"] + max_loc[0] + template.shape[1] // 2
                        abs_y = monitor["top"] + max_loc[1] + template.shape[0] // 2
                        return (abs_x, abs_y), max_val
                    else:
                        return None, max_val
                else:
                    return None, 0
        except Exception as e:
            self.app.logger.log("AntiAfk", f"Ошибка при поиске изображения {image_name}: {e}", "error")
            return None, 0

    def bot_loop(self):
        self.last_connection_check_time = time.time()
        controller = KeyboardController()
        if self.anti_afk_enabled:
            controller.press(KeyCode.from_vk(0x57))  
            controller.press(KeyCode.from_vk(0x53))  

        while self.bot_running:
            current_time_sec = time.time()
            if current_time_sec - self.last_connection_check_time >= 60:
                self.last_connection_check_time = current_time_sec
                self.app.logger.log("AntiAfk", "Начало проверки connect.jpg и connect2.jpg", "info")
                start_time = time.time()
                area = {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}
                while time.time() - start_time < 15:
                    connect_pos, _ = self.find_image_in_area('connect', area)
                    connect2_pos, _ = self.find_image_in_area('connect2', area)
                    if connect_pos or connect2_pos:
                        self.app.logger.log("AntiAfk", "Обнаружено connect.jpg или connect2.jpg, запуск реконнекта", "info")
                        self.perform_reconnect()
                        break
                    time.sleep(1)

            
            if self.lottery_enabled and time.time() >= self.next_lottery_time:
                if self.anti_afk_enabled:
                    controller.release(KeyCode.from_vk(0x57))
                    controller.release(KeyCode.from_vk(0x53))
                self.perform_lottery_purchase()
                self.next_lottery_time = time.time() + random.uniform(self.min_lottery_interval, self.max_lottery_interval)
                if self.anti_afk_enabled:
                    controller.press(KeyCode.from_vk(0x57))
                    controller.press(KeyCode.from_vk(0x53))

            if self.roulette_enabled:
                self.perform_roulette_spin()

            if self.anti_afk_enabled:
                self.check_for_payday()

            time.sleep(1)

        if self.anti_afk_enabled:
            controller.release(KeyCode.from_vk(0x57))
            controller.release(KeyCode.from_vk(0x53))

    def timer_loop(self):
        while self.bot_running:
            self.timer_value += 1
            self.update_labels()
            time.sleep(1)

    def check_connection_image(self):
        start_time = time.time()
        while time.time() - start_time < 10:
            result = self.find_image_in_area('connection', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height})
            if result[0] is not None:
                self.perform_reconnect()
                break
            time.sleep(1)

    def update_labels(self):
        hours = self.timer_value // 3600
        minutes = (self.timer_value % 3600) // 60
        seconds = self.timer_value % 60
        self.time_text.config(text=f"Время: {hours:02}:{minutes:02}:{seconds:02}")
        self.roulette_text.config(text=f"Рулетки: {self.roulette_count}")
        self.lottery_text.config(text=f"Лотерейки: {self.lottery_count}")
        self.payday_text.config(text=f"Payday: {self.payday_count}")

    def reset_stats(self):
        self.lottery_count = 0
        self.roulette_count = 0
        self.payday_count = 0
        self.timer_value = 0
        self.update_labels()

    def save_config(self):
        self.app.config["AntiAfk"]["AntiAfkEnabled"] = str(self.anti_afk_enabled)
        self.app.config["AntiAfk"]["LotteryEnabled"] = str(self.lottery_enabled)
        self.app.config["AntiAfk"]["RouletteEnabled"] = str(self.roulette_enabled)
        self.app.config["AntiAfk"]["AutoReconnect"] = str(self.auto_reconnect_enabled)
        self.app.config["AntiAfk"]["Password"] = self.password
        self.app.config["AntiAfk"]["MinLotteryInterval"] = str(self.min_lottery_interval)
        self.app.config["AntiAfk"]["MaxLotteryInterval"] = str(self.max_lottery_interval)
        self.app.config["AntiAfk"]["ReconnectInterval"] = str(self.reconnect_interval)
        if self.character_coords:
            self.app.config["AntiAfk"]["CharacterX"] = str(self.character_coords[0])
            self.app.config["AntiAfk"]["CharacterY"] = str(self.character_coords[1])
        with open(os.path.join(self.app.sniker_lite_path, "sniker_settings.ini"), "w") as f:
            self.app.config.write(f)

    def schedule_reconnect_check(self):
        if self.bot_running and self.auto_reconnect_enabled and self.password:
            self.reconnect_timer = threading.Timer(self.reconnect_check_interval, self.check_reconnect)
            self.reconnect_timer.start()

    def check_reconnect(self):
        if not self.bot_running or not self.auto_reconnect_enabled or not self.password:
            return
        self.reconnect_stage = "Проверка соединения"
        self.update_labels()
        start_time = time.time()
        while time.time() - start_time < 15:
            if self.app.find_image('connection'):
                self.perform_reconnect()
                break
            time.sleep(1)
        else:
            self.reconnect_stage = "Соединение в порядке"
            self.update_labels()
        self.schedule_reconnect_check()

    def perform_reconnect(self):
        self.is_reconnecting = True
        controller = KeyboardController()
        restart = True

        while restart:
            restart = False
            self.reconnect_stage = "Запуск F1"
            self.update_labels()
            controller.press(Key.f1)
            controller.release(Key.f1)
            time.sleep(1.5)

            self.reconnect_stage = "Поиск ipserv.jpg"
            self.update_labels()
            pos = self.find_image_with_timeout('ipserv', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=20)
            if pos:
                pyautogui.click(pos[0], pos[1])
                time.sleep(0.5)
            else:
                self.app.logger.log("AntiAfk", "Не удалось найти ipserv.jpg", "warning")
                self.reconnect_stage = "Ошибка"
                self.update_labels()
                self.is_reconnecting = False
                return

            self.reconnect_stage = "Поиск connect.jpg"
            self.update_labels()
            pos = self.find_image_with_timeout('connect', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=20)
            if pos:
                pyautogui.click(pos[0], pos[1])
                time.sleep(5.0)
            else:
                self.app.logger.log("AntiAfk", "Не удалось найти connect.jpg", "warning")
                self.reconnect_stage = "Ошибка"
                self.update_labels()
                self.is_reconnecting = False
                return

            self.reconnect_stage = "Поиск finish.jpg"
            self.update_labels()
            area = {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}
            while True:
                finish_pos, _ = self.find_image_in_area('finish', area)
                connect_pos, _ = self.find_image_in_area('connect', area)
                connect2_pos, _ = self.find_image_in_area('connect2', area)
                if finish_pos:
                    time.sleep(15)
                    break
                elif connect_pos or connect2_pos:
                    self.app.logger.log("AntiAfk", "Обнаружено connect.jpg или connect2.jpg, перезапуск реконнекта", "info")
                    controller.press(Key.f1)
                    controller.release(Key.f1)
                    time.sleep(1.5)
                    restart = True
                    break
                time.sleep(1)

        self.reconnect_stage = "Поиск passw.jpg"
        self.update_labels()
        
        start_time = time.time()
        passw_found = False
        while time.time() - start_time < 10:
            pos = self.find_image_with_timeout('passw', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=1)
            if pos:
                click_x = pos[0] + 50
                click_y = pos[1]
                pyautogui.click(click_x, click_y)
                time.sleep(0.5)
                
                
                click_x_rel = click_x - self.game_left
                click_y_rel = click_y - self.game_top
                left = max(0, click_x_rel - 100)
                top = max(0, click_y_rel - 100)
                right = min(self.app.game_width, click_x_rel + 100)
                bottom = min(self.app.game_height, click_y_rel + 100)
                width = right - left
                height = bottom - top
                if width > 0 and height > 0:
                    cursor_search_area = {"left": left, "top": top, "width": width, "height": height}
                    self.app.logger.log("AntiAfk", f"Поиск cursor.jpg в области: left={left}, top={top}, width={width}, height={height}", "info")
                    start_time_cursor = time.time()
                    cursor_found = False
                    while time.time() - start_time_cursor < 5:
                        cursor_pos, _ = self.find_image_in_area('cursor', cursor_search_area)
                        if cursor_pos is not None:
                            self.app.logger.log("AntiAfk", "cursor.jpg найден", "info")
                            cursor_found = True
                            break
                        time.sleep(0.1)
                    if not cursor_found:
                        self.app.logger.log("AntiAfk", "cursor.jpg не найден, нажимаем F2 и повторяем клик", "info")
                        controller.press(Key.f2)
                        controller.release(Key.f2)
                        time.sleep(0.5)
                        pyautogui.click(click_x, click_y)
                        time.sleep(0.5)
                else:
                    self.app.logger.log("AntiAfk", "Область поиска cursor.jpg вне игрового окна", "warning")
                
                self.reconnect_stage = "Ввод пароля"
                self.update_labels()
                pyperclip.copy(self.password)
                controller.press(Key.ctrl)
                controller.press(KeyCode.from_vk(0x56))  
                controller.release(KeyCode.from_vk(0x56))
                controller.release(Key.ctrl)
                time.sleep(0.5)
                passw_found = True
                break
            time.sleep(1)

        if not passw_found:
            self.app.logger.log("AntiAfk", "Не удалось найти passw.jpg в течение 10 секунд, пропускаем ввод пароля", "warning")

        self.reconnect_stage = "Поиск voit.jpg"
        self.update_labels()
        voit_pos = self.find_image_with_timeout('voit', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=15)
        if voit_pos:
            pyautogui.click(voit_pos[0] + 20, voit_pos[1])
            time.sleep(5)
            if self.character_coords:
                pyautogui.click(self.character_coords[0], self.character_coords[1])
            else:
                self.app.logger.log("AntiAfk", "Координаты выбора персонажа не установлены", "warning")

            self.reconnect_stage = "Подтверждение (acep.jpg)"
            self.update_labels()
            acep_pos = self.find_image_with_timeout('acep', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=15)
            if acep_pos:
                pyautogui.click(acep_pos[0], acep_pos[1])
                time.sleep(0.5)
                self.app.logger.log("AntiAfk", "Нажато на acep.jpg", "info")
            else:
                self.app.logger.log("AntiAfk", "Не удалось найти acep.jpg", "warning")
                self.reconnect_stage = "Ошибка"
                self.update_labels()
                return

            
            self.reconnect_stage = "Поиск last.jpg"
            self.update_labels()
            start_time = time.time()
            last_found = False
            while time.time() - start_time < 15:
                last_pos = self.find_image_with_timeout('last', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=1)
                if last_pos:
                    pyautogui.click(last_pos[0], last_pos[1])  
                    self.app.logger.log("AntiAfk", "Нажато на last.jpg", "info")
                    last_found = True
                    break
                time.sleep(1)

            if last_found:
                
                self.reconnect_stage = "Поиск lastacc.jpg"
                self.update_labels()
                start_time = time.time()
                lastacc_pos = None
                while time.time() - start_time < 15:
                    lastacc_pos = self.find_image_with_timeout('lastacc', {"left": 0, "top": 0, "width": self.app.game_width, "height": self.app.game_height}, timeout=1)
                    if lastacc_pos:
                        break
                    time.sleep(1)

                if lastacc_pos:
                    pyautogui.click(lastacc_pos[0], lastacc_pos[1])
                    self.app.logger.log("AntiAfk", "Нажато на lastacc.jpg", "info")
                else:
                    self.app.logger.log("AntiAfk", "Не удалось найти lastacc.jpg в течение 15 секунд, цикл завершен", "info")
            else:
                self.app.logger.log("AntiAfk", "Не удалось найти last.jpg в течение 15 секунд, цикл завершен", "info")

            self.reconnect_count += 1
            self.last_reconnect_time = time.time()
            self.reconnect_stage = "Ожидание"
            self.update_labels()
            self.app.logger.log("AntiAfk", "Реконект успешно выполнен", "info")

        else:
            self.app.logger.log("AntiAfk", "Не удалось найти voit.jpg", "warning")
            self.reconnect_stage = "Ошибка"
            self.update_labels()
            return
        
        self.is_reconnecting = False
                                                    
class EMSChecker:
    def __init__(self, app):
        self.app = app
        self.frame = self.app.bot_frames['ems']
        self.active = False
        self.game_left = self.app.game_left
        self.game_top = self.app.game_top
        self.game_width = self.app.game_width
        self.game_height = self.app.game_height
        self.scale_x = self.app.scale_x
        self.scale_y = self.app.scale_y
        self.status_label = None
        self.last_click_time = {}
        self.cooldown = 0.5
        self.images = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
        self.key_map = {
            '1': ['1'],
            '2': ['1'],
            '3': ['4'],
            '4': ['6'],
            '5': ['6'],
            '6': ['5'],
            '7': ['7'],
            '8': ['9'],
            '9': ['1', '0'],
            '10': ['0'],
            '11': ['2'],
            '12': ['3'],
            '13': ['8']
        }
        self.threshold = 0.8
        self.first_run = not self.app.config.has_section("EMSSettings")
        if self.first_run:
            self.search_area = {"left": self.app.game_left, "top": self.app.game_top,
                                "width": self.app.game_width, "height": self.app.game_height}
        else:
            self.search_area = {
                "left": int(self.app.config["EMSSettings"].get("SearchLeft", str(self.app.game_left))),
                "top": int(self.app.config["EMSSettings"].get("SearchTop", str(self.app.game_top))),
                "width": int(self.app.config["EMSSettings"].get("SearchWidth", str(self.app.game_width))),
                "height": int(self.app.config["EMSSettings"].get("SearchHeight", str(self.app.game_height)))
            }
        self.controller = KeyboardController()  
        self.setup_gui()

    def setup_gui(self):
        self.status_label = tk.Label(self.frame, text="Статус: Неактивен", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                 font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.status_label.pack(pady=5)
        control_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        control_frame.pack(anchor=tk.W, expand=True, pady=5)
        control_text = tk.Text(control_frame, wrap=tk.WORD, height=1, width=35, bd=0, bg=TEXT_BG_COLOR,
                            fg=TEXT_FG_COLOR, font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        control_text.configure(state='disabled')
        control_text.config(cursor="arrow", selectbackground=control_text.cget("bg"),
                            selectforeground=control_text.cget("fg"))
        control_text.pack()
        self.reconfigure_button = tk.Button(self.frame, text="Перенастроить", command=self.show_setup_window,
                                            bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR, font=('Roboto', 10, 'bold'),
                                            relief='flat', activebackground=ACTIVE_BUTTON_COLOR)
        self.reconfigure_button.pack(pady=5)
        
        self.stats_labels = [
            self.status_label
        ]

    def show_setup_window(self):
        if self.app.current_setup_window and self.app.current_setup_window.winfo_exists():
            messagebox.showinfo("Информация", "Уже открыто окно настроек. Закройте его, чтобы открыть новое.")
            return
        setup_window = tk.Toplevel(self.app.root)
        setup_window.overrideredirect(True)
        setup_window.attributes("-topmost", True)
        setup_window.configure(bg=BACKGROUND_COLOR)
        setup_window.geometry("300x250+10+10")

        title_bar = tk.Frame(setup_window, bg=BUTTON_COLOR, bd=0, highlightthickness=0)
        title_bar.pack(fill=tk.X)
        font_size = self.app.get_scaled_font_size(10)
        title_label = tk.Label(title_bar, text="Настройка бота EMS", bg=BUTTON_COLOR, fg=HEADER_TEXT_COLOR,
                               font=('Roboto', font_size, 'bold'))
        title_label.pack(side=tk.LEFT, padx=5)
        close_button = tk.Button(title_bar, text="X", command=setup_window.destroy, bg=BUTTON_COLOR,
                                 fg=HEADER_TEXT_COLOR, font=('Roboto', font_size - 1, 'bold'), relief='flat')
        close_button.pack(side=tk.RIGHT, padx=2)

        content_frame = tk.Frame(setup_window, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        instruction_label = tk.Label(content_frame,
                                     text="Для настройки нажмите G по любому гражданину чтобы появилось кольцо действий.",
                                     wraplength=280, bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', font_size))
        instruction_label.pack(pady=5)
        status_label = tk.Label(content_frame, text="Ожидание...", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                font=('Roboto', font_size))
        status_label.pack(pady=5)

        def search_for_emshelp():
            while setup_window.winfo_exists():
                pos = self.app.find_image('emshelp')
                if pos:
                    left = max(pos[0] - 100, self.app.game_left)
                    top = max(pos[1] - 100, self.app.game_top)
                    right = min(pos[0] + 100, self.app.game_left + self.app.game_width)
                    bottom = min(pos[1] + 100, self.app.game_top + self.app.game_height)
                    self.search_area = {'left': left, 'top': top, 'width': right - left, 'height': bottom - top}
                    self.app.config["EMSSettings"] = {
                        "SearchLeft": str(left),
                        "SearchTop": str(top),
                        "SearchWidth": str(right - left),
                        "SearchHeight": str(bottom - top)
                    }
                    with open(os.path.join(self.app.sniker_lite_path, "sniker_settings.ini"), "w") as f:
                        self.app.config.write(f)
                    status_label.config(text="Успешно!")
                    setup_window.after(3000, setup_window.destroy)
                    self.first_run = False
                    break
                time.sleep(0.5)

        threading.Thread(target=search_for_emshelp, daemon=True).start()
        self.app.current_setup_window = setup_window
        setup_window.protocol("WM_DELETE_WINDOW", lambda: self.app.on_setup_window_close(setup_window))

    def toggle_bot(self):
        if self.active:
            self.stop_bot()
            self.status_label.config(text="Статус: Неактивен")
        else:
            if self.first_run:
                self.show_setup_window()
            else:
                self.active = True
                self.start_checking()
                self.status_label.config(text="Статус: Активен")
                self.app.logger.log("EMS", "Бот запущен (f5)", "info")

    def start_checking(self):
        threading.Thread(target=self.checking_loop, daemon=True).start()

    def checking_loop(self):
        while self.active:
            self._check_images()
            time.sleep(0.01)

    def _check_images(self):
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(self.search_area))
            screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            current_time = time.time()
            for img_name in self.images:
                template = self.app.templates.get(img_name)
                if template is not None:
                    result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    if max_val > self.threshold:
                        if img_name not in self.last_click_time or current_time - self.last_click_time[img_name] > self.cooldown:
                            self.controller.press(pynput_keyboard.KeyCode.from_vk(0x31))  
                            self.controller.release(pynput_keyboard.KeyCode.from_vk(0x31))
                            time.sleep(0.1)

                            keys = self.key_map.get(img_name, [])
                            if len(keys) == 1:
                                vk_code = int(keys[0]) + 0x30 if keys[0].isdigit() else ord(keys[0].upper())
                                self.controller.press(pynput_keyboard.KeyCode.from_vk(vk_code))
                                self.controller.release(pynput_keyboard.KeyCode.from_vk(vk_code))
                            elif len(keys) == 2:
                                vk_code1 = int(keys[0]) + 0x30 if keys[0].isdigit() else ord(keys[0].upper())
                                vk_code2 = int(keys[1]) + 0x30 if keys[1].isdigit() else ord(keys[1].upper())
                                self.controller.press(pynput_keyboard.KeyCode.from_vk(vk_code1))
                                time.sleep(0.01)
                                self.controller.press(pynput_keyboard.KeyCode.from_vk(vk_code2))
                                self.controller.release(pynput_keyboard.KeyCode.from_vk(vk_code2))
                                self.controller.release(pynput_keyboard.KeyCode.from_vk(vk_code1))

                            self.last_click_time[img_name] = current_time
                            self.app.logger.log("EMS", f"Найдено и обработано изображение {img_name}", "info")

    def stop_bot(self):
        self.active = False

class DemorganBot:
    def __init__(self, app):
        self.app = app
        self.frame = self.app.bot_frames['demorgan']
        self.active = False
        self.game_left = self.app.game_left
        self.game_top = self.app.game_top
        self.game_width = self.app.game_width
        self.game_height = self.app.game_height
        self.scale_x = self.app.scale_x
        self.scale_y = self.app.scale_y
        self.search_area_base = {'left': 500, 'top': 500, 'width': 1920, 'height': 1080}
        self.update_search_area()
        self.targets = [('d{}'.format(i), 1 if i == 1 else 2) for i in range(1, 21)]
        self.threshold = 0.9
        self.setup_gui()

    def update_search_area(self):
        half_width = 500
        center_x = self.app.game_left + self.app.game_width / 2
        center_y = self.app.game_top + self.app.game_height / 2

        desired_left = center_x - half_width
        desired_top = center_y - half_width
        desired_right = center_x + half_width
        desired_bottom = center_y + half_width

        search_left_int = int(round(max(self.app.game_left, desired_left)))
        search_top_int = int(round(max(self.app.game_top, desired_top)))
        search_right_int = int(round(min(self.app.game_left + self.app.game_width, desired_right)))
        search_bottom_int = int(round(min(self.app.game_top + self.app.game_height, desired_bottom)))

        search_width = search_right_int - search_left_int
        search_height = search_bottom_int - search_top_int

        self.search_area = {
            'left': search_left_int,
            'top': search_top_int,
            'width': search_width,
            'height': search_height
        }

    def setup_gui(self):
        stats_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR)
        stats_frame.pack(pady=5, fill=tk.X)
        self.status_label = tk.Label(stats_frame, text="Статус: Неактивен", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                    font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.status_label.pack()
        control_label = tk.Label(stats_frame, text="f5 - выполнить один цикл швейки", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        control_label.pack()
        self.stats_labels = [self.status_label]

    def toggle_bot(self):
        if not self.active:
            self.active = True
            self.status_label.config(text="Статус: Активен")
            threading.Thread(target=self.check_images, daemon=True).start()
            self.app.logger.log("DM швейка", "Выполнен один цикл по нажатию f5", "info")
        else:
            self.app.logger.log("Demorgan", "Бот уже выполняет цикл", "warning")

    def check_images(self):
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(self.search_area))
            screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            for target, clicks in self.targets:
                template = self.app.templates.get(target)
                if template is None:
                    self.app.logger.log("Demorgan", f"Ошибка: шаблон {target} не загружен", "error")
                    continue
                result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > self.threshold:
                    center_x = self.search_area['left'] + max_loc[0] + template.shape[1] // 2
                    center_y = self.search_area['top'] + max_loc[1] + template.shape[0] // 2
                    for _ in range(clicks):
                        pyautogui.click(center_x, center_y)
                        time.sleep(0.1)
                    self.app.logger.log("Demorgan", f"Найдено и кликнуто по {target} {clicks} раз(а)", "info")
        self.active = False
        self.status_label.config(text="Статус: Неактивен")
        
class DMTokarBot:
    def __init__(self, app):
        self.app = app
        self.frame = self.app.bot_frames['dmtokar']
        self.active = False
        self.last_known_position = None
        self.setup_gui()

    def setup_gui(self):
        stats_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        stats_frame.pack(pady=5, fill=tk.X)
        self.status_label = tk.Label(stats_frame, text="Статус: Неактивен", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.status_label.pack(expand=True)

        control_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR, bd=0, highlightthickness=0)
        control_frame.pack(anchor=tk.W, expand=True, pady=5)
        control_text = tk.Text(control_frame, wrap=tk.WORD, height=1, width=35, bd=0, bg=TEXT_BG_COLOR,
                               fg=TEXT_FG_COLOR, font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        control_text.configure(state='disabled')
        control_text.pack()

    def toggle_bot(self):
        if self.active:
            self.stop_bot()
            self.status_label.config(text="Статус: Неактивен")
        else:
            self.start_bot()
            self.status_label.config(text="Статус: Активен")

    def start_bot(self):
        self.active = True
        self.status_label.config(text="Статус: Активен")
        threading.Thread(target=self.tracking_loop, daemon=True).start()

    def stop_bot(self):
        self.active = False
        self.status_label.config(text="Статус: Неактивен")

    def tracking_loop(self):
        while self.active:
            with mss.mss() as sct:
                template = self.app.templates['toka']
                h, w = template.shape[:2]
                if self.last_known_position:
                    cx, cy_bottom = self.last_known_position
                    small_left = max(cx - 100, self.app.game_left)
                    small_top = max(cy_bottom - 100 - h // 2, self.app.game_top)
                    small_right = min(cx + 100, self.app.game_left + self.app.game_width)
                    small_bottom = min(cy_bottom + 100 - h // 2, self.app.game_top + self.app.game_height)
                    small_monitor = {"left": small_left, "top": small_top,
                                    "width": small_right - small_left, "height": small_bottom - small_top}
                    screenshot = np.array(sct.grab(small_monitor))
                    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                    result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    if max_val > 0.9:
                        found_x = small_left + max_loc[0] + w // 2
                        found_y_bottom = small_top + max_loc[1] + h
                        self.last_known_position = (found_x, found_y_bottom)
                        cursor_x = found_x
                        cursor_y = found_y_bottom + 30
                        pyautogui.moveTo(cursor_x, cursor_y)
                        time.sleep(0.01)
                        continue
                
                monitor = {"left": self.app.game_left, "top": self.app.game_top,
                        "width": self.app.game_width, "height": self.app.game_height}
                screenshot = np.array(sct.grab(monitor))
                screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > 0.9:
                    found_x = self.app.game_left + max_loc[0] + w // 2
                    found_y_bottom = self.app.game_top + max_loc[1] + h
                    self.last_known_position = (found_x, found_y_bottom)
                    cursor_x = found_x
                    cursor_y = found_y_bottom + 30
                    pyautogui.moveTo(cursor_x, cursor_y)
                    time.sleep(0.01)
                else:
                    self.last_known_position = None
                    time.sleep(0.05)
                    
class CookingBot:
    def __init__(self, app):
        self.app = app
        self.frame = self.app.bot_frames['cooking']
        self.active = False
        self.cycles_count = 0
        self.recipe_var = tk.StringVar()
        self.recipes = {
            "Смузи": ["ovoshi", "voda", "whisk"],
            "Рагу": ["myaso", "ovoshi", "voda", "fire"]
        }
        self.setup_gui()

    def setup_gui(self):
        selection_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR)
        selection_frame.pack(pady=5)
        label = tk.Label(selection_frame, text="Выберите рецепт:", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                         font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        label.pack(side=tk.LEFT)
        combobox = ttk.Combobox(selection_frame, textvariable=self.recipe_var,
                        values=list(self.recipes.keys()), state="readonly",
                        style='Antiafk.TCombobox')
        combobox.pack(side=tk.LEFT)

        status_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR)
        status_frame.pack(pady=5)
        self.status_label = tk.Label(status_frame, text="Статус: Неактивен", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.status_label.pack()
        self.cycles_label = tk.Label(status_frame, text="Циклы: 0", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', self.app.get_scaled_font_size(10), 'bold'))
        self.cycles_label.pack()

    def toggle_bot(self):
        if self.active:
            self.stop_bot()
            self.status_label.config(text="Статус: Неактивен")
        else:
            if not self.recipe_var.get():
                self.app.show_error("Ошибка", "Выберите рецепт")
                return
            self.start_bot()
            self.status_label.config(text="Статус: Активен")

    def start_bot(self):
        if not self.recipe_var.get():
            self.app.show_error("Ошибка", "Выберите рецепт")
            return
        recipe = self.recipe_var.get()
        ingredients = self.recipes[recipe]
        positions = {}
        for img in ingredients + ["startCoocking"]:
            pos = self.app.find_image(img)
            if pos:
                positions[img] = pos
            else:
                self.app.show_error("Ошибка", f"Не удалось найти {img}")
                return
        self.active = True
        self.status_label.config(text="Статус: Активен")
        threading.Thread(target=self.cooking_loop, args=(positions,), daemon=True).start()

    def stop_bot(self):
        self.active = False
        self.status_label.config(text="Статус: Неактивен")

    def cooking_loop(self, positions):
        while self.active:
            for img in positions:
                if img != "startCoocking":
                    coord = positions[img]
                    pyautogui.moveTo(coord[0], coord[1])
                    pyautogui.click(button='right')
                    time.sleep(0.1)
            start_coord = positions["startCoocking"]
            pyautogui.moveTo(start_coord[0], start_coord[1])
            pyautogui.click(button='left')
            self.cycles_count += 1
            self.app.root.after(0, lambda: self.cycles_label.config(text=f"Циклы: {self.cycles_count}"))
            time.sleep(6)

    def reset_stats(self):
        self.cycles_count = 0
        self.cycles_label.config(text="Циклы: 0")

class GymCNN(nn.Module):
    def __init__(self):
        super(GymCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 56 * 56, 128)
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 32 * 56 * 56)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class GymBot:
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.app = parent
        self.frame = self.app.bot_frames['gym']
        self.active = False
        self.mode_var = tk.StringVar(value="Качалка")
        self.food_cooldown = self.app.food_cooldown_var.get()  
        self.device = torch.device("cpu")
        model_path = get_resource_path('neyro/GymBot.pth')
        self.model = GymCNN().to(self.device)
        try:
            self.model.load_state_dict(torch.load(model_path))
            self.app.logger.log("Gym", "Модель успешно загружена", "info")
        except Exception as e:
            self.app.logger.log("Gym", f"Ошибка загрузки модели: {e}", "error")
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.sct = mss.mss()
        monitor = self.sct.monitors[1]  
        self.capture_region = {
            "left": monitor["width"] // 3,
            "top": monitor["height"] // 2,
            "width": monitor["width"] // 3,
            "height": monitor["height"] // 2
        }
        self.done_template = self.app.templates.get('done')
        self.dont_template = self.app.templates.get('dont')
        if self.done_template is None or self.dont_template is None:
            self.app.logger.log("Gym", "Предупреждение: шаблоны изображений не найдены", "warning")
        self.last_eat_time = 0
        self.setup_gui()


    def setup_gui(self):
        mode_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR)
        mode_frame.pack(pady=5)
        rb1 = tk.Radiobutton(mode_frame, text="Качалка", variable=self.mode_var, value="Качалка",
                             bg=FRAME_BG_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR,
                             font=('Roboto', 13, 'bold'))  
        rb1.pack(side=tk.LEFT)
        rb2 = tk.Radiobutton(mode_frame, text="Эспандер", variable=self.mode_var, value="Эспандер", state='disabled',
                             bg=FRAME_BG_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR,
                             font=('Roboto', 13, 'bold'))  
        rb2.pack(side=tk.LEFT)
        status_frame = tk.Frame(self.frame, bg=FRAME_BG_COLOR)
        status_frame.pack(pady=5)
        self.status_label = tk.Label(status_frame, text="Статус: Неактивен", bg=LABEL_BG_COLOR, fg=LABEL_FG_COLOR,
                                     font=('Roboto', 13, 'bold'))  
        self.status_label.pack()

    def toggle_bot(self):
        if self.active:
            self.stop_bot()
            self.status_label.config(text="Статус: Неактивен")
            self.app.logger.log("GymBot", "Остановка GymBot", "info")
        else:
            self.start_bot()
            self.status_label.config(text="Статус: Активен")
            self.app.logger.log("GymBot", "Запуск GymBot", "info")

    def start_bot(self):
        self.active = True
        self.last_eat_time = time.time()
        if not self.app.hotkeys['eat']['key']:
            print("Предупреждение: клавиша еды не установлена, еда не будет использоваться")
        self.press_key('f5')
        threading.Thread(target=self.bot_loop, daemon=True).start()

    def stop_bot(self):
        self.active = False

    def press_key(self, key_str):
        if not key_str:
            return
        try:
            controller = KeyboardController()
            if key_str.lower() in Key.__members__:
                key = Key[key_str.lower()]
            else:
                key = KeyCode.from_char(key_str.lower())
            controller.press(key)
            time.sleep(0.05)
            controller.release(key)
        except Exception as e:
            self.app.logger.log("Gym", f"Ошибка при нажатии клавиши {key_str}: {e}", "error")
        
    def bot_loop(self):
        last_press_time = 0
        while self.active:
            try:
                self.app.logger.log("Gym", "Начинаю итерацию цикла", "debug")
                print("GymBot: Starting loop iteration")  

                start_capture = time.time()
                with mss.mss() as sct:
                    screenshot = sct.grab(self.capture_region)
                img = np.array(screenshot)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
                start_template = time.time()
                try:
                    done_found = self.find_template(self.done_template, img_gray)
                    dont_found = self.find_template(self.dont_template, img_gray)
                    print(f"GymBot: Template search took {time.time() - start_template:.2f} sec, done: {done_found}, dont: {dont_found}")
                except Exception as e:
                    print(f"GymBot: Error in find_template: {e}")
                    
                self.app.logger.log("Gym", f"Захват и обработка экрана заняли: {time.time() - start_capture:.2f} сек", "debug")
                print(f"GymBot: Capture took {time.time() - start_capture:.2f} sec")

                start_template = time.time()
                if self.find_template(self.done_template, img_gray) or self.find_template(self.dont_template, img_gray):
                    self.app.logger.log("Gym", "Обнаружен done/dont шаблон", "info")
                    if self.app.hotkeys['eat']['key'] and self.food_cooldown > 0 and time.time() - self.last_eat_time >= self.food_cooldown * 60:
                        if self.app.hotkeys['eat']['keycode'] is not None:
                            self.app.hotkeys['eat']['action']()
                        else:
                            self.app.logger.log("Gym", "Eat keycode not set, skipping eat", "warning")
                    time.sleep(33)
                    self.press_key('e')
                else:
                    start_transform = time.time()
                    img_tensor = self.transform(img_rgb).unsqueeze(0).to(self.device)
                    self.app.logger.log("Gym", f"Transform занял: {time.time() - start_transform:.2f} сек", "debug")
                    print(f"GymBot: Transform took {time.time() - start_transform:.2f} sec")

                    start_inference = time.time()
                    with torch.no_grad():
                        output = self.model(img_tensor)
                        prediction = torch.sigmoid(output).item()
                    self.app.logger.log("Gym", f"Prediction: {prediction:.4f}, занял: {time.time() - start_inference:.2f} сек", "info")
                    print(f"GymBot: Inference took {time.time() - start_inference:.2f} sec, Prediction: {prediction}")

                    if prediction >= 0.2000:
                        self.press_key('space')
                print("GymBot: Iteration completed")
            except Exception as e:
                self.app.logger.log("Gym", f"Ошибка в bot_loop: {e}", "error")
                print(f"GymBot Error: {e}")
                time.sleep(1)
            time.sleep(0.05)

    def find_template(self, template, img_gray):
        if template is None:
            return False
        
        if len(template.shape) == 3:
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        else:
            template_gray = template
        res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_val >= 0.8
              
if __name__ == "__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 12345))
        response = messagebox.askyesno("Программа уже запущенфа",
                                       "Программа уже запущена. Хотите закрыть предыдущий экземпляр и открыть новый?")
        if response:
            sock.send(b"shutdown")
            if sock.recv(1024).decode() == "ok":
                sock.close()
                app = MultiBotApp()
                app.start_socket_server()
                app.run()
            else:
                sock.close()
                sys.exit(1)
        else:
            sock.close()
            sys.exit(0)
    except socket.error as e:
        if os.name == 'nt' and not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.user32.MessageBoxW(0, "Запустите от администратора!", "Ошибка", 0x10)
            sys.exit(1)
        app = MultiBotApp()
        app.start_socket_server()
        app.run()
        time.sleep(1)