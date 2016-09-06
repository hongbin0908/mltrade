#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @author  Bin Hong

import os,sys
import pandas as pd

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..', '..')
sys.path.append(root)

from main.model import feat_select

dataroot = os.path.join(root, "data", "feat_select")

if __name__ == '__main__':
    # df = feat_select.phase1_dump("base1", "sp500")
    df = pd.read_pickle(os.path.join(dataroot,
                                     "phase1_dump",
                                     "sp500_base1.pkl"))
    feat_select.ana_fmetas(df, "base1", "sp500", sys.stdout)
        print >>f, "="*8
    for i in range(10):
        frm = 50  * i
        to  = frm + 50
        setname = "sp500R%dT%d" % (frm, to)
        taname = "base1"
        df2 = feat_select.apply(df,
                feat_select.split_dates(load_feat(setname, tanme))[0],
                "label5", "_p1")
        with open(sys.stdout, "w") as f:
            feat_select.ana2(df2,f)
            print >>f, "="*8
