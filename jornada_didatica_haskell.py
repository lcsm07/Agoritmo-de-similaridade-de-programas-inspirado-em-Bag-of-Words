#!/usr/bin/env python3
"""
Jornada didatica interativa do programa Main.hs.

Este arquivo e uma versao enriquecida da simulacao. Ele mantem a mesma ideia do
programa Haskell, mas apresenta o fluxo como uma jornada em fases:

- cada fase representa uma etapa do main;
- cada funcao chamada mostra o que recebe, o que transforma e o que devolve;
- o usuario aperta Enter para avancar;
- os valores aparecem como um "inventario" que vai crescendo;
- as contas sao abertas para facilitar o aprendizado de Haskell.

O objetivo nao e otimizar Python. O objetivo e enxergar o raciocinio funcional
do Haskell acontecendo passo a passo.
"""

from __future__ import annotations

import time
from collections import defaultdict
from pathlib import Path
from textwrap import dedent, indent, wrap


ROOT = Path(__file__).resolve().parent
LINE = "=" * 78
SMALL_LINE = "-" * 78


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


def paint(text: object, color: str, bold: bool = False) -> str:
    prefix = Color.BOLD if bold else ""
    return f"{prefix}{color}{text}{Color.RESET}"


class Guide:
    def __init__(self) -> None:
        self.phase = 0
        self.xp = 0
        self.fast_mode = False
        self.step_delay = 0.12

    def pause(self, message: str = "Pressione Enter para continuar...") -> None:
        print()
        try:
            input(paint(message, Color.YELLOW))
        except EOFError:
            print("(Entrada interativa indisponivel; seguindo automaticamente.)")

    def configure_speed(self) -> None:
        print(paint("Modo de ritmo", Color.CYAN, bold=True))
        print("  1 - Imersivo: mostra timers e pequenas pausas.")
        print("  2 - Rapido: pula esperas automaticas, mantendo as pausas de Enter.")
        choice = input(paint("Escolha 1 ou 2 e pressione Enter: ", Color.YELLOW)).strip()
        self.fast_mode = choice == "2"
        self.step_delay = 0.0 if self.fast_mode else 0.12
        print()
        if self.fast_mode:
            print(paint("Ritmo rapido ativado. As explicacoes continuam completas.", Color.GREEN))
        else:
            print(paint("Ritmo imersivo ativado. A jornada vai respirar entre as etapas.", Color.GREEN))

    def sleep(self, seconds: float) -> None:
        if not self.fast_mode:
            time.sleep(seconds)

    def countdown(self, label: str, seconds: int = 3) -> None:
        print(paint(label, Color.MAGENTA, bold=True))
        if self.fast_mode:
            print(paint("  timer pulado no modo rapido.", Color.DIM))
            return
        for remaining in range(seconds, 0, -1):
            print(paint(f"  iniciando em {remaining}...", Color.MAGENTA))
            time.sleep(0.45)

    def progress(self, label: str, steps: int = 12) -> None:
        print(paint(label, Color.BLUE, bold=True))
        if self.fast_mode:
            print("  [" + "#" * steps + "] pronto")
            return
        bar = ""
        for _ in range(steps):
            bar += "#"
            print(f"\r  [{bar:<{steps}}]", end="", flush=True)
            time.sleep(0.05)
        print(" pronto")

    def title(self, title: str) -> None:
        print()
        print(paint(LINE, Color.CYAN))
        print(paint(title, Color.CYAN, bold=True))
        print(paint(LINE, Color.CYAN))

    def phase_title(self, title: str) -> None:
        self.phase += 1
        self.xp += 10
        print()
        print(paint(LINE, Color.BLUE))
        print(paint(f"FASE {self.phase}: {title}", Color.BLUE, bold=True))
        print(paint(f"XP de entendimento: {self.xp}", Color.GREEN, bold=True))
        print(paint(LINE, Color.BLUE))
        self.sleep(0.25)

    def speak(self, text: str) -> None:
        paragraphs = dedent(text).strip().split("\n\n")
        for paragraph in paragraphs:
            if paragraph.startswith("    "):
                print(paragraph)
                continue
            for line in wrap(paragraph, width=78):
                print(line)
                self.sleep(0.015)
            print()

    def code(self, source: str) -> None:
        print(paint(indent(dedent(source).strip(), "    "), Color.CYAN))
        print()

    def inventory(self, title: str, items: dict[str, object]) -> None:
        print(paint(f"[Inventario: {title}]", Color.GREEN, bold=True))
        for name, value in items.items():
            print(f"  {paint(name, Color.GREEN)}: {value}")
        print()

    def checkpoint(self, question: str, expected_keywords: tuple[str, ...]) -> None:
        print(paint("Checkpoint de aprendizado", Color.YELLOW, bold=True))
        print(question)
        answer = input(paint("Sua resposta curta: ", Color.YELLOW)).strip().lower()
        if not answer:
            print(paint("Sem problema. Vamos revelar a ideia principal.", Color.MAGENTA))
        elif any(keyword in answer for keyword in expected_keywords):
            print(paint("Boa leitura. Essa e exatamente a direcao da ideia.", Color.GREEN))
        else:
            print(paint("Resposta util, mas vamos fixar a formulacao do programa.", Color.MAGENTA))
        print()


