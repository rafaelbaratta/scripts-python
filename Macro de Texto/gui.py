import customtkinter as ctk


class Gui(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")

        self.COLORS = {
            "primary_bg": "#242424",
            "secondary_bg": "#2e2e2e",
            "button": "#bb4f02",
            "button_hover": "#ce5804",
            "button_text": "#ffffff",
            "button_enable": "#005500",
            "button_hover_enable": "#007700",
            "button_disable": "#aa0000",
            "button_hover_disable": "#bb0000",
            "text": "#ffffff",
            "enabled": "#00ff00",
            "disabled": "#ff6666",
        }

        self.FONTS = {
            "title": ("Arial", 28, "bold"),
            "text": ("Arial", 14),
            "message": ("Arial", 12),
            "button": ("Arial", 16, "bold"),
        }

        self.height = 40
        self.pady = 5
        self.f_keys = ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12")

        self.build()

    def build(self):
        self.title("Macro de Texto")
        self.geometry("500x590")
        self.resizable(False, False)

        self.build_macro_configuration_section()
        self.build_macro_buttons_section()
        self.build_configuration_buttons_section()

    def build_macro_configuration_section(self):
        macro_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        macro_container.pack(fill="x", pady=self.pady, padx=10)

        ctk.CTkLabel(
            macro_container,
            text="Configurações da Macro",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).pack(pady=self.pady)

        self.macro_status = ctk.CTkLabel(
            macro_container,
            text="Macro desativada",
            font=self.FONTS["text"],
            text_color=self.COLORS["disabled"],
        )
        self.macro_status.pack()

        self.configuration_status = ctk.CTkLabel(
            macro_container,
            text="Configuração não salva",
            font=self.FONTS["text"],
            text_color=self.COLORS["disabled"],
        )
        self.configuration_status.pack(pady=self.pady)

        texts_container = ctk.CTkFrame(macro_container, fg_color="transparent")
        texts_container.pack(fill="x")

        for i in range(4):
            if i % 2 == 0:
                texts_container.grid_columnconfigure(i, weight=0)
            else:
                texts_container.grid_columnconfigure(i, weight=1)

        self.entries = []
        for i, key in enumerate(self.f_keys):
            row, column_label, column_entry = (i + 1, 0, 1) if i <= 5 else (i - 5, 2, 3)

            ctk.CTkLabel(
                texts_container,
                text=f"{key}:",
                font=self.FONTS["text"],
                text_color=self.COLORS["text"],
            ).grid(row=row, column=column_label, pady=self.pady, padx=5)

            self.entries.append(
                ctk.CTkEntry(
                    texts_container,
                    font=self.FONTS["text"],
                    text_color=self.COLORS["text"],
                    fg_color=self.COLORS["primary_bg"],
                    placeholder_text=f"(Ctrl + {key})",
                )
            )
            self.entries[i].grid(sticky="ew", row=row, column=column_entry, pady=self.pady, padx=5)

    def build_macro_buttons_section(self):
        macro_buttons_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        macro_buttons_container.pack(fill="x", pady=self.pady, padx=10)

        macro_buttons_container.grid_columnconfigure(0, weight=1)
        macro_buttons_container.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            macro_buttons_container,
            text="Botões de Controle da Macro",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(row=0, column=0, columnspan=2, pady=self.pady)

        self.activate_button = ctk.CTkButton(
            macro_buttons_container,
            height=self.height,
            text="Ativar Macro",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button_enable"],
            hover_color=self.COLORS["button_hover_enable"],
        )
        self.activate_button.grid(row=1, column=0, pady=self.pady, padx=30, sticky="ew")

        self.deactivate_button = ctk.CTkButton(
            macro_buttons_container,
            height=self.height,
            text="Desativar Macro",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button_disable"],
            hover_color=self.COLORS["button_hover_disable"],
        )

        self.clear_entries_button = ctk.CTkButton(
            macro_buttons_container,
            height=self.height,
            text="Limpar Campos",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.clear_entries_button.grid(row=1, column=1, pady=self.pady, padx=30, sticky="ew")

    def build_configuration_buttons_section(self):
        configurations_buttons_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        configurations_buttons_container.pack(fill="x", pady=self.pady, padx=10)

        configurations_buttons_container.grid_columnconfigure(0, weight=1)
        configurations_buttons_container.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            configurations_buttons_container,
            text="Botões de Controle de Configurações",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(row=0, column=0, columnspan=2, pady=self.pady)

        self.configuration_name_entry = ctk.CTkEntry(
            configurations_buttons_container,
            height=self.height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            fg_color=self.COLORS["primary_bg"],
            placeholder_text="Nome da configuração",
        )
        self.configuration_name_entry.grid(row=1, column=0, columnspan=2, pady=self.pady, padx=30, sticky="ew")

        self.save_button = ctk.CTkButton(
            configurations_buttons_container,
            height=self.height,
            text="Salvar Configuração",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.save_button.grid(row=2, column=0, pady=self.pady, padx=30, sticky="ew")

        self.load_button = ctk.CTkButton(
            configurations_buttons_container,
            height=self.height,
            text="Carregar Configuração",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.load_button.grid(row=2, column=1, pady=self.pady, padx=30, sticky="ew")
