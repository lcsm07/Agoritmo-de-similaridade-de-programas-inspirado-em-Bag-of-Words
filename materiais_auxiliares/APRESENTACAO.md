# Notas completas para apresentação

Este arquivo não é um roteiro rígido nem um conjunto de slides. Ele serve como
material de consulta para o grupo lembrar o contexto do trabalho, explicar as
decisões técnicas e responder perguntas prováveis do professor.

## Contexto do trabalho

O objetivo do trabalho é implementar um algoritmo de similaridade de programas
inspirado em Bag-of-Words.

Bag-of-Words é uma técnica que representa um texto pela frequência das palavras,
ignorando a ordem exata e a estrutura gramatical. Neste trabalho, a mesma ideia
foi adaptada para código-fonte: em vez de tentar entender toda a sintaxe ou a
semântica do programa, o algoritmo observa quais palavras aparecem e quantas
vezes aparecem.

O programa deve ler quatro arquivos:

- `res.txt`: palavras reservadas da linguagem;
- `sep.txt`: caracteres separadores que devem ser descartados;
- `c1.txt`: primeiro código-fonte;
- `c2.txt`: segundo código-fonte.

A saída deve conter:

- o relatório das frequências de cada palavra de `c1`;
- as frequências em ordem decrescente;
- desempate por ordem lexicográfica;
- o valor `m`;
- o índice de similaridade `m / soma(f1)`.

## Ideia principal para explicar em voz alta

O programa transforma cada código em uma lista de palavras. Depois conta a
frequência ponderada de cada palavra. Palavras reservadas recebem peso dobrado,
porque o enunciado determina que elas têm mais importância. Por fim, o programa
compara as frequências de `c1` e `c2` e calcula quanto de `c1` também aparece de
forma parecida em `c2`.

Uma forma simples de resumir:

> "Nós comparamos os códigos pela distribuição das palavras. Primeiro limpamos
> separadores, depois contamos frequências com peso especial para palavras
> reservadas, e finalmente calculamos a proporção das frequências de `c1` que
> têm correspondência próxima em `c2`."

## O que cada arquivo faz

### `Main.hs`

É o código principal em Haskell. Ele contém:

- leitura dos argumentos da linha de comando;
- leitura dos quatro arquivos;
- tokenização dos códigos;
- cálculo das frequências ponderadas;
- ordenação do relatório;
- cálculo de `m`;
- cálculo do índice de similaridade;
- impressão da saída.

### `Makefile`

Automatiza a compilação e a execução.

Comandos importantes:

```bash
make build
make run
make clean
```

### `res.txt`

Lista as palavras reservadas usadas nos exemplos.

Exemplo:

```text
if then else let in do return case of
```

Se uma palavra do código estiver nesse arquivo, cada ocorrência dela soma `2`
em vez de `1`.

### `sep.txt`

Lista caracteres separadores que devem ser descartados na tokenização.

Exemplo:

```text
= + - * / ( ) { } ; [ ] , .
```

O programa trata esses símbolos como separadores de palavras.

### `c1.txt` e `c2.txt`

São os dois códigos comparados.

Nos exemplos atuais, eles são parecidos na estrutura, mas usam identificadores
diferentes:

- `c1.txt` usa `x` e `y`;
- `c2.txt` usa `a` e `b`.

Isso ajuda a mostrar que palavras reservadas e números continuam contribuindo
para a similaridade, enquanto identificadores diferentes reduzem a pontuação.

## Fluxo do algoritmo

O fluxo pode ser explicado nesta ordem:

1. O programa recebe quatro caminhos pela linha de comando.
2. Lê o conteúdo de `res.txt`, `sep.txt`, `c1.txt` e `c2.txt`.
3. Transforma as palavras reservadas em um `Set`.
4. Transforma os separadores em um `Set` de caracteres.
5. Tokeniza `c1` e `c2`, trocando separadores por espaço.
6. Conta as frequências ponderadas de cada código.
7. Ordena as frequências de `c1`.
8. Compara as frequências de `c1` com as de `c2`.
9. Calcula `m`.
10. Calcula `m / soma(f1)`.
11. Imprime o relatório.

