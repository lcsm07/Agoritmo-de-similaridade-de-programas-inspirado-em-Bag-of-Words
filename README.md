# Algoritmo de Similaridade de Programas inspirado em Bag-of-Words

Implementação em Haskell de um algoritmo simples de similaridade entre dois
arquivos de código-fonte. O programa conta as palavras de cada arquivo,
aplica peso dobrado em palavras reservadas e calcula um índice de similaridade
baseado nas frequências ponderadas do primeiro código.

## Arquivos do projeto

- `Main.hs`: código-fonte principal em Haskell.
- `Makefile`: comandos de compilação, execução e limpeza.
- `.gitignore`: ignora executável e arquivos intermediários gerados pelo GHC.
- `res.txt`: palavras reservadas da linguagem usada nos exemplos.
- `sep.txt`: caracteres separadores que devem ser ignorados na tokenização.
- `c1.txt`: primeiro código-fonte de exemplo.
- `c2.txt`: segundo código-fonte de exemplo.
- `materiais_auxiliares/RELATORIO_INTEGRANTES.tex`: relatório de atuação do grupo de 3 alunos em LaTeX.
- `materiais_auxiliares/APRESENTACAO.md`: notas completas para lembrar durante a apresentação.
- `materiais_auxiliares/APRENDIZADO_HASKELL.md`: explicação linha a linha do código e dos conceitos de Haskell usados.

## Requisitos

É necessário ter o compilador GHC instalado.

Em distribuições Linux baseadas em Fedora:

```bash
sudo dnf install ghc make
```

Em distribuições baseadas em Debian/Ubuntu:

```bash
sudo apt install ghc make
```

## Como compilar

```bash
make build
```

Esse comando gera o executável `similaridade`.

## Como executar com os exemplos

```bash
make run
```

O alvo `run` executa:

```bash
./similaridade res.txt sep.txt c1.txt c2.txt
```

## Como executar com outros arquivos

```bash
./similaridade <res.txt> <sep.txt> <codigo1.txt> <codigo2.txt>
```

Exemplo:

```bash
./similaridade res.txt sep.txt c1.txt c2.txt
```

## Formato dos arquivos de entrada

### `res.txt`

Lista de palavras reservadas separadas por espaço, quebra de linha ou tabulação.

Exemplo:

```text
if then else let in do return case of
```

### `sep.txt`

Lista de caracteres separadores a descartar. Eles podem aparecer separados por
espaço para facilitar a leitura.

Exemplo:

```text
= + - * / ( ) { } ; [ ] , .
```

Durante a leitura dos códigos, cada caractere listado em `sep.txt` é substituído
por espaço. Depois disso, o programa quebra o texto em palavras com `words`.
Assim, trechos como `x==y`, `foo(bar)` e `valor;` são separados corretamente.

### `c1.txt` e `c2.txt`

Arquivos de código-fonte que serão comparados.

## Regra implementada

1. O programa lê os quatro arquivos informados por linha de comando.
2. As palavras reservadas são carregadas de `res.txt`.
3. Os separadores são carregados de `sep.txt`.
4. Cada código é tokenizado, removendo os separadores.
5. Cada palavra recebe frequência ponderada:
   - peso `2` se estiver em `res.txt`;
   - peso `1` caso contrário.
6. O relatório imprime as frequências ponderadas de `c1` em ordem decrescente.
7. Em caso de empate na frequência, a ordenação é lexicográfica crescente.
8. Para cada palavra de `c1`, o programa compara `f1` com a frequência da mesma palavra em `c2`.
9. Se `f2` diferir de `f1` em no máximo 10% de `f1`, o valor de `f1` entra no somatório `m`.
10. O índice final é:

```text
similaridade = m / soma(f1)
```

## Saída

A saída mostra:

- relatório de frequências de `c1`;
- valor de `m`;
- soma das frequências ponderadas de `c1`;
- índice de similaridade.

Exemplo de formato:

```text
--- Relatório de Frequências (c1) ---
let: 4
return: 4
x: 3
y: 3
else: 2
if: 2
then: 2
10: 1
20: 1
-------------------------------------
m = 16
Soma(f1) = 22
Índice de Similaridade = 0.7272727272727273
```

## Limpeza dos arquivos gerados

```bash
make clean
```

Esse comando remove o executável e os arquivos intermediários gerados pelo GHC.

## Como gerar o PDF do relatório

Caso tenha uma distribuição LaTeX instalada:

```bash
pdflatex materiais_auxiliares/RELATORIO_INTEGRANTES.tex
```
