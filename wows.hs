fst3 (x, _, _) = x
snd3 (_, x, _) = x
thd3 (_, _, x) = x

availableShips :: (Num a) => [(String, a, String)]
availableShips = [
  ("Myogi", 6700, "Kawachi"),
  ("Furutaka", 11500, "Kuma"),
  ("Akatsuki", 63000, "Fubuki"),
  ("Hatsuharu", 34000, "Minekaze"),
  ("Shokaku", 161000, "Ryujo"),
  ("Wyoming", 7200, "S. Carolina"),
  ("Helena", 75000, "Dallas"),
  ("New Orleans", 70000, "Pensacola"),
  ("Wickes", 2200, "Sampson"),
  ("Knyaz Suvorov", 2700, "Bogatyr"),
  ("Svietlana", 5700, "Bogatyr"),
  ("Derzki", 2350, "Storozhevoi"),
  ("Gneisenau", 80500, "Bayern"),
  ("Karlsruhe", 5800, "Kolberg"),
  ("G-101", 2000, "V-25"),
  ("Iron Duke", 13000, "Orion"),
  ("Danae", 5600, "Caledon"),
  ("Valkyrie", 2150, "Medea"),
  ("Turenne", 2850, "Friant"),
  ("Duguay-Trouin", 5600, "Friant"),
  ("Fusilier", 2100, "En. Gabolde"),
  ("Phra Ruang", 2100, "Longjiang"),
  ("Giussano", 5250, "Taranto"),
  ("Dante Alighieri", 1000000, "Taranto"),
  ("Klas Horn", 6000, "Romulus")
  ]

unlockedShips :: (Num a) => [(String, a)]
unlockedShips = [
  ("Kawachi", 0),
  ("Kuma", 3763),
  ("Fubuki", 27270),
  ("Minekaze", 10758),
  ("Ryujo", 2195),
  ("S. Carolina", 0),
  ("Dallas", 2382),
  ("Pensacola", 34683),
  ("Sampson", 0),
  ("Bogatyr", 0),
  ("Storozhevoi", 0),
  ("Bayern", 7118),
  ("Kolberg", 3553),
  ("V-25", 325),
  ("Orion", 1843),
  ("Caledon", 1591),
  ("Medea", 0),
  ("Friant", 0),
  ("En. Gabolde", 0),
  ("Longjiang", 0),
  ("Taranto", 0),
  ("Romulus", 0)
  ]

xpRemaining :: (Num a) => [(String, a)] -> [(String, a, String)] -> String ->Maybe a
xpRemaining [] _ _ = Nothing
xpRemaining _ [] _ = Nothing
xpRemaining ((us, uxp):uls) ((as, rxp, parent):avs) target | as /= target = xpRemaining ((us, uxp):uls) avs target
                                                           | us /= parent = xpRemaining uls [(as, rxp, parent)] target
                                                           | otherwise = Just (rxp - uxp)


isUnlocked :: (Eq a) => [(String, a)] -> String -> Bool
isUnlocked [] _ = False
isUnlocked ((front, _):library) ship | front == ship = True
                                       | otherwise = isUnlocked library ship

main :: IO ()
main = do
  print $ all (isUnlocked unlockedShips . fst) unlockedShips
  print $ all (isUnlocked unlockedShips . thd3) availableShips
  putStrLn . unlines $ map (show . ((,) <$> fst3 <*> (xpRemaining unlockedShips availableShips . fst3))) availableShips
