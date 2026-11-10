# Princípios de Design de Software: Guia Completo e Exemplos Práticos

A sustentabilidade de uma base de código ao longo do tempo depende fundamentalmente do respeito a princípios consolidados de design de software. Enquanto algumas aplicações se tornam inviáveis ou exigem reescritas completas após curtos períodos de desenvolvimento, outras permanecem flexíveis e fáceis de modificar mesmo após anos de evolução. A diferença crucial raramente reside na linguagem de programação ou nos frameworks adotados, mas sim na aplicação disciplinada de diretrizes arquiteturais que organizam responsabilidades, minimizam o acoplamento e preservam a clareza do sistema.

Neste guia, examinamos em detalhes os principais princípios de design de software — incluindo SOLID, DRY, KISS, YAGNI, Separação de Conceitos, Composição sobre Herança e a Lei de Demeter —, acompanhados por estruturas de código em Java que ilustram o problema original, a refatoração recomendada e os pontos de atenção em que o princípio pode ser levado ao extremo.

---

## 1. Princípios SOLID: Os Cinco Pilares Orientados a Objetos

O acrônimo SOLID reúne cinco princípios fundamentais projetados para estruturar classes e módulos orientados a objetos, garantindo alta coesão e facilidade de manutenção.

As cinco diretrizes que compõem o modelo são definidas da seguinte forma:

*   **Single Responsibility Principle (SRP):** Uma classe deve ter uma, e apenas uma, razão para mudar. Isso significa que a classe deve ser responsável por apenas um conceito ou função do sistema.
*   **Open-Closed Principle (OCP):** Entidades de software devem estar abertas para extensão, mas fechadas para modificação. Deve ser possível adicionar novos comportamentos sem alterar o código existente e já testado.
*   **Liskov Substitution Principle (LSP):** Subclasses devem ser capazes de substituir suas classes base em qualquer ponto do sistema sem alterar a integridade da aplicação.
*   **Interface Segregation Principle (ISP):** É preferível criar interfaces específicas e pequenas a ter uma única interface genérica e extensa que obrigue classes a implementar métodos dos quais não necessitam.
*   **Dependency Inversion Principle (DIP):** Módulos de alto nível devem depender de abstrações, e não de implementações concretas de baixo nível.

---

## 2. DRY (Don't Repeat Yourself): Centralização do Conhecimento

O princípio DRY estabelece que cada pedaço de conhecimento de negócio deve possuir uma representação única, não ambígua e autoritativa dentro de todo o sistema. A duplicidade de lógica de negócio em múltiplos pontos introduz sérios riscos de inconsistência quando as regras precisam ser atualizadas.

### O Problema da Regra Duplicada

Considere o cenário em que a regra de desconto para compras acima de 100 dólares é duplicada em dois serviços distintos da aplicação, como o serviço de carrinho (`CartService`) e o serviço de fatura (`InvoiceService`):

```java
// CartService
if (subtotal.compareTo(new BigDecimal("100")) > 0) {
  total = subtotal.multiply(new BigDecimal("0.90"));
}

// InvoiceService: a mesma regra duplicada
if (subtotal.compareTo(new BigDecimal("100")) > 0) {
  total = subtotal.multiply(new BigDecimal("0.90"));
}
```

Se a equipe de marketing alterar o valor do desconto para 15%, o desenvolvedor corre o risco de atualizar a regra no serviço de carrinho e esquecer o serviço de faturamento, gerando divergências em que o cliente vê um preço no carrinho e outro valor na fatura final.

### A Solução Centralizada

Para resolver essa duplicação, a regra de negócio é isolada em um único componente reutilizável responsável pela lógica de descontos:

```java
public final class Discounts {

  private static final BigDecimal THRESHOLD = new BigDecimal("100");
  private static final BigDecimal RATE = new BigDecimal("0.90");

  private Discounts() {}

  public static BigDecimal apply(BigDecimal subtotal) {
    BigDecimal total = subtotal.compareTo(THRESHOLD) > 0 ? subtotal.multiply(RATE) : subtotal;
    return total.setScale(2, RoundingMode.HALF_UP);
  }
}
```

### O Exagero no Princípio DRY

