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

#config
depth = 2
#end

if __name__ == '__main__':
    fphase1 = os.path.join(dataroot,
                                     "phase1_dump",
                                     "sp500_base1_%d.pkl" % depth)
    if not os.path.exists(fphase1):
        feat_select.phase1_dump("base1", "sp500",depth)
    df = pd.read_pickle(fphase1)

    f = open(os.path.join(dataroot, "feat_select_phase1_sp500_%d.ana" % depth), "w")
    feat_select.ana_fmetas(df, "base1", "sp500", f)

    abs_direct_p_set = set(df[df.direct == 1].name.unique())
    abs_direct_n_set = set(df[df.direct == -1].name.unique())

    orig_direct_p_set = abs_direct_p_set.copy()
    orig_direct_n_set = abs_direct_n_set.copy()
    print len(abs_direct_p_set)
    print len(abs_direct_n_set)
    print >>f, "="*8
    for i in range(10):
        frm = 50  * i
        to  = frm + 50
        setname = "sp500R%dT%d" % (frm, to)
        taname = "base1"
        filename = os.path.join(dataroot,
                    "phase1_dump",
                    "sp500_base1_apply_phase1_%s_%s_%d.pkl" % (setname, taname,depth)
                   )
        if not os.path.exists(filename):
            df2 = feat_select.apply(df,
                    feat_select.split_dates(feat_select.load_feat(taname, setname))[0],
                    "label5", "_p1")

            df2.to_pickle(filename)
        df2 = pd.read_pickle(filename)
        feat_select.ana_apply(df2, "_p1", setname, f)
        cur_p_set = set(df2[df2.direct_p1 == 1].name.unique())
        cur_n_set = set(df2[df2.direct_p1 == -1].name.unique())
        abs_direct_p_set = abs_direct_p_set.intersection(cur_p_set)
        abs_direct_n_set = abs_direct_n_set.intersection(cur_n_set)
        print list(abs_direct_n_set)
    df.loc[:,"istable"] = df.apply(lambda row: 1 if row["name"] in abs_direct_p_set else \
             (1 if row["name"] in abs_direct_n_set else 0), axis = 1)
    df.loc[:, "direct"] = df.apply(lambda row: 0 if row["istable"] == 0 else row["direct"], axis=1)
    df.to_pickle(os.path.join(dataroot,
                              "phase1_dump",
                              "sp500_base1_%d_stable.pkl" % depth))
    print "|%d|%d|%d|" % (len(orig_direct_p_set), len(abs_direct_p_set), len(orig_direct_p_set- abs_direct_p_set))
    print "|%d|%d|%d|" % (len(orig_direct_n_set), len(abs_direct_n_set), len(orig_direct_n_set- abs_direct_n_set))
    print >> f, "## stable feats on postive direct"
    for name in abs_direct_p_set:
        idx = 0
        for i, each in df[df.name == name].iterrows():
            print >>f, "|%s|%.4f|%.4f|" % (each["fname"],each["start"],each["end"])
            assert idx < 1
            idx += 1

    print >> f, "## UNstable feats on postive direct"
    for name in orig_direct_p_set - abs_direct_p_set:
        idx = 0
        for i, each in df[df.name == name].iterrows():
            print >>f, "|%s|%.4f|%.4f|" % (each["fname"],each["start"],each["end"])
            assert idx < 1
            idx += 1

    print >> f, "## stable feats on negtive direct"
    for name in abs_direct_n_set:
        idx = 0
        for i, each in df[df.name == name].iterrows():
            print >>f, "|%s|%.4f|%.4f|" % (each["fname"],each["start"],each["end"])
            assert idx < 1
            idx += 1

    print >> f, "## unstable feats on negtive direct"
    for name in orig_direct_n_set - abs_direct_n_set:
        idx = 0
        for i, each in df[df.name == name].iterrows():
            print >>f, "|%s|%.4f|%.4f|" % (each["fname"],each["start"],each["end"])
            assert idx < 1
            idx += 1

    f.close()
