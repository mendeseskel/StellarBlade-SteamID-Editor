import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import struct
import os
import shutil
import re
from datetime import datetime
import configparser
import io

class StellarBladeSteamIDEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Stellar Blade SteamID Editor")
        self.root.geometry("650x600")
        self.root.resizable(False, False)
        
        # Variáveis
        self.file_path = None
        self.original_data = None
        self.current_steamid = None
        self.old_steamid_folder = None
        self.config_path = None
        
        # Configurar cores
        self.bg_color = '#f5f5f5'
        self.entry_bg = 'white'
        self.button_bg = '#4a6fa5'
        self.button_fg = 'white'
        self.label_fg = '#333333'
        self.error_color = '#d32f2f'
        self.success_color = '#388e3c'
        self.info_bg = '#e8f4f8'
        self.info_fg = '#2c3e50'
        self.section_bg = '#e9ecef'
        
        self.root.configure(bg=self.bg_color)
        
        # Menu para instruções
        self.create_menu()
        
        # Criar interface principal
        self.create_widgets()
        
        # Tentar encontrar pasta padrão
        self.auto_find_save_folder()
    
    def create_menu(self):
        """Cria o menu superior"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Instructions", menu=help_menu)
        help_menu.add_command(label="Show Instructions", command=self.show_instructions)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
    
    def show_instructions(self):
        """Mostra janela com instruções completas"""
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instructions - Stellar Blade SteamID Editor")
        instructions_window.geometry("700x500")
        instructions_window.resizable(False, False)
        instructions_window.configure(bg=self.bg_color)
        
        # Frame principal com scrollbar
        main_frame = tk.Frame(instructions_window, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas com scrollbar
        canvas = tk.Canvas(main_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Conteúdo das instruções
        content_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Título
        title = tk.Label(content_frame, 
                        text="📖 Complete Instructions",
                        font=("Arial", 16, "bold"),
                        bg=self.bg_color,
                        fg='#2c3e50')
        title.pack(pady=(0, 20))
        
        # Seção 1: O que fazer
        section1 = tk.LabelFrame(content_frame,
                                text="  What You Need to Do  ",
                                font=("Arial", 11, "bold"),
                                bg=self.section_bg,
                                fg='#2c3e50',
                                relief=tk.GROOVE,
                                borderwidth=2)
        section1.pack(fill=tk.X, pady=(0, 15))
        
        steps = [
            "1. Find your NEW SteamID in the game files:",
            "   Location: Engine\\Binaries\\ThirdParty\\Steamworks\\Steamv159\\Win64\\steam_settings\\configs.user.ini",
            "   Look for: account_steamid=7656119xxxxxxxxxx",
            "",
            "2. Load that config file using the 'Load Config File' button",
            "   OR manually type the 17-digit SteamID",
            "",
            "3. Select your save game file (usually StellarBladeSave00.sav)",
            "",
            "4. Click 'Replace SteamID & Rename Folder'",
            "",
            "5. The tool will:",
            "   • Backup your original .sav file",
            "   • Replace SteamID in the save file",
            "   • Rename the save folder to match new SteamID"
        ]
        
        for step in steps:
            lbl = tk.Label(section1,
                          text=step,
                          font=("Arial", 9),
                          bg=self.section_bg,
                          fg='#2c3e50',
                          justify=tk.LEFT,
                          anchor='w')
            lbl.pack(fill=tk.X, padx=10, pady=2)
        
        # Seção 2: Caminhos importantes
        section2 = tk.LabelFrame(content_frame,
                                text="  Important Paths  ",
                                font=("Arial", 11, "bold"),
                                bg=self.section_bg,
                                fg='#2c3e50',
                                relief=tk.GROOVE,
                                borderwidth=2)
        section2.pack(fill=tk.X, pady=(0, 15))
        
        paths = [
            "Save Game Location:",
            "  %LOCALAPPDATA%\\SB\\Saved\\SaveGames\\7656119xxxxxxxxxx\\",
            "",
            "Config File Location:",
            "  Engine\\Binaries\\ThirdParty\\Steamworks\\Steamv159\\Win64\\steam_settings\\configs.user.ini",
            "",
            "Backup Files:",
            "  Same folder as original with .bak extension"
        ]
        
        for path in paths:
            lbl = tk.Label(section2,
                          text=path,
                          font=("Courier New", 8) if "\\" in path else ("Arial", 9),
                          bg=self.section_bg,
                          fg='#2c3e50',
                          justify=tk.LEFT,
                          anchor='w')
            lbl.pack(fill=tk.X, padx=10, pady=2)
        
        # Seção 3: Notas
        section3 = tk.LabelFrame(content_frame,
                                text="  Important Notes  ",
                                font=("Arial", 11, "bold"),
                                bg=self.section_bg,
                                fg='#d32f2f',
                                relief=tk.GROOVE,
                                borderwidth=2)
        section3.pack(fill=tk.X, pady=(0, 15))
        
        notes = [
            "⚠️ Always backup your saves before modifying",
            "⚠️ SteamID must be exactly 17 digits",
            "⚠️ The save folder name MUST match the SteamID",
            "⚠️ If folder rename fails, you must do it manually",
            "⚠️ Launch game with new SteamID after changes"
        ]
        
        for note in notes:
            lbl = tk.Label(section3,
                          text=note,
                          font=("Arial", 9, "bold" if "⚠️" in note else "normal"),
                          bg=self.section_bg,
                          fg='#d32f2f' if "⚠️" in note else '#2c3e50',
                          justify=tk.LEFT,
                          anchor='w')
            lbl.pack(fill=tk.X, padx=10, pady=2)
        
        # Botão para fechar
        close_btn = tk.Button(content_frame,
                             text="Close Instructions",
                             command=instructions_window.destroy,
                             bg=self.button_bg,
                             fg=self.button_fg,
                             font=("Arial", 10, "bold"),
                             relief=tk.RAISED,
                             borderwidth=2,
                             width=20)
        close_btn.pack(pady=20)
    
    def show_about(self):
        """Mostra informações sobre o programa"""
        messagebox.showinfo("About", 
                          "Stellar Blade SteamID Editor v1.0\n\n"
                          "This tool helps you transfer save games between\n"
                          "different Steam accounts by modifying the SteamID\n"
                          "in save files and renaming save folders.")
    
    def auto_find_save_folder(self):
        """Tenta encontrar a pasta de save automaticamente"""
        save_path = os.path.join(os.getenv('LOCALAPPDATA', ''), 'SB', 'Saved', 'SaveGames')
        if os.path.exists(save_path):
            for folder in os.listdir(save_path):
                if folder.isdigit() and len(folder) == 17:
                    self.old_steamid_folder = os.path.join(save_path, folder)
                    sav_file = self.find_sav_file_in_folder(self.old_steamid_folder)
                    if sav_file:
                        self.file_path = sav_file
                        self.file_entry.delete(0, tk.END)
                        self.file_entry.insert(0, self.file_path)
                        break
    
    def find_sav_file_in_folder(self, folder_path):
        """Encontra o primeiro arquivo .sav em uma pasta"""
        if not os.path.exists(folder_path):
            return None
        
        for file in os.listdir(folder_path):
            if file.lower().endswith('.sav'):
                return os.path.join(folder_path, file)
        return None
    
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=25, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="Stellar Blade SteamID Editor", 
                              font=("Arial", 18, "bold"),
                              bg=self.bg_color, 
                              fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Frame para carregar config
        config_frame = tk.LabelFrame(main_frame, 
                                    text="  STEP 1: Load Config File  ",
                                    font=("Arial", 10, "bold"),
                                    bg=self.bg_color,
                                    fg='#2c3e50',
                                    relief=tk.GROOVE,
                                    borderwidth=2)
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        config_inner = tk.Frame(config_frame, bg=self.bg_color)
        config_inner.pack(fill=tk.X, padx=10, pady=10)
        
        # Botão para carregar config
        load_config_btn = tk.Button(config_inner,
                                   text="Load Config File (configs.user.ini)",
                                   command=self.load_config_file,
                                   bg='#5d8aa8',
                                   fg='white',
                                   font=("Arial", 9, "bold"),
                                   relief=tk.RAISED,
                                   borderwidth=2,
                                   width=30)
        load_config_btn.pack(side=tk.LEFT)
        
        # Label para mostrar SteamID do config
        self.config_steamid_label = tk.Label(config_inner,
                                            text="No config loaded",
                                            font=("Arial", 9),
                                            bg=self.bg_color,
                                            fg='#7f8c8d')
        self.config_steamid_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Frame do arquivo de save
        file_frame = tk.LabelFrame(main_frame, 
                                  text="  STEP 2: Select Save File  ", 
                                  font=("Arial", 10, "bold"),
                                  bg=self.bg_color,
                                  fg='#2c3e50',
                                  relief=tk.GROOVE,
                                  borderwidth=2)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        file_inner = tk.Frame(file_frame, bg=self.bg_color)
        file_inner.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(file_inner, text="Save File:", 
                font=("Arial", 9),
                bg=self.bg_color,
                fg=self.label_fg).pack(side=tk.LEFT)
        
        self.file_entry = tk.Entry(file_inner,
                                  width=40,
                                  font=("Arial", 9),
                                  bg=self.entry_bg)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        browse_btn = tk.Button(file_inner,
                              text="Browse",
                              command=self.browse_file,
                              bg=self.button_bg,
                              fg=self.button_fg,
                              font=("Arial", 9, "bold"),
                              relief=tk.RAISED,
                              borderwidth=2)
        browse_btn.pack(side=tk.RIGHT)
        
        # Frame das informações atuais
        info_frame = tk.LabelFrame(main_frame,
                                  text="  Current Information  ",
                                  font=("Arial", 10, "bold"),
                                  bg=self.bg_color,
                                  fg='#2c3e50',
                                  relief=tk.GROOVE,
                                  borderwidth=2)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_inner = tk.Frame(info_frame, bg=self.bg_color)
        info_inner.pack(fill=tk.X, padx=10, pady=10)
        
        # Grid para informações
        tk.Label(info_inner, text="Current SteamID in file:", 
                font=("Arial", 9, "bold"),
                bg=self.bg_color,
                fg=self.label_fg).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.current_steamid_label = tk.Label(info_inner,
                                             text="[Not loaded]",
                                             font=("Arial", 9),
                                             bg=self.bg_color,
                                             fg=self.error_color)
        self.current_steamid_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        tk.Label(info_inner, text="Current Save Folder:", 
                font=("Arial", 9, "bold"),
                bg=self.bg_color,
                fg=self.label_fg).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.current_folder_label = tk.Label(info_inner,
                                            text="[Not loaded]",
                                            font=("Arial", 9),
                                            bg=self.bg_color,
                                            fg='#7f8c8d')
        self.current_folder_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Frame para novo SteamID
        new_frame = tk.LabelFrame(main_frame,
                                 text="  STEP 3: Enter/Verify New SteamID  ",
                                 font=("Arial", 10, "bold"),
                                 bg=self.bg_color,
                                 fg='#2c3e50',
                                 relief=tk.GROOVE,
                                 borderwidth=2)
        new_frame.pack(fill=tk.X, pady=(0, 15))
        
        new_inner = tk.Frame(new_frame, bg=self.bg_color)
        new_inner.pack(fill=tk.X, padx=10, pady=10)
        
        # Campo para novo SteamID
        entry_frame = tk.Frame(new_inner, bg=self.bg_color)
        entry_frame.pack(fill=tk.X)
        
        tk.Label(entry_frame, text="New SteamID (17 digits):", 
                font=("Arial", 9, "bold"),
                bg=self.bg_color,
                fg=self.label_fg).pack(side=tk.LEFT)
        
        self.new_steamid_var = tk.StringVar()
        self.new_steamid_var.trace('w', self.validate_steamid_length)
        
        self.new_steamid_entry = tk.Entry(entry_frame,
                                         width=22,
                                         font=("Arial", 9, "bold"),
                                         bg=self.entry_bg,
                                         textvariable=self.new_steamid_var)
        self.new_steamid_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        self.length_label = tk.Label(entry_frame,
                                    text="0/17",
                                    font=("Arial", 9),
                                    bg=self.bg_color,
                                    fg='#7f8c8d')
        self.length_label.pack(side=tk.LEFT)
        
        # Botão de ação principal
        action_frame = tk.Frame(main_frame, bg=self.bg_color)
        action_frame.pack(pady=20)
        
        self.replace_btn = tk.Button(action_frame,
                                    text="🚀 Replace SteamID & Rename Folder",
                                    command=self.replace_steamid_and_folder,
                                    state=tk.DISABLED,
                                    bg='#27ae60',
                                    fg='white',
                                    font=("Arial", 12, "bold"),
                                    relief=tk.RAISED,
                                    borderwidth=3,
                                    width=35,
                                    height=2)
        self.replace_btn.pack()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Load config file or select save file")
        
        status_frame = tk.Frame(main_frame, bg=self.bg_color, height=25)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(status_frame,
                                    textvariable=self.status_var,
                                    font=("Arial", 9),
                                    bg='#2c3e50',
                                    fg='white',
                                    relief=tk.SUNKEN,
                                    borderwidth=1,
                                    padx=10,
                                    pady=5)
        self.status_label.pack(fill=tk.X)
        
        # Nota rápida
        note_label = tk.Label(main_frame,
                             text="💡 Need help? Click 'Instructions' in the menu above",
                             font=("Arial", 8, "italic"),
                             bg=self.bg_color,
                             fg='#7f8c8d')
        note_label.pack(pady=(10, 0))
    
    def load_config_file(self):
        """Carrega arquivo configs.user.ini e extrai SteamID"""
        initial_dir = os.path.expanduser("~")
        
        file_path = filedialog.askopenfilename(
            title="Select configs.user.ini file",
            filetypes=[("Config files", "*.ini"), ("All files", "*.*")],
            initialdir=initial_dir
        )
        
        if not file_path:
            return
        
        self.config_path = file_path
        
        try:
            # Ler arquivo como texto
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Procurar account_steamid usando regex
            steamid_match = re.search(r'account_steamid\s*=\s*(\d+)', content)
            
            if steamid_match:
                steamid_str = steamid_match.group(1)
                
                if len(steamid_str) == 17 and steamid_str.startswith('7656'):
                    # Preencher automaticamente no campo
                    self.new_steamid_var.set(steamid_str)
                    
                    # Atualizar label
                    self.config_steamid_label.config(
                        text=f"Loaded: {steamid_str}",
                        fg=self.success_color
                    )
                    
                    self.status_var.set(f"Config loaded: SteamID {steamid_str}")
                    
                    # Se já temos arquivo .sav carregado, validar
                    if self.file_path:
                        self.validate_steamid_length()
                    
                    messagebox.showinfo("Success", 
                                      f"SteamID loaded from config:\n{steamid_str}")
                else:
                    messagebox.showerror("Error", 
                                       f"Invalid SteamID in config:\n"
                                       f"Must be 17 digits starting with 7656\n"
                                       f"Found: {steamid_str}")
            else:
                messagebox.showerror("Error", 
                                   "account_steamid not found in config file!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config file: {str(e)}")
    
    def validate_steamid_length(self, *args):
        """Valida se o SteamID tem exatamente 17 dígitos"""
        steamid = self.new_steamid_var.get().strip()
        digits = ''.join(filter(str.isdigit, steamid))
        
        # Atualizar contador
        length = len(digits)
        self.length_label.config(text=f"{length}/17")
        
        # Validar e atualizar cores
        if length == 17:
            self.length_label.config(fg=self.success_color)
            valid = True
        elif length > 17:
            self.length_label.config(fg=self.error_color)
            valid = False
        else:
            self.length_label.config(fg='#f39c12')
            valid = False
        
        # Ativar/desativar botão
        if valid and self.file_path and self.current_steamid:
            self.replace_btn.config(state=tk.NORMAL, bg='#27ae60')
        else:
            self.replace_btn.config(state=tk.DISABLED, bg='#95a5a6')
        
        return valid
    
    def browse_file(self):
        """Abre diálogo para selecionar arquivo .sav"""
        initial_dir = os.path.join(os.getenv('LOCALAPPDATA', ''), 'SB', 'Saved', 'SaveGames')
        if not os.path.exists(initial_dir):
            initial_dir = os.path.expanduser("~")
        
        file_path = filedialog.askopenfilename(
            title="Select Stellar Blade Save File",
            filetypes=[("Save files", "*.sav"), ("All files", "*.*")],
            initialdir=initial_dir
        )
        
        if file_path:
            self.file_path = file_path
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.load_file()
    
    def load_file(self):
        """Carrega e analisa o arquivo .sav"""
        if not self.file_path:
            self.file_path = self.file_entry.get().strip()
        
        if not self.file_path or not os.path.exists(self.file_path):
            messagebox.showerror("Error", "File not found!")
            return
        
        try:
            # Ler arquivo
            with open(self.file_path, 'rb') as f:
                self.original_data = bytearray(f.read())
            
            # Tentar encontrar SteamID
            self.find_steamid_auto()
            
            # Encontrar pasta do save atual
            self.find_current_save_folder()
            
            # Atualizar interface
            if self.current_steamid:
                self.current_steamid_label.config(
                    text=str(self.current_steamid),
                    fg=self.success_color
                )
            else:
                self.current_steamid_label.config(
                    text="[Not found in file]",
                    fg=self.error_color
                )
            
            # Atualizar status
            self.status_var.set(f"Save file loaded: {os.path.basename(self.file_path)}")
            
            # Validar SteamID entry
            self.validate_steamid_length()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def find_steamid_auto(self):
        """Tenta encontrar SteamID automaticamente"""
        if not self.original_data:
            return
        
        data = self.original_data
        
        # Padrão para SteamID (17 dígitos começando com 7656)
        steamid_pattern = rb'7656\d{13}'
        
        try:
            data_str = data.decode('ascii', errors='ignore')
            match = re.search(steamid_pattern.decode(), data_str)
            
            if match:
                steamid_str = match.group(0)
                if len(steamid_str) == 17:
                    self.current_steamid = int(steamid_str)
                    return
        except:
            pass
        
        self.current_steamid = None
    
    def find_current_save_folder(self):
        """Encontra a pasta do save atual"""
        if not self.file_path:
            return
        
        parent_dir = os.path.dirname(self.file_path)
        folder_name = os.path.basename(parent_dir)
        
        if folder_name.isdigit() and len(folder_name) == 17:
            self.old_steamid_folder = parent_dir
            self.current_folder_label.config(
                text=folder_name,
                fg=self.success_color
            )
        else:
            self.old_steamid_folder = None
            self.current_folder_label.config(
                text="[Not a SteamID folder]",
                fg=self.error_color
            )
    
    def create_backup(self, file_path):
        """Cria backup do arquivo atual"""
        backup_path = f"{file_path}.bak"
        
        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
            return None
    
    def replace_steamid_in_file(self, file_path, old_steamid, new_steamid):
        """Substitui SteamID em um arquivo"""
        try:
            with open(file_path, 'rb') as f:
                data = bytearray(f.read())
            
            old_str = str(old_steamid)
            new_str = str(new_steamid)
            old_bytes = old_str.encode('ascii')
            new_bytes = new_str.encode('ascii')
            
            replaced = False
            replacement_count = 0
            
            pos = data.find(old_bytes)
            while pos != -1:
                data[pos:pos + len(old_bytes)] = new_bytes
                replaced = True
                replacement_count += 1
                pos = data.find(old_bytes, pos + 1)
            
            if replaced:
                with open(file_path, 'wb') as f:
                    f.write(data)
                return replacement_count
            
            return 0
            
        except Exception as e:
            raise Exception(f"Failed to replace SteamID in file: {str(e)}")
    
    def rename_save_folder(self, old_steamid, new_steamid):
        """Renomeia a pasta do save game"""
        if not self.old_steamid_folder:
            return False, "No save folder found to rename"
        
        parent_dir = os.path.dirname(self.old_steamid_folder)
        new_folder_path = os.path.join(parent_dir, str(new_steamid))
        
        if os.path.exists(new_folder_path):
            return False, f"Folder already exists: {new_steamid}"
        
        try:
            os.rename(self.old_steamid_folder, new_folder_path)
            
            # Atualizar caminho do arquivo
            old_filename = os.path.basename(self.file_path)
            self.file_path = os.path.join(new_folder_path, old_filename)
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, self.file_path)
            
            self.old_steamid_folder = new_folder_path
            
            return True, f"Folder renamed to: {new_steamid}"
            
        except Exception as e:
            return False, f"Failed to rename folder: {str(e)}"
    
    def replace_steamid_and_folder(self):
        """Substitui o SteamID no arquivo E renomeia a pasta"""
        if not self.file_path or not self.original_data:
            messagebox.showwarning("Warning", "No save file loaded!")
            return
        
        # Obter novo SteamID
        new_steamid_str = self.new_steamid_var.get().strip()
        digits = ''.join(filter(str.isdigit, new_steamid_str))
        
        # Validar comprimento
        if len(digits) != 17:
            messagebox.showerror("Error", 
                               f"SteamID must be exactly 17 digits!\n"
                               f"Current: {len(digits)} digits")
            return
        
        try:
            new_steamid = int(digits)
        except ValueError:
            messagebox.showerror("Error", "Invalid SteamID! Must be a 17-digit number.")
            return
        
        if not self.current_steamid:
            messagebox.showerror("Error", "Current SteamID not found in file!")
            return
        
        # Confirmar
        confirm_msg = (
            f"Confirm replacement:\n\n"
            f"Current SteamID: {self.current_steamid}\n"
            f"New SteamID: {new_steamid}\n\n"
            f"This will:\n"
            f"1. Replace SteamID in save file\n"
            f"2. Rename save folder\n"
            f"3. Create backup of original file"
        )
        
        if not messagebox.askyesno("Confirm Replacement", confirm_msg):
            return
        
        # Criar backup
        backup_path = self.create_backup(self.file_path)
        if not backup_path:
            return
        
        try:
            # Substituir no arquivo
            replacements = self.replace_steamid_in_file(self.file_path, self.current_steamid, new_steamid)
            
            if replacements == 0:
                messagebox.showerror("Error", "Failed to find SteamID in file for replacement!")
                return
            
            # Renomear pasta
            folder_result = ""
            if self.old_steamid_folder:
                success, folder_result = self.rename_save_folder(self.current_steamid, new_steamid)
                if not success:
                    messagebox.showwarning("Warning", 
                                         f"File SteamID replaced but folder rename failed:\n{folder_result}")
            
            # Atualizar interface
            self.current_steamid = new_steamid
            self.current_steamid_label.config(text=str(new_steamid), fg=self.success_color)
            
            if self.old_steamid_folder:
                self.current_folder_label.config(text=str(new_steamid), fg=self.success_color)
            
            # Limpar campo
            self.new_steamid_var.set("")
            
            # Mostrar sucesso
            success_msg = (
                f"✅ SUCCESS!\n\n"
                f"SteamID replaced in file: {replacements} occurrence(s)\n"
                f"Backup: {os.path.basename(backup_path)}\n\n"
            )
            
            if folder_result:
                success_msg += f"Folder: {folder_result}\n\n"
            
            success_msg += (
                f"Next steps:\n"
                f"1. Launch the game with your new SteamID\n"
                f"2. The save should now load correctly"
            )
            
            messagebox.showinfo("Success", success_msg)
            
            self.status_var.set(f"Success! New SteamID: {new_steamid}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to complete replacement: {str(e)}")
            self.status_var.set("Error during replacement")

def main():
    root = tk.Tk()
    app = StellarBladeSteamIDEditor(root)
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()