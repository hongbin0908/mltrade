#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @author  Bin Hong

"""
"""

import sys
import os
import numpy as np
import pandas as pd
import multiprocessing

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..', '..')
sys.path.append(root)

from main.utils import time_me

import main.yeod.yeod as yeod
import main.base as base
import main.ta.build as build
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree

dataroot = os.path.join(root, "data", "feat_select")


istest = False

def split_dates(df):
    """
    split df to [1980-2000], [2000-2010], [2010-2015]
    """
    phase1 = df[(df.date >= '1980-01-01') & (df.date < '2000-01-01')]
    phase2 = df[(df.date >= '2000-01-01') & (df.date < '2010-01-01')]
    phase3 = df[(df.date >= '2010-01-01') & (df.date < '2016-01-01')]
    return (phase1, phase2, phase3)

@time_me
def load_feat(taname, setname,start="",end=""):
    # get all the features
    dfTa = base.get_merged(taname,
                           getattr(yeod, "get_%s" % setname)(),start, end)
    dfTa = dfTa[dfTa.label5 != 1.0]
    return dfTa

def get_leaves(tree, min_, max_):
    def visit(tree, node_id, list_leaf, maximum):
        if tree.children_left[node_id] == _tree.TREE_LEAF:
            # current node is leaf node
            list_leaf.append((node_id, maximum))
        else:
            visit(tree, tree.children_left[node_id], list_leaf,
                  tree.threshold[node_id])
            visit(tree, tree.children_right[node_id], list_leaf,
                  maximum)
    list_leaf = []
    visit(tree.tree_, 0, list_leaf, np.inf)
    assert len(list_leaf) >= 2
    for i in range(len(list_leaf)):
        node_id, threshold = list_leaf[i]
        leaf = {}
        leaf["node_id"] = node_id
        leaf["impurity"] = tree.tree_.impurity[node_id]
        leaf["n_samples"] = tree.tree_.n_node_samples[node_id]
        leaf["value"] = tree.tree_.value[node_id][0]
        p1 = leaf["value"][0]/leaf["n_samples"]
        p2 = leaf["value"][1]/leaf["n_samples"]
        assert abs(leaf["impurity"] - (1- p1*p1 -p2*p2)) < 0.00001

        if i == 0:
            leaf["min"] = min_
        else:
            leaf["min"] = list_leaf[i-1]["max"]
        leaf["max"] = threshold
        if np.isinf(leaf["max"]):
            leaf["max"] = max_ + 0.0001 #
        list_leaf[i] = leaf
    return list_leaf

def delta_impurity(tree, leaves):
    root_impurity = tree.tree_.impurity[0]
    root_n_samples = tree.tree_.n_node_samples[0]
    delta = 0.0
    for leaf in leaves:
        delta += 1.0*leaf["n_samples"]/root_n_samples*leaf["impurity"]
    delta = root_impurity - delta
    return delta

def get_tree(depth):
    tree = DecisionTreeClassifier(min_samples_leaf=10000,
                                  min_samples_split=40000, max_depth=depth)
    return tree
def leaves_n_samples(leaves):
    n_samples = []
    for each in leaves:
        n_samples.append(each["n_samples"])
    return n_samples
def leaves_range(leaves):
    range_ = []
    for each in leaves:
        range_.append((each["min"], each["max"]))
    return range_

def leaves_p(leaves):
    p_ = []
    for each in leaves:
        p_.append(each["value"][1]/each["n_samples"])
        assert each["value"][0] + each["value"][1] == each["n_samples"]
    return p_