def sorted_set_repr(values: set[str]) -> str:
    return "{" + ", ".join(repr(value) for value in sorted(values)) + "}"


def map_repr(values: dict[str, int]) -> str:
    return "{" + ", ".join(f"{key!r}: {values[key]}" for key in sorted(values)) + "}"


def load_text(file_name: str, guide: Guide) -> str:
    path = ROOT / file_name
    guide.progress(f"Abrindo portal de IO para {file_name}")
    content = path.read_text(encoding="utf-8")
    print(paint(f"Arquivo aberto: {file_name}", Color.GREEN, bold=True))
    print(f"Tamanho lido: {paint(len(content), Color.YELLOW)} caracteres")
    print(paint("Previa do conteudo:", Color.CYAN))
    print(indent(paint(repr(content), Color.WHITE), "  "))
    guide.speak(
        """
        Neste momento, o Haskell saiu do mundo puro e consultou o sistema de
        arquivos. O resultado de readFile e uma String. A partir daqui, essa
        String pode ser passada para funcoes puras sem que o arquivo original
        seja modificado.
        """
    )
    print()
    guide.pause()
    return content


def tokenize(separators: set[str], source: str, label: str, guide: Guide) -> list[str]:
    guide.phase_title(f"Entrando na funcao tokenize para {label}")
    guide.speak(
        """
        Esta fase corresponde a funcao pura tokenize.

        Em Haskell, ela recebe dois valores: o conjunto de separadores e o texto
        original do codigo. Ela nao altera o arquivo, nao altera variavel global
        e nao imprime nada no programa real. Ela apenas devolve uma lista nova
        de palavras.
        """
    )
    guide.code(
        """
        tokenize :: S.Set Char -> String -> [String]
        tokenize separators source =
            words [if char `S.member` separators then ' ' else char | char <- source]
        """
    )
    guide.inventory(
        "entrada da tokenize",
        {
            "separators": sorted_set_repr(separators),
            "source": repr(source),
        },
    )
    guide.checkpoint(
        "Antes de continuar: por que trocar '=' por espaco ajuda a tokenizar x=10?",
        ("separ", "token", "palavra", "espaco"),
    )
    guide.speak(
        """
        Resposta esperada: sem essa troca, x=10 poderia virar um unico token.
        Ao trocar '=' por espaco, o texto passa a ter x e 10 como tokens
        separados. Isso e essencial para contar frequencias corretamente.
        """
    )
    guide.countdown("Scanner de caracteres preparado", 3)
    guide.pause("Aperte Enter para percorrer os caracteres...")

    normalized_chars: list[str] = []
    replacements: list[tuple[int, str]] = []

    print(paint("Percurso caractere por caractere:", Color.CYAN, bold=True))
    for index, char in enumerate(source):
        if char in separators:
            normalized_chars.append(" ")
            replacements.append((index, char))
            action = paint("separador encontrado; vira espaco", Color.YELLOW)
            result = paint("' '", Color.YELLOW)
        else:
            normalized_chars.append(char)
            action = paint("caractere mantido", Color.GREEN)
            result = repr(char)

        printable = "\\n" if char == "\n" else char
        print(f"  posicao {index:>2}: {printable!r:<4} -> {result:<4} | {action}")
        guide.sleep(guide.step_delay)

    normalized = "".join(normalized_chars)

    guide.pause("Aperte Enter para ver o texto normalizado...")
    guide.speak(
        """
        A compreensao de lista terminou. Em Haskell, a parte entre colchetes
        construiu uma nova String. Lembre: String em Haskell e uma lista de Char.

        Agora entra a funcao words. Ela quebra o texto em palavras, usando
        espacos, quebras de linha e tabulacoes como divisores.
        """
    )
    guide.inventory(
        "saida intermediaria da compreensao de lista",
        {
            "separadores_trocados": replacements,
            "texto_normalizado": repr(normalized),
        },
    )

    tokens = normalized.split()
    guide.progress("Aplicando words: quebrando a String normalizada em tokens")
    print(paint("Aplicando words/split:", Color.CYAN, bold=True))
    print(f"  antes: {paint(repr(normalized), Color.WHITE)}")
    print(f"  depois: {paint(tokens, Color.GREEN)}")
    print()
    guide.inventory("saida da tokenize", {"tokens": tokens, "quantidade": len(tokens)})
    guide.speak(
        """
        Repare no tipo da saida: [String]. O codigo nao sabe ainda quais
        palavras sao importantes; ele so preparou uma lista limpa para a proxima
        funcao. Em Haskell, isso facilita a composicao: tokenize resolve uma
        tarefa pequena e entrega o resultado para getFrequencies.
        """
    )
    guide.pause()
    return tokens


