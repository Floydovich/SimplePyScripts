#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def search_empty_folders(disk):
    disk_letter = disk[0]
    file_name = 'log of {}.txt'.format(disk_letter)

    import time
    t = time.clock()
    print('  Start of ' + disk_letter)

    with open(file_name, mode='w', encoding='utf-8') as f:
        import os
        for root, dirs, files in os.walk(disk):
            # If dir is empty
            if not dirs and not files:
                f.write(root + '\n')

    print('  Finish "{}"! Elapsed time: {:.3f} secs'.format(disk_letter, time.clock() - t))


if __name__ == '__main__':
    import psutil
    disk_list = [disk.device for disk in psutil.disk_partitions() if 'fixed' in disk.opts]

    print('Start')

    import time
    t = time.clock()

    # Number of thread or process
    worker_number = len(disk_list)

    # If need use threads
    # from multiprocessing.dummy import Pool
    #
    # Or:
    from multiprocessing import Pool
    pool = Pool(worker_number)

    results = pool.map(search_empty_folders, disk_list)

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

    print('Finish! Elapsed time: {:.3f} secs'.format(time.clock() - t))
