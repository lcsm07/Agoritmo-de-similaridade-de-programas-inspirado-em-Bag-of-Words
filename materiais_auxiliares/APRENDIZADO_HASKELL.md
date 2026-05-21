# Aprendizado de Haskell pelo projeto

Este documento explica o código do projeto para pessoas que já conhecem programação, mas nunca trabalharam com Haskell.

O foco é entender:

- como Haskell organiza funções;
- como tipos aparecem no código;
- como listas, mapas e conjuntos são usados;
- como entrada e saída funcionam;
- como cada linha de `Main.hs` contribui para o algoritmo.

## 1. Ideia geral da linguagem

Haskell é uma linguagem funcional. Isso muda a forma de pensar em relação a linguagens imperativas como C, Java, Python ou JavaScript.

Em Haskell, o programa é organizado principalmente como composição de funções. Em vez de escrever muitos comandos que mudam variáveis ao longo do tempo, normalmente escrevemos funções que recebem valores e produzem novos valores.

### Funções puras

Uma função pura:

- recebe entradas;
- devolve uma saída;
- não altera estado global;
- não lê arquivos;
- não imprime na tela;
- não depende de algo escondido fora dela.

Exemplo deste projeto:

```haskell
wordWeight :: S.Set String -> String -> Int
wordWeight reserved word =
    if word `S.member` reserved then 2 else 1
```

Essa função sempre devolve o mesmo resultado para os mesmos argumentos.

### Entrada e saída com `IO`

Ler arquivos, receber argumentos e imprimir texto são efeitos externos. Em Haskell, esses efeitos aparecem no tipo da função.

Por isso a função principal tem o tipo:

```haskell
main :: IO ()
```

Isso significa: `main` é uma ação de entrada e saída que, ao terminar, não devolve um valor útil.

### Imutabilidade

Valores em Haskell são imutáveis por padrão. Quando escrevemos:

```haskell
let x = 10
```

`x` não é uma variável que será alterada depois. É um nome associado ao valor `10`.

### Tipos fortes

Haskell tem tipagem estática forte. Muitos erros são encontrados na compilação. Mesmo quando uma assinatura de tipo não é escrita, o compilador tenta inferir o tipo.

Neste projeto, as principais funções têm assinaturas explícitas para facilitar leitura e apresentação.

## 2. Conceitos usados no projeto

### `String`

Em Haskell, `String` é uma lista de caracteres.

```haskell
String
```

é equivalente a:

```haskell
[Char]
```

### Lista

Uma lista de palavras tem tipo:

```haskell
[String]
```

Ou seja: lista de `String`.

### Tupla

Uma tupla junta valores em uma estrutura pequena.

Exemplo:

```haskell
("if", 2)
```

Tipo:

```haskell
(String, Int)
```

No projeto, cada par representa:

```text
(palavra, frequência)
```

### `Map`

`Map` é uma estrutura de chave e valor.

Neste projeto:

```haskell
M.Map String Int
```

significa:

```text
palavra -> frequência
```

### `Set`

`Set` é um conjunto. Ele guarda valores sem repetição e permite consultar se um valor pertence ao conjunto.

Usamos:

```haskell
S.Set String
```

para palavras reservadas, e:

```haskell
S.Set Char
```

para separadores.

### `qualified import`

O projeto importa `Map` e `Set` assim:

```haskell
import qualified Data.Map as M
import qualified Data.Set as S
```

Isso significa que funções de `Map` serão chamadas com prefixo `M.` e funções de `Set` com prefixo `S.`.

Exemplos:

```haskell
M.toList
S.fromList
```

Essa prática evita conflito de nomes e deixa claro de qual módulo cada função veio.

### Assinatura de tipo

Uma assinatura de tipo tem este formato:

```haskell
nomeDaFuncao :: TipoEntrada -> TipoSaida
```

Quando há mais de uma entrada:

```haskell
nomeDaFuncao :: Tipo1 -> Tipo2 -> TipoResultado
```

Exemplo:

```haskell
wordWeight :: S.Set String -> String -> Int
```

Lê-se assim:

```text
wordWeight recebe um conjunto de strings, recebe uma string e devolve um inteiro.
```

### Aplicação de função

Em Haskell, chamada de função não usa parênteses como em muitas linguagens.

Em vez de:

```text
wordWeight(reserved, word)
```

