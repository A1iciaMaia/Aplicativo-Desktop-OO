import uuid
import sqlite3
from typing import List, Union, Dict, Any, Optional

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
DB_NAME = 'estante_virtual.db'

def setup_database():
    """Cria a tabela 'itens' no SQLite se ela não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # A coluna 'tipo' é crucial para sabermos qual classe instanciar ao carregar os dados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id TEXT PRIMARY KEY,
            tipo TEXT NOT NULL,
            titulo TEXT NOT NULL,
            autor TEXT,
            paginas INTEGER,
            edicao TEXT,
            mes_publicacao TEXT,
            desenhista TEXT
        )
    """)
    conn.commit()
    conn.close()
    print(f"💾 Conexão com o banco de dados '{DB_NAME}' estabelecida.")

# 1. CLASSE MÃE/BASE
class ItemDeLeitura:
    """Classe base para todos os itens de leitura (Livro, Revista, HQ)."""
    
    def __init__(self, titulo: str, autor: str, item_id: Optional[str] = None):
        # Se um ID for fornecido (carregamento do DB), usa-o. Senão, gera um novo.
        self.id = item_id if item_id else uuid.uuid4().hex
        self.titulo = titulo
        self.autor = autor
    
    def __str__(self) -> str:
        return f"ID: {self.id[:6]}... - Título: {self.titulo} - Autor: {self.autor}"

    def detalhes(self) -> str:
        return f"Tipo: {self.__class__.__name__}\n{self}"

    def to_dict(self) -> Dict[str, Any]:
        """Converte o objeto para um dicionário para salvar no DB."""
        return {
            'id': self.id,
            'tipo': self.__class__.__name__,
            'titulo': self.titulo,
            'autor': self.autor,
            # Placeholder para atributos específicos
            'paginas': None,
            'edicao': None,
            'mes_publicacao': None,
            'desenhista': None,
        }

# 2. CLASSES FILHAS (HERANÇA)
class Livro(ItemDeLeitura):
    """Classe para Livros, com atributo particular 'paginas'."""
    
    def __init__(self, titulo: str, autor: str, paginas: int, item_id: Optional[str] = None):
        super().__init__(titulo, autor, item_id)
        self.paginas = paginas
        
    def detalhes(self) -> str:
        detalhes_base = super().detalhes()
        return f"{detalhes_base}\nPáginas: {self.paginas}"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['paginas'] = self.paginas
        return data
        
class Revista(ItemDeLeitura):
    """Classe para Revistas, com atributos particulares 'edicao' e 'mes_publicacao'."""
    
    def __init__(self, titulo: str, autor: str, edicao: str, mes_publicacao: str, item_id: Optional[str] = None):
        super().__init__(titulo, autor, item_id)
        self.edicao = edicao
        self.mes_publicacao = mes_publicacao
        
    def detalhes(self) -> str:
        detalhes_base = super().detalhes()
        return f"{detalhes_base}\nEdição: {self.edicao} - Mês: {self.mes_publicacao}"
        
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['edicao'] = self.edicao
        data['mes_publicacao'] = self.mes_publicacao
        return data

class HQ(ItemDeLeitura):
    """Classe para Histórias em Quadrinhos, com atributo particular 'desenhista'."""
    
    def __init__(self, titulo: str, autor: str, desenhista: str, item_id: Optional[str] = None):
        super().__init__(titulo, autor, item_id)
        self.desenhista = desenhista
        
    def detalhes(self) -> str:
        detalhes_base = super().detalhes()
        return f"{detalhes_base}\nDesenhista: {self.desenhista}"
        
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['desenhista'] = self.desenhista
        return data