## Tokenização

Tokenização é o processo de transformar o texto do código em palavras.

O ponto importante é que o programa não separa palavras apenas por espaços. Ele
usa `sep.txt` para saber quais caracteres devem virar espaço.

Exemplos:

```text
x=10
x==y
foo(bar)
valor;
```

Depois da tokenização, esses trechos podem virar:

```text
x 10
x y
foo bar
valor
```

Isso é importante porque, sem esse tratamento, `x==y` poderia ser contado como
uma palavra única. Isso prejudicaria o cálculo de frequência.

## Frequência ponderada

O enunciado diz que palavras reservadas devem ter o dobro de peso.

Por isso:

- palavra comum soma `1`;
- palavra reservada soma `2`.

Exemplo:

```text
let x=10
let y=20
```

Se `let` está em `res.txt`, então:

- `let` aparece 2 vezes;
- cada ocorrência vale 2;
- frequência ponderada de `let` é 4.

Já `x`, `y`, `10` e `20` são palavras comuns nos exemplos, então cada ocorrência
vale 1.

## Valor `m`

Para cada palavra presente em `c1`, o programa procura a frequência da mesma
palavra em `c2`.

Usamos:

- `f1`: frequência ponderada da palavra em `c1`;
- `f2`: frequência ponderada da mesma palavra em `c2`.

Se a diferença entre `f1` e `f2` for de até 10% de `f1`, então `f1` entra na
soma de `m`.

A regra usada no código é:

```text
abs(f1 - f2) * 10 <= f1
```

Essa forma evita usar número decimal e evita problemas de arredondamento.

## Índice de similaridade

O índice final é:

```text
m / soma(f1)
```

Interpretação:

- `soma(f1)` representa o total de frequências ponderadas de `c1`;
- `m` representa a parte desse total que tem frequência parecida em `c2`;
- o resultado mostra a proporção de `c1` que é similar a `c2` pela métrica usada.

Se o índice for:

- próximo de `1`: os códigos têm frequências muito parecidas;
- próximo de `0`: os códigos têm frequências pouco parecidas.

## Por que a métrica não é necessariamente simétrica

O cálculo usa `c1` como base.

O relatório pedido é de `c1`, e o denominador do índice é `soma(f1)`. Por isso,
a comparação é orientada por `c1`.

Em outras palavras:

```text
similaridade(c1, c2)
```

não precisa ser exatamente igual a:

```text
similaridade(c2, c1)
```

Isso não é um erro necessariamente. É consequência da regra do enunciado, que
define o índice usando `soma(f1)`.

## Estruturas de dados usadas

### `Set`

Foi usado para palavras reservadas e separadores.

Motivo:

- consultar se uma palavra está em `res.txt`;
- consultar se um caractere está em `sep.txt`;
- evitar busca manual em lista.

Exemplo conceitual:

```text
if pertence a res?
= pertence a sep?
```

### `Map`

Foi usado para guardar as frequências.

Formato:

```text
palavra -> frequência
```

Exemplo:

```text
let -> 4
return -> 4
x -> 3
```

## Ordenação do relatório

O enunciado pede frequências decrescentes de `c1`.

Então o programa ordena assim:

1. maior frequência primeiro;
2. se empatar, ordem lexicográfica.

Exemplo de empate:

```text
else: 2
if: 2
then: 2
```

Como as três frequências são iguais, entra o critério lexicográfico.

## Exemplo atual do projeto

`c1.txt`:

```text
let x=10
let y=20
if x==y then
    return x
else
    return y
```

`c2.txt`:

```text
let a=10
let b=20
if a==b then
    return a
else
    return b
```

Após tokenização, a estrutura geral dos dois códigos é parecida. As palavras
reservadas são iguais, e os números também. Os identificadores mudam:

- `x` e `y` aparecem só em `c1`;
- `a` e `b` aparecem só em `c2`.

