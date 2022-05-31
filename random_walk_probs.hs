-- |

module Rw where

rwp 1 0 = 0
rwp 1 1 = 1
rwp n 0 = (rwp (n-1) 0) + (rwp (n-1) 1) * 0.5
rwp n 1 = (rwp (n-1) 2) * 0.5
rwp n k | n < 1 = error "Generations start at 1"
        | k < 0 = error "Columns start at 0"
        | k > n = 0
        | otherwise = ((rwp (n-1) (k-1)) + (rwp (n-1) (k+1))) * 0.5
