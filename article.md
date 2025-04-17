# Como desenvolvi um Order Book e Matching Engine com SOLID e Design Patterns na prática

<!-- ## ✨ Introdução -->

Sempre fui um grande entusiasta do mercado financeiro. Por anos atuando na área, tive bastante contato com o mercado de bolsa e balcão, onde compradores e vendedores fazem ofertas que formam o chamado **"livro de ofertas"**, ou **"order book"** — base de funcionamento de home brokers e corretoras online, como as usadas para comprar bitcoin.

Como engenheiro de software, decidi construir do zero um **matching engine** (motor de negociação, com order book) inspirado nessas corretoras tradicionais. 

A ideia era simples: não só fazer funcionar, mas construir algo que demonstrasse **arquitetura sólida**, **princípios de design** e **boas práticas de engenharia de software**, utilizando **Python**.

Então, se você trabalha com backend, fintech ou curte arquitetura limpa, esse artigo pode ser interessante.

Para começar, deixo abaixo alguns pontos que talvez nem todos saibam sobre mercado financeiro e livro de ordens.

O primeiro deles, é claro, um exemplo de order book:



<table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; background-color: #f9f9f9;">
  <thead>
    <tr>
      <!-- Header: Livro de Compras -->
      <th colspan="3" style="background-color: #1e4023; color: white; padding: 10px; border: 1px solid #ccc; text-align: center; font-size: 16px;">
        📈 Livro de Compras
      </th>
      <th style="padding: 10px; border: none;"></th>
      <!-- Header: Livro de Vendas -->
      <th colspan="3" style="background-color: #5e1f1f; color: white; padding: 10px; border: 1px solid #ccc; text-align: center; font-size: 16px;">
        📉 Livro de Vendas
      </th>
    </tr>
    <tr>
      <th style="background-color: #1e4023; color: white; padding: 8px; border: 1px solid #ccc;">Tipo</th>
      <th style="background-color: #1e4023; color: white; padding: 8px; border: 1px solid #ccc; text-align: center;">Quantidade (BTC)</th>
      <th style="background-color: #1e4023; color: white; padding: 8px; border: 1px solid #ccc;">Preço (US$)</th>
      <th style="padding: 8px; border: none;"></th>
      <th style="background-color: #5e1f1f; color: white; padding: 8px; border: 1px solid #ccc;">Preço (US$)</th>
      <th style="background-color: #5e1f1f; color: white; padding: 8px; border: 1px solid #ccc; text-align: center;">Quantidade (BTC)</th>
      <th style="background-color: #5e1f1f; color: white; padding: 8px; border: 1px solid #ccc;">Tipo</th>
    </tr>
  </thead>
  <tbody>
    <!-- Topo: maior compra e menor venda -->
    <tr>
      <td style="padding: 8px; border: 1px solid #ccc; background-color: #e0f4e0;">Compra (Topo)</td>
      <td style="padding: 8px; border: 1px solid #ccc; text-align: center; background-color: #e0f4e0;">0.6</td>
      <td style="background-color: #2e8b57; color: white; padding: 8px; border: 1px solid #ccc; font-weight: bold;">99,900.00</td>
      <td></td>
      <td style="background-color: #d34f4f; color: white; padding: 8px; border: 1px solid #ccc; font-weight: bold;">100,100.00</td>
      <td style="padding: 8px; border: 1px solid #ccc; text-align: center; background-color: #fbeaea;">0.4</td>
      <td style="padding: 8px; border: 1px solid #ccc; background-color: #fbeaea;">Venda (Topo)</td>
    </tr>
    <!-- Demais ordens -->
    <tr>
      <td style="padding: 8px; border: 1px solid #ccc; background-color: #e0f4e0;">Compra</td>
      <td style="padding: 8px; border: 1px solid #ccc; text-align: center; background-color: #e0f4e0;">1.0</td>
      <td style="background-color: #2e8b57; color: white; padding: 8px; border: 1px solid #ccc;">99,800.00</td>
      <td></td>
      <td style="background-color: #d34f4f; color: white; padding: 8px; border: 1px solid #ccc;">100,200.00</td>
      <td style="padding: 8px; border: 1px solid #ccc; text-align: center; background-color: #fbeaea;">0.8</td>
      <td style="padding: 8px; border: 1px solid #ccc; background-color: #fbeaea;">Venda</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ccc; background-color: #e0f4e0;">Compra</td>
      <td style="padding: 8px; border: 1px solid #ccc; text-align: center; background-color: #e0f4e0;">0.7</td>
      <td style="background-color: #2e8b57; color: white; padding: 8px; border: 1px solid #ccc;">99,700.00</td>
      <td></td>
      <td style="background-color: #d34f4f; color: white; padding: 8px; border: 1px solid #ccc;">100,300.00</td>
      <td style="padding: 8px; border: 1px solid #ccc; text-align: center; background-color: #fbeaea;">0.5</td>
      <td style="padding: 8px; border: 1px solid #ccc; background-color: #fbeaea;">Venda</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ccc; background-color: #e0f4e0;">Compra</td>
      <td style="padding: 8px; border: 1px solid #ccc; text-align: center; background-color: #e0f4e0;">0.3</td>
      <td style="background-color: #2e8b57; color: white; padding: 8px; border: 1px solid #ccc;">99,600.00</td>
      <td></td>
      <td style="background-color: #d34f4f; color: white; padding: 8px; border: 1px solid #ccc;">100,400.00</td>
      <td style="padding: 8px; border: 1px solid #ccc; text-align: center; background-color: #fbeaea;">0.6</td>
      <td style="padding: 8px; border: 1px solid #ccc; background-color: #fbeaea;">Venda</td>
    </tr>
  </tbody>
