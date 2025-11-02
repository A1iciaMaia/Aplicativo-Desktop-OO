import uuid
from typing import List

# 1. CLASSE MÃE/BASE
class ItemDeLeitura:
    """Classe base para todos os itens de leitura (Livro, Revista, HQ)."""
    
    # Anotações de tipo no construtor
    def __init__(self, titulo: str, autor: str):
        self.id = uuid.uuid4()  # Gera um ID único para cada item
        self.titulo = titulo
        self.autor = autor
    
    # Anotação de tipo no retorno
    def __str__(self) -> str:
        """Representação em string para exibição básica."""
        return f"ID: {self.id.hex[:6]} - Título: {self.titulo} - Autor: {self.autor}"

    # Anotação de tipo no retorno
    def detalhes(self) -> str:
        """Método para exibir detalhes, será sobrescrito nas classes filhas."""
        return f"Tipo: {self.__class__.__name__}\n{self}"

# 2. CLASSES FILHAS (HERANÇA)
class Livro(ItemDeLeitura):
    """Classe para Livros, com atributo particular 'paginas'."""
    
    # Anotações de tipo no construtor (incluindo o novo parâmetro)
    def __init__(self, titulo: str, autor: str, paginas: int):
        super().__init__(titulo, autor)
        self.paginas = paginas
        
    # Anotação de tipo no retorno
    def detalhes(self) -> str:
        """Sobrescreve o método detalhes() para incluir o número de páginas."""
        detalhes_base = super().detalhes()
        return f"{detalhes_base}\nPáginas: {self.paginas}"
        
class Revista(ItemDeLeitura):
    """Classe para Revistas, com atributos particulares 'edicao' e 'mes_publicacao'."""
    
    # Anotações de tipo no construtor
    def __init__(self, titulo: str, autor: str, edicao: str, mes_publicacao: str):
        super().__init__(titulo, autor)
        self.edicao = edicao
        self.mes_publicacao = mes_publicacao
        
    # Anotação de tipo no retorno
    def detalhes(self) -> str:
        """Sobrescreve o método detalhes() para incluir edição e mês."""
        detalhes_base = super().detalhes()
        return f"{detalhes_base}\nEdição: {self.edicao} - Mês: {self.mes_publicacao}"

class HQ(ItemDeLeitura):
    """Classe para Histórias em Quadrinhos, com atributo particular 'desenhista'."""
    
    # Anotações de tipo no construtor
    def __init__(self, titulo: str, autor: str, desenhista: str):
        super().__init__(titulo, autor)
        self.desenhista = desenhista
        
    # Anotação de tipo no retorno
    def detalhes(self) -> str:
        """Sobrescreve o método detalhes() para incluir o desenhista."""
        detalhes_base = super().detalhes()
        return f"{detalhes_base}\nDesenhista: {self.desenhista}"

# 3. CLASSE DE GERENCIAMENTO (ESTANTE)
class Estante:
    """Gerencia a coleção de itens de leitura."""
    
    def __init__(self):
        # Anotação de tipo para a lista de itens
        self.itens: List[ItemDeLeitura] = []
        
    # Anotação de tipo para o parâmetro 'item' (pode ser qualquer subclasse de ItemDeLeitura)
    def adicionar_item(self, item: ItemDeLeitura) -> None:
        """Adiciona um item (Livro, Revista ou HQ) à estante."""
        self.itens.append(item)
        print(f"\n✅ '{item.titulo}' adicionado(a) à estante!")

    # Anotação de tipo no retorno (o método não retorna nada)
    def listar_todos(self) -> None:
        """Lista todos os itens presentes na estante."""
        if not self.itens:
            print("\n⚠️ A estante está vazia.")
            return
            
        print("\n📚 ITENS NA ESTANTE 📚")
        print("-" * 30)
        for item in self.itens:
            print(f"- [{item.__class__.__name__}] {item}")
        print("-" * 30)

    # Anotações de tipo nos parâmetros e retorno
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
    
    # Anotações de tipo nos parâmetros e retorno. 
    # 'type' é usado para indicar que espera-se uma classe como parâmetro.
    def exibir_detalhes_por_tipo(self, tipo_classe: type) -> None:
        """Lista e exibe detalhes de itens de um tipo específico."""
        
        itens_do_tipo = [item for item in self.itens if isinstance(item, tipo_classe)]
        
        if not itens_do_tipo:
            print(f"\n⚠️ Nenhum(a) {tipo_classe.__name__} encontrado(a) na estante.")
            return
            
        print(f"\n DETALHES DE {tipo_classe.__name__.upper()}S ")
        print("=" * 30)
        for item in itens_do_tipo:
            print(item.detalhes())
            print("=" * 30)

# 4. FUNÇÃO DO MENU (Interface com o usuário)
# A anotação de tipo 'Estante' garante que o VS Code saiba o que é 'estante' dentro da função.
def exibir_menu(estante: Estante) -> None:
    """Exibe o menu principal e gerencia as interações do usuário."""
    
    while True:
        print("\n╔═══════════════════════════════════╗")
        print("║          ESTANTE VIRTUAL          ║")
        print("╠═══════════════════════════════════╣")
        print("║ 1. Adicionar Item                 ║")
        print("║ 2. Listar Todos os Itens          ║")
        print("║ 3. Buscar por Título              ║")
        print("║ 4. Detalhes de Livros             ║")
        print("║ 5. Detalhes de Revistas           ║")
        print("║ 6. Detalhes de HQs                ║")
        print("║ 0. Sair                           ║")
        print("╚═══════════════════════════════════╝")
        
        escolha = input("➡️ Digite sua opção: ")
        
        if escolha == '1':
            menu_adicionar(estante)
        elif escolha == '2':
            estante.listar_todos()
        elif escolha == '3':
            termo = input("Digite o título ou parte dele para buscar: ")
            estante.buscar_por_titulo(termo)
        elif escolha == '4':
            estante.exibir_detalhes_por_tipo(Livro)
        elif escolha == '5':
            estante.exibir_detalhes_por_tipo(Revista)
        elif escolha == '6':
            estante.exibir_detalhes_por_tipo(HQ)
        elif escolha == '0':
            print("\n👋 Saindo do sistema. Até mais!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")

# Anotação de tipo para o parâmetro 'estante'
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
        
    # Coleta de dados comuns
    titulo = input("Título: ")
    autor = input("Autor/Escritor: ")
    
    if tipo == 'a':
        try:
            paginas = int(input("Número de Páginas: "))
            # A variável novo_item é inferida como Livro, que é um ItemDeLeitura
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
    minha_estante = Estante()
    
    # Adiciona alguns itens de exemplo (Opcional, para testes iniciais)
    minha_estante.adicionar_item(Livro("A Sociedade do Anel", "J.R.R. Tolkien", 576))
    minha_estante.adicionar_item(HQ("Watchmen", "Alan Moore", "Dave Gibbons"))
    minha_estante.adicionar_item(Revista("Python Magazine", "Equipe XYZ", "150", "Setembro"))
    minha_estante.adicionar_item(Livro("O Hobbit", "J.R.R. Tolkien", 300))

    # Inicia o menu
    exibir_menu(minha_estante)