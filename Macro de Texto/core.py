import csv
import threading
from platform import system

import pyautogui
import pyperclip
from CTkMessagebox import CTkMessagebox
from customtkinter import filedialog
from pynput.keyboard import Key, Listener


class Core:

    def __init__(self, gui):
        self.gui = gui

        self.macro_activated = False
        self.configuration_has_changed = False

        self.pressed_keys = set()

        self.configure_buttons()
        self.define_keys()
        self.key_listener_thread()

    # ========== STARTING APP FUNCTIONS ==========

    def configure_buttons(self):
        self.gui.activate_button.configure(command=self.activate_macro)
        self.gui.deactivate_button.configure(command=self.deactivate_macro)

        self.gui.clear_entries_button.configure(command=self.clear_entries)

        self.gui.save_button.configure(command=self.save_configuration)
        self.gui.load_button.configure(command=self.load_configuration)

    def define_keys(self):
        if system() == "Darwin":
            self.ctrl_key = [Key.cmd, Key.cmd_l, Key.cmd_r]
        else:
            self.ctrl_key = [Key.ctrl, Key.ctrl_l, Key.ctrl_r]

        self.f_keys = [
            Key.f1,
            Key.f2,
            Key.f3,
            Key.f4,
            Key.f5,
            Key.f6,
            Key.f7,
            Key.f8,
            Key.f9,
            Key.f10,
            Key.f11,
            Key.f12,
        ]

    def key_listener_thread(self):
        key_listener_thread = threading.Thread(
            target=lambda: Listener(on_press=self.on_press, on_release=self.on_release).start()
        )
        key_listener_thread.daemon = True
        key_listener_thread.start()

    # ========== MACRO CONFIGURATION FUNCTIONS ==========

    def on_press(self, key):
        self.pressed_keys.add(key)

        ctrl_pressed = any(k in self.pressed_keys for k in self.ctrl_key)

        if self.macro_activated:
            for key_number, f_key in enumerate(self.f_keys):
                if f_key in self.pressed_keys:
                    self.paste_text(f_key, key_number)
        elif ctrl_pressed:
            for key_number, f_key in enumerate(self.f_keys):
                if f_key in self.pressed_keys:
                    self.entry_insert_selected_text(key_number)

    def on_release(self, key):
        self.pressed_keys.discard(key)

    def entry_insert_selected_text(self, key_number):
        self.gui.entries[key_number].delete(0, "end")
        self.gui.entries[key_number].insert(0, pyperclip.paste())
        self.gui.configuration_status.configure(text_color=self.gui.COLORS["disabled"], text="Configuração não salva")

    # ========== MACRO BUTTONS FUNCTIONS ==========

    def activate_macro(self):
        self.macro_activated = True

        self.gui.macro_status.configure(text_color=self.gui.COLORS["enabled"], text="Macro ativada")

        self.gui.activate_button.grid_remove()
        self.gui.deactivate_button.grid(row=1, column=0, pady=self.gui.pady, padx=30, sticky="ew")

    def deactivate_macro(self):
        self.macro_activated = False

        self.gui.macro_status.configure(text_color=self.gui.COLORS["disabled"], text="Macro desativada")

        self.gui.deactivate_button.grid_remove()
        self.gui.activate_button.grid(row=1, column=0, pady=self.gui.pady, padx=30, sticky="ew")

    def clear_entries(self):
        for key, entry in enumerate(self.gui.entries):
            entry.delete(0, "end")
            entry.configure(placeholder_text=f"(Ctrl + F{key + 1})")

        self.gui.configuration_status.configure(text_color=self.gui.COLORS["disabled"], text="Configuração não salva")

    def paste_text(self, key, key_number):
        content = self.gui.entries[key_number].get()

        if content:
            pyperclip.copy(content)

            if system() == "Darwin":
                pyautogui.hotkey("command", "v")
            else:
                pyautogui.hotkey("ctrl", "v")

        self.pressed_keys.discard(key)

    # ========== CONFIGURATIONS BUTTONS FUNCTIONS ==========

    def save_configuration(self):
        configuration_name = self.gui.configuration_name_entry.get()

        if not configuration_name:
            CTkMessagebox(
                title="Info!",
                message="Insira um nome para a configuração a ser salva!",
                icon="info",
            )
            return

        content = [configuration_name]
        for entry in self.gui.entries:
            content.append(entry.get())

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos csv", "*.csv"), ("Todos os arquivos", "*.*")],
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(content)

        self.gui.configuration_status.configure(text_color=self.gui.COLORS["enabled"], text="Configuração salva")

    def load_configuration(self):
        file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("Arquivos csv", "*.csv")])

        try:
            if file_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    content = next(reader)

                if len(content) < 13:
                    CTkMessagebox(
                        title="Erro!",
                        message="Arquivo de configuração com menos campos que o necessário!",
                        icon="cancel",
                    )
                    return

        except:
            CTkMessagebox(
                title="Erro!",
                message="Erro ao carregar dados do arquivo!",
                icon="cancel",
            )
            return

        self.gui.configuration_name_entry.delete(0, "end")
        self.gui.configuration_name_entry.insert(0, content[0])
        del content[0]

        for number, entry in enumerate(self.gui.entries):
            entry.delete(0, "end")
            entry.insert(0, content[number])

        self.gui.configuration_status.configure(text_color=self.gui.COLORS["enabled"], text="Configuração salva")