</table>



> 📘 **O que é o Order Book?**
>
> O **order book** mostra, em tempo real, quem quer comprar e quem quer vender um ativo, junto com os respectivos preços e quantidades.
>
> - Do **lado esquerdo**, estão as ordens de **compra**, organizadas do **maior para o menor preço**.
> - Do **lado direito**, as ordens de **venda**, organizadas do **menor para o maior preço**.
>
> 💡 O topo de cada lado representa o **melhor preço disponível** naquele momento:
> - O **maior preço de compra** (quem paga mais).
> - O **menor preço de venda** (quem vende mais barato).
>
> Quando esses dois preços se cruzam — ou seja, quando **alguém aceita o preço do outro lado** — acontece um **trade**, ou seja, a negociação é executada.



**Ordem a mercado (market order):**  
É uma ordem executada imediatamente ao melhor preço disponível no livro de ofertas. Prioriza velocidade de execução em vez de preço, mas sua execução depende da liquidez (quantidade disponível no order book) do mercado no momento.

**Ordem limite (limit order):**  
É uma ordem para **tentar** comprar ou vender a um preço específico. Garante controle sobre o preço, mas pode não ser executada se o mercado não atingir o valor desejado.

**Trade (Ordem que foi executada):**  
Basicamente, o Trade é uma ordem que foi executada. Por exemplo, se um comprador faz uma oferta para comprar 1 Bitcoin por USD 100.000 e um vendedor aceita essa oferta, essa negociação é concretizada e registrada como um Trade. Ou seja, o Trade é o resultado do encontro entre uma ordem de compra e uma ordem de venda com condições compatíveis.


## 🧠 O problema

**Matching engines** são o coração de bolsas de valores e exchanges. 

Eles precisam casar ordens de compra e venda com regras claras, lidar com diferentes tipos de ordens, priorização por preço e tempo e manter histórico de negociações. 

Além disso, é preciso velocidade. Por exemplo, como casar essas ordens de forma veloz, sem que hajam erros? 