def word_weight(reserved: set[str], word: str, guide: Guide) -> int:
    weight = 2 if word in reserved else 1
    kind = "palavra reservada" if weight == 2 else "palavra comum"
    print(
        f"    {paint('wordWeight', Color.CYAN)} reserved {paint(repr(word), Color.YELLOW)}: "
        f"{paint(kind, Color.GREEN if weight == 2 else Color.WHITE)}; "
        f"peso devolvido = {paint(weight, Color.MAGENTA, bold=True)}"
    )
    guide.sleep(guide.step_delay)
    return weight


def get_frequencies(
    reserved: set[str],
    tokens: list[str],
    label: str,
    guide: Guide,
) -> dict[str, int]:
    guide.phase_title(f"Entrando na funcao getFrequencies para {label}")
    guide.speak(
        """
        Agora a jornada entra no contador ponderado.

        O Haskell monta uma lista de pares no formato (palavra, peso). Depois
        M.fromListWith (+) transforma essa lista em Map. Quando a mesma palavra
        aparece mais de uma vez, o (+) soma os pesos.
        """
    )
    guide.code(
        """
        type Frequencies = M.Map String Int

        getFrequencies :: S.Set String -> [String] -> Frequencies
        getFrequencies reserved tokens =
            M.fromListWith (+) [(word, wordWeight reserved word) | word <- tokens]
        """
    )
    guide.inventory(
        "entrada da getFrequencies",
        {
            "reserved": sorted_set_repr(reserved),
            "tokens": tokens,
        },
    )
    guide.checkpoint(
        "Se a palavra 'let' aparece duas vezes e cada 'let' pesa 2, qual sera a frequencia ponderada?",
        ("4", "quatro"),
    )
    guide.speak(
        """
        A frequencia ponderada sera 4. O programa nao esta contando apenas
        aparicoes; ele conta pontos. Palavra comum vale 1 ponto por aparicao.
        Palavra reservada vale 2 pontos por aparicao.
        """
    )
    guide.countdown("Oficina de pesos iniciada", 3)
    guide.pause("Aperte Enter para transformar tokens em pares (palavra, peso)...")

    pairs: list[tuple[str, int]] = []
    print(paint("Construindo a lista [(word, wordWeight reserved word) | word <- tokens]", Color.CYAN, bold=True))
    for word in tokens:
        weight = word_weight(reserved, word, guide)
        pairs.append((word, weight))

    print()
    guide.inventory("lista criada pela compreensao", {"pares": pairs})
    guide.pause("Aperte Enter para ver M.fromListWith (+) somando repeticoes...")

    frequencies: dict[str, int] = defaultdict(int)
    guide.progress("Ativando M.fromListWith (+): palavras repetidas serao somadas")
    print(paint("Construindo o Map de frequencias:", Color.CYAN, bold=True))
    for step, (word, weight) in enumerate(pairs, start=1):
        before = frequencies[word]
        after = before + weight
        frequencies[word] = after
        print(
            f"  passo {paint(f'{step:>2}', Color.BLUE)}: "
            f"chave={paint(f'{word!r:<8}', Color.YELLOW)} "
            f"peso={paint(weight, Color.MAGENTA)} | "
            f"valor antigo={paint(f'{before:<2}', Color.RED)} "
            f"valor novo={paint(f'{after:<2}', Color.GREEN, bold=True)}"
        )
        guide.sleep(guide.step_delay)

    result = dict(frequencies)
    print()
    guide.inventory(
        "saida da getFrequencies",
        {
            "freq": map_repr(result),
            "soma": total_frequency(result),
        },
    )
    guide.speak(
        """
        Esta fase mostra uma diferenca importante entre o jeito imperativo e o
        jeito funcional de pensar. No Haskell original, nao escrevemos um loop
        manual para atualizar uma variavel. Descrevemos uma lista de pares e
        pedimos ao Map para combinar chaves repetidas com (+).

        A simulacao mostra o loop apenas para tornar visivel a soma que
        M.fromListWith (+) faria por baixo.
        """
    )
    guide.pause()
    return result


