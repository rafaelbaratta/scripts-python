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
            "text": ("Arial", 14),
            "message": ("Arial", 12),
            "button": ("Arial", 16, "bold"),
        }

        self.height = 40
        self.pady = 5
        self.edit_entry_height = 30
        self.checkbox_size = 20
        self.checkbox_border = 2

        self.build()

    def build(self):
        self.title("Renomeador de Arquivos")
        self.geometry("500x610")
        self.resizable(False, False)

        self.build_path_section()
        self.build_standard_name_section()
        self.build_options_section()
        self.build_buttons_section()

    def build_path_section(self):
        entry_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        entry_container.pack(fill="both", pady=self.pady, padx=10)

        ctk.CTkLabel(
            entry_container,
            text="Insira ou procure o caminho da pasta/diretório dos arquivos:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).pack(pady=self.pady, padx=30)

        self.path_entry = ctk.CTkEntry(
            entry_container,
            width=340,
            height=self.height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        )
        self.path_entry.pack(side="left", pady=self.pady, padx=(20, 0))

        self.directory_button = ctk.CTkButton(
            entry_container,
            height=self.height,
            width=40,
            text="Procurar",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.directory_button.pack(side="right", pady=self.pady, padx=(0, 20))

    def build_standard_name_section(self):
        standard_name_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        standard_name_container.pack(fill="both", padx=10, pady=self.pady)

        ctk.CTkLabel(
            standard_name_container,
            text="Nomear arquivos com texto padrão:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).pack(pady=self.pady)

        self.standard_name_entry = ctk.CTkEntry(
            standard_name_container,
            width=400,
            height=self.edit_entry_height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="Nome padrão para todos os arquivos",
        )
        self.standard_name_entry.pack(pady=self.pady, padx=20)

        self.standard_name_checkbox = ctk.CTkCheckBox(
            standard_name_container,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text="Nomear todos arquivos com um texto padrão?",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.standard_name_checkbox.pack(pady=self.pady, padx=20)

    def build_options_section(self):
        options_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        options_container.pack(fill="both", pady=self.pady, padx=10)

        options_container.grid_columnconfigure(0, weight=1)
        options_container.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            options_container,
            text="Escolha as opções para renomear os arquivos:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(column=0, row=0, columnspan=2, pady=self.pady, padx=20, sticky="nsew")

        ctk.CTkLabel(
            options_container,
            text="Adicionar Texto:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(column=0, row=1, pady=self.pady, padx=25, sticky="w")

        insert_container = ctk.CTkFrame(options_container, fg_color="transparent")
        insert_container.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.insert_entry = ctk.CTkEntry(
            insert_container,
            width=350,
            height=self.edit_entry_height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="Texto a ser adicionado",
        )
        self.insert_entry.pack(padx=(20, 5), side="left")

        self.position_insert_entry = ctk.CTkEntry(
            insert_container,
            width=100,
            height=self.edit_entry_height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="Posição",
        )
        self.position_insert_entry.pack(padx=(5, 20), side="right")

        ctk.CTkLabel(
            options_container,
            text="Remover Texto:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(column=0, row=4, pady=self.pady, padx=25, sticky="w")

        self.remove_entry = ctk.CTkEntry(
            options_container,
            width=400,
            height=self.edit_entry_height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="Texto a ser removido",
        )
        self.remove_entry.grid(column=0, row=5, columnspan=2, padx=20, sticky="nsew")

        ctk.CTkLabel(
            options_container,
            text="Substituir Texto:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(column=0, row=6, pady=self.pady, padx=25, sticky="w")

        self.text_to_be_replaced_entry = ctk.CTkEntry(
            options_container,
            width=400,
            height=self.edit_entry_height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="Texto a ser substituído",
        )
        self.text_to_be_replaced_entry.grid(column=0, row=7, padx=(20, 5), sticky="nsew")

        self.text_to_replace_entry = ctk.CTkEntry(
            options_container,
            width=400,
            height=self.edit_entry_height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="Texto substituto",
        )
        self.text_to_replace_entry.grid(column=1, row=7, columnspan=2, padx=(5, 20), sticky="nsew")

        ctk.CTkLabel(
            options_container,
            text="Adicionar Prefixo/Sufixo:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(column=0, row=8, pady=self.pady, padx=25, sticky="w")

        self.prefix_entry = ctk.CTkEntry(
            options_container,
            width=400,
            height=self.edit_entry_height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="Prefixo a ser adicionado",
        )
        self.prefix_entry.grid(column=0, row=9, pady=self.pady, padx=(20, 5), sticky="nsew")

        self.suffix_entry = ctk.CTkEntry(
            options_container,
            width=400,
            height=self.edit_entry_height,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="Sufixo a ser adicionado",
        )
        self.suffix_entry.grid(column=1, row=9, pady=self.pady, padx=(5, 20), sticky="nsew")

    def build_buttons_section(self):
        self.rename_button = ctk.CTkButton(
            self,
            height=self.height,
            text="Renomear Arquivos",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.rename_button.pack(side="left", pady=self.pady, padx=(70, 0))

        self.clear_fields_button = ctk.CTkButton(
            self,
            height=self.height,
            text="  Limpar Campos  ",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.clear_fields_button.pack(side="right", pady=self.pady, padx=(0, 70))