Aqui, entram algoritmos importantes como [Heap](https://www.geeksforgeeks.org/heap-data-structure/?ref=header_outind), [Binary Search Tree (BST)](https://www.geeksforgeeks.org/binary-search-tree-data-structure/?ref=header_outind
), entre outros. Cada um tem suas vantagens particulares que não vou aprofundar aqui neste artigo, o Heap por exemplo traz uma complexidade `O(1)` para obter máximos e mínimos, o que é perfeito para obter Bid e Ask de um orderbook em tempo mínimo.


Neste artigo, usei Heap com a biblioteca `heapq` para deixar sempre no topo do order book os melhores preços, sejam de compra ou venda.

O desafio: como criar isso de forma **modular, testável e extensível**?

A estrutura do projeto foi dividida da forma mais clara possivel no momento.

```plaintext
matching-engine/
├── core/                      # Núcleo do sistema: onde mora a lógica principal
│   ├── __init__.py
│   ├── factory.py             # Fábrica para criação de ordens
│   ├── interfaces.py          # Interfaces (ABCs) para garantir contratos
│   ├── matching.py            # Estratégias e lógica de matching
│   ├── orderbook.py           # Implementação do livro de ordens (order book)
│   ├── orders.py              # Modelos de ordens (limit, market, etc)
│   ├── trades.py              # Representação de trades realizados
│
├── logs/                      # Armazena os logs gerados durante execução com data e hora
│   └── log-12-03-2025.txt                 # (ex: app.log, errors.log, etc.)
│
├── services/                  # Serviços auxiliares
│   └── trade_manager.py       # Gerencia e armazena os trades realizados
│
├── tests/                     # Testes automatizados
│   └── test_core.py           # Testes básicos das funcionalidades (Não Unitários!!)
│
├── utils/                     # Utilitários e funções de suporte
│   ├── logger.py              # Configuração de logging
│   └── helpers.py             # Funções utilitárias diversas
│
├── .gitignore                 # Arquivos e pastas ignorados pelo Git
├── README.md                  # Documentação principal do projeto
├── main.py                    # Entry point da aplicação (pode rodar o sistema)
├── requirements.txt           # Dependências do projeto (ex: via pip)
```


## ▶️ Exemplo de Uso

Here's a simple usage example to get started with the matching engine:

```python
from core.matching import LimitOrderMatching, MarketOrderMatching
from core.factory import OrderFactory
from core.orders import LimitOrder, MarketOrder
from services.trade_manager import TradeManager
from core.orderbook import HeapOrderBook

# Setup: Register order types and matching strategies
strategies = {
    "limit": LimitOrderMatching(),
    "market": MarketOrderMatching(),
}

OrderFactory.register_order_type("limit", LimitOrder)
OrderFactory.register_order_type("market", MarketOrder)

# Initialize the order book
order_book = HeapOrderBook("BTC-USD", TradeManager(), strategies)

# Add limit orders (buy & sell)
order_book.addOrder(
    order_type="limit",
    order=OrderFactory.create_order(
      "limit", 
      order_id=1, 
      price=100, 
      quantity=10, 
      order_side="buy", 
      asset="BTC-USD"
      )
)
order_book.addOrder(
    order_type="limit",
    order=OrderFactory.create_order(
      "limit", 
      order_id=2, 
      price=105, 
      quantity=5, 
      order_side="sell", 
      asset="BTC-USD"
      )
)

# Top-of-book inspection
order_book.getBid()
order_book.getAsk()

# Add a market order that triggers matching
order_book.addOrder(
    order_type="market",
    order=OrderFactory.create_order(
      "market", 
      order_id=3, 
      quantity=15, 
      order_side="buy", 
      asset="BTC-USD"
      )
)


# log recorded trades, look in folder /logs
order_book.trade_manager.list_trades()

```

## 🛠️ Como desenvolvi o projeto com SOLID + Design Patterns