O princípio DRY foca na centralização do **conhecimento de negócio**, e não na simples eliminação de trechos de código que parecem idênticos visualmente. Caso dois métodos apresentem sintaxe semelhante hoje, mas mudem por razões de negócio completamente distintas no futuro, eles devem ser mantidos separados. Unificá-los prematuramente cria uma abstração incorreta, que frequentemente se enche de estruturas condicionais (`if`) para atender aos diferentes chamadores.

---

## 3. KISS (Keep It Simple): Simplicidade na Solução

O princípio KISS defende a escolha da solução mais simples e direta possível que atenda aos requisitos do problema. Códigos excessivamente complexos dificultam a leitura, tornam os testes mais trabalhosos e aumentam a probabilidade de falhas.

### Comparando Abordagens para Verificação de Duplicados

A verificação de elementos duplicados em uma lista de nomes pode ser escrita utilizando chamadas complexas à API de Streams do Java:

```java
boolean hasDuplicates = names.stream()
    .collect(Collectors.groupingBy(n -> n, Collectors.counting()))
    .values().stream()
    .anyMatch(count -> count > 1);
```

Embora o código acima funcione, sua leitura exige decodificação mental por parte do revisor. Uma abordagem fundamentada no princípio KISS aproveita a propriedade fundamental de uma coleção de conjunto (`Set`), que não aceita elementos duplicados:

```java
boolean hasDuplicates = new HashSet<>(names).size() < names.size();
```

A solução simplificada cumpre exatamente o mesmo objetivo em uma linha legível, permitindo que revisores e mantenedores confirmem a correção do código instantaneamente.

---

## 4. YAGNI (You Aren't Gonna Need It): Evitando Abstrações Prematuras

O princípio YAGNI estabelece que funcionalidades, interfaces ou pontos de flexibilidade não devem ser construídos até que exista um requisito real e imediato que os exija. A tentativa de prever necessidades futuras gera complexidade desnecessária e custos contínuos de manutenção.

### O Impacto da Flexibilidade Antecipada

Em um sistema que processa pagamentos via cartão de crédito no momento presente, a equipe de engenharia pode ser tentada a criar uma arquitetura genérica antecipando novos provedores:

```java
// Criado prematuramente para provedores de pagamento hipotéticos
public interface PaymentProvider { PaymentResult charge(Order order); }
public class PaymentProviderRegistry { /* localiza provedores por nome */ }
public class PaymentProviderConfigLoader { /* lê provedores de arquivos de configuração */ }
```

Caso o segundo provedor de pagamento nunca seja contratado, o sistema fica onerado com três classes adicionais que precisam ser lidas, testadas e mantidas sem necessidade. Além disso, quando um novo requisito real surgir, o design projetado por antecipação raramente se ajusta perfeitamente às reais demandas.

### Implementação Direta baseada em Requisitos Reais

A abordagem correta segundo o YAGNI é implementar estritamente o necessário para cobrir os requisitos atuais:

```java
public class CardPayments {
  public PaymentResult charge(Order order) {
    // chamada para a API de cartão de crédito e retorno do resultado
  }
}
```

Se a necessidade de integrar um segundo provedor surgirá no futuro, a extração de uma interface levará poucos minutos e será desenhada com base nas especificações concretas de dois provedores reais, e não em hipóteses.

---

## 5. Separação de Conceitos (Separation of Concerns): Organização em Camadas

A Separação de Conceitos orienta que cada componente do código deve ser responsável por apenas um domínio funcional específico, separando claramente responsabilidades como comunicação HTTP, regras de negócio e persistência de dados.

### Violação por Mistura de Responsabilidades

Um controlador REST que executa diretamente comandos SQL e valida regras de negócio mistura múltiplas preocupações no mesmo bloco de código:

```java
@RestController
public class OrderController {

  private final JdbcTemplate jdbc;

  public OrderController(JdbcTemplate jdbc) {
    this.jdbc = jdbc;
  }

  @PostMapping("/orders/{id}/cancel")
  public void cancel(@PathVariable long id) {
    String status = jdbc.queryForObject("SELECT status FROM orders WHERE id = ?", String.class, id);
    if ("SHIPPED".equals(status)) {
      throw new ResponseStatusException(HttpStatus.CONFLICT, "A shipped order can't be cancelled");
    }
    jdbc.update("UPDATE orders SET status = 'CANCELLED' WHERE id = ?", id);
  }
}
```

