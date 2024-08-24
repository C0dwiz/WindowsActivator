import json
import os
from customtkinter import *
from os import system as cmd

KEYS = {
    "Home Edition": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
    "Home N Edition": "3KHY7-WNT83-DGQKR-F7HPR-844BM",
    "Home Single Language": "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",
    "Home Country Specific": "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR",
    "Professional Edition": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
    "Professional N Edition": "MH37W-N47XK-V7XM9-C7227-GCQG9",
    "Education Edition": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
    "Education N Edition": "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ",
    "Enterprise Edition": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
    "Enterprise N Edition": "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",
}

CONFIG_FILE = "config.json"


class WindowsActivatorApp:
    def __init__(self):
        self.enabled = False
        self.language = "English"

        self.win = CTk()
        self.win.title("Windows Activator")
        self.win.geometry("450x400")
        self.win.resizable(False, False)

        self.create_widgets()

        if os.path.exists(CONFIG_FILE):
            self.load_config()

        self.win.mainloop()

    def create_widgets(self):
        title = CTkLabel(self.win, text="Windows Activator", font=("Impact", 20))
        title.place(x=125, y=50)

        self.option_menu = CTkOptionMenu(
            self.win, values=list(KEYS.keys()) + ["Custom"]
        )
        self.option_menu.configure(height=30, width=400)
        self.option_menu.place(x=25, y=150)

        self.custom_key_switch = CTkSwitch(
            self.win, text="Custom Key", command=self.toggle_custom_key
        )
        self.custom_key_switch.place(x=25, y=245)

        self.custom_key = CTkEntry(
            self.win,
            placeholder_text="Enter Custom Key...",
            height=30,
            width=400,
            state="disabled",
        )
        self.custom_key.place(x=25, y=275)

        self.activate_btn = CTkButton(
            self.win, text="Activate", font=("Impact", 15), command=self.activate
        )
        self.activate_btn.configure(height=30, width=400)
        self.activate_btn.place(x=25, y=310)
        settings_btn = CTkButton(self.win, text="⚙️", command=self.open_settings)
        settings_btn.configure(height=25, width=25)
        settings_btn.place(x=10, y=10)

    def activate(self):
        """Активация Windows с заданным ключом."""
        selection = self.option_menu.get()
        key = KEYS.get(selection, self.custom_key.get() if self.enabled else None)

        if key:
            cmd(f"slmgr /ipk {key}")
            cmd(f"slmgr /skms kms8.msguides.com")
            cmd("slmgr /ato")

    def toggle_custom_key(self):
        """Переключить использование пользовательского ключа."""
        self.enabled = not self.enabled
        state = "normal" if self.enabled else "disabled"
        placeholder = "Enter Custom Key..." if self.enabled else ""

        self.custom_key.configure(placeholder_text=placeholder, state=state)

    def open_settings(self):
        """Открыть окно настроек для изменения темы и языка интерфейса."""
        self.settings_window = CTkToplevel(self.win)
        self.settings_window.title("Settings")
        self.settings_window.geometry("300x200")

        theme_label = CTkLabel(self.settings_window, text="Choose Theme:")
        theme_label.pack(pady=(10, 0))

        self.theme_option = CTkOptionMenu(
            self.settings_window, values=["Dark", "Light"], command=self.change_theme
        )
        self.theme_option.pack(pady=10)

        language_label = CTkLabel(self.settings_window, text="Choose Language:")
        language_label.pack(pady=(10, 0))

        self.language_option = CTkOptionMenu(
            self.settings_window,
            values=["English", "Русский"],
            command=self.change_language,
        )
        self.language_option.pack(pady=10)

    def change_theme(self, theme):
        """Изменить тему интерфейса и сохранить настройки."""
        set_appearance_mode(theme.lower())
        self.save_config(theme=theme.lower(), lang=self.language)

    def change_language(self, language):
        """Изменить язык интерфейса и сохранить настройки."""
        self.language = language

        if language == "English":
            self.option_menu.configure(values=list(KEYS.keys()) + ["Custom"])
            self.custom_key_switch.configure(text="Custom Key")
            self.activate_btn.configure(text="Activate")
            self.custom_key.configure(placeholder_text="Enter Custom Key...")
        elif language == "Русский":
            self.option_menu.configure(
                values=[key + " (Рус)" for key in KEYS.keys()] + ["Пользовательский"]
            )
            self.custom_key_switch.configure(text="Пользовательский ключ")
            self.activate_btn.configure(text="Активировать")
            self.custom_key.configure(placeholder_text="Ведите кастомный ключ...")

        self.save_config(theme=self.language, lang=self.language)

    def load_config(self):
        """Загрузить конфигурацию из файла."""
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
            set_appearance_mode(config.get("theme", "dark"))
            self.language = config.get("language", "English")

            self.change_language(self.language)

    def save_config(self, theme, lang):
        """Сохранить конфигурацию в файл."""
        config = {"theme": theme, "language": lang}
        with open(CONFIG_FILE, "w") as config_file:
            json.dump(config, config_file)


if __name__ == "__main__":
    WindowsActivatorApp()