usa-se:

```haskell
wordWeight reserved word
```

### Operador `$`

O operador `$` evita alguns parênteses. Ele aplica a função à direita.

Exemplo:

```haskell
putStrLn $ "m = " ++ show m
```

é equivalente a:

```haskell
putStrLn ("m = " ++ show m)
```

### Operador `++`

`++` concatena listas. Como `String` é lista de caracteres, `++` concatena strings.

Exemplo:

```haskell
"m = " ++ show m
```

### `show`

`show` converte valores para texto quando eles pertencem à classe `Show`.

Exemplo:

```haskell
show 10
```

resultado:

```text
"10"
```

### `do`

`do` é usado para sequenciar ações de `IO`, como:

- ler argumentos;
- ler arquivos;
- imprimir na tela.

Ele deixa o código de entrada e saída parecido com um fluxo sequencial.

## 3. Código completo explicado linha por linha

As explicações abaixo se referem ao arquivo `Main.hs`.

### Linhas 1 a 4: importações

**Linha 1**

```haskell
import System.Environment (getArgs)
```

Importa a função `getArgs`, que lê os argumentos passados pela linha de comando.

Se o usuário executar:

```bash
./similaridade res.txt sep.txt c1.txt c2.txt
```

`getArgs` devolve:

```haskell
["res.txt", "sep.txt", "c1.txt", "c2.txt"]
```

**Linha 2**

```haskell
import Data.List (sortBy)
```

Importa `sortBy`, função usada para ordenar listas com uma regra customizada.

Neste projeto, usamos `sortBy` para ordenar as frequências:

- maior frequência primeiro;
- empate por ordem lexicográfica.

**Linha 3**

```haskell
import qualified Data.Map as M
```

Importa o módulo `Data.Map` com o apelido `M`.

Assim, usamos:

```haskell
M.Map
M.toList
M.fromListWith
M.findWithDefault
```

**Linha 4**

```haskell
import qualified Data.Set as S
```

Importa o módulo `Data.Set` com o apelido `S`.

Assim, usamos:

```haskell
S.Set
S.fromList
S.member
```

**Linha 5**

Linha em branco para separar visualmente as importações do restante do código.

### Linha 6: apelido de tipo

**Linha 6**

```haskell
type Frequencies = M.Map String Int
```

Cria um apelido de tipo.

Em vez de repetir:

```haskell
M.Map String Int
```

o código pode escrever:

```haskell
Frequencies
```

Isso melhora a legibilidade. O significado é:

```text
Frequencies = mapa de palavra para frequência inteira
```

**Linha 7**

Linha em branco para separar o tipo das funções.

### Linhas 8 a 11: tokenização

**Linha 8**

```haskell
-- | Transforma cada separador em espaço e depois quebra o texto em palavras.
```

Comentário de documentação. Em Haskell, comentários de uma linha começam com `--`.

O símbolo `|` depois de `--` é usado por ferramentas de documentação, mas aqui também ajuda a indicar que o comentário descreve a função abaixo.

**Linha 9**

```haskell
tokenize :: S.Set Char -> String -> [String]
```

Assinatura de tipo da função `tokenize`.

Ela recebe:

- um conjunto de caracteres separadores: `S.Set Char`;
- o texto do código-fonte: `String`;
- e devolve uma lista de palavras: `[String]`.

**Linha 10**

```haskell
tokenize separators source =
```

Define a função `tokenize`.

Os parâmetros são:

- `separators`: conjunto de caracteres que devem ser descartados;
- `source`: conteúdo do arquivo de código.

O sinal `=` introduz o corpo da função.

**Linha 11**

```haskell
    words [if char `S.member` separators then ' ' else char | char <- source]
```

Essa é uma das linhas mais importantes.

Ela faz duas coisas:

1. percorre cada caractere de `source`;
2. troca separadores por espaço;
3. aplica `words` para quebrar o resultado em palavras.

A parte:

```haskell
[if char `S.member` separators then ' ' else char | char <- source]
```

é uma compreensão de lista. Para cada `char` em `source`, ela produz:

- espaço `' '` se `char` estiver no conjunto `separators`;
- o próprio `char` caso contrário.

O trecho:

```haskell
char `S.member` separators
```

usa a função `S.member` em formato infixo. É equivalente a:

```haskell
S.member char separators
```