def frequency_order(item: tuple[str, int]) -> tuple[int, str]:
    word, frequency = item
    return (-frequency, word)


def explain_frequency_order(freq1: dict[str, int], guide: Guide) -> list[tuple[str, int]]:
    guide.phase_title("Ordenando o relatorio com frequencyOrder")
    guide.speak(
        """
        O relatorio final nao imprime o Map em qualquer ordem. Primeiro as
        palavras sao convertidas para lista com M.toList. Depois sortBy usa
        frequencyOrder.

        A regra e: maior frequencia primeiro. Se duas palavras tiverem a mesma
        frequencia, vence a ordem lexicografica, isto e, a ordem alfabetica dos
        textos.
        """
    )
    guide.code(
        """
        frequencyOrder :: (String, Int) -> (String, Int) -> Ordering
        frequencyOrder (word1, freq1) (word2, freq2) =
            case compare freq2 freq1 of
                EQ -> compare word1 word2
                other -> other
        """
    )

    list1 = sorted(freq1.items())
    sorted1 = sorted(list1, key=frequency_order)
    guide.inventory(
        "antes e depois da ordenacao",
        {
            "list1 = M.toList freq1": list1,
            "sorted1": sorted1,
        },
    )

    guide.progress("Aplicando sortBy frequencyOrder")
    print(paint("Como ler alguns casos:", Color.CYAN, bold=True))
    print(f"  {paint('let', Color.YELLOW)} aparece 4 vezes ponderadas, por isso fica antes de x e y.")
    print(f"  {paint('x', Color.YELLOW)} e {paint('y', Color.YELLOW)} empatam com frequencia 3; x vem antes de y pela ordem lexicografica.")
    print("  do, else, if, return e then empatam com frequencia 2; ficam em ordem de texto.")
    guide.speak(
        """
        A funcao frequencyOrder nao calcula frequencias novas. Ela e apenas uma
        regra de comparacao. O sortBy chama essa regra varias vezes para decidir
        qual par deve aparecer antes no relatorio.
        """
    )
    print()
    guide.pause()
    return sorted1


