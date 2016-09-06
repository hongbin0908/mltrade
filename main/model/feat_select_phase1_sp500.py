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
    # TODO check if file exsits
    # df = feat_select.phase1_dump("base1", "sp500")
    f = open(os.path.join(dataroot, "feat_select_phase1_sp500.ana"), "w")
    df = pd.read_pickle(os.path.join(dataroot,
                                     "phase1_dump",
                                     "sp500_base1.pkl"))
    feat_select.ana_fmetas(df, "base1", "sp500", f)

    abs_direct_p_set = set(df[df.direct == 1].name.unique())
    print >>f, "="*8
    for i in range(10):
        frm = 50  * i
        to  = frm + 50
        setname = "sp500R%dT%d" % (frm, to)
        taname = "base1"
        filename = os.path.join(dataroot,
                    "phase1_dump",
                    "sp500_base1_apply_phase1_%s_%s.pkl" % (setname, taname)
                   )
        if not os.path.exists(filename):
            df2 = feat_select.apply(df,
                    feat_select.split_dates(feat_select.load_feat(taname, setname))[0],
                    "label5", "_p1")

            df2.to_pickle(filename)
        df2 = pd.read_pickle(filename)
        cur_set = set(df2[df2.direct_p1 == 1].name.unique())
        abs_direct_p_set = abs_direct_p_set.intersection(cur_set)
        print len(abs_direct_p_set)

            #feat_select.ana_apply(df2,"_p1",f)
            #print >>f, "="*8
    f.close()