Por fim, `words` quebra a string resultante em palavras, separando por espaços, quebras de linha e tabulações.

**Linha 12**

Linha em branco para separar funções.

### Linhas 13 a 16: peso das palavras

**Linha 13**

```haskell
-- | Retorna 2 para palavras reservadas e 1 para as demais.
```

Comentário explicando a função `wordWeight`.

**Linha 14**

```haskell
wordWeight :: S.Set String -> String -> Int
```

Assinatura de tipo.

A função recebe:

- conjunto de palavras reservadas;
- uma palavra;
- devolve o peso inteiro da palavra.

**Linha 15**

```haskell
wordWeight reserved word =
```

Define a função `wordWeight`.

Parâmetros:

- `reserved`: conjunto de palavras reservadas;
- `word`: palavra que será avaliada.

**Linha 16**

```haskell
    if word `S.member` reserved then 2 else 1
```

Expressão condicional.

Em Haskell, `if` sempre precisa ter `then` e `else`, porque ele é uma expressão que produz um valor.

Se `word` está no conjunto `reserved`, retorna `2`. Caso contrário, retorna `1`.

**Linha 17**

Linha em branco.

### Linhas 18 a 21: cálculo das frequências

**Linha 18**

```haskell
-- | Computa as frequências ponderadas das palavras.
```

Comentário explicando a função `getFrequencies`.

**Linha 19**

```haskell
getFrequencies :: S.Set String -> [String] -> Frequencies
```

Assinatura de tipo.

A função recebe:

- conjunto de palavras reservadas;
- lista de tokens;
- retorna um mapa de frequências.

**Linha 20**

```haskell
getFrequencies reserved tokens =
```

Define a função `getFrequencies`.

**Linha 21**

```haskell
    M.fromListWith (+) [(word, wordWeight reserved word) | word <- tokens]
```

Cria o mapa de frequências.

A compreensão de lista:

```haskell
[(word, wordWeight reserved word) | word <- tokens]
```

transforma cada palavra em um par:

```text
(palavra, peso)
```

Por exemplo:

```haskell
["let", "x", "let"]
```

pode virar:

```haskell
[("let", 2), ("x", 1), ("let", 2)]
```

`M.fromListWith (+)` cria um `Map` e, quando encontra chaves repetidas, soma os valores.

Resultado:

```haskell
fromList [("let", 4), ("x", 1)]
```

**Linha 22**

Linha em branco.

### Linhas 23 a 28: regra de ordenação

**Linha 23**

```haskell
-- | Ordena por frequência decrescente e usa ordem lexicográfica como desempate.
```

Comentário da função de comparação.

**Linha 24**

```haskell
frequencyOrder :: (String, Int) -> (String, Int) -> Ordering
```

Assinatura de tipo.

A função compara dois pares:

```text
(palavra, frequência)
```

e devolve um `Ordering`.

`Ordering` pode ser:

- `LT`: menor que;
- `EQ`: igual;
- `GT`: maior que.

**Linha 25**

```haskell
frequencyOrder (word1, freq1) (word2, freq2) =
```

Define a função e já desempacota as tuplas.

Isso é pattern matching. Em vez de receber `pair1` e depois extrair seus campos, o código já recebe:

```haskell
(word1, freq1)
```

e:

```haskell
(word2, freq2)
```

**Linha 26**

```haskell
    case compare freq2 freq1 of
```

Compara `freq2` com `freq1`.

A ordem parece invertida de propósito. Para ordenar de forma decrescente, queremos que frequências maiores venham antes.

`case ... of` é parecido com `switch`, mas com pattern matching.

**Linha 27**

```haskell
        EQ -> compare word1 word2
```

Se as frequências forem iguais, compara as palavras em ordem lexicográfica crescente.

Isso implementa o desempate pedido no enunciado.

**Linha 28**

```haskell
        other -> other
```

Se a comparação das frequências não deu empate, devolve o próprio resultado.

`other` é apenas um nome escolhido para capturar qualquer outro valor de `Ordering`.

**Linha 29**

Linha em branco.

### Linhas 30 a 33: regra dos 10%

**Linha 30**

```haskell
-- | Verifica se f2 difere de f1 em no máximo 10% de f1.
```

Comentário explicando a função.

**Linha 31**

```haskell
isWithinTenPercent :: Int -> Int -> Bool
```

Assinatura de tipo.

