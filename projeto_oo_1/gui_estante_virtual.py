import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from banco_de_dados import setup_database, Estante, Livro, Revista, HQ, ItemDeLeitura 


# --- 1. CONFIGURAÇÕES VISUAIS PERSONALIZADAS (ESTILO TTK) ---
# Paleta de Cores Roxo/Lavanda
COR_ROXO_PRINCIPAL = '#6A0DAD'  
COR_LAVANDA = '#E6E6FA'        
COR_ROXO_CLARO = '#9370DB'    
COR_BRANCO = '#FFFFFF'

def configurar_estilo():
    """Configura o tema e estilos personalizados usando ttk."""
    style = ttk.Style()
    
    # Define o tema base
    style.theme_use('clam')
    
    # Estilo do Frame Principal
    style.configure('TFrame', background=COR_LAVANDA)
    
    # Estilo dos Botões Principais (ROXO)
    style.configure('Acao.TButton', 
                    font=('Arial', 10, 'bold'), 
                    foreground=COR_BRANCO,
                    background=COR_ROXO_PRINCIPAL, 
                    padding=10,
                    relief='flat')
    style.map('Acao.TButton', 
              background=[('active', COR_ROXO_CLARO)]) 

    # Estilo dos Botões de Informação/Secundários 
    style.configure('Info.TButton', 
                    font=('Arial', 10), 
                    foreground=COR_ROXO_PRINCIPAL,
                    background=COR_BRANCO, 
                    padding=8,
                    borderwidth=1,
                    relief='solid')
    style.map('Info.TButton', 
              background=[('active', COR_LAVANDA)])

    # Estilo do Label/Título
    style.configure('Titulo.TLabel', 
                    font=('Arial', 18, 'bold'), 
                    foreground=COR_ROXO_PRINCIPAL, 
                    background=COR_LAVANDA)
    
    # Estilo da Treeview (para listar itens)
    style.configure('Estante.Treeview.Heading', 
                    font=('Arial', 11, 'bold'), 
                    background=COR_ROXO_PRINCIPAL, 
                    foreground=COR_BRANCO)
    style.configure('Estante.Treeview', 
                    font=('Arial', 10),
                    background=COR_BRANCO,
                    fieldbackground=COR_BRANCO,
                    foreground='#333333',
                    rowheight=25)
    
    # Ajusta o foco da seleção (linha roxa)
    style.map('Estante.Treeview', 
              background=[('selected', COR_ROXO_CLARO)],
              foreground=[('selected', COR_BRANCO)])