No exemplo acima, a regra de negócio ("um pedido enviado não pode ser cancelado") está enterrada entre instruções SQL. Isso impede a realização de testes unitários isolados sem um banco de dados e inviabiliza o reúso dessa regra por outros componentes, como rotinas em lote (batch jobs).

### Isolamento das Camadas de Apresentação, Negócio e Dados

A refatoração adequada separa o tratamento das requisições web, a execução da regra no modelo de domínio e o gerenciamento da persistência:

```java
@RestController
public class OrderController {

  private final OrderService orderService;

  public OrderController(OrderService orderService) {
    this.orderService = orderService;
  }

  @PostMapping("/orders/{id}/cancel")
  public void cancel(@PathVariable long id) {
    orderService.cancel(id);
  }
}

public class OrderService {

  private final OrderRepository orders;

  public OrderService(OrderRepository orders) {
    this.orders = orders;
  }

  public void cancel(long id) {
    Order order = orders.findById(id);
    order.cancel();     // a regra de negócio reside na entidade Order
    orders.save(order);
  }
}
```

Com essa estrutura, o controlador limita-se a traduzir requisições HTTP, o repositório encarrega-se do armazenamento de dados, e a regra de negócio é preservada no método `Order.cancel()`, onde pode ser validada por testes unitários simples.

---

## 6. Composição sobre Herança: Preferindo "Tem Um" a "É Um"

A herança estabelece um relacionamento do tipo "é um" e expõe incondicionalmente todos os métodos da classe pai. Já a composição estabelece um relacionamento do tipo "tem um", oferecendo maior controle sobre quais operações são visíveis para os clientes da classe.

### Os Riscos do Acoplamento por Herança

Quando uma estrutura de dados do tipo Pilha estende diretamente a classe `ArrayList`, ela herda todos os métodos da lista:

```java
public class Stack<E> extends ArrayList<E> {
  public void push(E item) { add(item); }
  public E pop() { return remove(size() - 1); }
}
```

Essa abordagem violaria o comportamento esperado de uma pilha (LIFO - Last-In, First-Out), pois qualquer chamador poderia executar `stack.add(0, item)` ou `stack.remove(0)`. Esse equívoco ocorreu historicamente no próprio Java Kit de Desenvolvimento (JDK), onde `java.util.Stack` estendeu `Vector`, levando a documentação oficial a recomendar o uso de `Deque` em seu lugar.

### Encapsulamento com Composição

Ao aplicar composição, a pilha passa a possuir uma lista interna como atributo privado, exposto apenas os métodos específicos de uma pilha:

```java
public class Stack<E> {

  private final List<E> items = new ArrayList<>();

  public void push(E item) { items.add(item); }

  public E pop() {
    if (items.isEmpty()) throw new NoSuchElementException("stack is empty");
    return items.remove(items.size() - 1);
  }

  public boolean isEmpty() { return items.isEmpty(); }
}
```

A vantagem essencial da composição é o controle de encapsulamento: a classe determina exatamente a sua interface pública, pode substituir a implementação interna de `ArrayList` sem afetar os clientes e evita acoplamento a alterações da classe pai. A herança só deve ser empregada quando a subclasse realmente for um tipo válido da classe base em todos os contexts, atendendo ao Princípio de Substituição de Liskov.

---

## 7. Lei de Demeter: Fale Apenas com Seus Amigos Próximos

A Lei de Demeter estabelece que um método deve interagir apenas com seus colaboradores diretos, evitando navegar através de estruturas internas de objetos distantes.

### Violações por Encadeamento Excessivo

Uma chamada que atravessa múltiplos objetos para obter uma informação revela conhecimento excessivo sobre a estrutura interna do sistema:

```java
String city = order.getCustomer().getAddress().getCity();
```

Essa instrução assume que o pedido possui um cliente, o cliente possui um endereço e o endereço possui uma cidade. Se qualquer um desses relacionamentos for alterado (por exemplo, se um cliente passar a ter múltiplos endereços), todas as chamadas semelhantes serão quebradas.

### Refatoração via Delegação

A solução consiste em delegar a responsabilidade para o colaborador imediato:

```java
public class Order {
  private final Customer customer;

  public String shippingCity() {
    return customer.shippingCity();
  }
}

public class Customer {
  private final Address address;

  public String shippingCity() {
    return address.city();
  }
}
```

