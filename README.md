# Algoritmo de Similaridade de Programas inspirado em Bag-of-Words

Implementação em Haskell de um algoritmo simples de similaridade entre dois arquivos de código-fonte.

## Compilação e Execução

Para compilar o código (é necessário possuir o compilador GHC e a ferramenta `make`):
```bash
make build
```

Para rodar com os exemplos fornecidos no repositório:
```bash
make run
```

Para rodar com outros arquivos, utilize a estrutura abaixo:
```bash
./similaridade <arquivo_palavras_reservadas> <arquivo_separadores> <codigo_1> <codigo_2>
```

## Arquivos de Entrada Esperados

O programa aguarda as seguintes entradas (passadas via linha de comando):
- **Palavras reservadas** (ex: `res.txt`): Lista de palavras-chave da linguagem (possuem peso dobrado no cálculo de similaridade).
- **Separadores** (ex: `sep.txt`): Caracteres que devem ser ignorados, como  `=`, `+`, `{`, `;`, etc.
- **Códigos Reais** (ex: `c1.txt` e `c2.txt`): Os dois arquivos com o código-fonte a serem comparados.

## Saída Esperada

Ao longo da execução, o terminal imprimirá um cabeçalho com o relatório de frequências de ocorrência no primeiro arquivo (ordenado em ordem decrescente) e os cálculos finais do índice de similaridade.

**Exemplo:**
```text
--- Relatório de Frequências (c1) ---
let: 4
x: 3
y: 3
do: 2
else: 2
if: 2
return: 2
...
-------------------------------------
m = 17
Soma(f1) = 23
Índice de Similaridade = 0.7391304347826086
```