Muito se fala em SOLID, conjunto de praticas para desenvolver codigo orientado a objeto de forma escalavel XXXXX, como algo muito tecnico, mas de certa forma já da pra sentir a sua importância em certos momentos:
1) Quando você precisar de corrigir certas funções, e sua pequena correção vira uma caça interminável.
2) Ainda resultado da primeira, quando uma alteração poderia ter sido muito mais simples se o desenho inicial do projeto tivesse seguido alguma regras, essas regras eu descobri que moram no SOLID.


# Princípios SOLID

1. S — Single Responsibility Principle (Responsabilidade Única)
   Cada classe deve ter apenas uma responsabilidade e uma única razão para mudar.

2. O — Open/Closed Principle (Aberto/Fechado)
   O código deve estar aberto para extensão, mas fechado para modificação.

3. L — Liskov Substitution Principle (Substituição de Liskov)
   Subtipos devem poder substituir seus tipos base sem quebrar o sistema.

4. I — Interface Segregation Principle (Segregação de Interfaces)
   Prefira várias interfaces específicas a uma única interface genérica e inchada.

5. D — Dependency Inversion Principle (Inversão de Dependência)
   Dependa de abstrações, não de implementações concretas.

Vou exemplificar cada um desses principios direto no projeto:

### ✅ Single Responsibility Principle (SRP)

> Cada classe tem uma única responsabilidade clara:

- `HeapOrderBook`: gerencia o estado das ordens (ver orderbook.py)
- `OrderFactory`: registra e instancia diferentes tipos de ordens (ver factory.py)
- `Trade`: é a classe que cuida da representação dos trades (ver trades.py)
- `TradeManager`: Cuida do registro e da listagem dos trades existentes (ver matching.py)

🔍 *Isso deixa o código desacoplado, fácil de testar e de extender.*

Mas mais que isso, não chega na granularidade de uma classe fazer uma coisa só, como somar por exemplo, mas sim realizar uma tarefa. `TradeManager`, vai cuidar dos trades, mas essa classe pode fazer diversas coisas com os trades, gravar, alterar, então é uma forma de separar responsabilidades por tema, digamos. E veja bem, não é preciso que uma classe `Trade` faça absolutamente tudo relacionado ao trade, mas tudo que se proponha a fazer, por exemplo `Trade` cuida só da representação, e `TradeManager` cuida do registro e da listagem, e não há problema nisso.


### 🔁 Open/Closed Principle (OCP)

> Aberto para extensão, fechado para modificação

As ordens são construídas com herança e interfaces, podendo ser estendidas sem modificar código existente:

```python
class OrderBookInterface(ABC):

    @abstractmethod
    def addOrder(self, order_type, order) -> None:
        pass

    @abstractmethod
    def removeOrder(self, order_id: int) -> None:
        pass
```
O exemplo acima pega por exemplo a criação de uma interface para o Order Book usando classe abstrata `ABC` da biblioteca padrão python, mas o porquê disso? ali, por simplicidade, peguei somente duas funções básicas pra exemplificar seu conteúdo, mas pense só, se eu criasse uma classe `OrderBook()` e injetasse ela em outras classes e arquivos do projeto e o sistema crescesse bastante, seria inteligente?. Amanhã surge uma demanda e meu OrderBook não serve mais e preciso alterá-lo. O que isso vai gerar? um caça infinita nó código e com certeza vou ter que alterar o código de `OrderBook()`, certo? mas e se eu criasse outra classe? e não mexesse em `OrderBook()`, criasse por exemplo `NewOrderBook()`?, é aí que mora a utilidade do OCP, não prejudico quem já usa o `OrderBook()` por que não vou mexer nele, e resolvo meu problema com meu novo order book `NewOrderBook()`. E claro `NewOrderBook(OrderBookInterface)` herda de `OrderBookInterface(ABC)` assim como minha antiga `OrderBook(OrderBookInterface)`, ou seja, extendem da minha interface, isso que o OCP prega.

