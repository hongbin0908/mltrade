#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#@author  Bin Hong

import sys,os
import json
import numpy as np
import pandas as pd
from sklearn.externals import joblib # to dump model

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..', '..')
sys.path.append(root)

import main.base as base
import main.ta as ta
from main.utils import time_me


def print_empty(df, fout):
    for each in df.iterrows():
        pred = each[1]["pred"]
        pred_dfTrue = each[1]["pred_dfTrue"]
        if np.isnan(pred_dfTrue):
            pre_dfTrue = 0
        pred_df2 = each[1]["pred_df2"];
        if np.isnan(pred_df2):
            pred_df2 = 0
        pred_df2True = each[1]["pred_df2True"]
        if np.isnan(pred_df2True):
            pred_df2True = 0
        if pred_df2 > 0:
            continue
        print >> fout,  "%s\t" % each[0],
        print >> fout, "%d\t" % pred,
        print >> fout, "%d\t" % pred_dfTrue,
        print >> fout, "%d\t" % pred_df2,
        print >> fout, "%d\t" % pred_df2True,
        print >> fout

def get_selected(dfTa, top, thresh):
    df = dfTa #pd.read_csv(infile)
    df['yyyy'] = df.date.str.slice(0,4)
    df["yyyyMM"] = df.date.str.slice(0,7)
    df2 = df[df.pred >= thresh].sort_values(["pred"], ascending=False).groupby('date').head(top)[["date", 'yyyy','yyyyMM',
        'sym', 'pred', 'label5']]
    return df2
def group_by_month(df, df2, level):
    dfTrue = df[df["label5"] > level]
    df2True = df2[df2["label5"] > level]
    return df.groupby('yyyyMM').count()\
          .join(dfTrue.groupby('yyyyMM').count(), rsuffix='_dfTrue')\
          .join(df2.groupby('yyyyMM').count(),rsuffix='_df2')\
          .join(df2True.groupby('yyyyMM').count(), rsuffix='_df2True')[['pred','pred_dfTrue', 'pred_df2','pred_df2True']]

def group_by_year(df, df2, level):
    dfTrue = df[df["label5"] > level]
    df2True = df2[df2["label5"] > level]
    re =  df.groupby('yyyy').count()\
          .join(dfTrue.groupby('yyyy').count(), rsuffix='_dfTrue')\
          .join(df2.groupby('yyyy').count(),rsuffix='_df2')\
          .join(df2True.groupby('yyyy').count(), rsuffix='_df2True')
    re = re[['pred','pred_dfTrue', 'pred_df2','pred_df2True']]
    re["rate1"] = re["pred_dfTrue"]*1.0/re["pred"]
    re["rate2"] = re["pred_df2True"]*1.0/re["pred_df2"]
    return re

def print_top_good_bad(df):
    print df[df["label5"] < 0.96].groupby('yyyy').head(1)
    print df[df["label5"] > 1.04].groupby('yyyy').head(1)

def accurate(df, level):
    return len(df[df["label5"] > level ]) * 1.0 /len(df)

@time_me
def main(argv):
    dfTa = argv[0]
    top = int(argv[1])
    thresh = float(argv[2])
    outfile = argv[3]
    level = argv[4]
    with open(outfile, "w") as fout:
        dfAll = dfTa #get_all(infile)
        dfAll['yyyy'] = dfAll.date.str.slice(0,4)
        dfAll["yyyyMM"] = dfAll.date.str.slice(0,7)
        dfSelected = get_selected(dfTa, top, thresh)
        print >> fout, "=" * 8 , "accurate", "=" * 8
        print >> fout, "%.3f\t%.3f" % (accurate(dfAll,level), accurate(dfSelected,level))

        dfMonth = group_by_month(dfAll, dfSelected,level)

        dfAll.groupby('sym').count

        print >> fout,  "=" * 8 , "detail", "=" * 8
        print_empty(dfMonth, fout)

        print >> fout,  "=" * 8, "view of years", "=" * 8
        print >> fout, group_by_year(dfAll, dfSelected, level)

        #
        print >> fout,  "="*8, "top good perfomance", '='*8
        print >> fout, dfSelected.sort_values(["pred"],ascending=False).groupby('yyyy').head(2).sort_values(['yyyy'])
        print >> fout, "="*8, "bad good perfomance", '='*8
        print >> fout, dfSelected.sort_values(["pred"],ascending=True).groupby('yyyy').head(2).sort_values(['yyyy'])
        print >> fout, "="*8, "all", "="*8
        pd.set_option('display.max_rows', len(dfSelected))
        print >> fout, dfSelected.sort_values(["yyyy","pred"], ascending=True)
        pd.reset_option('display.max_rows')



if __name__ == '__main__':
    main(sys.argv[1:])