Por isso o índice não será `1`, mas ainda será relativamente alto.

## Demonstração

Compilar:

```bash
make build
```

Executar com os exemplos:

```bash
make run
```

Execução manual equivalente:

```bash
./similaridade res.txt sep.txt c1.txt c2.txt
```

Se o ambiente não tiver GHC instalado, explicar:

> "O projeto depende do compilador GHC. Em uma máquina com GHC instalado, o
> Makefile compila o arquivo `Main.hs` e gera o executável `similaridade`."

## O que o algoritmo faz bem

- Implementa diretamente as regras do enunciado.
- Mantém a solução pequena e explicável.
- Usa arquivos de configuração para palavras reservadas e separadores.
- Mostra as frequências de `c1`, o valor `m` e o índice final.
- Permite trocar os arquivos de entrada sem alterar o código.

## Limitações que devemos assumir

- O algoritmo não entende semântica.
- O algoritmo não constrói árvore sintática.
- O algoritmo não sabe se dois códigos fazem a mesma coisa.
- Comentários e strings não recebem tratamento especial.
- Renomear variáveis pode reduzir a similaridade.
- Dois programas equivalentes podem ter similaridade baixa.
- Dois programas diferentes podem ter similaridade alta se usarem palavras muito parecidas.

Essas limitações são aceitáveis porque o objetivo do trabalho é implementar uma
métrica inspirada em Bag-of-Words, não um detector perfeito de plágio ou
equivalência semântica.

## Perguntas prováveis do professor

### 1. O que é Bag-of-Words?

Bag-of-Words é uma representação que ignora a ordem e a estrutura de um texto,
mantendo apenas as palavras e suas frequências. No trabalho, aplicamos essa
ideia a código-fonte: contamos palavras do programa em vez de analisar a
estrutura sintática completa.

### 2. Por que esse algoritmo é "inspirado" em Bag-of-Words e não exatamente Bag-of-Words clássico?

Porque existe uma adaptação para o contexto de programas. No Bag-of-Words
clássico, normalmente todas as palavras têm o mesmo peso ou pesos estatísticos
como TF-IDF. Aqui, o enunciado define um peso especial: palavras reservadas
valem o dobro.

### 3. Por que palavras reservadas recebem peso 2?

Porque o enunciado exige isso. A justificativa conceitual é que palavras
reservadas representam estruturas importantes da linguagem, como condicionais,
retornos e blocos. Por isso elas têm mais influência na métrica.

### 4. O que acontece com palavras que não estão em `res.txt`?

Elas continuam sendo contadas, mas com peso 1. Isso inclui identificadores,
números e outros tokens que não foram removidos pelos separadores.

### 5. O que exatamente é descartado pelo `sep.txt`?

Os caracteres presentes em `sep.txt` são tratados como separadores. O programa
substitui cada ocorrência deles por espaço. Eles não entram como palavras no
relatório final.

### 6. Por que tratar `sep.txt` como caracteres, e não como palavras?

Porque separadores normalmente aparecem grudados em tokens de código. Exemplos:
`x=10`, `x==y`, `foo(bar)` e `valor;`. Se o programa removesse apenas
separadores isolados por espaço, esses casos seriam tokenizados incorretamente.

### 7. O algoritmo conta operadores como palavras?

Não, se esses operadores estiverem em `sep.txt`. No exemplo, símbolos como `=`,
`+`, `-`, `*`, `/`, `(`, `)` e `;` são descartados durante a tokenização.

### 8. Como o programa calcula a frequência de uma palavra reservada?

Cada ocorrência de palavra reservada soma 2. Então, se `return` aparece duas
vezes, a frequência ponderada é 4.

### 9. Como o programa calcula a frequência de uma palavra comum?

Cada ocorrência de palavra comum soma 1. Então, se `x` aparece três vezes, a
frequência ponderada é 3.

### 10. O que é `m`?

