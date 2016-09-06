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
    assert 68 == df[df.direct == 1]
    assert 83 == df[df.direct == -1]
