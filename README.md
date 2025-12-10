# Aplicativo-Desktop-OO
## Estante Virtual - Gerenciador de Coleção (Python/Tkinter)

Este projeto é uma aplicação de desktop desenvolvida em Python para gerenciar uma coleção pessoal de itens de leitura (Livros, Revistas e HQs). A aplicação utiliza uma Interface Gráfica de Usuário (GUI) construída com a biblioteca Tkinter, incorporando estilos personalizados para um visual moderno e limpo.

### Tecnologias Utilizadas

* **Linguagem de Programação:** Python
* **Interface Gráfica:** Tkinter e Tkinter Themed (ttk)
* **Persistência de Dados:** SQLite

### Design Personalizado

A interface gráfica foi customizada para utilizar uma paleta de cores focada em tons de **Roxo (Deep Violet)** e **Lavanda**, proporcionando uma experiência visual coesa e agradável.

* O título principal é centralizado.
* Os botões de ação principal (Adicionar/Remover) são preenchidos com o roxo escuro.
* Os botões secundários (Detalhes/Atualizar) utilizam um estilo de contorno para diferenciação.
* A listagem de itens na tabela (`Treeview`) utiliza o roxo para o cabeçalho e para destacar a linha selecionada.

### Funcionalidades Principais

A aplicação suporta as operações essenciais de um gerenciador de coleções:

| Operação | Descrição |
| :--- | :--- |
| **Listar (Read)** | Exibe todos os itens salvos no banco de dados SQLite (`estante_virtual.db`) em uma tabela (`Treeview`). |
| **Adicionar (Create)** | Abre uma janela auxiliar que permite o cadastro de novos **Livros**, **Revistas** ou **HQs**, solicitando campos específicos para cada tipo. |
| **Remover (Delete)** | Exclui um item selecionado da lista e do banco de dados, após confirmação do usuário. |
| **Detalhes** | Exibe todas as propriedades de um item selecionado em uma caixa de diálogo informativa. |
| **Atualizar Lista** | Força a recarga dos dados diretamente do banco de dados, sincronizando a visualização. |