`m` é a soma das frequências de `c1` que têm frequência parecida em `c2`. Para
cada palavra de `c1`, se a diferença entre `f1` e `f2` for de até 10% de `f1`,
somamos `f1` em `m`.

### 11. Por que o índice final é `m / soma(f1)`?

Porque `soma(f1)` é o total de frequências ponderadas do primeiro código, e `m`
é a parte desse total que teve correspondência parecida no segundo código. A
divisão transforma isso em uma proporção.

### 12. O resultado fica sempre entre 0 e 1?

Sim, quando `soma(f1)` é maior que zero. Como `m` soma apenas valores que vêm de
`f1`, ele não ultrapassa `soma(f1)`. Portanto, `m / soma(f1)` fica entre 0 e 1.

### 13. O que acontece se `c1` estiver vazio?

Se `c1` não tiver palavras, `soma(f1)` será zero. Para evitar divisão por zero,
o programa retorna similaridade `0.0`.

### 14. A comparação é simétrica?

Não necessariamente. O cálculo usa `c1` como base, porque o denominador é
`soma(f1)`. Se invertermos os arquivos, o resultado pode mudar.

### 15. Isso é um problema?

Não necessariamente, porque o enunciado define a fórmula usando `f1`. O programa
segue essa regra. Se quiséssemos uma métrica simétrica, precisaríamos definir
outra fórmula.

### 16. Por que a regra dos 10% foi implementada como `abs(f1 - f2) * 10 <= f1`?

Essa forma é equivalente a verificar se a diferença é menor ou igual a 10% de
`f1`, mas sem usar números decimais. Isso evita problemas de arredondamento.

### 17. Por que usar `Map`?

Porque precisamos associar cada palavra à sua frequência. Um `Map` representa
naturalmente uma tabela do tipo `palavra -> frequência`.

### 18. Por que usar `Set`?

Porque precisamos consultar pertencimento: se uma palavra está no conjunto de
reservadas ou se um caractere está no conjunto de separadores. `Set` deixa essa
consulta clara e evita percorrer listas manualmente.

### 19. O programa diferencia maiúsculas de minúsculas?

Sim. Do jeito que está, `If`, `if` e `IF` seriam palavras diferentes. Isso é
coerente com linguagens case-sensitive, como Haskell, C e Java. Se quiséssemos
ignorar caixa, precisaríamos normalizar tudo para minúsculas.

### 20. O programa remove comentários?

Não. Comentários serão tokenizados como texto comum, exceto pelos separadores.
Isso é uma limitação conhecida. O enunciado não exigiu tratamento específico
para comentários.

### 21. O programa trata strings de forma especial?

Não. Conteúdo de strings também pode ser contado como palavras. Isso foi mantido
simples para respeitar o escopo do trabalho.

### 22. O algoritmo detecta plágio?

Ele pode ajudar a indicar similaridade lexical, mas não é um detector completo
de plágio. Programas semanticamente iguais podem parecer diferentes se usarem
nomes de variáveis diferentes, e programas diferentes podem parecer parecidos se
usarem vocabulário semelhante.

### 23. Por que escolher Haskell para essa implementação?

Porque era a linguagem definida para o trabalho. Além disso, Haskell combina bem
com esse problema, pois o processamento é composto por transformações de dados:
texto para tokens, tokens para frequências, frequências para métrica.

### 24. O que é uma função pura no projeto?

Funções como `tokenize`, `wordWeight`, `getFrequencies`, `matchingScore` e
`similarityIndex` são puras. Elas recebem valores e devolvem valores, sem ler
arquivos nem imprimir na tela.

### 25. Onde está a parte de entrada e saída?

Está na função `main`. Ela lê argumentos, lê arquivos e imprime o relatório. O
restante do algoritmo fica separado em funções puras.

### 26. Por que separar funções puras da `main`?

Porque isso deixa o código mais fácil de entender, testar e explicar. A `main`
cuida do mundo externo, enquanto as funções puras cuidam do algoritmo.

### 27. O que `words` faz?

