# Notas para apresentação

Este arquivo não é um roteiro rígido. A ideia é servir como lista de lembretes
para o grupo consultar antes da apresentação.

## Ideia central

- O trabalho compara dois arquivos de código usando uma ideia parecida com Bag-of-Words.
- Em vez de analisar a árvore sintática ou o significado do programa, contamos palavras.
- O resultado é uma métrica simples de similaridade entre `0` e `1`.
- Quanto mais próximo de `1`, mais parecidas são as frequências ponderadas dos códigos.

## Entradas que precisamos lembrar

- `res.txt`: palavras reservadas da linguagem.
- `sep.txt`: caracteres que devem separar palavras e ser descartados.
- `c1.txt`: primeiro código.
- `c2.txt`: segundo código.

## Ponto importante da tokenização

- O programa não usa apenas espaços para separar palavras.
- Ele lê os caracteres de `sep.txt` e troca cada um deles por espaço.
- Isso faz diferença em exemplos como `x=10`, `x==y`, `foo(bar)` e `valor;`.
- Depois dessa troca, a função `words` quebra o texto em palavras.

## Frequência ponderada

- Palavra comum soma `1`.
- Palavra reservada soma `2`.
- Exemplo: se `let` aparece duas vezes e está em `res.txt`, a frequência ponderada de `let` é `4`.
- A estrutura usada para guardar isso é um `Map`, no formato `palavra -> frequência`.

## Similaridade

- Para cada palavra de `c1`, olhamos a frequência dela em `c1` e em `c2`.
- Chamamos a frequência em `c1` de `f1`.
- Chamamos a frequência em `c2` de `f2`.
- Se a diferença entre `f1` e `f2` for de até 10% de `f1`, somamos `f1` em `m`.
- O índice final é `m / soma(f1)`.

## Saída

- Primeiro aparece o relatório das frequências de `c1`.
- A ordenação é por frequência decrescente.
- Se houver empate, a palavra menor lexicograficamente aparece primeiro.
- Depois aparecem `m`, `Soma(f1)` e o índice de similaridade.

## Comandos para demonstração

```bash
make build
make run
```

Execução manual equivalente:

```bash
./similaridade res.txt sep.txt c1.txt c2.txt
```

## O que cada pessoa deve conseguir explicar

- Por que o algoritmo é inspirado em Bag-of-Words.
- Por que `sep.txt` é tratado como conjunto de caracteres.
- Por que palavras reservadas têm peso dobrado.
- Como `m` é calculado.
- Por que o índice final usa `m / soma(f1)`.
- O que o programa não faz: ele não entende semântica do código nem detecta plágio perfeitamente.

## Possíveis perguntas

### O algoritmo é simétrico?

Não necessariamente. A base do cálculo é `c1`, porque o índice final usa
`soma(f1)` e o relatório pedido também é das frequências de `c1`.

### Por que usar `Map`?

Porque precisamos associar cada palavra a um número de frequência.

### Por que usar `Set`?

Porque precisamos consultar rapidamente se uma palavra é reservada e se um
caractere é separador.

### O que acontece se `c1` estiver vazio?

O programa retorna similaridade `0.0`, evitando divisão por zero.

### Qual é a principal limitação?

Dois códigos podem fazer a mesma coisa e ainda assim ter baixa similaridade se
usarem palavras muito diferentes. O algoritmo compara frequência lexical, não
significado.