def is_within_ten_percent(freq1: int, freq2: int) -> bool:
    return abs(freq1 - freq2) * 10 <= freq1


def explain_ten_percent_rule(freq1: int, freq2: int) -> tuple[int, bool]:
    difference_rule_value = abs(freq1 - freq2) * 10
    return difference_rule_value, difference_rule_value <= freq1


def matching_score(
    freq1: dict[str, int],
    freq2: dict[str, int],
    guide: Guide,
) -> int:
    guide.phase_title("Calculando m com matchingScore")
    guide.speak(
        """
        Esta e a fase de comparacao. O programa olha somente para as palavras
        existentes em c1. Para cada palavra, ele procura a frequencia da mesma
        palavra em c2.

        A palavra contribui para m quando a frequencia de c2 esta dentro de uma
        margem de 10% em relacao a frequencia de c1.
        """
    )
    guide.code(
        """
        matchingScore :: Frequencies -> Frequencies -> Int
        matchingScore freq1 freq2 =
            sum [value1 | (word, value1) <- M.toList freq1,
                          let value2 = M.findWithDefault 0 word freq2,
                          isWithinTenPercent value1 value2]

        isWithinTenPercent :: Int -> Int -> Bool
        isWithinTenPercent freq1 freq2 =
            abs (freq1 - freq2) * 10 <= freq1
        """
    )
    guide.inventory(
        "entrada da matchingScore",
        {
            "freq1": map_repr(freq1),
            "freq2": map_repr(freq2),
        },
    )
    guide.checkpoint(
        "Se uma palavra existe em c1 mas nao existe em c2, qual valor f2 o codigo usa?",
        ("0", "zero"),
    )
    guide.speak(
        """
        O codigo usa 0. Isso vem de M.findWithDefault 0 word freq2. A traducao
        da ideia e: procure a palavra em c2; se ela nao existir, finja que a
        frequencia dela em c2 e zero.
        """
    )
    guide.countdown("Arena de comparacao aberta", 3)
    guide.pause("Aperte Enter para comparar palavra por palavra...")

    score = 0
    for word in sorted(freq1):
        value1 = freq1[word]
        value2 = freq2.get(word, 0)
        difference_rule_value, matches = explain_ten_percent_rule(value1, value2)

        print(paint(SMALL_LINE, Color.BLUE))
        print(f"Palavra investigada: {paint(repr(word), Color.YELLOW, bold=True)}")
        print(f"  f1 vem de c1: {paint(value1, Color.GREEN, bold=True)}")
        print(f"  f2 vem de c2: {paint(value2, Color.GREEN if value2 else Color.RED, bold=True)}")
        print(f"  regra: {paint('abs(f1 - f2) * 10 <= f1', Color.CYAN)}")
        print(
            f"  conta: abs({value1} - {value2}) * 10 = "
            f"{paint(difference_rule_value, Color.MAGENTA, bold=True)}"
        )
        print(f"  limite permitido: {paint(value1, Color.YELLOW, bold=True)}")

        if matches:
            before = score
            score += value1
            print(paint("  resultado: passou na regra de 10%.", Color.GREEN, bold=True))
            print(
                f"  m recebe f1: {paint(before, Color.WHITE)} + "
                f"{paint(value1, Color.YELLOW)} = {paint(score, Color.GREEN, bold=True)}"
            )
        else:
            print(paint("  resultado: nao passou na regra de 10%.", Color.RED, bold=True))
            print(f"  m fica como esta: {paint(score, Color.YELLOW)}")

        guide.pause("Enter para a proxima palavra...")

    print(paint(SMALL_LINE, Color.BLUE))
    guide.inventory("saida da matchingScore", {"m": score})
    guide.speak(
        """
        O m nao e uma contagem de quantas palavras combinaram. Ele soma os pesos
        de c1 das palavras que combinaram. Por isso uma palavra reservada que
        aparece muito pode influenciar mais o resultado do que um identificador
        comum que aparece uma unica vez.
        """
    )
    return score


def total_frequency(frequencies: dict[str, int]) -> int:
    return sum(frequencies.values())


