import re
import threading
from time import sleep

from CTkMessagebox import CTkMessagebox
from pyautogui import click, doubleClick
from pynput import keyboard, mouse


class Core:

    def __init__(self, gui):
        self.gui = gui

        self.configure_variables()
        self.configure_buttons()
        self.print_initial_slider_positions()
        self.key_listener_thread()

    # ========== STARTING APP FUNCTIONS ==========

    def configure_variables(self):
        self.f_keys = [
            keyboard.Key.f1,
            keyboard.Key.f2,
            keyboard.Key.f3,
            keyboard.Key.f4,
            keyboard.Key.f5,
            keyboard.Key.f6,
            keyboard.Key.f7,
            keyboard.Key.f8,
            keyboard.Key.f9,
            keyboard.Key.f10,
            keyboard.Key.f11,
            keyboard.Key.f12,
        ]

        self.listener = None

        self.clicking = False
        self.fixed_clicking = False
        self.recording = False
        self.double_click = False

        self.positions = []
        self.clicks_counter = 0

        self.position_key = self.f_keys[0]
        self.clicker_key = self.f_keys[1]
        self.fixed_clicker_key = self.f_keys[2]

    def configure_buttons(self):
        self.gui.positions_start.configure(command=self.start_recording_positions)
        self.gui.positions_end.configure(command=lambda: self.finish_recording_positions("click"))
        self.gui.reset_positions.configure(command=self.reset_positions)

        self.gui.start_button.configure(command=self.start_clicker)
        self.gui.finish_button.configure(command=self.finish_clicker)
        self.gui.reset_clicks.configure(command=self.reset_clicks)

        self.gui.fixed_clicker_start_button.configure(command=self.start_fixed_clicker)
        self.gui.fixed_clicker_finish_button.configure(command=self.finish_fixed_clicker)

        self.gui.clicks_delay_slider.configure(command=self.print_clicker_delay_values)
        self.gui.cycles_delay_slider.configure(command=self.print_cycles_delay_values)
        self.gui.fixed_clicks_delay_slider.configure(command=self.print_fixed_clicker_delay_values)

        self.gui.apply_button.configure(command=self.verify_shortcut_keys)

        self.gui.protocol("WM_DELETE_WINDOW", self.cleanup)

    def print_initial_slider_positions(self):
        self.print_clicker_delay_values(self.gui.clicks_delay_slider.get())
        self.print_cycles_delay_values(self.gui.cycles_delay_slider.get())
        self.print_fixed_clicker_delay_values(self.gui.fixed_clicks_delay_slider.get())

    def key_listener_thread(self):
        key_listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=self.on_press).start())
        key_listener_thread.daemon = True
        key_listener_thread.start()

    def on_press(self, key):
        if key == self.position_key:
            if self.recording:
                self.finish_recording_positions("keyboard")
            else:
                self.start_recording_positions()
        elif key == self.clicker_key:
            if self.clicking:
                self.finish_clicker()
            else:
                self.start_clicker()
        elif key == self.fixed_clicker_key:
            if self.fixed_clicking:
                self.finish_fixed_clicker()
            else:
                self.start_fixed_clicker()

    # ========== POSITIONS SECTION FUNCTIONS ==========

    def start_recording_positions(self):
        if self.clicking or self.fixed_clicking:
            return

        self.reset_positions()
        self.recording = True

        self.gui.positions_start.pack_forget()
        self.gui.positions_end.pack(side="left", padx=(70, 0))

        self.listener = mouse.Listener(on_click=self.record_position_on_click)
        self.listener.start()

    def finish_recording_positions(self, event):
        if self.clicking or self.fixed_clicking:
            return

        self.recording = False

        self.gui.positions_start.pack(side="left", padx=(70, 0))
        self.gui.positions_end.pack_forget()

        self.listener.stop()

        if event == "click" and self.positions:
            self.positions.pop()
            self.count_positions()

    def record_position_on_click(self, x, y, button, pressed):
        button = str(button).split(".")[1]

        if pressed:
            self.positions.append((button, x, y))
            self.count_positions()

    def count_positions(self):
        self.gui.positions_counter.configure(text=f"Total de posições: {len(self.positions)}")

    def reset_positions(self):
        if self.clicking or self.fixed_clicking:
            return

        self.positions = []
        self.count_positions()

    # ========== STANDARD FUNCTIONS FOR BOTH CLICKERS ==========

    def start_clicker_thread(self, target):
        self.clicker_thread = threading.Thread(target=target)
        self.clicker_thread.daemon = True
        self.clicker_thread.start()

    def increase_clicks(self):
        self.clicks_counter += 1
        self.gui.clicks_counter.configure(text=f"Total de cliques: {self.clicks_counter}")

    def reset_clicks(self):
        self.clicks_counter = 0
        self.gui.clicks_counter.configure(text=f"Total de cliques: {self.clicks_counter}")

    # ========== CLICKER SECTION FUNCTIONS ==========

    def start_clicker(self):
        if self.recording or self.fixed_clicking:
            return

        if not self.positions:
            CTkMessagebox(
                title="Info!",
                message="Não há posições definidas para o Clicker funcionar!",
                icon="info",
            )
            return

        self.clicking = True
        double_click = self.gui.double_click_checkbox.get()

        self.gui.start_button.pack_forget()
        self.gui.finish_button.pack(side="left", padx=(70, 0))

        if double_click:
            self.start_clicker_thread(self.double_clicker)
        else:
            self.start_clicker_thread(self.clicker)

    def finish_clicker(self):
        if self.recording or self.fixed_clicking:
            return

        self.clicking = False

        self.gui.start_button.pack(side="left", padx=(70, 0))
        self.gui.finish_button.pack_forget()

    def clicker(self):
        clicks_delay = self.gui.clicks_delay_slider.get()
        cycles_delay = self.gui.cycles_delay_slider.get()

        while self.clicking:
            for button, x, y in self.positions:
                if not self.clicking:
                    break
                click(x, y, button=button)
                self.increase_clicks()
                sleep(clicks_delay)
            sleep(cycles_delay)

    def double_clicker(self):
        clicks_delay = self.gui.clicks_delay_slider.get()
        cycles_delay = self.gui.cycles_delay_slider.get()

        while self.clicking:
            for button, x, y in self.positions:
                if not self.clicking:
                    break
                doubleClick(x, y, button=button)
                self.increase_clicks()
                self.increase_clicks()
                sleep(clicks_delay)
            sleep(cycles_delay)

    def print_clicker_delay_values(self, value):
        self.gui.clicks_delay_value.configure(text=f"Intervalo cliques: ({value:.3f})")

    def print_cycles_delay_values(self, value):
        self.gui.cycles_delay_value.configure(text=f"Intervalo ciclos: ({value:.3f})")

    # ========== FIXED CLICKER SECTION FUNCTIONS ==========

    def start_fixed_clicker(self):
        if self.recording or self.clicking:
            return

        self.fixed_clicking = True
        double_click = self.gui.fixed_double_click_checkbox.get()

        self.gui.fixed_clicker_start_button.pack_forget()
        self.gui.fixed_clicker_finish_button.pack(pady=5)

        if double_click:
            self.start_clicker_thread(self.fixed_double_clicker)
        else:
            self.start_clicker_thread(self.fixed_clicker)

    def finish_fixed_clicker(self):
        if self.recording or self.clicking:
            return

        self.fixed_clicking = False

        self.gui.fixed_clicker_finish_button.pack_forget()
        self.gui.fixed_clicker_start_button.pack(pady=5)

    def fixed_clicker(self):
        delay = self.gui.fixed_clicks_delay_slider.get()

        while self.fixed_clicking:
            click(button="left")
            self.increase_clicks()
            sleep(delay)

    def fixed_double_clicker(self):
        delay = self.gui.fixed_clicks_delay_slider.get()

        while self.fixed_clicking:
            doubleClick(button="left")
            self.increase_clicks()
            self.increase_clicks()
            sleep(delay)

    def print_fixed_clicker_delay_values(self, value):
        self.gui.fixed_clicks_delay_value.configure(text=f"Intervalo cliques: ({value:.3f})")

    # ========== SHORTCUT KEYS SECTION FUNCTIONS ==========

    def verify_shortcut_keys(self):
        self.verify_position_shortcut_key()
        self.verify_clicker_shortcut_key()
        self.verify_fixed_clicker_shortcut_key()

    def verify_position_shortcut_key(self):
        value = self.gui.position_key_entry.get()

        if not value or not self.verify_valid_value(value):
            return

        key = int(value[1:]) - 1
        f_key = self.f_keys[key]
        if self.clicker_key == f_key or self.fixed_clicker_key == f_key:
            CTkMessagebox(
                title="Info!",
                message="O atalho para o controle das posições não foi alterado por conflitar com outro atalho",
                icon="info",
            )
            return False
        self.position_key = f_key
        self.gui.position_key_entry.delete(0, "end")
        self.gui.position_key_entry.configure(placeholder_text=value.upper())

    def verify_clicker_shortcut_key(self):
        value = self.gui.clicker_key_entry.get()

        if not value or not self.verify_valid_value(value):
            return

        key = int(value[1:]) - 1
        f_key = self.f_keys[key]
        if self.position_key == f_key or self.fixed_clicker_key == f_key:
            CTkMessagebox(
                title="Info!",
                message="O atalho para o controle do clicker não foi alterado por conflitar com outro atalho",
                icon="info",
            )
            return False
        self.clicker_key = f_key
        self.gui.clicker_key_entry.delete(0, "end")
        self.gui.clicker_key_entry.configure(placeholder_text=value.upper())

    def verify_fixed_clicker_shortcut_key(self):
        value = self.gui.fixed_clicker_key_entry.get()

        if not value or not self.verify_valid_value(value):
            return

        key = int(value[1:]) - 1
        f_key = self.f_keys[key]
        if self.position_key == f_key or self.clicker_key == f_key:
            CTkMessagebox(
                title="Info!",
                message="O atalho para o controle do clicker fixo não foi alterado por conflitar com outro atalho",
                icon="info",
            )
            return False
        self.fixed_clicker_key = f_key
        self.gui.fixed_clicker_key_entry.delete(0, "end")
        self.gui.fixed_clicker_key_entry.configure(placeholder_text=value.upper())

    def verify_valid_value(self, value):
        value = value.strip().upper()

        if re.match("^F(1[0-2]|[1-9])$", value):
            return True
        else:
            CTkMessagebox(
                title="Info!",
                message="Valores possíveis:\nF1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12",
                icon="info",
            )
            return False

    # ========== FINISHING APP FUNCTIONS ==========

    def cleanup(self):
        self.clicking = False
        self.fixed_clicking = False
        self.recording = False

        if self.listener:
            self.listener.stop()

        self.gui.destroy()
