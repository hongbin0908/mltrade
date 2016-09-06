#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @author  Bin Hong

import os,sys
import multiprocessing



local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..', '..')
sys.path.append(root)



if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = int(10) )
    results = []
    for i in range(10):
        frm = 50  * i
        to  = frm + 50
        cmdstr = """
                  python main/model/feat_select.py sp500R%dT%d base1
                  """ % (frm, to)
        print cmdstr
        results.append(pool.apply_async(os.system, (cmdstr,)))
    for result in results:
        print result.get()