def explain_total_frequency(freq1: dict[str, int], guide: Guide) -> int:
    guide.phase_title("Somando todas as frequencias de c1")
    guide.speak(
        """
        totalFrequency pega todos os valores do Map e soma.

        No Haskell, M.toList transforma o Map em lista de pares. map snd pega
        somente o segundo item de cada par, ou seja, a frequencia. sum soma tudo.
        """
    )
    guide.code(
        """
        totalFrequency :: Frequencies -> Int
        totalFrequency frequencies =
            sum (map snd (M.toList frequencies))
        """
    )

    pairs = sorted(freq1.items())
    values = [frequency for _, frequency in pairs]
    total = total_frequency(freq1)
    guide.progress("Coletando somente as frequencias com map snd")
    guide.inventory(
        "conta da totalFrequency",
        {
            "M.toList freq1": pairs,
            "map snd": values,
            "sum": total,
        },
    )
    print(paint("Soma aberta:", Color.CYAN, bold=True))
    print("  " + " + ".join(str(value) for value in values) + f" = {paint(total, Color.GREEN, bold=True)}")
    guide.pause()
    return total


def explain_similarity_index(
    freq1: dict[str, int],
    freq2: dict[str, int],
    matching_total: int,
    total1: int,
    guide: Guide,
) -> float:
    guide.phase_title("Calculando o indice de similaridade")
    guide.speak(
        """
        A ultima funcao pura transforma os dois numeros principais em uma
        proporcao.

        m representa a parte de c1 que encontrou uma frequencia parecida em c2.
        Soma(f1) representa o tamanho ponderado total de c1. A divisao m /
        Soma(f1) gera um numero entre 0 e 1 neste exemplo.
        """
    )
    guide.code(
        """
        similarityIndex :: Frequencies -> Frequencies -> Double
        similarityIndex freq1 freq2 =
            let matchingTotal = matchingScore freq1 freq2
                total1 = totalFrequency freq1
            in if total1 == 0 then 0.0 else fromIntegral matchingTotal / fromIntegral total1
        """
    )

    calculated_again = sum(
        value1
        for word, value1 in freq1.items()
        if is_within_ten_percent(value1, freq2.get(word, 0))
    )
    sim = 0.0 if total1 == 0 else matching_total / total1

    guide.countdown("Preparando divisao final", 3)
    guide.inventory(
        "conta da similarityIndex",
        {
            "matchingTotal": matching_total,
            "matchingTotal recalculado pela regra": calculated_again,
            "total1": total1,
            "divisao": f"{matching_total} / {total1}",
            "resultado": sim,
        },
    )
    guide.speak(
        """
        O fromIntegral no Haskell aparece porque matchingTotal e total1 sao Int,
        mas a divisao final precisa produzir Double. Em outras palavras: antes
        de dividir, o Haskell converte os inteiros para numeros capazes de ter
        casas decimais.
        """
    )
    guide.pause()
    return sim


def show_final_report(
    sorted1: list[tuple[str, int]],
    matching_total: int,
    total1: int,
    similarity: float,
    guide: Guide,
) -> None:
    guide.phase_title("Relatorio final: a recompensa da jornada")
    guide.speak(
        """
        O main termina imprimindo exatamente o relatorio pedido pelo trabalho.
        Esta parte ja nao transforma mais os dados principais; ela apenas mostra
        na tela os valores calculados nas fases anteriores.
        """
    )
    guide.code(
        """
        putStrLn "--- Relatório de Frequências (c1) ---"
        mapM_ (\\(w, f) -> putStrLn $ w ++ ": " ++ show f) sorted1
        putStrLn "-------------------------------------"
        putStrLn $ "m = " ++ show m
        putStrLn $ "Soma(f1) = " ++ show sumF1
        putStrLn $ "Índice de Similaridade = " ++ show sim
        """
    )

    guide.progress("Renderizando relatorio final")
    print(paint("--- Relatório de Frequências (c1) ---", Color.CYAN, bold=True))
    for word, frequency in sorted1:
        print(f"{paint(word, Color.YELLOW)}: {paint(frequency, Color.GREEN)}")
    print(paint("-------------------------------------", Color.CYAN))
    print(f"m = {paint(matching_total, Color.GREEN, bold=True)}")
    print(f"Soma(f1) = {paint(total1, Color.GREEN, bold=True)}")
    print(f"Índice de Similaridade = {paint(similarity, Color.GREEN, bold=True)}")
    print()

    guide.speak(
        """
        Interpretacao final: c1 e c2 sao parecidos na estrutura, nas palavras
        reservadas e nos numeros. A diferenca principal e que c1 usa x e y,
        enquanto c2 usa a e b. Como matchingScore procura a mesma palavra nos
        dois codigos, x e y nao contribuem para m.

        Por isso o total ponderado de c1 e 23, mas somente 17 pontos entram em
        m. O indice final fica 17 / 23.
        """
    )


