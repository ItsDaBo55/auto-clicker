import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import keyboard
import json
import os

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")

        self.settings_file = "autoclicker_settings.json"
        self.load_settings()

        self.interval = tk.DoubleVar(value=self.settings.get("interval", 0.1))
        self.clicks = tk.IntVar(value=self.settings.get("clicks", 100))
        self.click_type = tk.StringVar(value=self.settings.get("click_type", "left"))
        self.keep_clicking = tk.BooleanVar(value=self.settings.get("keep_clicking", False))
        self.hotkey = tk.StringVar(value=self.settings.get("hotkey", "F8"))
        self.running = False
        self.stopped = True

        style = ttk.Style()
        style.configure("TLabel", padding=5)
        style.configure("TEntry", padding=5)
        style.configure("TButton", padding=5)
        style.configure("TCheckbutton", padding=5)

        ttk.Label(root, text="Click Interval (seconds):").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(root, textvariable=self.interval).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Number of Clicks:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(root, textvariable=self.clicks).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Click Type:").grid(row=2, column=0, padx=5, pady=5)
        ttk.OptionMenu(root, self.click_type, "left", "left", "right").grid(row=2, column=1, padx=5, pady=5)

        ttk.Checkbutton(root, text="Keep Clicking Until Stopped", variable=self.keep_clicking).grid(row=3, columnspan=2, padx=5, pady=5)

        ttk.Label(root, text="Start/Stop Hotkey:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(root, textvariable=self.hotkey).grid(row=4, column=1, padx=5, pady=5)

        self.start_button = ttk.Button(root, text="Start", command=self.start)
        self.start_button.grid(row=5, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop)
        self.stop_button.grid(row=5, column=1, padx=5, pady=5)

        self.set_hotkey()
        root.bind("<FocusOut>", lambda e: self.save_settings())
        root.bind("<Button-1>", lambda e: self.save_settings())

    def set_hotkey(self):
        keyboard.add_hotkey(self.hotkey.get(), self.toggle)

    def toggle(self):
        if self.running:
            if self.stopped == False:
                self.stopped == True
                self.stop()
        else:
            if self.stopped:
                self.stopped = False
                self.start()

    def start(self):
        if not self.running:
            self.running = True
            self.click_thread = threading.Thread(target=self.click)
            self.click_thread.start()
            messagebox.showinfo("Info", "Auto Clicker Started")

    def stop(self):
        if self.running:
            self.running = False
            if self.click_thread.is_alive():
                self.click_thread.join()
            messagebox.showinfo("Info", "Auto Clicker Stopped")

    def click(self):
        try:
            if self.keep_clicking.get():
                while self.running:
                    pyautogui.click(button=self.click_type.get())
                    time.sleep(self.interval.get())
            else:
                for _ in range(self.clicks.get()):
                    if not self.running:
                        break
                    pyautogui.click(button=self.click_type.get())
                    time.sleep(self.interval.get())
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.running = False

    def save_settings(self):
        self.settings = {
            "interval": self.interval.get(),
            "clicks": self.clicks.get(),
            "click_type": self.click_type.get(),
            "keep_clicking": self.keep_clicking.get(),
            "hotkey": self.hotkey.get(),
        }
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {}

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