def feat_meta(feat, df, label, depth = 1):
    rlt = {}
    tree = get_tree(depth)
    npFeat = df[[feat]].values.copy()
    npLabel = df[label].values.copy()
    npLabel[npLabel > 1.0] = 1
    npLabel[npLabel < 1.0] = 0

    min_ = npFeat.min()
    max_ = npFeat.max()
    tree.fit(npFeat, npLabel)
    assert isinstance(tree.tree_, _tree.Tree)

    leaves = get_leaves(tree, min_, max_)
    rlt["splits"] = leaves
    rlt["name"] = feat
    rlt["p"] = 1.0 * len(df[df[label] > 1.0])/len(df)
    rlt["n"] = 1.0 * len(df[df[label] < 1.0])/len(df)
    rlt["delta_impurity"] = delta_impurity(tree, leaves)
    rlt["impurity"] = tree.tree_.impurity[0]
    p1 = 1.0*len(df[df[label]>1.0])/len(df)
    p2 = 1.0*len(df[df[label]<1.0])/len(df)
    assert abs(rlt["impurity"] - (1- p1*p1 -p2*p2)) < 0.0001
    rlt["range"] = leaves_range(leaves)
    rlt["children_p"] = leaves_p(leaves)
    rlt["children_n"] = [(1-each) for each in leaves_p(leaves)]
    rlt["p_chvfa"] = [each/rlt["p"] for each in rlt["children_p"]]
    rlt["n_chvfa"] = [each/rlt["n"] for each in rlt["children_n"]]
    rlt["n_samples"] =leaves_n_samples(leaves)

    for i in range(len(rlt["range"])):
        cur_range = rlt["range"][i]
        print feat, rlt["n_samples"][i],cur_range,len(df[(df[feat]>=cur_range[0])&(df[feat]<cur_range[1])])
        assert abs(rlt["n_samples"][i] - len(df[(df[feat]>=cur_range[0])&(df[feat]<cur_range[1])])) < 200
    return rlt


@time_me
def get_metas(dfTa, depth):
    #pool = multiprocessing.Pool(processes=20)
    feat_names = base.get_feat_names(dfTa)
    idx = 0
    results = []
    for cur_feat in feat_names:
        idx += 1
        if istest :
            if idx > 10:
                break
        #results.append(pool.apply_async(feat_meta, (cur_feat, dfTa, "label5")))
        results.append(feat_meta(cur_feat, dfTa, "label5", depth))
        print "%d done!" % idx
    return [result for result in results]

def flat_metas(metas, depth):
    fmetas = []
    for each in metas:
        for i, term in enumerate(each["range"]):
            d = {}
            d["fname"] = each["name"]
            d["name"] = "%s_d%d_%d" % (each["name"], depth, i)
            d["start"] = each["range"][i][0]
            d["end"] = each["range"][i][1]
            d["p_chvfa"] = each["p_chvfa"][i]
            d["n_chvfa"] = each["n_chvfa"][i]
            d["c_p"] = each["children_p"][i]
            d["c_n"] = each["children_n"][i]
            d["p"] = each["p"]
            d["n"] = each["n"]
            assert 1 == d["p"] + d["n"]
            d["score"] = each["delta_impurity"]
            d["n_samples"] = each["n_samples"][i]
            d["direct"] = 1 if d["p_chvfa"] > 1.01  else (-1 if d["n_chvfa"] > 1.01 else 0)
            fmetas.append(d)
    df = pd.DataFrame(fmetas)
    return df

@time_me
def ana_fmetas(df,taname, setname,f):
    head = df.sort_values(["score"], ascending=False).head(40)
    for i, each in head.iterrows():
        print >>f, "%s,%s,%s,%s,%d,%.4f,%.4f,%d" % (each["name"],each["fname"],
            each["start"],each["end"],
            each["direct"],each["p_chvfa"], each["n_chvfa"],
            each["n_samples"])

    max_score = head["score"].max()
    mean_score = df["score"].mean()

    max_p_rate = df["p_chvfa"].max()
    mean_p_rate = df[df.direct == 1]["p_chvfa"].mean()

    max_n_rate = df["n_chvfa"].max()
    mean_n_rate = df[df.direct == -1]["n_chvfa"].mean()

    direct_p_num =  len(df[df.direct == 1])
    direct_n_num =  len(df[df.direct == -1])
    direct_0_num =  len(df[df.direct == 0])



    print >> f, "delta_dis: |%s|%.8f|%.8f|%.4f|%.4f|%.4f|%.4f|" % (setname,
                                max_score, mean_score,
                                max_p_rate, mean_p_rate,
                                max_n_rate, mean_n_rate)
    assert len(df) == direct_p_num + direct_n_num + direct_0_num
    print >> f, "direct_dis: |%s|%d|%d|%d|%d|" % (setname,
                              len(df), direct_p_num, direct_n_num, direct_0_num)
