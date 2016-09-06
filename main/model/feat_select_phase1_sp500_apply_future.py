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
    df = pd.read_pickle(os.path.join(dataroot,
                              "phase1_dump",
                              "sp500_base1_stable.pkl"))

    assert 68 == len(df[df.direct == 1])
    assert 83 == len(df[df.direct == -1])

    for i in range(10):
        frm = 50  * i
        to  = frm + 50
        setname = "sp500R%dT%d" % (frm, to)
        taname = "base1"
        (phase1, phase2, phase3) = \
            feat_select.split_dates(feat_select.load_feat(taname, setname))
        df2 = feat_select.apply(df,phase2, "label5", "_p2")
        df2 = feat_select.apply(df2,phase3, "label5", "_p3")

        fout = os.path.join(dataroot,
                            "feat_select_phase1_sp500_apply_future.ana")
        with open(fout, "w") as f:
            feat_select.ana2(df2, f)


