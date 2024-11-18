{-# LANGUAGE OverloadedStrings #-}

import System.FilePath ((</>))
import System.IO (readFile)
import Data.Text (Text)
import qualified Data.Text as T
import qualified Data.Text.IO as TIO

base :: FilePath
base = "C:/Users/raikoug/SyncThing/shared_code_tests/adventOfCode/2023/"

getFilePath :: Int -> Bool -> FilePath
getFilePath day test = base </> ("day_" ++ show day) </> fileName
  where
    fileName = if test then "test_input.txt" else "input.txt"

getDayInput :: Int -> Bool -> IO [Text]
getDayInput day test = do
    content <- TIO.readFile $ getFilePath day test
    return $ T.lines content