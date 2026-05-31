import System.Environment (getArgs)
import Data.List (sortBy)
import qualified Data.Map as M
import qualified Data.Set as S

type Frequencies = M.Map String Int

-- | Transforma cada separador em espaço e depois quebra o texto em palavras.
tokenize :: S.Set Char -> String -> [String]
tokenize separators source =
    words [if char `S.member` separators then ' ' else char | char <- source]

-- | Retorna 2 para palavras reservadas e 1 para as demais.
wordWeight :: S.Set String -> String -> Int
wordWeight reserved word =
    if word `S.member` reserved then 2 else 1

-- | Computa as frequências ponderadas das palavras.
getFrequencies :: S.Set String -> [String] -> Frequencies
getFrequencies reserved tokens =
    M.fromListWith (+) [(word, wordWeight reserved word) | word <- tokens]

-- | Ordena por frequência decrescente e usa ordem lexicográfica como desempate.
frequencyOrder :: (String, Int) -> (String, Int) -> Ordering
frequencyOrder (word1, freq1) (word2, freq2) =
    case compare freq2 freq1 of
        EQ -> compare word1 word2
        other -> other

-- | Verifica se f2 difere de f1 em no máximo 10% de f1.
isWithinTenPercent :: Int -> Int -> Bool
isWithinTenPercent freq1 freq2 =
    abs (freq1 - freq2) * 10 <= freq1

matchingScore :: Frequencies -> Frequencies -> Int
matchingScore freq1 freq2 =
    sum [value1 | (word, value1) <- M.toList freq1,
                  let value2 = M.findWithDefault 0 word freq2,
                  isWithinTenPercent value1 value2]

totalFrequency :: Frequencies -> Int
totalFrequency frequencies =
    sum (map snd (M.toList frequencies))

similarityIndex :: Frequencies -> Frequencies -> Double
similarityIndex freq1 freq2 =
    let matchingTotal = matchingScore freq1 freq2
        total1 = totalFrequency freq1
    in if total1 == 0 then 0.0 else fromIntegral matchingTotal / fromIntegral total1

main :: IO ()
main = do
    args <- getArgs
    if length args /= 4
        then putStrLn "Uso: ./similaridade <res.txt> <sep.txt> <c1.txt> <c2.txt>"
        else do
            let [resFile, sepFile, c1File, c2File] = args
            resContent <- readFile resFile
            sepContent <- readFile sepFile
            c1Content <- readFile c1File
            c2Content <- readFile c2File
            
            let reserved = S.fromList (words resContent)
                separators = S.fromList (concat (words sepContent))
                c1 = tokenize separators c1Content
                c2 = tokenize separators c2Content
                
                freq1 = getFrequencies reserved c1
                freq2 = getFrequencies reserved c2
                
                list1 = M.toList freq1
                sorted1 = sortBy frequencyOrder list1
                m = matchingScore freq1 freq2
                sumF1 = totalFrequency freq1
                similarity = similarityIndex freq1 freq2
                
            putStrLn "--- Relatório de Frequências (c1) ---"
            mapM_ (\(w, f) -> putStrLn $ w ++ ": " ++ show f) sorted1
            putStrLn "-------------------------------------"
            putStrLn $ "m = " ++ show m
            putStrLn $ "Soma(f1) = " ++ show sumF1
            putStrLn $ "Índice de Similaridade = " ++ show similarity