# 3. CLASSE DE GERENCIAMENTO (ESTANTE) COM PERSISTÊNCIA DE DADOS
class Estante:
    """Gerencia a coleção de itens de leitura, com persistência em SQLite."""
    
    def __init__(self):
        self.itens: List[ItemDeLeitura] = []
        self._carregar_itens_db()
        
    def _get_db_connection(self):
        """Método utilitário para conectar ao DB."""
        return sqlite3.connect(DB_NAME)

    def _carregar_itens_db(self) -> None:
        """Carrega todos os itens do banco de dados para a memória."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM itens")
        registros = cursor.fetchall()
        conn.close()

        self.itens = []
        
        for registro in registros:
            item_data = {
                'id': registro[0],
                'tipo': registro[1],
                'titulo': registro[2],
                'autor': registro[3],
                'paginas': registro[4],
                'edicao': registro[5],
                'mes_publicacao': registro[6],
                'desenhista': registro[7]
            }
            
            # Recria a instância da classe correta (Polimorfismo e Herança)
            try:
                if item_data['tipo'] == 'Livro':
                    item = Livro(item_data['titulo'], item_data['autor'], item_data['paginas'], item_data['id'])
                elif item_data['tipo'] == 'Revista':
                    item = Revista(item_data['titulo'], item_data['autor'], item_data['edicao'], item_data['mes_publicacao'], item_data['id'])
                elif item_data['tipo'] == 'HQ':
                    item = HQ(item_data['titulo'], item_data['autor'], item_data['desenhista'], item_data['id'])
                else:
                    continue # Ignora tipo desconhecido
                    
                self.itens.append(item)
            except Exception as e:
                print(f"Erro ao carregar item ID {item_data['id']}: {e}")

        print(f"\n📦 {len(self.itens)} itens carregados do banco de dados.")

    def adicionar_item(self, item: ItemDeLeitura) -> None:
        """Adiciona item à memória e ao DB."""
        data = item.to_dict()
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO itens VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['id'], data['tipo'], data['titulo'], data['autor'], 
                data['paginas'], data['edicao'], data['mes_publicacao'], data['desenhista']
            ))
            conn.commit()
            self.itens.append(item)
            print(f"\n✅ '{item.titulo}' adicionado(a) e SALVO no banco de dados!")
        except sqlite3.Error as e:
            print(f"\n❌ ERRO ao salvar no banco de dados: {e}")
        finally:
            conn.close()

    def remover_item(self, item_id: str) -> None:
        """Remove item da memória e do DB pelo ID."""
        
        # 1. Tenta remover do banco de dados
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM itens WHERE id LIKE ?", (item_id + '%',))
            removidos_db = cursor.rowcount
            conn.commit()
            
            if removidos_db > 0:
                # 2. Se removeu do DB, remove da memória (operação mais eficiente)
                self.itens = [item for item in self.itens if not item.id.startswith(item_id)]
                print(f"\n🗑️ Item com ID '{item_id}' removido com sucesso!")
            else:
                print(f"\n⚠️ Nenhum item encontrado com o ID '{item_id}'.")
                
        except sqlite3.Error as e:
            print(f"\n❌ ERRO ao remover do banco de dados: {e}")
        finally:
            conn.close()

    def listar_todos(self) -> None:
        """Lista todos os itens presentes na estante (da memória)."""
        if not self.itens:
            print("\n⚠️ A estante está vazia.")
            return
            
        print("\n📚 ITENS NA ESTANTE 📚")
        print("-" * 30)
        for item in self.itens:
            print(f"- [{item.__class__.__name__}] {item}")
        print("-" * 30)

    def buscar_por_titulo(self, termo: str) -> None:
        """Busca itens por um termo no título (case-insensitive)."""
        termo = termo.lower()
        resultados = [item for item in self.itens if termo in item.titulo.lower()]
        
        if not resultados:
            print(f"\n⚠️ Nenhum item encontrado com o termo '{termo}'.")
            return

        print(f"\n🔍 RESULTADOS DA BUSCA POR '{termo.upper()}' 🔍")
        print("-" * 30)
        for item in resultados:
            print(item.detalhes())
            print("-" * 30)
    
    def exibir_detalhes_por_tipo(self, tipo_classe: type) -> None:
        """Lista e exibe detalhes de itens de um tipo específico."""
        
        itens_do_tipo = [item for item in self.itens if isinstance(item, tipo_classe)]
        
        if not itens_do_tipo:
            print(f"\n⚠️ Nenhum(a) {tipo_classe.__name__} encontrado(a) na estante.")
            return
            
        print(f"\n📋 DETALHES DE {tipo_classe.__name__.upper()}S 📋")
        print("=" * 30)
        for item in itens_do_tipo:
            print(item.detalhes())
            print("=" * 30)

# 4. FUNÇÕES DO MENU (Interface com o usuário)
def exibir_menu(estante: Estante) -> None:
    """Exibe o menu principal e gerencia as interações do usuário."""
    
    while True:
        print("\n╔═══════════════════════════════════╗")
        print("║      ESTANTE VIRTUAL (SQLite)     ║")
        print("╠═══════════════════════════════════╣")
        print("║ 1. Adicionar Novo Item            ║")
        print("║ 2. Remover Item pelo ID           ║") # Nova funcionalidade
        print("║ 3. Listar Todos os Itens          ║")
        print("║ 4. Buscar por Título              ║")
        print("║ 5. Detalhes de Livros             ║")
        print("║ 6. Detalhes de Revistas           ║")
        print("║ 7. Detalhes de HQs                ║")
        print("║ 0. Sair e Fechar DB               ║")
        print("╚═══════════════════════════════════╝")
        
        escolha = input("➡️ Digite sua opção: ")
        
        if escolha == '1':
            menu_adicionar(estante)
        elif escolha == '2':
            item_id = input("Digite o ID COMPLETO ou PARCIAL (ex: f1a2b3) do item a remover: ")
            estante.remover_item(item_id)
        elif escolha == '3':
            estante.listar_todos()
        elif escolha == '4':
            termo = input("Digite o título ou parte dele para buscar: ")
            estante.buscar_por_titulo(termo)
        elif escolha == '5':
            estante.exibir_detalhes_por_tipo(Livro)
        elif escolha == '6':
            estante.exibir_detalhes_por_tipo(Revista)
        elif escolha == '7':
            estante.exibir_detalhes_por_tipo(HQ)
        elif escolha == '0':
            print("\n👋 Saindo do sistema. Todos os dados estão salvos em estante_virtual.db!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")

def menu_adicionar(estante: Estante) -> None:
    """Submenu para adicionar diferentes tipos de itens."""
    print("\n  ** ADICIONAR ITEM **")
    print("  a. Livro")
    print("  b. Revista")
    print("  c. HQ")
    
    tipo = input("  ➡️ Escolha o tipo de item (a/b/c): ").lower()
    
    if tipo not in ['a', 'b', 'c']:
        print("\n❌ Opção inválida para o tipo de item.")
        return
        
    titulo = input("Título: ")
    autor = input("Autor/Escritor: ")
    
    if tipo == 'a':
        try:
            paginas = int(input("Número de Páginas: "))
            novo_item = Livro(titulo, autor, paginas)
            estante.adicionar_item(novo_item)
        except ValueError:
            print("\n❌ O número de páginas deve ser um valor inteiro.")
            
    elif tipo == 'b':
        edicao = input("Edição: ")
        mes = input("Mês de Publicação: ")
        novo_item = Revista(titulo, autor, edicao, mes)
        estante.adicionar_item(novo_item)
        
    elif tipo == 'c':
        desenhista = input("Desenhista/Ilustrador: ")
        novo_item = HQ(titulo, autor, desenhista)
        estante.adicionar_item(novo_item)
        

# 5. EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    # Garante que o banco de dados e a tabela existam
    setup_database()
    
    # Cria e carrega os itens da estante do DB
    minha_estante = Estante()
    
    # Inicia o menu
    exibir_menu(minha_estante)