module Main where

import HaskellAssignment

unit_test :: (Eq a) => a -> a -> [Char]
unit_test expected actual
  | expected == actual = "Pass"
  | otherwise = "Fail"

main :: IO ()
main = do
  -- Test findFirst
  putStrLn $ unit_test (NoMatch) $ findFirst ((==) 1) []
  putStrLn $ unit_test (Match 0) $ findFirst ((/=) 1) [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
  putStrLn $ unit_test (Match 9) $ findFirst ((==) 5) [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
  putStrLn $ unit_test (Match 0) $ findFirst (11 >) [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
  putStrLn $ unit_test (NoMatch) $ findFirst (const False) [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
  putStrLn $ unit_test (NoMatch) $ findFirst ((==) 11) [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
  putStrLn $ unit_test (Match 0) $ findFirst ((==) 11) [11, 10, 1, 9, 2, 8, 3, 7, 4, 6, 5, 11]
  putStrLn $ unit_test (Match 10) $ findFirst ((==) 11) [10, 1, 9, 2, 8, 3, 7, 4, 6, 5, 11]
  putStrLn $ unit_test (Match 2) $ findFirst (id) [False, False, True]
  -- Test palindrome
  putStrLn $ unit_test True $ palindrome ""
  putStrLn $ unit_test True $ palindrome "a"
  putStrLn $ unit_test True $ palindrome "aa"
  putStrLn $ unit_test False $ palindrome "ab"
  putStrLn $ unit_test True $ palindrome "aba"
  putStrLn $ unit_test True $ palindrome "abba"
  putStrLn $ unit_test True $ palindrome "amanaplanacanalpanama"
  putStrLn $ unit_test True $ palindrome "madamimadam"
  putStrLn $ unit_test True $ palindrome "neveroddoreven"
  putStrLn $ unit_test True $ palindrome "ablewasiereisawelba"
  putStrLn $ unit_test True $ palindrome "tacocat"
