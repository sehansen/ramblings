# Ramblings

## Auction producers

A little simulated economy with a daily food for gold auction.

Each person needs 1 food per day to survive. The option is to farm, giving 5 food, or work, giving 1.0 gold. Food comes in units of 1, gold is infinitely divisible (well, it's a `double`).

Three strategies are implemented: Go farming everyday, go working for gold every day, do what would have been the best strategy yesterday, and do what would have been the best strategy two days ago.

## Lattice Learner

The beginning of an idea I had for a recommendation system. At the moment it's just a semi-implementation of a lattice datastructure in Julia.