A função recebe dois inteiros:

- `freq1`;
- `freq2`;

e devolve um booleano.

**Linha 32**

```haskell
isWithinTenPercent freq1 freq2 =
```

Define a função.

**Linha 33**

```haskell
    abs (freq1 - freq2) * 10 <= freq1
```

Implementa:

```text
diferença <= 10% de f1
```

Em matemática:

```text
abs(f1 - f2) <= 0.1 * f1
```

Para evitar número decimal, multiplicamos por `10`:

```text
abs(f1 - f2) * 10 <= f1
```

**Linha 34**

Linha em branco.

### Linhas 35 a 39: cálculo de `m`

**Linha 35**

```haskell
matchingScore :: Frequencies -> Frequencies -> Int
```

Assinatura de tipo.

A função recebe:

- frequências de `c1`;
- frequências de `c2`;
- retorna o valor inteiro `m`.

**Linha 36**

```haskell
matchingScore freq1 freq2 =
```

Define a função `matchingScore`.

**Linha 37**

```haskell
    sum [value1 | (word, value1) <- M.toList freq1,
```

Começa uma compreensão de lista.

`M.toList freq1` transforma o mapa de frequências de `c1` em lista de pares:

```haskell
[("let", 4), ("x", 3), ...]
```

Para cada par, o código pega:

- `word`: palavra;
- `value1`: frequência ponderada em `c1`.

No final, `sum` soma todos os `value1` que passarem na regra.

**Linha 38**

```haskell
                  let value2 = M.findWithDefault 0 word freq2,
```

Define `value2` dentro da compreensão de lista.

`M.findWithDefault 0 word freq2` procura `word` no mapa de `c2`.

Se a palavra existir, retorna sua frequência. Se não existir, retorna `0`.

**Linha 39**

```haskell
                  isWithinTenPercent value1 value2]
```

Filtra a compreensão de lista.

Somente palavras cuja frequência em `c2` esteja a até 10% da frequência em `c1` entram no resultado.

Esses valores somados formam `m`.

**Linha 40**

Linha em branco.

### Linhas 41 a 43: soma das frequências de `c1`

**Linha 41**

```haskell
totalFrequency :: Frequencies -> Int
```

Assinatura de tipo.

Recebe um mapa de frequências e devolve a soma das frequências.

**Linha 42**

```haskell
totalFrequency frequencies =
```

Define a função.

**Linha 43**

```haskell
    sum (map snd (M.toList frequencies))
```

Calcula a soma dos valores do mapa.

Passos:

1. `M.toList frequencies` transforma o mapa em lista de pares.
2. `map snd` pega o segundo elemento de cada par.
3. `sum` soma esses valores.

`snd` significa "second", ou seja, segundo elemento da tupla.

**Linha 44**

Linha em branco.

### Linhas 45 a 49: índice de similaridade

**Linha 45**

```haskell
similarityIndex :: Frequencies -> Frequencies -> Double
```

Assinatura de tipo.

A função recebe dois mapas de frequência e devolve um `Double`, porque o resultado pode ser decimal.

**Linha 46**

```haskell
similarityIndex freq1 freq2 =
```

Define a função.

**Linha 47**

```haskell
    let matchingTotal = matchingScore freq1 freq2
```

Começa um bloco `let`.

Aqui criamos o nome `matchingTotal`, que guarda o valor de `m`.

**Linha 48**

```haskell
        total1 = totalFrequency freq1
```

Ainda dentro do `let`, criamos `total1`, que representa `soma(f1)`.

**Linha 49**

```haskell
    in if total1 == 0 then 0.0 else fromIntegral matchingTotal / fromIntegral total1
```

Fecha o bloco `let` com `in` e calcula o resultado.

Se `total1` for zero, retorna `0.0` para evitar divisão por zero.

Caso contrário, calcula:

```text
m / soma(f1)
```

`fromIntegral` converte `Int` para um tipo numérico compatível com divisão real. Sem isso, Haskell tentaria dividir inteiros, o que não é o comportamento desejado aqui.

**Linha 50**

Linha em branco.

### Linhas 51 a 56: início do programa principal

**Linha 51**

```haskell
main :: IO ()
```

Assinatura da função principal.

`IO ()` indica uma ação de entrada e saída que não retorna um valor útil ao final.

**Linha 52**

```haskell
main = do
```

