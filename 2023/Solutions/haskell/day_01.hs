import System.Environment (getArgs)
import Data.Char (isDigit)

getDayInput :: Int -> IO [String]
getDayInput day = readFile ("input" ++ show day ++ ".txt") >>= return . lines

main :: IO ()
main = do
    inputList <- getDayInput 1
    let res = sum $ map processRow inputList
    putStrLn $ "Part 1: " ++ show res
    where
        processRow :: String -> Int
        processRow row = read value :: Int
            where
                digits = filter isDigit row
                value = if length digits == 1 then digits ++ digits else [head digits] ++ [last digits]