👎 *Errado seria algo assim: usar OrderBook para todo mundo sem pensar em futuras alterações*

```python
class OrderBook():

    def addOrder(self, order_type, order) -> None:
        pass

    def removeOrder(self, order_id: int) -> None:
        pass
```

---

### 🧼 Liskov Substitution Principle (LSP)

> Subtipos devem substituir seus tipos base sem quebrar o sistema

Exemplo real: `ConvertibleMarketOrder` herda de `MarketOrder`, que herda de `BaseOrder`.

```python
class AbstractOrder(ABC):
    def __init__(self, order_id: int, quantity: int, order_side: str, asset: str):
        self.order_id = order_id
        self.quantity = quantity
        self.order_side = order_side
        self.asset = asset
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

class BaseOrder(AbstractOrder):
    def __init__(
        self,
        order_id: int,
        quantity: int,
        order_side: str,
        asset: str,
        partial_fill_behavior: str,
        fallback_price: float,
    ):
        super().__init__(order_id, quantity, order_side, asset)
        self.partial_fill_behavior = partial_fill_behavior
        self.fallback_price = fallback_price

class MarketOrder(BaseOrder):
    def __init__(
        self, order_id, quantity, order_side, asset, partial_fill_behavior="cancel", fallback_price = None,
    ):
        super().__init__(order_id, quantity, order_side, asset, partial_fill_behavior, fallback_price)

class ConvertibleMarketOrder(MarketOrder):
    def __init__(self, order: MarketOrder):
        super().__init__(order.order_id, order.quantity, order.order_side, order.asset,order.partial_fill_behavior, order.fallback_price)

    def convert_to_limit(self, price):
        """Convert order to limit if needed, as a market order
        that has to be hanged in book because of lacking liquidity"""
        if price is None:
            raise ValueError("Cannot convert to limit order without a price.")

        return LimitOrder(
            self.order_id, price, self.quantity, self.order_side, self.asset
        )


class PricedOrder(AbstractOrder):
    def __init__(self, order_id, price, quantity, order_side, asset):
        super().__init__(order_id, quantity, order_side, asset)
        self.price = price

class LimitOrder(PricedOrder):
    def __init__(self, order_id, price, quantity, order_side, asset):
        super().__init__(order_id, price, quantity, order_side, asset)

```
Podemos observar que ao longo da hierarquia de heranças como `BaseOrder(AbstractOrder)`herdando de `AbstractOrder`novo atributos vão sendo adicionados, como `partial_fill_behavior` e `fallback_price`, e isso não fere Liskov, o contrário iria ferir diretamente, se nas classes filhas não houvessem todos os atributos que existiam na classe pai, pois dessa forma a classe filha não poderia substituir a classe pai, já que ela não possui todos os atributos do pai, correto?
Por exemplo, posso passar `ConvertibleMarketOrder` onde se espera `MarketOrder`. E isso não traz comportamentos inesperados. Posso também passar `LimitOrder` onde se espera `PricedOrder`, agora claramente não posso passar `MarketOrder` onde se espera `LimitOrder`, pois `LimitOrder` tem preço e `MarketOrder` não possui esse atributo, e é por isso também que elas herdam de classes diferentes. Você pode se questionar se isso vale somente para atributos, mas não, métodos também, caso algum método impeça que a classe filha susbtitua a sua classe pai elá irá ferir Liskov. Como exemplo, refleti um bom tempo se o método `convert_to_limit(price)` da classe `ConvertibleMarketOrder` feriria Liskov pois ele trás a capacidade de uma ordem do tipo `MarketOrder` a se transformar numa `LimitOrder`, e a resposta é não! mas é sútil, ele não transforma a `ConvertibleMarketOrder` que é do tipo `MarketOrder` em `LimitOrder`, mas sim retorna uma nova ordem do tipo limite. Se de fato transformasse a ordem numa ordem limite sem avisar ou de forma obscura aí teríamos um problema, pois uma ordem limite tem preço e não se espera que uma ordem a mercado `MarketOrder` tenha preço, então essa transformação feriria Liskov, mas na realidade ele retornou uma nova ordem, fez sentido?