Define `main` usando notação `do`.

O bloco `do` permite escrever várias ações de `IO` em sequência.

**Linha 53**

```haskell
    args <- getArgs
```

Executa `getArgs` e guarda o resultado em `args`.

O operador `<-` só aparece dentro de `do` para extrair o resultado de uma ação de `IO`.

Aqui, `args` será uma lista de strings.

**Linha 54**

```haskell
    if length args /= 4
```

Verifica se o número de argumentos é diferente de `4`.

`/=` significa "diferente", equivalente a `!=` em outras linguagens.

**Linha 55**

```haskell
        then putStrLn "Uso: ./similaridade <res.txt> <sep.txt> <c1.txt> <c2.txt>"
```

Se o usuário não passou quatro argumentos, imprime uma mensagem de uso.

`putStrLn` imprime uma string seguida de quebra de linha.

**Linha 56**

```haskell
        else do
```

Se foram passados exatamente quatro argumentos, executa outro bloco `do`.

Esse bloco contém a leitura dos arquivos, o processamento e a impressão do resultado.

### Linhas 57 a 61: leitura dos arquivos

**Linha 57**

```haskell
            let [resFile, sepFile, c1File, c2File] = args
```

Usa pattern matching para extrair os quatro argumentos.

Como a linha 54 já garantiu que existem quatro argumentos, essa atribuição é segura.

Resultado:

- `resFile`: caminho do arquivo de palavras reservadas;
- `sepFile`: caminho do arquivo de separadores;
- `c1File`: caminho do primeiro código;
- `c2File`: caminho do segundo código.

**Linha 58**

```haskell
            resContent <- readFile resFile
```

Lê o arquivo de palavras reservadas.

`readFile` é uma ação de `IO`, por isso usa `<-`.

**Linha 59**

```haskell
            sepContent <- readFile sepFile
```

Lê o arquivo de separadores.

**Linha 60**

```haskell
            c1Content <- readFile c1File
```

Lê o primeiro arquivo de código.

**Linha 61**

```haskell
            c2Content <- readFile c2File
```

Lê o segundo arquivo de código.

**Linha 62**

Linha em branco.

### Linhas 63 a 75: processamento dos dados

**Linha 63**

```haskell
            let reserved = S.fromList (words resContent)
```

Começa um bloco `let` com vários nomes intermediários.

`words resContent` quebra o conteúdo de `res.txt` em palavras.

`S.fromList` transforma essa lista em conjunto.

Resultado: `reserved` é um conjunto de palavras reservadas.

**Linha 64**

```haskell
                separators = S.fromList (concat (words sepContent))
```

Cria o conjunto de separadores.

Passos:

1. `words sepContent` quebra `sep.txt` em tokens.
2. `concat` junta esses tokens em uma única string.
3. `S.fromList` transforma a string em conjunto de caracteres.

Exemplo:

```text
= + - ( )
```

vira o conjunto de caracteres:

```haskell
fromList ['=', '+', '-', '(', ')']
```

**Linha 65**

```haskell
                c1 = tokenize separators c1Content
```

Tokeniza o primeiro código.

Resultado: lista de palavras de `c1`.

**Linha 66**

```haskell
                c2 = tokenize separators c2Content
```

Tokeniza o segundo código.

Resultado: lista de palavras de `c2`.

**Linha 67**

Linha em branco dentro do bloco `let`, usada apenas para legibilidade.

**Linha 68**

```haskell
                freq1 = getFrequencies reserved c1
```

Calcula as frequências ponderadas do primeiro código.

**Linha 69**

```haskell
                freq2 = getFrequencies reserved c2
```

Calcula as frequências ponderadas do segundo código.

**Linha 70**

Linha em branco para separar etapas.

**Linha 71**

```haskell
                list1 = M.toList freq1
```

Transforma o mapa de frequências de `c1` em lista de pares.

Isso é necessário porque a saída precisa ser ordenada, e `sortBy` ordena listas.

**Linha 72**

```haskell
                sorted1 = sortBy frequencyOrder list1
```

Ordena as frequências de `c1` usando a regra definida em `frequencyOrder`.

**Linha 73**

```haskell
                m = matchingScore freq1 freq2
```

Calcula o valor `m`, que soma as frequências de `c1` que têm correspondência parecida em `c2`.

**Linha 74**

