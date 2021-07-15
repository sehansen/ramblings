#!/usr/bin/env python3

import functools

import scipy.stats

a = 100

l = [64, 32, 4]

assert(a == sum(l))

ll = [[32, 16, 8, 4, 2, 1, 1], [16, 8, 4, 2, 1, 1], [2, 1, 1]]

assert(all(x == sum(y) for x, y in zip(l, ll)))

assert(a == sum(functools.reduce(lambda x, y: x + y, ll)))

pl = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

print([x for x, y in zip(functools.reduce(lambda v, w: v + w, ll), pl)
       if y == 1])

print(sum(x
          for x, y in zip(functools.reduce(lambda v, w: v + w, ll), pl)
          if y == 1))


def chrom2prob(chrom):
    return sum(x
               for x, y
               in zip(functools.reduce(lambda v, w: v + w, ll), chrom)
               if y == 1)


print(chrom2prob(pl))

pl2 = [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0]
pl3 = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]

print(chrom2prob(pl2))
print(chrom2prob(pl3))

print((chrom2prob(pl) + chrom2prob(pl2)) / 2)

print(scipy.stats.gamma.ppf(0.1, 1))
print(scipy.stats.gamma.ppf(0.1, 2, scale=0.5))
print(scipy.stats.gamma.ppf(0.1, 3, scale=0.33333))


def cmg_ppf(shape):
    return lambda p: scipy.stats.gamma.ppf(p, shape, scale=(10/shape))


print(cmg_ppf(1)(0.1))
print(cmg_ppf(2)(0.1))
print(cmg_ppf(3)(0.1))

print(len(pl))


def genetic_attraction(a, b):
    score = 0
    for x, y in zip(a, b):
        if x == y:
            score += 1

    return abs(score - 10)


print(genetic_attraction(pl, pl2))
print(genetic_attraction(pl, pl3))
print(genetic_attraction(pl2, pl3))

dist_a = scipy.random.uniform(1, 3)
print(dist_a)
dist_b = scipy.random.uniform(1, 3)
print(dist_b)

for x in range(20):
    print(f"{(x+1)/21:4.2f}  ", end='')
    print(f"{cmg_ppf(dist_a)((x+1)/21):5.2f}  ", end='')
    print(f"{cmg_ppf(dist_b)((x+1)/21):5.2f}")


def pick(a, b, p):
    if cmg_ppf(a)(p/100) < cmg_ppf(b)(p/100):
        return "prefer B"
    else:
        return "prefer A"


print(pick(dist_a, dist_b, chrom2prob(pl3)))

random_chrom = scipy.random.binomial(1, 0.5, size=len(pl))
print(random_chrom)

population = [scipy.random.binomial(1, 0.5, size=len(pl)) for x in range(1000)]

a_count = 0
b_count = 0

for pop in population:
    preference = pick(dist_a, dist_b, chrom2prob(pop))
    if preference == "prefer A":
        a_count += 1
    elif preference == "prefer B":
        b_count += 1
    else:
        exit("Badness")

print(f"A count: {a_count}")
print(f"B count: {b_count}")

print("All OK")
