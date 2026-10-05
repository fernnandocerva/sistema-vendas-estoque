
"""
Sistema de Vendas e Estoque (versão terminal) - v2

Finalidade: controlar o estoque de uma loja pequena, montar um carrinho
de compras, aplicar desconto e frete e finalizar a venda.

Como rodar:  python main.py
"""

# ---------------------------------------------------------------
# DADOS DA LOJA
# ---------------------------------------------------------------
# Cada produto guarda o seu preço e a sua quantidade em estoque.
# Os preços são só exemplos, troque pelos que quiser.
estoque = {
    "mouse":   {"preco": 40.00,  "quantidade": 8},
    "teclado": {"preco": 90.00,  "quantidade": 5},
    "monitor": {"preco": 650.00, "quantidade": 2},
}

# O carrinho guarda só o nome do produto e a quantidade escolhida.
# Exemplo: {"mouse": 2, "teclado": 1}
# O estoque só diminui quando a compra é finalizada.
carrinho = {}

# Regras da loja (mude aqui e o sistema inteiro se ajusta)
DESCONTO_A_PARTIR_DE = 100.00   # compras a partir deste valor ganham desconto
DESCONTO_PERCENTUAL = 5         # percentual do desconto (5 = 5%)
FRETE_GRATIS_A_PARTIR_DE = 150.00
FRETE_LOCAL = 12.00
FRETE_OUTRA_REGIAO = 25.00


# ---------------------------------------------------------------
# FUNÇÕES AUXILIARES DE ENTRADA
# ---------------------------------------------------------------
def ler_inteiro(mensagem):
    """Pede um número inteiro e repete a pergunta se o usuário digitar errado."""
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit():
            return int(texto)
        print("Valor inválido. Digite apenas números inteiros.")


def ler_preco(mensagem):
    """Pede um valor em reais. Aceita 12,50  12.50  ou  2.999,90."""
    while True:
        texto = input(mensagem).strip()
        if "," in texto:
            texto = texto.replace(".", "")   # tira o ponto de milhar (2.999,90)
        texto = texto.replace(",", ".")      # vírgula vira ponto decimal
        try:
            valor = float(texto)
        except ValueError:
            print("Valor inválido. Exemplo: 25,90")
            continue
        if valor <= 0:
            print("O preço precisa ser maior que zero.")
            continue
        return valor


def ler_produto():
    """Pede o nome de um produto e padroniza (minúsculo, sem espaços sobrando)."""
    return input("Digite o nome do produto: ").strip().lower()


