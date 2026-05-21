import System.Environment (getArgs)
import Data.List (sortBy)
import qualified Data.Map as M

-- | Retorna as frequências das palavras, aplicando peso em dobro para palavras reservadas,
-- e ignorando as palavras presentes na lista de separadores (sep).
getFrequencies :: [String] -> [String] -> [String] -> M.Map String Int
getFrequencies res sep text = 
    let filteredText = filter (`notElem` sep) text
        wordCounts = M.fromListWith (+) [(w, if w `elem` res then 2 else 1) | w <- filteredText]
    in wordCounts

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
            
            let res = words resContent
                sep = words sepContent
                c1 = words c1Content
                c2 = words c2Content
                
                freq1 = getFrequencies res sep c1
                freq2 = getFrequencies res sep c2
                
                list1 = M.toList freq1
                
                -- Ordena de forma decrescente pela frequência, desempate lexicográfico crescente
                sorted1 = sortBy (\(w1, f1) (w2, f2) -> 
                    case compare f2 f1 of
                        EQ -> compare w1 w2
                        other -> other) list1
                        
                -- Diferença de até 10%: abs(f1 - f2) / max(f1, f2) <= 0.1
                -- Usamos inteiros: abs(f1 - f2) * 10 <= max(f1, f2)
                m = sum [ f1 | (w, f1) <- list1, 
                               let f2 = M.findWithDefault 0 w freq2,
                               abs (f1 - f2) * 10 <= max f1 f2 ]
                               
                sumF1 = sum (map snd list1)
                
                sim = if sumF1 == 0 then 0.0 else fromIntegral m / fromIntegral sumF1 :: Double
                
            putStrLn "--- Relatório de Frequências (c1) ---"
            mapM_ (\(w, f) -> putStrLn $ w ++ ": " ++ show f) sorted1
            putStrLn "-------------------------------------"
            putStrLn $ "m = " ++ show m
            putStrLn $ "Soma(f1) = " ++ show sumF1
            putStrLn $ "Índice de Similaridade = " ++ show sim