---

### 🔬 Interface Segregation Principle (ISP)

> Não force classes a implementarem métodos que não usam

Usei interfaces específicas para cada tipo de funcionalidade:

```python
class TradeStorage(ABC):
    def record_trade(self, trade): ...

class TradeHistory(ABC):
    def list_trades(self): ...

```

👎 *Errado seria algo assim:*

```python
class TradeManager:
    def record_trade(self)
    def list_trades(self)
```

✅ *Certo: criei contratos específicos pro necessário:*

```python
class TradeManagerInterface(TradeStorage, TradeHistory): ...

class TradeManager(TradeManagerInterface):

    def record_trade(self, trade): ...
       
    def list_trades(self): ...
```

Esse princípio é interessante e muito útil, o exemplo acima acho que exemplifica muito bem. Preciso de um trade manager pro meu projeto que por exemplo, grave e liste os trades existentes, simples certo? então pode ser óbvio pensar em criar algo como mostrado no exemplo errado acima, qual o problema dele? é que toda vez que alguem for usar a classe `TradeManager`, vai ser obrigada a carregar os dois métodos, mas e se eu só quiser, usar o record_trade? não seria legal e mais limpo separar isso em classes diferentes então? como `TradeStorage()`e `TradeHistory()` por que aí posso chamar só o que eu preciso, concorda? como por exemplo acima
`TradeManager(TradeManagerInterface)`herda de `TradeManagerInterface`, que herda de `TradeStorage()` e `TradeHistory()`, mas poderia herdar de outras interfaces, que poderiam herdar somente de uma delas por vez ou com a combinação desejada, essa é a utilidade de interfaces, e daí a utilidade do ISP.

---

### 🔌 Dependency Inversion Principle (DIP)

> Dependa de abstrações, não implementações

No `OrderBook`, injeto tudo por interfaces:

```python
class HeapOrderBook(OrderBookInterface):
    def __init__(
        self,
        asset,
        trade_manager: TradeManagerInterface,
        strategies: dict[str, MatchingStrategy],
    ):
        ...
```

Assim, posso passar implementações diferentes `TradeManagerA(TradeManagerInterface)` ou `TradeManagerB(TradeManagerInterface)` com funcionalidades únicas  para a variável `trade_manager` pois ambos herdam de `TradeManagerInterface`, e serão aceitos, assim como mudar a lógica de matching pois strategies aceitam um dicionário com todas estratégias que herdem de `MatchingStrategy`. Ou seja, usar interfaces que funcionam como abstrações nos permitem criar uma máscara para infinitas implementações diferentes, que podem ser necessárias no futuro, e além disso que evitem mudanças extensivas no código.

```python

class TradeManagerA(TradeManagerInterface):
    pass

class TradeManagerB(TradeManagerInterface):
    pass

class MarketOrderMatching(MatchingStrategy):
    pass

class LimitOrderMatching(MatchingStrategy):
    pass

```

## 🧱 Design Patterns usados

- **Factory Pattern**: instanciando ordens via `OrderFactory.create_order(...)`
- **Strategy Pattern**: lógica de matching separada em `LimitOrderMatching` e `MarketOrderMatching`

---

## 📂 Repositório

👉 [github.com/paasxx/OrderBook](https://github.com/paasxx/OrderBook)

Prints do terminal, arquivos de log e execução de trades disponíveis no repositório.

---

## 📣 Curtiu o projeto?


Me segue aqui no Medium ou conecta no [LinkedIn](https://www.linkedin.com/in/pedro-andre-silveira/) 🚀