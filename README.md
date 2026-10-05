#  Sistema de Vendas e Estoque (terminal)

Sistema em Python, executado no terminal feito com aprendizados de aula, para controlar o estoque de uma loja pequena, montar um carrinho de compras, aplicar desconto e frete e finalizar a venda.

##  Funcionalidades

**Estoque**
- Listar produtos com preço e quantidade
- Consultar o estoque de um produto
- Cadastrar produto novo
- Repor estoque

**Compra**
- Adicionar e remover itens do carrinho (sem ultrapassar o estoque disponível)
- Ver carrinho com subtotal e desconto
- Finalizar compra (dá baixa no estoque e esvazia o carrinho)
- Cancelar compra

## Regras da loja

Ficam no topo do `main.py` e podem ser alteradas facilmente:

| Regra | Valor padrão |
|---|---|
| Desconto | 5% em compras a partir de R$ 100,00 |
| Frete grátis | A partir de R$ 150,00 (calculado sobre o valor já com desconto) |
| Frete local | R$ 12,00 |
| Frete outra região | R$ 25,00 |

## Como rodar

Requisito: [Python 3](https://www.python.org/downloads/) instalado. Não precisa instalar nenhuma biblioteca.

```bash
git clone https://github.com/fernnandocerva/sistema-vendas-estoque.git
cd NOME-DO-REPOSITORIO
python main.py
```

## O que pratiquei neste projeto

- Dicionários para representar produtos e carrinho
- Funções com responsabilidade única
- Validação de entrada do usuário (números inteiros e preços no formato brasileiro, como `2.999,90`)
- Menu interativo com `while` e dicionário de funções
- Formatação de moeda no padrão brasileiro (`R$ 1.234,50`)

## Ideias para evoluir

- Salvar o estoque em arquivo (JSON ou CSV) para não perder os dados ao fechar
- Histórico de vendas
- Testes automatizados com `pytest`
- Interface gráfica ou versão web

## Autor

**Fernando Cerva** — [LinkedIn](https://linkedin.com/in/fernando-cerva-950041423)