`words` quebra uma string em lista de palavras, usando espaços, quebras de linha
e tabulações como divisores. No projeto, antes de chamar `words`, o programa
troca os separadores por espaços.

### 28. O que `M.fromListWith (+)` faz?

Ele cria um `Map` a partir de uma lista de pares. Quando a mesma palavra aparece
mais de uma vez, os valores são somados com `(+)`. É isso que permite acumular
frequências.

### 29. O que `M.findWithDefault 0` faz?

Procura uma palavra no mapa de frequências. Se a palavra não existir em `c2`,
retorna 0. Isso permite comparar toda palavra de `c1` mesmo quando ela não
aparece no segundo código.

### 30. Como funciona o desempate lexicográfico?

Quando duas palavras têm a mesma frequência, elas são comparadas como texto. A
que vier primeiro na ordem lexicográfica aparece antes no relatório.

### 31. Por que a saída só mostra as frequências de `c1`?

Porque o enunciado pede um relatório com as frequências decrescentes de cada
palavra de `c1`. As frequências de `c2` são usadas internamente para calcular a
similaridade.

### 32. O programa aceita outros arquivos além dos exemplos?

Sim. Basta passar os quatro caminhos na linha de comando:

```bash
./similaridade outro_res.txt outro_sep.txt codigo1.txt codigo2.txt
```

### 33. O programa depende dos nomes `res.txt`, `sep.txt`, `c1.txt` e `c2.txt`?

Não no código principal. Esses nomes são usados pelo `make run` como exemplo,
mas a execução manual aceita qualquer caminho.

### 34. O que acontece se uma palavra aparece em `c2`, mas não em `c1`?

Ela não entra diretamente no cálculo de `m`, porque o algoritmo percorre as
palavras de `c1`. Isso segue a fórmula baseada em `f1`.

### 35. O que aconteceria se uma palavra aparece em `c1`, mas não em `c2`?

O programa considera `f2 = 0` para essa palavra. Normalmente ela não passará na
regra dos 10%, então não contribuirá para `m`.

### 36. Por que não foi feita uma análise sintática da linguagem?

Porque o objetivo do trabalho é uma abordagem inspirada em Bag-of-Words. Análise
sintática exigiria parser, regras específicas da linguagem e uma complexidade
muito maior do que a proposta.

### 37. O projeto está completo em relação ao enunciado?

Sim, em termos de implementação e entregáveis principais:

- código-fonte em Haskell;
- Makefile;
- arquivos de exemplo;
- relatório de integrantes;
- notas para apresentação;
- documentação de execução.

### 38. Qual é a principal decisão técnica do projeto?

A principal decisão foi separar o código por caracteres de `sep.txt` antes de
chamar `words`. Isso torna a contagem correta para código-fonte realista, onde
operadores e pontuação aparecem grudados nos identificadores.

### 39. Qual é a principal limitação técnica do projeto?

A principal limitação é que ele mede similaridade lexical, não semântica. Ele
não sabe se dois programas fazem a mesma coisa; ele só compara frequências de
palavras.

### 40. Como explicar o projeto em menos de um minuto?

> "Nosso programa lê quatro arquivos: reservadas, separadores e dois códigos.
> Ele remove os separadores, quebra os códigos em palavras, conta frequências
> ponderadas com peso 2 para reservadas e peso 1 para as demais, imprime as
> frequências de `c1` ordenadas e calcula uma similaridade. Para cada palavra de
> `c1`, se a frequência em `c2` estiver a até 10% da frequência em `c1`, essa
> frequência entra em `m`. O índice final é `m / soma(f1)`."

## Resumo final para decorar

- O projeto compara códigos por frequência de palavras.
- `res.txt` define palavras com peso 2.
- `sep.txt` define caracteres descartados.
- `Map` guarda frequências.
- `Set` guarda reservadas e separadores.
- `m` soma frequências de `c1` que aparecem de forma parecida em `c2`.
- O índice é `m / soma(f1)`.
- A solução é simples, funcional e alinhada ao Bag-of-Words.