# --- 2. CLASSE DA APLICAÇÃO TKINTER ---
class EstanteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da Janela
        self.title("Estante Virtual - Gerenciador GUI")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # Inicializa o estilo e o banco de dados
        configurar_estilo()
        setup_database()
        
        # Inicializa a lógica de dados
        self.estante = Estante()
        
        # Cria a interface do usuário
        self._criar_widgets()
        self._carregar_dados_na_treeview()

    def _criar_widgets(self):
        # Frame Principal (Content)
        main_frame = ttk.Frame(self, padding="15 15 15 15")
        main_frame.pack(fill='both', expand=True)

        # Título Personalizado com Icone
        ttk.Label(main_frame, text="📖 Minha Coleção de Leitura", style='Titulo.TLabel').pack(pady=(0, 20))

        columns = ('tipo', 'titulo', 'autor', 'id_curto')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', style='Estante.Treeview')
        
        # Configura as colunas
        self.tree.heading('tipo', text='Tipo', anchor=tk.W)
        self.tree.heading('titulo', text='Título', anchor=tk.W)
        self.tree.heading('autor', text='Autor/Escritor', anchor=tk.W)
        self.tree.heading('id_curto', text='ID (Curto)', anchor=tk.W)

        # Configura a largura das colunas
        self.tree.column('tipo', width=80, stretch=tk.NO)
        self.tree.column('titulo', width=300, anchor=tk.W)
        self.tree.column('autor', width=200, anchor=tk.W)
        self.tree.column('id_curto', width=100, stretch=tk.NO)
        
        self.tree.pack(fill='both', expand=True, pady=10)
        
        # Scrollbar para a Treeview
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)
        
        # --- Botões de Ação ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        # Botão Adicionar
        ttk.Button(button_frame, text="➕ Adicionar Novo Item", 
                   command=self._abrir_janela_adicionar, 
                   style='Acao.TButton').pack(side='left', padx=5)
        
        # Botão Remover
        ttk.Button(button_frame, text="🗑️ Remover Item", 
                   command=self._remover_item_selecionado, 
                   style='Acao.TButton').pack(side='left', padx=5)
                   
        # Botão Detalhes
        ttk.Button(button_frame, text="ℹ️ Ver Detalhes", 
                   command=self._exibir_detalhes, 
                   style='Info.TButton').pack(side='left', padx=5)
                   
        # Botão Atualizar
        ttk.Button(button_frame, text="🔄 Atualizar Lista", 
                   command=self._carregar_dados_na_treeview, 
                   style='Info.TButton').pack(side='right', padx=5)
                   

    def _carregar_dados_na_treeview(self):
        # ... [Método idêntico ao anterior] ...
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.estante._carregar_itens_db() 
        
        for item in self.estante.itens:
            self.tree.insert('', tk.END, iid=item.id,
                             values=(item.__class__.__name__, item.titulo, item.autor, item.id[:6]),
                             tags=(item.__class__.__name__.lower(),)) 
                             
    def _remover_item_selecionado(self):
        # ... [Método idêntico ao anterior] ...
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return

        item_id_completo = selected_item
        item_titulo = self.tree.item(selected_item, 'values')[1]
        resposta = messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover '{item_titulo}' (ID: {item_id_completo[:6]}...)?")

        if resposta:
            self.estante.remover_item(item_id_completo) 
            self._carregar_dados_na_treeview() 
            messagebox.showinfo("Sucesso", f"Item removido: {item_titulo}")
            
    def _exibir_detalhes(self):
        # ... [Método idêntico ao anterior] ...
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item para ver os detalhes.")
            return

        item_id = selected_item
        item_obj = next((item for item in self.estante.itens if item.id == item_id), None)

        if item_obj:
            detalhes_texto = item_obj.detalhes()
            messagebox.showinfo(f"Detalhes de {item_obj.__class__.__name__}", detalhes_texto)
        else:
            messagebox.showerror("Erro", "Item não encontrado na memória.")
            
    def _abrir_janela_adicionar(self):
        # ... [Método idêntico ao anterior] ...
        popup = tk.Toplevel(self)
        popup.title("➕ Adicionar Novo Item")
        popup.geometry("400x350")
        popup.resizable(False, False)
        
        self.tipo_item_var = tk.StringVar(value='Livro')
        
        form_frame = ttk.Frame(popup, padding="10")
        form_frame.pack(fill='both', expand=True)

        ttk.Label(form_frame, text="Tipo de Item:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        
        tipos = [('Livro', Livro), ('Revista', Revista), ('HQ', HQ)]
        
        for i, (nome, classe) in enumerate(tipos):
            ttk.Radiobutton(form_frame, 
                            text=nome, 
                            value=nome, 
                            variable=self.tipo_item_var, 
                            command=lambda: self._atualizar_campos_adicionar(form_frame, self.tipo_item_var.get())
                            ).grid(row=0, column=i + 1, sticky='w', padx=10, pady=5)
                            
        ttk.Label(form_frame, text="Título:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_titulo = ttk.Entry(form_frame, width=40)
        self.entry_titulo.grid(row=1, column=1, columnspan=3, sticky='ew', padx=5)

        ttk.Label(form_frame, text="Autor/Escritor:").grid(row=2, column=0, sticky='w', pady=5)
        self.entry_autor = ttk.Entry(form_frame, width=40)
        self.entry_autor.grid(row=2, column=1, columnspan=3, sticky='ew', padx=5)
        
        self.specific_fields_frame = ttk.Frame(form_frame)
        self.specific_fields_frame.grid(row=3, column=0, columnspan=4, sticky='ew', pady=10)
        
        self._atualizar_campos_adicionar(form_frame, 'Livro')

        ttk.Button(form_frame, 
                   text="SALVAR ITEM", 
                   command=lambda: self._salvar_novo_item(popup), 
                   style='Acao.TButton').grid(row=4, column=0, columnspan=4, pady=15)
                   
    def _atualizar_campos_adicionar(self, parent_frame, tipo):
        # ... [Método idêntico ao anterior] ...
        for widget in self.specific_fields_frame.winfo_children():
            widget.destroy()

        self.specific_entries = {}
        row = 0
        
        if tipo == 'Livro':
            ttk.Label(self.specific_fields_frame, text="Nº de Páginas:").grid(row=row, column=0, sticky='w', pady=5)
            entry = ttk.Entry(self.specific_fields_frame, width=15)
            entry.grid(row=row, column=1, sticky='w', padx=5)
            self.specific_entries['paginas'] = entry
            
        elif tipo == 'Revista':
            ttk.Label(self.specific_fields_frame, text="Edição:").grid(row=row, column=0, sticky='w', pady=5)
            entry_edicao = ttk.Entry(self.specific_fields_frame, width=15)
            entry_edicao.grid(row=row, column=1, sticky='w', padx=5)
            self.specific_entries['edicao'] = entry_edicao
            row += 1
            
            ttk.Label(self.specific_fields_frame, text="Mês de Publicação:").grid(row=row, column=0, sticky='w', pady=5)
            entry_mes = ttk.Entry(self.specific_fields_frame, width=15)
            entry_mes.grid(row=row, column=1, sticky='w', padx=5)
            self.specific_entries['mes_publicacao'] = entry_mes
            
        elif tipo == 'HQ':
            ttk.Label(self.specific_fields_frame, text="Desenhista/Ilustrador:").grid(row=row, column=0, sticky='w', pady=5)
            entry = ttk.Entry(self.specific_fields_frame, width=40)
            entry.grid(row=row, column=1, columnspan=3, sticky='ew', padx=5)
            self.specific_entries['desenhista'] = entry
            
    def _salvar_novo_item(self, popup):
        # ... [Método idêntico ao anterior] ...
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        tipo = self.tipo_item_var.get()
        
        if not titulo or not autor:
            messagebox.showerror("Erro de Validação", "Título e Autor são obrigatórios.")
            return

        novo_item: Optional[ItemDeLeitura] = None
        
        try:
            if tipo == 'Livro':
                paginas_str = self.specific_entries['paginas'].get().strip()
                paginas = int(paginas_str)
                if paginas <= 0:
                     raise ValueError("O número de páginas deve ser um valor inteiro positivo.")
                novo_item = Livro(titulo, autor, paginas)
            
            elif tipo == 'Revista':
                edicao = self.specific_entries['edicao'].get().strip()
                mes_publicacao = self.specific_entries['mes_publicacao'].get().strip()
                if not edicao or not mes_publicacao:
                    raise ValueError("Edição e Mês são obrigatórios para Revistas.")
                novo_item = Revista(titulo, autor, edicao, mes_publicacao)
                
            elif tipo == 'HQ':
                desenhista = self.specific_entries['desenhista'].get().strip()
                if not desenhista:
                    raise ValueError("Desenhista é obrigatório para HQs.")
                novo_item = HQ(titulo, autor, desenhista)

        except ValueError as e:
            messagebox.showerror("Erro de Dados", f"Erro na entrada de dados: {e}")
            return
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
            return
            
        if novo_item:
            self.estante.adicionar_item(novo_item)
            self._carregar_dados_na_treeview() 
            messagebox.showinfo("Sucesso", f"'{titulo}' ({tipo}) foi adicionado com sucesso!")
            popup.destroy() 


# --- 3. EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    app = EstanteApp()
    app.mainloop()