def start_story(guide: Guide) -> None:
    guide.title("JORNADA GUIADA: entendendo Main.hs como um jogo de fases")
    guide.configure_speed()
    guide.speak(
        """
        Bem-vindo ao modo jornada.

        Imagine que o main de Main.hs e o mapa principal. Cada let cria um item
        novo no inventario. Cada funcao pura e uma fase que recebe itens,
        transforma esses itens e devolve um novo item para a proxima fase.

        O objetivo final e derrotar a duvida central: como o programa chega no
        indice de similaridade 0.7391304347826086?
        """
    )
    guide.speak(
        """
        Durante a jornada, cores indicam papeis diferentes:

        verde mostra resultados ou valores que entraram no inventario;
        amarelo destaca palavras, tokens e escolhas importantes;
        azul marca mudancas de fase;
        magenta chama atencao para contas;
        vermelho aparece quando uma comparacao falha ou uma palavra nao existe
        no segundo codigo.
        """
    )
    guide.code(
        """
        main :: IO ()
        main = do
            args <- getArgs
            ...
            let reserved = S.fromList (words resContent)
                separators = S.fromList (concat (words sepContent))
                c1 = tokenize separators c1Content
                c2 = tokenize separators c2Content
                freq1 = getFrequencies reserved c1
                freq2 = getFrequencies reserved c2
                sorted1 = sortBy frequencyOrder list1
                m = matchingScore freq1 freq2
                sumF1 = totalFrequency freq1
                sim = similarityIndex freq1 freq2
        """
    )
    guide.countdown("Mapa principal carregado", 3)
    guide.pause("Aperte Enter para iniciar a Fase 1...")


