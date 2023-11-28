module HaskellAssignment where

------------------------------------------------
-- findFirst
------------------------------------------------
data Found = Match Int | NoMatch deriving (Eq)

instance Show Found where
  show (Match index) = "Found match at " ++ show index
  show NoMatch = "No match found!"

findFirst :: (Eq a) => (a -> Bool) -> [a] -> Found -- function takes a function and a list and returns a SearchResult
findFirst _ [] = NoMatch -- if list is empty, return NoMatch immediately
findFirst needle haystack = findFirst' needle haystack 0 -- call helper function (needle) with index 0 and the list (haystack), declared as modified because it takes an index as well
  where
    -- helper function body
    findFirst' _ [] _ = NoMatch -- if list is empty, return NoMatch
    findFirst' needle (x : xs) index -- if list is not empty, check if needle is found at the head of the list
      | needle x = Match index -- if needle is found, return Match with the index, guarded by the result of the function call
      | otherwise = findFirst' needle xs (index + 1) -- otherwise (keyword), if needle is not found, call helper function with the tail of the list and the index incremented by 1, guarded by the result of the recursive call

------------------------------------------------
-- palindrome
------------------------------------------------
palindrome :: [Char] -> Bool -- function takes a list of Chars (string) and returns a Bool
palindrome [] = True -- if list is empty, return True
palindrome [_] = True -- if list has only one element, return True
palindrome (x : xs) = x == last xs && palindrome (init xs) -- if list has more than one element, check if the first element is equal to the last element and call the function with the tail of the list excluding the last element (init xs)