Dessa forma, a chamada no cliente principal é reduzida a uma consulta simples e direta:

```java
String city = order.shippingCity();
```

### Limites e Exceções da Lei de Demeter

A Lei de Demeter aplica-se a objetos que possuem comportamento. Cadeias de chamadas em estruturas de dados sem comportamento (como registros e DTOs) ou em APIs fluentes (como Streams e Builders do Java, por exemplo `list.stream().filter(...).map(...)`) não constituem violações desse princípio.

---

## 8. Padrões de Projeto como Encarnação Prática dos Princípios

Os padrões de projeto catalogados na engenharia de software nada mais são do que a aplicação prática e combinada desses princípios em soluções reutilizáveis para problemas recorrentes:

*   **Strategy:** Combina composição e o princípio Open-Closed. A adição de um novo método de pagamento é realizada via criação de uma nova classe, sem alterar estruturas condicionais pré-existentes.
*   **Decorator:** Adiciona comportamentos a um objeto dinamicamente através de composição, evitando a expansão excessiva de hierarquias de herança.
*   **Factory e Injeção de Dependência:** Aplicam o princípio de Inversão de Dependência, fazendo com que o código chamador dependa de interfaces e abstrações em vez de instâncias concretas.
*   **Observer:** Mantém o emissor de eventos e seus receptores fracamente acoplados.

O valor dos padrões inclui a criação de um vocabulário compartilhado entre os membros da equipe de desenvolvimento, permitindo expressar conceitos arquiteturais complexos de maneira concisa.

---

## 9. Matriz de Conflitos e Trade-offs Arquiteturais

Os princípios de design não representam leis dogmáticas, mas ferramentas para suporte à tomada de decisão. Em diversos cenários reais, diferentes princípios apontam para direções opostas:

*   **DRY vs. Acoplamento Fraco (Microserviços):** Compartilhar bibliotecas genéricas entre microserviços para evitar duplicação de classes gera acoplamento temporal, exigindo o deploy simultâneo das aplicações. Em fronteiras de serviços, suportar uma pequena duplicação de código é frequentemente mais vantajoso do que introduzir acoplamento rígido.
*   **YAGNI vs. Open-Closed (OCP):** O princípio Open-Closed orienta a criação de pontos de extensão, enquanto o YAGNI recomenda não construir o que não é necessário imediatamente. A regra prática consiste em introduzir o ponto de extensão na segunda vez em que a mesma variação de requisito ocorrer.
*   **KISS vs. Padrões de Projeto:** Aplicar um padrão de projeto a um problema trivial de poucas linhas aumenta a complexidade em vez de reduzi-la. Padrões devem ser aplicados apenas quando eliminam complexidade real.

---

## 10. Matriz de Diagnóstico e Sinais de Alerta (Code Smells)

A tabela a seguir resume os princípios analisados e os principais sintomas identificáveis no código que sinalizam suas violações:

| Princípio | Sinal de Alerta no Código (Code Smell) |
| :--- | :--- |
| **Single Responsibility (SRP)** | Classes genéricas nomeadas como `Manager` ou `Utils` com milhares de linhas. |
| **Open-Closed (OCP)** | Instruções `switch` baseadas em tipos que crescem a cada nova funcionalidade. |
| **DRY** | Correções de bugs que precisam ser aplicadas manualmente em múltiplos arquivos. |
| **KISS** | Revisores de código perguntando frequentemente "o que este trecho faz?". |
| **YAGNI** | Interfaces contendo apenas uma única implementação criada "para uso futuro". |
| **Separação de Conceitos** | Instruções de banco de dados SQL incorporadas diretamente em controladores HTTP. |
| **Composição sobre Herança** | Subclasses que desabilitam ou sobrescrevem métodos da classe pai para lançar exceções. |
| **Lei de Demeter** | Encadeamentos extensos de métodos seletores (`get().get().get()`). |

---

## 11. Conclusão e Próximos Passos

A adoção dos princípios de design de software reduz a complexidade do desenvolvimento, prepara o sistema para mudanças inevitáveis e minimiza o impacto da introdução de falhas. A identificação de violações e a aplicação de refatorações sob restrições de prazo exigem prática constante, equilibrando a simplicidade do código com a necessidade de extensão futura.