def formatar_reais(valor):
    """Formata um número no padrão brasileiro: 1234.5 -> 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}"                       # 1,234.50
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


# ---------------------------------------------------------------
# ESTOQUE
# ---------------------------------------------------------------
def listar_produtos():
    """Mostra todos os produtos com preço e quantidade em estoque."""
    print("\n--- PRODUTOS EM ESTOQUE ---")
    if not estoque:
        print("Nenhum produto cadastrado.")
        return
    for nome, dados in estoque.items():
        print(f"{nome.capitalize():<12} {formatar_reais(dados['preco']):>12}   "
              f"{dados['quantidade']} unidade(s)")


def consultar_estoque():
    """Mostra quantas unidades existem de um produto."""
    produto = ler_produto()

    if produto in estoque:
        quantidade = estoque[produto]["quantidade"]
        print(f"Temos {quantidade} unidade(s) de {produto} no estoque.")
    else:
        print(f"{produto} não existe no estoque.")


def cadastrar_produto():
    """Cadastra um produto novo com preço e quantidade inicial."""
    produto = ler_produto()

    if produto == "":
        print("O nome do produto não pode ficar vazio.")
        return
    if produto in estoque:
        print(f"{produto} já está cadastrado. Use 'Repor estoque' para somar unidades.")
        return

    preco = ler_preco("Preço (R$): ")
    quantidade = ler_inteiro("Quantidade inicial: ")

    estoque[produto] = {"preco": preco, "quantidade": quantidade}
    print(f"{produto} cadastrado com sucesso!")


def repor_estoque():
    """Soma unidades ao estoque de um produto que já existe."""
    produto = ler_produto()

    if produto not in estoque:
        print("Produto não cadastrado. Cadastre primeiro.")
        return

    quantidade = ler_inteiro("Quantas unidades chegaram? ")
    estoque[produto]["quantidade"] += quantidade
    print(f"Estoque de {produto} agora: {estoque[produto]['quantidade']} unidade(s).")


# ---------------------------------------------------------------
# CARRINHO
# ---------------------------------------------------------------
def adicionar_ao_carrinho():
    """Adiciona um produto ao carrinho, sem passar do que existe no estoque."""
    produto = ler_produto()

    if produto not in estoque:
        print("Produto não cadastrado.")
        return

    quantidade = ler_inteiro("Digite a quantidade desejada: ")
    if quantidade <= 0:
        print("A quantidade precisa ser maior que zero.")
        return

    # Conta o que já está no carrinho para não passar do estoque
    ja_no_carrinho = carrinho.get(produto, 0)
    disponivel = estoque[produto]["quantidade"]

    if ja_no_carrinho + quantidade > disponivel:
        print(f"Estoque insuficiente. Temos {disponivel} unidade(s) "
              f"e você já tem {ja_no_carrinho} no carrinho.")
        return

    carrinho[produto] = ja_no_carrinho + quantidade
    print(f"{quantidade}x {produto} adicionado(s) ao carrinho.")


def remover_do_carrinho():
    """Remove unidades de um produto do carrinho."""
    produto = ler_produto()

    if produto not in carrinho:
        print(f"{produto} não está no carrinho.")
        return

    quantidade = ler_inteiro("Quantas unidades remover? ")
    if quantidade <= 0:
        print("A quantidade precisa ser maior que zero.")
        return

    if quantidade >= carrinho[produto]:
        del carrinho[produto]        # tirou tudo: apaga o produto do carrinho
        print(f"{produto} removido do carrinho.")
    else:
        carrinho[produto] -= quantidade
        print(f"Agora há {carrinho[produto]} unidade(s) de {produto} no carrinho.")


def calcular_subtotal():
    """Soma o valor de todos os itens do carrinho (sem desconto e sem frete)."""
    subtotal = 0
    for produto, quantidade in carrinho.items():
        subtotal += estoque[produto]["preco"] * quantidade
    return subtotal


def calcular_desconto(subtotal):
    """Desconto percentual para compras a partir de um valor mínimo."""
    if subtotal >= DESCONTO_A_PARTIR_DE:
        return subtotal * DESCONTO_PERCENTUAL / 100
    return 0.00


def calcular_frete(valor_produtos, regiao):
    """
    Regras:
    - compras a partir do valor mínimo têm frete grátis
    - abaixo disso: frete local ou de outra região
    """
    if valor_produtos >= FRETE_GRATIS_A_PARTIR_DE:
        return 0.00
    if regiao == "local":
        return FRETE_LOCAL
    return FRETE_OUTRA_REGIAO


def ver_carrinho():
    """Mostra o que há no carrinho, com o subtotal e o desconto."""
    print("\n--- SEU CARRINHO ---")
    if not carrinho:
        print("O carrinho está vazio.")
        return

    for produto, quantidade in carrinho.items():
        preco = estoque[produto]["preco"]
        print(f"{produto.capitalize():<12} {quantidade} x {formatar_reais(preco)}"
              f" = {formatar_reais(preco * quantidade)}")

    subtotal = calcular_subtotal()
    desconto = calcular_desconto(subtotal)
    print(f"\nSubtotal: {formatar_reais(subtotal)}")
    if desconto > 0:
        print(f"Desconto de {DESCONTO_PERCENTUAL}%: -{formatar_reais(desconto)}")


def cancelar_compra():
    """Esvazia o carrinho. O estoque não é alterado."""
    carrinho.clear()
    print("Compra cancelada. Carrinho vazio.")


# ---------------------------------------------------------------
# FINALIZAR COMPRA
# ---------------------------------------------------------------
def finalizar_compra():
    """Aplica desconto e frete, dá baixa no estoque e esvazia o carrinho."""
    if not carrinho:
        print("O carrinho está vazio. Adicione produtos primeiro.")
        return

    regiao = input("A entrega é 'local' ou 'outra' região? ").strip().lower()
    if regiao not in ("local", "outra"):
        print("Região inválida. Use 'local' ou 'outra'.")
        return

    # Processamento
    subtotal = calcular_subtotal()
    desconto = calcular_desconto(subtotal)
    valor_com_desconto = subtotal - desconto
    frete = calcular_frete(valor_com_desconto, regiao)   # frete olha o valor já com desconto
    total = valor_com_desconto + frete

    # Saída
    print("\n==================================================")
    print("                 RESUMO DO PEDIDO                 ")
    print("==================================================")
    for produto, quantidade in carrinho.items():
        preco = estoque[produto]["preco"]
        print(f"{produto.capitalize():<12} {quantidade} x {formatar_reais(preco)}"
              f" = {formatar_reais(preco * quantidade)}")
    print("--------------------------------------------------")
    print(f"Subtotal:  {formatar_reais(subtotal)}")
    if desconto > 0:
        print(f"Desconto ({DESCONTO_PERCENTUAL}%): -{formatar_reais(desconto)}")
    if frete == 0:
        print("Frete:     GRÁTIS")
    else:
        print(f"Frete:     {formatar_reais(frete)}")
    print(f"TOTAL:     {formatar_reais(total)}")
    print("==================================================")

    # Dá baixa no estoque só agora, com a compra confirmada
    for produto, quantidade in carrinho.items():
        estoque[produto]["quantidade"] -= quantidade

    carrinho.clear()
    print("Compra finalizada com sucesso!")


# ---------------------------------------------------------------
# MENU PRINCIPAL
# ---------------------------------------------------------------
def mostrar_cabecalho():
    print("##################################################")
    print("#          SISTEMA DE VENDAS E ESTOQUE           #")
    print("##################################################")


def mostrar_menu():
    print("--- ESTOQUE ---")
    print("1 - Listar produtos")
    print("2 - Consultar estoque de um produto")
    print("3 - Cadastrar produto novo")
    print("4 - Repor estoque")
    print("--- COMPRA ---")
    print("5 - Adicionar ao carrinho")
    print("6 - Remover do carrinho")
    print("7 - Ver carrinho")
    print("8 - Finalizar compra")
    print("9 - Cancelar compra")
    print("0 - Sair")


def menu():
    """Repete o menu até o usuário escolher sair (opção 0)."""
    mostrar_cabecalho()

    # Cada opção do menu aponta para a função que ela executa
    opcoes = {
        "1": listar_produtos,
        "2": consultar_estoque,
        "3": cadastrar_produto,
        "4": repor_estoque,
        "5": adicionar_ao_carrinho,
        "6": remover_do_carrinho,
        "7": ver_carrinho,
        "8": finalizar_compra,
        "9": cancelar_compra,
    }

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        elif opcao in opcoes:
            opcoes[opcao]()      # chama a função da opção escolhida
        else:
            print("Opção inválida. Tente novamente.")


# Só roda o menu quando o arquivo é executado diretamente
if __name__ == "__main__":
    menu()