def simulate_main_as_journey() -> None:
    guide = Guide()
    start_story(guide)

    guide.phase_title("Recebendo argumentos da linha de comando")
    guide.speak(
        """
        No programa real, getArgs pergunta ao sistema operacional quais
        argumentos foram passados na execucao.

        Aqui vamos simular a chamada usada pelo Makefile:

        ./similaridade res.txt sep.txt c1.txt c2.txt
        """
    )
    args = ["res.txt", "sep.txt", "c1.txt", "c2.txt"]
    guide.inventory("args", {"args": args, "length args": len(args)})
    guide.checkpoint(
        "O main espera quantos argumentos para continuar o processamento?",
        ("4", "quatro"),
    )
    guide.progress("Avaliando guarda de entrada")
    print(paint("Decisao do if:", Color.CYAN, bold=True))
    print(f"  {paint('length args /= 4 ?', Color.YELLOW)}")
    print(f"  {len(args)} /= 4 -> {paint('False', Color.GREEN, bold=True)}")
    print("  Como a condicao e falsa, o programa entra no else e continua.")
    guide.speak(
        """
        Esse if protege o programa contra uma execucao incompleta. Se faltasse
        algum arquivo, o programa nao teria como saber quais textos comparar.
        Por isso o ramo then imprime a mensagem de uso, e o ramo else executa a
        jornada principal.
        """
    )
    guide.pause()

    guide.phase_title("Lendo arquivos com readFile")
    guide.speak(
        """
        Esta e uma parte de IO. Diferente das funcoes puras, readFile conversa
        com o mundo externo: ele abre arquivos do disco e traz o conteudo para o
        programa.

        Depois que o texto entra no programa, as proximas fases trabalham com
        valores imutaveis.
        """
    )
    res_content = load_text("res.txt", guide)
    sep_content = load_text("sep.txt", guide)
    c1_content = load_text("c1.txt", guide)
    c2_content = load_text("c2.txt", guide)
    guide.inventory(
        "conteudos carregados",
        {
            "resContent": repr(res_content),
            "sepContent": repr(sep_content),
            "c1Content": repr(c1_content),
            "c2Content": repr(c2_content),
        },
    )
    guide.pause()

    guide.phase_title("Criando os conjuntos reserved e separators")
    guide.speak(
        """
        Agora comeca o bloco let. Em Haskell, let nao cria variaveis mutaveis.
        Ele associa nomes a valores.

        reserved vira um Set de String. separators vira um Set de Char.
        Set e importante porque a pergunta "este item pertence ao conjunto?" e
        direta e clara.
        """
    )
    guide.code(
        """
        let reserved = S.fromList (words resContent)
            separators = S.fromList (concat (words sepContent))
        """
    )
    reserved_words = res_content.split()
    separator_groups = sep_content.split()
    separators_joined = "".join(separator_groups)
    reserved = set(reserved_words)
    separators = set(separators_joined)

    guide.inventory(
        "construcao de reserved",
        {
            "words resContent": reserved_words,
            "S.fromList (...)": sorted_set_repr(reserved),
        },
    )
    guide.speak(
        """
        words resContent quebra o arquivo de reservadas em palavras. S.fromList
        remove repeticoes e cria um conjunto. Esse conjunto sera consultado por
        wordWeight para decidir se uma palavra vale 2 ou 1.
        """
    )
    guide.inventory(
        "construcao de separators",
        {
            "words sepContent": separator_groups,
            "concat (...)": repr(separators_joined),
            "S.fromList (...)": sorted_set_repr(separators),
        },
    )
    guide.speak(
        """
        A construcao dos separadores tem uma etapa a mais: concat. O arquivo
        sep.txt pode ter espacos entre os simbolos para ficar legivel. words
        separa esses simbolos em pequenos textos, concat junta tudo em uma unica
        String, e S.fromList transforma essa String em conjunto de caracteres.
        """
    )
    guide.checkpoint(
        "Qual conjunto sera usado pela tokenize: reserved ou separators?",
        ("separators", "separador", "separadores"),
    )
    guide.pause()

    c1_tokens = tokenize(separators, c1_content, "c1.txt", guide)
    c2_tokens = tokenize(separators, c2_content, "c2.txt", guide)

    freq1 = get_frequencies(reserved, c1_tokens, "c1.txt", guide)
    freq2 = get_frequencies(reserved, c2_tokens, "c2.txt", guide)

    sorted1 = explain_frequency_order(freq1, guide)
    matching_total = matching_score(freq1, freq2, guide)
    total1 = explain_total_frequency(freq1, guide)
    similarity = explain_similarity_index(freq1, freq2, matching_total, total1, guide)
    show_final_report(sorted1, matching_total, total1, similarity, guide)

    guide.title("FIM DA JORNADA")
    guide.speak(
        """
        Resumo do caminho:

        1. IO trouxe textos para dentro do programa.
        2. Set organizou palavras reservadas e separadores.
        3. tokenize limpou os codigos e produziu listas de tokens.
        4. getFrequencies transformou tokens em Map palavra -> frequencia.
        5. frequencyOrder definiu a ordem do relatorio.
        6. matchingScore calculou m comparando c1 contra c2.
        7. totalFrequency somou o tamanho ponderado de c1.
        8. similarityIndex dividiu m por Soma(f1).

        Essa e a ideia funcional central: valores entram em funcoes, novos
        valores saem, e o main encadeia a jornada.
        """
    )


if __name__ == "__main__":
    simulate_main_as_journey()
