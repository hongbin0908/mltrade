from ..model import feat_select
import pandas as pd
def test_ana_fmetas():
    df = pd.DataFrame(data=[
        ["name1", "fname1",1,2,100,1,1.10,100],
        ["name2", "fname2",2,3,101,-1,0.90,100],
        ["name3", "fname3",1,2,99,1,1.20,100],
        ["name4", "fname4",1,2,99,-1,0.80,100],

    ],
    columns=["name", "fname", "start", "end", "score", "direct",
                "chvfa", "n_samples"]
    )

    feat_select.ana_fmetas(df)

    assert 0
