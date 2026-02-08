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
            "text": "#ffffff",
        }

        self.FONTS = {
            "text": ("Arial", 14),
            "button": ("Arial", 16, "bold"),
        }

        self.height = 40
        self.pady = 5
        self.code_size = 330

        self.build()

    def build(self):
        self.title("Gerador de QR Code")
        self.geometry("500x570")
        self.resizable(False, False)

        self.build_entry_section()
        self.build_qr_code_size_section()
        self.build_qr_code_section()
        self.build_buttons_section()

    def build_entry_section(self):
        entry_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        entry_container.pack(fill="x", pady=self.pady, padx=10)

        ctk.CTkLabel(
            entry_container,
            text="Insira um texto, link ou arquivo para gerar um QR Code:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).pack(pady=self.pady, padx=30)

        self.text_entry = ctk.CTkEntry(
            entry_container,
            height=self.height,
            width=340,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="Digite ou insira o conteúdo...",
        )
        self.text_entry.pack(side="left", pady=self.pady, padx=(20, 0))

        self.file_button = ctk.CTkButton(
            entry_container,
            height=self.height,
            width=40,
            text="Procurar",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.file_button.pack(side="right", pady=self.pady, padx=(0, 20))

    def build_qr_code_size_section(self):
        qr_code_size_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        qr_code_size_container.pack(fill="x", pady=self.pady, padx=10)

        for i in range(3):
            qr_code_size_container.grid_columnconfigure(i, weight=1)

        self.qr_code_size_value = ctk.CTkLabel(
            qr_code_size_container,
            text="Tamanho da imagem:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        )
        self.qr_code_size_value.grid(row=0, column=0, pady=self.pady)

        self.qr_code_size_slider = ctk.CTkSlider(
            qr_code_size_container, width=150, from_=24, to=330, number_of_steps=330 - 24
        )
        self.qr_code_size_slider.grid(row=0, column=1, pady=self.pady)
        self.qr_code_size_slider.set(330)

    def build_qr_code_section(self):
        code_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        code_container.pack(fill="x", pady=self.pady, padx=10)

        self.code_label = ctk.CTkLabel(
            code_container,
            image=None,
            text="Código a ser gerado...",
            height=self.code_size,
            width=self.code_size,
            fg_color=self.COLORS["primary_bg"],
        )
        self.code_label.pack(pady=self.pady, padx=30)

    def build_buttons_section(self):
        button_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        button_container.pack(fill="x", pady=self.pady, padx=10)

        for i in range(3):
            button_container.columnconfigure(i, weight=1)

        self.generate_button = ctk.CTkButton(
            button_container,
            height=self.height,
            text="Gerar Código",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.generate_button.grid(row=0, column=0, pady=self.pady)

        self.clean_button = ctk.CTkButton(
            button_container,
            height=self.height,
            text="Limpar Tudo",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.clean_button.grid(row=0, column=1, pady=self.pady)

        self.save_button = ctk.CTkButton(
            button_container,
            height=self.height,
            text="Salvar Código",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["primary_bg"],
            state="disabled",
        )
        self.save_button.grid(row=0, column=2, pady=self.pady)
