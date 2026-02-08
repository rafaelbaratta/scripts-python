import os

import qrcode
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkImage, filedialog
from PIL import Image


class Core:

    def __init__(self, gui):
        self.gui = gui
        self.img = None

        self.configure_buttons()

    # ========== STARTING APP FUNCTION ==========

    def configure_buttons(self):
        self.gui.file_button.configure(command=self.get_path)
        self.gui.generate_button.configure(command=self.generate_code)
        self.gui.clean_button.configure(command=self.clean_everything)
        self.gui.save_button.configure(command=self.save_code)

        self.gui.qr_code_size_slider.configure(command=self.print_qr_code_size)
        self.print_qr_code_size(self.gui.qr_code_size_slider.get())

    # ========== QR CODE SIZE FUNCTIONS ==========

    def print_qr_code_size(self, value):
        self.gui.qr_code_size_value.configure(text=f"Tamanho da Imagem: ({int(value)})")

    # ========== GENERATE CODE FUNCTIONS ==========

    def get_path(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos texto", "*.txt")])
        self.gui.text_entry.delete(0, "end")
        self.gui.text_entry.insert(0, file_path)

    def generate_code(self):
        data = self.get_data()

        if not data:
            return

        try:
            self.img = qrcode.make(data)
        except ValueError:
            option = CTkMessagebox(
                title="Info!",
                message="Conteúdo extenso para QR code, uma parte poderá ser cortada!",
                icon="info",
                option_1="Aceitar mesmo assim",
                option_2="Cancelar",
            )
            if option.get() == "Cancelar":
                return
            self.img = qrcode.make(data[:2100])

        self.img_size = int(self.gui.qr_code_size_slider.get())
        self.img = self.img.resize((self.img_size, self.img_size), Image.Resampling.NEAREST)

        converted_img = self.img.convert("RGB")

        ctk_img = CTkImage(
            light_image=converted_img,
            dark_image=converted_img,
            size=(self.img_size, self.img_size),
        )
        self.gui.code_label.configure(image=ctk_img, text="")

        self.gui.save_button.configure(
            state="normal",
            fg_color=self.gui.COLORS["button"],
            hover_color=self.gui.COLORS["button_hover"],
        )

    def get_file_content(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

        except UnicodeDecodeError:
            CTkMessagebox(
                title="Atenção!",
                message="Não foi possível ler o conteúdo do arquivo (erro de codificação)!",
                icon="warning",
            )
            return None

        except FileNotFoundError:
            CTkMessagebox(
                title="Info!",
                message="Arquivo não encontrado!",
                icon="info",
            )
            return None

        except Exception:
            CTkMessagebox(
                title="Atenção!",
                message="Erro ao ler o conteúdo do arquivo!",
                icon="warning",
            )
            return None

    def get_data(self):
        data = self.gui.text_entry.get()

        if not data:
            CTkMessagebox(
                title="Info!",
                message="Não deixe o campo em branco!",
                icon="info",
            )
            return None

        elif os.path.isfile(data):
            file_content = self.get_file_content(data)
            data = file_content

        return data

    # ========== SAVE CODE FUNCTION ==========

    def save_code(self):
        if not self.img:
            CTkMessagebox(
                title="Info!",
                message="Nenhum QR code para salvar!",
                icon="info",
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagens PNG", "*.png"), ("Todos os arquivos", "*.*")],
        )

        if file_path:
            self.img.save(file_path)

    # ========== CLEAN FIELDS FUNCTION ==========

    def clean_everything(self):
        self.gui.text_entry.delete(0, "end")
        self.gui.text_entry.configure(placeholder_text="Digite ou insira o conteúdo...")

        if self.img is not None:
            self.img = None
            self.gui.code_label.configure(image=self.img, text="Código a ser gerado...")

        self.gui.save_button.configure(state="disabled", fg_color=self.gui.COLORS["primary_bg"])
        self.gui.save_button.configure(state="disabled", fg_color=self.gui.COLORS["primary_bg"])
