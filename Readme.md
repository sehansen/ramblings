# Ramblings

## Auction producers

A little simulated economy with a daily food for gold auction.

Each person needs 1 food per day to survive. The option is to farm, giving 5 food, or work, giving 1.0 gold. Food comes in units of 1, gold is infinitely divisible (well, it's a `double`).

Three strategies are implemented: Go farming everyday, go working for gold every day, do what would have been the best strategy yesterday, and do what would have been the best strategy two days ago.

## Lattice Learner

The beginning of an idea I had for a recommendation system. At the moment it's just a semi-implementation of a lattice datastructure in Julia.

## Probability Genes

An attempt at a genetic representation of risk seeking and risk aversion. The idea is that the genes encode for a percentile and the individuals compare probability distrubutions by comparing the outcome at that percentile.

That means noone will compare two choices by their expected outcome.

## Space Noises

Toying a bit around with wavefile generation in Python. Will output two (ugly) tones, a chirp and a glitchy shepard tone.

## Water Distribution

The beginnings of the water management parts of a city builder like Sim City 4 or Cities Skylines. In this case water pressure and such is also supposed to be needed to be taken into account (sentences, man, they're hard). So you'll actually need water towers for their height in the beginning, or maybe you have a hilly area and can build a dam for a reservoir.

But now it just displays a random, very simple height map in green, with a cool, random-dissolution-gradient of blue on top.

## World of Warships Ships

How much XP do I need to get to unlock the next unlockable ships in World of Warships, a game I play a little bit twice a year.

## Better Chunksize (Python Multiprocessing.starmap improvement)

Created because I want to pass a list of chunksizes to starmap. The need arises from a problem with large per-process startup time, so the first process has time to process a significant part of it's workload before the second thread starts. The code here works if you pass the parameters correctly, but it'll fail if you do something wrong. Oh! The return values are gone in the void as well.

## City Distance

An attempt at simulating distances in time from an pre-modern city, inspired by [Bret Deveraux's ](https://acoup.blog/2019/07/19/the-lonely-city-part-ii-real-cities-have-curves/). Currently this simulated world is non-Euclidean since I'm using Manhattan distances.

## Falling Group with Springs

What happens if five 1 kg masses with compressed springs in between are dropped from some height with some initial lateral speed?

## Random Walk Probs

Recursively compute the probability of a random walk on $\mathbb{N} \union \left\{0\right\}$ being at number $k$ in generation $n$, with $k=0$ absorbing. Due to the stupid non-memoized recursive algorithm, this is $O\left(2^{n}\right)$!