```haskell
                sumF1 = totalFrequency freq1
```

Calcula `soma(f1)`, a soma de todas as frequências ponderadas de `c1`.

**Linha 75**

```haskell
                sim = similarityIndex freq1 freq2
```

Calcula o índice final de similaridade.

**Linha 76**

Linha em branco.

### Linhas 77 a 82: impressão da saída

**Linha 77**

```haskell
            putStrLn "--- Relatório de Frequências (c1) ---"
```

Imprime o cabeçalho do relatório de frequências.

**Linha 78**

```haskell
            mapM_ (\(w, f) -> putStrLn $ w ++ ": " ++ show f) sorted1
```

Percorre a lista ordenada `sorted1` e imprime cada par.

Essa linha reúne vários conceitos:

- `mapM_`: aplica uma ação de `IO` a cada item da lista e ignora os resultados;
- `\(w, f) -> ...`: função anônima, também chamada de lambda;
- `(w, f)`: pattern matching para extrair palavra e frequência;
- `++`: concatenação de strings;
- `show f`: converte a frequência para string;
- `$`: aplica `putStrLn` ao texto montado.

Exemplo de saída desta linha:

```text
let: 4
```

**Linha 79**

```haskell
            putStrLn "-------------------------------------"
```

Imprime uma linha separadora.

**Linha 80**

```haskell
            putStrLn $ "m = " ++ show m
```

Imprime o valor de `m`.

**Linha 81**

```haskell
            putStrLn $ "Soma(f1) = " ++ show sumF1
```

Imprime a soma das frequências ponderadas de `c1`.

**Linha 82**

```haskell
            putStrLn $ "Índice de Similaridade = " ++ show sim
```

Imprime o índice final de similaridade.

`sim` é um `Double`, e `show sim` converte o número decimal em texto.

## 4. Fluxo completo do algoritmo

O fluxo do programa é:

1. Ler os quatro argumentos da linha de comando.
2. Se a quantidade de argumentos estiver errada, mostrar a forma correta de uso.
3. Ler o conteúdo dos quatro arquivos.
4. Transformar `res.txt` em conjunto de palavras reservadas.
5. Transformar `sep.txt` em conjunto de caracteres separadores.
6. Tokenizar `c1` e `c2`.
7. Calcular frequências ponderadas dos dois códigos.
8. Ordenar as frequências de `c1`.
9. Calcular `m`.
10. Calcular `soma(f1)`.
11. Calcular `m / soma(f1)`.
12. Imprimir o relatório.

## 5. Exemplo manual com os arquivos atuais

Com `c1.txt`:

```text
let x=10
let y=20
if x==y then
    return x
else
    return y
```

Após remover os separadores, os tokens principais são:

```text
let x 10 let y 20 if x y then return x else return y
```

Palavras reservadas do exemplo:

```text
if then else let in do return case of
```

Frequências ponderadas de `c1`:

| Palavra | Ocorrências | Peso | Frequência ponderada |
|---|---:|---:|---:|
| `let` | 2 | 2 | 4 |
| `return` | 2 | 2 | 4 |
| `x` | 3 | 1 | 3 |
| `y` | 3 | 1 | 3 |
| `if` | 1 | 2 | 2 |
| `then` | 1 | 2 | 2 |
| `else` | 1 | 2 | 2 |
| `10` | 1 | 1 | 1 |
| `20` | 1 | 1 | 1 |

Soma de `f1`:

```text
4 + 4 + 3 + 3 + 2 + 2 + 2 + 1 + 1 = 22
```

Como `c2.txt` usa `a` e `b` no lugar de `x` e `y`, as palavras reservadas e os números continuam parecidos, mas os identificadores mudam.

Por isso:

```text
m = 16
similaridade = 16 / 22 = 0.7272727272727273
```

## 6. O que cada integrante precisa dominar

Todos devem saber explicar:

- o que é Bag-of-Words;
- por que o algoritmo ignora separadores;
- por que palavras reservadas têm peso maior;
- como a frequência ponderada é calculada;
- como a regra dos 10% define se uma palavra contribui para `m`;
- por que o índice final fica entre 0 e 1;
- como compilar e executar com `make run`.

O grupo não precisa decorar cada função da biblioteca Haskell, mas precisa saber justificar por que `Map`, `Set`, `sortBy`, `words` e `readFile` foram usados.
