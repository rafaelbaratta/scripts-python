import errno
import os
from pathlib import Path

from CTkMessagebox import CTkMessagebox
from customtkinter import filedialog


class Core:

    def __init__(self, gui):
        self.gui = gui

        self.gui.directory_button.configure(command=self.get_path)
        self.gui.rename_button.configure(command=self.rename_files)
        self.gui.clear_fields_button.configure(command=self.clear_fields)

        self.entries = [
            self.gui.insert_entry,
            self.gui.position_insert_entry,
            self.gui.remove_entry,
            self.gui.text_to_be_replaced_entry,
            self.gui.text_to_replace_entry,
            self.gui.prefix_entry,
            self.gui.suffix_entry,
        ]

    # ========== PATH/DIRECTORY FUNCTIONS ==========

    def get_path(self):
        directory_path = filedialog.askdirectory()
        self.gui.path_entry.delete(0, "end")
        self.gui.path_entry.insert(0, directory_path)

    def get_directory(self):
        data = self.gui.path_entry.get()

        if not data:
            CTkMessagebox(
                title="Info!",
                message="Não deixe o caminho em branco!",
                icon="info",
            )
            return None

        elif not os.path.isdir(data):
            CTkMessagebox(
                title="Info!",
                message="Caminho inserido não é um diretório!",
                icon="info",
            )
            return None

        return data

    # ========== BUTTONS FUNCTIONS ==========

    def clear_fields(self):
        self.gui.standard_name_entry.delete(0, "end")
        self.gui.standard_name_entry.configure(placeholder_text="Nome padrão para todos os arquivos")

        placeholders_texts = [
            "Texto a ser adicionado",
            "Posição",
            "Texto a ser removido",
            "Texto a ser substituído",
            "Texto substituto",
            "Prefixo a ser adicionado",
            "Sufixo a ser adicionado",
        ]

        for number, entry in enumerate(self.entries):
            entry.delete(0, "end")
            entry.configure(placeholder_text=placeholders_texts[number])

    def rename_files(self):
        directory = self.get_directory()

        if not directory:
            return

        os.chdir(directory)

        files = os.listdir(directory)

        if not files:
            CTkMessagebox(
                title="Info!",
                message="Não há nada no diretório fornecido!",
                icon="info",
            )
            return

        if self.gui.standard_name_checkbox.get():
            if not self.gui.standard_name_entry.get():
                CTkMessagebox(
                    title="Info!",
                    message="Preencha o nome que os arquivos devem possuir!",
                    icon="info",
                )
                return
            counter = self.rename_whole_filename(files)
        else:
            if self.empty_fields():
                CTkMessagebox(
                    title="Info!",
                    message="Todas as opções de modificação estão em branco!",
                    icon="info",
                )
                return
            counter = self.modify_current_filename(files)

        CTkMessagebox(
            title="Sucesso!",
            message=f"{counter} arquivos renomeados com sucesso!",
            icon="check",
        )
        return None

    def empty_fields(self):
        for entry in self.entries:
            if entry.get():
                return False
        return True

    # ========== RENAME/MODIFY FILENAME FUNCTIONS ==========

    def rename_whole_filename(self, files):
        counter = 0
        for file in files:
            file = Path(file)
            new_filename = self.gui.standard_name_entry.get()

            try:
                if counter == 0:
                    os.rename(file, new_filename + file.suffix)
                else:
                    os.rename(file, new_filename + f"{str(counter)}" + file.suffix)

            except FileExistsError:
                CTkMessagebox(
                    title="Info!",
                    message=f"Já existe um arquivo com o nome {new_filename}!",
                    icon="info",
                )
                break

            except PermissionError:
                CTkMessagebox(
                    title="Info!",
                    message=f"Você não tem permissão para mover renomear o arquivo {file}!",
                    icon="info",
                )
                break

            except OSError as e:
                if e.errno == errno.EINVAL:
                    CTkMessagebox(
                        title="Info!",
                        message=f'Nome do arquivo inválido!\nCertifique-se que o nome não contenha: \ / : * ? " < > |',
                        icon="info",
                    )
                    break

                else:
                    CTkMessagebox(
                        title="Info!",
                        message=f"Arquivo não renomeado por falha no sistema!",
                        icon="info",
                    )
                    break

            except Exception as e:
                CTkMessagebox(
                    title="Info!",
                    message=f"Falha ao renomear o arquivo {file}!",
                    icon="info",
                )
                break

            else:
                counter += 1

        return counter

    def modify_current_filename(self, files):
        counter = 0
        for file in files:
            file = Path(file)
            new_filename = self.add_modifications(file.stem)

            try:
                os.rename(file, new_filename + file.suffix)

            except FileExistsError:
                CTkMessagebox(
                    title="Info!",
                    message=f"Já existe um arquivo com o nome {new_filename}!",
                    icon="info",
                )
                break

            except PermissionError:
                CTkMessagebox(
                    title="Info!",
                    message=f"Você não tem permissão para mover renomear o arquivo {file}!",
                    icon="info",
                )
                break

            except OSError as e:
                if e.errno == errno.EINVAL:
                    CTkMessagebox(
                        title="Info!",
                        message=f'Nome do arquivo inválido!\nCertifique-se que o nome não contenha: \ / : * ? " < > |',
                        icon="info",
                    )
                    break

                else:
                    CTkMessagebox(
                        title="Info!",
                        message=f"Arquivo não renomeado por falha no sistema!",
                        icon="info",
                    )
                    break

            except Exception:
                CTkMessagebox(
                    title="Info!",
                    message=f"Falha ao renomear o arquivo {file}!",
                    icon="info",
                )
                break

            else:
                counter += 1

        return counter

    # ========== MODIFY FILENAMES FUNCTIONS ==========

    def add_modifications(self, filename):
        filename = self.remove_text(filename)
        filename = self.replace_text(filename)
        filename = self.insert_text(filename)
        filename = self.insert_prefix_and_suffix(filename)

        return filename

    def remove_text(self, filename):
        text_to_remove = self.entries[2].get()

        if text_to_remove:
            filename = filename.replace(text_to_remove, "")

        return filename

    def replace_text(self, filename):
        text_to_be_replaced = self.entries[3].get()
        text_to_replace = self.entries[4].get()

        if text_to_be_replaced and text_to_replace:
            filename = filename.replace(text_to_be_replaced, text_to_replace)

        return filename

    def insert_text(self, filename):
        text_to_insert = self.entries[0].get()
        position_to_insert = self.entries[1].get()

        try:
            if position_to_insert:
                position_to_insert = int(position_to_insert)

                if position_to_insert > len(filename):
                    position_to_insert = len(filename) - 1

                if text_to_insert:
                    filename = filename[:position_to_insert] + text_to_insert + filename[position_to_insert:]

                return filename

        except ValueError:
            CTkMessagebox(
                title="Info!",
                message="Insira um número inteiro para a posição do texto que será inserido!",
                icon="info",
            )
            return filename

    def insert_prefix_and_suffix(self, filename):
        prefix_to_insert = self.entries[5].get()
        suffix_to_insert = self.entries[6].get()

        if prefix_to_insert:
            filename = prefix_to_insert + filename

        if suffix_to_insert:
            filename = filename + suffix_to_insert

        return filename
