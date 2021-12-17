#!/usr/bin/env python3
from logging import INFO
import multiprocessing as mp
import numpy as np
from time import sleep


def smart_starmap(f, args, chunksizes):
    args_tail = args
    with mp.Pool() as p:
        rezzes = []

        for zzz in chunksizes:
            this_chunk = args_tail[:zzz]
            args_tail = args_tail[zzz:]
            rez = p.starmap_async(f, this_chunk, chunksize=zzz)
            rezzes.append(rez)

        for rez in rezzes:
            rez.wait()


def _fun(ix, trash):
    sleep(np.mean(trash))
    loggy = mp.get_logger()
    loggy.info(f"Done with {ix}")

def main():
    biggy = np.ones((128, 128, 128, 64))

    loggy = mp.log_to_stderr(INFO)

    loggy.info("Starting threadpool")

    smart_starmap(_fun, [(x, biggy) for x in range(128)], [35, 33, 31, 29])
    pass

if __name__ == "__main__":
    main()