@time_me
def apply(dfmetas, df, label, subfix):
    fp = len(df[df[label] > 1.0]) * 1.0 / len(df)
    fn = len(df[df[label] < 1.0]) * 1.0 / len(df)

    shadows = []
    for i, each in dfmetas.iterrows():
        d = {}
        d["name"] = each["name"]
        d["fname"] =  each["fname"]
        d["start"] = each["start"]
        d["end"] = each["end"]
        d["p"] = fp
        d["n"] = fn
        dfc = df[(df[d["fname"]]>=d["start"]) & (df[d["fname"]]<d["end"])]
        d["c_p"] = 0 if len(dfc) == 0 else len(dfc[dfc[label]>1.0]) * 1.0 / len(dfc)
        d["c_n"] = 0 if len(dfc) == 0 else len(dfc[dfc[label]<1.0]) * 1.0 / len(dfc)
        d["p_chvfa"] = d["c_p"]/d["p"]
        d["n_chvfa"] = d["c_n"]/d["n"]
        d["direct"] = 1 if d["p_chvfa"] > 1.01  else (-1 if d["n_chvfa"] > 1.01 else 0)
        d["n_samples"] = len(dfc)
        shadows.append(d)
    df2 = pd.DataFrame(shadows)
    return dfmetas.merge(df2, left_on=["name", "fname", "start", "end"],
                            right_on=["name", "fname", "start", "end"],
                            suffixes = ("",subfix))
def ana_apply(df, suffix, setname,f):
    df1 = df[df.direct == 1]
    rate1 = len(df1[df1["direct%s" % suffix] == 1]) * 1.0 / len(df1)

    df2 = df[df.direct == -1]
    rate2 = len(df2[df2["direct%s"% suffix] == -1]) * 1.0 / len(df2)

    print >> f, "|%s|%.4f|%.4f|" % (setname,rate1, rate2)

def ana2(df,f, setname):
    df1 = df[df.direct == 1]
    #for i, each in df1.iterrows():
    #    print >> f, each["name"], each["direct"], each["direct_p2"], each["direct_p3"]
    rate1_p2 = len(df1[df1.direct_p2 == 1])*1.0/len(df1)
    rate1_p3 = len(df1[df1.direct_p3 == 1])*1.0/len(df1)

    df2 = df[df.direct == -1]
    #for i, each in df2.iterrows():
    #    print >> f, each["name"], each["direct"], each["direct_p2"], each["direct_p3"]
    rate2_p2 = len(df2[df2.direct_p2 == -1]) * 1.0 / len(df2)
    rate2_p3 = len(df2[df2.direct_p3 == -1]) * 1.0 / len(df2)

    print >> f, "|%s|%.4f|%.4f|%.4f|%.4f|" % (setname, rate1_p2, rate1_p3, rate2_p2, rate2_p3)

def phase1_dump(taname, setname, depth):
    dfTa = load_feat(taname, setname)
    (phase1, phase2, phase3) = split_dates(dfTa)
    dfmetas = flat_metas(get_metas(phase1,depth),depth)
    outdir = os.path.join(root, "data", "feat_select", "phase1_dump")
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    dfmetas.to_pickle(os.path.join(outdir, "%s_%s_%d.pkl" % (setname, taname, depth)))
    return dfmetas

@time_me
def main(args):
    dfTa = load_feat(args.taname, args.setname)
    (phase1,phase2,phase3) = split_dates(dfTa)

    dfmetas = flat_metas(get_metas(phase1))
    outname = os.path.join(root, "data",
                           "feat_select",
                           "feat_select_%s_%s_%d" % (args.setname, args.taname,args.depth))
    if not os.path.exists(os.path.dirname(outname)):
        os.makedirs(os.path.dirname(outname))
    with open(outname, "w") as fout:
        ana_fmetas(dfmetas, fout, args)

    sys.exit(0)
    dfmetas = apply(dfmetas, phase2, "label5", "_p2")
    dfmetas = apply(dfmetas, phase3, "label5", "_p3")

    print dfmetas.head()

    outname = os.path.join(root, "data",
                           "feat_select",
                           "feat_select_ana2_%s_%s" % (args.setname, args.taname))
    with open(outname, "w") as fout:
        ana2(dfmetas, fout)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='No desc')

    #parser.add_argument('--start', dest='start',
    #                    action='store', default='1700-01-01')

    #parser.add_argument('--end',   dest='end',   action='store',
    #                    default='1999-12-31', help="model end time")

    #parser.add_argument('--label', dest='labelname', action='store',
    #                    default='label3', help="the label name")
    parser.add_argument('--depth', dest='depth', action='store',
                        default=1, type=int)
    parser.add_argument('setname', help="setname")
    parser.add_argument('taname', help="taname")

    args = parser.parse_args()
    main(args)
