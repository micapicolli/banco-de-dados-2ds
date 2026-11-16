import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class SistemaCadastroClientes:

    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Clientes")
        self.root.geometry("460x260")
        self.root.resizable(False, False)

        # Inicializa o banco de dados
        self.conectar_banco()

        # Constrói a interface gráfica principal
        self.criar_interface()

    def conectar_banco(self):
        """Conecta ao banco SQLite e cria a tabela de clientes se não existir."""
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def criar_interface(self):
        """Cria os rótulos, campos de entrada e botões do formulário."""
        frame_principal = tk.Frame(self.root, padx=20, pady=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Campo Nome
        tk.Label(frame_principal, text="Nome Completo:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=8
        )
        self.entry_nome = tk.Entry(frame_principal, width=35, font=("Arial", 10))
        self.entry_nome.grid(row=0, column=1, pady=8, padx=(10, 0))

        # Campo E-mail
        tk.Label(frame_principal, text="E-mail:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=8
        )
        self.entry_email = tk.Entry(
            frame_principal, width=35, font=("Arial", 10)
        )
        self.entry_email.grid(row=1, column=1, pady=8, padx=(10, 0))

        # Campo Telefone
        tk.Label(frame_principal, text="Telefone:", font=("Arial", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=8
        )
        self.entry_telefone = tk.Entry(
            frame_principal, width=35, font=("Arial", 10)
        )
        self.entry_telefone.grid(row=2, column=1, pady=8, padx=(10, 0))

        # Frame para os Botões
        frame_botoes = tk.Frame(frame_principal)
        frame_botoes.grid(row=3, column=0, columnspan=2, pady=20)

        btn_salvar = tk.Button(
            frame_botoes,
            text="Salvar Cliente",
            command=self.salvar_cliente,
            bg="#2E7D32",
            fg="white",
            font=("Arial", 9, "bold"),
            width=14,
            cursor="hand2",
        )
        btn_salvar.pack(side=tk.LEFT, padx=5)

        btn_limpar = tk.Button(
            frame_botoes,
            text="Limpar",
            command=self.limpar_formulario,
            bg="#C62828",
            fg="white",
            font=("Arial", 9, "bold"),
            width=12,
            cursor="hand2",
        )
        btn_limpar.pack(side=tk.LEFT, padx=5)

        # Novo botão: Visualizar Clientes
        btn_visualizar = tk.Button(
            frame_botoes,
            text="Visualizar Clientes",
            command=self.visualizar_clientes,
            bg="#1565C0",
            fg="white",
            font=("Arial", 9, "bold"),
            width=16,
            cursor="hand2",
        )
        btn_visualizar.pack(side=tk.LEFT, padx=5)

    def salvar_cliente(self):
        """Valida os campos e insere os dados no banco SQLite."""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        if not nome or not email or not telefone:
            messagebox.showwarning(
                "Campos Obrigatórios",
                "Por favor, preencha todos os campos (Nome, E-mail e Telefone) antes de salvar.",
            )
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning(
                "E-mail Inválido",
                "Por favor, insira um endereço de e-mail válido.",
            )
            return

        try:
            self.cursor.execute(
                """
                INSERT INTO clientes (nome, email, telefone)
                VALUES (?, ?, ?)
            """,
                (nome, email, telefone),
            )
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.limpar_formulario()

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro no Banco de Dados",
                f"Não foi possível salvar os dados:\n{erro}",
            )

    def limpar_formulario(self):
        """Apaga o conteúdo de todos os campos e devolve o foco ao campo Nome."""
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_nome.focus()

    def visualizar_clientes(self):
        """Abre uma nova janela exibindo todos os clientes cadastrados em uma tabela."""
        try:
            self.cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            registros = self.cursor.fetchall()
        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro no Banco de Dados",
                f"Não foi possível consultar os clientes:\n{erro}",
            )
            return

        # Cria a janela secundária (Toplevel)
        janela_lista = tk.Toplevel(self.root)
        janela_lista.title("Clientes Cadastrados")
        janela_lista.geometry("620x350")
        janela_lista.grab_set()  # Mantém o foco na janela aberta

        frame_tabela = tk.Frame(janela_lista, padx=15, pady=15)
        frame_tabela.pack(fill=tk.BOTH, expand=True)

        # Configuração da tabela (Treeview)
        colunas = ("id", "nome", "email", "telefone")
        tabela = ttk.Treeview(
            frame_tabela, columns=colunas, show="headings", height=12
        )

        # Cabeçalhos das colunas
        tabela.heading("id", text="ID")
        tabela.heading("nome", text="Nome Completo")
        tabela.heading("email", text="E-mail")
        tabela.heading("telefone", text="Telefone")

        # Largura e alinhamento das colunas
        tabela.column("id", width=45, anchor=tk.CENTER)
        tabela.column("nome", width=210, anchor=tk.W)
        tabela.column("email", width=200, anchor=tk.W)
        tabela.column("telefone", width=115, anchor=tk.CENTER)

        # Barra de rolagem vertical
        scrollbar = ttk.Scrollbar(
            frame_tabela, orient=tk.VERTICAL, command=tabela.yview
        )
        tabela.configure(yscrollcommand=scrollbar.set)

        tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Preenche a tabela com os registros do SQLite
        if registros:
            for cliente in registros:
                tabela.insert("", tk.END, values=cliente)
        else:
            messagebox.showinfo(
                "Lista Vazia",
                "Ainda não há clientes cadastrados no banco de dados.",
                parent=janela_lista,
            )

        # Botão para fechar a janela de visualização
        btn_fechar = tk.Button(
            janela_lista,
            text="Fechar",
            command=janela_lista.destroy,
            bg="#455A64",
            fg="white",
            font=("Arial", 9, "bold"),
            width=12,
            cursor="hand2",
        )
        btn_fechar.pack(pady=(0, 15))

    def __del__(self):
        """Fecha a conexão com o banco de dados ao encerrar o programa."""
        if hasattr(self, "conn"):
            self.conn.close()


if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaCadastroClientes(janela)
    janela.mainloop()
