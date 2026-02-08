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
            "message": ("Arial", 12),
            "button": ("Arial", 16, "bold"),
        }

        self.height = 40
        self.pady = 5

        self.build()

    def build(self):
        self.title("Auto Clicker")
        self.geometry("500x620")
        self.resizable(False, False)

        self.build_positions_section()
        self.build_clicker_section()
        self.build_fixed_clicker_section()
        self.build_shortcut_keys_section()

    def build_positions_section(self):
        positions_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        positions_container.pack(fill="x", pady=self.pady, padx=10)

        ctk.CTkLabel(
            positions_container,
            text="Pressione o botão para gravar as posições dos cliques",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).pack(pady=self.pady, padx=30)

        self.positions_counter = ctk.CTkLabel(
            positions_container,
            width=400,
            text="Total de posições: 0",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            fg_color=self.COLORS["primary_bg"],
        )
        self.positions_counter.pack(pady=self.pady, padx=30)

        positions_buttons_frame = ctk.CTkFrame(positions_container, fg_color="transparent")
        positions_buttons_frame.pack(fill="x", pady=self.pady, padx=10)

        self.positions_start = ctk.CTkButton(
            positions_buttons_frame,
            height=self.height,
            text="Gravar Posições",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.positions_start.pack(side="left", padx=(70, 0))

        self.positions_end = ctk.CTkButton(
            positions_buttons_frame,
            height=self.height,
            text="Parar de Gravar",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )

        self.reset_positions = ctk.CTkButton(
            positions_buttons_frame,
            height=self.height,
            text="Resetar Posições",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.reset_positions.pack(side="right", padx=(0, 70))

    def build_clicker_section(self):
        clicker_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        clicker_container.pack(fill="x", pady=self.pady, padx=10)

        ctk.CTkLabel(
            clicker_container,
            text="Controles para o 'Auto Clicker' nas posições gravadas",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).pack(pady=self.pady, padx=30)

        self.clicks_counter = ctk.CTkLabel(
            clicker_container,
            width=400,
            text="Total de cliques: 0",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            fg_color=self.COLORS["primary_bg"],
        )
        self.clicks_counter.pack(pady=self.pady, padx=30)

        options_container = ctk.CTkFrame(clicker_container, fg_color="transparent")
        options_container.pack(fill="x")

        for i in range(3):
            options_container.grid_columnconfigure(i, weight=1)

        self.clicks_delay_value = ctk.CTkLabel(
            options_container,
            text="Intervalo cliques:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        )
        self.clicks_delay_value.grid(row=0, column=0, pady=self.pady)

        self.clicks_delay_slider = ctk.CTkSlider(options_container, width=150, from_=0.001, to=120.0)
        self.clicks_delay_slider.grid(row=0, column=1, pady=self.pady)
        self.clicks_delay_slider.set(5)

        self.cycles_delay_value = ctk.CTkLabel(
            options_container,
            text="Intervalo ciclos:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        )
        self.cycles_delay_value.grid(row=1, column=0, pady=self.pady)

        self.cycles_delay_slider = ctk.CTkSlider(options_container, width=150, from_=0.001, to=120.0)
        self.cycles_delay_slider.grid(row=1, column=1, pady=self.pady)
        self.cycles_delay_slider.set(5)

        self.double_click_checkbox = ctk.CTkCheckBox(
            options_container,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text="Duplo Clique?",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.double_click_checkbox.grid(row=0, column=2, rowspan=2)

        clicker_buttons_frame = ctk.CTkFrame(clicker_container, fg_color="transparent")
        clicker_buttons_frame.pack(fill="x", pady=self.pady, padx=10)

        self.start_button = ctk.CTkButton(
            clicker_buttons_frame,
            height=self.height,
            text="Iniciar Clicker",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.start_button.pack(side="left", padx=(70, 0))

        self.finish_button = ctk.CTkButton(
            clicker_buttons_frame,
            height=self.height,
            text="Encerrar Clicker",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )

        self.reset_clicks = ctk.CTkButton(
            clicker_buttons_frame,
            height=self.height,
            text="Resetar Clicks",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.reset_clicks.pack(side="right", padx=(0, 70))

    def build_fixed_clicker_section(self):
        fixed_clicker_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        fixed_clicker_container.pack(fill="x", pady=self.pady, padx=10)

        ctk.CTkLabel(
            fixed_clicker_container,
            text="Controles para o 'Auto Clicker' fixo na posição do mouse",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).pack(pady=self.pady, padx=30)

        options_container = ctk.CTkFrame(fixed_clicker_container, fg_color="transparent")
        options_container.pack(fill="x")

        for i in range(3):
            options_container.grid_columnconfigure(i, weight=1)

        self.fixed_clicks_delay_value = ctk.CTkLabel(
            options_container,
            text="Intervalo cliques:",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        )
        self.fixed_clicks_delay_value.grid(row=0, column=0, pady=self.pady)

        self.fixed_clicks_delay_slider = ctk.CTkSlider(options_container, width=150, from_=0.001, to=120.0)
        self.fixed_clicks_delay_slider.grid(row=0, column=1, pady=self.pady)
        self.fixed_clicks_delay_slider.set(5)

        self.fixed_double_click_checkbox = ctk.CTkCheckBox(
            options_container,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text="Duplo Clique?",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.fixed_double_click_checkbox.grid(row=0, column=2)

        fixed_clicker_buttons_frame = ctk.CTkFrame(fixed_clicker_container, fg_color="transparent")
        fixed_clicker_buttons_frame.pack(fill="x", padx=10)

        self.fixed_clicker_start_button = ctk.CTkButton(
            fixed_clicker_buttons_frame,
            height=self.height,
            text="Iniciar Clicker",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.fixed_clicker_start_button.pack(pady=self.pady)

        self.fixed_clicker_finish_button = ctk.CTkButton(
            fixed_clicker_buttons_frame,
            height=self.height,
            text="Encerrar Clicker",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )

    def build_shortcut_keys_section(self):
        shortcut_keys_container = ctk.CTkFrame(self, fg_color=self.COLORS["secondary_bg"])
        shortcut_keys_container.pack(fill="x", pady=self.pady, padx=10)

        for i in range(6):
            shortcut_keys_container.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(
            shortcut_keys_container,
            text="Defina os atalhos para controlar o aplicativo",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(row=0, column=0, columnspan=6, pady=self.pady, padx=30, sticky="nsew")

        ctk.CTkLabel(
            shortcut_keys_container,
            text="Posições",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(row=1, column=0, pady=self.pady, padx=15)

        self.position_key_entry = ctk.CTkEntry(
            shortcut_keys_container,
            height=30,
            width=40,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="F1",
            justify="center",
        )
        self.position_key_entry.grid(row=1, column=1, pady=self.pady, padx=15, sticky="nsew")

        ctk.CTkLabel(
            shortcut_keys_container,
            text="Clicker",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(row=1, column=2, pady=self.pady, padx=15, sticky="nsew")

        self.clicker_key_entry = ctk.CTkEntry(
            shortcut_keys_container,
            height=30,
            width=40,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="F2",
            justify="center",
        )
        self.clicker_key_entry.grid(row=1, column=3, pady=self.pady, padx=15, sticky="nsew")

        ctk.CTkLabel(
            shortcut_keys_container,
            text="Clicker Fixo",
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
        ).grid(row=1, column=4, pady=self.pady, padx=15, sticky="nsew")

        self.fixed_clicker_key_entry = ctk.CTkEntry(
            shortcut_keys_container,
            height=30,
            width=40,
            font=self.FONTS["text"],
            text_color=self.COLORS["text"],
            placeholder_text="F3",
            justify="center",
        )
        self.fixed_clicker_key_entry.grid(row=1, column=5, pady=self.pady, padx=15, sticky="nsew")

        self.apply_button = ctk.CTkButton(
            shortcut_keys_container,
            height=self.height,
            text="Aplicar Atalhos",
            font=self.FONTS["button"],
            text_color=self.COLORS["button_text"],
            fg_color=self.COLORS["button"],
            hover_color=self.COLORS["button_hover"],
        )
        self.apply_button.grid(row=2, column=0, columnspan=6, pady=self.pady)
