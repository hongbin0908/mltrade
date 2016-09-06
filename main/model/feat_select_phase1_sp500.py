#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @author  Bin Hong

import os,sys
import multiprocessing

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..', '..')
sys.path.append(root)

from main.model import feat_select

if __name__ == '__main__':
    df = feat_select.phase1_dump("base1", "sp500")
    feat_select.ana_fmetas(df, "base1", "sp500")


